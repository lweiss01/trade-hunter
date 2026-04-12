from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta

from .config import Settings
from .models import MarketEvent, SpikeSignal


@dataclass
class MarketWindow:
    last_event: MarketEvent | None = None
    volume_deltas: deque[float] | None = None
    last_signal_at: datetime | None = None
    event_history: deque[MarketEvent] | None = None  # For M002 enriched context
    whale_history: deque[MarketEvent] | None = None

    def __post_init__(self) -> None:
        if self.volume_deltas is None:
            self.volume_deltas = deque()
        if self.event_history is None:
            self.event_history = deque(maxlen=100)  # Keep last 100 events
        if self.whale_history is None:
            self.whale_history = deque()


class SpikeDetector:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.windows: dict[str, MarketWindow] = defaultdict(MarketWindow)

    def process(self, event: MarketEvent, baselines: dict[str, float] | None = None) -> SpikeSignal | None:
        window = self.windows[event.market_id]
        previous = window.last_event

        volume_delta = self._volume_delta(event, previous)
        price_move = self._price_move(event, previous)
        baseline = self._baseline(window)

        should_alert = self._should_alert(
            window=window,
            event=event,
            volume_delta=volume_delta,
            price_move=price_move,
            baseline=baseline,
        )

        is_whale_cluster = False
        p_value = 1.0
        eff_lam = 0.0
        if baselines and event.event_kind == "trade" and event.trade_size is not None:
            p99 = baselines.get("percentile_99", 200.0)
            lam = baselines.get("lambda_120s", 0.0)
            
            pr = event.yes_price if event.yes_price is not None else 1.0
            notional = float(event.trade_size) * pr
            
            if notional >= p99:
                window.whale_history.append(event)
                
                cutoff = event.timestamp - timedelta(seconds=120)
                while window.whale_history and window.whale_history[0].timestamp < cutoff:
                    window.whale_history.popleft()
                
                k = len(window.whale_history)
                if k >= 3:
                    import math
                    eff_lam = max(lam, 0.001)
                    prob_less_than_k = 0.0
                    for i in range(k):
                        prob_less_than_k += math.exp(-eff_lam) * (eff_lam**i) / math.factorial(i)
                    p_value = 1.0 - prob_less_than_k
                    
                    if p_value < 0.01:
                        is_whale_cluster = True


        if volume_delta > 0:
            window.volume_deltas.append(volume_delta)
            while len(window.volume_deltas) > self.settings.spike_baseline_points:
                window.volume_deltas.popleft()

        # Track event history for M002 enriched context
        window.event_history.append(event)
        window.last_event = event

        if not should_alert and not is_whale_cluster:
            return None

        if is_whale_cluster:
            score = max(self._score(volume_delta, price_move, baseline), 8.0)
            tier = "whale-cluster"
            topic = self._topic(event)
            reason = f"whale-cluster: {len(window.whale_history)} whales in 120s (p={p_value:.4f}, λ={eff_lam:.3f})"
        else:
            score = self._score(volume_delta, price_move, baseline)
            tier = self._tier(event, score, volume_delta, price_move, baseline)
            topic = self._topic(event)
            reason = (
                f"{tier}: volume +{volume_delta:.0f} vs baseline {baseline:.0f}, "
                f"price move {price_move:.1%}, score {score:.2f}"
            )
        
        # M002: Calculate enriched context fields
        baseline_1h, baseline_24h = self._multi_window_baselines(window)
        price_move_1m, price_move_5m, price_move_30m = self._multi_window_price_moves(window, event)
        leading_events = self._get_leading_events(window, event)
        
        window.last_signal_at = event.timestamp
        return SpikeSignal(
            event=event,
            score=score,
            volume_delta=volume_delta,
            price_move=price_move,
            baseline_volume_delta=baseline,
            reason=reason,
            tier=tier,
            topic=topic,
            source_label=event.source,
            baseline_1h=baseline_1h,
            baseline_24h=baseline_24h,
            price_move_1m=price_move_1m,
            price_move_5m=price_move_5m,
            price_move_30m=price_move_30m,
            leading_events=leading_events,
        )

    def _volume_delta(self, event: MarketEvent, previous: MarketEvent | None) -> float:
        if event.volume is None:
            return 0.0
        if event.volume_kind == "delta":
            return max(float(event.volume), 0.0)
        if previous is None or previous.volume is None:
            return 0.0
        return max(float(event.volume) - float(previous.volume), 0.0)

    def _price_move(self, event: MarketEvent, previous: MarketEvent | None) -> float:
        if previous is None or previous.yes_price is None or event.yes_price is None:
            return 0.0
        return abs(float(event.yes_price) - float(previous.yes_price))

    def _baseline(self, window: MarketWindow) -> float:
        deltas = list(window.volume_deltas or [])
        if not deltas:
            return self.settings.spike_min_volume_delta / 2
        return max(sum(deltas) / len(deltas), 1.0)

    def _score(self, volume_delta: float, price_move: float, baseline: float) -> float:
        volume_score = volume_delta / max(baseline, 1.0)
        price_score = price_move / max(self.settings.spike_min_price_move, 0.01)
        return (volume_score * 0.75) + (price_score * 1.25)

    def _tier(
        self,
        event: MarketEvent,
        score: float,
        volume_delta: float,
        price_move: float,
        baseline: float,
    ) -> str:
        if event.metadata.get("cross_venue"):
            return "cross-venue divergence"

        volume_multiple = volume_delta / max(baseline, 1.0)
        notable_min_price_move = 0.005
        if (
            score >= 6.0
            and price_move >= (self.settings.spike_min_price_move * 1.75)
            and volume_multiple >= 3.0
        ):
            return "signal"
        if price_move >= notable_min_price_move and (
            score >= 4.0 or (
                price_move >= (self.settings.spike_min_price_move * 1.2)
                and volume_multiple >= 2.4
            )
        ):
            directional_bias = self._directional_trade_bias(self.windows[event.market_id])
            if price_move < 0.01 and directional_bias is not None and directional_bias <= 0.60:
                return "watch"
            return "notable"
        return "watch"

    def _topic(self, event: MarketEvent) -> str:
        if event.topic:
            return event.topic

        haystack = f"{event.title} {event.market_id}".lower()
        keyword_map = {
            "crypto": ("btc", "bitcoin", "eth", "ethereum", "sol", "crypto"),
            "elections": (
                "election",
                "vote",
                "president",
                "senate",
                "house",
                "republican",
                "democrat",
                "trump",
                "biden",
            ),
            "macro": ("fed", "inflation", "cpi", "rate", "gdp", "jobs", "tariff", "recession"),
            "sports": ("nba", "nfl", "mlb", "nhl", "soccer", "tennis", "ufc", "march madness"),
            "geopolitics": ("china", "russia", "ukraine", "israel", "iran", "war", "nato"),
        }
        for topic, keywords in keyword_map.items():
            if any(keyword in haystack for keyword in keywords):
                return topic
        return "general"

    def _should_alert(
        self,
        *,
        window: MarketWindow,
        event: MarketEvent,
        volume_delta: float,
        price_move: float,
        baseline: float,
    ) -> bool:
        if volume_delta <= 0:
            return False

        if window.last_signal_at is not None:
            age_seconds = (event.timestamp - window.last_signal_at).total_seconds()
            if age_seconds < self.settings.spike_cooldown_seconds:
                return False

        score = self._score(volume_delta, price_move, baseline)
        hard_move = (
            volume_delta >= self.settings.spike_min_volume_delta
            and price_move >= self.settings.spike_min_price_move
        )
        outlier_move = (
            volume_delta >= baseline * 2.2
            and score >= self.settings.spike_score_threshold
        )
        if not (hard_move or outlier_move):
            return False

        if not self._ultra_thin_market_ok(window, event, volume_delta, baseline):
            return False

        if not self._trade_flow_is_coherent(window, event):
            return False

        required_move = self._required_price_move(event)
        if price_move >= required_move:
            return True

        directional_bias = self._directional_trade_bias(window)
        if directional_bias is None:
            return (
                required_move <= 0.01
                and self._normalized_directional_side(event.trade_side) is not None
                and event.event_kind == "trade"
            )

        return directional_bias > 0.60
    
    def _multi_window_baselines(self, window: MarketWindow) -> tuple[float | None, float | None]:
        """Calculate 1-hour and 24-hour volume baselines from real event timestamps."""
        if not window.event_history or len(window.event_history) < 3:
            return None, None

        history = list(window.event_history)
        prior_history = history[:-1]
        now = history[-1].timestamp

        def avg_delta_since(duration: timedelta) -> float | None:
            cutoff = now - duration
            deltas: list[float] = []
            for previous, current in zip(prior_history, prior_history[1:]):
                if current.timestamp < cutoff:
                    continue
                delta = self._volume_delta(current, previous)
                if delta > 0:
                    deltas.append(delta)
            if not deltas:
                return None
            return sum(deltas) / len(deltas)

        return avg_delta_since(timedelta(hours=1)), avg_delta_since(timedelta(hours=24))

    def _multi_window_price_moves(self, window: MarketWindow, current_event: MarketEvent) -> tuple[float | None, float | None, float | None]:
        """Calculate price moves over real 1-minute, 5-minute, and 30-minute windows."""
        if not window.event_history or len(window.event_history) < 2:
            return None, None, None

        if current_event.yes_price is None:
            return None, None, None

        history = list(window.event_history)
        prior_history = history[:-1]

        def price_move_since(duration: timedelta) -> float | None:
            cutoff = current_event.timestamp - duration
            for event in prior_history:
                if event.timestamp >= cutoff and event.yes_price is not None:
                    return abs(current_event.yes_price - event.yes_price)
            return None

        return (
            price_move_since(timedelta(minutes=1)),
            price_move_since(timedelta(minutes=5)),
            price_move_since(timedelta(minutes=30)),
        )

    def _get_leading_events(self, window: MarketWindow, current_event: MarketEvent) -> list[MarketEvent]:
        """Get last 5 events before the current spike event."""
        if not window.event_history:
            return []

        history = list(window.event_history)

        # Get last 5 events before current (current is already in history at -1)
        # So get events from -6 to -2 (5 events)
        if len(history) >= 6:
            return history[-6:-1]
        if len(history) >= 2:
            return history[:-1]  # All except current
        return []

    def _directional_trade_bias(self, window: MarketWindow, limit: int = 12) -> float | None:
        """Return dominant recent trade-side share for yes/buy vs no/sell trades.

        Uses recent same-market trade history only. Returns None when there is not
        enough directional trade data to make a coherence decision.
        """
        directional = self._recent_directional_trades(window, limit=limit)
        total = len(directional)
        if total < 3:
            return None

        yes_count = sum(1 for side in directional if side == "yes")
        no_count = total - yes_count
        return max(yes_count, no_count) / total

    def _recent_directional_trades(self, window: MarketWindow, limit: int = 12) -> list[str]:
        if not window.event_history:
            return []

        directional: list[str] = []
        for event in reversed(window.event_history):
            if event.event_kind != "trade":
                continue
            side = self._normalized_directional_side(event.trade_side)
            if side is not None:
                directional.append(side)
            if len(directional) >= limit:
                break
        return directional

    def _recent_trade_count(self, window: MarketWindow, limit: int = 12) -> int:
        if not window.event_history:
            return 0
        count = 0
        for event in reversed(window.event_history):
            if event.event_kind == "trade":
                count += 1
            if count >= limit:
                break
        return count

    def _dominant_directional_side(self, window: MarketWindow, limit: int = 12) -> str | None:
        directional = self._recent_directional_trades(window, limit=limit)
        total = len(directional)
        if total < 3:
            return None

        yes_count = sum(1 for side in directional if side == "yes")
        no_count = total - yes_count
        dominant = "yes" if yes_count >= no_count else "no"
        share = max(yes_count, no_count) / total
        return dominant if share > 0.60 else None

    def _required_price_move(self, event: MarketEvent) -> float:
        required = 0.01
        if event.yes_price is not None and event.yes_price <= 0.01:
            required = max(required, 0.02)
        if event.liquidity is not None and event.liquidity <= 1000:
            required = max(required, 0.02)
        return required

    def _ultra_thin_market_ok(
        self,
        window: MarketWindow,
        event: MarketEvent,
        volume_delta: float,
        baseline: float,
    ) -> bool:
        volume_multiple = volume_delta / max(baseline, 1.0)
        ultra_low_price = event.yes_price is not None and event.yes_price <= 0.01
        ultra_thin = volume_delta < 500 or ultra_low_price
        if not ultra_thin:
            return True

        current_trade = 1 if event.event_kind == "trade" else 0
        executed_trades = self._recent_trade_count(window) + current_trade
        return volume_multiple >= 100 or executed_trades > 0

    def _trade_flow_is_coherent(self, window: MarketWindow, event: MarketEvent) -> bool:
        previous = window.last_event
        if previous is None or previous.yes_price is None or event.yes_price is None:
            return True

        delta = float(event.yes_price) - float(previous.yes_price)
        current_side = self._normalized_directional_side(event.trade_side)
        if current_side == "yes" and delta < 0:
            return False
        if current_side == "no" and delta > 0:
            return False

        dominant_side = self._dominant_directional_side(window)
        if dominant_side == "yes" and delta < 0:
            return False
        if dominant_side == "no" and delta > 0:
            return False
        return True

    def _normalized_directional_side(self, trade_side: str | None) -> str | None:
        side = str(trade_side or "").strip().lower()
        if side in {"yes", "buy"}:
            return "yes"
        if side in {"no", "sell"}:
            return "no"
        return None
