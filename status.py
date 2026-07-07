"""status.py -- accrual monitor for the Trade Hunter eval log.

Read-only. Intentionally does NOT modify score.py or signal_log.py, so the
scorer hash pinned in EVAL_PREREGISTRATION.md stays valid. Run any time:

    python status.py eval_log.jsonl

Tells you how many resolved, scorable pairs you have and how far you are from
the 30 (first honest read) and 100 (publish minimum) gates.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone

from signal_log import SignalLog

GATES = (30, 100)


def _age_days(iso):
    try:
        t = datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - t).total_seconds() / 86400.0
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description="Eval log accrual status.")
    ap.add_argument("log", help="path to eval_log.jsonl")
    args = ap.parse_args()

    log = SignalLog(args.log)
    chain_ok = log.verify_chain()

    signals, resolved_ids, voids = {}, set(), 0
    for rec in log._iter_records():
        if rec["event_type"] == "signal":
            signals[rec["event_id"]] = rec
        elif rec["event_type"] == "resolution":
            resolved_ids.add(rec["signal_event_id"])
            if rec.get("outcome") == "void":
                voids += 1

    pairs = log.load_scored_pairs()  # resolved, non-void, scorable
    n_pairs, n_signals = len(pairs), len(signals)
    pending = [s for sid, s in signals.items() if sid not in resolved_ids]
    ages = [a for a in (_age_days(s["ts_signal"]) for s in pending) if a is not None]

    print("=" * 52)
    print("TRADE HUNTER -- EVAL ACCRUAL STATUS")
    print("=" * 52)
    print(f"hash chain:          {'OK' if chain_ok else 'BROKEN (do not score)'}")
    print(f"signals logged:      {n_signals}")
    print(f"resolved & scorable: {n_pairs}")
    print(f"voided (dropped):    {voids}")
    print(f"still pending:       {len(pending)}")
    if ages:
        print(f"oldest pending:      {max(ages):.0f} days")
    print("-" * 52)
    for g in GATES:
        if n_pairs >= g:
            print(f"gate {g:>3}: REACHED ({n_pairs})")
        else:
            print(f"gate {g:>3}: {n_pairs}/{g}  ({g - n_pairs} more to go)")
    print("=" * 52)
    if len(pending) and not any(sid in resolved_ids for sid in signals):
        print("Note: 0 resolutions recorded. If markets have settled, check your")
        print("resolver is polling Kalshi and calling log_resolution().")


if __name__ == "__main__":
    main()
