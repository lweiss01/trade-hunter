from __future__ import annotations

import argparse
from datetime import UTC, datetime

from .config import load_settings
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


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.smoke_test:
        return run_smoke_test()

    settings = load_settings()
    run_server(settings)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
