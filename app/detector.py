from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime

from .config import Settings
from .models import MarketEvent, SpikeSignal


@dataclass
class MarketWindow:
    last_event: MarketEvent | None = None
    volume_deltas: deque[float] | None = None
    last_signal_at: datetime | None = None
    event_history: deque[MarketEvent] | None = None  # For M002 enriched context

    def __post_init__(self) -> None:
        if self.volume_deltas is None:
            self.volume_deltas = deque()
        if self.event_history is None:
            self.event_history = deque(maxlen=100)  # Keep last 100 events


class SpikeDetector:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.windows: dict[str, MarketWindow] = defaultdict(MarketWindow)

    def process(self, event: MarketEvent) -> SpikeSignal | None:
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

        if volume_delta > 0:
            window.volume_deltas.append(volume_delta)
            while len(window.volume_deltas) > self.settings.spike_baseline_points:
                window.volume_deltas.popleft()

        # Track event history for M002 enriched context
        window.event_history.append(event)
        window.last_event = event

        if not should_alert:
            return None

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
        if (
            score >= 6.0
            and price_move >= (self.settings.spike_min_price_move * 1.75)
            and volume_multiple >= 3.0
        ):
            return "high conviction flow"
        if score >= 4.0 or (
            price_move >= (self.settings.spike_min_price_move * 1.2)
            and volume_multiple >= 2.4
        ):
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
        return hard_move or outlier_move
    
    def _multi_window_baselines(self, window: MarketWindow) -> tuple[float | None, float | None]:
        """Calculate 1-hour and 24-hour volume baselines from event history."""
        if not window.event_history or len(window.event_history) < 2:
            return None, None
        
        # For MVP, use event count as proxy for time windows
        # 1h baseline: last ~6 events (assuming 10min cadence)
        # 24h baseline: last ~24 events (current spike_baseline_points)
        
        history = list(window.event_history)
        
        # Calculate 1h baseline (last 6 events)
        baseline_1h = None
        if len(history) >= 6:
            recent_deltas = []
            for i in range(1, min(7, len(history))):
                prev_event = history[-(i+1)]
                curr_event = history[-i]
                delta = self._volume_delta(curr_event, prev_event)
                if delta > 0:
                    recent_deltas.append(delta)
            if recent_deltas:
                baseline_1h = sum(recent_deltas) / len(recent_deltas)
        
        # Calculate 24h baseline (last 24 events or all available)
        baseline_24h = None
        if len(history) >= 3:
            all_deltas = []
            for i in range(1, min(25, len(history))):
                prev_event = history[-(i+1)]
                curr_event = history[-i]
                delta = self._volume_delta(curr_event, prev_event)
                if delta > 0:
                    all_deltas.append(delta)
            if all_deltas:
                baseline_24h = sum(all_deltas) / len(all_deltas)
        
        return baseline_1h, baseline_24h
    
    def _multi_window_price_moves(self, window: MarketWindow, current_event: MarketEvent) -> tuple[float | None, float | None, float | None]:
        """Calculate price moves over 1-minute, 5-minute, and 30-minute windows."""
        if not window.event_history or len(window.event_history) < 2:
            return None, None, None
        
        if current_event.yes_price is None:
            return None, None, None
        
        history = list(window.event_history)
        
        # For MVP, use event count as proxy for time windows
        # 1m: last 1-2 events
        # 5m: last 3-5 events
        # 30m: last 10-15 events
        
        price_move_1m = None
        if len(history) >= 2:
            prev_event = history[-2]
            if prev_event.yes_price is not None:
                price_move_1m = abs(current_event.yes_price - prev_event.yes_price)
        
        price_move_5m = None
        if len(history) >= 5:
            prev_event = history[-5]
            if prev_event.yes_price is not None:
                price_move_5m = abs(current_event.yes_price - prev_event.yes_price)
        
        price_move_30m = None
        if len(history) >= 15:
            prev_event = history[-15]
            if prev_event.yes_price is not None:
                price_move_30m = abs(current_event.yes_price - prev_event.yes_price)
        
        return price_move_1m, price_move_5m, price_move_30m
    
    def _get_leading_events(self, window: MarketWindow, current_event: MarketEvent) -> list[MarketEvent]:
        """Get last 5 events before the current spike event."""
        if not window.event_history:
            return []
        
        history = list(window.event_history)
        
        # Get last 5 events before current (current is already in history at -1)
        # So get events from -6 to -2 (5 events)
        if len(history) >= 6:
            return history[-6:-1]
        elif len(history) >= 2:
            return history[:-1]  # All except current
        else:
            return []
