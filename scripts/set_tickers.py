#!/usr/bin/env python3
"""
One-shot helper: writes the tracked-ticker watchlist that the running exe uses.
Run from the project root:  python scripts/set_tickers.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import save_watchlist, _default_watchlist_path

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

print(f"Writing {len(TICKERS)} tickers to: {_default_watchlist_path()}")
save_watchlist(TICKERS)
print("Done. Restart the exe to pick up the changes.")
