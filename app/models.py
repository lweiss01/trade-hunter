from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class MarketEvent:
    source: str
    platform: str
    market_id: str
    title: str
    event_kind: str = "quote"
    yes_price: float | None = None
    no_price: float | None = None
    volume: float | None = None
    volume_kind: str = "cumulative"
    trade_size: float | None = None
    trade_side: str | None = None
    liquidity: float | None = None
    live: bool = True
    topic: str | None = None
    market_url: str | None = None
    timestamp: datetime = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "platform": self.platform,
            "market_id": self.market_id,
            "title": self.title,
            "event_kind": self.event_kind,
            "yes_price": self.yes_price,
            "no_price": self.no_price,
            "volume": self.volume,
            "volume_kind": self.volume_kind,
            "trade_size": self.trade_size,
            "trade_side": self.trade_side,
            "liquidity": self.liquidity,
            "live": self.live,
            "topic": self.topic,
            "market_url": self.market_url,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class SpikeSignal:
    event: MarketEvent
    score: float
    volume_delta: float
    price_move: float
    baseline_volume_delta: float
    reason: str
    tier: str = "watch"
    topic: str | None = None
    source_label: str | None = None
    detected_at: datetime = field(default_factory=utc_now)
    # Enriched context fields for M002
    baseline_1h: float | None = None
    baseline_24h: float | None = None
    price_move_1m: float | None = None
    price_move_5m: float | None = None
    price_move_30m: float | None = None
    leading_events: list[MarketEvent] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event": self.event.to_dict(),
            "score": round(self.score, 3),
            "volume_delta": round(self.volume_delta, 3),
            "price_move": round(self.price_move, 4),
            "baseline_volume_delta": round(self.baseline_volume_delta, 3),
            "reason": self.reason,
            "tier": self.tier,
            "topic": self.topic,
            "source_label": self.source_label,
            "detected_at": self.detected_at.isoformat(),
            "baseline_1h": round(self.baseline_1h, 3) if self.baseline_1h is not None else None,
            "baseline_24h": round(self.baseline_24h, 3) if self.baseline_24h is not None else None,
            "price_move_1m": round(self.price_move_1m, 4) if self.price_move_1m is not None else None,
            "price_move_5m": round(self.price_move_5m, 4) if self.price_move_5m is not None else None,
            "price_move_30m": round(self.price_move_30m, 4) if self.price_move_30m is not None else None,
            "leading_events": [e.to_dict() for e in self.leading_events],
        }
