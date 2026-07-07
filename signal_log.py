"""
signal_log.py -- tamper-evident, append-only evaluation log for Trade Hunter.

Two record types, each written exactly ONCE, never mutated:

  1. "signal"     frozen at signal time T (the agent's view + the market's view)
  2. "resolution" written later, references the signal by id

You join them at scoring time. Because the frozen signal record is never
touched again, the numbers the test depends on (agent_prob, market price at T)
cannot be contaminated by anything that happens after the outcome is known.

Records are hash-chained: each carries the previous record's hash. Any edit,
reorder, or deletion after the fact breaks verify_chain(). That is your chain
of custody. A score is only trustworthy if the inputs provably were not
touched after the outcome was known.

Stdlib only. Drop it in the repo, no dependencies.

Units, stated once so nothing is ambiguous:
  agent_prob        float in [0.0, 1.0]      probability the market resolves YES
  *_bid / *_ask     int cents in [0, 100]    Kalshi book, implied prob = cents/100
  market_yes_price  int cents in [0, 100]    fallback last/mark when no book
  outcome           1 (YES), 0 (NO), or "void"
"""

from __future__ import annotations

import hashlib
import json
import threading
import time
import uuid
from pathlib import Path
from typing import Iterator, Optional

SCHEMA_VERSION = 1
GENESIS_HASH = "0" * 64

# benchmark_type tells the scorer what to compare the agent against.
#   "kalshi_price" -> beat the market's implied probability (price / 100)
#   "no_change"    -> directional call on a non-probability ticker
#   "custom"       -> you supply the baseline in the scorer
VALID_BENCHMARKS = {"kalshi_price", "no_change", "custom"}


def _utc_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _canonical(payload: dict) -> str:
    # Deterministic serialization so the hash is stable across machines.
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _hash_record(payload: dict, prev_hash: str) -> str:
    h = hashlib.sha256()
    h.update(_canonical(payload).encode("utf-8"))
    h.update(prev_hash.encode("utf-8"))
    return h.hexdigest()


class SignalLog:
    """Append-only JSONL log with a SHA-256 hash chain."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Serializes _append: the app writes signal records from multiple analyst
        # daemon threads (and resolution records from the resolver thread).
        # Concurrent appends would race on _last_hash and break the hash chain,
        # which the scorer treats as a tampered log and refuses to score.
        self._lock = threading.Lock()
        self._last_hash = self._read_tail_hash()

    def _read_tail_hash(self) -> str:
        if not self.path.exists() or self.path.stat().st_size == 0:
            return GENESIS_HASH
        last = None
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    last = line
        if last is None:
            return GENESIS_HASH
        return json.loads(last)["record_hash"]

    def _append(self, payload: dict) -> dict:
        # payload must NOT yet contain prev_hash / record_hash.
        # The read of _last_hash, the file append, and the update of _last_hash
        # must be one atomic unit or the chain forks under concurrent writers.
        with self._lock:
            payload = dict(payload)
            payload["prev_hash"] = self._last_hash
            payload["record_hash"] = _hash_record(payload, self._last_hash)
            with self.path.open("a", encoding="utf-8") as f:
                f.write(_canonical(payload) + "\n")
            self._last_hash = payload["record_hash"]
            return payload

    # -- writers -----------------------------------------------------------

    def log_signal(
        self,
        *,
        market_id: str,
        agent_prob: Optional[float],
        agent_action: Optional[str],
        benchmark_type: str = "kalshi_price",
        market_yes_bid: Optional[int] = None,
        market_yes_ask: Optional[int] = None,
        market_yes_price: Optional[int] = None,
        market_title: Optional[str] = None,
        category: Optional[str] = None,
        agent_confidence: Optional[float] = None,
        agent_version: Optional[str] = None,
        agent_rationale: Optional[str] = None,
        volume: Optional[int] = None,
        open_interest: Optional[int] = None,
        ts_signal: Optional[str] = None,
    ) -> str:
        """Record a signal, frozen at T. Returns the event_id (use it to
        attach the resolution later). Validates ranges so garbage never
        enters the log, because garbage in the log poisons every score."""
        if benchmark_type not in VALID_BENCHMARKS:
            raise ValueError(f"benchmark_type must be one of {VALID_BENCHMARKS}")
        if agent_prob is not None and not (0.0 <= agent_prob <= 1.0):
            raise ValueError("agent_prob must be in [0.0, 1.0]")
        for name, cents in (
            ("market_yes_bid", market_yes_bid),
            ("market_yes_ask", market_yes_ask),
            ("market_yes_price", market_yes_price),
        ):
            if cents is not None and not (0 <= cents <= 100):
                raise ValueError(f"{name} must be int cents in [0, 100]")
        if benchmark_type == "kalshi_price" and (
            market_yes_bid is None
            and market_yes_ask is None
            and market_yes_price is None
        ):
            raise ValueError(
                "kalshi_price benchmark needs at least one market price at T"
            )

        payload = {
            "event_id": uuid.uuid4().hex,
            "event_type": "signal",
            "schema_version": SCHEMA_VERSION,
            "ts_signal": ts_signal or _utc_iso(),
            "market_id": market_id,
            "market_title": market_title,
            "category": category,
            "benchmark_type": benchmark_type,
            "agent_prob": agent_prob,
            "agent_action": agent_action,
            "agent_confidence": agent_confidence,
            "agent_version": agent_version,
            "agent_rationale": agent_rationale,
            "market_yes_bid": market_yes_bid,
            "market_yes_ask": market_yes_ask,
            "market_yes_price": market_yes_price,
            "volume": volume,
            "open_interest": open_interest,
        }
        return self._append(payload)["event_id"]

    def log_resolution(
        self,
        *,
        signal_event_id: str,
        market_id: str,
        outcome,  # 1, 0, or "void"
        resolution_source: str = "kalshi_settlement",
        ts_resolve: Optional[str] = None,
    ) -> str:
        """Record how a market settled, as a NEW row that points back at the
        signal. The signal row is never edited."""
        if outcome not in (0, 1, "void"):
            raise ValueError("outcome must be 1, 0, or 'void'")
        payload = {
            "event_id": uuid.uuid4().hex,
            "event_type": "resolution",
            "schema_version": SCHEMA_VERSION,
            "signal_event_id": signal_event_id,
            "market_id": market_id,
            "ts_resolve": ts_resolve or _utc_iso(),
            "outcome": outcome,
            "resolution_source": resolution_source,
        }
        return self._append(payload)["event_id"]

    # -- readers -----------------------------------------------------------

    def _iter_records(self) -> Iterator[dict]:
        if not self.path.exists():
            return
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield json.loads(line)

    def verify_chain(self) -> bool:
        """Return True iff the hash chain is intact end to end. A False here
        means the log was edited, reordered, or truncated after writing, and
        any score computed from it should NOT be trusted."""
        prev = GENESIS_HASH
        for rec in self._iter_records():
            stated = rec.get("record_hash")
            # Rehash exactly what _append hashed: the whole record minus
            # record_hash (prev_hash stays in), plus the running prev hash.
            payload = {k: v for k, v in rec.items() if k != "record_hash"}
            if payload.get("prev_hash") != prev:
                return False
            if _hash_record(payload, prev) != stated:
                return False
            prev = stated
        return True

    def load_scored_pairs(self, drop_void: bool = True) -> list[dict]:
        """Join signals to their resolutions and emit exactly what the Step 4-5
        scorer needs: agent_prob, the market benchmark, the ask (for honest
        P&L), the outcome, and category (for stratification).

        A signal with no resolution yet is skipped (still pending)."""
        signals: dict[str, dict] = {}
        resolutions: dict[str, dict] = {}
        for rec in self._iter_records():
            if rec["event_type"] == "signal":
                signals[rec["event_id"]] = rec
            elif rec["event_type"] == "resolution":
                # last resolution wins if a market were ever re-settled
                resolutions[rec["signal_event_id"]] = rec

        pairs = []
        for sid, sig in signals.items():
            res = resolutions.get(sid)
            if res is None:
                continue  # unresolved, not scorable yet
            if drop_void and res["outcome"] == "void":
                continue

            bid = sig.get("market_yes_bid")
            ask = sig.get("market_yes_ask")
            last = sig.get("market_yes_price")
            mid_cents = None
            if bid is not None and ask is not None:
                mid_cents = (bid + ask) / 2.0
            elif last is not None:
                mid_cents = float(last)

            pairs.append(
                {
                    "signal_event_id": sid,
                    "market_id": sig["market_id"],
                    "category": sig.get("category"),
                    "benchmark_type": sig["benchmark_type"],
                    "agent_prob": sig.get("agent_prob"),
                    "agent_action": sig.get("agent_action"),
                    # market implied prob at T = mid / 100
                    "market_prob": (mid_cents / 100.0) if mid_cents is not None else None,
                    # you BUY at the ask; this is what makes P&L honest
                    "entry_ask_cents": ask if ask is not None else last,
                    "spread_cents": (ask - bid) if (bid is not None and ask is not None) else None,
                    "outcome": res["outcome"],
                    "ts_signal": sig["ts_signal"],
                    "ts_resolve": res["ts_resolve"],
                    "agent_version": sig.get("agent_version"),
                }
            )
        return pairs

    def pending_signals(self) -> list[dict]:
        """Return signal records that have no resolution yet, oldest first.

        The resolver polls these for settlement. Reads from the log itself, not
        the events table, because event retention deletes rows long before some
        markets settle."""
        signals: list[dict] = []
        resolved: set[str] = set()
        for rec in self._iter_records():
            if rec["event_type"] == "signal":
                signals.append(rec)
            elif rec["event_type"] == "resolution":
                resolved.add(rec["signal_event_id"])
        return [s for s in signals if s["event_id"] not in resolved]

    def pending_market_ids(self) -> set[str]:
        """market_ids that currently have an unresolved signal.

        Used to enforce the pre-registered "log only the first unresolved signal
        per market" policy: a market already open in the log is not re-logged
        until it resolves."""
        return {s["market_id"] for s in self.pending_signals()}


if __name__ == "__main__":
    # Tiny smoke test you can run: python signal_log.py
    log = SignalLog("eval_log.jsonl")
    sid = log.log_signal(
        market_id="KX-DEMO-2026",
        market_title="Demo market resolves YES",
        category="politics",
        agent_prob=0.72,
        agent_action="buy_yes",
        agent_version="th-agent-0.4.1",
        market_yes_bid=60,
        market_yes_ask=63,
        volume=1500,
        open_interest=8000,
    )
    log.log_resolution(signal_event_id=sid, market_id="KX-DEMO-2026", outcome=1)
    print("chain intact:", log.verify_chain())
    print("scored pairs:", log.load_scored_pairs())