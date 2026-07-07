from __future__ import annotations

import json
import os
import shutil
import stat
import sys
from datetime import UTC, datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


APP_DATA_DIR_NAME = "Trade Hunter"
STATE_FILE_NAMES = (
    ".env",
    "trade_hunter.db",
    "trade_hunter.db-wal",
    "trade_hunter.db-shm",
    "docs/TUNING-BACKLOG.md",
)
STATE_DIRECTORY_NAMES = ("cache", "state", "logs")
RUNTIME_STATUS_FILE_NAME = "runtime-status.json"
MAX_RUNTIME_STATUS_ENTRIES = 20

# Hardened security array extending tracking to explicit OAuth elements
_SENSITIVE_KEY_PARTS = (
    "access_token",
    "api_key",
    "authorization",
    "bearer",
    "private_key",
    "refresh_token",
    "secret",
    "token",
    "webhook",
)


def _check_file_permissions(path: Path, desc: str) -> None:
    """Evaluates security context permissions on highly sensitive credential objects."""
    try:
        st = os.stat(path)
        # Check POSIX configurations for over-permissive group/world visibility
        if os.name == 'posix':
            if st.st_mode & (stat.S_IRGRP | stat.S_IROTH):
                print(f"[SECURITY WARNING] {desc} '{path}' has overly permissive read privileges. "
                      f"Consider executing 'chmod 600' to secure it to owner-only access.")
    except FileNotFoundError:
        pass


def _path_has_existing_state(path: Path) -> bool:
    return any((path / name).exists() for name in (*STATE_FILE_NAMES, *STATE_DIRECTORY_NAMES))


def _runtime_status_path(data_root: Path | None = None) -> Path:
    return (data_root or DATA_ROOT) / RUNTIME_STATUS_FILE_NAME


def _sanitize_runtime_value(value: Any, key_hint: str = "") -> Any:
    key = key_hint.lower()
    if any(part in key for part in _SENSITIVE_KEY_PARTS):
        return value if isinstance(value, bool) else "[redacted]"
    if isinstance(value, dict):
        return {str(k): _sanitize_runtime_value(v, str(k)) for k, v in value.items()}
    if isinstance(value, list):
        return [_sanitize_runtime_value(item, key_hint) for item in value]
    if isinstance(value, tuple):
        return [_sanitize_runtime_value(item, key_hint) for item in value]
    return value


def read_runtime_status(data_root: Path | None = None) -> list[dict[str, Any]]:
    path = _runtime_status_path(data_root)
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    entries = payload if isinstance(payload, list) else payload.get("entries", [])
    return [entry for entry in entries if isinstance(entry, dict)][-MAX_RUNTIME_STATUS_ENTRIES:]


def record_runtime_status(
    category: str,
    buyer_headline: str,
    support_detail: str,
    *,
    details: dict[str, Any] | None = None,
    data_root: Path | None = None,
) -> dict[str, Any]:
    root = data_root or DATA_ROOT
    entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        "category": str(category),
        "buyer_headline": str(buyer_headline),
        "support_detail": str(support_detail),
        "details": _sanitize_runtime_value(details or {}),
    }
    entries = [*read_runtime_status(root), entry][-MAX_RUNTIME_STATUS_ENTRIES:]
    path = _runtime_status_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(entries, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return entry


def _move_state_item(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.move(str(source), str(destination))
        return
    try:
        source.replace(destination)
    except OSError:
        shutil.copy2(source, destination)
        source.unlink()


def _migrate_legacy_state(exe_dir: Path, data_root: Path) -> None:
    moved: list[str] = []
    conflicts: list[str] = []
    for rel_name in (*STATE_FILE_NAMES, *STATE_DIRECTORY_NAMES):
        source = exe_dir / rel_name
        if not source.exists():
            continue
        destination = data_root / rel_name
        if destination.exists():
            conflicts.append(rel_name)
            continue
        _move_state_item(source, destination)
        moved.append(rel_name)

    if conflicts:
        record_runtime_status(
            "data-root-conflict",
            "Existing app data was kept.",
            "Legacy beside-exe state was found, but app-data already had matching state. App-data won and legacy files were left in place.",
            details={"conflict_categories": conflicts},
            data_root=data_root,
        )
    if moved:
        record_runtime_status(
            "data-root-migrated",
            "Existing Trade Hunter data was moved to durable app storage.",
            "Legacy beside-exe runtime state was migrated into the platform app-data root for future packaged launches.",
            details={"migrated_categories": moved},
            data_root=data_root,
        )


def _platform_data_root() -> Path | None:
    if sys.platform == "win32":
        base = os.getenv("LOCALAPPDATA") or os.getenv("APPDATA")
        return Path(base) / APP_DATA_DIR_NAME if base else None
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / APP_DATA_DIR_NAME

    base = os.getenv("XDG_DATA_HOME")
    if base:
        return Path(base) / "trade-hunter"
    return Path.home() / ".local" / "share" / "trade-hunter"


def _resolve_data_root(exe_dir: Path) -> Path:
    override = os.getenv("TRADE_HUNTER_DATA_ROOT")
    if override:
        return Path(override).expanduser().resolve()

    # Dev build: exe is in dist/ alongside the source tree — use project root.
    if exe_dir.name.lower() == "dist" and (exe_dir.parent / "app").exists():
        return exe_dir.parent

    platform_root = _platform_data_root()

    # If AppData already has existing state, platform mode is active and wins.
    if platform_root and _path_has_existing_state(platform_root):
        if _path_has_existing_state(exe_dir):
            _migrate_legacy_state(exe_dir, platform_root)
        return platform_root

    # If AppData is empty, but we have a legacy database beside the exe, migrate it.
    if platform_root and (exe_dir / "trade_hunter.db").exists():
        _migrate_legacy_state(exe_dir, platform_root)
        return platform_root

    # Portable mode: customer placed a .env next to the exe.
    if (exe_dir / ".env").exists():
        return exe_dir

    return platform_root or exe_dir


# Root paths for asset management and persistence
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    # Running in a PyInstaller bundle
    ASSET_ROOT = Path(sys._MEIPASS)
    # Persist data in a stable app-data location for installed bundles, but keep
    # existing beside-exe data and dev dist runs working.
    exe_dir = Path(sys.executable).resolve().parent
    DATA_ROOT = _resolve_data_root(exe_dir)
else:
    # Running in a normal Python environment
    ASSET_ROOT = Path(__file__).resolve().parents[1]
    DATA_ROOT = ASSET_ROOT

ROOT = ASSET_ROOT  # Back-compat for internal asset lookups
TUNING_BACKLOG_PATH = DATA_ROOT / "docs" / "TUNING-BACKLOG.md"
ENV_PATH = DATA_ROOT / ".env"
# Analyst-accuracy evaluation log (hash-chained JSONL). Lives under DATA_ROOT so
# it survives packaged installs; excluded from distribution via the `data` ignore.
EVAL_LOG_PATH = DATA_ROOT / "data" / "eval" / "eval_log.jsonl"


def _is_frozen() -> bool:
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


def _legacy_user_data_dir() -> Path | None:
    """Pre-v0.29 writable path kept for one-time .env merge on upgrade."""
    if not _is_frozen():
        return None
    if sys.platform == "win32":
        base = Path(os.getenv("APPDATA", "~")).expanduser()
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.getenv("XDG_DATA_HOME", "~/.local/share")).expanduser()
    return base / "trade-hunter"


def _get_user_data_dir() -> Path:
    """Return the canonical writable directory for app data."""
    return DATA_ROOT


def _load_all_env_sources() -> None:
    """Load .env from DATA_ROOT, then merge missing/empty keys from the legacy path."""
    _load_env_file(ENV_PATH)
    legacy = _legacy_user_data_dir()
    if not legacy:
        return
    legacy_env = legacy / ".env"
    if legacy_env.resolve() != ENV_PATH.resolve():
        # fill_empty: a legacy value may fill a key the primary .env left MISSING
        # *or EMPTY*. Without this, an empty primary value (e.g. "KALSHI_MARKETS=")
        # would shadow the legacy value via setdefault — the bug that hid users'
        # watchlists after an upgrade.
        _load_env_file(legacy_env, fill_empty=True)


def _load_env_file(path: Path, *, fill_empty: bool = False) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if fill_empty and os.environ.get(key, "") == "":
            os.environ[key] = value
        else:
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


def build_setup_diagnostics(
    settings: "Settings",
    *,
    feed_state: dict[str, Any] | None = None,
    invalid_tickers: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Return sanitized setup/status diagnostics for buyer-visible surfaces."""
    diagnostics: list[dict[str, Any]] = []
    diagnostics.append({
        "category": "missing-credentials",
        "buyer_headline": "Credential setup status is available.",
        "support_detail": "Credential presence is reported as booleans only.",
        "details": _sanitize_runtime_value({
            "kalshi_api_key_id": bool(settings.kalshi_api_key_id),
            "kalshi_private_key_path": bool(settings.kalshi_private_key_path),
            "ingest_api_token": bool(settings.ingest_api_token),
            "polyalerthub_token": bool(settings.polyalerthub_token),
        }),
    })

    feeds = feed_state or {}
    diagnostics.append({
        "category": "feed-state",
        "buyer_headline": "Feed status is available.",
        "support_detail": "Runtime feed state is summarized without secrets.",
        "details": {
            name: {
                "running": bool(value.get("running")) if isinstance(value, dict) else False,
                "status": str(value.get("detail") or "unknown") if isinstance(value, dict) else "unknown",
            }
            for name, value in feeds.items()
        },
    })

    tickers = [str(ticker).upper() for ticker in (invalid_tickers or [])]
    diagnostics.append({
        "category": "invalid-tickers",
        "buyer_headline": "Ticker validation status is available.",
        "support_detail": "Invalid or expired tickers are reported by symbol only.",
        "details": {"count": len(tickers), "tickers": tickers},
    })

    diagnostics.append({
        "category": "discord-setup",
        "buyer_headline": "Discord alert setup status is available.",
        "support_detail": "Discord setup is summarized without webhook URLs.",
        "details": _sanitize_runtime_value({
            "discord_webhook_url": bool(settings.discord_webhook_url),
            "discord_webhook_routes": sorted(settings.discord_webhook_routes.keys()),
        }),
    })
    return diagnostics


def _persist_env_updates(updates: dict[str, str], env_path: Path | None = None) -> None:
    path = env_path or ENV_PATH
    path.parent.mkdir(parents=True, exist_ok=True)

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


# ── Watchlist (tracked tickers) storage ───────────────────────────────────────
# The tracked-ticker watchlist lives in its OWN file, decoupled from .env. Storing
# it in .env alongside credentials made it fragile: an empty KALSHI_MARKETS= line
# in the primary .env could shadow markets in the legacy .env (frozen-exe merge
# bug), and any .env corruption took the watchlist with it. watchlist.json is
# per-install runtime state like the database — updates never touch it.

def _default_watchlist_path() -> Path:
    # Derived from ENV_PATH at call time so tests that repoint ENV_PATH follow.
    return ENV_PATH.parent / "data" / "watchlist.json"


def _read_markets_line(env_path: Path) -> list[str]:
    """Read KALSHI_MARKETS directly from a .env file (bypasses env-var shadowing)."""
    if not env_path.exists():
        return []
    try:
        lines = env_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    for raw in lines:
        line = raw.strip()
        if line.startswith("KALSHI_MARKETS="):
            value = line.split("=", 1)[1].strip().strip('"').strip("'")
            return [m.strip().upper() for m in value.split(",") if m.strip()]
    return []


def _migrate_markets_from_env() -> list[str]:
    """One-time watchlist seed: gather KALSHI_MARKETS from the active .env and the
    legacy .env (order-preserving, de-duplicated). Reads the files directly so the
    env-var shadow bug can't hide markets during migration."""
    markets: list[str] = []
    seen: set[str] = set()
    sources = [ENV_PATH]
    legacy = _legacy_user_data_dir()
    if legacy:
        sources.append(legacy / ".env")
    for src in sources:
        for m in _read_markets_line(src):
            if m not in seen:
                seen.add(m)
                markets.append(m)
    return markets


def _read_watchlist_file(path: Path) -> list[str] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    markets = payload.get("markets") if isinstance(payload, dict) else payload
    if not isinstance(markets, list):
        return None
    return [str(m).strip().upper() for m in markets if str(m).strip()]


def _write_watchlist_file(markets: list[str], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"version": 1, "updated_at": datetime.now(UTC).isoformat(), "markets": list(markets)}
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)  # atomic


def load_watchlist(path: Path | None = None) -> list[str]:
    """Return the tracked-ticker watchlist. Source of truth is watchlist.json under
    DATA_ROOT/data/. On first run (no file) it is seeded ONCE from the .env
    KALSHI_MARKETS (active + legacy) so existing users keep their markets."""
    resolved = path or _default_watchlist_path()
    existing = _read_watchlist_file(resolved)
    # A NON-EMPTY watchlist file is authoritative. An empty (or missing) file
    # falls through to re-seed from .env — this makes the watchlist self-healing:
    # if the file is ever emptied (a bug, a race, a bad write), the markets are
    # recovered from .env on the next load rather than silently lost. The cost is
    # that a deliberately-empty watchlist re-seeds from .env; for a market-tracking
    # app, never-lose-markets is the right trade-off (clear .env to truly empty it).
    if existing:
        return existing
    seeded = _migrate_markets_from_env()
    # Only persist a NON-EMPTY seed (never write an empty file). Skip the write
    # under pytest for the default path so the suite never touches the developer's
    # real data/watchlist.json.
    if seeded and (path is not None or not os.getenv("PYTEST_CURRENT_TEST")):
        try:
            _write_watchlist_file(seeded, resolved)
        except OSError:
            pass
    return seeded


def save_watchlist(markets: list[str], path: Path | None = None) -> None:
    """Persist the tracked-ticker watchlist (replaces the old .env write)."""
    _write_watchlist_file(list(markets), path or _default_watchlist_path())


def persist_kalshi_markets(markets: list[str], env_path: Path | None = None) -> None:
    """Deprecated alias — the watchlist now lives in watchlist.json, not .env.
    Kept so existing callers/imports keep working; ``env_path`` is ignored."""
    save_watchlist(markets)


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
    # Trigger permission audits for the core configuration file layout context
    _check_file_permissions(ENV_PATH, ".env configuration file")
    _load_all_env_sources()

    # Resolve a relative KALSHI_PRIVATE_KEY_PATH against DATA_ROOT so the key
    # file is found regardless of the exe's working directory.  Customers can
    # put private_key.pem next to their .env and just write:
    #   KALSHI_PRIVATE_KEY_PATH=private_key.pem
    _raw_key_path = os.getenv("KALSHI_PRIVATE_KEY_PATH")
    if _raw_key_path:
        _key_path = Path(_raw_key_path)
        if not _key_path.is_absolute():
            resolved_key_path = (DATA_ROOT / _key_path).resolve()
            os.environ["KALSHI_PRIVATE_KEY_PATH"] = str(resolved_key_path)
            # Trigger permission audits for the resolved sensitive private key asset location
            _check_file_permissions(resolved_key_path, "Kalshi private key file")
        else:
            _check_file_permissions(_key_path, "Kalshi private key file")

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
        kalshi_markets=load_watchlist(),
        kalshi_api_key_id=os.getenv("KALSHI_API_KEY_ID") or os.getenv("KALSHI_API_KEY") or None,
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
        print(f"--- SECURITY NOTICE: Generated a new ADMIN_TOKEN and saved it to {ENV_PATH} ---")
        print("--- It is required for remote (non-loopback) dashboard access. ---")

    if not settings.ingest_api_token:
        import secrets
        token = secrets.token_urlsafe(32)
        env_updates["INGEST_API_TOKEN"] = token
        settings = Settings(**{**settings.__dict__, "ingest_api_token": token})
        print(f"--- SECURITY NOTICE: Generated a new INGEST_API_TOKEN and saved it to {ENV_PATH} ---")
        print("--- Use it for external alert webhooks (Bearer auth); see your .env. ---")

    if env_updates:
        _persist_env_updates(env_updates, env_path=ENV_PATH)

    return settings