"""Tuning ruleset store — Phase 1 foundation.

Persistent, append-only-audited store for the self-improving analyst ruleset.
This module owns the *data*, not the behavior: it can add / list / scope-filter /
supersede / retire rules and record every lifecycle event. Later phases wire this
into the Layer 1 analyst prompt (consume), Layer 2 advisor (propose), Governor
(review), the apply endpoint, and compaction.

Design notes
------------
- Two files under ``<data_root>/data/tuning/``:
    active_rules.json  — curated, capped, live set (what the analyst will consult)
    rules_audit.jsonl  — append-only lifecycle log, never rewritten
- The store never hard-deletes a rule. Retiring/superseding flips status and logs
  the transition; history is preserved for audit + future outcome analysis.
- ``data_root`` is injectable so tests use a tmp dir and production uses DATA_ROOT.
- No LLM calls, no network, no app imports beyond config — keeps Phase 1 isolated
  and trivially testable.
"""

from __future__ import annotations

import json
import logging
import re
import threading
from dataclasses import dataclass, field, asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Literal

log = logging.getLogger(__name__)

# ── Vocabulary ────────────────────────────────────────────────────────────────
# Kept in sync with the detector/analyst topic + tier vocabulary.
VALID_TOPICS = ("all", "crypto", "macro", "elections", "sports", "geopolitics", "general")
VALID_TIERS = ("all", "watch", "notable", "signal", "whale-cluster")
VALID_PRIORITIES = ("low", "normal", "high")
VALID_STATUSES = ("active", "superseded", "retired")

RuleStatus = Literal["active", "superseded", "retired"]

DEFAULT_ACTIVE_CAP = 150
SCHEMA_VERSION = 1

_ID_RE = re.compile(r"RULE-(\d+)")


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


# ── Rule model ──────────────────────────────────────────────────────────────
@dataclass
class RuleScope:
    topic: str = "all"
    tier: str = "all"

    def normalized(self) -> "RuleScope":
        topic = self.topic if self.topic in VALID_TOPICS else "all"
        tier = self.tier if self.tier in VALID_TIERS else "all"
        return RuleScope(topic=topic, tier=tier)

    def to_dict(self) -> dict[str, str]:
        return {"topic": self.topic, "tier": self.tier}

    @classmethod
    def from_dict(cls, d: dict[str, Any] | None) -> "RuleScope":
        d = d or {}
        return cls(topic=str(d.get("topic", "all")), tier=str(d.get("tier", "all"))).normalized()


@dataclass
class Rule:
    id: str
    text: str
    scope: RuleScope = field(default_factory=RuleScope)
    source_tb: str | None = None
    created_at: str = field(default_factory=_now_iso)
    status: RuleStatus = "active"
    superseded_by: str | None = None
    priority: str = "normal"
    hit_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["scope"] = self.scope.to_dict()
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Rule":
        priority = d.get("priority", "normal")
        if priority not in VALID_PRIORITIES:
            priority = "normal"
        status = d.get("status", "active")
        if status not in VALID_STATUSES:
            status = "active"
        return cls(
            id=str(d["id"]),
            text=str(d.get("text", "")),
            scope=RuleScope.from_dict(d.get("scope")),
            source_tb=(str(d["source_tb"]) if d.get("source_tb") else None),
            created_at=str(d.get("created_at") or _now_iso()),
            status=status,  # type: ignore[arg-type]
            superseded_by=(str(d["superseded_by"]) if d.get("superseded_by") else None),
            priority=priority,
            hit_count=int(d.get("hit_count", 0) or 0),
        )


# ── Store ─────────────────────────────────────────────────────────────────────
class RulesetStore:
    """Disk-backed store for the tuning ruleset.

    Thread-safe for the simple mutations Phase 1 needs (a single process lock).
    All public mutators persist immediately and append an audit record.
    """

    def __init__(self, data_root: Path | str | None = None, *, active_cap: int = DEFAULT_ACTIVE_CAP) -> None:
        if data_root is None:
            from .config import DATA_ROOT  # lazy import so tests need not touch global config
            data_root = DATA_ROOT
        self.base_dir = Path(data_root) / "data" / "tuning"
        self.active_path = self.base_dir / "active_rules.json"
        self.audit_path = self.base_dir / "rules_audit.jsonl"
        self.active_cap = active_cap
        self._lock = threading.RLock()

    # ── persistence ────────────────────────────────────────────────────────
    def _ensure_dir(self) -> None:
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _load_raw(self) -> dict[str, Any]:
        if not self.active_path.exists():
            return {"version": SCHEMA_VERSION, "updated_at": None, "rules": []}
        try:
            payload = json.loads(self.active_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            # Corrupt or unreadable — treat as empty rather than crash the app.
            return {"version": SCHEMA_VERSION, "updated_at": None, "rules": []}
        if not isinstance(payload, dict):
            return {"version": SCHEMA_VERSION, "updated_at": None, "rules": []}
        payload.setdefault("version", SCHEMA_VERSION)
        payload.setdefault("rules", [])
        return payload

    def load(self) -> list[Rule]:
        """Return every rule on disk regardless of status."""
        with self._lock:
            raw = self._load_raw()
            rules: list[Rule] = []
            for item in raw.get("rules", []):
                if isinstance(item, dict) and item.get("id"):
                    try:
                        rules.append(Rule.from_dict(item))
                    except Exception:
                        continue
            return rules

    def _save(self, rules: Iterable[Rule]) -> None:
        self._ensure_dir()
        payload = {
            "version": SCHEMA_VERSION,
            "updated_at": _now_iso(),
            "rules": [r.to_dict() for r in rules],
        }
        tmp = self.active_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")
        tmp.replace(self.active_path)  # atomic swap

    def _audit(self, event: str, rule_id: str | None, detail: str, *, actor: str = "system") -> None:
        self._ensure_dir()
        record = {
            "ts": _now_iso(),
            "event": event,
            "rule_id": rule_id,
            "detail": detail,
            "actor": actor,
        }
        with self.audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, sort_keys=True) + "\n")

    def read_audit(self) -> list[dict[str, Any]]:
        if not self.audit_path.exists():
            return []
        out: list[dict[str, Any]] = []
        for line in self.audit_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return out

    # ── id allocation ────────────────────────────────────────────────────────
    def _next_id(self, existing: list[Rule]) -> str:
        highest = 0
        for r in existing:
            m = _ID_RE.fullmatch(r.id)
            if m:
                highest = max(highest, int(m.group(1)))
        return f"RULE-{highest + 1:04d}"

    # ── mutations ──────────────────────────────────────────────────────────
    def add_rule(
        self,
        text: str,
        *,
        scope: RuleScope | dict[str, Any] | None = None,
        source_tb: str | None = None,
        priority: str = "normal",
        actor: str = "system",
    ) -> Rule:
        """Append a new active rule, persist, audit, and enforce the cap."""
        text = (text or "").strip()
        if not text:
            raise ValueError("rule text cannot be empty")
        if priority not in VALID_PRIORITIES:
            priority = "normal"
        if isinstance(scope, dict):
            scope = RuleScope.from_dict(scope)
        elif scope is None:
            scope = RuleScope()
        else:
            scope = scope.normalized()

        with self._lock:
            rules = self.load()
            rule = Rule(
                id=self._next_id(rules),
                text=text,
                scope=scope,
                source_tb=source_tb,
                priority=priority,
            )
            rules.append(rule)
            self._save(rules)
            self._audit(
                "added",
                rule.id,
                f"scope={scope.topic}/{scope.tier} tb={source_tb or '-'} prio={priority}",
                actor=actor,
            )
            self._enforce_cap(actor=actor)
            return rule

    def _set_status(
        self,
        rule_id: str,
        status: RuleStatus,
        *,
        event: str,
        detail: str,
        superseded_by: str | None = None,
        actor: str = "system",
    ) -> Rule:
        with self._lock:
            rules = self.load()
            target = next((r for r in rules if r.id == rule_id), None)
            if target is None:
                raise ValueError(f"{rule_id} not found")
            target.status = status
            if superseded_by is not None:
                target.superseded_by = superseded_by
            self._save(rules)
            self._audit(event, rule_id, detail, actor=actor)
            return target

    def supersede_rule(self, rule_id: str, superseded_by: str, *, actor: str = "system") -> Rule:
        return self._set_status(
            rule_id,
            "superseded",
            event="superseded",
            detail=f"superseded_by={superseded_by}",
            superseded_by=superseded_by,
            actor=actor,
        )

    def retire_rule(self, rule_id: str, *, reason: str = "", actor: str = "system") -> Rule:
        return self._set_status(
            rule_id,
            "retired",
            event="retired",
            detail=reason or "retired",
            actor=actor,
        )

    def record_hit(self, rule_id: str) -> None:
        """Increment usefulness counter (used later by compaction + outcome loop)."""
        with self._lock:
            rules = self.load()
            target = next((r for r in rules if r.id == rule_id), None)
            if target is None:
                return
            target.hit_count += 1
            self._save(rules)

    # ── cap enforcement ────────────────────────────────────────────────────
    def _enforce_cap(self, *, actor: str = "system") -> None:
        """Retire lowest-value active rules when the active set exceeds the cap.

        Value ordering (kept simple in Phase 1; compaction in Phase 6 is smarter):
          keep higher priority, then more hits, then more recent.
        Retire the losers — never hard-delete.
        """
        rules = self.load()
        active = [r for r in rules if r.status == "active"]
        if len(active) <= self.active_cap:
            return

        prio_rank = {"high": 2, "normal": 1, "low": 0}
        # Sort best-first; the tail beyond the cap gets retired.
        active_sorted = sorted(
            active,
            key=lambda r: (prio_rank.get(r.priority, 1), r.hit_count, r.created_at),
            reverse=True,
        )
        to_retire = active_sorted[self.active_cap:]
        for r in to_retire:
            r.status = "retired"
        self._save(rules)
        for r in to_retire:
            self._audit("retired", r.id, "auto-retired: active cap exceeded", actor=actor)

    # ── compaction / dedup ────────────────────────────────────────────────────
    @staticmethod
    def _normalize_for_compact(text: str) -> str:
        return " ".join(text.lower().split())

    def compaction_candidate(self) -> dict[str, list[str]]:
        """Preview duplicate groups without mutating.

        Returns {normalized_text: [rule_id, ...]} for groups larger than 1.
        """
        rules = self.load()
        groups: dict[str, list[str]] = {}
        for r in rules:
            if r.status != "active":
                continue
            key = self._normalize_for_compact(r.text)
            groups.setdefault(key, []).append(r.id)
        return {k: v for k, v in groups.items() if len(v) > 1}

    def compact(self, *, actor: str = "system") -> dict[str, int]:
        """Retire active duplicate rules.

        For each active rule group sharing normalized text, keep the
        highest-value rule, retire the rest.

        Returns {"retired": N}. Never raises on IO issues.
        """
        retired = 0

        with self._lock:
            rules = self.load()
            active = [r for r in rules if r.status == "active"]
            groups: dict[str, list[Rule]] = {}
            for r in active:
                key = self._normalize_for_compact(r.text)
                groups.setdefault(key, []).append(r)

            for members in groups.values():
                if len(members) <= 1:
                    continue
                best = max(
                    members,
                    key=lambda r: (
                        {"high": 2, "normal": 1, "low": 0}.get(r.priority, 1),
                        r.hit_count,
                        r.created_at,
                    ),
                )
                for r in members:
                    if r.id == best.id:
                        continue
                    r.status = "retired"
                    retired += 1
                    self._audit("retired", r.id, "auto-retired: duplicate text", actor=actor)

            if retired:
                self._save(rules)

        return {"retired": retired}

    # ── queries ──────────────────────────────────────────────────────────────
    def active_rules(self) -> list[Rule]:
        return [r for r in self.load() if r.status == "active"]

    def rules_for_scope(
        self,
        topic: str | None = None,
        tier: str | None = None,
        *,
        limit: int | None = None,
    ) -> list[Rule]:
        """Return active rules relevant to a signal's topic + tier.

        A rule matches when its scope dimension is 'all' or equals the signal's.
        Ordered best-first (priority, hits, recency) so an optional ``limit``
        keeps the highest-value rules — this is the per-call token bound.
        """
        topic = topic if topic in VALID_TOPICS else None
        tier = tier if tier in VALID_TIERS else None

        def matches(r: Rule) -> bool:
            topic_ok = r.scope.topic == "all" or (topic is not None and r.scope.topic == topic)
            tier_ok = r.scope.tier == "all" or (tier is not None and r.scope.tier == tier)
            return topic_ok and tier_ok

        prio_rank = {"high": 2, "normal": 1, "low": 0}
        selected = [r for r in self.active_rules() if matches(r)]
        selected.sort(
            key=lambda r: (prio_rank.get(r.priority, 1), r.hit_count, r.created_at),
            reverse=True,
        )
        if limit is not None:
            selected = selected[:limit]
        return selected

    def counts(self) -> dict[str, int]:
        rules = self.load()
        return {
            "total": len(rules),
            "active": sum(1 for r in rules if r.status == "active"),
            "superseded": sum(1 for r in rules if r.status == "superseded"),
            "retired": sum(1 for r in rules if r.status == "retired"),
            "cap": self.active_cap,
        }
