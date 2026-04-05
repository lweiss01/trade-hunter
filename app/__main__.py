from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime

from .config import Settings, load_settings
from .models import MarketEvent
from .server import run_server
from .service import TradeHunterService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Trade Hunter local dashboard")
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Inject a short fake sequence and verify the detector produces output.",
    )
    return parser


def run_smoke_test() -> int:
    service = TradeHunterService(load_settings())
    base = datetime.now(UTC)
    samples = [
        MarketEvent(
            source="smoke-test",
            platform="kalshi",
            market_id="smoke-btc",
            title="BTC above 110k by year end",
            yes_price=0.43,
            volume=100,
            volume_kind="cumulative",
            timestamp=base,
        ),
        MarketEvent(
            source="smoke-test",
            platform="kalshi",
            market_id="smoke-btc",
            title="BTC above 110k by year end",
            yes_price=0.45,
            volume=170,
            volume_kind="cumulative",
            timestamp=base,
        ),
        MarketEvent(
            source="smoke-test",
            platform="kalshi",
            market_id="smoke-btc",
            title="BTC above 110k by year end",
            yes_price=0.53,
            volume=420,
            volume_kind="cumulative",
            timestamp=base,
        ),
    ]

    signals = 0
    for event in samples:
        if service.ingest_event(event):
            signals += 1

    state = service.dashboard_state()
    print(
        f"Smoke test complete: markets={len(state['markets'])} "
        f"signals={len(state['signals'])} triggered={signals}"
    )
    return 0 if signals else 1


def _probe_host(settings: Settings) -> str:
    host = (settings.host or "127.0.0.1").strip()
    if host in {"0.0.0.0", "::", ""}:
        return "127.0.0.1"
    return host


def _app_url(settings: Settings, path: str) -> str:
    return f"http://{_probe_host(settings)}:{settings.port}{path}"


def _read_json(url: str, *, method: str = "GET", timeout: float = 1.5) -> dict | None:
    request = urllib.request.Request(url, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8") or "{}")
    except (
        urllib.error.URLError,
        TimeoutError,
        json.JSONDecodeError,
        ConnectionResetError,
        ConnectionAbortedError,
        BrokenPipeError,
    ):
        return None


def _existing_trade_hunter_running(settings: Settings) -> bool:
    payload = _read_json(_app_url(settings, "/api/settings"))
    return isinstance(payload, dict) and isinstance(payload.get("settings"), dict)


def _request_existing_instance_shutdown(settings: Settings) -> bool:
    payload = _read_json(_app_url(settings, "/api/admin/shutdown"), method="POST")
    return bool(payload and payload.get("ok"))


def _wait_for_existing_instance_to_exit(settings: Settings, *, timeout_seconds: float = 8.0) -> bool:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        if not _existing_trade_hunter_running(settings):
            return True
        time.sleep(0.2)
    return False


def _replace_existing_local_instance(settings: Settings) -> None:
    if not _existing_trade_hunter_running(settings):
        return

    location = f"{_probe_host(settings)}:{settings.port}"
    print(f"Trade Hunter already running at {location}; requesting shutdown before restart.")

    shutdown_acknowledged = _request_existing_instance_shutdown(settings)
    if not shutdown_acknowledged and not _wait_for_existing_instance_to_exit(settings, timeout_seconds=2.5):
        raise RuntimeError(
            "Trade Hunter is already running, but the existing instance did not accept a scoped shutdown request. "
            "Stop the old instance manually before retrying."
        )

    if not _wait_for_existing_instance_to_exit(settings):
        raise RuntimeError(
            "Trade Hunter shutdown was requested, but the existing instance did not release the port in time. "
            "Stop the old instance manually before retrying."
        )

    print(f"Previous Trade Hunter instance at {location} stopped cleanly.")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.smoke_test:
        return run_smoke_test()

    settings = load_settings()
    try:
        _replace_existing_local_instance(settings)
    except RuntimeError as exc:
        print(str(exc))
        return 1
    run_server(settings)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
