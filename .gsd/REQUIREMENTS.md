# Requirements

This file is the explicit capability and coverage contract for the project.

## Active

### R001 — Expose detector tuning and apply-with-audit workflows that let operators adjust sensitivity safely.
- Class: functional
- Status: active
- Description: Expose detector tuning and apply-with-audit workflows that let operators adjust sensitivity safely.
- Why it matters: Thresholds need to adapt without turning the system into an opaque or fragile control panel.
- Source: ROADMAP.md Phase 5 / M004 / M005-M006
- Primary owning slice: tuning
- Supporting slices: M004,M005,M006,M007
- Validation: Tuning advisor, suggestion surfacing, and apply-tuning endpoint exist in project state, but requirement-level validation is not yet recorded.
- Notes: Corresponds to R010 referenced in milestone planning.

### R002 — Whale Detection: identify large-size position entries that deviate significantly from typical market trade size.
- Class: functional
- Status: active
- Description: Whale Detection: identify large-size position entries that deviate significantly from typical market trade size.
- Why it matters: Large positions often indicate informed flow or significant conviction, which is a high-value signal for traders.
- Source: user-request
- Validation: Whale signals appear in the dashboard and Discord when trades exceeding a dynamic threshold are detected.

## Traceability

| ID | Class | Status | Primary owner | Supporting | Proof |
|---|---|---|---|---|---|
| R001 | functional | active | tuning | M004,M005,M006,M007 | Tuning advisor, suggestion surfacing, and apply-tuning endpoint exist in project state, but requirement-level validation is not yet recorded. |
| R002 | functional | active | none | none | Whale signals appear in the dashboard and Discord when trades exceeding a dynamic threshold are detected. |

## Coverage Summary

- Active requirements: 2
- Mapped to slices: 2
- Validated: 0
- Unmapped active requirements: 0
