from __future__ import annotations

import json
import urllib.error
import urllib.request

from .models import SpikeSignal


_TIER_COLORS = {
    "watch": 0xF4C542,
    "notable": 0xFF9B54,
    "high conviction flow": 0xFF6B57,
    "cross-venue divergence": 0x5AC8FA,
}


class DiscordWebhookNotifier:
    def __init__(self, webhook_url: str | None, routed_webhooks: dict[str, str] | None = None) -> None:
        self.webhook_url = webhook_url
        self.routed_webhooks = {key.lower(): value for key, value in (routed_webhooks or {}).items()}

    def enabled(self) -> bool:
        return bool(self.webhook_url or self.routed_webhooks)

    def notify(self, signal: SpikeSignal) -> bool:
        webhook_url = self._resolve_webhook(signal)
        if not webhook_url:
            return False

        payload = self.build_payload(signal)
        request = urllib.request.Request(
            webhook_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
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

    def _resolve_webhook(self, signal: SpikeSignal) -> str | None:
        topic = (signal.topic or signal.event.topic or "").lower()
        return self.routed_webhooks.get(topic) or self.webhook_url
