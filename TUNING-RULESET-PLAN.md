# Tuning Ruleset — Self-Improving Analyst Loop (Option A)

**Status:** Planning · not yet implemented
**Goal:** Turn the Tuning Advisor from "generates prose no code reads" into a real,
compounding loop where applied rules are appended to a persistent ruleset that the
Layer 1 analyst consults on every signal — so the app actually gets better at
identifying signals over time.

---

## The loop we're building

```
Layer 1 (Analyst)   reads each signal → produces readout, JUDGING against the ACTIVE RULESET
Layer 2 (Advisor)   reviews Layer 1 readouts → proposes a NEW rule (structured: id + text + scope)
Governor            checks the new rule vs the ACTIVE RULESET → clash / undo / duplicate?
[Apply] (Settings)  appends the rule to the ACTIVE RULESET + marks the TB item applied (real linkage)
Next signals        Layer 1 now judges with the larger ruleset → compounding improvement
Compaction (audit)  periodically merges/retires rules so the set stays small + cheap to inject
```

The **active ruleset** is the artifact that "gets smarter." It is natural-language
rules consumed by the Layer 1 analyst prompt — NOT the 3 detector floats.

---

## Design decisions (locked)

- **Consumer = Layer 1 analyst prompt** (Option A). The `SpikeDetector` stays a coarse
  candidate net; the *intelligence* lives in the accumulating analyst ruleset.
- **Rules are natural language** (the advisor already emits prose). We add lightweight
  structure around each rule (id, scope, provenance, status) for management + retrieval.
- **The 3-slider threshold tuning stays** as a separate coarse control. We are ADDING a
  ruleset layer, not removing the existing knobs.
- **Scale is a first-class requirement**, not a later optimization. We never inject the
  whole ruleset. We inject a bounded, scope-relevant subset. See Phase 4.

---

## Scale strategy — how we survive 1000s of rules

Three mechanisms, layered:

1. **Scoped retrieval (per-signal subset).** Every rule has a `scope`
   (`topic`: all/crypto/macro/elections/sports/geopolitics, `tier`: all/watch/notable/signal).
   A crypto signal only loads `topic=all + topic=crypto` rules. Per-call token cost is
   bounded by *relevant* rules, not total rules.
2. **Active-set cap + retirement.** The active set is capped (default 150, configurable).
   Rules carry `priority` and optional `hit_count`. When over cap, low-value/stale rules
   are retired (moved to the audit log, not deleted).
3. **Periodic compaction/audit (the "get-smaller" pass).** An LLM pass merges overlapping
   rules, marks redundant ones `superseded`, and flags contradictions for review. The
   Governor validates the compaction dropped no real constraint. Full history is preserved
   append-only; only the curated active set is ever injected.

Net effect: **injected tokens per analyst call stay roughly constant** no matter how large
the historical ruleset grows.

---

## Data model

### `data/tuning/active_rules.json` — the live ruleset (curated, capped)
```json
{
  "version": 1,
  "updated_at": "2026-07-02T...",
  "rules": [
    {
      "id": "RULE-0007",
      "text": "For volume_delta > 5000x baseline, require price_move >= 5%. For >1000x baseline, require >= 1%.",
      "scope": { "topic": "all", "tier": "all" },
      "source_tb": "TB-042",
      "created_at": "2026-07-02T...",
      "status": "active",
      "superseded_by": null,
      "priority": "normal",
      "hit_count": 0
    }
  ]
}
```

### `data/tuning/rules_audit.jsonl` — append-only provenance log
One JSON object per line, every lifecycle event:
`{ts, event: added|superseded|retired|merged|compacted, rule_id, detail, actor}`.
Never rewritten. This is the source of truth for "what happened and why."

Both live under `DATA_ROOT` (same durable location as `.env` / db), so they survive
restarts and packaged installs. They are dev/user state → **must be gitignored and
excluded from distribute.py** (same treatment as `.env`).

---

## Phased build

### Phase 1 — Ruleset store (foundation, no behavior change yet) ✅ DONE
- New module `app/ruleset.py`: load/save `active_rules.json`, append to `rules_audit.jsonl`,
  id allocation (`RULE-NNNN`), status transitions, cap enforcement stub.
- Pure functions + a thin store class. Fully unit-tested in isolation.
- **Done when:** can add/list/supersede/retire rules with provenance; round-trips to disk;
  100% of new store logic covered by tests.
- **DELIVERED:** `app/ruleset.py` (Rule/RuleScope/RulesetStore) + `tests/test_ruleset_store.py`
  (24 tests, all green). Includes scoped retrieval (`rules_for_scope`), cap+auto-retire,
  hit_count, atomic writes, corrupt-file resilience. `data/tuning/` added to `.gitignore` and
  `scripts/distribute.py` ignore set. NOTE: run tests with `/c/Python314/python -m pytest`
  (the project's pytest env; the Hermes venv has no pytest). 8 unrelated failures pre-exist in
  the suite (Py3.14 `re` backreference tightening + missing pykalshi module) — not caused by
  this phase.

### Phase 2 — Layer 1 consumes the ruleset ✅ DONE
- Modify `_build_prompt` (analyst.py) to inject the scope-relevant active rules for the
  signal being judged (topic + tier + "all").
- Add a bounded selector: cap injected rules, order by priority then recency.
- **Done when:** analyst prompt provably includes matching rules (assert via test double);
  empty ruleset behaves exactly like today (no regression).
- **DELIVERED:** `_scoped_rule_texts()` helper derives topic/tier from the signal and calls
  `store.rules_for_scope(topic, tier, limit=40)` (defensive: None store or any error → []).
  `_build_prompt(signal, flow, ruleset_rules=None)` injects an "APPLIED TUNING RULES" block
  before YOUR TASK — omitted entirely when empty so the prompt is BYTE-IDENTICAL to before
  (zero-regression test asserts none==[]==base). Threaded through `analyze_signal` +
  `SignalAnalyst(ruleset_store=...)`; `service.py` builds one shared `self.ruleset =
  RulesetStore()` and passes it in. Tests: `tests/test_analyst_ruleset.py` (10, green);
  full store+advisor suite still 40 green. Committed Phase 1 as cea24c8 first.

### Phase 3 — Layer 2 emits structured rules ✅ DONE
- Change the advisor output contract: alongside `suggested_thresholds`, emit a
  `proposed_rules` array (`{text, scope}`). Keep `recommendations` prose for display.
- Update `_build_tuning_prompt` + parsing in `analyze_tuning`.
- **Done when:** advisor returns structured proposed rules; prose still rendered; malformed
  LLM output degrades gracefully (no crash, logged).
- **DELIVERED:** `TuningAdvice` gained `proposed_rules: list[dict]` (in `to_dict` as
  `"proposed_rules"`, `[]` default). `_build_tuning_prompt` now asks for `proposed_rules`
  `[{text, scope{topic,tier}}]` with the topic/tier vocabulary spelled out. `analyze_tuning`
  parses via new `_normalize_proposed_rules(raw, limit=5)` — tolerant coercion: non-list→[],
  skips non-dict/empty-text items, clamps scope to `ruleset.VALID_TOPICS/VALID_TIERS`
  (defaults 'all'), lowercases, caps count; NEVER raises. Prose `recommendations` untouched.
  Tests: `tests/test_advisor_proposed_rules.py` (12, green); combined suite 62 green.

### Phase 4 — Governor reviews against the active ruleset 🔴
- `TuningGovernor.review` compares a proposed rule against the **active ruleset** (not just
  condensed backlog prose): detects clash / undo / duplicate, returns verdict + which
  RULE-id it conflicts with.
- Preserve existing threshold-conflict behavior.
- **Done when:** a rule that undoes RULE-0007 is rejected citing RULE-0007; a genuinely new
  rule passes; a near-duplicate is flagged as duplicate not conflict.

### Phase 5 — Apply endpoint appends to ruleset (closes the cosmetic-checkbox gap) 🟡
- `/api/config/apply-tuning` (or a new `/api/tuning/apply-rule`) appends the approved rule
  to the active set AND marks the originating TB item applied — one atomic action.
- This finally makes "mark applied" mean something: applied == in the active ruleset.
- **Done when:** clicking Apply adds the rule, logs to audit, flips the TB checkbox, and the
  next analyst call includes it — verified end to end.

### Phase 6 — Compaction / audit job 🔴
- `app/ruleset_compaction.py`: triggered when active count > cap OR on demand.
- LLM pass: merge overlapping, mark superseded, flag contradictions → proposes a smaller set.
- Governor validates no constraint dropped. Writes new active set; logs `compacted` events.
- Expose a manual "Audit ruleset now" button + show last-compaction summary.
- **Done when:** a 200-rule set with known overlaps compacts to a smaller set with zero lost
  constraints (fixture test); audit log records every merge.

### Phase 7 — Settings UI: make the invisible visible 🟡
- New "Active Ruleset" panel: list active rules (id, text, scope, source TB), count vs cap,
  last-compaction time. Read-only presence-style view (consistent with the app's other
  panels).
- Apply / reject actions wired to Phase 5. "Audit now" wired to Phase 6.
- **Done when:** the page reflects the *actual* ruleset the analyst is using — no more
  "looks like it works." What you see is what Layer 1 sees.

### Phase 7.5 — AI API key presence indicators (companion UX fix) 🟢
- Separate, pre-existing gap: the Settings page has NO field showing whether the agent-layer
  keys (`ANTHROPIC_API_KEY`, `PERPLEXITY_API_KEY`, and any future provider) are configured.
  Users can't tell if the analyst/advisor/governor layers are even powered.
- Add presence-only indicators (`configured` / `not set`) — NEVER show the actual key value.
- Backend: extend `serialize_settings()` `presence` block in `app/server.py` with
  `anthropic_api_key: bool(...)`, `perplexity_api_key: bool(...)`. `Settings` already reads
  these via `os.getenv` in `config.py`; just surface the booleans.
- Frontend: add a small "AI Analyst" settings section rendering the presence flags, mirroring
  the existing Kalshi/Discord presence pattern in `dashboard.js` (`formatPresenceLabel`).
- **Done when:** Settings shows configured/not-set for each AI provider key, actual keys never
  leave the backend, and the whole self-improving loop is finally legible end to end (keys →
  layers → ruleset).

### Phase 8 — Ship checks 🟢
- `.gitignore` + `distribute.py` exclude `data/tuning/` (dev/user state, may contain nothing
  sensitive but is per-install runtime data — treat like the db/.env).
- Cost guardrail test: injected-token estimate stays under a ceiling as ruleset scales to 1000.
- Full suite green; README/USER_GUIDE updated to describe the real loop honestly.

---

## Risks & open questions

- **Rule quality drift.** LLM-authored rules can be vague or contradictory. Mitigation:
  Governor gate + compaction + human Apply step (nothing auto-applies).
- **Scope mis-tagging.** If the advisor tags scope wrong, a rule may not load for the signals
  it should. Mitigation: default new rules to `topic=all` unless clearly specific; audit surfaces this.
- **hit_count is optional.** True usefulness tracking needs the analyst to report which rules
  it actually leaned on. Nice-to-have; can start with recency+priority only.
- **Still no ground-truth outcome loop.** This design makes the analyst *judgment* compound,
  but it does not yet learn from whether signals were profitable. That's a separate, later
  feature (outcome tracking). Worth naming so we don't over-claim again.

## TODO / investigations (non-blocking, track here)

- **[ ] Audit provider fallback in `service.py` + `AIProviderManager`.** Verify what actually
  happens when one of `ANTHROPIC_API_KEY` / `PERPLEXITY_API_KEY` is missing, invalid, rate-
  limited, or out of credits. Questions to answer: (1) Does `AIProviderManager` correctly
  reorder/skip a failing provider and fall back to the other? (2) Is a dead provider retried,
  and with what backoff? (3) When BOTH fail, does the analyst/advisor/governor degrade cleanly
  (analysis skipped, status surfaced) rather than crash or silently stall? (4) Does the
  ruleset loop behave sanely when the AI layer is fully down (no rules created, existing rules
  still injected, no exceptions)? Relevant code: `service.py:47-73` (key load + analyst/advisor
  construction), `AIProviderManager.get_ordered_providers` / `report_success` / `report_failure`
  / `health_status` in `analyst.py`. Likely a companion to Phase 7.5 (API-key presence UI) so
  the Settings page can show not just "configured" but "working / failing".

---

## What this explicitly does NOT do (honesty guardrails)

- Does not touch the detector's hardcoded scoring formula.
- Does not learn from trade outcomes (no ground truth in the loop yet).
- Does not auto-apply anything — every rule requires human Apply.
- The Settings page will state plainly what the loop does and doesn't do.

---

## Next effort (planned, after this ships): close the outcome loop

This ruleset feature makes the analyst's *judgment* compound. The NEXT feature makes the
whole system learn from reality:

```
signal fired → record it → observe outcome (was the predicted direction right? profitable?)
            → feed outcome stats back to Layer 2 → rules adjusted by EVIDENCE, not just LLM opinion
```

Prereqs to design in that effort:
- **Outcome tracking**: persist each signal with its prediction, then resolve it against the
  market's later price / settlement. Needs a resolver + storage.
- **Profitability metric**: define "was this signal good?" (directional accuracy, hypothetical
  PnL at signal time vs N minutes later, or settlement outcome).
- **Backtest harness**: replay historical signals against a candidate ruleset to measure
  win-rate BEFORE applying — so rule changes are validated, not guessed.
- Ties directly into `hit_count` / rule-value scoring from this plan (Phase 1 data model
  already reserves the field).

Target: the long-weekend session — build the testing/profitability plan first, then wire
outcomes back into the advisor so rules adjust on evidence.
