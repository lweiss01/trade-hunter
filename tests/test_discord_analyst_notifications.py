from __future__ import annotations

from unittest.mock import Mock

from app.models import MarketEvent, SpikeSignal
from app.notifiers import DiscordWebhookNotifier
from app.service import TradeHunterService


class ImmediateAnalyst:
    def __init__(self, analyst_result: dict[str, object]) -> None:
        self.analyst_result = analyst_result
        self.enqueue_calls = 0

    def enqueue(self, signal, recent_flow, on_complete=None):
        self.enqueue_calls += 1
        if on_complete:
            on_complete(signal, self.analyst_result)


def _mock_settings(**overrides):
    defaults = {
        "enable_simulation": False,
        "enable_kalshi": False,
        "discord_webhook_url": None,
        "discord_webhook_routes": {},
        "discord_alert_mode": "all",
        "discord_analyst_followup": True,
        "discord_analyst_min_confidence": "medium",
        "polyalerthub_token": None,
        "ingest_api_token": None,
        "spike_min_volume_delta": 120.0,
        "spike_min_price_move": 0.03,
        "spike_score_threshold": 3.0,
        "spike_baseline_points": 24,
        "spike_cooldown_seconds": 300,
        "retention_days": 7,
        "quiet_mode": True,
        "kalshi_markets": [],
        "kalshi_api_key_id": None,
        "kalshi_private_key_path": None,
        "host": "127.0.0.1",
        "port": 8765,
    }
    defaults.update(overrides)
    return Mock(**defaults)


def _signal() -> SpikeSignal:
    event = MarketEvent(
        source="test",
        platform="kalshi",
        market_id="TEST-MARKET",
        title="Test Market",
        yes_price=0.61,
        volume=500.0,
        volume_kind="delta",
    )
    return SpikeSignal(
        event=event,
        score=5.0,
        volume_delta=500.0,
        price_move=0.04,
        baseline_volume_delta=100.0,
        reason="Test signal",
        tier="notable",
        topic="crypto",
        source_label="test",
    )


def _analyst_result(noise_or_signal: str = "signal", confidence: str = "high") -> dict[str, object]:
    return {
        "noise_or_signal": noise_or_signal,
        "direction": "yes",
        "confidence": confidence,
        "rationale": "Looks actionable.",
        "threshold_note": "none",
        "generated_at": "2026-04-03T21:00:00+00:00",
    }


def test_all_mode_sends_detector_and_analyst_followup():
    service = TradeHunterService(_mock_settings(discord_alert_mode="all", discord_analyst_followup=True))
    service.store = Mock()
    service.store.recent_events.return_value = []
    service.detector.process = Mock(return_value=_signal())
    service.notifier = Mock()
    service.notifier.should_send_detector_alert.return_value = True
    service.notifier.should_send_analyst_followup.return_value = True
    service.notifier.should_send_analyst_signal_only.return_value = False
    service.notifier.notify_analyst_followup.return_value = True
    service._analyst = ImmediateAnalyst(_analyst_result())

    assert service.ingest_event(_signal().event) is True

    service.notifier.notify.assert_called_once()
    service.notifier.notify_analyst_followup.assert_called_once()


def test_analyst_signals_only_suppresses_detector_alert_until_analyst_signal():
    service = TradeHunterService(_mock_settings(discord_alert_mode="analyst-signals-only", discord_analyst_min_confidence="medium"))
    service.store = Mock()
    service.store.recent_events.return_value = []
    service.detector.process = Mock(return_value=_signal())
    service.notifier = Mock()
    service.notifier.should_send_detector_alert.return_value = False
    service.notifier.should_send_analyst_followup.return_value = False
    service.notifier.should_send_analyst_signal_only.return_value = True
    service.notifier.notify_analyst_followup.return_value = True
    service._analyst = ImmediateAnalyst(_analyst_result(noise_or_signal="signal", confidence="high"))

    assert service.ingest_event(_signal().event) is True

    service.notifier.notify.assert_not_called()
    service.notifier.notify_analyst_followup.assert_called_once()


def test_analyst_signals_only_skips_noise_followup():
    service = TradeHunterService(_mock_settings(discord_alert_mode="analyst-signals-only", discord_analyst_min_confidence="medium"))
    service.store = Mock()
    service.store.recent_events.return_value = []
    service.detector.process = Mock(return_value=_signal())
    service.notifier = Mock()
    service.notifier.should_send_detector_alert.return_value = False
    service.notifier.should_send_analyst_followup.return_value = False
    service.notifier.should_send_analyst_signal_only.return_value = False
    service.notifier.notify_analyst_followup.return_value = True
    service._analyst = ImmediateAnalyst(_analyst_result(noise_or_signal="noise", confidence="high"))

    assert service.ingest_event(_signal().event) is True

    service.notifier.notify.assert_not_called()
    service.notifier.notify_analyst_followup.assert_not_called()


def test_notifier_builds_analyst_followup_payload_with_reference():
    notifier = DiscordWebhookNotifier(
        "https://discord.example/webhook",
        {"crypto": "https://discord.example/webhook"},
        alert_mode="all",
        analyst_followup=True,
        analyst_min_confidence="medium",
    )
    signal = _signal().to_dict()
    payload = notifier.build_analyst_followup_payload(signal, _analyst_result())
    embed = payload["embeds"][0]

    assert embed["title"] == "Analyst follow-up: Test Market"
    assert embed["description"] == "Looks actionable."
    assert embed["footer"]["text"].startswith("TEST-MARKET • ")
    field_names = [field["name"] for field in embed["fields"]]
    assert "Verdict" in field_names
    assert "Confidence" in field_names
    assert "Original tier" in field_names
