# Tuning Backlog

Last updated: 2026-04-05

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

- [x] **TB-002** `applied` — Extend minimum price-move gate to `watch` alerts.
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


## 2026-04-05 — Advisor snapshot C

### Summary
Low-liquidity markets are generating false positives via quote-stacking and single small trades triggering disproportionate scores despite minimal price moves (2-3%) and modest volume deltas.

### Next step
Require either minimum trade size as a percentage of quote volume (5-10%) OR multiple consecutive same-direction trades before scoring, to distinguish real flow from quote-manipulation artifacts.

### Suggested thresholds
`min_volume_delta` → `150000.0`, `min_price_move` → `0.04`, `score_threshold` → `3.0`

### Recommendations

- [ ] **TB-009** `planned` — Add rule: exclude trades smaller than 5% of best-bid/ask quote volume from spike score contribution
- [ ] **TB-010** `planned` — Add rule: require 2+ consecutive trades in same direction within 2-3 seconds to qualify for spike scoring
- [ ] **TB-011** `planned` — Raise spike_min_price_move from 0.03 to 0.04 (4%) to filter marginal moves in low-liquidity pairs

---

## 2026-04-05 — Advisor snapshot D

### Summary
Low-liquidity niche markets are generating false positives from small absolute volume swings and modest price moves that lack genuine directional conviction. Both recent signals show thin baseline volumes with marginal price deltas that don't reflect market-moving information.

### Next step
Introduce a liquidity-gated threshold system: require minimum absolute volume baseline (e.g., 1000+ contracts) before applying relative delta rules, and scale price-move thresholds inversely with baseline liquidity (thin markets need >5% moves, deep markets can trigger at 2-3%).

### Suggested thresholds
`min_volume_delta` → `1000.0`, `score_threshold` → `2.5`

### Recommendations

- [ ] **TB-012** `planned` — Add absolute volume floor: skip detection entirely if baseline_volume < 1000 contracts, regardless of relative delta
- [ ] **TB-013** `planned` — Implement liquidity-aware price thresholds: require priceΔ > 5% for markets with <20k baseline volume, priceΔ > 3% for 20k-100k, priceΔ > 2% for >100k
- [ ] **TB-014** `planned` — Raise spike_min_volume_delta to 800-1000 for all markets as floor, then apply percentage-of-baseline multipliers (e.g., 15-20% delta on thin markets vs. 10% on deep markets)

---

## 2026-04-05 — Advisor snapshot E

### Summary
Low-liquidity political markets are generating false positives on small absolute volume swings and modest price moves that lack meaningful directional conviction. Relative volume deltas alone are insufficient filters.

### Next step
Introduce a liquidity-aware detection model: require absolute volume thresholds (e.g., 1000+ contracts) AND percentage-based price moves (>5% for low-liquidity tiers) rather than uniform fractional thresholds across all market types.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.05`, `score_threshold` → `8.0`

### Recommendations

- [ ] **TB-015** `planned` — Add a baseline liquidity check: only emit signals on markets with >20k baseline volume, or require volume_delta to exceed 1.5x+ baseline AND absolute volume >1000 contracts for thin markets
- [ ] **TB-016** `planned` — Raise spike_min_price_move to 0.05 (5%) for markets with <20k baseline volume; keep 0.03-0.04 for liquid markets
- [ ] **TB-017** `planned` — Require sustained directional bias: filter out uniform/neutral moves by checking for consistent bid-ask imbalance or consecutive candle directionality, not just single-timeframe deltas

---

## 2026-04-05 — Advisor snapshot F

### Summary
Low-liquidity political markets are generating false positives on small price moves with modest volume deltas. Both signals had low yes-probability (0.2–0.38) and were labeled noise despite crossing current thresholds.

### Next step
Introduce an absolute minimum volume threshold (e.g., 1000+ contracts traded) for niche/low-liquidity markets before any spike detection, rather than relying solely on volume delta or relative baseline changes.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-018** `planned` — Add liquidity tier classification: require min_absolute_volume >= 1000 for political markets before spike scoring; apply higher thresholds to low-liquidity tiers
- [ ] **TB-019** `planned` — Raise spike_min_volume_delta to ~1000 or enforce 2.0x baseline multiplier (not 1.5x) to filter micro-moves on thin order books
- [ ] **TB-020** `planned` — Require price move >= 0.05 (5%) for low-liquidity markets, or boost score_threshold when volume is below median for market category

---

## 2026-04-05 — Advisor snapshot G

### Summary
Low-liquidity markets (cabinet, political) are generating false positives with small absolute volumes and modest price moves. The detector is triggering on single trades or micro-moves that lack meaningful market conviction.

### Next step
Introduce an absolute minimum volume threshold (e.g., 1000+ contracts) as a hard floor, independent of baseline comparisons, to filter out niche/low-liquidity spike noise before score evaluation.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-021** `planned` — Add spike_min_absolute_volume floor of 1000 contracts; reject any signal where volΔ < 1000 regardless of score or price move
- [ ] **TB-022** `planned` — Raise spike_min_price_move to 0.05 (5%) for markets with avg_volume < 500 contracts to avoid micro-moves in thin cabinets
- [ ] **TB-023** `planned` — Require trade_count_delta ≥ 2 or sustained multi-candle volume confirmation for price moves under 0.10 (10%) to filter single-trade artifacts

---

## 2026-04-05 — Advisor snapshot H

### Summary
Low-liquidity markets are generating false positives from single large trades or minimal sustained volume. Both recent signals show modest volume deltas (692–108k) and small price moves (3–4%) that lack confirmation via trade count or multi-candle persistence.

### Next step
Introduce a trade-count or volume-persistence filter: require either sustained volume across ≥2 consecutive 1m candles OR minimum recent trade count (e.g., ≥3 trades in lookback window) before emitting a signal in low-liquidity venues.

### Suggested thresholds
`min_volume_delta` → `150000.0`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-024** `planned` — Add min_trade_count (≥3) or min_consecutive_candles (≥2) requirement to filter single-trade spikes in cabinet/political markets.
- [ ] **TB-025** `planned` — Raise spike_min_volume_delta to 150,000+ for watch-tier signals, or scale the threshold dynamically by market liquidity tier (lower for high-volume markets, higher for cabinet/political).
- [ ] **TB-026** `planned` — Increase spike_score_threshold to 3.5+ to suppress scores driven purely by small fractional moves on low volume; reserve lower scores (2.5–3.2) for signals with high trade count or multi-candle confirmation.

---

## 2026-04-05 — Advisor snapshot I

### Summary
Low-liquidity markets are generating false positives from single large trades or routine algorithmic activity that move price minimally. The detector lacks filters for market depth and trade persistence.

### Next step
Implement a baseline-relative volume delta rule (e.g., require volΔ > 1.5x recent 5m average) and enforce multi-candle price persistence before signaling in markets with <1000 baseline volume.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-027** `planned` — Require volume delta to exceed 1.5x–2.0x the 5-minute rolling average baseline, not just an absolute threshold, to filter single-trade spikes in thin markets
- [ ] **TB-028** `planned` — Add a sustained price move filter: flag only if price move persists or increases across 2+ consecutive 1-minute candles, filtering single-candle noise
- [ ] **TB-029** `planned` — Implement liquidity-aware thresholds: markets with baseline volume <1000 require stricter filters (e.g., min 5–10 contracts traded, or 2%+ price move) vs. baseline >10k contracts

---

## 2026-04-05 — Advisor snapshot J

### Summary
Low-liquidity markets are generating false positives from single large trades and routine algorithmic activity. Both signals have low analyst confidence (yes=0.26 and yes=0.16) despite crossing current thresholds, indicating thresholds are too permissive for thin markets.

### Next step
Implement market-aware thresholds that scale by baseline liquidity: require percentage-based volume deltas (5-10% of recent baseline) and sustained multi-candle confirmation rather than single-spike detection in low-volume instruments.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `3.0`

### Recommendations

- [ ] **TB-030** `planned` — Require volume delta as % of 5-minute baseline volume, not absolute delta; flag only when delta exceeds 5-10% of baseline in thin markets (<1000 contracts/min baseline)
- [ ] **TB-031** `planned` — Add persistence filter: require price move to sustain or repeat across 2+ consecutive 1-minute candles before emitting signal, filtering single-trade artifacts
- [ ] **TB-032** `planned` — Increase minimum absolute trade volume requirement to >10 contracts per constituent trade for cabinet markets, preventing single-lot spikes from triggering

---

## 2026-04-05 — Advisor snapshot K

### Summary
Quote-only volume accumulation in low-liquidity markets is inflating spike scores without genuine executed trades, causing false positives on both notable and watch-tier signals.

### Next step
Implement a minimum executed trade volume filter (50+ contracts per side) before any volume delta contributes to spike score calculation, effectively decoupling quote activity from signal generation.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `9.0`

### Recommendations

- [ ] **TB-033** `planned` — Add executed_trade_volume_minimum: 50 contracts per side per 1-minute window; reject spike signals where volume delta is primarily quote-based
- [ ] **TB-034** `planned` — Segment spike detection by market liquidity tier: apply stricter thresholds (higher min_trade_volume, higher price_move%) to low-ADV prediction markets
- [ ] **TB-035** `planned` — Increase spike_score_threshold to 9.0+ for tier=notable signals to filter marginal signals like the 8.056 score on KXTRUMPSAYNICKNAME

---

## 2026-04-05 — Advisor snapshot L

### Summary
Quote-only activity in low-liquidity prediction markets is generating false positives across political and niche markets. Volume deltas are being inflated by quote accumulation without corresponding executed trades.

### Next step
Distinguish between quote volume and executed trade volume; require minimum executed trade volume (e.g., >20 shares/contracts per side) before any volume delta contributes to spike scoring.

### Suggested thresholds
`min_volume_delta` → `200.0`, `min_price_move` → `0.05`, `score_threshold` → `7.0`

### Recommendations

- [ ] **TB-036** `planned` — Implement minimum executed trade volume threshold (20-50 contracts per side per 1-minute window) before counting volume delta toward spike score—quote-only activity should be excluded or heavily discounted.
- [ ] **TB-037** `planned` — For watch-tier signals on low-liquidity markets (e.g., political, niche contracts), require spike_score_threshold ≥4.0 to reduce noise; for notable-tier, require ≥7.0.
- [ ] **TB-038** `planned` — Add market-liquidity filter: on markets with <500 total daily volume, enforce spike_min_volume_delta ≥200 (executed only) and spike_min_price_move ≥0.05 (5%).

---

## 2026-04-05 — Advisor snapshot M

### Summary
Quote-only volume activity in low-liquidity political markets is generating false positives with misleading high scores despite low executed trade volume and weak price conviction (yes=0.07-0.63).

### Next step
Implement a minimum executed trade volume filter (e.g., >20 shares) that must be met before quote volume counts toward spike detection, rather than relying on quote volume deltas alone.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-039** `planned` — Add executed_trade_volume_min threshold (suggest: >20 shares) and only count quote volume when this threshold is met
- [ ] **TB-040** `planned` — Discount or exclude quote-only volume spikes from score calculation in markets with liquidity < some baseline (e.g., <500 total shares traded in period)
- [ ] **TB-041** `planned` — Raise spike_score_threshold to >5.0 for tier=watch signals on political/low-liquidity markets to require stronger conviction before flagging

---

## 2026-04-05 — Advisor snapshot N

### Summary
False positives are concentrated in low-liquidity political markets where quote-only movements and minimal actual trades trigger signals despite low conviction. Price moves alone (2%) are insufficient filters without volume validation.

### Next step
Implement trade-count validation and tiered volume thresholds by liquidity/conviction level rather than a single global volume delta threshold.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `2.5`

### Recommendations

- [ ] **TB-042** `planned` — Require minimum number of actual trades (not just quote updates) during spike window to filter quote-only events in low-liquidity markets
- [ ] **TB-043** `planned` — Set volume delta thresholds conditionally: for yes_prob < 0.10 or volumes < 500 baseline units, require volume delta ≥ 10% of baseline; for others use 5%
- [ ] **TB-044** `planned` — Raise spike_min_price_move from 0.02 to 0.03 (3%) as a global floor, since 2% moves without supporting volume are predominantly noise in these markets

---

## 2026-04-05 — Advisor snapshot O

### Summary
High-scoring signals with minimal price impact (1-2%) and no executed trade confirmation are generating false positives, particularly in thin/political markets where order book activity doesn't translate to real price discovery.

### Next step
Require minimum executed trade volume confirmation alongside order book delta, and enforce a price-move floor that scales with market liquidity tier.

### Suggested thresholds
`min_price_move` → `0.025`

### Recommendations

- [ ] **TB-045** `planned` — Add executed_trade_volume_min threshold (e.g., >500 units or >$5k notional) to filter quote-only layering/spoofing in thin markets
- [ ] **TB-046** `planned` — Raise spike_min_price_move to 0.025 (2.5%) for tier=watch/notable signals, or scale dynamically by liquidity tier (1.5% for high-liquidity, 3% for thin markets)
- [ ] **TB-047** `planned` — Implement volume_delta_baseline_multiplier rule requiring volΔ > 1.5x rolling 30-min baseline to reduce sensitivity to absolute volume figures in low-liquidity pairs

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
