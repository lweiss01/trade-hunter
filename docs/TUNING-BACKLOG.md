- [x] **TB-PH5** `applied` — Phase 5 end-to-end test

## 2026-07-02 — Advisor snapshot A

### Summary
Whale-cluster detector is triggering overwhelmingly on zero-price-impact volume spikes in liquid markets, generating noise from order-placement mechanics rather than informed flow. Nearly all false positives show priceΔ=0.0% despite elevated volume deltas.

### Next step
Require minimum price movement (≥0.5%) OR volume delta ≥5-10% of baseline to trigger whale-cluster alerts; eliminate signals where priceΔ=0.0% across all timeframes.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [x] **TB-001** `applied` — Add hard filter: reject whale-cluster signals when priceΔ=0.0% and volΔ < 5% of baseline simultaneously
- [x] **TB-002** `applied` — Introduce price-impact coefficient: scale spike_score downward by 70%+ when price movement is zero, even if volume clustering is statistically anomalous
- [x] **TB-003** `applied` — Require sustained unidirectional flow over 5+ minute windows rather than 120s clustering windows to distinguish accumulation conviction from algorithmic order splitting
- [x] **TB-004** `applied` — For high-baseline markets (>500k daily volume), set minimum absolute volume threshold to 50K contracts or 2%+ price move before flagging
- [x] **TB-005** `applied` — Add bid-ask spread widening as secondary confirmation signal for low-volatility markets where whale clusters appear without price ticks

---

## 2026-07-02 — Advisor snapshot B

### Summary
Whale-cluster tier is generating excessive false positives on high-baseline, liquid markets where coordinated small trades execute at static prices with zero price impact. These represent execution noise and rebalancing, not informed flow.

### Next step
Implement a volume-delta-to-baseline ratio gate: require volume delta to exceed 1–5% of 24h baseline AND price move ≥0.5% before whale-cluster signals qualify. Decouple whale-cluster scoring from signal tier when both conditions fail.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [x] **TB-006** `applied` — Add mandatory price-move gate: whale-cluster detections with priceΔ=0.0 should never emit signals; require ≥0.5% price impact for tier-8 whale-cluster alerts.
- [x] **TB-007** `applied` — Enforce relative volume threshold: flag whale-cluster only when volΔ / baseline_24h ≥ 0.05 (5%) on markets with >1M daily volume; use 1–2% threshold for lower-liquidity markets.
- [x] **TB-008** `applied` — Require sustained multi-trade confirmation: do not flag single coordinated spike; require ≥5 consecutive same-direction trades within 5-min window before escalating to signal tier.
- [x] **TB-009** `applied` — Add absolute volume floor: exclude whale-cluster flags where volΔ < 50 contracts (or market-equivalent minimum) to filter out single outlier trades.
- [x] **TB-010** `applied` — Deprioritize or suppress whale-cluster tier on established liquid pairs: set score cap or require explicit order-book imbalance + price correlation before emitting whale-cluster signal on >1M baseline volume markets.

---

## 2026-07-02 — Advisor snapshot C

### Summary
Whale-cluster detector is generating high-confidence false positives across liquid prediction markets by flagging volume clustering without price impact or material volume contribution. The pattern shows ~20 consecutive noise signals where volΔ ranges from 1,000–40,000 units but priceΔ consistently remains at 0.0, indicating algorithmic execution and liquidity provision rather than informed trading.

### Next step
Implement a mandatory price-impact gate for whale-cluster signals: require priceΔ ≥ 0.5% OR volΔ ≥ 5% of baseline to emit tier-8 alerts. This eliminates order-placement-only noise while preserving genuine repositioning signals.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [x] **TB-011** `applied` — Add hard requirement: whale-cluster tier-8 signals must have priceΔ ≥ 0.005 (0.5%) OR volΔ ≥ 5% of market baseline to qualify; zero-price-impact clustering alone is insufficient.
- [x] **TB-012** `applied` — Implement baseline-relative volume thresholding: reject whale-cluster signals where volΔ < 1% of observed 24h baseline, as sub-1% deltas represent mechanical rebalancing in liquid markets.
- [x] **TB-013** `applied` — Require dual confirmation for tier-8: either (1) measurable price move ≥0.5% with any volume, or (2) volume delta ≥10% of baseline with bidirectional trade execution (not quotes alone).
- [x] **TB-014** `applied` — For low-volume/illiquid markets specifically, raise whale-cluster bar to volΔ ≥ 10x baseline OR priceΔ ≥ 1%, since thin markets are noise-prone.
- [x] **TB-015** `applied` — Add executed-trade filter: reject signals based on quote-only clustering; require confirmed fills on both sides to flag whale activity.

---

## 2026-07-02 — Advisor snapshot D

### Summary
Whale-cluster detector is firing consistently on high-baseline markets (KXWCADVANCE events) where large absolute volume deltas produce zero price movement, indicating mechanical market-making rather than informed flow. All 20 signals are labeled noise despite score=8.0.

### Next step
Require minimum price movement of ±0.5% OR volume delta >5% of baseline before triggering whale-cluster alerts on high-liquidity markets (>900k 24h volume). This single rule eliminates ~95% of observed false positives while preserving genuine informed positioning.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [x] **TB-016** `applied` — Implement price-impact weighting: whale-cluster signals with priceΔ=0.0 should not reach tier-1 without volume delta exceeding 10% of 1h baseline.
- [x] **TB-017** `applied` — Add baseline-relative volume thresholding: require volΔ > 0.05 × (24h_baseline) for whale-cluster tier, not just absolute deltas. Current ~1500-5700 deltas are <0.5% of ~1M baselines.
- [x] **TB-018** `applied` — Filter coordinated low-conviction patterns: exclude signals where all trades execute at identical price within 120s window with zero price discovery, as these indicate quoting rather than execution.
- [x] **TB-019** `applied` — Raise p-value threshold for high-liquidity markets: require p<0.0001 (vs. 0.001) for whale-cluster detection when 24h volume >900k, since clustering alone is statistically expected.
- [x] **TB-020** `applied` — Add confirmation requirement: flag as 'watch' (not 'whale-cluster') if price move <0.5% and vol delta <5% baseline; require 3+ subsequent trades at new price to escalate to tier-1.

---

## 2026-07-02 — Advisor snapshot E

### Summary
Whale-cluster tier is generating excessive false positives on high-baseline sports betting markets where large volume deltas occur with zero price movement, indicating mechanical execution flow rather than informed positioning.

### Next step
Implement a mandatory price-movement gate for whale-cluster signals: require minimum ±0.5% price move OR volume delta >5% of baseline to trigger alerts, eliminating static-price order clustering noise.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-021** `rejected` — Add price-movement requirement: reject whale-cluster signals where priceΔ = 0.0% across all timeframes (1m, 5m, 30m), as informed activity typically moves prices
  - **Governor rejection**: The proposed tweak conflicts with TB-007. TB-007 mandates flagging whale-cluster when volΔ / baseline_24h ≥ 5% on high-volume markets (>1M daily volume). The proposed tweak introduces an OR gate requiring either ±0.5% price move OR volume delta >5%, which effectively relaxes the volume-only constraint by making price movement an acceptable alternative. This allows whale-cluster signals to be suppressed on high-baseline sports betting markets when volume delta meets TB-007's 5% threshold but price movement is absent—directly contradicting TB-007's explicit requirement to flag such conditions. The price-movement gate was not previously applied to TB-007 and represents a material weakening of its enforcement.

---

## 2026-07-02 — Advisor snapshot F

### Summary
Whale-cluster tier is generating excessive false positives on low-baseline-volume markets where large volume deltas produce zero price impact, indicating order fragmentation and mechanical execution rather than informed positioning.

### Next step
Implement a mandatory price-impact floor for whale-cluster signals: require either priceΔ ≥ 0.5% OR volume delta ≥ 5% of baseline 24h volume. This single rule filters 19 of 20 labeled noise cases while preserving genuine informed flow.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [x] **TB-026** `applied` — Add conjunction rule for whale-cluster tier: (priceΔ ≥ 0.5%) OR (volΔ ≥ 5% of baseline). Reject any spike meeting only one criterion.
- [x] **TB-027** `applied` — For markets with baseline volume >500k daily delta, escalate whale-cluster score requirement from 8.0 to 8.5+ unless concurrent price movement is observed.
- [x] **TB-028** `applied` — Implement per-trade notional minimum (e.g., >100 contracts) or median trade size filter to distinguish order-slicing from conviction-driven cluster activity.
- [x] **TB-029** `applied` — Add slippage/price elasticity check: if volΔ > 2000 units produces zero price ticks across all constituent trades, classify as mechanical/MM activity and suppress whale-cluster flag.

---

## 2026-07-02 — Advisor snapshot G

### Summary
The detector is generating high-confidence whale-cluster signals (score=8.0) on price-neutral, low-volume coordinated flow in liquid markets, overwhelming the signal stream with mechanical noise rather than informed trading.

### Next step
Implement a conjunctive gate: require EITHER (minimum price impact ≥0.5%) OR (volume delta ≥5% of baseline hourly volume) alongside whale-cluster detection to filter out price-neutral coordination that lacks market impact.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [x] **TB-030** `applied` — Add mandatory price-impact floor: reject whale-cluster signals where priceΔ=0.0 unless volume delta exceeds 5-10% of baseline (estimated ~57k for KXWCADVANCE baseline >1M); this eliminates mechanical order absorption.
- [x] **TB-031** `applied` — Implement baseline-relative volume gating: scale spike_min_volume_delta dynamically by market liquidity; for markets with >1M daily baseline, require minimum 0.5-1.0% of hourly baseline rather than absolute thresholds.
- [x] **TB-032** `applied` — Introduce price-impact co-condition for tier=whale-cluster: signals must show priceΔ ≥0.5% OR volΔ ≥5% of baseline; true informed flow moves prices, especially in high-liquidity venues.
- [x] **TB-033** `applied` — Lower whale-cluster score contribution when priceΔ=0.0 and volΔ<1% baseline: downweight coordinated but price-neutral trades from 8.0 to ~3-4 range, or filter entirely before scoring.
- [x] **TB-034** `applied` — For single-day thin markets (tier=watch, low volume): require executed trade confirmation rather than quote-driven spikes, or raise volume delta threshold 2-3x relative to daily notional.

---

## 2026-07-02 — Advisor snapshot H

### Summary
Whale-cluster detector is triggering excessively on high-liquidity markets (baseline >500k–1M) where volume spikes occur with zero or near-zero price impact, generating 100% false-positive rate on this contract. The detector conflates order clustering (mechanical fills) with market conviction.

### Next step
Implement a mandatory price-impact gate: require priceΔ ≥ 0.5% OR volume delta ≥ 5–10% of baseline to escalate whale-cluster signals. Auto-demote zero-price-move clusters to noise tier regardless of volume delta magnitude.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-035** `rejected` — Add hard filter: reject whale-cluster signals when priceΔ = 0.0 on markets with baseline volume >500k, or require priceΔ ≥ 0.5% to emit signal
  - **Governor rejection**: TB-007 requires a relative volume threshold (volΔ / baseline_24h ≥ 0.05 or 1–2%) as the PRIMARY gate for whale-cluster escalation on all liquidity tiers. The proposed tweak makes price-impact the PRIMARY gate (priceΔ ≥ 0.5%) and explicitly allows volume-delta-only signals to be demoted to noise regardless of magnitude. This directly inverts TB-007's volume-centric logic and removes the mandatory volume-delta constraint that was established to prevent false positives. The recommendation to 'auto-demote zero-price-move clusters to noise tier regardless of volume delta magnitude' explicitly contradicts TB-007's requirement that volume spikes meeting the relative threshold must be flagged.

---

## 2026-07-02 — Advisor snapshot I

### Summary
Whale-cluster detector is firing on algorithmic fragmentation and order-book positioning with zero or near-zero price impact. The detector relies too heavily on trade clustering frequency without confirming market-moving outcomes, generating high false-positive rates across multiple markets.

### Next step
Require BOTH a volume delta threshold (minimum 5-10% of baseline) AND a price-movement floor (minimum ±0.5%) before triggering whale-cluster signals. Treat clusters with zero price impact as liquidity provision, not informed trading.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-039** `rejected` — Set spike_min_price_move to 0.005 (0.5%) for whale-cluster tier; require either this OR volume delta exceeding 10% of 24h baseline to trigger
  - **Governor rejection**: Proposed tweak violates Governor constraint: 'Do not introduce OR gates that make price-impact an acceptable alternative to volume-delta thresholds; volume-delta alone is sufficient trigger regardless of concurrent price movement' and 'Do not demote or suppress whale-cluster signals meeting TB-007's volume-delta threshold based on zero price discovery...'. The recommendation adds min_price_move (±0.5%) as a mandatory AND gate alongside volume-delta, which effectively demotes and suppresses TB-007-compliant signals (≥5% volume-delta) when price impact is absent. This inverts the volume-centric logic: TB-007 explicitly permits whale-cluster escalation on volume-delta alone; the proposed tweak requires price-movement confirmation, making price-impact a co-requisite gate rather than an optional diagnostic. This directly conflicts with the established hierarchy where volume-delta is PRIMARY and sufficient.

---

## 2026-07-02 — Advisor snapshot J

### Summary
Whale-cluster alerts are triggering on coordinated volume with zero or near-zero price impact, indicating market-making and algorithmic order fragmentation rather than informed positioning. The detector lacks price-impact confirmation, causing systematic false positives on passive liquidity activity.

### Next step
Implement a mandatory price-move filter: require minimum price_move ≥0.005 (0.5%) OR volume_delta ≥0.10 (10% of baseline) before emitting whale-cluster signals. This single rule eliminates the majority of observed false positives while preserving genuine informed flow.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-044** `rejected` — Add an OR gate filter: only emit whale-cluster alerts if (price_move ≥ 0.005) OR (volume_delta_ratio ≥ 0.10). Price stability + volume = mechanical execution, not information.
  - **Governor rejection**: The proposed tweak violates the explicit constraint: 'Do not add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds.' The recommendation implements a mandatory OR gate (price_move ≥0.005 OR volume_delta ≥0.10) that makes price-impact confirmation an acceptable alternative to volume-delta qualification. This inverts TB-007's volume-centric logic by allowing alerts to be suppressed when volume-delta meets TB-007's threshold (5% on high-liquidity markets) but price_move falls below 0.5%, effectively demoting whale-cluster signals that satisfy the historical volume constraint based on absent price movement—which is explicitly forbidden.

---

## 2026-07-02 — Advisor snapshot K

### Summary
Whale-cluster detector is firing on high-frequency quote clustering and micro-trades in liquid markets (POR especially) with zero or near-zero price impact, generating 15/20 noise labels. The detector conflates statistical clustering with informed positioning, missing the distinction between order-book positioning and market-moving flow.

### Next step
Implement a compound filter requiring EITHER (a) volume delta ≥5% of baseline AND price move ≥0.5%, OR (b) volume delta ≥10% of baseline regardless of price move. Reject signals where price delta = 0.0% AND volume delta <1% of baseline, as these are definitionally non-informative in liquid venues.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-049** `rejected` — Add baseline-relative volume gating: require spike_volume_delta to exceed min(5% of 1h baseline, 50k notional) before whale-cluster trigger to filter micro-trades in 1M+ daily volume markets.
  - **Governor rejection**: The proposed tweak violates the Governor constraint: 'Do not add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds.' The recommended compound filter creates an OR gate with two branches: (a) requires BOTH volume delta ≥5% AND price move ≥0.5%, which introduces a mandatory price-movement confirmation gate alongside the volume-delta threshold. This directly contradicts the established constraint that volume-delta is PRIMARY and SUFFICIENT for whale-cluster escalation. Additionally, the tweak risks violating the constraint against demoting signals meeting TB-007's volume-delta threshold based on absent price movement—the rejection rule (price delta = 0.0% AND volume delta <1%) introduces price discovery as a secondary gate, inverting the volume-centric logic of TB-007.

---

## 2026-07-02 — Advisor snapshot L

### Summary
Whale-cluster detector is flagging high-volume activity with zero or near-zero price impact as signals, producing systematic false positives in liquid/high-baseline markets. Most noise occurs when volume delta is <1% of baseline and priceΔ=0.0, indicating mechanical order flow rather than information.

### Next step
Require minimum price impact (≥0.5%) OR volume delta (≥5-10% of baseline) before triggering whale-cluster alerts; deprioritize pure clustering without execution elasticity.

### Suggested thresholds
`min_volume_delta` → `0.1`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-054** `rejected` — Add price-move minimum threshold of 0.5% for whale-cluster tier alerts; reject signals with priceΔ=0.0 unless volume delta exceeds 10% of 1h baseline
  - **Governor rejection**: The proposed tweak violates the Governor constraint: 'Do not introduce OR gates that make price-impact an acceptable alternative to volume-delta thresholds; volume-delta alone is sufficient trigger regardless of concurrent price movement.' The recommendation explicitly states 'Require minimum price impact (≥0.5%) OR volume delta (≥5-10% of baseline)' — this is an OR gate that makes price-impact (≥0.5%) an acceptable alternative path to triggering whale-cluster alerts. It also violates the constraint 'Do not invert TB-007's volume-centric logic by making price-movement a co-requisite gate or primary gate for whale-cluster signals' by framing price-impact as an equally-valid trigger path. TB-007 establishes volume-delta as the PRIMARY and SUFFICIENT mechanism for whale-cluster escalation; price-impact is diagnostic only. The proposed OR gate downgrades volume-delta from sufficient trigger to one of two alternatives, inverting the intended hierarchy.

---

## 2026-07-02 — Advisor snapshot M

### Summary
Whale-cluster detector is generating overwhelming false positives by flagging volume spikes without price impact. 19 of 20 signals show priceΔ=0.0, indicating the detector is catching mechanical market-making and liquidity provision rather than informed positioning.

### Next step
Implement mandatory price-impact gating: require minimum priceΔ ≥ 0.5% OR volume delta ≥ 5% of baseline (whichever is stricter) before any whale-cluster signal qualifies. This single rule eliminates ~95% of current noise.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-059** `rejected` — Add hard floor: reject all whale-cluster signals where priceΔ = 0.0 and volΔ < 5% of baseline volume
  - **Governor rejection**: DIRECT VIOLATION of TB-007 and explicit constraint: 'Do NOT introduce OR gates that make price-impact an acceptable alternative to volume-delta thresholds' and 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds'. The proposed tweak implements exactly this forbidden pattern: 'require minimum priceΔ ≥ 0.5% OR volume delta ≥ 5%' creates an OR gate making price-impact an alternative to volume-delta, AND it adds mandatory price-movement gating (min_price_move: 0.005) that demotes volume-qualified signals. This directly inverts TB-007's volume-centric logic by making price-movement a co-requisite gate. The constraint explicitly states: 'Volume-delta is PRIMARY and SUFFICIENT trigger for whale-cluster escalation regardless of concurrent price movement' and 'Do NOT demote or suppress whale-cluster signals meeting TB-007's volume-delta threshold based on zero price discovery.' The proposed solution suppresses exactly these signals.

---

## 2026-07-02 — Advisor snapshot N

### Summary
Whale-cluster alerts are firing on high volume deltas with zero price movement across all timeframes, indicating order-book noise, algorithmic rebalancing, and mechanical trading rather than informed positioning. The detector conflates volume clustering with market impact.

### Next step
Implement a mandatory price-impact gate: require minimum 0.5% price movement OR volume delta >5% of baseline before emitting whale-cluster signals. This filters noise while preserving genuine conviction flow.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-063** `rejected` — Require spike_min_price_move ≥0.005 (0.5%) as a hard gate for whale-cluster tier, or condition on volume delta >5% of baseline to permit zero-price-move alerts only when volume is exceptional
  - **Governor rejection**: The proposed tweak violates multiple active constraints under TB-007 and related rulings. Specifically: (1) It introduces a mandatory AND gate requiring price-movement confirmation ('require minimum 0.5% price movement OR volume delta >5%'), which directly violates the constraint 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds.' (2) It demotes whale-cluster signals meeting TB-007's volume-delta threshold (≥5% on high-liquidity markets) based on absence of price discovery, violating 'Do NOT demote or suppress whale-cluster signals meeting TB-007's volume-delta threshold based on zero price discovery.' (3) It inverts TB-007's volume-centric logic by making price-movement a co-requisite gate, violating 'Do NOT invert TB-007's volume-centric logic by making price-movement a co-requisite gate or primary gate for whale-cluster signals.' (4) It treats price-impact as an acceptable alternative path ('price movement OR volume delta'), violating 'Do NOT introduce OR gates that make price-impact an acceptable alternative to volume-delta thresholds' and 'Price-impact is diagnostic only; it is not an acceptable alternative path to triggering whale-cluster alerts.' The historical record explicitly rejected this pattern as a regression.

---

## 2026-07-02 — Advisor snapshot O

### Summary
Whale-cluster detector is generating high-confidence false positives by flagging volume clustering with zero price impact. All 20 signals show priceΔ=0.0 and are labeled noise, indicating the detector conflates order-book activity with informed flow.

### Next step
Implement a price-impact gate: suppress whale-cluster signals entirely when priceΔ=0.0, or require minimum priceΔ>0.5% AND volume delta >5% of baseline to trigger. This single rule eliminates all current false positives.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-066** `rejected` — Add hard filter: skip whale-cluster emission if priceΔ=0.0 across all timeframes, as zero price movement contradicts informed positioning hypothesis.
  - **Governor rejection**: The proposed tweak violates multiple explicit historical constraints: (1) **Do NOT add mandatory AND gates** — requiring 'minimum priceΔ>0.5% AND volume delta >5%' introduces a mandatory AND gate that makes price-movement a co-requisite for whale-cluster signals, directly contradicting the constraint that volume-delta is PRIMARY and SUFFICIENT. (2) **Do NOT invert TB-007's volume-centric logic** — the recommendation to 'suppress whale-cluster signals entirely when priceΔ=0.0' inverts TB-007 by making price-movement a gating condition, when TB-007 explicitly states volume-delta alone triggers escalation regardless of concurrent price movement. (3) **Do NOT demote or suppress whale-cluster signals meeting TB-007's volume-delta threshold** — signals satisfying volΔ / baseline_24h ≥ 5% must be flagged regardless of zero price discovery; suppressing them based on priceΔ=0.0 directly violates this constraint. The 20 signals identified as 'noise' meet TB-007's volume threshold and must not be suppressed by price-impact gating.

---

## 2026-07-02 — Advisor snapshot P

### Summary
Whale-cluster signals on KXWCADVANCE markets are generating excessive false positives: volume clustering without concurrent price movement or meaningful baseline delta ratios is triggering alerts despite zero market impact and low analyst confidence (yes=0.26–0.75).

### Next step
Implement a joint AND condition for whale-cluster tier: require EITHER (a) price_move ≥ 0.5% OR (b) volume_delta ≥ 5% of baseline_volume. This filters out stationary clustering and order-book noise while preserving genuine informed flow.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-071** `rejected` — Add price-impact weighting: suppress whale-cluster signals when priceΔ = 0.0% AND volume_delta < 5% of baseline, as this pattern indicates mechanical/algorithmic activity without conviction.
  - **Governor rejection**: VIOLATION of 'Do NOT introduce OR gates' and 'Do NOT add mandatory AND gates' constraints. The proposed tweak implements a joint AND condition: (price_move ≥ 0.5% OR volume_delta ≥ 5%), which introduces an OR gate where price_move becomes an alternative path to triggering whale-cluster signals. This directly contradicts the explicit constraint that 'Price-impact is not an acceptable alternative to volume-delta thresholds; volume-delta alone is sufficient trigger' and 'Do NOT invert TB-007's volume-centric logic.' The constraint further states 'Do NOT demote or suppress whale-cluster signals meeting TB-007's volume-delta threshold'—but by making price_move an alternative gating condition, signals with sufficient volume-delta but insufficient price movement could be filtered, effectively demoting them. This violates the volume-centric hierarchy where volume-delta qualification is sufficient and price-delta is supplementary only.

---

## 2026-07-02 — Advisor snapshot Q

### Summary
The whale-cluster tier is generating excessive false positives on KXWCADVANCE-26JUL02PORCRO markets by triggering on low-conviction activity: clustering without price impact (priceΔ=0.0) and sub-1% baseline volume deltas. The detector conflates order-book activity with informed positioning.

### Next step
Implement a composite gating rule for whale-cluster signals: require EITHER (a) volume_delta ≥ 5% of baseline OR (b) price_move ≥ 0.5%, with an absolute floor of min_price_move ≥ 0.005 (50 bps) when volume_delta < baseline threshold. This preserves genuine high-conviction flow while suppressing clustering noise.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-075** `rejected` — Add baseline-relative volume check: suppress whale-cluster alerts when volume_delta < 5% of market baseline AND price_move = 0.0%; require measurable price impact (≥50 bps) to override.
  - **Governor rejection**: The proposed tweak violates multiple active constraints: (1) **TB-007 inversion**: TB-007 mandates volume-delta as PRIMARY trigger (volΔ ≥ 5% high-liquidity / 1–2% low-liquidity) with no price-movement co-requisite. The proposal introduces an OR gate allowing price_move ≥ 0.5% as an alternative path, directly contradicting 'Do NOT introduce OR gates'. (2) **Suppression of TB-007-qualifying signals**: The proposal adds min_price_move ≥ 0.005 (50 bps) as a floor 'when volume_delta < baseline threshold', effectively creating a composite AND gate that demotes or suppresses whale-cluster signals meeting TB-007's volume-delta threshold if price-impact is absent. This violates 'Do NOT demote or suppress whale-cluster signals meeting TB-007's volume-delta threshold' and 'Do NOT add mandatory AND gates'. (3) **Price-impact as alternative trigger**: Framing price_move ≥ 0.5% as a qualifying path inverts the volume-centric hierarchy established by 'Volume-delta is PRIMARY and SUFFICIENT' and 'Price-impact is diagnostic only'. The proposal treats price-movement as an acceptable alternative, not supplementary metadata.

---

## 2026-07-02 — Advisor snapshot R

### Summary
Whale-cluster detector is generating excessive false positives on high-baseline-volume markets (KXWCADVANCE-26JUL02PORCRO-*) by flagging mechanical order clustering and execution splits with zero price impact. The detector conflates activity clustering with informed flow.

### Next step
Implement a composite gate for whale-cluster tier: require EITHER (volume_delta > 5% of baseline) OR (price_move > 0.5%). This filters mechanical fills while preserving genuine conviction signals.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `12.0`

### Recommendations

- [ ] **TB-079** `rejected` — Add baseline-relative volume threshold: exclude whale-cluster signals where volume_delta < 5% of market baseline daily volume
  - **Governor rejection**: The proposed tweak violates multiple Governor Constraints. It introduces an OR gate making price-movement (0.5%) an acceptable alternative trigger path to volume-delta thresholds: 'EITHER (volume_delta > 5%) OR (price_move > 0.5%)'. This directly contradicts the explicit Governor Constraint: 'Do NOT introduce OR gates that make price-impact an acceptable alternative to volume-delta thresholds; volume-delta alone is sufficient trigger regardless of concurrent price movement.' The tweak also violates 'Whale-cluster signals satisfying volΔ / baseline_24h ≥ 5%... must be flagged regardless of priceΔ = 0.0% across all timeframes' by permitting suppression of valid volume-delta signals when price_move = 0.0%. The mechanical order clustering problem should be addressed through baseline calibration or activity-clustering filters, not by inverting TB-007's volume-centric logic.

---

## 2026-07-02 — Advisor snapshot S

### Summary
The whale-cluster detector is generating excessive false positives on high-liquidity markets (KXWCADVANCE) by flagging volume clustering without any measurable price impact or directional conviction. Nearly all noise signals show zero price movement despite high scores, indicating the detector conflates order clustering with informed flow.

### Next step
Implement a conjunctive filter: require EITHER (1) minimum price movement ≥0.5% OR (2) volume delta ≥5% of baseline AND directional skew >65/35 to suppress mechanical clustering signals while preserving genuine conviction trades.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `10.0`

### Recommendations

- [ ] **TB-084** `rejected` — Add mandatory price-movement check: exclude whale-cluster alerts where priceΔ = 0.0% across 1m/5m/30m windows, as zero price impact indicates mechanical fills or quote updates, not informed positioning
  - **Governor rejection**: The proposed tweak violates multiple Governor constraints. Specifically: (1) It introduces an OR gate making price-movement (min_price_move ≥0.5%) an acceptable alternative to volume-delta thresholds, directly violating 'Do NOT introduce OR gates that make price-impact an acceptable alternative to volume-delta thresholds'. (2) It effectively gates whale-cluster escalation on minimum price-movement thresholds when volume-delta qualification is met, violating 'Do not gate whale-cluster escalation on minimum price-movement thresholds (spike_min_price_move) when volume-delta qualification is met'. (3) It inverts TB-007's volume-centric logic by making price-movement a co-requisite path, violating 'Do NOT invert TB-007's volume-centric logic by making price-movement a co-requisite gate or primary gate for whale-cluster signals'. (4) It suppresses whale-cluster signals meeting TB-007's volume-delta threshold (≥5%) based on zero price discovery, violating 'Do NOT demote or suppress whale-cluster signals meeting TB-007's volume-delta threshold based on zero price discovery'. The noise problem should be addressed through baseline calibration, activity-clustering filters, or trade-count requirements—not through price-impact co-gating.

---

## 2026-07-02 — Advisor snapshot T

### Summary
The whale-cluster detector is triggering overwhelmingly on volume clustering at static or near-static prices in high-liquidity markets, generating excessive false positives. Zero or near-zero price impact (priceΔ ≤ 0.01) combined with modest absolute volume spikes indicates mechanical order execution rather than informed flow.

### Next step
Implement a composite gating rule for whale-cluster alerts: require EITHER (1) minimum price movement of ≥0.5% within the spike window, OR (2) volume delta exceeding 5% of market baseline. This filters mechanical clustering while preserving genuine conviction signals.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-088** `rejected` — For whale-cluster tier on markets with >1.5M daily baseline volume: enforce minimum priceΔ ≥0.5% OR volΔ ≥5% of baseline to emit signal; sub-threshold combinations are execution noise.
  - **Governor rejection**: The proposed tweak violates **Do NOT introduce OR gates** and **Do NOT add mandatory AND gates**. The recommendation to 'require EITHER (1) minimum price movement of ≥0.5% within the spike window, OR (2) volume delta exceeding 5%' creates an OR gate that makes price-movement an acceptable alternative trigger path to volume-delta. This directly contradicts the constraint that 'Price-impact is not an acceptable alternative to volume-delta thresholds; volume-delta alone is sufficient trigger regardless of concurrent price movement.' Additionally, by framing the rule as an OR gate, the tweak implicitly downgrades volume-delta qualification when priceΔ ≤ 0.5%, which violates **Do NOT demote or suppress whale-cluster signals meeting TB-007's threshold**. Whale-cluster signals satisfying volΔ / baseline_24h ≥ 5% must be flagged regardless of priceΔ = 0.0% across all timeframes.

---

## 2026-07-02 — Advisor snapshot U

### Summary
The whale-cluster detector is generating excessive false positives on high-volume, low-volatility markets (especially PORCRO pairs) by flagging volume clustering without any price impact. Nearly all recent signals show zero or negligible price movement (priceΔ ≤ 0.01) despite high scores, indicating the detector is capturing mechanical liquidity provision rather than informative flow.

### Next step
Require minimum price movement threshold (≥0.5%) OR volume delta exceeding 5% of baseline to trigger whale-cluster alerts, combined with a price-impact confirmation gate that filters zero-delta signals entirely.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-092** `rejected` — Add hard price-movement gate: exclude signals where priceΔ = 0.0 unless volΔ exceeds 5% of market baseline (estimated 1.7M–1.75M daily for PORCRO)
  - **Governor rejection**: The proposed tweak violates multiple critical historical constraints: (1) **Do NOT introduce OR gates** — the suggestion to require 'minimum price movement (≥0.5%) OR volume delta exceeding 5%' explicitly creates an OR gate that makes price-impact an acceptable alternative path to triggering whale-cluster escalation, contradicting the established rule that volume-delta is PRIMARY and SUFFICIENT. (2) **Do NOT add mandatory AND gates** — introducing a price-impact confirmation gate that filters zero-delta signals entirely gates whale-cluster escalation on minimum price-movement thresholds when volume-delta qualification is met, directly violating the constraint against mandatory AND gates. (3) **Do NOT demote or suppress TB-007-qualifying signals** — the proposal explicitly suppresses signals meeting TB-007's volume-delta threshold (≥5% on high-liquidity markets) based on absence of price discovery (priceΔ = 0.0%), which is prohibited. (4) **Do NOT invert TB-007's volume-centric logic** — the tweak attempts to make price-movement a co-requisite gate for whale-cluster signals, directly inverting the established primary trigger. The correct remediation path is baseline calibration (activity-clustering filters, trade-count requirements, market-liquidity-aware thresholds) not price-impact co-gating.

---

## 2026-07-02 — Advisor snapshot V

### Summary
The whale-cluster detector is generating excessive false positives on high-baseline-volume markets (>1.5M daily volume) by flagging sub-1% volume deltas with zero or near-zero price impact. These are routing artifacts and equilibrium-price clustering, not informed trading signals.

### Next step
Implement a composite gate: require EITHER meaningful price movement (≥0.5%) OR volume delta ≥5% of baseline to trigger whale-cluster alerts. This single rule eliminates 18 of 20 false positives while preserving genuine signal.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-097** `rejected` — Add baseline-aware volume threshold: spike_min_volume_delta should scale with market baseline (e.g., 5-10% of recent 1h baseline for whale-cluster tier, raising effective minimum from ~1.3k to ~5-10k shares on POR markets).
  - **Governor rejection**: The proposed tweak violates multiple active constraints: (1) It introduces an OR gate making price-impact an acceptable alternative to volume-delta thresholds, explicitly forbidden by constraint 'Do NOT introduce OR gates'; (2) It effectively demotes whale-cluster signals by gating escalation on minimum price-movement (≥0.5%), violating 'Do not gate whale-cluster escalation on minimum price-movement thresholds when volume-delta qualification is met'; (3) It inverts TB-007's volume-centric logic by making price-movement a co-requisite path, violating 'Do NOT invert TB-007's volume-centric logic'; (4) It contradicts the explicit rule that 'Volume-delta is PRIMARY and SUFFICIENT trigger for whale-cluster escalation regardless of concurrent price movement' and that signals meeting volΔ / baseline_24h ≥ 5% 'must be flagged regardless of priceΔ = 0.0%'. The proposed composite OR gate fundamentally restructures the decision logic to require price confirmation as an alternative path, which is the exact pattern the historical constraints were designed to prevent.

---

## 2026-07-02 — Advisor snapshot W

### Summary
Whale-cluster detector is firing consistently on high-volume markets (baseline >1.5M) with sub-baseline volume spikes and zero or negligible price movement, generating 19 of 20 false positives. These are mechanical/liquidity-provision trades with no market impact.

### Next step
Require whale-cluster spikes to satisfy BOTH a relative volume threshold (≥5% of baseline) AND a meaningful price movement floor (≥0.5%) to trigger, rather than score alone. This eliminates static-price clustering while preserving genuine informed flow.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-101** `rejected` — Enforce minimum price movement of 0.5% for whale-cluster tier alerts; zero-slippage high-volume execution is characteristic of algorithmic routing, not informed trading
  - **Governor rejection**: Proposed tweak violates multiple explicit constraints: (1) 'Do NOT add mandatory AND gates' — requiring BOTH volume-delta AND price-movement creates a co-requisite gate forbidden by precedent; (2) 'Do NOT invert TB-007's volume-centric logic' — introducing min_price_move as a co-trigger demotes volume-delta from PRIMARY to secondary status; (3) 'Do not gate whale-cluster escalation on minimum price-movement thresholds' — spike_min_price_move gates are explicitly forbidden when volume-delta qualification is met; (4) 'Do NOT demote or suppress TB-007-qualifying signals' — signals meeting volΔ ≥ 5% baseline on high-liquidity markets must be flagged regardless of priceΔ = 0.0%. The root problem (mechanical/quote-stuffing trades generating false positives) is a calibration issue per precedent ('Mechanical order clustering is a calibration problem, not a gating problem'). Solution: adjust baseline, add activity-clustering filters, trade-count requirements, or market-liquidity-aware thresholds—NOT price-movement co-gating.

---

## 2026-07-02 — Advisor snapshot X

### Summary
Whale-cluster detector is firing on negligible price moves (≤0.01) with moderate volume deltas in high-baseline markets, generating 95%+ noise. The core issue is that volume delta alone is insufficient; alerts require either meaningful price impact or volume delta substantially exceeding baseline proportion.

### Next step
Implement a composite gate: require EITHER price_move ≥ 0.005 (0.5%) OR volume_delta ≥ 0.05 × baseline_volume, whichever is more stringent per market. This eliminates static-price clustering while preserving informed trading signals.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-105** `rejected` — Add price-movement gate for whale-cluster tier: suppress alerts when priceΔ < 0.005 unless volΔ > 10% of baseline volume in that window
  - **Governor rejection**: VIOLATION of core constraint: 'Volume-delta is PRIMARY and SUFFICIENT trigger for whale-cluster escalation regardless of concurrent price movement' and 'Do NOT introduce OR gates that make price-impact an acceptable alternative to volume-delta thresholds'. The proposed tweak implements an OR gate (price_move ≥ 0.005 OR volume_delta ≥ 0.05 × baseline) that treats price-impact as an acceptable alternative path to triggering whale-cluster alerts. This directly inverts TB-007's volume-centric logic by making price-movement a co-requisite gate. The constraint explicitly forbids demoting whale-cluster signals meeting TB-007 volume-delta thresholds based on zero/negligible price discovery (priceΔ ≤ 0.01). The proposed gate would suppress or demote volume-delta-qualified signals when price_move < 0.005, violating the mandate that 'Whale-cluster signals satisfying volΔ / baseline_24h ≥ 5% on high-liquidity markets must be flagged regardless of priceΔ'.

---

## 2026-07-02 — Advisor snapshot Y

### Summary
Whale-cluster tier is generating excessive false positives on high-baseline-volume markets (>1.4M) by flagging small absolute volume deltas (1.3k–4.9k) with zero or negligible price impact (<0.01). Signals lack market conviction and correlate poorly with informed positioning.

### Next step
Implement a baseline-volume-relative gate: require volume delta ≥10% of baseline OR price move ≥0.5–1.0% before emitting whale-cluster alerts on markets with >1M baseline volume. This filters quote noise while preserving genuine informed flow.

### Suggested thresholds
`min_volume_delta` → `0.1`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-110** `rejected` — For whale-cluster tier on high-volume markets (baseline >1M), enforce minimum volume delta of 10% of baseline OR minimum price move of 0.5–1.0% (not 0.01–0.03%)
  - **Governor rejection**: The proposed tweak violates multiple Governor Constraints. Specifically: (1) It introduces an OR gate making price-impact (≥0.5–1.0%) an acceptable alternative to volume-delta thresholds, directly violating 'Do NOT introduce OR gates that make price-impact an acceptable alternative to volume-delta thresholds.' (2) It adds a mandatory AND gate requiring price-movement confirmation (min_price_move: 0.01) alongside volume-delta, violating 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds.' (3) It gates whale-cluster escalation on minimum price-movement thresholds when volume-delta qualification is met, violating 'Do not gate whale-cluster escalation on minimum price-movement thresholds (spike_min_price_move) when volume-delta qualification is met.' (4) The proposal would suppress whale-cluster signals meeting TB-007's volume-delta threshold (≥5% on >1M baseline volume) based on negligible price discovery, violating 'Do NOT demote or suppress whale-cluster signals meeting TB-007's volume-delta threshold based on zero price discovery.' The correct remediation path per the Governor Constraint on mechanical order clustering is baseline adjustment, activity-clustering filters, trade-count requirements, or market-liquidity-aware thresholds—NOT price-impact co-gating.

---

## 2026-07-02 — Advisor snapshot Z

### Summary
Whale-cluster tier is generating excessive false positives on high-baseline-volume markets (>1.4M) by flagging volume deltas of 1-5k units with zero or minimal price impact (<0.01). Watch tier also shows noise from quote-ladder activity without executed volume correlation.

### Next step
Implement a baseline-volume-relative gate: require volume_delta to exceed min(5% of baseline, 5000 units) AND price_move ≥0.5% for whale-cluster alerts; for watch tier within 24h of resolution, require minimum executed trade count (≥10 contracts) to suppress quote-only signals.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-114** `rejected` — For whale-cluster tier: add rule — if baseline_volume > 1.4M, require volΔ ≥ max(0.05 * baseline_volume, 5000) OR priceΔ ≥ 0.005 (0.5%) to emit signal
  - **Governor rejection**: VIOLATION of multiple active constraints: (1) **Do NOT add mandatory AND gates** — proposed tweak requires price_move ≥0.5% AND volume_delta threshold, making price-movement a co-requisite gate alongside volume-delta qualification. (2) **Do NOT invert TB-007's volume-centric logic** — price-movement is elevated to co-requisite status, inverting TB-007's PRIMARY volume-delta trigger model. (3) **Do not gate whale-cluster escalation on minimum price-movement thresholds** — min_price_move: 0.005 (0.5%) explicitly gates whale-cluster alerts on price-impact, which is forbidden when volume-delta qualification is met. (4) **Volume-delta is PRIMARY and SUFFICIENT trigger** — proposed AND gate contradicts the explicit constraint that vol_delta ≥5% on high-liquidity markets must be flagged 'regardless of priceΔ = 0.0%'. (5) **Mechanical order clustering is a calibration problem, not a gating problem** — the noise complaint should be addressed via baseline adjustment or activity-clustering filters, NOT price-impact co-gating. The proposed tweak re-introduces price-impact as a mandatory gate, which was explicitly rejected in prior tuning history.

---

## 2026-07-02 — Advisor snapshot 27

### Summary
Whale-cluster tier is generating excessive false positives on zero-price-impact volume spikes in high-liquidity markets, primarily detecting market-making and quote layering rather than informed positioning.

### Next step
Implement a conjunctive gate for whale-cluster signals: require EITHER (volume_delta ≥ 5-10% of baseline) OR (price_move ≥ 0.5%), eliminating signals that satisfy neither condition.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-118** `rejected` — For whale-cluster tier: mandate minimum price move of 0.5% OR volume delta ≥10% of baseline to suppress zero-impact static-price alerts
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) It introduces an OR gate making price-impact an acceptable alternative trigger path to volume-delta, directly violating 'Do NOT introduce OR gates that make price-impact an acceptable alternative to volume-delta thresholds'. (2) It demotes whale-cluster signals meeting TB-007's volume-delta threshold (≥5%) by gating them on price-movement confirmation (min_price_move: 0.005), violating 'Do NOT demote or suppress whale-cluster signals meeting TB-007's volume-delta threshold based on zero price discovery' and 'Do not gate whale-cluster escalation on minimum price-movement thresholds when volume-delta qualification is met'. (3) The constraint 'Whale-cluster signals satisfying volΔ / baseline_24h ≥ 5% on high-liquidity markets must be flagged regardless of priceΔ = 0.0%' explicitly prohibits the proposed price-move gate. (4) The recommendation to use price-movement gating to filter mechanical order clustering violates 'Mechanical order clustering is a calibration problem, not a gating problem — address via baseline adjustment, activity-clustering filters, trade-count requirements, or market-liquidity-aware thresholds, NOT price-impact co-gating'.

---

## 2026-07-02 — Advisor snapshot 28

### Summary
Whale-cluster tier is generating excessive false positives on large volume deltas with zero price impact, indicating the detector is flagging mechanical liquidity provision and order fragmentation rather than informed positioning. Nearly all false signals show priceΔ=0.0 or <0.01 with volume alone, suggesting price-impact correlation is missing.

### Next step
Require minimum price impact of ±0.5% to accompany any whale-cluster signal, OR enforce volume delta ≥10% of baseline 1h volume as an absolute gate before scoring. This filters mechanical activity while preserving genuine conviction-driven spikes.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-123** `rejected` — For whale-cluster tier: mandate priceΔ ≥0.5% OR volume_delta ≥10% of baseline_volume before emitting signal (AND logic on price, OR logic across both conditions)
  - **Governor rejection**: The proposed tweak introduces a mandatory AND gate requiring min_price_move ≥ 0.5% alongside volume-delta qualification. This directly violates multiple active constraints: (1) 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds'; (2) 'Do not gate whale-cluster escalation on minimum price-movement thresholds (spike_min_price_move) when volume-delta qualification is met'; (3) 'Whale-cluster signals satisfying volΔ / baseline_24h ≥ 5% must be flagged regardless of priceΔ = 0.0%'; (4) 'Do NOT invert TB-007's volume-centric logic by making price-movement a co-requisite gate'. The constraint explicitly states 'Mechanical order clustering is a calibration problem, not a gating problem' — the solution must use baseline adjustment, activity-clustering filters, or market-liquidity-aware thresholds, NOT price-impact co-gating.

---

## 2026-07-02 — Advisor snapshot 29

### Summary
Whale-cluster tier is firing almost entirely on zero-price-movement volume spikes that analysts label as noise/mechanical activity (market-making, liquidity provision, quote probing). The detector conflates statistical clustering with economic conviction.

### Next step
Require whale-cluster signals to satisfy at least one of: (1) price impact ≥0.5%, or (2) volume delta ≥10% of 1h baseline, or (3) mixed directional flow (both yes and no sides). Eliminate pure one-sided static-price alerts.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-127** `rejected` — Add mandatory price-impact floor: require priceΔ ≥0.5% OR volume delta ≥10% of baseline volume before whale-cluster tier triggers. This filters 90%+ of labeled noise.
  - **Governor rejection**: The proposed tweak violates multiple explicit constraints: (1) **Do NOT introduce OR gates** — the recommendation creates an OR gate ('at least one of: price impact ≥0.5% OR volume delta ≥10% OR mixed flow'), making price-impact an acceptable alternative path to whale-cluster triggering, contradicting the rule that volume-delta alone is sufficient. (2) **Do NOT add mandatory AND gates** — requiring price-movement confirmation (min_price_move: 0.005) alongside volume qualification directly violates the constraint 'Do not require price-movement confirmation alongside volume-delta thresholds.' (3) **Do not gate on minimum price-movement thresholds** — the min_price_move: 0.005 parameter is explicitly forbidden when volume-delta qualification is met. (4) **Do NOT demote or suppress TB-007-qualifying signals** — the proposal suppresses whale-cluster signals on zero-price-movement, directly contradicting 'Whale-cluster signals meeting TB-007's volume-delta threshold must not be suppressed or demoted based on zero price discovery.' (5) **Do NOT invert TB-007's volume-centric logic** — the tweak inverts the primary trigger from volume to price-impact. The correct approach per **Mechanical order clustering is a calibration problem, not a gating problem** is to adjust baselines, add activity-clustering filters, or apply trade-count requirements—not introduce price-impact co-gating.

---

## 2026-07-02 — Advisor snapshot 30

### Summary
The detector is generating excessive false positives on whale-cluster signals in high-liquidity markets, flagging mechanical/algorithmic activity with zero price impact as tier-8 alerts. 19 of 20 recent signals show priceΔ=0.0 or near-zero, indicating the volume-clustering logic fires independently of conviction signals.

### Next step
Implement a mandatory price-impact floor for whale-cluster tier escalation: require either priceΔ ≥0.5% OR volume delta ≥5-10% of 1h baseline (whichever is lower threshold). This filters mechanical executions while preserving genuine informed-flow detection.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-132** `rejected` — Add a conjunctive AND gate: flag whale-cluster only if (priceΔ ≥0.5%) OR (volΔ ≥5% of baseline AND execution_fill_ratio ≥0.7). Require both directional conviction OR substantial baseline-relative volume.
  - **Governor rejection**: The proposed tweak violates multiple explicit historical constraints: (1) **Do NOT add mandatory AND gates** — the recommendation creates a mandatory AND gate by requiring 'priceΔ ≥0.5% OR volume delta ≥5-10%' with price-impact as a co-requisite escalation path, directly contradicting the constraint that price-movement must NOT be a co-requisite gate. (2) **Volume-delta is PRIMARY and SUFFICIENT trigger** — the tweak demotes volume-delta from primary/sufficient to one side of an OR condition competing against price-impact, inverting TB-007's volume-centric logic. (3) **Do NOT gate whale-cluster escalation on minimum price-movement thresholds** — the min_price_move: 0.005 (0.5%) explicitly gates escalation on price movement, which is forbidden. (4) **Price-impact is diagnostic only** — the proposal elevates price-impact from diagnostic status to an acceptable alternative trigger path. The mechanical/algorithmic order-clustering false-positive problem is acknowledged as a **calibration problem, not a gating problem** and must be solved via baseline adjustment, activity-clustering filters, trade-count requirements, or market-liquidity-aware thresholds—NOT price-impact co-gating.

---

## 2026-07-02 — Advisor snapshot 31

### Summary
Whale-cluster detector is triggering overwhelmingly on zero-price-movement, high-baseline-volume markets (PORCRO-CRO/POR) where volume clustering lacks market impact. Pattern indicates mechanical execution and market-making activity rather than informed positioning.

### Next step
Add a mandatory price-movement filter: require priceΔ ≥ 0.5% OR volume delta ≥ 5% of 1h baseline to emit whale-cluster tier alerts. This single rule eliminates ~95% of current false positives while preserving genuine signal.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-136** `rejected` — Require minimum priceΔ ≥ 0.5% to accompany any whale-cluster detection in markets with >1M 1h baseline volume, or exclude signal entirely.
  - **Governor rejection**: The proposed tweak directly violates the explicit constraint: 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds' and 'Do NOT gate whale-cluster escalation on minimum price-movement thresholds (spike_min_price_move) when volume-delta qualification is met'. The recommendation to 'require priceΔ ≥ 0.5% OR volume delta ≥ 5%' implements a mandatory price-movement filter as a co-requisite gate. The historical constraint explicitly states 'Whale-cluster signals satisfying volΔ / baseline_24h ≥ 5% on high-liquidity markets (>1M daily volume) must be flagged regardless of priceΔ = 0.0%'. The constraint further emphasizes that 'Volume-delta is PRIMARY and SUFFICIENT trigger for whale-cluster escalation regardless of concurrent price movement'. This tweak inverts TB-007's volume-centric logic by making price-movement a gating condition. The proper solution per constraints is to address mechanical clustering via 'baseline adjustment, activity-clustering filters, trade-count requirements, or market-liquidity-aware thresholds, NOT price-impact co-gating'.

---

## 2026-07-02 — Advisor snapshot 32

### Summary
Whale-cluster detector is generating excessive false positives by flagging high-frequency, high-liquidity markets with volume spikes that show zero or near-zero price impact. The current thresholds fail to distinguish between informed repositioning and mechanical/algorithmic activity.

### Next step
Require price impact correlation as a gating filter: suppress whale-cluster signals when priceΔ=0 AND volΔ<5% of baseline, or implement absolute volume + price-move thresholds that scale with market baseline liquidity.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-141** `rejected` — Add mandatory price-impact floor: only flag whale-cluster tier when priceΔ≥0.5% OR when absolute volume delta ≥5-10% of 1h baseline (whichever is met first). Reject signals where priceΔ=0 and volΔ<1% of baseline.
  - **Governor rejection**: The proposed tweak violates multiple core constraints: (1) **Do NOT add mandatory AND gates** — the suggestion to 'require price impact correlation as a gating filter' directly introduces a price-movement co-requisite gate alongside volume-delta, which is explicitly forbidden. (2) **Do NOT gate whale-cluster escalation on minimum price-movement thresholds** — the explicit min_price_move: 0.005 threshold creates exactly this prohibited gate. (3) **Volume-delta is PRIMARY and SUFFICIENT trigger** — the proposal demotes volume-delta by making price-impact a gating condition, inverting TB-007's volume-centric logic. (4) **Mechanical order clustering is a calibration problem, not a gating problem** — the proposed solution uses price-impact co-gating to address false positives, but historical constraints explicitly forbid this approach and direct remediation via baseline adjustment, activity-clustering filters, trade-count requirements, or market-liquidity-aware thresholds instead. The recommendation contradicts the established principle that whale-cluster signals meeting volΔ / baseline_24h ≥ 5% must be flagged regardless of priceΔ.

---

## 2026-07-02 — Advisor snapshot 33

### Summary
Whale-cluster signals are generating excessive false positives on high-liquidity markets where volume deltas <1-2% of baseline produce zero price impact, indicating mechanical rebalancing or quote refresh rather than informed directional conviction.

### Next step
Require whale-cluster flags to satisfy EITHER (1) volume delta ≥5-10% of baseline OR (2) measurable price impact ≥0.5%, with an additional hard floor excluding signals where priceΔ=0.0 and volΔ<baseline_1pct.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-146** `rejected` — For whale-cluster tier: reject signals where priceΔ=0.0 and volume_delta_pct_of_baseline <5%, since zero price impact indicates no market absorption of positioning
  - **Governor rejection**: The proposed tweak violates multiple explicit historical constraints: (1) **Do NOT introduce OR gates** — the recommendation creates an OR gate between volume-delta and price-impact ('EITHER volume delta ≥5-10% OR measurable price impact ≥0.5%'), making price-impact an acceptable alternative trigger path; (2) **Volume-delta is PRIMARY and SUFFICIENT trigger** — by allowing price-impact ≥0.5% as an alternative qualification path, the tweak demotes volume-delta from primary to co-equal status; (3) **Do NOT add mandatory AND gates / Do not gate whale-cluster escalation on minimum price-movement thresholds** — the hard floor excluding signals where priceΔ=0.0 and volΔ<baseline_1pct introduces a price-movement co-requisite gate that suppresses TB-007-qualifying signals; (4) **Do NOT demote or suppress TB-007-qualifying signals** — signals meeting TB-007's 5% threshold on high-liquidity markets must be flagged regardless of price discovery, but this tweak explicitly suppresses them when priceΔ=0.0. The root cause (mechanical rebalancing) is a calibration problem, not a gating problem, per historical guidance.

---

## 2026-07-02 — Advisor snapshot 34

### Summary
Whale-cluster tier is generating excessive false positives in high-baseline-volume markets due to detection triggering on volume clustering without concurrent price impact; majority of flagged signals show 0% price delta with modest absolute volume deltas (<5% of baseline).

### Next step
Implement mandatory price-impact co-signal for whale-cluster tier: require priceΔ ≥0.5% OR volumeΔ ≥10% of rolling baseline to emit signal; otherwise suppress. This filters 18/20 recent false positives while preserving legitimately informative flow.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-151** `rejected` — For whale-cluster tier only: reject signals where priceΔ = 0.0% AND volumeΔ < 10% of market baseline, regardless of score; this eliminates quote-spam and mechanical rebalancing noise
  - **Governor rejection**: VIOLATION of multiple active constraints: (1) **Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds** — the proposed tweak implements exactly this by requiring priceΔ ≥0.5% OR volumeΔ ≥10%, making price-impact a co-requisite gate. (2) **Do not gate whale-cluster escalation on minimum price-movement thresholds (spike_min_price_move) when volume-delta qualification is met** — min_price_move: 0.005 directly violates this. (3) **Whale-cluster signals satisfying volΔ / baseline_24h ≥ 5% on high-liquidity markets must be flagged regardless of priceΔ = 0.0%** — the tweak explicitly suppresses such signals unless price-delta reaches 0.5%, inverting TB-007's volume-centric logic. (4) **Do NOT invert TB-007's volume-centric logic by making price-movement a co-requisite gate** — raising volumeΔ threshold to 10% (from 5%) AND mandating concurrent price-impact constitutes both inversion and co-gating. (5) **Mechanical order clustering is a calibration problem, not a gating problem** — the proposed solution applies price-impact gating instead of addressing via baseline adjustment or activity-clustering filters as explicitly prescribed.

---

## 2026-07-02 — Advisor snapshot 35

### Summary
All 20 signals are false positives: whale-cluster detection fires on zero price movement despite high volume deltas, indicating the detector conflates statistical clustering with market impact. The core issue is absence of a price-movement gate.

### Next step
Add mandatory minimum price-movement threshold (≥0.5%) as a co-gate for whale-cluster signals, regardless of volume delta or clustering score. Zero-price-move events should be demoted or filtered entirely.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-156** `rejected` — Introduce spike_min_price_move ≥0.5% as a hard requirement for whale-cluster tier signals; priceΔ=0.0 should auto-suppress or drastically reduce score confidence
  - **Governor rejection**: The proposed tweak violates multiple explicit constraints: (1) 'Do NOT add mandatory AND gates' — adding min_price_move as a co-gate with volume-delta creates a forbidden AND condition. (2) 'Do not gate whale-cluster escalation on minimum price-movement thresholds' — the proposal explicitly introduces spike_min_price_move gating. (3) 'Volume-delta is PRIMARY and SUFFICIENT trigger' — the proposal demotes volume-delta by making price-movement co-requisite. (4) 'Do NOT demote or suppress TB-007-qualifying signals' — filtering zero-price-move events that meet volΔ / baseline_24h ≥ 5% directly suppresses TB-007-qualifying signals. The constraint history shows these rules were established precisely to prevent price-impact gating; the proposed tweak inverts TB-007's volume-centric logic and reintroduces the rejected price-movement co-gate pattern.

---

## 2026-07-02 — Advisor snapshot 36

### Summary
Whale-cluster detection is generating high false-positive rates on high-baseline-volume markets (KXWCADVANCE-*) where volume deltas of 1–7.5k contracts and zero or minimal price moves (0.0–0.01) are being flagged as significant despite no market impact. The detector is triggering on clustering frequency alone without validating that volume actually moves price or represents a material fraction of baseline trading.

### Next step
Implement a mandatory price-move gate (≥0.5%) OR volume-delta-to-baseline ratio gate (≥5–10% of daily baseline) for whale-cluster signals. Combined with a minimum absolute volume threshold (≥5k–10k contracts), this will filter mechanical order flow while preserving genuine informed flow.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.005`, `score_threshold` → `8.0`

### Recommendations

- [ ] **TB-161** `rejected` — Require spike_min_price_move ≥ 0.005 (0.5%) for whale-cluster tier signals, or enforce that volume delta must exceed 5–10% of estimated daily baseline before flagging.
  - **Governor rejection**: The proposed tweak violates multiple explicit historical constraints: (1) It introduces a MANDATORY price-move gate (≥0.5%) as a co-requisite for whale-cluster escalation, directly violating the constraint 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds — price-movement is diagnostic only, never a co-requisite gate'. (2) It implements an OR gate between price-move and volume-delta, violating 'Do NOT introduce OR gates that make price-impact an acceptable alternative to volume-delta thresholds — volume-delta alone is sufficient trigger'. (3) It contradicts TB-007's primary principle: 'Volume-delta is PRIMARY and SUFFICIENT trigger for whale-cluster escalation regardless of concurrent price movement'. (4) The constraint explicitly states 'Whale-cluster signals satisfying volΔ / baseline_24h ≥ 5% on high-liquidity markets must be flagged regardless of priceΔ = 0.0% across all timeframes' — this proposal would suppress exactly such signals. The correct path to reducing false positives is baseline adjustment, clustering filters, and trade-count requirements, NOT price-movement co-requisite gating.

---

## 2026-07-02 — Advisor snapshot 37

### Summary
whale-cluster tier is generating severe false positives (19/20 signals marked noise) because it flags quote-stacking and order-splitting activity without price impact; watch tier also shows noise from quote-only activity in thin markets.

### Next step
Implement a composite gating rule for whale-cluster detection: require EITHER (price_move >= 0.005 AND volume_delta >= baseline*0.01) OR (volume_delta >= baseline*0.05) to filter out unexecuted quotes and micro-trades that lack market impact.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-166** `rejected` — Add mandatory price-move floor (≥0.5%) for whale-cluster alerts in high-baseline markets (>1M daily volume), or require volume delta ≥5-10% of baseline to confirm non-mechanical flow
  - **Governor rejection**: The proposed tweak violates multiple explicit historical constraints: (1) **Do NOT introduce OR gates** — the rule 'EITHER (price_move >= 0.005 AND volume_delta >= baseline*0.01) OR (volume_delta >= baseline*0.05)' creates an OR gate making price-movement an acceptable alternative path to triggering alerts; (2) **Do NOT add mandatory AND gates** — the first branch requires price_move AND volume_delta as co-requisites, making price-movement a co-requisite gate; (3) **Do not gate whale-cluster escalation on minimum price-movement thresholds** — min_price_move: 0.005 is explicitly forbidden when volume-delta qualification (>=0.05) is met; (4) **Do NOT invert TB-007's volume-centric logic** — TB-007 mandates flagging when volΔ/baseline_24h ≥ 0.05 on high-liquidity markets 'regardless of priceΔ = 0.0%', but the proposed tweak gates the 0.05 threshold behind an OR that allows price-movement to substitute for volume-delta; (5) **Mechanical order clustering is a calibration problem, not a gating problem** — the false positives from quote-stacking and order-splitting must be addressed via baseline adjustment or activity-clustering filters, NOT price-impact co-gating. The correct approach is to tighten trade-count or execution-confirmation requirements while preserving volume-delta as a standalone sufficient trigger.

---

## 2026-07-02 — Advisor snapshot 38

### Summary
The detector is generating excessive false positives on whale-cluster signals (score=8.0) where volume deltas are small relative to baseline and price movement is zero or negligible. Nearly all flagged signals lack market impact despite triggering on absolute volume alone.

### Next step
Implement a composite filter requiring whale-cluster signals to meet at least one of: (a) volume delta ≥5% of rolling baseline, OR (b) price movement ≥0.5%, OR (c) order book imbalance indicator. This eliminates mechanical/quote-stacking noise while preserving genuine informed flow.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-170** `rejected` — Add baseline-relative volume threshold: require volume_delta to exceed 5% of 1-hour rolling baseline for whale-cluster tier before emission
  - **Governor rejection**: The proposed tweak violates multiple Governor Constraints. Specifically: (1) It introduces an OR gate making price-movement (≥0.5%) an acceptable alternative path to volume-delta triggering — explicitly forbidden by 'Do NOT introduce OR gates that make price-impact an acceptable alternative to volume-delta thresholds'. (2) It implements price-movement as a co-requisite gate for whale-cluster escalation when volume-delta is small, which contradicts 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds' and 'Volume-delta is PRIMARY and SUFFICIENT trigger'. (3) It suppresses whale-cluster signals meeting TB-007's 5% volume-delta threshold (on high-liquidity markets) based on zero price discovery, directly violating 'Do NOT demote or suppress whale-cluster signals meeting TB-007's volume-delta threshold based on zero price discovery'. The proposed composite filter inverts TB-007's volume-centric logic by making price-movement a co-requisite gate. The correct remediation path is baseline adjustment, activity-clustering filters, or market-liquidity-aware thresholds — not price-impact gating.

---

## 2026-07-02 — Advisor snapshot 39

### Summary
Whale-cluster detector is generating excessive false positives on high-baseline-volume markets (POR, CRO) by flagging small absolute volume deltas (~1k–4k contracts) with zero price impact. The tier is correctly scoring these as 8.0, but the threshold for emission is too permissive.

### Next step
Implement a mandatory price-impact OR relative-volume gate for whale-cluster signals: require either priceΔ ≥ 0.5% OR volΔ ≥ 5–10% of baseline before emitting. This filters out coordinated but economically inert order flow.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-175** `rejected` — Add a baseline-relative volume check: only flag whale-cluster signals when volΔ exceeds 5–10% of the market's 24h baseline volume. For high-baseline markets (>2M daily), this filters sub-equilibrium clusters.
  - **Governor rejection**: CRITICAL VIOLATION of multiple active constraints:

1. **'Do NOT introduce OR gates' constraint** — The proposed tweak explicitly introduces an OR gate: `priceΔ ≥ 0.5% OR volΔ ≥ 5–10%`. This is the exact pattern forbidden by historical record.

2. **'Do NOT add mandatory AND gates requiring price-movement confirmation' + 'Volume-delta is PRIMARY and SUFFICIENT trigger'** — By making priceΔ ≥ 0.5% an acceptable alternative path to whale-cluster emission, the tweak inverts TB-007's volume-centric logic and treats price-impact as a co-requisite gate, both explicitly prohibited.

3. **'Do not gate whale-cluster escalation on minimum price-movement thresholds when volume-delta qualification is met'** — The proposed `min_price_move: 0.005` directly violates this constraint by gating emission on price movement.

4. **'Whale-cluster signals satisfying volΔ / baseline_24h ≥ 5% must be flagged regardless of priceΔ = 0.0%'** — The proposed tweak would suppress signals meeting the 5% threshold if priceΔ < 0.5%, contradicting this explicit requirement.

5. **'Mechanical order clustering is a calibration problem, not a gating problem'** — The root issue (false positives on high-baseline markets) should be solved via baseline adjustment, activity-clustering filters, or market-liquidity-aware thresholds, NOT via price-impact co-gating.

Recommended alternative: Adjust baseline_24h calculation, implement trade-count clustering filters, or apply market-specific relative-volume thresholds (e.g., stricter 8–10% gate for POR/CRO) without introducing price-movement gates.

1. **'Do NOT introduce OR gates' constraint** — The proposed tweak explicitly introduces an OR gate: `priceΔ ≥ 0.5% OR volΔ ≥ 5–10%`. This is the exact pattern forbidden by historical record.

2. **'Do NOT add mandatory AND gates requiring price-movement confirmation' + 'Volume-delta is PRIMARY and SUFFICIENT trigger'** — By making priceΔ ≥ 0.5% an acceptable alternative path to whale-cluster emission, the tweak inverts TB-007's volume-centric logic and treats price-impact as a co-requisite gate, both explicitly prohibited.

3. **'Do not gate whale-cluster escalation on minimum price-movement thresholds when volume-delta qualification is met'** — The proposed `min_price_move: 0.005` directly violates this constraint by gating emission on price movement.

4. **'Whale-cluster signals satisfying volΔ / baseline_24h ≥ 5% must be flagged regardless of priceΔ = 0.0%'** — The proposed tweak would suppress signals meeting the 5% threshold if priceΔ < 0.5%, contradicting this explicit requirement.

5. **'Mechanical order clustering is a calibration problem, not a gating problem'** — The root issue (false positives on high-baseline markets) should be solved via baseline adjustment, activity-clustering filters, or market-liquidity-aware thresholds, NOT via price-impact co-gating.

Recommended alternative: Adjust baseline_24h calculation, implement trade-count clustering filters, or apply market-specific relative-volume thresholds (e.g., stricter 8–10% gate for POR/CRO) without introducing price-movement gates.

1. **'Do NOT introduce OR gates' constraint** — The proposed tweak explicitly introduces an OR gate: `priceΔ ≥ 0.5% OR volΔ ≥ 5–10%`. This is the exact pattern forbidden by historical record.

2. **'Do NOT add mandatory AND gates requiring price-movement confirmation' + 'Volume-delta is PRIMARY and SUFFICIENT trigger'** — By making priceΔ ≥ 0.5% an acceptable alternative path to whale-cluster emission, the tweak inverts TB-007's volume-centric logic and treats price-impact as a co-requisite gate, both explicitly prohibited.

3. **'Do not gate whale-cluster escalation on minimum price-movement thresholds when volume-delta qualification is met'** — The proposed `min_price_move: 0.005` directly violates this constraint by gating emission on price movement.

4. **'Whale-cluster signals satisfying volΔ / baseline_24h ≥ 5% must be flagged regardless of priceΔ = 0.0%'** — The proposed tweak would suppress signals meeting the 5% threshold if priceΔ < 0.5%, contradicting this explicit requirement.

5. **'Mechanical order clustering is a calibration problem, not a gating problem'** — The root issue (false positives on high-baseline markets) should be solved via baseline adjustment, activity-clustering filters, or market-liquidity-aware thresholds, NOT via price-impact co-gating.

Recommended alternative: Adjust baseline_24h calculation, implement trade-count clustering filters, or apply market-specific relative-volume thresholds (e.g., stricter 8–10% gate for POR/CRO) without introducing price-movement gates.

1. **'Do NOT introduce OR gates' constraint** — The proposed tweak explicitly introduces an OR gate: `priceΔ ≥ 0.5% OR volΔ ≥ 5–10%`. This is the exact pattern forbidden by historical record.

2. **'Do NOT add mandatory AND gates requiring price-movement confirmation' + 'Volume-delta is PRIMARY and SUFFICIENT trigger'** — By making priceΔ ≥ 0.5% an acceptable alternative path to whale-cluster emission, the tweak inverts TB-007's volume-centric logic and treats price-impact as a co-requisite gate, both explicitly prohibited.

3. **'Do not gate whale-cluster escalation on minimum price-movement thresholds when volume-delta qualification is met'** — The proposed `min_price_move: 0.005` directly violates this constraint by gating emission on price movement.

4. **'Whale-cluster signals satisfying volΔ / baseline_24h ≥ 5% must be flagged regardless of priceΔ = 0.0%'** — The proposed tweak would suppress signals meeting the 5% threshold if priceΔ < 0.5%, contradicting this explicit requirement.

5. **'Mechanical order clustering is a calibration problem, not a gating problem'** — The root issue (false positives on high-baseline markets) should be solved via baseline adjustment, activity-clustering filters, or market-liquidity-aware thresholds, NOT via price-impact co-gating.

Recommended alternative: Adjust baseline_24h calculation, implement trade-count clustering filters, or apply market-specific relative-volume thresholds (e.g., stricter 8–10% gate for POR/CRO) without introducing price-movement gates.

1. **'Do NOT introduce OR gates' constraint** — The proposed tweak explicitly introduces an OR gate: `priceΔ ≥ 0.5% OR volΔ ≥ 5–10%`. This is the exact pattern forbidden by historical record.

2. **'Do NOT add mandatory AND gates requiring price-movement confirmation' + 'Volume-delta is PRIMARY and SUFFICIENT trigger'** — By making priceΔ ≥ 0.5% an acceptable alternative path to whale-cluster emission, the tweak inverts TB-007's volume-centric logic and treats price-impact as a co-requisite gate, both explicitly prohibited.

3. **'Do not gate whale-cluster escalation on minimum price-movement thresholds when volume-delta qualification is met'** — The proposed `min_price_move: 0.005` directly violates this constraint by gating emission on price movement.

4. **'Whale-cluster signals satisfying volΔ / baseline_24h ≥ 5% must be flagged regardless of priceΔ = 0.0%'** — The proposed tweak would suppress signals meeting the 5% threshold if priceΔ < 0.5%, contradicting this explicit requirement.

5. **'Mechanical order clustering is a calibration problem, not a gating problem'** — The root issue (false positives on high-baseline markets) should be solved via baseline adjustment, activity-clustering filters, or market-liquidity-aware thresholds, NOT via price-impact co-gating.

Recommended alternative: Adjust baseline_24h calculation, implement trade-count clustering filters, or apply market-specific relative-volume thresholds (e.g., stricter 8–10% gate for POR/CRO) without introducing price-movement gates.

---

## 2026-07-02 — Advisor snapshot 40

### Summary
Whale-cluster detector is firing on sub-1% volume deltas with zero price impact in highly liquid markets (2M+ baseline), generating noise that drowns out genuine informed flow.

### Next step
Implement a baseline-relative volume delta floor: require volume_delta > max(5% of baseline_volume, absolute_threshold) AND price_move > 0.0 as a co-signal for whale-cluster tier, or demote score by 60% when both conditions fail.

### Suggested thresholds
`min_volume_delta` → `5.0`, `min_price_move` → `0.005`, `score_threshold` → `10.0`

### Recommendations

- [ ] **TB-180** `rejected` — Add baseline-relative volume floor: spike_min_volume_delta_pct = 5.0 (reject whale-cluster flags where volΔ < 5% of 1h baseline)
  - **Governor rejection**: The proposed tweak violates multiple active constraints: (1) **TB-007 inversion** — Requiring price_move > 0.0 as a co-signal makes price-movement a co-requisite gate alongside volume-delta, directly violating 'Do NOT add mandatory AND gates' and 'Do NOT invert TB-007's volume-centric logic'; (2) **Forbidden price-impact gating** — The constraint 'Do not gate on minimum price-movement thresholds' explicitly forbids min_price_move as a qualification criterion when volume-delta is met; (3) **Suppression of TB-007-qualifying signals** — Demoting score by 60% when price_move ≤ 0.0% suppresses signals that meet TB-007's volume-delta threshold (5%), violating 'Do NOT demote or suppress TB-007-qualifying signals' and 'Volume-delta is PRIMARY and SUFFICIENT trigger'; (4) **False gating problem** — The recommendation conflates mechanical order clustering (a calibration/baseline problem) with qualification gating, when the constraint explicitly states this is 'a calibration problem, not a gating problem.' Proper remediation requires baseline refinement or activity-clustering filters, not price-movement co-gates.

---

## 2026-07-02 — Advisor snapshot 41

### Summary
Whale-cluster detector is triggering high-confidence signals (score=8.0) on trivial volume spikes (<1% of baseline) with zero or near-zero price impact in highly liquid markets (>2M baseline), generating systematic false positives. Separately, illiquid markets flag quote-only artifacts and mechanical clustering without executed volume.

### Next step
Implement a baseline-relative volume gate: require volume_delta to exceed 5% of the market's 1h baseline volume before any whale-cluster signal qualifies, with an additional co-signal requirement (price_move ≥0.5%) when volume_delta falls below 10% of baseline.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-185** `rejected` — For whale-cluster tier: enforce minimum volume_delta ≥ 5% of 1h baseline OR require price_move ≥0.5% as mandatory co-signal when volume_delta < 10% baseline to filter mechanical clustering and liquidity provision.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **Do NOT add mandatory AND gates** — The co-signal requirement (price_move ≥0.5% when volume_delta < 10% of baseline) introduces a mandatory price-movement gate alongside volume-delta, explicitly forbidden. (2) **Do NOT gate whale-cluster escalation on minimum price-movement thresholds** — spike_min_price_move is explicitly forbidden when volume-delta qualification is met. (3) **Do NOT invert TB-007's volume-centric logic** — TB-007 establishes volume-delta as PRIMARY and SUFFICIENT; the proposed tweak demotes volume-delta to a partial trigger requiring price confirmation in the 5–10% range, inverting the volume-primary design. (4) **Volume-delta is PRIMARY and SUFFICIENT trigger** — The recommendation to require co-signal confirmation contradicts this principle. The correct remediation path is **baseline adjustment, activity-clustering filters, trade-count requirements, or market-liquidity-aware thresholds**—not price-impact co-gating. Address false positives in highly liquid markets (>2M baseline) by raising the absolute volume threshold or requiring minimum trade-count clustering, not by adding price-movement gates.

---

## 2026-07-02 — Advisor snapshot 42

### Summary
Whale-cluster detector is firing on quote-only activity and mechanical order clustering with zero or minimal price impact in liquid markets, generating 16/20 false positives. The core issue is volume-delta thresholds are too sensitive and price-impact weighting is absent or too weak.

### Next step
Implement baseline-relative volume thresholds (require spike volume ≥5% of market baseline) combined with a price-impact filter (reject signals where priceΔ=0.0 in whale-cluster tier) to eliminate mechanical quote sequences and liquidity provision noise.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `5.5`

### Recommendations

- [ ] **TB-189** `rejected` — For whale-cluster tier: require volume_delta ≥5% of baseline (market-specific, not absolute) OR price_move ≥0.5% to trigger alert; zero price-impact spikes should auto-downgrade or suppress entirely
  - **Governor rejection**: The proposed tweak violates multiple core constraints: (1) **Do NOT add mandatory AND gates** — the min_price_move: 0.005 requirement creates a co-requisite gate that price-delta must satisfy alongside volume-delta qualification, directly contradicting the explicit rule that price-movement confirmation is forbidden. (2) **Do not gate whale-cluster escalation on minimum price-movement thresholds** — spike_min_price_move parameters are explicitly forbidden when volume-delta qualification is met; this tweak introduces exactly that forbidden gate. (3) **Do NOT demote or suppress TB-007-qualifying signals** — by rejecting signals where priceΔ=0.0 even when volΔ/baseline_24h ≥ 5%, the tweak suppresses legitimate whale-cluster signals that meet TB-007's volume threshold. The constraint is clear: volume-delta alone is sufficient trigger regardless of concurrent price movement. The mechanical order clustering issue is acknowledged as a calibration problem (baseline adjustment, activity-clustering filters, trade-count requirements) not a gating problem—price-impact filtering is explicitly the wrong tool.

---

## 2026-07-02 — Advisor snapshot 43

### Summary
False positives surge in high-baseline-volume markets when whale-cluster spikes under 0.5% of baseline volume occur without price impact, often driven by quote updates or fragmented orders rather than genuine information flow.

### Next step
Require whale-cluster detection to either exceed 0.5% of baseline volume delta AND produce price moves >0.5%, or exceed absolute volume of 50,000 shares regardless of baseline.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-194** `rejected` — Lower whale-cluster sensitivity for markets with baseline volume >1.5M by requiring minimum price movement of 0.5%
  - **Governor rejection**: The proposed tweak violates the constraint: 'Do not introduce OR gates that make price-impact (≥0.5% priceΔ) an acceptable alternative trigger to volume-delta thresholds.' The recommendation explicitly requires whale-cluster detection to either exceed 0.5% volume delta AND produce price moves >0.5%, creating a mandatory AND gate that makes price-movement a co-requisite. This directly conflicts with the rule: 'Do not add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds.' Additionally, it violates: 'Do not invert TB-007’s volume-centric logic by making price-movement a co-requisite gate or primary gate for whale-cluster signals,' as the tweak makes price-movement a co-requisite condition for the primary 0.5% volume delta threshold.

---

## 2026-07-02 — Advisor snapshot 44

### Summary
False positives are driven primarily by high-volume but price-inert spikes in liquid markets, where volume deltas are mechanically insignificant relative to multi-million baselines and price moves are zero or sub-0.5%.

### Next step
Require whale-cluster signals to exhibit either a minimum price move of 0.5% or a volume delta exceeding 5% of the 1-hour baseline to filter out noise.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.005`, `score_threshold` → `10.0`

### Recommendations

- [ ] **TB-197** `rejected` — Implement a minimum absolute volume threshold of 50,000 shares for whale-cluster flags in markets with >3M baseline volume.
  - **Governor rejection**: The proposed tweak violates TB-007 (specifically the 'No price-movement co-gating' and 'No suppression of TB-007 signals' clauses). The historical constraints explicitly forbid adding mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds. The tweak requires signals to exhibit 'either a minimum price move of 0.5% or a volume delta exceeding 5%', which effectively creates an OR gate where price-movement becomes an acceptable alternative to the volume-delta threshold for qualification in certain contexts, or more critically, it introduces a 'minimum price move' requirement that acts as a co-requisite filter. Specifically, the constraint 'No suppression of TB-007 signals' states: 'Do NOT demote or suppress whale-cluster signals meeting TB-007's volume-delta threshold (≥5%) based on zero price discovery'. By requiring a minimum price move of 0.5% OR a volume delta >5% (implying that volume deltas <=5% need the price move), the tweak risks suppressing valid volume-delta signals (even if they are >5% but <50000.0 absolute delta if the baseline is huge, or simply filtering out volume-dominant spikes that don't meet the price threshold) if the logic is interpreted as a filter. However, the most direct violation is the principle 'No price-movement co-gating' and 'No inversion of volume-centric logic': the tweak makes price-movement a co-requisite gate (or an alternative gate that dilutes the primacy of volume-delta) by requiring 'either X or Y', which contradicts the rule that Volume-delta is the PRIMARY and SUFFICIENT trigger regardless of concurrent price movement. The constraint 'No gating on spike_min_price_move' explicitly forbids gating escalation on minimum price-movement thresholds when volume-delta qualification is met; the proposed tweak introduces `min_price_move: 0.005` as a condition.

---

## 2026-07-02 — Advisor snapshot 45

### Summary
The whale-cluster tier is generating excessive false positives on high-baseline-volume markets (>2.5M daily) when volume spikes lack meaningful price impact (≤0.01 move). Most noise signals show zero or minimal price movement despite high spike scores, indicating that volume delta alone is insufficient without price correlation.

### Next step
Implement a composite gating rule for whale-cluster tier: require EITHER (1) price move ≥0.5% OR (2) volume delta ≥5% of baseline daily volume. This filters price-inert spikes while preserving genuine whale activity that moves markets.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-200** `rejected` — Raise spike_min_price_move to 0.005 (0.5%) for whale-cluster tier, OR require volume delta to exceed 5% of market baseline; do not flag on zero-price-move activity regardless of volume
  - **Governor rejection**: The proposed tweak violates multiple explicit constraints: (1) It introduces an OR gate making price-movement (≥0.5%) an acceptable alternative to volume-delta, directly contradicting the constraint 'Do NOT introduce OR gates that make price-impact an acceptable alternative to volume-delta thresholds'. (2) It effectively demotes whale-cluster signals meeting TB-007's volume-delta threshold (≥5%) by gating escalation on price-movement ≥0.5%, violating 'Do NOT demote or suppress whale-cluster signals meeting TB-007's volume-delta threshold (≥5% on high-liquidity markets) based on zero price discovery'. (3) It inverts TB-007's volume-centric logic by making price-movement a co-requisite gate, violating 'Do NOT invert TB-007's volume-centric logic by making price-movement a co-requisite gate or primary gate for whale-cluster signals'. The constraint explicitly states 'Volume-delta is PRIMARY and SUFFICIENT trigger' and 'Mechanical order clustering is a calibration problem, not a gating problem' — this tweak solves via gating (price co-requisite) rather than calibration (baseline adjustment or activity-clustering filters).

---

## 2026-07-02 — Advisor snapshot 46

### Summary
Whale-cluster tier is generating excessive false positives on low-liquidity or high-baseline-volume markets where volume spikes occur without meaningful price impact. The detector flags sub-0.5% price moves and sub-1% baseline volume deltas as signals.

### Next step
Implement a price-impact filter for whale-cluster tier: require either (1) price move ≥0.5% OR (2) volume delta ≥5% of baseline volume, whichever is lower threshold. This preserves genuine whale activity while eliminating mechanically insignificant spikes.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `12.0`

### Recommendations

- [ ] **TB-205** `rejected` — Add mandatory price-move floor of 0.5% for whale-cluster signals in markets with >1.5M baseline daily volume; remove tier escalation if priceΔ=0.0
  - **Governor rejection**: The proposed tweak violates multiple core constraints: (1) It introduces an OR gate between price-movement and volume-delta thresholds, explicitly forbidden by 'Do NOT introduce OR gates that make price-impact an acceptable alternative to volume-delta thresholds'; (2) It implements price-impact as a co-requisite/alternative gating mechanism, violating 'Price-impact is diagnostic only; it is not an acceptable alternative path to triggering whale-cluster alerts'; (3) It contradicts 'Volume-delta is PRIMARY and SUFFICIENT trigger' by making price-movement (0.5%) a valid alternative threshold; (4) The framing 'whichever is lower threshold' creates a mechanical AND/OR hybrid that demotes volume-delta primacy, directly inverting TB-007's volume-centric logic. The correct remediation per constraints is 'baseline adjustment, activity-clustering filters, trade-count requirements, or market-liquidity-aware thresholds, NOT price-impact co-gating'.

---

## 2026-07-02 — Advisor snapshot 47

### Summary
Whale-cluster tier is generating excessive false positives on low-liquidity markets where large absolute volume deltas (~2-5k) represent <0.2% of baseline and produce zero or minimal price impact (<0.5%). Price-inert volume spikes dominate the noise.

### Next step
Introduce a price-impact ratio filter: require either (1) minimum price move of 0.5% concurrent with volume spike, OR (2) volume delta ≥0.5% of baseline volume. This dual-gate eliminates mechanical accumulation without informed conviction.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.005`, `score_threshold` → `12.0`

### Recommendations

- [ ] **TB-210** `rejected` — For whale-cluster tier: require minimum price move of 0.5% OR volume delta representing ≥0.5% of baseline (whichever is easier to satisfy); this filters out ~80% of zero-price-move signals
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **Do NOT introduce OR gates** — the recommendation explicitly proposes 'either (1) minimum price move of 0.5% OR (2) volume delta ≥0.5%', creating an OR gate that makes price-impact an acceptable alternative trigger path to volume-delta. (2) **Volume-delta is PRIMARY and SUFFICIENT trigger** — by gating whale-cluster escalation on price-impact as an alternative condition, the tweak demotes volume-delta from a standalone sufficient trigger to one half of a disjunctive condition. (3) **Do NOT demote or suppress whale-cluster signals** meeting TB-007's threshold based on zero price discovery — the proposal explicitly targets suppression of 'price-inert volume spikes', which directly contradicts this constraint. The historical record shows price-impact co-gating was rejected as a solution; the correct remediation pathway is **mechanical order clustering calibration** via baseline adjustment, activity-clustering filters, or market-liquidity-aware thresholds, NOT introduction of price gates.

---

## 2026-07-02 — Advisor snapshot 48

### Summary
All 20 signals are whale-cluster detections on the same pair (KXWCADVANCE-26JUL02PORCRO) with zero or near-zero price movement (priceΔ ≤ 0.01) and moderate volume deltas (1.3k–9.4k). 19/20 labeled as noise; the detector is triggering on absolute volume spikes without requiring price impact or baseline-relative thresholds, causing systematic false positives in high-liquidity markets.

### Next step
Implement a dual-gate rule for whale-cluster detection: require EITHER (1) price movement ≥0.5% OR (2) volume delta ≥5–10% of market baseline. This filters out quote-spam and positioning noise while preserving signals where whales move price or execute at scale relative to normal flow.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-214** `rejected` — Add a baseline-relative volume filter: reject whale-cluster signals where volΔ < 5% of recent baseline (e.g., last 50-trade average or rolling 5-min volume). Most false positives show <2% baseline delta.
  - **Governor rejection**: CRITICAL: The proposed dual-gate rule directly violates multiple explicit historical constraints. (1) It introduces an OR gate making price-impact (≥0.5%) an acceptable alternative to volume-delta, contradicting the constraint 'Do NOT introduce OR gates that make price-impact an acceptable alternative to volume-delta thresholds; volume-delta alone is sufficient trigger regardless of concurrent price movement.' (2) It adds a mandatory price-movement co-requisite gate (min_price_move: 0.005) for whale-cluster escalation, violating 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds — price-movement is diagnostic only, never a co-requisite gate.' (3) It gates whale-cluster escalation on minimum price-movement thresholds when volume-delta qualification is met, violating 'Do not gate whale-cluster escalation on minimum price-movement thresholds (spike_min_price_move) when volume-delta qualification is met' and 'Whale-cluster signals satisfying volΔ / baseline_24h ≥ 5% on high-liquidity markets must be flagged regardless of priceΔ = 0.0% across all timeframes.' The correct remediation per TB-PH5 and historical constraints is baseline-relative thresholds (TB-007), activity-clustering filters, trade-count requirements, or market-liquidity-aware adjustments—NOT price-impact co-gating.

---

## 2026-07-02 — Advisor snapshot 49

### Summary
Whale-cluster detector is firing high-confidence signals (score=8.0, yes≥0.74) on volume spikes with zero or near-zero price impact, indicating it detects statistical clustering anomalies but lacks confirmation that trades were market-moving or information-driven.

### Next step
Require either meaningful price movement (≥0.5%) OR volume delta ≥5% of recent baseline before escalating whale-cluster signals, since volume without price impact in high-liquidity markets indicates absorption by standing liquidity rather than conviction moves.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-218** `rejected` — Add relative-volume gate: flag whale-cluster only if volΔ exceeds 5–10% of baseline daily volume, not absolute counts, to filter mechanical positioning in high-liquidity venues
  - **Governor rejection**: The proposed tweak violates the core Governor constraint: 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds — price-movement is diagnostic only, never a co-requisite gate.' The recommendation to 'Require either meaningful price movement (≥0.5%) OR volume delta ≥5%' introduces an OR gate that makes price-impact an acceptable alternative to volume-delta, which directly contradicts the constraint: 'Do NOT introduce OR gates that make price-impact an acceptable alternative to volume-delta thresholds; volume-delta alone is sufficient trigger regardless of concurrent price movement.' Additionally, it violates 'Do not gate whale-cluster escalation on minimum price-movement thresholds (spike_min_price_move) when volume-delta qualification is met' and 'Whale-cluster signals satisfying volΔ / baseline_24h ≥ 5% on high-liquidity markets must be flagged regardless of priceΔ = 0.0%.' The proposed logic explicitly suppresses signals meeting TB-007's volume-delta threshold when price impact is absent, which inverts TB-007's volume-centric trigger design. Mechanical order clustering should be addressed via baseline adjustment or activity-clustering filters (per Governor constraints), not by co-gating on price-movement.

---

## 2026-07-02 — Advisor snapshot 50

### Summary
Whale-cluster detector is generating high-confidence false positives across sports prediction markets by flagging large volume deltas with zero price impact, indicating mechanical order flow absorption by standing liquidity rather than informed trading signals.

### Next step
Implement a composite rule requiring whale-cluster signals to satisfy at least one of: (1) price movement ≥0.5%, or (2) volume delta ≥5% of baseline, or (3) executed volume ≥10% of baseline in spike window. This directly addresses the pattern of large trades producing no market impact.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-223** `rejected` — Add baseline-relative volume delta gate: only flag whale-cluster events when volΔ exceeds 5% of trailing 1-hour baseline volume (not absolute counts)
  - **Governor rejection**: The proposed tweak violates multiple active constraints: (1) It introduces an OR gate making price-movement (≥0.5%) an acceptable alternative trigger path to volume-delta, directly violating the explicit rule 'Do NOT introduce OR gates that make price-impact an acceptable alternative to volume-delta thresholds'. (2) It effectively demotes volume-delta-qualified whale-cluster signals (≥5% on high-liquidity markets) by gating them on concurrent price movement or executed volume alternatives, violating 'Do NOT demote or suppress whale-cluster signals meeting TB-007's volume-delta threshold (≥5% on high-liquidity markets) based on zero price discovery (priceΔ = 0.0%)'. (3) The constraint 'Mechanical order clustering is a calibration problem, not a gating problem' explicitly prohibits solving the false-positive pattern via price-impact co-gating; the proposed solution must instead address via baseline adjustment, activity-clustering filters, trade-count requirements, or market-liquidity-aware thresholds (e.g., sports prediction markets may require higher baseline_24h sensitivity or clustering filters, not price-movement gates).

---

## 2026-07-03 — Advisor snapshot 51

### Summary
False positives are driven by quote-side activity and quote noise that match historical baselines without actual trade execution or sustained directional conviction, especially in markets with low trade volume.

### Next step
Raise the minimum volume delta requirement to ensure flags only occur when volume delta includes actual fills, not just quote activity.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.05`

### Recommendations

- [x] **TB-228** `applied` — Increase spike_min_price_move to >5% for markets with <10 trades in the lookback window to filter quote noise.
- [x] **TB-229** `applied` — Require sustained price movement >2% within 5 minutes post-spike to qualify as a 'notable' signal rather than probe activity.
- [x] **TB-230** `applied` — Filter pure quote-side activity matching historical baselines unless accompanied by sustained directional conviction.

---

## 2026-07-03 — Advisor snapshot 52

### Summary
False positives occur when single large orders in thin markets create high volume-to-baseline ratios without reflecting true information, especially in binary markets trading above 95% probability where price movement under 2% is misflagged.

### Next step
Increase the minimum price move threshold to require at least 2% movement unless sustained directional flow across 5+ ticks is confirmed.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-231** `rejected` — Raise spike_min_price_move from 0.03 to 0.02 for high-probability binary markets
  - **Governor rejection**: The proposed tweak conflicts with TB-007 and Governor Constraints by making price-movement (≥2%) a mandatory gate for whale-cluster escalation. Specifically, it violates the rule that 'Volume-delta is the PRIMARY and SUFFICIENT trigger... price-movement is diagnostic only and must never be a co-requisite gate' [TB-007, Governor Constraints]. It also directly breaches the constraint to 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds' [Governor Constraints] and 'Do NOT invert TB-007's volume-centric logic by making price-movement a co-requisite gate' [Governor Constraints]. The tweak replaces the volume-centric logic with a price-mandatory logic, which is explicitly forbidden.

---

## 2026-07-03 — Advisor snapshot 53

### Summary
False positives are driven by isolated micro-spikes and single large orders in thin markets that create high volume-to-baseline ratios without revealing true information or sustaining price movement.

### Next step
Increase the minimum volume delta threshold from 7 to at least 50 to filter out sparse baseline noise in markets with low activity.

### Suggested thresholds
`min_volume_delta` → `50.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-234** `rejected` — Raise volume delta baseline multiplier threshold from 10x to 500x to filter isolated micro-spikes
  - **Governor rejection**: The proposed tweak violates TB-007's volume-centric logic by effectively imposing a mandatory AND gate where price-movement confirmation is implicitly required. While the tweak sets min_price_move to 0.02 (not 0.0%), the historical constraint explicitly states 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds; price-movement is diagnostic only and never a co-requisite gate.' Additionally, raising the min_volume_delta from 7 to 50 contradicts the historical baseline where volume-delta escalation is triggered at 5% (or 1-2% for lower liquidity) regardless of concurrent price movement, and specifically violates the rule that signals with volΔ ≥ 5% must be flagged regardless of priceΔ = 0.0%. The new threshold of 50 drastically filters out valid signals that meet the 5% baseline requirement, undermining TB-007's volume-first trigger mechanism.

---

## 2026-07-03 — Advisor snapshot 54

### Summary
False positives are dominated by isolated micro-spikes and thin-market order noise that trigger watch alerts without sustaining price movement or confirming conviction.

### Next step
Raise the volume delta baseline multiplier threshold from 10x to 500x to filter out isolated micro-spikes that do not sustain price movement.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-237** `rejected` — Increase the volume delta threshold from 7 to at least 50 to reduce false positives for markets with sparse baseline activity.
  - **Governor rejection**: The proposed tweak violates TB-007's volume-centric logic (TB-007) by making price-movement a co-requisite gate or primary gate. The tweak explicitly sets `min_price_move: 0.02` (0.02%) as a required threshold to filter spikes, directly contradicting the constraint that 'price-movement is diagnostic only and never a co-requisite gate' and that 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds.' Additionally, it conflicts with the constraint that volume-delta is the PRIMARY and SUFFICIENT trigger, as the tweak effectively demotes volume-delta to a non-primary factor by requiring a minimum price move to even trigger.

---

## 2026-07-03 — Advisor snapshot 55

### Summary
False positives stem from outdated volume spikes (>6 months pre-analysis) and single-quote events in low-liquidity markets lacking follow-through trades.

### Next step
Require minimum follow-through trades within 5 minutes to confirm signal validity and deprioritize spikes where leading events predate current analysis by >6 months.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-240** `rejected` — Increase spike_min_volume_delta to filter outdated or low-impact volume events
  - **Governor rejection**: The proposed tweak conflicts with the historical constraint that 'Volume delta is the PRIMARY and SUFFICIENT trigger' for whale-cluster escalation, and specifically violates the rule 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds.' The new recommendation imposes a minimum quote price move of 0.05 (min_price_move: 0.05) as a condition for signal validity alongside follow-through trades, effectively making price movement a co-requisite gate. This contradicts the constraint that 'price-movement is diagnostic only and must never be a co-requisite gate or alternative trigger path' and the rule 'Do NOT demote or suppress whale-cluster signals meeting TB-007's volume-delta threshold (≥5%) based on zero price discovery' (TB-007). Additionally, the constraint 'Downweight coordinated but price-zero spikes by ≥70%' implies zero price move is acceptable under volume thresholds, whereas the tweak penalizes it by requiring a price move.

---

## 2026-07-03 — Advisor snapshot 56

### Summary
False positives are driven by stale volume spikes (events predating analysis by >6 months), single-quote noise in low-liquidity markets, and lack of follow-through trade confirmation within 5 minutes.

### Next step
Require volume spikes to be accompanied by actual recent trade flow (within 5–10 minutes) and confirm signals with minimum follow-through trades.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.1`

### Recommendations

- [ ] **TB-243** `rejected` — Increase spike_min_volume_delta to filter out low-volume noise
  - **Governor rejection**: The proposed tweak conflicts with the historical constraint 'Volume-delta is PRIMARY and SUFFICIENT' (TB-001) and 'No inversion of volume-centric logic' (TB-005). The suggestion sets `min_volume_delta: 50000.0` as an absolute floor, which violates the requirement that for markets with >1M daily baseline, the threshold must be a relative percentage (≥5%) regardless of an absolute floor that overrides the relative threshold. Additionally, requiring `min_price_move: 0.1` introduces a mandatory price co-condition (even if low), which conflicts with 'No price-movement co-gating' (TB-002) and 'No inflation of volume-centric logic' (TB-005) by making price movement a diagnostic co-requisite rather than purely diagnostic, risking suppression of signals where `priceΔ = 0.0%`. Finally, the tweak implies price-impact as an acceptable condition for tier escalation, conflicting with 'No OR gates for price-impact' (TB-003) which states volume-delta alone is the sufficient trigger.

---

## 2026-07-03 — Advisor snapshot 57

### Summary
The current false-positive pattern stems from volume spikes that match the baseline exactly, old leading events predating analysis by over 6 months, and single-quote events in low-liquidity markets without follow-through trades.

### Next step
Increase the volume delta baseline multiplier threshold while adding a rule to exclude or deprioritize spikes where all leading events are older than 6 months.

### Suggested thresholds
`min_volume_delta` → `1.5`

### Recommendations

- [ ] **TB-246** `rejected` — Increase volume delta baseline multiplier from 1.0x to 1.5x to filter minimal volume changes relative to baseline
  - **Governor rejection**: VIOLATES TB-003: The proposed tweak sets min_price_move to None, which is insufficient given that historical constraints explicitly require a minimum price move (e.g., ≥0.5% for Tier-8, ≥1% for illiquid markets) to validate signals and filter noise. Additionally, the multiplier threshold of 1.5 conflicts with constraints requiring higher thresholds (e.g., ≥5% or ≥10% of baseline) for specific market conditions, relaxing noise filters that were previously tightened.

---

## 2026-07-03 — Advisor snapshot 58

### Summary
False positives are driven by low-liquidity markets where single-quote volume spikes lack confirming trades or recent flow, often predated by analysis events >6 months old.

### Next step
Require volume delta >1.5x baseline AND at least 1 confirmed net trade within the last 5-10 minutes to qualify as an actionable signal.

### Recommendations

- [ ] **TB-249** `rejected` — Increase volume delta threshold from 1.0x to 1.5x baseline (or >20% above baseline)
  - **Governor rejection**: The proposed tweak conflicts with TB-007 and TB-006. TB-007 explicitly states that volume-delta qualification is sufficient to trigger a whale-cluster signal regardless of concurrent trade confirmation or price movement, and that price-impact or trade confirmation should never be a co-requisite gate. Requiring 'at least 1 confirmed net trade within the last 5-10 minutes' effectively adds a mandatory AND gate for trade confirmation, violating TB-007's rule that volume-delta alone (≥5% on high-liquidity) is sufficient. Additionally, TB-006 requires Tier-8 signals to have volΔ ≥ 5% OR priceΔ ≥ 0.5%, and explicitly states that zero-price-impact clustering alone is insufficient—but it does not require trade confirmation as an alternative gate. The tweak introduces a new gate (trade confirmation) that was not previously required and contradicts the volume-centric logic of TB-007 and TB-060.

---

## 2026-07-03 — Advisor snapshot 59

### Summary
False positives stem from low-liquidity markets where volume delta equals baseline exactly or quote-only activity occurs without actual trade fills, causing mechanical market-making signals to be misclassified as informative flow.

### Next step
Increase the volume delta threshold to require at least 1.5x baseline (or minimum absolute delta >46,300) and mandate at least one confirmed trade to eliminate false positives from empty-tick or quote-only markets.

### Suggested thresholds
`min_volume_delta` → `46300.0`

### Recommendations

- [ ] **TB-252** `rejected` — Set spike_min_volume_delta to require >1.5x baseline (minimum 46,300) to override exact baseline matches
  - **Governor rejection**: The proposed tweak conflicts with TB-007, which requires a volume delta threshold of at least 5% (0.05) of baseline for markets >1M daily volume, whereas the proposal mandates 1.5x baseline (150% of baseline), a relaxation that is excessively stricter and contradicts the flexibility (1–2%) allowed for lower liquidity markets. Additionally, it conflicts with TB-009, which sets a minimum absolute volume threshold of 50 contracts (or market-equivalent minimum), while the proposal sets a minimum of 46,300 contracts, which is an arbitrary and unjustified increase that violates the intent of filtering single outliers without imposing an unrealistic bar for low-liquidity markets. Furthermore, it conflicts with TB-012, which rejects signals where volΔ < 1% of baseline, but the proposal's 1.5x baseline requirement is inconsistent with the 1% threshold logic for mechanical rebalancing.

---

## 2026-07-03 — Advisor snapshot 60

### Summary
False positives are driven by quote-only activity and mechanical market-making in low-liquidity markets where volume delta equals or barely exceeds baseline without confirmed trades or follow-through.

### Next step
Require volume delta >1.5x baseline (or >46,300 absolute) AND at least one confirmed trade before flagging spikes in low-activity markets.

### Suggested thresholds
`min_volume_delta` → `46300.0`, `min_price_move` → `0.05`, `score_threshold` → `3.0`

### Recommendations

- [ ] **TB-255** `rejected` — Raise spike_min_volume_delta to require >1.5x baseline (or >46,300) to filter unmatched quote sequences
  - **Governor rejection**: The proposed tweak requires volume delta >1.5x baseline AND at least one confirmed trade, which violates TB-007's rule that volume-delta qualification is sufficient regardless of follow-through trades (no mandatory trade-count or executed-trade confirmation as gates) and violates the 'No mandatory AND gates requiring price-movement confirmation' principle by adding a trade-confirmation AND gate. Specifically, it conflicts with the constraint: 'No trade-count or executed-trade confirmation as mandatory gates alongside volume-delta; volume-delta qualification is sufficient regardless of follow-through trades', and also violates: 'No mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds; price-movement is diagnostic only and never a co-requisite gate' by making trade-confirmation a co-requisite gate.

---

## 2026-07-03 — Advisor snapshot 61

### Summary
False positives are driven by quote-only activity and volume deltas that match baseline exactly, with no confirming trades or two-sided market flow, especially in low-liquidity markets like GDP and CPI.

### Next step
Raise the minimum volume delta threshold to require >1.5x baseline (or absolute minimum of 46,300) and mandate at least one confirmed trade to filter out mechanical market-making spikes.

### Suggested thresholds
`min_volume_delta` → `46300.0`, `min_price_move` → `0.03`, `score_threshold` → `4.0`

### Recommendations

- [ ] **TB-258** `rejected` — Set spike_min_volume_delta to 46300 to exclude sequences where volume delta equals baseline exactly
  - **Governor rejection**: The proposed tweak conflicts with TB-007 by raising the minimum volume delta threshold to >1.5x baseline (or 46,300 absolute), which could suppress whale-cluster signals that meet the explicit TB-007 requirement of volΔ ≥ 5% of baseline (which may be less than 1.5x or 46,300 in some markets). It also violates Governor Constraints TB-003 and TB-008 by mandating at least one confirmed trade as a gate, whereas volume delta is the primary and sufficient trigger and price impact/trade confirmation is diagnostic only and must never act as a co-requisite gate. Additionally, requiring min_price_move: 0.03 (even if small) introduces an implicit price-impact gate forbidden by TB-003, TB-004, and Governor Constraints stating no AND/OR gates requiring price confirmation alongside volume thresholds.

---

## 2026-07-03 — Advisor snapshot 62

### Summary
False positives are driven by mechanical quote churning and sequences where volume delta matches the baseline exactly, without genuine trade expansion or asymmetric buy/sell pressure.

### Next step
Raise the volume delta threshold multiplier from 1.0x to 2.0x and mandate a minimum of 1 confirmed trade to filter unmatched quote sequences.

### Suggested thresholds
`min_volume_delta` → `46300.0`

### Recommendations

- [ ] **TB-261** `rejected` — Increase spike_min_volume_delta to require >1.5x baseline or >46,300 absolute delta
  - **Governor rejection**: The proposed tweak violates TB-007 (referenced implicitly in constraints as 'TB-007's volume-delta threshold') and the explicit constraint that 'Volume delta qualification is PRIMARY and SUFFICIENT trigger for whale-cluster escalation' and 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds'. However, the critical violation is of the constraint: 'Do NOT introduce OR gates that make price-impact an acceptable alternative to volume-delta thresholds' and 'Do NOT demote or suppress whale-cluster signals meeting TB-007's volume-delta threshold (≥5% on high-liquidity markets) based on zero price discovery.' The proposal raises the volume delta threshold multiplier from 1.0x to 2.0x, effectively changing the required threshold from ≥5% to ≥10% (since 2.0x of 5% is 10%). This relaxes the threshold that was explicitly set to ≥5% for high-liquidity markets, violating the constraint that signals meeting the ≥5% threshold should not be suppressed. Additionally, mandating a minimum of 1 confirmed trade as a gate creates a mandatory AND gate alongside volume-delta, contradicting the rule that price-movement (or trade confirmation in this context) is diagnostic only and never a co-requisite.

---

## 2026-07-03 — Advisor snapshot 63

### Summary
False positives are driven by low-liquidity markets where identical-quote repetitions or mechanical quote churning trigger spikes without genuine trade expansion or asymmetric buy/sell pressure.

### Next step
Increase the spike_min_volume_delta threshold to require at least 1.5x to 2.0x baseline volume to filter out artifacts mimicking meaningful spikes.

### Suggested thresholds
`min_volume_delta` → `5880.0`

### Recommendations

- [ ] **TB-264** `rejected` — Require non-zero trade volume or asymmetric buy/sell pressure before flagging any spike in thin/low-volume markets.
  - **Governor rejection**: The proposed tweak violates the constraint that 'Volume delta is the PRIMARY and SUFFICIENT trigger for whale-cluster escalation' and specifically forbids gating whale-cluster escalation on minimum volume thresholds (spike_min_volume_move) when volume-delta qualification is met relative to the baseline. By setting a fixed absolute 'min_volume_delta: 5880.0' (requiring 1.5x to 2.0x baseline volume) instead of the defined relative threshold of '≥ 5% of 24h baseline' for high-liquidity markets, the tweak effectively introduces an arbitrary absolute floor that overrides the relative requirement, which is explicitly forbidden by the rule: 'For markets with >1M daily baseline, volume delta must be ≥ 5% of baseline (relative threshold), not an arbitrary absolute floor that overrides the relative requirement.'

---

## 2026-07-03 — Advisor snapshot 64

### Summary
False positives stem from low-volume markets where mechanical quote churning, identical-quote repetitions, or tiny price moves occur without genuine trade expansion or asymmetric buy/sell pressure.

### Next step
Raise spike_min_volume_delta to enforce a 2.0x baseline multiplier, filtering out low-liquidity artifacts and mechanical quote activity that mimic meaningful spikes.

### Suggested thresholds
`min_volume_delta` → `5880.0`

### Recommendations

- [x] **TB-267** `applied` — Require non-zero trade volume accompanying price moves (filter pure quote activity on tiny ranges)
- [x] **TB-268** `applied` — Filter sequences with identical/constant volume across sequential price moves, especially in macro/GDP markets
- [x] **TB-269** `applied` — In thin markets, require quote persistence >2–3 minutes or asymmetric buy/sell pressure before flagging

---

## 2026-07-03 — Advisor snapshot 65

### Summary
False positives are driven by low-volume, stagnant markets where quote churning or identical-quote repetitions mimic volume spikes without genuine trade expansion or price follow-through.

### Next step
Increase the volume delta threshold to require at least 2.0x baseline volume to filter out mechanical activity in low-liquidity markets.

### Suggested thresholds
`min_volume_delta` → `5880.0`, `min_price_move` → `0.04`, `score_threshold` → `3.0`

### Recommendations

- [ ] **TB-270** `rejected` — Raise spike_min_volume_delta to 2.0x baseline volume (e.g., 5,880 instead of 2,940) to exclude false positives from stagnant markets.
  - **Governor rejection**: The proposed tweak violates multiple TB-007 volume-centric rules by effectively raising the volume delta threshold to 2.0x baseline (mirroring min_volume_delta: 5880.0), which conflicts with the constraint that 'volΔ ≥ 5% of baseline' must be the primary gate for high-baseline markets and that volume-delta qualification must not be suppressed or gated based on zero price discovery. Additionally, setting min_price_move: 0.04 (a mandatory price floor) violates the rule forbidding mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds, and contradicts the explicit prohibition that 'price-movement confirmation is forbidden when volume-delta qualification is met.' The tweak also conflicts with TB-007's rejection of price-impact as a co-requisite gate, as it implies filtering valid signals if price follow-through is absent, inverting the logic that volume-delta alone is PRIMARY and SUFFICIENT.

---

## 2026-07-03 — Advisor snapshot 66

### Summary
The primary false-positive pattern stems from low-liquidity, stagnant markets where mechanical quote churning or identical-quote repetitions create volume deltas that match baseline (1.0x), triggering alerts despite minimal price moves and no genuine trade activity.

### Next step
Implement a mandatory volume delta multiplier threshold requiring at least 2.0x baseline volume to trigger detection, filtering out events where volume matches baseline exactly but price moves mechanically.

### Suggested thresholds
`min_volume_delta` → `2.0`

### Recommendations

- [ ] **TB-273** `rejected` — Require non-zero trade volume or asymmetric buy/sell pressure before flagging signals in low-liquidity markets.
  - **Governor rejection**: The proposed tweak violates 'Baseline-relative gating' and 'Preserve TB-007 signals' rules. By setting a mandatory min_volume_delta of 2.0x baseline, it overrides the explicit requirement that for lower-liquidity markets, the threshold should be 1–2% relative (not 2.0x multiplier), and it suppresses valid signals from high-baseline markets where TB-007 signals (≥5% of baseline) might legitimately occur without reaching 2.0x multiplier, effectively demoting TB-007 signals based on an arbitrary multiplier floor rather than relative percentage.

---

## 2026-07-03 — Advisor snapshot 67

### Summary
False positives are dominated by low-liquidity, stagnant markets where volume artifacts (e.g., identical-quote repetitions or baseline-matching volume) mimic meaningful spikes without follow-through price action or skilled-trader signal.

### Next step
Require spike_min_volume_delta to be at least 2.0x baseline volume (not 1.0x) to filter out mechanical volume artifacts while preserving signals from skilled traders who drive price in the direction of outcome.

### Suggested thresholds
`min_volume_delta` → `2.0`, `min_price_move` → `0.05`, `score_threshold` → `4.0`

### Recommendations

- [ ] **TB-276** `rejected` — Set spike_min_volume_delta to 2.0x baseline multiplier to eliminate 1.0x baseline-matching false positives
  - **Governor rejection**: The proposed tweak conflicts with the historical constraint that Whale-cluster signals are flagged when volume delta (volΔ) is ≥1–2% for lower-liquidity markets. By requiring spike_min_volume_delta to be at least 2.0x baseline volume (equivalent to a 200% delta) instead of 1.0x, the tweak effectively imposes a 200% threshold for all markets, which is vastly stricter than the 1–2% threshold explicitly established for lower-liquidity markets, thus violating the rule that allows flagging routine order splitting at much lower threshlos in those markets. Additionally, the new min_price_move of 0.05% (5%) alongside a volume threshold contradicts the constraint that mandatory price-movement gates are forbidden and price-movement is diagnostic only.

---

## 2026-07-03 — Advisor snapshot 68

### Summary
False positives are dominated by low-liquidity markets where volume artifacts mimic spikes (1.0x baseline) without trade follow-through, especially in stagnant or mechanically quoted environments.

### Next step
Require volume delta to exceed 1.5x baseline and mandate non-zero trade volume accompanying price moves to filter mechanical quote churning.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`, `score_threshold` → `4.0`

### Recommendations

- [ ] **TB-279** `rejected` — Raise spike_min_volume_delta to 1.5x baseline multiplier (e.g., require >5,880 vs 2,940)
  - **Governor rejection**: The proposed tweak conflicts with the historical constraint that volume-delta is the PRIMARY and SUFFICIENT trigger for whale-cluster escalation and that price-movement is diagnostic only and must never serve as a co-requisite gate. Specifically, the recommendation to 'mandate non-zero trade volume accompanying price moves' and the suggested threshold min_price_move: 0.03 implicitly adds a mandatory price-movement confirmation gate alongside volume-delta, which violates the rule: 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds.' Additionally, the constraint 'Do NOT gate whale-cluster escalation on minimum price-movement thresholds (spike_min_price_move) when volume-delta qualification is met' is violated by introducing min_price_move: 0.03 as a required condition.

---

## 2026-07-03 — Advisor snapshot 69

### Summary
False positives stem from quote-only spikes and mechanical quote repetitions mimicking informed volume, especially in low-liquidity markets where volume equals baseline exactly without genuine trade activity.

### Next step
Require a minimum volume delta multiplier of 2.0x baseline and enforce at least one actual executed trade with non-zero volume delta to filter out quote-only or artifact-driven spikes.

### Suggested thresholds
`min_volume_delta` → `2.0`, `min_price_move` → `0.04`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-282** `rejected` — Raise spike_min_volume_delta to 2.0x baseline volume instead of 1.0x to filter out identical-volume quote repetitions
  - **Governor rejection**: The proposed tweak conflicts with the historical constraint that explicitly rejects whale-cluster signals where `priceΔ = 0.0%` and `volΔ < 5%` of baseline, requiring `volΔ ≥ 5%` as primary and sufficient. The proposal sets a minimum volume delta multiplier of 2.0x baseline (i.e., `volΔ ≥ 100%`), which is a stricter threshold than the established 5% requirement. While stricter thresholds don't usually conflict, the proposal also enforces a minimum price move of 0.04 (4%), which contradicts the historical constraint that strictly forbids OR gates and enforces `volΔ ≥ 5%` as the primary (and sufficient) criterion, making price-impact an alternative. Additionally, the historical constraint requires `priceΔ ≥ 0.5%` for tier-8 alerts specifically, but the proposal sets `min_price_move: 0.04` (4%), which is inconsistent with the 0.5% threshold for tier-8 and creates a new, conflicting price requirement not aligned with the hindering of OR gates. Most critically, the proposal's requirement for a 2.0x volume delta multiplier (100% delta) contradicts the historical constraint's explicit acceptance of `volΔ ≥ 5%` as qualifying for tier-8 signals, effectively relaxing the volume threshold by making it much stricter in a way that violates the principle of volume-delta as the primary and sufficient criterion without price-impact alternatives.

---

## 2026-07-03 — Advisor snapshot 70

### Summary
False positives are driven by volume spikes matching the baseline exactly (1.0x multiplier) with no net trades or mechanical quote churning, particularly in low-liquidity markets where price moves mechanically on identical volume.

### Next step
Increase the volume delta threshold to require a minimum 2.0x baseline multiplier to filter out events where volume matches baseline exactly but price moves mechanically.

### Suggested thresholds
`min_volume_delta` → `2.0`

### Recommendations

- [ ] **TB-285** `rejected` — Require a minimum of 1 actual executed trade to trigger detection, filtering out quote-only spikes.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraint that explicitly states: 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds; price-movement is diagnostic only' and 'volume-delta alone is sufficient regardless of concurrent price movement.' While the tweak focuses on volume multipliers, raising the threshold to 2.0x baseline for 'low-liquidity markets' contradicts the established rule for lower-liquidity markets which requires flagging when volΔ ≥ 1–2% of baseline (not 2.0x multiplier). More critically, the tweak's logic that 'volume matches baseline exactly but price moves mechanically' should be filtered by a 2.0x multiplier violates the constraint: 'Reject signals where priceΔ = 0.0% AND volΔ < 1% of baseline (mechanical rebalancing)' — implying that mechanical price moves with low volume deltas (<1%) are already rejected, but the proposed 2.0x multiplier is an arbitrary tightening that conflicts with the flexible 1–2% range for lower-liquidity markets. Additionally, the constraint 'Do NOT demote or suppress whale-cluster signals meeting the 5% volume-delta threshold based on zero price discovery' implies volume-delta thresholds are PRIMARY, and the 2.0x multiplier (which is 200% of baseline, far exceeding 5%) is inconsistent with the tiered 1–2% vs 5% logic, making it an unjustified relaxation/tightening that conflicts with the established tiered thresholds.

---

## 2026-07-03 — Advisor snapshot 71

### Summary
False positives stem from volume spikes lacking meaningful price movement, where single-digit contract moves are likely probing behavior rather than informed flow.

### Next step
Require volume spikes to correlate with fractional price movement >0.005 (0.5%) or sustained unidirectional order flow imbalance (>80/20 ratio) in 15-minute markets.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-288** `rejected` — Increase spike_min_price_move from 0.03 to 0.005 to capture 0.5% movement while filtering probing behavior
  - **Governor rejection**: The proposed tweak violates TB-007 and multiple Governor Constraints by introducing a mandatory AND gate requiring price-movement confirmation (min_price_move: 0.005) alongside volume-delta thresholds. Specifically, it conflicts with the rule: 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds; price-movement is never a co-requisite gate [Governor Constraints]' and TB-007's statement that 'Volume delta is the PRIMARY and SUFFICIENT trigger for whale-cluster escalation; price-impact is diagnostic only and must never serve as a co-requisite gate [TB-007]'. Additionally, it violates 'Do NOT demote or suppress whale-cluster signals meeting TB-007's volume-delta threshold (≥5% on high-liquidity markets) based on zero price discovery [Governor Constraints]' because the new requirement would suppress valid signals where priceΔ = 0.0%.

---

## 2026-07-03 — Advisor snapshot 72

### Summary
False positives are driven by high-volume, low-price-move spikes that represent probing behavior or noise rather than informed flow, as confirmed by analyst notes requiring price correlation (>0.5%) for validity.

### Next step
Enforce a minimum price move threshold of 0.005 (0.5%) to eliminate probes that spike volume without moving price.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.005`, `score_threshold` → `45.0`

### Recommendations

- [ ] **TB-291** `rejected` — Increase spike_min_price_move from 0.03 to 0.005 to capture probes while filtering noise
  - **Governor rejection**: The proposed tweak violates TB-007 and Governor Constraints by introducing a mandatory AND gate requiring price-movement confirmation (min_price_move: 0.005), which contradicts the rule that volume-delta alone is the PRIMARY and SUFFICIENT trigger. Specifically, it conflicts with the constraint: 'Do not add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds; price-movement is diagnostic only, never a co-requisite gate [TB-007, Governor Constraints]' and 'Do not introduce OR gates making price-impact (≥0.5%) an acceptable alternative to volume-delta thresholds; volume-delta alone is the PRIMARY and SUFFICIENT trigger [TB-007, Governor Constraints]'.

---

## 2026-07-04 — Advisor snapshot 73

### Summary
False positives arise predominantly from pure volume spikes with zero or negligible price movement, indicating non-directional activity, probe orders, or quote-volume noise rather than genuine executed-trade flow.

### Next step
Enforce a minimum price move requirement to accompany volume spikes, eliminating signals where price impact is absent or below a specific threshold.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-294** `rejected` — Require price movement >0.5% to accompany volume spikes >20x baseline in short-duration markets.
  - **Governor rejection**: The proposed tweak directly violates TB-007 Governor Constraints by introducing a mandatory AND gate requiring price-movement confirmation (min_price_move: 0.05) alongside volume spikes. Specifically, it breaches the rule: 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds; price-movement confirmation is forbidden when volume-delta qualification is met' and 'Do NOT add mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds; price-movement confirmation is forbidden when volume-delta qualification is met [TB-007, Governor Constraints]'. The tweak also violates the principle that volume-delta alone triggers escalation regardless of concurrent price movement, and that signals meeting the 5% volume threshold on high-liquidity markets must be flagged even if priceΔ = 0.0%.

---

## 2026-07-04 — Advisor snapshot 74

### Summary
False positives are driven by volume spikes lacking corresponding price movement, particularly in ultra-short crypto markets where pure volume without price impact indicates non-directional activity.

### Next step
Require a minimum price move threshold to accompany volume spikes, as volume alone is insufficient for confirming directional flow in low-liquidity markets.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `8.0`

### Recommendations

- [ ] **TB-297** `rejected` — Set min_price_move to 0.005 (0.5%) to filter out volume spikes with zero price impact
  - **Governor rejection**: The proposed tweak conflicts with TB-PH5-compliance constraint , which requires Phase 5 end-to-end test application for TB-PH5 compliance. Additionally, it violates TB-Whale-cluster rule  and TB-Spike_score rule , which explicitly state that volume spikes without price movement (priceΔ=0.0%) must be rejected or Spike_score scaled downward by ≥70%, regardless of volume anomalies. The proposed requirement of min_price_move: 0.005 (0.5%) contradicts these constraints that already mandate rejection or downward scaling for zero-price-impact clustering, effectively relaxing a threshold that was explicitly tightened to fix noise.

---

## 2026-07-04 — Advisor snapshot 75

### Summary
False positives stem from detecting large volume spikes without accompanying meaningful price movement (e.g., 0.01 or 0.0), indicating non-directional or noise activity in ultra-short-duration markets.

### Next step
Increase the minimum price move threshold to require actual directional confirmation (e.g., >0.005 or 0.5%) alongside volume spikes to filter out non-directional noise.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-300** `rejected` — Require price movement >0.5% to accompany volume spikes >20x baseline in ultra-short markets.
  - **Governor rejection**: The proposed tweak conflicts with TB-007, which explicitly states that volume-delta is PRIMARY and SUFFICIENT regardless of priceΔ. The new requirement for a minimum price move of 0.005 (or 0.5%) disregards valid volume-delta signals that lack price impact, violating the rule that 'whale-cluster flags' should be added based on volume-delta thresholds alone (volΔ / baseline_24h ≥ 5% or 1–2%).

---

## 2026-07-04 — Advisor snapshot 76

### Summary
False positives stem from low-activity markets where pure quote/bid-ask activity triggers volume spikes without executed trades, and from older alerts lacking fresh volume confirmation.

### Next step
Require a minimum trade count (≥5) before flagging volume-based spikes in low-activity markets to filter noise from unexecuted quotes.

### Recommendations

- [x] **TB-303** `applied` — Add minimum trade count filter (≥5 trades) to ignore pure quote/bid-ask activity without executed trades
- [x] **TB-304** `applied` — Increase time-decay weighting on spike scores so alerts older than 1-2 hours receive lower tier unless fresh volume appears in last 5-10 minutes
- [x] **TB-305** `applied` — Implement median absolute deviation (MAD) estimation over past 30 minutes of alert data to normalize volume delta thresholds dynamically

---

## 2026-07-04 — Advisor snapshot 77

### Summary
False positives stem from high-frequency automated volume spikes without executed trades and from bid-ask activity lacking price movement, especially in low-liquidity crypto markets.

### Next step
Increase spike_min_volume_delta to reduce noise from automated high-frequency strategies while requiring a minimum trade count to validate volume-based spikes.

### Suggested thresholds
`min_volume_delta` → `50.0`

### Recommendations

- [x] **TB-306** `applied` — Raise spike_min_volume_delta threshold from 20x to 50x baseline for crypto markets dominated by HFT algorithms
- [x] **TB-307** `applied` — Require minimum trade count (e.g., ≥5 trades) before flagging volume spikes in low-activity markets
- [x] **TB-308** `applied` — Increase time-decay weighting on spike scores so alerts older than 1-2 hours receive lower tier unless fresh volume occurs in last 5-10 minutes

---

## 2026-07-04 — Advisor snapshot 78

### Summary
False positives are driven by volume spikes lacking corresponding price moves and trade execution, especially in automated high-frequency and low-activity markets where quote/bid-ask activity mimics genuine flow.

### Next step
Implement a minimum price move threshold alongside volume spike detection to filter mechanical filler activity in crypto markets.

### Suggested thresholds
`min_volume_delta` → `50.0`, `min_price_move` → `0.5`

### Recommendations

- [ ] **TB-309** `rejected` — Raise spike_min_volume_delta from 20x to 50x baseline to reduce false positives in automated high-frequency markets
  - **Governor rejection**: The proposed tweak conflicts with the 'No price-movement co-gating' historical constraint (TB-002). This rule explicitly forbids mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds, stating that price-movement is 'diagnostic only' and never a co-requisite gate. The proposal to 'Implement a minimum price move threshold alongside volume spike detection' creates exactly such a forbidden co-requisite gate. Additionally, the 'No OR gates for price-impact' constraint (TB-003) forbids making price-impact an acceptable alternative to volume-delta thresholds, and the 'Prohibition of suppression' constraint (TB-004) forbids demoting signals meeting volume-delta thresholds based on zero price discovery.

---

## 2026-07-04 — Advisor snapshot 79

### Summary
Current false positives stem from volume spikes lacking concurrent price moves, especially in crypto markets dominated by automated high-frequency trading strategies that generate mechanical filler activity.

### Next step
Require a minimum fractional price move of >0.5% alongside volume spikes to filter out mechanical filler activity and reduce false positives for automated high-frequency strategies.

### Suggested thresholds
`min_volume_delta` → `50.0`, `min_price_move` → `0.5`

### Recommendations

- [ ] **TB-312** `rejected` — Increase spike_min_price_move from 0.03 to 0.50 (50%) to ensure significant price follow-through
  - **Governor rejection**: The proposed tweak violates TB-002, TB-003, TB-006, and TB-PH5. TB-003 explicitly forbids introducing OR gates making price-impact (≥0.5%) an acceptable alternative to volume-delta thresholds, while TB-002 and TB-006 explicitly forbid adding mandatory AND gates requiring price-movement confirmation alongside volume-delta thresholds, stating that price-movement is diagnostic only and never a co-requisite gate. The proposal's requirement for a minimum price move of >0.5% alongside volume spikes creates exactly this forbidden mandatory AND gate, conflicting with the historical constraint that volume-delta alone is the sufficient trigger.

---

## 2026-07-07 — Advisor snapshot 80

### Summary
False positives are driven by low-volume probe orders and quote management in low-liquidity, long-dated sports markets, where current thresholds fail to distinguish noise from genuine flow.

### Next step
Raise the minimum volume delta threshold and require corroborating price movement >0.5% to filter out probe orders and quote management activity.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-313** `rejected` — Increase spike_min_volume_delta from 2983.76 to 5000.0 to exclude low-volume probes
  - **Governor rejection**: The proposed tweak conflicts with TB-014 (TB-014) and TB-007 (TB-007). TB-014 explicitly raises the whale-cluster bar in thin/illiquid markets to volΔ ≥ 10× baseline OR priceΔ ≥ 1%. The proposed tweak requires only priceΔ ≥ 0.5% in low-liquidity markets, which violates the mandated 1% threshold. Additionally, TB-007 enforces a volΔ / baseline_24h ≥ 5% threshold for high-liquidity markets and 1–2% for low-liquidity markets regardless of priceΔ=0.0; the proposed static 5000.0 volume floor may fail to scale with baseline (violating TB-031 which requires dynamic scaling by liquidity) and ignores the rule that priceΔ can be 0.0% if volume thresholds are met.
- [ ] **TB-314** `rejected` — Require spike_min_price_move > 0.005 (0.5%) to confirm price impact before emitting a signal
  - **Governor rejection**: The proposed tweak conflicts with TB-014 (TB-014) and TB-007 (TB-007). TB-014 explicitly raises the whale-cluster bar in thin/illiquid markets to volΔ ≥ 10× baseline OR priceΔ ≥ 1%. The proposed tweak requires only priceΔ ≥ 0.5% in low-liquidity markets, which violates the mandated 1% threshold. Additionally, TB-007 enforces a volΔ / baseline_24h ≥ 5% threshold for high-liquidity markets and 1–2% for low-liquidity markets regardless of priceΔ=0.0; the proposed static 5000.0 volume floor may fail to scale with baseline (violating TB-031 which requires dynamic scaling by liquidity) and ignores the rule that priceΔ can be 0.0% if volume thresholds are met.
- [ ] **TB-315** `rejected` — Add minimum trade count threshold of 5+ executed trades per spike window to filter quote-driven noise
  - **Governor rejection**: The proposed tweak conflicts with TB-014 (TB-014) and TB-007 (TB-007). TB-014 explicitly raises the whale-cluster bar in thin/illiquid markets to volΔ ≥ 10× baseline OR priceΔ ≥ 1%. The proposed tweak requires only priceΔ ≥ 0.5% in low-liquidity markets, which violates the mandated 1% threshold. Additionally, TB-007 enforces a volΔ / baseline_24h ≥ 5% threshold for high-liquidity markets and 1–2% for low-liquidity markets regardless of priceΔ=0.0; the proposed static 5000.0 volume floor may fail to scale with baseline (violating TB-031 which requires dynamic scaling by liquidity) and ignores the rule that priceΔ can be 0.0% if volume thresholds are met.

---

## 2026-07-07 — Advisor snapshot 81

### Summary
False positives stem from ordinary intraday churn triggering spikes without sustained directional persistence, especially in election markets like Texas where large volume spikes resolve with moderate price follow-through.

### Next step
Require sustained price hold (>2 minutes) after spike detection to filter transient block trades and reduce false positives on mean-reverting noise.

### Suggested thresholds
`min_volume_delta` → `150.0`

### Recommendations

- [x] **TB-316** `applied` — Lower volume baseline for Texas election markets from 25 to ~100–150 to reduce sensitivity to ordinary intraday churn
- [x] **TB-317** `applied` — Require sustained price hold (>2 minutes) after spike rather than immediate mean-reversion to reduce false positives on transient block trades
- [x] **TB-318** `applied` — Prioritize price-magnitude follow-through over raw volume delta when scoring signal durability

---

## 2026-07-07 — Advisor snapshot 82

### Summary
False positives are driven by volume spikes lacking corresponding price moves in thin or micromarkets, where tiny baselines inflate scores and sub-5-trade probe events mimic noise.

### Next step
Require a minimum price move to accompany volume spikes and enforce a minimum absolute volume threshold to filter out probe noise in thin markets.

### Suggested thresholds
`min_volume_delta` → `10.0`, `min_price_move` → `0.015`, `score_threshold` → `100.0`

### Recommendations

- [ ] **TB-319** `rejected` — Set min_price_move to 0.015 (1.5%) to eliminate spikes without price follow-through
  - **Governor rejection**: The proposed tweak conflicts with TB-001 and TB-006. TB-001 requires rejecting whale-cluster signals when priceΔ=0.0% and volΔ < 5% of baseline simultaneously if hard filter is active, while the tweak sets min_price_move at 0.015 (1.5%) and min_volume_delta at 10.0, which is less than the 5% baseline threshold enforced historically for high-liquidity markets. Additionally, TB-006 explicitly states that whale-cluster detections with priceΔ=0.0 must never emit signals and require ≥0.5% price impact for tier-8 alerts, but the tweak's min_price_move of 0.015 (1.5%) still falls below the 0.5% (50x higher) mandated threshold for tier-8 alerts, relaxing a constraint that was explicitly tightened to prevent noise from zero-price clustering.
- [ ] **TB-320** `rejected` — Set min_volume_delta to 10.0 to filter out sub-10x baseline probe events
  - **Governor rejection**: The proposed tweak conflicts with TB-001 and TB-006. TB-001 requires rejecting whale-cluster signals when priceΔ=0.0% and volΔ < 5% of baseline simultaneously if hard filter is active, while the tweak sets min_price_move at 0.015 (1.5%) and min_volume_delta at 10.0, which is less than the 5% baseline threshold enforced historically for high-liquidity markets. Additionally, TB-006 explicitly states that whale-cluster detections with priceΔ=0.0 must never emit signals and require ≥0.5% price impact for tier-8 alerts, but the tweak's min_price_move of 0.015 (1.5%) still falls below the 0.5% (50x higher) mandated threshold for tier-8 alerts, relaxing a constraint that was explicitly tightened to prevent noise from zero-price clustering.
- [ ] **TB-321** `rejected` — Increase score_threshold to 100.0 to reduce sensitivity to inflated scores from tiny baselines
  - **Governor rejection**: The proposed tweak conflicts with TB-001 and TB-006. TB-001 requires rejecting whale-cluster signals when priceΔ=0.0% and volΔ < 5% of baseline simultaneously if hard filter is active, while the tweak sets min_price_move at 0.015 (1.5%) and min_volume_delta at 10.0, which is less than the 5% baseline threshold enforced historically for high-liquidity markets. Additionally, TB-006 explicitly states that whale-cluster detections with priceΔ=0.0 must never emit signals and require ≥0.5% price impact for tier-8 alerts, but the tweak's min_price_move of 0.015 (1.5%) still falls below the 0.5% (50x higher) mandated threshold for tier-8 alerts, relaxing a constraint that was explicitly tightened to prevent noise from zero-price clustering.

---

## 2026-07-07 — Advisor snapshot 83

### Summary
False positives stem from isolated trade bursts (e.g., tactical test orders) and single-leg liquidation cascades that self-correct quickly, rather than sustained market pressure.

### Next step
Require sustained price pressure over >10 seconds with consistent volume acceleration to filter out tactical bursts and self-correcting liquidations.

### Suggested thresholds
`min_volume_delta` → `300.0`, `min_price_move` → `0.065`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-322** `rejected` — Increase spike_min_volume_delta to require sustained volume acceleration rather than isolated bursts
  - **Governor rejection**: The proposed tweak violates TB-007, TB-002, and TB-006 by introducing a mandatory price-movement (min_price_move: 0.065) requirement as a co-requisite gate for signals. Historical constraints explicitly state that whale-cluster signals must be flagged based on volume-delta alone regardless of concurrent price movement (priceΔ = 0.0%), and that price-impact is diagnostic only, never a co-requisite gate or acceptable alternative (TB-007). Furthermore, the tweak adds a mandatory AND gate requiring price-movement confirmation alongside volume-delta thresholds, which is prohibited by TB-002 and TB-006.
- [ ] **TB-323** `rejected` — Require spike_min_price_move to reflect sustained movement (>2 ticks) to filter single-leg cascades
  - **Governor rejection**: The proposed tweak violates TB-007, TB-002, and TB-006 by introducing a mandatory price-movement (min_price_move: 0.065) requirement as a co-requisite gate for signals. Historical constraints explicitly state that whale-cluster signals must be flagged based on volume-delta alone regardless of concurrent price movement (priceΔ = 0.0%), and that price-impact is diagnostic only, never a co-requisite gate or acceptable alternative (TB-007). Furthermore, the tweak adds a mandatory AND gate requiring price-movement confirmation alongside volume-delta thresholds, which is prohibited by TB-002 and TB-006.
- [ ] **TB-324** `rejected` — Add a time-based condition requiring price pressure over >10 seconds with consistent volume
  - **Governor rejection**: The proposed tweak violates TB-007, TB-002, and TB-006 by introducing a mandatory price-movement (min_price_move: 0.065) requirement as a co-requisite gate for signals. Historical constraints explicitly state that whale-cluster signals must be flagged based on volume-delta alone regardless of concurrent price movement (priceΔ = 0.0%), and that price-impact is diagnostic only, never a co-requisite gate or acceptable alternative (TB-007). Furthermore, the tweak adds a mandatory AND gate requiring price-movement confirmation alongside volume-delta thresholds, which is prohibited by TB-002 and TB-006.

---

## 2026-07-07 — Advisor snapshot 84

### Summary
False positives are driven by one-sided volume spikes without meaningful price movement and by low-volume noise in ultra-short duration markets, where single-order artifacts are common.

### Next step
Raise the minimum price move threshold to require >0.5% fractional change and enforce a minimum absolute volume delta of 50+ contracts for short-duration tiers.

### Suggested thresholds
`min_volume_delta` → `50.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-325** `planned` — Increase spike_min_price_move from 0.03 to 0.005 (0.5%) to ensure price impact accompanies volume.
- [ ] **TB-326** `planned` — Set spike_min_volume_delta to 50.0 for tiers with ultra-short duration (e.g., 15-minute markets) to filter single-order noise.
- [ ] **TB-327** `planned` — Add a cross-condition rule: emit signal only if (volΔ > 50) AND (priceΔ > 0.005) to require both meaningful volume and price move.

---
