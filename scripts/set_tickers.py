#!/usr/bin/env python3
"""
One-shot helper: writes KALSHI_MARKETS to whichever .env the running exe uses.
Run from the project root:  python scripts/set_tickers.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import ENV_PATH, persist_kalshi_markets

TICKERS = [
    "KXNEXTAG-29-JPIR",
    "KXIMPEACH-27-MAR01",
    "KXNEXTSPEAKER-31-HJEF",
    "KXTOPCHEF",
    "KXNEXTAG-29-TBLA",
    "KXTRUMPPARDONS-29JAN21-GMAX",
    "KXTRUMPPARDONS-29JAN21",
    "KXGREENTERRITORY-29",
    "KXIMPEACH-26-SEP01",
    "KXNEXTAG",
    "KXCPI",
    "KXGREENTERRITORY",
    "KXNEXTODNI",
    "KXNEXTSTATE",
    "KXTRUMPPARDONS",
    "KXFED",
    "KXTRUMPRESIGN",
    "KXGDP",
    "KXSCOTUSRESIGN",
    "KXIMPEACH",
    "KXCABOUT-26MAY22-SWIL",
]

print(f"Writing {len(TICKERS)} tickers to: {ENV_PATH}")
persist_kalshi_markets(TICKERS, env_path=ENV_PATH)
print("Done. Restart the exe to pick up the changes.")
