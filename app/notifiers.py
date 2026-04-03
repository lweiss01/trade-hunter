from __future__ import annotations

import json
import urllib.error
import urllib.request

from .models import SpikeSignal


_ANALYST_COLORS = {
    "signal": 0x4BBFC9,
    "noise": 0xF85525,
    "uncertain": 0xC8A96A,
}


_TIER_COLORS = {
    "watch": 0xF4C542,
    "notable": 0xFF9B54,
    "high conviction flow": 0xFF6B57,
    "cross-venue divergence": 0x5AC8FA,
}


class DiscordWebhookNotifier:
    def __init__(
        self,
        webhook_url: str | None,
        routed_webhooks: dict[str, str] | None = None,
        alert_mode: str = "all",
        analyst_followup: bool = True,
        analyst_min_confidence: str = "medium",
    ) -> None:
        self.webhook_url = webhook_url
        self.routed_webhooks = {key.lower(): value for key, value in (routed_webhooks or {}).items()}
        self.alert_mode = alert_mode.strip().lower() if alert_mode else "all"
        self.analyst_followup = analyst_followup
        self.analyst_min_confidence = analyst_min_confidence.strip().lower() if analyst_min_confidence else "medium"

    def enabled(self) -> bool:
        return bool(self.webhook_url or self.routed_webhooks)

    def notify(self, signal: SpikeSignal) -> bool:
        webhook_url = self._resolve_webhook(signal)
        if not webhook_url:
            return False

        payload = self.build_payload(signal)
        return self._post_payload(webhook_url, payload)

    def notify_analyst_followup(self, signal: dict[str, object], analyst: dict[str, object]) -> bool:
        webhook_url = self._resolve_webhook_from_dict(signal)
        if not webhook_url:
            return False

        payload = self.build_analyst_followup_payload(signal, analyst)
        return self._post_payload(webhook_url, payload)

    def should_send_detector_alert(self) -> bool:
        return self.alert_mode in {"all", "detector-only"}

    def should_send_analyst_followup(self) -> bool:
        return self.alert_mode == "all" and self.analyst_followup

    def should_send_analyst_signal_only(self, analyst: dict[str, object]) -> bool:
        if self.alert_mode != "analyst-signals-only":
            return False
        if str(analyst.get("noise_or_signal") or "").lower() != "signal":
            return False
        return self._confidence_rank(str(analyst.get("confidence") or "low")) >= self._confidence_rank(
            self.analyst_min_confidence
        )

    def _post_payload(self, webhook_url: str, payload: dict[str, object]) -> bool:
        request = urllib.request.Request(
            webhook_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Trade-Hunter-Bot/1.0"
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=10):
                return True
        except (urllib.error.URLError, TimeoutError):
            return False

    def build_payload(self, signal: SpikeSignal) -> dict[str, object]:
        topic = signal.topic or signal.event.topic or "general"
        fields = [
            {"name": "Tier", "value": signal.tier, "inline": True},
            {"name": "Topic", "value": topic, "inline": True},
            {"name": "Source", "value": signal.source_label or signal.event.source, "inline": True},
            {"name": "Platform", "value": signal.event.platform, "inline": True},
            {"name": "Event", "value": signal.event.event_kind, "inline": True},
            {"name": "Market", "value": signal.event.market_id, "inline": True},
            {
                "name": "Yes price",
                "value": (
                    f"{signal.event.yes_price:.1%}" if signal.event.yes_price is not None else "n/a"
                ),
                "inline": True,
            },
            {"name": "Volume delta", "value": f"{signal.volume_delta:.0f}", "inline": True},
            {"name": "Baseline", "value": f"{signal.baseline_volume_delta:.0f}", "inline": True},
            {"name": "Price move", "value": f"{signal.price_move:.1%}", "inline": True},
            {"name": "Score", "value": f"{signal.score:.2f}", "inline": True},
        ]
        if signal.event.trade_size is not None:
            fields.append(
                {
                    "name": "Trade size",
                    "value": f"{signal.event.trade_size:.0f}",
                    "inline": True,
                }
            )
        if signal.event.trade_side:
            fields.append(
                {
                    "name": "Trade side",
                    "value": signal.event.trade_side,
                    "inline": True,
                }
            )

        footer_bits = [signal.event.platform, signal.event.source, "live" if signal.event.live else "demo"]
        embed: dict[str, object] = {
            "title": f"{signal.tier.title()}: {signal.event.title}",
            "description": signal.reason,
            "color": _TIER_COLORS.get(signal.tier, _TIER_COLORS["watch"]),
            "fields": fields,
            "footer": {"text": " • ".join(footer_bits)},
            "timestamp": signal.detected_at.isoformat(),
        }
        if signal.event.market_url:
            embed["url"] = signal.event.market_url
        return {"embeds": [embed]}

    def build_analyst_followup_payload(self, signal: dict[str, object], analyst: dict[str, object]) -> dict[str, object]:
        event = signal.get("event") or {}
        market_id = str(event.get("market_id") or "unknown")
        title = str(event.get("title") or market_id)
        verdict = str(analyst.get("noise_or_signal") or "uncertain")
        direction = str(analyst.get("direction") or "unclear")
        confidence = str(analyst.get("confidence") or "low")
        rationale = str(analyst.get("rationale") or "")
        threshold_note = str(analyst.get("threshold_note") or "none")
        detected_at = str(signal.get("detected_at") or "")

        fields = [
            {"name": "Verdict", "value": verdict, "inline": True},
            {"name": "Direction", "value": direction, "inline": True},
            {"name": "Confidence", "value": confidence, "inline": True},
            {"name": "Market", "value": market_id, "inline": True},
            {"name": "Original tier", "value": str(signal.get("tier") or "watch"), "inline": True},
        ]
        if threshold_note and threshold_note != "none":
            fields.append({"name": "Threshold note", "value": threshold_note, "inline": False})

        embed: dict[str, object] = {
            "title": f"Analyst follow-up: {title}",
            "description": rationale or "No analyst rationale provided.",
            "color": _ANALYST_COLORS.get(verdict, _ANALYST_COLORS["uncertain"]),
            "fields": fields,
            "footer": {"text": f"{market_id} • {detected_at}"},
            "timestamp": str(analyst.get("generated_at") or detected_at),
        }
        market_url = event.get("market_url")
        if market_url:
            embed["url"] = market_url
        return {"embeds": [embed]}

    def _confidence_rank(self, value: str) -> int:
        return {"low": 0, "medium": 1, "high": 2}.get(value.strip().lower(), 0)

    def _resolve_webhook(self, signal: SpikeSignal) -> str | None:
        topic = (signal.topic or signal.event.topic or "").lower()
        return self.routed_webhooks.get(topic) or self.webhook_url

    def _resolve_webhook_from_dict(self, signal: dict[str, object]) -> str | None:
        event = signal.get("event") or {}
        topic = str(signal.get("topic") or event.get("topic") or "").lower()
        return self.routed_webhooks.get(topic) or self.webhook_url
