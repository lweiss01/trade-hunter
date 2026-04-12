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
        for key, value in updates.items():
            os.environ[key] = str(value)
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
    for key, value in updates.items():
        os.environ[key] = str(value)


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


def _coerce_bool(value: object, field: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "on"}:
            return True
        if lowered in {"0", "false", "no", "off"}:
            return False
    raise ValueError(f"{field} must be a boolean")


def _coerce_int(value: object, field: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be an integer")
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str) and value.strip():
        return int(value.strip())
    raise ValueError(f"{field} must be an integer")


def _coerce_float(value: object, field: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be a number")
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str) and value.strip():
        return float(value.strip())
    raise ValueError(f"{field} must be a number")


def _coerce_text(value: object, field: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be text")
    if "\n" in value or "\r" in value:
        raise ValueError(f"{field} cannot contain newlines")
    if "=" in value and field.upper() not in {"DISCORD_WEBHOOK_ROUTES", "DISCORD_WEBHOOK_URL"}:
        # Routes and URLs can naturally have = in query params, but others shouldn't
        raise ValueError(f"{field} cannot contain '='")
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field} cannot contain only whitespace")
    return cleaned


def persist_runtime_settings(updates: dict[str, object], env_path: Path | None = None) -> dict[str, str]:
    """Persist editable runtime settings to .env for restart-required apply."""
    if not isinstance(updates, dict):
        raise ValueError("settings payload must be an object")

    env_updates: dict[str, str] = {}

    if "enable_simulation" in updates:
        env_updates["ENABLE_SIMULATION"] = "true" if _coerce_bool(updates["enable_simulation"], "enable_simulation") else "false"
    if "quiet_mode" in updates:
        env_updates["QUIET_MODE"] = "true" if _coerce_bool(updates["quiet_mode"], "quiet_mode") else "false"
    if "enable_kalshi" in updates:
        env_updates["ENABLE_KALSHI"] = "true" if _coerce_bool(updates["enable_kalshi"], "enable_kalshi") else "false"

    if "discord_alert_mode" in updates:
        alert_mode = _coerce_text(updates["discord_alert_mode"], "discord_alert_mode")
        if alert_mode not in {"all", "detector-only", "analyst-signals-only"}:
            raise ValueError("discord_alert_mode must be all, detector-only, or analyst-signals-only")
        env_updates["DISCORD_ALERT_MODE"] = alert_mode

    if "discord_analyst_followup" in updates:
        env_updates["DISCORD_ANALYST_FOLLOWUP"] = "true" if _coerce_bool(updates["discord_analyst_followup"], "discord_analyst_followup") else "false"

    if "discord_analyst_min_confidence" in updates:
        confidence = _coerce_text(updates["discord_analyst_min_confidence"], "discord_analyst_min_confidence")
        if confidence not in {"low", "medium", "high"}:
            raise ValueError("discord_analyst_min_confidence must be low, medium, or high")
        env_updates["DISCORD_ANALYST_MIN_CONFIDENCE"] = confidence

    if "spike_min_volume_delta" in updates:
        value = _coerce_float(updates["spike_min_volume_delta"], "spike_min_volume_delta")
        if value < 0:
            raise ValueError("spike_min_volume_delta must be >= 0")
        env_updates["SPIKE_MIN_VOLUME_DELTA"] = str(value)

    if "spike_min_price_move" in updates:
        value = _coerce_float(updates["spike_min_price_move"], "spike_min_price_move")
        if value < 0:
            raise ValueError("spike_min_price_move must be >= 0")
        env_updates["SPIKE_MIN_PRICE_MOVE"] = str(value)

    if "spike_score_threshold" in updates:
        value = _coerce_float(updates["spike_score_threshold"], "spike_score_threshold")
        if value < 0:
            raise ValueError("spike_score_threshold must be >= 0")
        env_updates["SPIKE_SCORE_THRESHOLD"] = str(value)

    if "spike_baseline_points" in updates:
        value = _coerce_int(updates["spike_baseline_points"], "spike_baseline_points")
        if value < 1:
            raise ValueError("spike_baseline_points must be >= 1")
        env_updates["SPIKE_BASELINE_POINTS"] = str(value)

    if "spike_cooldown_seconds" in updates:
        value = _coerce_int(updates["spike_cooldown_seconds"], "spike_cooldown_seconds")
        if value < 0:
            raise ValueError("spike_cooldown_seconds must be >= 0")
        env_updates["SPIKE_COOLDOWN_SECONDS"] = str(value)

    if "retention_days" in updates:
        value = _coerce_int(updates["retention_days"], "retention_days")
        if value < 1:
            raise ValueError("retention_days must be >= 1")
        env_updates["RETENTION_DAYS"] = str(value)

    if "host" in updates:
        env_updates["APP_HOST"] = _coerce_text(updates["host"], "host")

    if "port" in updates:
        value = _coerce_int(updates["port"], "port")
        if value < 1 or value > 65535:
            raise ValueError("port must be between 1 and 65535")
        env_updates["APP_PORT"] = str(value)

    if not env_updates:
        raise ValueError("No editable settings were provided")

    _persist_env_updates(env_updates, env_path=env_path)
    return env_updates


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
    admin_token: str | None = None
    retention_days: int = 7
    quiet_mode: bool = False
    is_commercial: bool = True


def load_settings() -> Settings:
    _load_env_file(ROOT / ".env")
    settings = Settings(
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
        admin_token=os.getenv("ADMIN_TOKEN") or None,
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
    
    # Load version/edition info
    from .edition import IS_COMMERCIAL
    settings = Settings(**{**settings.__dict__, "is_commercial": IS_COMMERCIAL})
    
    # Ensure security tokens exist (M014, M015)
    env_updates = {}
    if not settings.admin_token:
        import secrets
        token = secrets.token_urlsafe(32)
        env_updates["ADMIN_TOKEN"] = token
        settings = Settings(**{**settings.__dict__, "admin_token": token})
        print(f"--- SECURITY NOTICE: Generated new ADMIN_TOKEN: {token} ---")
        print("--- Save this token for administrative dashboard access! ---")
    
    if not settings.ingest_api_token:
        import secrets
        token = secrets.token_urlsafe(32)
        env_updates["INGEST_API_TOKEN"] = token
        settings = Settings(**{**settings.__dict__, "ingest_api_token": token})
        print(f"--- SECURITY NOTICE: Generated new INGEST_API_TOKEN: {token} ---")
        print("--- Use this token for external alert webhooks (Bearer auth)! ---")

    if env_updates:
        _persist_env_updates(env_updates)
    
    return settings
