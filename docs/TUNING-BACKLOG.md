# Tuning Backlog

Last updated: 2026-04-03

This file is the durable backlog for detector-tuning recommendations surfaced by the AI analyst and tuning advisor.

Status values:
- `planned` — accepted but not implemented yet
- `applied` — implemented in code
- `rejected` — intentionally not taking this suggestion
- `superseded` — replaced by a newer or better rule

---

## 2026-04-03 — Advisor snapshot A

### Summary
The detector is flagging massive volume spikes (100x–1600x multipliers) with zero price movement across multiple markets, indicating it captures order-book churn and liquidity provision rather than conviction-shifting information flow. Nearly all false positives share `priceΔ = 0.0`, suggesting the volume-only signal is decoupled from market impact.

### Best next tweak
Implement a mandatory minimum price-move threshold (`±0.5%` for liquid markets, `±1–5%` for illiquid/ultra-low-price markets) as a kill-switch for all volume-spike alerts.

### Recommendations

- [x] **TB-001** `applied` — Add minimum price-move gate for `notable` alerts.
  - Rule: reject `notable` promotion unless `|priceΔ| >= 0.5%`.
  - Notes: already implemented in `app/detector.py` via `notable_min_price_move = 0.005` inside `_tier()`, with coverage in `tests/test_detector_migration.py` (`test_notable_requires_half_percent_absolute_price_move`, `test_notable_promotes_once_half_percent_price_move_is_met`).

- [ ] **TB-002** `planned` — Extend minimum price-move gate to `watch` alerts.
  - Rule: reject `watch` alerts unless `|priceΔ| >= 0.5%` for liquid markets.
  - Notes: advisor now recommends this should apply to both `watch` and `notable`; not implemented yet.

- [x] **TB-003** `applied` — Add special stricter gating for illiquid or ultra-low-price markets.
  - Rule: require `|priceΔ| >= 2%` when `yes_price <= 0.01` or `liquidity <= 1000`.
  - Notes: implemented in `app/detector.py` via `_required_price_move()`. Ultra-low-price and low-liquidity markets now keep a stricter minimum move floor before alerting. Covered in `tests/test_detector_migration.py`.

- [x] **TB-004** `applied` — Add ultra-thin market volume rule.
  - Rule: if `volΔ < 500` or `yes_price <= 0.01`, require `100x+` volume multiplier or executed trades > 0 before alerting.
  - Notes: implemented in `app/detector.py` via `_ultra_thin_market_ok()`. Quote-only ultra-thin spikes below `100x` baseline are suppressed, while executed trades can still alert. Covered in `tests/test_detector_migration.py`.

- [x] **TB-005** `applied` — Add order-flow coherence check.
  - Rule: reject alerts where side-specific trade flow and price direction disagree, or where balanced/quote-only weak-price volume spikes lack confirming flow.
  - Notes: implemented in `app/detector.py` via `_trade_flow_is_coherent()` plus the existing directional-flow gating. Current trade-side and dominant recent flow now have to agree with price direction for alerts to emit. Covered in `tests/test_detector_migration.py`.

---

## 2026-04-03 — Advisor snapshot B

### Summary
Watch-tier alerts are firing on volume spikes without sufficient price conviction or directional trade confirmation, generating noise in balanced or low-momentum markets.

### Best next tweak
Implement a composite gate requiring either meaningful price movement (`>= 1–2%` for watch tier) OR sustained directional bias in recent trades, rather than triggering on volume delta alone.

### Recommendations

- [ ] **TB-006** `planned` — Add higher watch-tier minimum move when volume is weak relative to baseline.
  - Rule: for `watch`, require `1–2%` price move when `volΔ < 2x baseline`; require `5–6%` if `volΔ` is only `1.2x baseline`.
  - Notes: overlaps with TB-002 and may supersede it once implemented.

- [x] **TB-007** `applied` — Add directional trade-flow confirmation.
  - Rule: require `>60%` of recent trades to lean one side before escalating balanced volume spikes.
  - Notes: implemented in `app/detector.py`. Weak-price outlier alerts (`price_move < 1%`) now require either meaningful repricing (`>= 1%`) or directional trade confirmation (`> 60%` dominant recent trade-side share`) to emit. Balanced directional flow and quote-only weak outliers no longer alert on volume alone. Covered in `tests/test_detector_migration.py`.

- [ ] **TB-008** `planned` — Increase watch-tier volume multiple requirement.
  - Rule: only alert on `volΔ > 3x baseline` at watch tier, or require `volΔ > 1.5x` paired with `priceΔ > 1%`.
  - Notes: may be better as a config knob rather than hardcoded.

---

## Applied changes

- [x] **AP-001** `applied` — Added Claude/Perplexity signal analyst to classify individual spikes as `signal`, `noise`, or `uncertain` and provide threshold notes inline on signal cards.
- [x] **AP-002** `applied` — Added tuning advisor second pass to summarize recent false-positive patterns and recommend threshold changes.
- [x] **AP-003** `applied` — Added durable manual backlog file (`docs/TUNING-BACKLOG.md`) so advisor recommendations are not lost when the live panel changes.
- [x] **AP-004** `applied` — Added the first explicit apply-advice path: `POST /api/config/apply-tuning`, `.env` persistence for detector thresholds, and a dashboard **Apply recommended tweak** control.
  - Notes: covered by unit tests and verified live on the negative path (`no tuning suggestions available`). Clean live positive-path verification still depends on the running app currently exposing structured `tuning_advisor.suggested_thresholds`.

---

## Next recommended implementation order

1. **TB-008** — baseline/multiplier tightening for thin markets
2. **TB-006** — higher watch-tier minimum move when volume is weak relative to baseline
3. **TB-002** — extend the minimum price-move gate to more watch-tier cases
4. Apply-advice follow-through — live success-path verification / visible audit message when current advisor suggestions are present
