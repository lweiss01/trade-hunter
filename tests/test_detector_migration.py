"""Tests for detector behavior consistency across store backends."""
from __future__ import annotations

from collections import deque
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


def test_detector_baseline_calculation_consistent():
    """Verify detector baseline calculation is deterministic."""
    settings = make_settings(
        spike_baseline_points=10,
        spike_min_volume_delta=500,
        spike_min_price_move=0.05,
        spike_score_threshold=3.0,
    )
    
    detector1 = SpikeDetector(settings)
    detector2 = SpikeDetector(settings)
    
    # Feed same event sequence to both
    base_time = datetime.now(UTC)
    events = []
    for i in range(15):
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="test-market",
            title="Test Market",
            yes_price=0.50 + (i * 0.01),
            volume=1000 + (i * 100),  # Cumulative
            volume_kind="cumulative",
            timestamp=base_time + timedelta(seconds=i * 10),
        )
        events.append(event)
        detector1.process(event)
        detector2.process(event)
    
    # Verify both have identical window state
    window1 = detector1.windows["test-market"]
    window2 = detector2.windows["test-market"]
    
    assert list(window1.volume_deltas) == list(window2.volume_deltas)
    assert detector1._baseline(window1) == detector2._baseline(window2)


def test_detector_volume_delta_cumulative():
    """Verify volume delta calculation for cumulative volumes."""
    settings = make_settings()
    detector = SpikeDetector(settings)
    
    event1 = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="cumulative-test",
        title="Test",
        volume=1000,
        volume_kind="cumulative",
        timestamp=datetime.now(UTC),
    )
    detector.process(event1)
    
    event2 = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="cumulative-test",
        title="Test",
        volume=1500,  # Delta should be 500
        volume_kind="cumulative",
        timestamp=datetime.now(UTC) + timedelta(seconds=10),
    )
    signal = detector.process(event2)
    
    # Verify delta calculation
    window = detector.windows["cumulative-test"]
    assert list(window.volume_deltas) == [500.0]


def test_detector_volume_delta_explicit():
    """Verify volume delta calculation for explicit deltas."""
    settings = make_settings()
    detector = SpikeDetector(settings)
    
    event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="delta-test",
        title="Test",
        volume=750,
        volume_kind="delta",
        timestamp=datetime.now(UTC),
    )
    detector.process(event)
    
    window = detector.windows["delta-test"]
    assert list(window.volume_deltas) == [750.0]


def test_detector_baseline_window_limit():
    """Verify baseline window respects max points limit."""
    settings = make_settings(spike_baseline_points=5)
    detector = SpikeDetector(settings)
    
    base_time = datetime.now(UTC)
    
    # Add 10 events
    for i in range(10):
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="limit-test",
            title="Test",
            volume=1000 + (i * 100),
            volume_kind="cumulative",
            timestamp=base_time + timedelta(seconds=i * 10),
        )
        detector.process(event)
    
    window = detector.windows["limit-test"]
    
    # Should only keep last 5 deltas
    assert len(window.volume_deltas) == 5
    # Should be [100, 100, 100, 100, 100] (last 5 deltas)
    assert list(window.volume_deltas) == [100.0, 100.0, 100.0, 100.0, 100.0]


def test_detector_signal_generation_threshold():
    """Verify signal generated when thresholds exceeded."""
    settings = make_settings(
        spike_min_volume_delta=500,
        spike_min_price_move=0.05,
        spike_score_threshold=3.0,
    )
    detector = SpikeDetector(settings)
    
    base_time = datetime.now(UTC)
    
    # Establish baseline with small deltas
    for i in range(5):
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="threshold-test",
            title="Test",
            yes_price=0.50,
            volume=1000 + (i * 50),
            volume_kind="cumulative",
            timestamp=base_time + timedelta(seconds=i * 10),
        )
        detector.process(event)
    
    # Large spike should trigger signal
    # Last volume was 1200 (1000 + 4*50), so delta will be 1300
    spike_event = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="threshold-test",
        title="Test",
        yes_price=0.58,  # 8% move
        volume=2500,  # Delta of 1300 (vs baseline ~50)
        volume_kind="cumulative",
        timestamp=base_time + timedelta(seconds=60),
    )
    signal = detector.process(spike_event)
    
    assert signal is not None
    assert signal.score > settings.spike_score_threshold
    assert signal.volume_delta == 1300.0
    assert signal.price_move == pytest.approx(0.08)


def test_detector_cooldown_prevents_duplicate_signals():
    """Verify cooldown prevents rapid duplicate signals."""
    settings = make_settings(
        spike_min_volume_delta=500,
        spike_min_price_move=0.05,
        spike_cooldown_seconds=60,
    )
    detector = SpikeDetector(settings)
    
    base_time = datetime.now(UTC)
    
    # First spike
    event1 = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="cooldown-test",
        title="Test",
        yes_price=0.50,
        volume=2000,
        volume_kind="delta",
        timestamp=base_time,
    )
    signal1 = detector.process(event1)
    assert signal1 is not None
    
    # Second spike within cooldown
    event2 = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="cooldown-test",
        title="Test",
        yes_price=0.58,
        volume=2500,
        volume_kind="delta",
        timestamp=base_time + timedelta(seconds=30),
    )
    signal2 = detector.process(event2)
    assert signal2 is None  # Suppressed by cooldown
    
    # Third spike after cooldown
    event3 = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="cooldown-test",
        title="Test",
        yes_price=0.65,
        volume=3000,
        volume_kind="delta",
        timestamp=base_time + timedelta(seconds=120),
    )
    signal3 = detector.process(event3)
    assert signal3 is not None  # Cooldown expired


def test_detector_regression_known_sequence():
    """Regression test: known event sequence produces expected signals."""
    settings = make_settings(
        spike_baseline_points=5,
        spike_min_volume_delta=500,
        spike_min_price_move=0.05,
        spike_score_threshold=3.0,
        spike_cooldown_seconds=60,
    )
    detector = SpikeDetector(settings)
    
    base_time = datetime.now(UTC)
    
    # Known sequence: 5 small events, then 1 spike
    small_events = [
        (1000, 0.50),
        (1050, 0.51),
        (1100, 0.52),
        (1150, 0.51),
        (1200, 0.50),
    ]
    
    signals = []
    for i, (volume, price) in enumerate(small_events):
        event = MarketEvent(
            source="test",
            platform="polymarket",
            market_id="regression-test",
            title="Test",
            yes_price=price,
            volume=volume,
            volume_kind="cumulative",
            timestamp=base_time + timedelta(seconds=i * 10),
        )
        signal = detector.process(event)
        if signal:
            signals.append(signal)
    
    # No signals from small events
    assert len(signals) == 0
    
    # Baseline should be ~50 (average of [50, 50, 50, 50])
    window = detector.windows["regression-test"]
    baseline = detector._baseline(window)
    assert 45 <= baseline <= 55
    
    # Spike event
    spike = MarketEvent(
        source="test",
        platform="polymarket",
        market_id="regression-test",
        title="Test",
        yes_price=0.62,  # 12% move from last
        volume=3200,  # Delta of 2000
        volume_kind="cumulative",
        timestamp=base_time + timedelta(seconds=60),
    )
    spike_signal = detector.process(spike)
    
    assert spike_signal is not None
    assert spike_signal.volume_delta == 2000.0
    assert spike_signal.baseline_volume_delta == baseline
    assert spike_signal.score > 10.0  # Very high score
