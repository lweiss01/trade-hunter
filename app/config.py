from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def _bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _int(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value else default


def _float(name: str, default: float) -> float:
    value = os.getenv(name)
    return float(value) if value else default


def _text(name: str, default: str) -> str:
    value = os.getenv(name)
    return value.strip() if value else default


def _csv(name: str) -> list[str]:
    value = os.getenv(name, "")
    return [item.strip() for item in value.split(",") if item.strip()]


def _kv_pairs(name: str) -> dict[str, str]:
    value = os.getenv(name, "")
    if not value:
        return {}

    pairs: dict[str, str] = {}
    for raw_item in value.replace("\n", ";").split(";"):
        item = raw_item.strip()
        if not item or "=" not in item:
            continue
        key, mapped = item.split("=", 1)
        key = key.strip().lower()
        mapped = mapped.strip()
        if key and mapped:
            pairs[key] = mapped
    return pairs


def _persist_env_updates(updates: dict[str, str], env_path: Path | None = None) -> None:
    path = env_path or (ROOT / ".env")

    if not path.exists():
        content = "\n".join(f"{key}={value}" for key, value in updates.items()) + "\n"
        path.write_text(content, encoding="utf-8")
        return

    lines = path.read_text(encoding="utf-8").splitlines()
    remaining = dict(updates)

    for idx, raw in enumerate(lines):
        stripped = raw.strip()
        if not stripped or "=" not in stripped:
            continue
        key = stripped.split("=", 1)[0].strip()
        if key in remaining:
            lines[idx] = f"{key}={remaining.pop(key)}"

    if remaining:
        if lines and lines[-1].strip() != "":
            lines.append("")
        lines.extend(f"{key}={value}" for key, value in remaining.items())

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def persist_kalshi_markets(markets: list[str], env_path: Path | None = None) -> None:
    """Persist KALSHI_MARKETS to .env for restart-safe ticker management."""
    _persist_env_updates({"KALSHI_MARKETS": ",".join(markets)}, env_path=env_path)


def persist_detector_thresholds(
    *,
    min_volume_delta: float | None = None,
    min_price_move: float | None = None,
    score_threshold: float | None = None,
    env_path: Path | None = None,
) -> None:
    updates: dict[str, str] = {}
    if min_volume_delta is not None:
        updates["SPIKE_MIN_VOLUME_DELTA"] = str(min_volume_delta)
    if min_price_move is not None:
        updates["SPIKE_MIN_PRICE_MOVE"] = str(min_price_move)
    if score_threshold is not None:
        updates["SPIKE_SCORE_THRESHOLD"] = str(score_threshold)
    if updates:
        _persist_env_updates(updates, env_path=env_path)


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    enable_simulation: bool
    enable_kalshi: bool
    discord_webhook_url: str | None
    discord_webhook_routes: dict[str, str]
    discord_alert_mode: str = "all"
    discord_analyst_followup: bool = True
    discord_analyst_min_confidence: str = "medium"
    ingest_api_token: str | None = None
    spike_min_volume_delta: float = 120.0
    spike_min_price_move: float = 0.03
    spike_score_threshold: float = 3.0
    spike_baseline_points: int = 24
    spike_cooldown_seconds: int = 300
    kalshi_markets: list[str] = field(default_factory=list)
    kalshi_api_key_id: str | None = None
    kalshi_private_key_path: str | None = None
    polyalerthub_token: str | None = None
    retention_days: int = 7
    quiet_mode: bool = False


def load_settings() -> Settings:
    _load_env_file(ROOT / ".env")
    return Settings(
        host=os.getenv("APP_HOST", "127.0.0.1"),
        port=_int("APP_PORT", 8765),
        enable_simulation=_bool("ENABLE_SIMULATION", True),
        enable_kalshi=_bool("ENABLE_KALSHI", False),
        discord_webhook_url=os.getenv("DISCORD_WEBHOOK_URL") or None,
        discord_webhook_routes=_kv_pairs("DISCORD_WEBHOOK_ROUTES"),
        discord_alert_mode=_text("DISCORD_ALERT_MODE", "all"),
        discord_analyst_followup=_bool("DISCORD_ANALYST_FOLLOWUP", True),
        discord_analyst_min_confidence=_text("DISCORD_ANALYST_MIN_CONFIDENCE", "medium"),
        ingest_api_token=os.getenv("INGEST_API_TOKEN") or None,
        polyalerthub_token=os.getenv("POLYALERTHUB_TOKEN") or None,
        spike_min_volume_delta=_float("SPIKE_MIN_VOLUME_DELTA", 120.0),
        spike_min_price_move=_float("SPIKE_MIN_PRICE_MOVE", 0.03),
        spike_score_threshold=_float("SPIKE_SCORE_THRESHOLD", 3.0),
        spike_baseline_points=_int("SPIKE_BASELINE_POINTS", 24),
        spike_cooldown_seconds=_int("SPIKE_COOLDOWN_SECONDS", 300),
        retention_days=_int("RETENTION_DAYS", 7),
        kalshi_markets=_csv("KALSHI_MARKETS"),
        kalshi_api_key_id=os.getenv("KALSHI_API_KEY_ID") or None,
        kalshi_private_key_path=os.getenv("KALSHI_PRIVATE_KEY_PATH") or None,
        quiet_mode=_bool("QUIET_MODE", False),
    )
