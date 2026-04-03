"""Tests for M002 signal enrichment features."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from app.analyst import MAX_SIGNAL_ANALYST_CACHE, SignalAnalyst, _build_prompt
from app.config import Settings
from app.detector import SpikeDetector
from app.models import MarketEvent


def make_settings(**overrides) -> Settings:
    """Create test Settings with minimal required fields."""
    defaults = {
        "host": "127.0.0.1",
        "port": 8765,
        "enable_simulation": False,
        "enable_kalshi": False,
        "discord_webhook_url": None,
        "discord_webhook_routes": {},
        "ingest_api_token": None,
        "polyalerthub_token": None,
        "spike_min_volume_delta": 500.0,
        "spike_min_price_move": 0.05,
        "spike_score_threshold": 3.0,
        "spike_baseline_points": 24,
        "spike_cooldown_seconds": 300,
        "retention_days": 7,
        "kalshi_markets": [],
        "kalshi_api_key_id": None,
        "kalshi_private_key_path": None,
    }
    defaults.update(overrides)
    return Settings(**defaults)


def test_signal_has_enriched_baseline_fields():
    """Verify signals include baseline_1h and baseline_24h fields."""
    settings = make_settings(
        spike_min_volume_delta=100,
        spike_min_price_move=0.03,
    )
    detector = SpikeDetector(settings)

    base_time = datetime.now(UTC)

    # Add 10 events with small deltas to establish baseline.
    for i in range(10):
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="test-market",
            title="Test Market",
            yes_price=0.50 + (i * 0.001),
            volume=1000 + (i * 50),
            volume_kind="cumulative",
            timestamp=base_time + timedelta(minutes=i * 5),
        )
        detector.process(event)

    spike_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="test-market",
        title="Test Market",
        yes_price=0.60,
        volume=3000,
        volume_kind="cumulative",
        timestamp=base_time + timedelta(minutes=55),
    )
    signal = detector.process(spike_event)

    assert signal is not None
    assert signal.baseline_1h is not None
    assert signal.baseline_24h is not None
    assert signal.baseline_1h > 0
    assert signal.baseline_24h > 0


def test_signal_has_enriched_price_move_fields():
    """Verify signals include price_move_1m, 5m, 30m fields when enough time-based history exists."""
    settings = make_settings(
        spike_min_volume_delta=100,
        spike_min_price_move=0.03,
    )
    detector = SpikeDetector(settings)

    base_time = datetime.now(UTC)

    for i in range(20):
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="test-market",
            title="Test Market",
            yes_price=0.40 + (i * 0.01),
            volume=1000 + (i * 50),
            volume_kind="cumulative",
            timestamp=base_time - timedelta(minutes=40 - (i * 2)),
        )
        detector.process(event)

    spike_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="test-market",
        title="Test Market",
        yes_price=0.70,
        volume=5000,
        volume_kind="cumulative",
        timestamp=base_time + timedelta(minutes=2),
    )
    signal = detector.process(spike_event)

    assert signal is not None
    assert signal.price_move_1m is None
    assert signal.price_move_5m is not None
    assert signal.price_move_30m is not None
    assert signal.price_move_30m >= signal.price_move_5m


def test_signal_has_leading_events():
    """Verify signals include leading_events (last 5 before spike)."""
    settings = make_settings(
        spike_min_volume_delta=100,
        spike_min_price_move=0.03,
    )
    detector = SpikeDetector(settings)

    base_time = datetime.now(UTC)

    for i in range(8):
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="test-market",
            title="Test Market",
            yes_price=0.50,
            volume=1000 + (i * 50),
            volume_kind="cumulative",
            timestamp=base_time + timedelta(seconds=i * 10),
        )
        detector.process(event)

    spike_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="test-market",
        title="Test Market",
        yes_price=0.60,
        volume=3000,
        volume_kind="cumulative",
        timestamp=base_time + timedelta(seconds=80),
    )
    signal = detector.process(spike_event)

    assert signal is not None
    assert isinstance(signal.leading_events, list)
    assert len(signal.leading_events) == 5
    assert all(e.volume < 3000 for e in signal.leading_events)


def test_signal_to_dict_includes_enriched_fields():
    """Verify signal.to_dict() includes all enriched fields."""
    settings = make_settings(
        spike_min_volume_delta=100,
        spike_min_price_move=0.03,
    )
    detector = SpikeDetector(settings)

    base_time = datetime.now(UTC)

    for i in range(10):
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="test-market",
            title="Test Market",
            yes_price=0.50 + (i * 0.01),
            volume=1000 + (i * 50),
            volume_kind="cumulative",
            timestamp=base_time + timedelta(minutes=i * 3),
        )
        detector.process(event)

    spike_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="test-market",
        title="Test Market",
        yes_price=0.65,
        volume=3000,
        volume_kind="cumulative",
        timestamp=base_time + timedelta(minutes=31),
    )
    signal = detector.process(spike_event)

    assert signal is not None
    signal_dict = signal.to_dict()

    assert "baseline_1h" in signal_dict
    assert "baseline_24h" in signal_dict
    assert "price_move_1m" in signal_dict
    assert "price_move_5m" in signal_dict
    assert "price_move_30m" in signal_dict
    assert "leading_events" in signal_dict
    assert isinstance(signal_dict["leading_events"], list)
    if signal_dict["leading_events"]:
        assert isinstance(signal_dict["leading_events"][0], dict)
        assert "market_id" in signal_dict["leading_events"][0]


def test_enriched_baselines_calculation():
    """Verify multi-window baseline calculations are correct with real time windows."""
    settings = make_settings(spike_baseline_points=24)
    detector = SpikeDetector(settings)

    base_time = datetime.now(UTC)

    # Older events fall outside the 1h window but inside the 24h window.
    volume = 1000
    for minutes_ago, delta in [
        (180, 100),
        (170, 100),
        (160, 100),
        (50, 200),
        (40, 200),
        (30, 50),
        (20, 50),
        (10, 50),
    ]:
        volume += delta
        detector.process(
            MarketEvent(
                source="test",
                platform="polymarket",
                market_id="test-market",
                title="Test",
                yes_price=0.50,
                volume=volume,
                volume_kind="cumulative",
                timestamp=base_time - timedelta(minutes=minutes_ago),
            )
        )

    spike_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="test-market",
        title="Test",
        yes_price=0.60,
        volume=volume + 2000,
        volume_kind="cumulative",
        timestamp=base_time,
    )
    signal = detector.process(spike_event)

    assert signal is not None
    assert signal.baseline_1h == pytest.approx(110.0, abs=0.01)
    assert signal.baseline_24h == pytest.approx(107.143, abs=0.01)


def test_enriched_price_moves_use_real_time_windows():
    """Verify multi-window price moves are based on elapsed time, not event count."""
    settings = make_settings(
        spike_min_volume_delta=1000,
        spike_min_price_move=0.03,
        spike_score_threshold=10.0,
    )
    detector = SpikeDetector(settings)

    base_time = datetime.now(UTC)

    events = [
        (base_time - timedelta(minutes=40), 0.40, 1000),
        (base_time - timedelta(minutes=10), 0.50, 1100),
        (base_time - timedelta(minutes=4), 0.60, 1200),
        (base_time - timedelta(seconds=30), 0.70, 1300),
    ]
    for timestamp, price, volume in events:
        detector.process(
            MarketEvent(
                source="test",
                platform="polymarket",
                market_id="test-market",
                title="Test",
                yes_price=price,
                volume=volume,
                volume_kind="cumulative",
                timestamp=timestamp,
            )
        )

    spike_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="test-market",
        title="Test",
        yes_price=0.85,
        volume=5000,
        volume_kind="cumulative",
        timestamp=base_time,
    )
    signal = detector.process(spike_event)

    assert signal is not None
    assert signal.price_move_1m == pytest.approx(0.15, abs=0.001)
    assert signal.price_move_5m == pytest.approx(0.25, abs=0.001)
    assert signal.price_move_30m == pytest.approx(0.35, abs=0.001)


def test_enriched_fields_handle_sparse_real_time_history():
    """Verify sparse history still yields partial enriched context when appropriate."""
    settings = make_settings(
        spike_min_volume_delta=500,
        spike_min_price_move=0.05,
        spike_score_threshold=2.0,
    )
    detector = SpikeDetector(settings)

    base_time = datetime.now(UTC)

    for minutes_ago, price, volume in [
        (120, 0.45, 1000),
        (30, 0.50, 1100),
        (2, 0.55, 1200),
    ]:
        detector.process(
            MarketEvent(
                source="test",
                platform="polymarket",
                market_id="test-market",
                title="Test",
                yes_price=price,
                volume=volume,
                volume_kind="cumulative",
                timestamp=base_time - timedelta(minutes=minutes_ago),
            )
        )

    spike_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="test-market",
        title="Test",
        yes_price=0.70,
        volume=10000,
        volume_kind="delta",
        timestamp=base_time,
    )
    signal = detector.process(spike_event)

    assert signal is not None
    assert signal.baseline_24h is not None or signal.baseline_1h is not None
    assert signal.price_move_1m is None
    assert signal.price_move_5m == pytest.approx(0.15, abs=0.001)
    assert signal.price_move_30m == pytest.approx(0.20, abs=0.001)
    assert len(signal.leading_events) >= 2


def test_enriched_fields_serialization():
    """Verify enriched fields serialize correctly to JSON."""
    settings = make_settings(
        spike_min_volume_delta=100,
        spike_min_price_move=0.03,
    )
    detector = SpikeDetector(settings)

    base_time = datetime.now(UTC)

    for i in range(10):
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="test-market",
            title="Test",
            yes_price=0.50 + (i * 0.01),
            volume=1000 + (i * 50),
            volume_kind="cumulative",
            timestamp=base_time + timedelta(minutes=i * 4),
        )
        detector.process(event)

    spike_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="test-market",
        title="Test",
        yes_price=0.65,
        volume=3000,
        volume_kind="cumulative",
        timestamp=base_time + timedelta(minutes=41),
    )
    signal = detector.process(spike_event)

    assert signal is not None

    import json

    signal_dict = signal.to_dict()
    json_str = json.dumps(signal_dict)

    parsed = json.loads(json_str)
    assert "baseline_1h" in parsed
    assert "leading_events" in parsed
    assert isinstance(parsed["leading_events"], list)
def test_analyst_prompt_includes_enriched_context():
    """Verify analyst prompt uses enriched detector context instead of discarding it."""
    signal = {
        "event": {
            "market_id": "test-market",
            "title": "Will BTC finish green?",
            "yes_price": 0.61,
        },
        "volume_delta": 1500.0,
        "baseline_volume_delta": 300.0,
        "price_move": 0.04,
        "score": 5.2,
        "tier": "notable",
        "reason": "notable: volume +1500 vs baseline 300, price move 4.0%, score 5.2",
        "baseline_1h": 275.0,
        "baseline_24h": 180.0,
        "price_move_1m": 0.01,
        "price_move_5m": 0.03,
        "price_move_30m": 0.08,
        "leading_events": [
            {
                "event_kind": "trade",
                "timestamp": "2026-04-03T16:55:00+00:00",
                "yes_price": 0.58,
                "volume": 120.0,
                "trade_side": "yes",
            },
            {
                "event_kind": "quote",
                "timestamp": "2026-04-03T16:56:00+00:00",
                "yes_price": 0.60,
                "volume": 450.0,
                "trade_side": None,
            },
        ],
    }
    recent_flow = [
        {"market_id": "test-market", "yes_price": 0.58, "event_kind": "trade", "trade_side": "yes"},
        {"market_id": "test-market", "yes_price": 0.60, "event_kind": "trade", "trade_side": "no"},
        {"market_id": "other-market", "yes_price": 0.20, "event_kind": "quote", "trade_side": None},
    ]

    prompt = _build_prompt(signal, recent_flow)

    assert "ENRICHED DETECTOR CONTEXT" in prompt
    assert "1h baseline delta: 275" in prompt
    assert "24h baseline delta: 180" in prompt
    assert "Price moves: 1m=1.0%, 5m=3.0%, 30m=8.0%" in prompt
    assert "Leading events before spike:" in prompt
    assert "trade @ 2026-04-03T16:55:00+00:00" in prompt
    assert "quote @ 2026-04-03T16:56:00+00:00" in prompt


def test_signal_analyst_cache_is_bounded_lru():
    """Verify analyst cache evicts least-recently-used entries when over capacity."""
    analyst = SignalAnalyst()

    analyst._remember_result("sig-1@a", {"value": 1})
    analyst._remember_result("sig-2@b", {"value": 2})
    analyst._remember_result("sig-3@c", {"value": 3})

    # Touch sig-1 so sig-2 becomes the least recently used entry.
    assert analyst.get({"event": {"market_id": "sig-1"}, "detected_at": "a"}) == {"value": 1}

    for idx in range(4, MAX_SIGNAL_ANALYST_CACHE + 2):
        analyst._remember_result(f"sig-{idx}@z", {"value": idx})

    assert len(analyst._cache) == MAX_SIGNAL_ANALYST_CACHE
    assert "sig-2@b" not in analyst._cache
    assert "sig-1@a" in analyst._cache
    assert f"sig-{MAX_SIGNAL_ANALYST_CACHE + 1}@z" in analyst._cache
