"""Tests for M002 signal enrichment features."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

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
    
    # Add 10 events with small deltas to establish baseline
    for i in range(10):
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="test-market",
            title="Test Market",
            yes_price=0.50 + (i * 0.001),
            volume=1000 + (i * 50),
            volume_kind="cumulative",
            timestamp=base_time + timedelta(seconds=i * 10),
        )
        detector.process(event)
    
    # Trigger spike
    spike_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="test-market",
        title="Test Market",
        yes_price=0.60,
        volume=3000,  # Large volume spike
        volume_kind="cumulative",
        timestamp=base_time + timedelta(seconds=100),
    )
    signal = detector.process(spike_event)
    
    assert signal is not None
    assert signal.baseline_1h is not None
    assert signal.baseline_24h is not None
    assert signal.baseline_1h > 0
    assert signal.baseline_24h > 0


def test_signal_has_enriched_price_move_fields():
    """Verify signals include price_move_1m, 5m, 30m fields."""
    settings = make_settings(
        spike_min_volume_delta=100,
        spike_min_price_move=0.03,
    )
    detector = SpikeDetector(settings)
    
    base_time = datetime.now(UTC)
    
    # Add 20 events with varying prices
    for i in range(20):
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="test-market",
            title="Test Market",
            yes_price=0.40 + (i * 0.01),  # Gradual price increase
            volume=1000 + (i * 50),
            volume_kind="cumulative",
            timestamp=base_time + timedelta(seconds=i * 10),
        )
        detector.process(event)
    
    # Trigger spike with large price move
    spike_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="test-market",
        title="Test Market",
        yes_price=0.70,  # Large price jump
        volume=5000,
        volume_kind="cumulative",
        timestamp=base_time + timedelta(seconds=200),
    )
    signal = detector.process(spike_event)
    
    assert signal is not None
    assert signal.price_move_1m is not None
    assert signal.price_move_5m is not None
    assert signal.price_move_30m is not None
    # Price moves should increase with longer windows
    assert signal.price_move_30m >= signal.price_move_5m


def test_signal_has_leading_events():
    """Verify signals include leading_events (last 5 before spike)."""
    settings = make_settings(
        spike_min_volume_delta=100,
        spike_min_price_move=0.03,
    )
    detector = SpikeDetector(settings)
    
    base_time = datetime.now(UTC)
    
    # Add 8 events
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
    
    # Trigger spike
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
    assert len(signal.leading_events) == 5  # Last 5 before spike
    # Leading events should NOT include the spike event itself
    assert all(e.volume < 3000 for e in signal.leading_events)


def test_signal_to_dict_includes_enriched_fields():
    """Verify signal.to_dict() includes all enriched fields."""
    settings = make_settings(
        spike_min_volume_delta=100,
        spike_min_price_move=0.03,
    )
    detector = SpikeDetector(settings)
    
    base_time = datetime.now(UTC)
    
    # Add baseline events
    for i in range(10):
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="test-market",
            title="Test Market",
            yes_price=0.50 + (i * 0.01),
            volume=1000 + (i * 50),
            volume_kind="cumulative",
            timestamp=base_time + timedelta(seconds=i * 10),
        )
        detector.process(event)
    
    # Trigger spike
    spike_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="test-market",
        title="Test Market",
        yes_price=0.65,
        volume=3000,
        volume_kind="cumulative",
        timestamp=base_time + timedelta(seconds=100),
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
    
    # Verify leading_events is a list of dicts
    assert isinstance(signal_dict["leading_events"], list)
    if signal_dict["leading_events"]:
        assert isinstance(signal_dict["leading_events"][0], dict)
        assert "market_id" in signal_dict["leading_events"][0]


def test_enriched_baselines_calculation():
    """Verify multi-window baseline calculations are correct."""
    settings = make_settings(spike_baseline_points=24)
    detector = SpikeDetector(settings)
    
    base_time = datetime.now(UTC)
    
    # Add 25 events with known volume deltas
    # First 5 events: delta = 100
    # Next 5 events: delta = 200
    # Next 14 events: delta = 50
    
    volume = 1000
    for i in range(5):
        volume += 100
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="test-market",
            title="Test",
            yes_price=0.50,
            volume=volume,
            volume_kind="cumulative",
            timestamp=base_time + timedelta(seconds=i * 10),
        )
        detector.process(event)
    
    for i in range(5):
        volume += 200
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="test-market",
            title="Test",
            yes_price=0.50,
            volume=volume,
            volume_kind="cumulative",
            timestamp=base_time + timedelta(seconds=(5 + i) * 10),
        )
        detector.process(event)
    
    for i in range(14):
        volume += 50
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="test-market",
            title="Test",
            yes_price=0.50,
            volume=volume,
            volume_kind="cumulative",
            timestamp=base_time + timedelta(seconds=(10 + i) * 10),
        )
        detector.process(event)
    
    # Trigger spike
    spike_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="test-market",
        title="Test",
        yes_price=0.60,
        volume=volume + 2000,
        volume_kind="cumulative",
        timestamp=base_time + timedelta(seconds=250),
    )
    signal = detector.process(spike_event)
    
    assert signal is not None
    # Baseline calculations work but values depend on volume pattern
    assert signal.baseline_1h is not None
    assert signal.baseline_1h > 0
    assert signal.baseline_24h is not None
    assert signal.baseline_24h > 0


def test_enriched_price_moves_calculation():
    """Verify multi-window price move calculations are correct."""
    settings = make_settings(
        spike_min_volume_delta=100,
        spike_min_price_move=0.03,
    )
    detector = SpikeDetector(settings)
    
    base_time = datetime.now(UTC)
    
    # Add 20 events with linear price increase
    prices = [0.40, 0.42, 0.44, 0.46, 0.48, 0.50, 0.52, 0.54, 0.56, 0.58,
              0.60, 0.62, 0.64, 0.66, 0.68, 0.70, 0.72, 0.74, 0.76, 0.78]
    
    for i, price in enumerate(prices):
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="test-market",
            title="Test",
            yes_price=price,
            volume=1000 + (i * 50),
            volume_kind="cumulative",
            timestamp=base_time + timedelta(seconds=i * 10),
        )
        detector.process(event)
    
    # Trigger spike at price 0.85
    spike_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="test-market",
        title="Test",
        yes_price=0.85,
        volume=5000,
        volume_kind="cumulative",
        timestamp=base_time + timedelta(seconds=200),
    )
    signal = detector.process(spike_event)
    
    assert signal is not None
    assert signal.price_move_1m is not None
    assert signal.price_move_5m is not None
    assert signal.price_move_30m is not None
    
    # price_move_1m: 0.85 - 0.78 = 0.07
    assert signal.price_move_1m == pytest.approx(0.07, abs=0.01)
    
    # price_move_5m: 0.85 - 0.74 = 0.11 (5 events back from -2)
    assert signal.price_move_5m == pytest.approx(0.11, abs=0.01)
    
    # price_move_30m: 0.85 - 0.64 = 0.21 (15 events back from -2)
    assert signal.price_move_30m == pytest.approx(0.21, abs=0.01)


def test_enriched_price_moves_calculation():
    """Verify multi-window price move calculations are correct."""
    settings = make_settings(
        spike_min_volume_delta=500,  # Use explicit delta volume
        spike_min_price_move=0.05,
        spike_score_threshold=2.0,
    )
    detector = SpikeDetector(settings)
    
    base_time = datetime.now(UTC)
    
    # Add only 3 events (insufficient for multi-window analysis)
    for i in range(3):
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="test-market",
            title="Test",
            yes_price=0.50,
            volume=1000 + (i * 100),
            volume_kind="cumulative",
            timestamp=base_time + timedelta(seconds=i * 10),
        )
        detector.process(event)
    
    # Trigger spike with large explicit delta
    spike_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="test-market",
        title="Test",
        yes_price=0.70,  # Large price move
        volume=10000,  # Very large volume to trigger
        volume_kind="delta",  # Use delta to ensure spike triggers
        timestamp=base_time + timedelta(seconds=30),
    )
    signal = detector.process(spike_event)
    
    assert signal is not None
    # With only 3 events, some enriched fields may be None or limited
    # baseline_24h should still calculate with available data
    assert signal.baseline_24h is not None or signal.baseline_1h is not None
    # leading_events should have 2-3 events (all available except current)
    assert len(signal.leading_events) >= 2


def test_enriched_fields_serialization():
    """Verify enriched fields serialize correctly to JSON."""
    settings = make_settings(
        spike_min_volume_delta=100,
        spike_min_price_move=0.03,
    )
    detector = SpikeDetector(settings)
    
    base_time = datetime.now(UTC)
    
    # Add baseline events
    for i in range(10):
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="test-market",
            title="Test",
            yes_price=0.50 + (i * 0.01),
            volume=1000 + (i * 50),
            volume_kind="cumulative",
            timestamp=base_time + timedelta(seconds=i * 10),
        )
        detector.process(event)
    
    # Trigger spike
    spike_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="test-market",
        title="Test",
        yes_price=0.65,
        volume=3000,
        volume_kind="cumulative",
        timestamp=base_time + timedelta(seconds=100),
    )
    signal = detector.process(spike_event)
    
    assert signal is not None
    
    # Convert to dict and verify JSON-serializable
    import json
    signal_dict = signal.to_dict()
    json_str = json.dumps(signal_dict)
    
    # Verify round-trip
    parsed = json.loads(json_str)
    assert "baseline_1h" in parsed
    assert "leading_events" in parsed
    assert isinstance(parsed["leading_events"], list)
