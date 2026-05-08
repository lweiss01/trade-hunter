from __future__ import annotations

import os
import signal
import subprocess
import sys
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
            event_kind="trade",
            yes_price=0.43,
            volume=100,
            volume_kind="cumulative",
            trade_size=100,
            trade_side="buy",
            timestamp=base,
        ),
        MarketEvent(
            source="smoke-test",
            platform="kalshi",
            market_id="smoke-btc",
            title="BTC above 110k by year end",
            event_kind="trade",
            yes_price=0.45,
            volume=170,
            volume_kind="cumulative",
            trade_size=70,
            trade_side="buy",
            timestamp=base,
        ),
        MarketEvent(
            source="smoke-test",
            platform="kalshi",
            market_id="smoke-btc",
            title="BTC above 110k by year end",
            event_kind="trade",
            yes_price=0.53,
            volume=420,
            volume_kind="cumulative",
            trade_size=250,
            trade_side="buy",
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
    payload = _read_json(_app_url(settings, "/api/health"))
    return isinstance(payload, dict) and payload.get("app") == "trade-hunter"


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




def _get_pid_holding_port(port: int) -> int | None:
    if sys.platform == "win32" or sys.platform == "cygwin" or sys.platform == "msys":
        # Windows-specific: Suppress terminal window flicker
        CREATE_NO_WINDOW = 0x08000000
        cmd = "netstat"
        try:
            subprocess.run(["where", "netstat"], capture_output=True, check=True, creationflags=CREATE_NO_WINDOW)
        except (subprocess.CalledProcessError, FileNotFoundError):
            cmd = os.path.join(os.environ.get("windir", r"C:\Windows"), "System32", "netstat.exe")
        
        try:
            output = subprocess.check_output([cmd, "-ano"], creationflags=CREATE_NO_WINDOW).decode()
            for line in output.splitlines():
                if f":{port}" in line and "LISTEN" in line:
                    parts = line.strip().split()
                    if parts:
                        return int(parts[-1])
        except Exception:
            pass
    else:
        try:
            output = subprocess.check_output(["lsof", "-t", "-i", f":{port}"]).decode()
            if output.strip():
                return int(output.strip().split()[0])
        except Exception:
            pass
    return None

def _force_kill_pid(pid: int) -> None:
    try:
        os.kill(pid, signal.SIGTERM)
    except Exception:
        pass


def _replace_existing_local_instance(settings: Settings) -> None:
    location = f"{_probe_host(settings)}:{settings.port}"
    
    # Check if someone holds the port (even if it's hung and not answering /api/settings)
    pid = _get_pid_holding_port(settings.port)
    if not pid and not _existing_trade_hunter_running(settings):
        return

    print(f"Trade Hunter (or another process) is using {location}; attempting cleanup before restart.")

    if _existing_trade_hunter_running(settings):
        shutdown_acknowledged = _request_existing_instance_shutdown(settings)
        if shutdown_acknowledged and _wait_for_existing_instance_to_exit(settings, timeout_seconds=4.0):
            print("Previous Trade Hunter instance stopped cleanly.")
            return

    # If we get here, either it didn't acknowledge shutdown, it didn't exit in time,
    # or it's hung and not responding to HTTP at all.
    pid = _get_pid_holding_port(settings.port)
    if pid:
        print(f"Process {pid} is blocking the port. Forcing termination...")
        _force_kill_pid(pid)
        # Wait a moment for it to exit
        deadline = time.time() + 3.0
        while time.time() < deadline:
            if not _get_pid_holding_port(settings.port):
                print(f"Process {pid} terminated successfully.")
                return
            time.sleep(0.2)

        raise RuntimeError(
            f"Process {pid} is stubbornly holding the port. "
            "Stop the old instance manually before retrying."
        )
    else:
        # Check if the port freed up magically
        if not _existing_trade_hunter_running(settings) and not _get_pid_holding_port(settings.port):
            return
        raise RuntimeError(
            "The port is blocked but the owning process cannot be identified. "
            "Stop the old instance manually before retrying."
        )


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
    restart_requested = run_server(settings)
    return 3 if restart_requested else 0


if __name__ == "__main__":
    raise SystemExit(main())
