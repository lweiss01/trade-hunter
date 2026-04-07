# Tuning Backlog

Last updated: 2026-04-07

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

- [x] **TB-006** `applied` — Add higher watch-tier minimum move when volume is weak relative to baseline.
  - Rule: for `watch`, require `1–2%` price move when `volΔ < 2x baseline`; require `5–6%` if `volΔ` is only `1.2x baseline`.
  - Notes: overlaps with TB-002 and may supersede it once implemented.

- [x] **TB-007** `applied` — Add directional trade-flow confirmation.
  - Rule: require `>60%` of recent trades to lean one side before escalating balanced volume spikes.
  - Notes: implemented in `app/detector.py`. Weak-price outlier alerts (`price_move < 1%`) now require either meaningful repricing (`>= 1%`) or directional trade confirmation (`> 60%` dominant recent trade-side share`) to emit. Balanced directional flow and quote-only weak outliers no longer alert on volume alone. Covered in `tests/test_detector_migration.py`.

- [x] **TB-008** `applied` — Increase watch-tier volume multiple requirement.
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

- [x] **TB-009** `applied` — Add rule: exclude trades smaller than 5% of best-bid/ask quote volume from spike score contribution
- [x] **TB-010** `applied` — Add rule: require 2+ consecutive trades in same direction within 2-3 seconds to qualify for spike scoring
- [x] **TB-011** `applied` — Raise spike_min_price_move from 0.03 to 0.04 (4%) to filter marginal moves in low-liquidity pairs

---

## 2026-04-05 — Advisor snapshot D

### Summary
Low-liquidity niche markets are generating false positives from small absolute volume swings and modest price moves that lack genuine directional conviction. Both recent signals show thin baseline volumes with marginal price deltas that don't reflect market-moving information.

### Next step
Introduce a liquidity-gated threshold system: require minimum absolute volume baseline (e.g., 1000+ contracts) before applying relative delta rules, and scale price-move thresholds inversely with baseline liquidity (thin markets need >5% moves, deep markets can trigger at 2-3%).

### Suggested thresholds
`min_volume_delta` → `1000.0`, `score_threshold` → `2.5`

### Recommendations

- [x] **TB-012** `applied` — Add absolute volume floor: skip detection entirely if baseline_volume < 1000 contracts, regardless of relative delta
- [x] **TB-013** `applied` — Implement liquidity-aware price thresholds: require priceΔ > 5% for markets with <20k baseline volume, priceΔ > 3% for 20k-100k, priceΔ > 2% for >100k
- [x] **TB-014** `applied` — Raise spike_min_volume_delta to 800-1000 for all markets as floor, then apply percentage-of-baseline multipliers (e.g., 15-20% delta on thin markets vs. 10% on deep markets)

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

## 2026-04-05 — Advisor snapshot P

### Summary
False positives stem from quote-only volume spikes without sustained trade follow-through, and high scores driven by volume deltas that don't correlate with genuine price conviction or informed positioning.

### Next step
Introduce a trade-volume confirmation gate: require a minimum percentage of the volume delta to be represented by actual executed trades (not just quote/bid-ask activity) before emitting a signal.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-048** `planned` — Add minimum executed trade count requirement (e.g., 10+ contracts traded) relative to total volume delta to filter market-making noise
- [ ] **TB-049** `planned` — Require price move persistence: price must hold or improve for at least N subsequent trades after the spike event, not just static snapshot
- [ ] **TB-050** `planned` — Reduce reliance on raw volume_delta in score calculation; weight it lower relative to trade-count and price-move conviction metrics

---

## 2026-04-05 — Advisor snapshot Q

### Summary
False positives are driven by thin-market noise: high relative volume deltas on low absolute baselines (SDUF) and high conviction scores disconnected from actual price impact (KXCABOUT-26APR-TGAB with 9% move but only 3% underlying probability).

### Next step
Introduce liquidity-aware thresholds that scale requirements based on baseline volume and market depth. For markets with baseline volume <20, enforce stricter absolute volume deltas and require price-volume correlation.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-051** `planned` — Require sustained volume >5x baseline (not 3.3x) for 'high conviction flow' classification on tail outcomes (yes probability <10%)
- [ ] **TB-052** `planned` — For ultra-low-liquidity markets (baseline volume <20), enforce minimum absolute volume delta of 50+ units AND price move >0.5%, or volume >20x baseline only if accompanied by directional price move
- [ ] **TB-053** `planned` — Reduce reliance on score alone for emission—add veto rule: suppress signals where price delta is <1% AND baseline volume <50, regardless of score, unless volume delta >10x baseline with coherent directionality

---

## 2026-04-05 — Advisor snapshot R

### Summary
Thin markets and low-liquidity contracts are generating false positives through amplified price moves and inflated scores on minimal volume. The spike detector lacks safeguards for markets with low absolute liquidity or microprice conditions.

### Next step
Introduce a minimum absolute volume threshold (e.g., 10,000+ contracts in market) and exclude or dampen signals from contracts priced below 0.05 before applying spike detection logic.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.05`, `score_threshold` → `100.0`

### Recommendations

- [ ] **TB-054** `planned` — Add market liquidity floor: skip spike detection for markets with total outstanding contracts < 10,000 or current price < 0.05
- [ ] **TB-055** `planned` — Require minimum confirmed trade volume within a time window (5 min): demand 10+ contracts in recent trades, not just quoted volume delta, to validate a spike
- [ ] **TB-056** `planned` — Reduce score_threshold for low-liquidity markets or apply a liquidity-adjusted score multiplier (e.g., divide score by sqrt(market_volume)) to penalize thin-market signals

---

## 2026-04-05 — Advisor snapshot S

### Summary
Low-liquidity nickname markets are generating false positives from single-trade outliers and mechanical quote-flush events that lack sustained flow conviction.

### Next step
Implement a liquidity-tier-based minimum trade size requirement: require multi-contract spikes or sustained order flow on markets with typical trade sizes below 20 contracts, rather than relying on single outlier trades.

### Suggested thresholds
`min_volume_delta` → `1500.0`, `min_price_move` → `0.05`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-057** `planned` — For markets with typical trade size < 20 contracts, require spike_min_contracts ≥ 3 (or equivalent notional minimum) instead of accepting single-trade volume deltas
- [ ] **TB-058** `planned` — Add a sustained_flow check: spike signals on low-liquidity venues should require either multiple fills in same direction within short window, or price persistence, not just instantaneous price move
- [ ] **TB-059** `planned` — Raise spike_min_volume_delta for tier=notable contracts with yes/no confidence near 0.50 (indicating genuine uncertainty rather than directional conviction)

---

## 2026-04-05 — Advisor snapshot T

### Summary
Low-liquidity niche markets (TRUMP nickname contracts) are generating false positives from thin order books where small single trades cause outsized price moves without reflecting genuine market consensus.

### Next step
Implement liquidity-tier-aware thresholds that require higher volume deltas and minimum trade sizes for low-liquidity markets, rather than applying uniform global thresholds.

### Suggested thresholds
`min_volume_delta` → `1.3`, `min_price_move` → `0.08`

### Recommendations

- [ ] **TB-060** `planned` — For markets with typical trade size <20 contracts, raise minimum trade size threshold from 1 contract to 3+ contracts or require sustained multi-trade order flow within a window
- [ ] **TB-061** `planned` — For low-liquidity markets, increase volume delta multiplier requirement from 1.1x to 1.3x+ to filter mechanical quote-flush and single-outlier events
- [ ] **TB-062** `planned` — Implement a liquidity-adjusted score penalty that reduces spike_score for thin markets (e.g., typical trade size <20 or open interest <1000) unless price move exceeds 8%+ and volume delta exceeds 1.5x

---

## 2026-04-05 — Advisor snapshot U

### Summary
Low-liquidity niche markets (like nickname contracts) are generating false positives from small absolute volumes and single large trades that create outsized price moves without reflecting genuine market consensus.

### Next step
Implement market-liquidity-aware thresholds: apply stricter volume delta multipliers (1.3x+) and minimum contract size filters for low-liquidity tiers, rather than using uniform global thresholds.

### Suggested thresholds
`min_volume_delta` → `1.3`

### Recommendations

- [ ] **TB-063** `planned` — Raise minimum contract size threshold for single-trade spikes on low-liquidity markets from current baseline to ≥15–20 contracts to filter fat-finger/execution noise on nickname markets
- [ ] **TB-064** `planned` — Increase volume delta multiplier floor for low-liquidity contracts from 1.1x to 1.3x to require more sustained volume flow, not just absolute deltas
- [ ] **TB-065** `planned` — Add liquidity-tier routing: detect base liquidity (e.g., total open interest or avg daily volume) and apply stricter price_move thresholds (e.g. 0.05+ for low-liquidity vs 0.03+ for standard) to reduce noise sensitivity

---

## 2026-04-05 — Advisor snapshot V

### Summary
Micro-probability markets with large volume deltas but minimal price moves are generating false positives; the detector is triggering on mechanical quote clustering and passive liquidity provision rather than directional conviction.

### Next step
Implement a composite gating rule: require either (a) price move ≥2% OR (b) directional flow consensus ≥70% for at least 2 consecutive seconds, before emitting a signal in markets with yes-probability <0.10.

### Suggested thresholds
`min_price_move` → `0.02`, `score_threshold` → `7.5`

### Recommendations

- [ ] **TB-066** `planned` — For ultra-low-probability markets (yes < 0.10), enforce minimum price_move of 0.02 (2%) OR directional consensus >70% over 2s window, to filter mechanical order clustering.
- [ ] **TB-067** `planned` — Decouple volume_delta from score weighting when price_move is near-zero; volume alone should not drive high scores in micro-probability regimes.
- [ ] **TB-068** `planned` — Add a market-context filter: if market is within 7 days of expiration AND yes-probability <0.05, increase spike_score_threshold by 1.5x or require 3% price move instead of volume spike alone.

---

## 2026-04-05 — Advisor snapshot W

### Summary
Detector is triggering on volume spikes without sustained price conviction, particularly in micro-probability and near-expiry markets where mechanical order clustering creates false positives.

### Next step
Implement a multi-factor gate: require either (1) price move >0.5% sustained over 5min, OR (2) directional order-flow imbalance >70% over >15sec, OR (3) price move >2% for ultra-low probability markets (<5% implied prob) within 24h of expiry. This separates passive quote updates from genuine informed flow.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `12.0`

### Recommendations

- [ ] **TB-069** `planned` — For markets within 24h of expiry with yes-price <0.05: raise effective spike_score_threshold to 12+ OR require price move >2% OR require >70% directional flow consensus over ≥15sec window
- [ ] **TB-070** `planned` — For all markets with priceΔ <0.005 and volΔ >75k: require sustained directional imbalance (>15sec at >70% one-side) before emitting signal, not instantaneous volume spikes
- [ ] **TB-071** `planned` — Add temporal duration gate: volume spikes with zero meaningful price move should only signal if order-side imbalance persists >15 seconds; single-second volume bursts are quote-update noise in low-liquidity markets

---

## 2026-04-05 — Advisor snapshot X

### Summary
The detector is generating false positives in ultra-low-probability micro-markets near expiration, where mechanical order clustering and quote updates trigger volume spikes without genuine directional conviction or meaningful price movement.

### Next step
Implement a composite filter requiring either (a) price movement >2% OR (b) sustained directional order-side imbalance (>70% one-side over >5 seconds) for markets with base probability <0.10 within 24h of expiry, rather than relying on volume delta alone.

### Suggested thresholds
`min_volume_delta` → `150000.0`, `min_price_move` → `0.02`, `score_threshold` → `12.0`

### Recommendations

- [ ] **TB-072** `planned` — Exclude or downweight markets with base probability <0.05, or require minimum trade size per fill (>100 volume) to filter passive micro-conviction noise
- [ ] **TB-073** `planned` — For short-duration markets within 24h of expiry with zero/minimal price movement (priceΔ <0.005), require either sustained directional order flow (>15min persistence or >70% one-side consensus over 5+ seconds) OR price move >2%
- [ ] **TB-074** `planned` — Require price_move >0.005 (0.5%) alongside volume spikes in low-probability markets, since genuine signal should produce measurable mid-price shifts even in thin markets

---

## 2026-04-05 — Advisor snapshot Y

### Summary
High false-positive rate in micro-probability markets (yes <0.06) with volume spikes but minimal or zero price movement. Volume delta alone is insufficient; price action and order-flow persistence are needed to distinguish signal from noise.

### Next step
Require either meaningful price movement (≥0.5%) OR sustained directional order-flow persistence (≥15 seconds) for markets within 24h of expiry with base probability <0.10, to filter passive quote updates.

### Suggested thresholds
`min_volume_delta` → `100000.0`, `min_price_move` → `0.005`, `score_threshold` → `12.0`

### Recommendations

- [ ] **TB-075** `planned` — Exclude or penalize markets with base probability (yes) <0.05 unless price move exceeds 1.0% or order imbalance persists >20 seconds
- [ ] **TB-076** `planned` — For markets with 0.0 price delta, require minimum order-side imbalance persistence of 15+ seconds or volume concentration in top 2–3 fills >40% of spike_volume_delta
- [ ] **TB-077** `planned` — Add time-to-expiry decay: within 24h of expiry, increase score_threshold by +3 points or require min_price_move ≥0.5% to account for elevated micro-market volatility

---

## 2026-04-05 — Advisor snapshot Z

### Summary
Low-conviction micro-markets near expiry are generating noise signals with weak price moves and small base probabilities. The first signal (score=5.525, priceΔ=0.04, yes=0.02) is clearly false positive; the second (score=17.831, priceΔ=0.0) suggests volume alone without sustained price action is insufficient.

### Next step
Require minimum base probability threshold (yes ≥ 0.05) AND sustained price movement or order-imbalance persistence for markets within 24h of expiry to filter micro-market noise.

### Suggested thresholds
`min_volume_delta` → `150000.0`, `min_price_move` → `0.005`, `score_threshold` → `12.0`

### Recommendations

- [ ] **TB-078** `planned` — Exclude or deprioritize signals from markets with base probability <0.05 (yes or no side), as these indicate low conviction and are noise-prone
- [ ] **TB-079** `planned` — For markets ≤24h from expiry, require either price move >0.5% sustained over 5min window OR order-side imbalance >15min duration before emitting signal
- [ ] **TB-080** `planned` — Implement minimum trade-size filter: require individual fills >100 notional volume to prevent signal inflation from fragmented micro-trades in low-liquidity markets

---

## 2026-04-05 — Advisor snapshot 27

### Summary
False positives are clustering in low-conviction micro-markets (base probability <0.05) and quote-driven volume spikes lacking executed trade confirmation, particularly in short-duration expiry windows where noise dominates signal.

### Next step
Implement a two-tier filter: (1) exclude or deprioritize markets with base probability <0.05, and (2) require minimum executed trade size (not just volume delta from quotes) to validate spike legitimacy before emitting watch/notable tier alerts.

### Suggested thresholds
`min_volume_delta` → `150000.0`, `min_price_move` → `0.035`, `score_threshold` → `12.0`

### Recommendations

- [ ] **TB-081** `planned` — Filter out markets with yes/no probability <0.05; these are noise-prone micro-markets where small quote activity creates outsized volume deltas relative to conviction
- [ ] **TB-082** `planned` — Require minimum trade size per fill (e.g., >100 volume per executed trade) to distinguish real order flow from quote stuffing; volume delta alone is insufficient in thin markets
- [ ] **TB-083** `planned` — For markets within 24h of expiry, enforce either sustained price movement (>0.5% over 5min window) OR order-side imbalance persistence (>15min) before triggering watch tier; single-spike events are noise

---

## 2026-04-05 — Advisor snapshot 28

### Summary
False positives are concentrated in low-conviction micro-markets with quote-driven volume spikes that lack substantive executed trades, particularly when base probability is very low (<5%).

### Next step
Require minimum executed trade size (not just volume delta from quotes) and enforce base probability floor to filter noise in low-liquidity prediction markets.

### Suggested thresholds
`min_volume_delta` → `150000.0`, `min_price_move` → `0.04`, `score_threshold` → `5.5`

### Recommendations

- [ ] **TB-084** `planned` — Add minimum_executed_trade_size threshold (e.g., ≥100 volume per fill) to distinguish real trades from quote-only activity
- [ ] **TB-085** `planned` — Exclude or downweight signals in markets with base_probability < 0.05 to avoid noise in extremely low-conviction contracts
- [ ] **TB-086** `planned` — Increase spike_min_volume_delta to 150000+ to filter marginal quote moves that don't represent material market conviction

---

## 2026-04-05 — Advisor snapshot 29

### Summary
Both signals on the same market near expiration show legitimate activity (medium confidence labels) but low price moves (0.04% and 0.0%), indicating the detector is correctly identifying flow but baseline thresholds are too rigid for end-of-life market dynamics.

### Next step
Implement time-to-expiration (TTX) bucketing: apply relaxed volume_delta thresholds for markets within 48h of resolution, since mechanical rebalancing and informed positioning naturally produce elevated volume on lower price impact.

### Recommendations

- [ ] **TB-087** `planned` — Create TTX-aware volume threshold: use 50% of standard spike_min_volume_delta for markets <48h to expiration, 75% for <24h
- [ ] **TB-088** `planned` — Add trade-sequencing filter to detect coordinated multi-leg orders: flag when multiple small volume chunks execute within <5min at consistent price levels as lower-confidence signal
- [ ] **TB-089** `planned` — Lower spike_score_threshold specifically for high-volume, low-price-move signals near expiration (score >15 + volΔ >100k + priceΔ <0.01 = eligible for lower threshold)

---

## 2026-04-05 — Advisor snapshot 30

### Summary
Near-expiration micro-event markets are generating medium-confidence signals with low price moves (0–4%) but moderate volume spikes, driven by mechanical rebalancing and quote-rebounding rather than informed positioning.

### Next step
Introduce time-to-expiration (TTX) and quote-to-trade ratio buckets to dynamically adjust volume-delta thresholds and filter mechanical noise in final 48 hours.

### Suggested thresholds
`min_price_move` → `0.02`, `score_threshold` → `8.0`

### Recommendations

- [ ] **TB-090** `planned` — For TTX < 48h: lower spike_min_volume_delta by 30–40% (e.g., 80k–100k instead of 130k+) to catch genuine late-stage informed flow, but require quote_to_trade_ratio < 100:1 to reject pure post-quote mechanical rebounds.
- [ ] **TB-091** `planned` — For TTX < 24h: add trade sequencing filter—flag coordinated multi-leg orders (same counterparty, <500ms apart) as low-confidence and suppress tier=watch elevation.
- [ ] **TB-092** `planned` — Raise spike_score_threshold from current ~3.5–17.8 range to 5.0+ for TTX > 48h, and to 8.0+ for TTX < 48h (to force price_move or trade-quality confirmation in compressed-liquidity regimes).

---

## 2026-04-05 — Advisor snapshot 31

### Summary
Near-expiration micro-event markets are generating medium-confidence signals with modest price moves (1-4%) on moderate volume deltas, suggesting the detector is catching genuine flow but needs context-aware tuning to separate informed trading from mechanical rebalancing.

### Next step
Implement time-to-expiration and market-liquidity bucketing: lower volume_delta thresholds for sub-24h markets while adding quote-to-trade ratio and baseline volatility filters to distinguish informed flow from post-quote mechanical moves.

### Suggested thresholds
`min_volume_delta` → `105000.0`, `min_price_move` → `0.02`, `score_threshold` → `3.8`

### Recommendations

- [ ] **TB-093** `planned` — For markets within 24h of resolution, reduce spike_min_volume_delta by 30-40% (e.g., from typical ~150k to ~90-105k) to account for lower baseline activity, but require quote-to-trade ratio <100:1 to gate out quote-driven noise.
- [ ] **TB-094** `planned` — Add a micro-event submarket classifier: when TTL<24h AND market depth is thin, require price_move ≥ 0.02 (2%) as compensatory floor, even if volume_delta is low.
- [ ] **TB-095** `planned` — Introduce baseline volatility normalization: scale spike_score by (realized_vol_1h / median_vol_lookback) so that genuinely quiet markets don't auto-inflate scores from small absolute moves.

---

## 2026-04-05 — Advisor snapshot 32

### Summary
False positives are driven by quote-side volume spikes without corresponding executed trade follow-through or price impact, particularly on ultra-low-liquidity markets where large quotes fail to materialize into actual fills.

### Next step
Require post-spike trade confirmation: signal only after observing ≥3 consecutive executed trades in the same direction within a tight time window post-quote, rather than flagging on quote delta alone.

### Suggested thresholds
`min_volume_delta` → `250000.0`, `min_price_move` → `0.03`, `score_threshold` → `12.0`

### Recommendations

- [ ] **TB-096** `planned` — Filter out single-sided quote spikes (bid or ask only) on markets with <500k base liquidity unless accompanied by ≥3 consecutive same-direction executions within 30 seconds
- [ ] **TB-097** `planned` — Increase executed trade volume requirement: only flag volume delta if at least 40% of the delta is confirmed by filled trades, not just posted liquidity
- [ ] **TB-098** `planned` — Raise spike_score_threshold to 12.0 to suppress low-conviction signals; the 4.266 signal on RIGG should not reach analyst review without price move >0.03 or execution confirmation

---

## 2026-04-05 — Advisor snapshot 33

### Summary
Low-liquidity, near-expiry markets (KXTRUMPSAY-26APR06) are generating false positives from quote-driven volume spikes without real directional trade follow-through or meaningful price impact.

### Next step
Introduce liquidity-aware filtering: require minimum trade-to-quote ratio and consecutive directional trade confirmation before emitting signals in markets below a liquidity threshold.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-099** `planned` — Add trade_fill_ratio threshold: require >10% of quoted volume to be actually filled in trades before counting volume delta as valid spike signal
- [ ] **TB-100** `planned` — Add consecutive_trade_confirmation rule: require ≥3 consecutive trades in the same direction within a short time window (e.g., 30s) post-spike to validate directional intent
- [ ] **TB-101** `planned` — Demote or exclude signals from ultra-low-liquidity markets (e.g., <1000 contracts total open interest or <5 active market makers) unless they meet stricter thresholds

---

## 2026-04-05 — Advisor snapshot 34

### Summary
Large volume deltas without corresponding price movement or genuine trade execution are triggering false positives, particularly in low-liquidity near-expiry markets dominated by quote refreshes rather than filled trades.

### Next step
Introduce a trade-to-quote ratio filter requiring minimum 10-15% of quoted volume to be actually filled before flagging volume spikes, combined with a mandatory price-movement floor of 1% for volume-only signals.

### Suggested thresholds
`min_price_move` → `0.01`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-102** `planned` — Add trade_fill_ratio constraint: require ≥10% of volume delta to represent filled trades (not just quotes) before spike qualifies
- [ ] **TB-103** `planned` — Raise min_price_move floor to 0.01 (1%) when volume delta is high but isolated to single counterparty or quote refresh cycles
- [ ] **TB-104** `planned` — Implement counterparty_diversity check: require volume delta to come from ≥2 distinct counterparties OR accompany ≥1% price move to trigger signal

---

## 2026-04-05 — Advisor snapshot 35

### Summary
Detector is firing on thin markets with negligible absolute volume and quote-dominated activity lacking real price impact. Three false positives share low liquidity, near-expiry conditions, and minimal or absent price moves despite high nominal volume deltas.

### Next step
Implement a multi-factor gating rule: require both (1) volume delta as % of baseline daily volume ≥2%, AND (2) price move ≥1% OR confirmed multi-party trade volume ≥10% of quoted delta, before emitting watch-tier signals.

### Suggested thresholds
`min_price_move` → `0.01`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-105** `planned` — Gate on volume delta as percentage of baseline daily volume: reject spikes where volΔ < 0.02 × baseline_daily_volume (197/62k = 0.3% is well below threshold)
- [ ] **TB-106** `planned` — Require price move ≥1% OR validate trade-to-quote ratio: if priceΔ < 0.01, only flag if actual filled volume exceeds 10% of quoted size delta
- [ ] **TB-107** `planned` — For near-expiry/micro-cap markets, raise spike_score_threshold from current level to 5.0+ to suppress low-signal-strength detections in thin order books

---

## 2026-04-05 — Advisor snapshot 36

### Summary
Detector is triggering on noise in thin micro-cap markets: either trivial volume deltas relative to baseline daily volume, or large volume moves without accompanying price pressure indicating genuine information flow.

### Next step
Implement relative volume delta (as % of baseline daily volume) rather than absolute volume delta, and require minimum price movement (≥1%) for watch-tier signals unless volume originates from multiple counterparties.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-108** `planned` — Replace absolute spike_min_volume_delta with relative threshold: require volume delta ≥2-5% of baseline daily volume (KXTRUMPSAY has 62k baseline; 197 shares = 0.3% is negligible)
- [ ] **TB-109** `planned` — Raise spike_min_price_move to 0.01 (1%) for watch-tier signals, or relax requirement only when volume spike shows multi-counterparty distribution rather than single quote refreshes
- [ ] **TB-110** `planned` — Add conditional logic: if price_move < 0.01, require volume delta to be >10% of baseline daily volume to avoid flagging mechanical quote updates as signals

---

## 2026-04-05 — Advisor snapshot 37

### Summary
Ultra-thin markets with low baseline volume and extreme probability distributions are generating false positives: small absolute volumes create outsized percentage moves, and volume spikes without meaningful price movement are being incorrectly flagged as informative signals.

### Next step
Implement a market-liquidity-adjusted volume threshold that scales minimum volume delta by baseline daily volume and probability tier, rather than using a fixed absolute threshold across all markets.

### Suggested thresholds
`min_price_move` → `0.01`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-111** `planned` — Require volume delta to represent ≥2-5% of baseline daily volume before flagging as watch-tier (e.g., 62k daily baseline → min 1.24k-3.1k volume delta); adjust percentage based on market tier/probability
- [ ] **TB-112** `planned` — Enforce minimum price movement of ≥1% when volume spike originates from single counterparty or quote refresh, to distinguish genuine flow from inventory management
- [ ] **TB-113** `planned` — For markets with extreme probabilities (<5%), require either (a) sustained multi-tick price movement or (b) volume from multiple counterparties, not single-tick volume concentration

---

## 2026-04-06 — Advisor snapshot 38

### Summary
Ultra-thin micro-cap markets are generating false positives: tiny absolute volumes trigger outsized percentage price moves, creating high-scoring signals that lack genuine information content.

### Next step
Introduce a volume-relative threshold: require spike_min_volume_delta to be a minimum percentage of the market's baseline daily volume (e.g., 2-5%) rather than an absolute number. This filters noise in thin markets while preserving sensitivity in liquid ones.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `2.5`

### Recommendations

- [ ] **TB-114** `planned` — Add a daily-volume-relative gate: only flag spikes where volΔ ≥ 3% of 7-day average daily volume; exempts thin markets like STUP (197 shares ≈ 0.3% of 62k baseline) while catching real moves in liquid pairs
- [ ] **TB-115** `planned` — Require sustained multi-tick confirmation for ultra-low-probability markets (<5%): single-tick price moves are more susceptible to bid-ask bounce and crossing order noise; require at least 2 consecutive ticks in same direction
- [ ] **TB-116** `planned` — Raise spike_min_price_move to 0.04 (4%) for markets with <20k daily volume baseline; keeps sensitivity for normal markets while eliminating tick-scale churn in micro-caps

---

## 2026-04-06 — Advisor snapshot 39

### Summary
Detector is triggering on low-conviction, thin-market microbursts—high volume deltas without price persistence, single-tick moves in ultra-low-probability markets, and negligible absolute volumes. These are noise spikes, not genuine flow signals.

### Next step
Require price persistence (5+ minute hold) or multi-sided order book activity before emitting watch-tier signals; this filters one-directional dumps that reverse immediately.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `5.5`

### Recommendations

- [ ] **TB-117** `planned` — Add price_persistence_minutes=5 rule: price move must hold for at least 5 minutes to qualify, eliminating immediate counterparty absorption reversals
- [ ] **TB-118** `planned` — Implement minimum_volume_pct_of_baseline: flag only when volΔ exceeds 2-5% of market's rolling 24h baseline volume, not just absolute deltas (STUP's 197 shares is <0.3% of 62k baseline)
- [ ] **TB-119** `planned` — Require multi-sided activity for ultra-low-probability markets (<5% implied): demand both buy and sell-side order book acceleration, not unidirectional volume spikes

---

## 2026-04-06 — Advisor snapshot 40

### Summary
Low-probability markets are generating high false-positive rates due to outsized percentage moves on small absolute volumes, and volume spikes without price persistence are being flagged despite lacking genuine directional conviction.

### Next step
Require multi-tick price persistence (≥2 consecutive ticks holding direction) or bilateral order activity, rather than relying on single-tick moves or one-directional absorption patterns.

### Suggested thresholds
`min_volume_delta` → `120000.0`, `min_price_move` → `0.015`

### Recommendations

- [ ] **TB-120** `planned` — Add price_persistence_ticks=2 requirement: price move must hold across at least 2 consecutive ticks before triggering signal
- [ ] **TB-121** `planned` — For markets with yes_prob < 0.05, raise min_volume_delta threshold by 50% or require minimum single-trade size to reduce noise from fragmented small orders
- [ ] **TB-122** `planned` — Add bilateral_activity check: reject signals where >80% of volume delta is one-directional without meaningful counterparty absorption at new price level

---

## 2026-04-06 — Advisor snapshot 41

### Summary
Detector is triggering on quote-driven volume without executed trades and one-directional price spikes that fail to persist, generating noise on low-conviction moves.

### Next step
Add execution quality filters: require minimum trade count (25+ executed trades) and price persistence (5+ minute hold) before emitting spike signals, rather than relying on volume and price deltas alone.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-123** `planned` — Introduce min_executed_trades threshold of 25+ to filter quote-stuffing and large quoted volumes without actual fills
- [ ] **TB-124** `planned` — Add price_persistence_window of 5 minutes: price move must hold at ≥80% of peak delta for signal to qualify
- [ ] **TB-125** `planned` — Implement executed_to_quoted_ratio minimum (e.g., 0.4+) to ensure meaningful traded volume backs volume delta claims
- [ ] **TB-126** `planned` — Raise spike_score_threshold from current baseline to 6.5+ given the high false-positive rate at scores near 2.6 and 9.0 with poor fundamentals

---

## 2026-04-06 — Advisor snapshot 42

### Summary
Large volume spikes in micro-cap/illiquid markets are triggering false positives despite zero or negligible price impact, indicating volume alone is insufficient for signal quality.

### Next step
Require minimum price movement alongside volume delta in low-liquidity markets, or filter signals where volume delta exceeds executed notional by a wide margin (quote refresh artifact).

### Suggested thresholds
`min_price_move` → `0.01`, `score_threshold` → `10.0`

### Recommendations

- [ ] **TB-127** `planned` — Add a co-requisite rule: if probability < 5% (illiquid), require priceΔ ≥ 0.01 (1%) alongside any volume spike to reduce quote-refresh noise
- [ ] **TB-128** `planned` — Implement volume-weighted conviction check: reject signals where volΔ >> typical trade size for that market; use median trade size or 20th percentile as baseline
- [ ] **TB-129** `planned` — Raise spike_score_threshold to 10.0+ for markets with < 5% implied probability to filter low-confidence signals in thin order books

---

## 2026-04-06 — Advisor snapshot 43

### Summary
Both signals fired on micro-cap markets with high volume deltas but minimal or zero price impact, indicating the detector is triggering on liquidity noise rather than genuine directional conviction.

### Next step
Require minimum price move sustained alongside volume spike in micro-cap markets; add notional volume floor (~$500k) for tail-event contracts to filter out thin-book noise.

### Suggested thresholds
`min_volume_delta` → `200000.0`, `min_price_move` → `0.03`, `score_threshold` → `12.0`

### Recommendations

- [ ] **TB-130** `planned` — Enforce spike_min_price_move >= 0.03 (3%) when spike_min_volume_delta > 200k, or require price move to persist across 2+ consecutive 1-min candles
- [ ] **TB-131** `planned` — Add notional volume filter: reject signals where (volume_delta * mid_price) < $500k for contracts with <$2M open interest
- [ ] **TB-132** `planned` — For zero or near-zero price impact (priceΔ < 0.01) with high volume, downweight score by 60% or exclude entirely, as this signals cross-side liquidity provision rather than directional pressure

---

## 2026-04-06 — Advisor snapshot 44

### Summary
Ultra-low-price markets (<5¢) are generating false positives due to algorithmic order splitting and micro-market noise, with scores well below typical quality thresholds yet still triggering detection.

### Next step
Introduce market-tier-specific thresholds: require either sustained multi-minute price holds above spike level OR minimum per-trade size filters for markets with notional values <$500k, combined with a price-move floor of 5% for low-probability tail events.

### Suggested thresholds
`min_volume_delta` → `500000.0`, `min_price_move` → `0.05`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-133** `planned` — For markets <5¢: require minimum per-trade size (e.g., >$5k notional per order) OR sustained price hold >2 minutes above spike level to filter algorithmic splitting
- [ ] **TB-134** `planned` — For low-probability tail events (yes probability <0.05): enforce minimum absolute volume threshold of $500k notional OR minimum price move of 5% to suppress micro-market noise
- [ ] **TB-135** `planned` — Raise spike_score_threshold to 3.5+ for markets with <$500k notional to block marginal signals like the 2.451 score on RIGG

---

## 2026-04-06 — Advisor snapshot 45

### Summary
Both recent false positives occur in ultra-low-price markets with large volume deltas but minimal sustained price impact, suggesting the detector is picking up liquidity noise and algorithmic order fragmentation rather than informed flow.

### Next step
Implement a price-hold duration filter: require detected price moves to persist for at least 2-3 minutes before emitting a signal, or add minimum per-trade size enforcement for markets under 5¢ to filter algorithmic splitting.

### Suggested thresholds
`min_volume_delta` → `150000.0`, `min_price_move` → `0.05`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-136** `planned` — Add a 2-minute price persistence check: if price reverts >50% within 5 minutes of spike detection, downgrade or suppress the alert tier
- [ ] **TB-137** `planned` — For markets with absolute price <$0.05, enforce minimum single-trade notional value (e.g. $50-100 per trade) to exclude algorithmic order splitting that fragments volume across many micro-orders
- [ ] **TB-138** `planned` — Require multi-minute volume sustainability: spike must sustain elevated volume flow for ≥2 consecutive minutes; single-minute volume spikes with rapid reversion are noise

---

## 2026-04-06 — Advisor snapshot 46

### Summary
Detector is triggering on passive liquidity events and expired/settled markets where volume deltas lack genuine repricing signals, creating false positives despite moderate scores.

### Next step
Add market-state validation: exclude or heavily downweight signals from markets where resolution_date <= current_date, and implement quote/trade volume decomposition to filter passive liquidity masquerading as informative flow.

### Suggested thresholds
`min_price_move` → `0.02`, `score_threshold` → `4.0`

### Recommendations

- [ ] **TB-139** `planned` — Reject or tier-down signals from markets with resolution_date in past; KXTRUMPSAY-26APR06-RIGG shows large volume delta (163k) with minimal price move (3%) typical of settlement mechanics rather than information flow.
- [ ] **TB-140** `planned` — Decompose volume delta by side (quote vs trade): KXTRUMPSAY-26APR06-NOBE has 107k volume delta but 0% price move, suggesting passive MM liquidity provision. Flag these separately or apply 2x score penalty when price_move < 1%.
- [ ] **TB-141** `planned` — Raise score_threshold from current implied ~3.0-3.6 range to 4.0+ when price_move < 2%, or require additional confirmation signals (bid-ask spread, order-book imbalance) before emitting watch-tier alerts.

---

## 2026-04-06 — Advisor snapshot 47

### Summary
Detector is flagging low-conviction signals in ultra-low-probability markets where passive liquidity provision mimics genuine repricing. The first signal shows technical artifacts at extreme price levels, the second shows volume movement without actual price discovery.

### Next step
Implement price-range filtering (exclude price <= $0.00 or >= $0.95) and volume-side discrimination for markets with implied probability < 5%, separating quote-side passive liquidity from trade-side active repricing.

### Suggested thresholds
`min_price_move` → `0.01`, `score_threshold` → `3.8`

### Recommendations

- [ ] **TB-142** `planned` — Filter out quotes with price = $0.00 or price > $0.95 to eliminate technical artifacts and focus on economically meaningful trading activity
- [ ] **TB-143** `planned` — For ultra-low-probability markets (<5% implied), flag large quote-side volume separately and require trade-side confirmation before emitting signal
- [ ] **TB-144** `planned` — Raise score_threshold to 3.8+ to eliminate tier=watch signals with priceΔ = 0.0 or priceΔ < 0.01 in low-conviction regimes

---

## 2026-04-06 — Advisor snapshot 48

### Summary
Watch-tier alerts are triggering on ultra-low-probability political markets with minimal price moves (0.00–0.03) and ambiguous volume signals that lack sustained directional bias or meaningful trade-side activity. The detector is conflating passive liquidity provision with genuine repricing.

### Next step
Implement dual-volume tracking (quote-side vs. trade-side) and enforce minimum contract thresholds for ultra-low-probability markets (<5% implied probability) before emitting watch-tier signals.

### Suggested thresholds
`min_volume_delta` → `300000.0`, `min_price_move` → `0.02`, `score_threshold` → `4.0`

### Recommendations

- [ ] **TB-145** `planned` — Require minimum 50+ executed contracts (trade-side volume) per spike window for markets with yes-price ≤ $0.05, regardless of quote-side volume delta.
- [ ] **TB-146** `planned` — Separate quote-side volume from trade-side volume in score calculation; only count trade-side volume toward spike_min_volume_delta for markets under $0.05.
- [ ] **TB-147** `planned` — Exclude price moves ≤ 0.01 (1%) from triggering watch-tier alerts; raise minimum to 0.02 for markets with yes-price < $0.03.
- [ ] **TB-148** `planned` — Add persistence filter: require multi-minute directional bias (≥2 consecutive samples in same direction) before flagging watch tier on ultra-low-probability markets.

---

## 2026-04-06 — Advisor snapshot 49

### Summary
Low-probability political speech markets are generating watch-tier alerts on minimal volume and price moves (2-3% moves on <0.05 contracts), creating noise that drowns out genuine signal.

### Next step
Implement market-depth-aware thresholds: require either absolute minimum trade size (50+ contracts) OR sustained directional bias across multiple minutes for sub-$0.05 markets, rather than relying on volume delta and price move percentages alone.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-149** `planned` — Add absolute contract minimum (50+ contracts per trade) for markets with yes-probability <0.05 or price <$0.05 before triggering watch-tier alerts
- [ ] **TB-150** `planned` — Exclude technical artifacts: filter out quotes at price=$0.00 or price>$0.95 to focus on economically meaningful trading range
- [ ] **TB-151** `planned` — For binary event markets with shallow depth, require volume_delta to represent 5-10% of baseline rolling volume or price_move >5%, not just 2-3% fractional moves

---

## 2026-04-06 — Advisor snapshot 50

### Summary
Ultra-low-probability political markets (<5%) are generating watch-tier false positives from small absolute trades creating outsized percentage moves without genuine conviction. The detector is too sensitive to price moves in illiquid markets with minimal volume anchors.

### Next step
Implement market-context-aware thresholds: require minimum absolute trade volume (50+ contracts) and filter edge-case price ranges ($0.00, >$0.95) before applying percentage-based move detection on low-probability events.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-152** `planned` — Add minimum absolute trade volume gate of 50 contracts before triggering watch-tier on markets with yes-price <5%, regardless of percentage move or volume delta
- [ ] **TB-153** `planned` — Exclude signals where price is $0.00 or >$0.95 to filter technical artifacts and focus on economically meaningful trading
- [ ] **TB-154** `planned` — Raise spike_min_volume_delta to 5-10% of baseline rolling volume for binary event markets with <$10k depth, rather than fixed absolute thresholds

---

## 2026-04-06 — Advisor snapshot 51

### Summary
All five recent watch-tier signals are labeled as false positives. The detector is triggering on mechanical/trivial activity in ultra-low-probability political markets (<5% implied), where small absolute volumes create outsized percentage moves without genuine conviction.

### Next step
Implement a minimum absolute trade volume threshold (50–100 contracts) for watch-tier alerts on markets with yes-price <$0.05, combined with a baseline volume delta filter (5–10% of rolling baseline) to distinguish real flow from market-making noise.

### Suggested thresholds
`score_threshold` → `4.5`

### Recommendations

- [ ] **TB-155** `planned` — Reject watch-tier alerts on markets with yes-price <$0.05 unless trade volume exceeds 50 contracts or volume delta is >10% of baseline
- [ ] **TB-156** `planned` — Filter out quotes at price extremes (price ≤$0.00 or price ≥$0.95) to eliminate technical artifacts in low-liquidity binary markets
- [ ] **TB-157** `planned` — For watch-tier alerts, require volume delta to exceed 5–10% of rolling baseline volume rather than absolute deltas, which are context-blind in low-liquidity venues

---

## 2026-04-06 — Advisor snapshot 52

### Summary
Watch-tier alerts are triggering on mechanical micro-moves in ultra-low-probability political markets (<5%) with insufficient conviction signals. Volume deltas appear large in absolute terms but represent trivial percentages of baseline liquidity, while price moves of 2-3% lack substantive market conviction.

### Next step
Implement tier-specific thresholds: require volume delta to exceed 5-10% of baseline liquidity for watch-tier alerts, and enforce minimum absolute trade size (50+ contracts) or price-move floors (>5%) for sub-$0.05 binary event markets.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `4.5`

### Recommendations

- [ ] **TB-158** `planned` — For watch-tier alerts on markets with yes-probability <5%: require volumeΔ ≥ 5-10% of recent baseline volume, not absolute deltas, to filter mechanical market-making noise
- [ ] **TB-159** `planned` — Enforce minimum absolute trade size threshold (50+ contracts) or minimum price move (>5%) for ultra-low-probability political speech markets trading under $0.05
- [ ] **TB-160** `planned` — Add conviction filter: require sustained multi-minute directional bias or explicit tape evidence before flagging single trades on low-liquidity pairs

---

## 2026-04-06 — Advisor snapshot 53

### Summary
Watch-tier alerts are triggering on mechanical micro-movements in low-liquidity markets. Volume deltas are too small relative to baseline, and price moves lack conviction even when absolute volume numbers appear large.

### Next step
Implement volume-delta as a percentage of baseline rather than absolute units, with market-liquidity-aware thresholds. Require minimum 5-10% baseline volume delta for low-liquidity watch-tier markets.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `4.5`

### Recommendations

- [ ] **TB-161** `planned` — Replace absolute spike_min_volume_delta with a percentage-of-baseline rule: require ≥5% of recent baseline volume for watch-tier alerts on markets with <$100k typical depth
- [ ] **TB-162** `planned` — Increase spike_min_price_move to 0.05 (5%) for watch-tier alerts on markets with probability <5% or baseline volume <1000 contracts
- [ ] **TB-163** `planned` — Raise spike_score_threshold to ≥4.5 for watch-tier alerts on low-conviction markets (yes/no probabilities in outer 5% ranges)

---

## 2026-04-06 — Advisor snapshot 54

### Summary
Watch-tier alerts are triggering on mechanical micro-moves in low-liquidity markets: tiny absolute volume shifts and sub-3% price moves in ultra-low-probability contracts are generating noise without conviction.

### Next step
Introduce liquidity-aware thresholds: require volume delta as a percentage of baseline volume (not absolute delta), and enforce minimum absolute trade size for sub-5% probability markets to filter out trivial fills.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `4.5`

### Recommendations

- [ ] **TB-164** `planned` — For watch-tier alerts on markets with <5% implied probability, require minimum absolute volume delta of at least 500–1000 contracts (or equivalent notional) to filter out single-lot fills.
- [ ] **TB-165** `planned` — Replace absolute volume_delta with percentage-of-baseline metric: require volΔ ≥ 5–10% of the preceding 1-hour baseline volume for watch-tier, not raw deltas like 149 or 111840 which are meaningless without context.
- [ ] **TB-166** `planned` — Raise spike_min_price_move to 0.05 (5%) for watch-tier on low-liquidity venues, since 2–6% moves in illiquid markets are routine market-making spread adjustments, not genuine flow.

---

## 2026-04-06 — Advisor snapshot 55

### Summary
False positives are driven by two distinct failure modes: (1) low-baseline volume amplification turning small absolute trades into extreme spike scores, and (2) quote-management noise in high-volume markets being flagged as meaningful price signals despite minimal fractional moves.

### Next step
Implement a minimum baseline volume gate before computing volume multiples, combined with a relative volume delta threshold that scales with market size. This prevents both extreme-score amplification on thin books and noise-flagging on liquid markets.

### Suggested thresholds
`min_price_move` → `0.04`

### Recommendations

- [ ] **TB-167** `planned` — Add a min_baseline_volume_contracts threshold (e.g., 500) that must be met before a signal qualifies; signals below baseline are suppressed or downtiered automatically.
- [ ] **TB-168** `planned` — Replace or augment spike_min_volume_delta with a relative threshold (e.g., volΔ must exceed 5-10% of rolling baseline volume, not just an absolute delta) to avoid noise in high-volume markets.
- [ ] **TB-169** `planned` — Raise spike_min_price_move to 0.04–0.05 (4–5%) for 'watch' tier on markets with volΔ < 10% of baseline, since sub-3% moves without proportional volume are likely quote management rather than information.

---

## 2026-04-06 — Advisor snapshot 56

### Summary
The detector is generating false positives on thin/expiring markets and low-baseline contracts. Expiration-driven liquidations, quote management noise, and extreme volume multiples on tiny baselines are being flagged as genuine signals.

### Next step
Implement a baseline volume floor (500+ contracts) before computing spike scores, and apply a time-decay multiplier that attenuates signals within 24 hours of market expiration.

### Suggested thresholds
`min_volume_delta` → `0.05`, `score_threshold` → `50.0`

### Recommendations

- [ ] **TB-170** `planned` — Require minimum baseline volume of 500+ contracts before flagging any volume delta multiples; reject spike signals on markets below this floor
- [ ] **TB-171** `planned` — Apply 0.5x decay multiplier to spike scores for markets within 24 hours of expiration to suppress deadline-driven settlement positioning artifacts
- [ ] **TB-172** `planned` — Raise spike_min_volume_delta to 5–10% of recent baseline volume for 'watch' and 'notable' tiers to filter out quote management noise and sub-1% moves

---

## 2026-04-06 — Advisor snapshot 57

### Summary
Detector is generating false positives on thin/expiring markets by treating small absolute volumes and deadline-driven liquidations as informative flow signals. Extreme spike scores on low-baseline markets and quote management noise on high-volume markets are also inflating false alerts.

### Next step
Introduce market-context filters before spike scoring: require minimum baseline volume threshold (~500 contracts), apply expiration-proximity decay (down-weight <24h to expiry), and enforce directional-flow validation (>70% one-sided over 30+ trades) for ultra-low-probability markets.

### Suggested thresholds
`score_threshold` → `5.0`

### Recommendations

- [ ] **TB-173** `planned` — Add baseline volume gate: skip spike detection entirely if 24h baseline volume < 500 contracts (prevents extreme score inflation on thin order books)
- [ ] **TB-174** `planned` — Apply expiration decay: reduce spike_score by 40-60% for markets within 24 hours of expiry to suppress settlement/liquidation noise
- [ ] **TB-175** `planned` — For markets with implied probability <5%, require sustained directional flow (>70% one-sided over minimum 30 trades) instead of single-spike triggers
- [ ] **TB-176** `planned` — Raise volume-delta sensitivity on high-volume markets: require volΔ ≥ 5-10% of baseline before flagging 'watch' tier (not absolute delta)
- [ ] **TB-177** `planned` — Reduce score_threshold for markets meeting directional-flow criteria to allow genuine low-probability signals through, while keeping baseline threshold high

---

## 2026-04-06 — Advisor snapshot 58

### Summary
False positives are driven by thin order books amplifying small absolute volumes into high spike scores, and by deadline/liquidation effects in low-probability markets near expiration. Quote-adjustment noise on sub-1% price moves is triggering watch/notable tiers inappropriately.

### Next step
Implement a baseline volume floor (500+ contracts) and context-aware penalties: require either (a) price move >5% for low-liquidity markets, (b) sustained directional flow (>70% one-sided) for ultra-low-probability markets, or (c) score suppression for markets within 24 hours of expiration.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-178** `planned` — Enforce minimum baseline volume threshold of 500+ contracts before applying volume-multiple scoring; markets below this floor should not generate spike signals.
- [ ] **TB-179** `planned` — For markets with probability <5% OR <24 hours to expiration, require either price move >5% OR sustained directional flow (>70% one-sided over 30+ trades) instead of brief volume spikes.
- [ ] **TB-180** `planned` — For high-volume markets (>10k baseline contracts), raise minimum volume delta to 5–10% of baseline; sub-1% deltas are quote management noise and should not trigger 'watch' tier.

---

## 2026-04-06 — Advisor snapshot 59

### Summary
The detector is generating high-scoring false positives on thin markets, low-liquidity pairs, and markets near expiration by amplifying small absolute volumes into inflated spike scores. Quote-management activity and settlement positioning are being misclassified as informed flow.

### Next step
Implement a baseline volume floor (500+ contracts minimum) and require contextual filters (time-to-expiration, one-sidedness duration, baseline liquidity %) before scoring volume multiples, rather than relying on raw deltas and price moves alone.

### Suggested thresholds
`min_volume_delta` → `500.0`

### Recommendations

- [ ] **TB-181** `planned` — Require minimum baseline volume threshold of 500+ contracts before flagging any volume delta multiple; reject signals where baseline < 500 regardless of delta ratio
- [ ] **TB-182** `planned` — Penalize spike scores by 60-80% for markets within 24 hours of expiration, and by 40% for markets within 72 hours, to account for liquidation and settlement noise
- [ ] **TB-183** `planned` — For ultra-low-probability markets (yes-prob < 5%), require sustained one-sided directional flow (>70% same-side trades) over 30+ consecutive trades rather than brief spikes to confirm informed flow vs. quote-adjustment noise
- [ ] **TB-184** `planned` — For high-volume baseline markets (>10k contracts), require volume delta to be >5-10% of baseline before escalating to 'notable' tier; sub-1% deltas should remain 'watch' or below
- [ ] **TB-185** `planned` — Add a filter to exclude single-sided order-book quotes >2M volume that lack follow-on trade aggression or sustained price impact, as these typically indicate market-maker depth rather than informed flow

---

## 2026-04-06 — Advisor snapshot 60

### Summary
System is emitting high-confidence scores on low-signal activity: quote-adjustment noise on thin books, deadline-driven liquidations in near-expiration markets, and single-sided market-maker volume that lacks follow-on aggression or sustained directional flow.

### Next step
Implement market-context filters (baseline volume percentage, time-to-expiration discount, directional persistence check) before relying on raw volume and price deltas, rather than raising thresholds uniformly.

### Suggested thresholds
`score_threshold` → `5.0`

### Recommendations

- [ ] **TB-186** `planned` — Require volume delta ≥5-10% of baseline market volume for 'watch' and 'notable' tiers, not absolute volume, to filter quote-adjustment noise on thin order books
- [ ] **TB-187** `planned` — Apply expiration-penalty scoring: discount or suppress spike signals within 24 hours of market settlement, as liquidation and positioning activity is structural noise
- [ ] **TB-188** `planned` — For ultra-low probability markets (<5%), require sustained directional flow (>70% one-sided over 30+ trades minimum) instead of brief volume spikes, to distinguish informed flow from thin-book artifacts
- [ ] **TB-189** `planned` — Flag and downweight single-sided quote blocks >2M volume when they lack correlated follow-on trade aggression or sustained price movement, as these are typically market-maker inventory management

---

## 2026-04-06 — Advisor snapshot 61

### Summary
False positives cluster around thin/low-liquidity markets, single-sided market-maker quotes, ultra-low-probability instruments, and expiration-driven liquidations. Current thresholds trigger on volume and price moves that lack genuine informed flow signals.

### Next step
Implement context-aware filtering: require sustained directional flow (>70% one-sided over 30+ trades) for ultra-low-probability markets (<5%), add liquidity-relative thresholds (5-10% of baseline volume), apply expiration decay (downweight signals <24h to expiry), and explicitly filter single-sided quotes >2M without follow-on aggression.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-190** `planned` — For markets with yes probability <5%: require sustained one-sided flow >70% over 30+ trades instead of single spike, to filter thin-market artifacts
- [ ] **TB-191** `planned` — Replace absolute volume_delta with liquidity-relative threshold: require volΔ to exceed 5-10% of baseline 24h volume, or price_move >5% for low-liquidity pairs
- [ ] **TB-192** `planned` — Add expiration proximity decay: reduce spike_score by 30-50% for signals <24h from market close, as liquidations and settlement positioning are structural not informational
- [ ] **TB-193** `planned` — Filter single-sided quote noise: exclude signals where volume spike is dominated by one-sided quotes >2M without subsequent aggressive counter-flow within 5 minutes

---

## 2026-04-06 — Advisor snapshot 62

### Summary
False positives are driven by market-maker quote adjustments and thin-book noise rather than informed flow. Large single-sided volume spikes without sustained price action or directional aggression are being incorrectly flagged as signals.

### Next step
Introduce a sustained directional flow requirement (>70% one-sided volume over a rolling window) as a gating filter before emitting signals, especially in low-liquidity or ultra-low-probability markets.

### Suggested thresholds
`min_volume_delta` → `500000.0`, `min_price_move` → `0.05`, `score_threshold` → `2.5`

### Recommendations

- [ ] **TB-194** `planned` — Filter out single-sided quote blocks >2M volume that fail to correlate with sustained price moves or follow-on aggression—flag these as MM activity, not informed flow
- [ ] **TB-195** `planned` — Raise minimum volume delta thresholds dynamically based on baseline liquidity: require volΔ to be at least 5-10% of 24h or hourly baseline to reduce thin-book noise
- [ ] **TB-196** `planned` — For markets with implied probability <5%, require >70% directional concentration over 30+ trades and >2% price move; brief spikes on ultra-thin order books are uninformative

---

## 2026-04-06 — Advisor snapshot 63

### Summary
System is generating false positives in low-liquidity and ultra-low-probability markets by flagging quote-driven noise and single large unexecuted orders as informed flow. Volume spikes lack confirmation through sustained directional trade execution.

### Next step
Implement executed-to-quoted volume ratio filter (require >5-10% of flagged volume to be actual executed trades) before emitting signals, especially for markets with implied probability <5% or baseline volume <500k.

### Suggested thresholds
`min_volume_delta` → `500000.0`, `min_price_move` → `0.05`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-197** `planned` — Add executed_trade_ratio requirement: reject signals where executed trades represent <5% of reported volume delta, filtering quote-only noise
- [ ] **TB-198** `planned` — For ultra-low-probability markets (<5% implied prob), require sustained directional flow (>70% one-sided over 30+ trades) rather than single-spike detection
- [ ] **TB-199** `planned` — Exclude or downweight single-sided quotes >2M volume that lack follow-on trade aggression or sustained price movement correlation; treat as likely market-maker activity
- [ ] **TB-200** `planned` — Raise minimum volume threshold for thin markets: require volΔ to exceed 10% of baseline volume or price move >5%, whichever is more conservative

---

## 2026-04-06 — Advisor snapshot 64

### Summary
The detector is triggering on quote-driven noise rather than executed trades, particularly in low-liquidity markets where large unexecuted orders and single-sided quotes create false signals despite weak price conviction.

### Next step
Introduce an executed-to-quoted volume ratio filter (minimum 5-10% of flagged volume must be actual executed trades) to distinguish real conviction from quote noise, especially in markets with implied probability <5%.

### Suggested thresholds
`min_volume_delta` → `500000.0`, `min_price_move` → `0.04`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-201** `planned` — Add executed_trade_ratio requirement: filter out spikes where executed volume is <5% of total quoted volume delta, or require >10% ratio for markets with prob <5%
- [ ] **TB-202** `planned` — Exclude single-sided quotes >2M volume that lack sustained multi-trade follow-on or correlated price movement; flag as market-maker activity rather than informed flow
- [ ] **TB-203** `planned` — Raise minimum volume delta baseline to 5-10% of recent baseline trading volume (not absolute delta), or require price_move >0.05 (5%) for thin markets, to suppress order-book adjustment noise

---

## 2026-04-06 — Advisor snapshot 65

### Summary
Current detector is generating false positives in low-liquidity, low-probability markets by triggering on large unexecuted quote volume without distinguishing real conviction (executed trades) from quote-driven noise.

### Next step
Implement a mandatory executed-to-quoted volume ratio filter (5-10% minimum) before any signal emission, regardless of score or volume delta magnitude.

### Suggested thresholds
`score_threshold` → `4.5`

### Recommendations

- [ ] **TB-204** `planned` — Add executed_trade_ratio requirement: flag only when executed trade volume exceeds 5-10% of total flagged volume delta, filtering out quote-only spikes
- [ ] **TB-205** `planned` — For markets with implied probability <5%, require multi-trade confirmation in the direction of price move rather than single large quotes, even if volume delta is high
- [ ] **TB-206** `planned` — Increase spike_score_threshold to 4.0+ to suppress watch-tier signals (score ~2.3-3.8) in thin markets; require score ≥4.5 for volume deltas >2M without strong executed volume backing

---

## 2026-04-06 — Advisor snapshot 66

### Summary
Two consecutive false positives driven by thin-market volume spikes without meaningful price movement or informed flow signals. The detector is over-weighting volume deltas in low-liquidity venues and ignoring the absence of price action as a disqualifier.

### Next step
Implement a minimum absolute volume floor (not just multiplier-based delta) and require price movement as a gating condition rather than a weak contributor to scoring, especially in thin markets.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-207** `planned` — Add minimum absolute volume gate: require volΔ > 500 shares (or market-dependent baseline) before scoring, to filter routine small-market trades
- [ ] **TB-208** `planned` — Enforce price-movement gate for watch tier and above: require priceΔ >= 0.01 (1%) as a mandatory condition, not just a scoring factor—high volume with zero price move is liquidity provision, not informed flow
- [ ] **TB-209** `planned` — Reduce score weighting of volume delta in low-baseline venues: apply a liquidity-adjusted penalty to score when hourly baseline < 200 shares, or use percentile-based thresholds instead of raw deltas

---

## 2026-04-06 — Advisor snapshot 67

### Summary
Low-absolute-volume markets are generating false positives through high multiplier ratios on routine trades. The detector is conflating relative volatility (high % moves on tiny baselines) with informed flow.

### Next step
Introduce a minimum absolute volume floor (e.g., 500+ shares/hour baseline) independent of multiplier-based scoring, to prevent thin markets from triggering alerts on statistically normal small trades.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-210** `planned` — Require minimum absolute volume delta of 500+ shares before any signal can trigger, regardless of multiplier ratio or score
- [ ] **TB-211** `planned` — Add a mandatory price-move floor: watch-tier and notable-tier alerts require ≥1-2% price delta alongside volume spikes in low-liquidity markets (<500 baseline vol/hour)
- [ ] **TB-212** `planned` — For markets with <100 baseline shares/hour, increase spike_min_volume_delta multiplier threshold to 10x+ (not 5-6x) to avoid flagging routine block trades as notable

---

## 2026-04-06 — Advisor snapshot 68

### Summary
Both signals are noisy detections in thin sports-betting markets where small absolute volumes trigger alerts despite marginal price moves. The issue is reliance on volume delta ratios without minimum absolute volume guards.

### Next step
Introduce a minimum absolute volume threshold (e.g., 200–300 contracts) before any signal qualifies as 'notable', regardless of delta ratio or score.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `45.0`

### Recommendations

- [ ] **TB-213** `planned` — Add min_absolute_volume constraint: reject signals where total volume in window < 200 contracts, even if volΔ ratio is high
- [ ] **TB-214** `planned` — Raise spike_min_price_move from 0.02 to 0.04 (4%) for markets with <500 baseline volume to filter single-tick noise
- [ ] **TB-215** `planned` — Require price impact persistence: flag only if price move sustained across 2+ consecutive ticks, not single-tick spikes in thin markets

---

## 2026-04-06 — Advisor snapshot 69

### Summary
The detector is generating false positives in thin sports betting markets by flagging routine liquidity provision and small absolute volumes that trigger high relative deltas. All three recent notable-tier signals were labeled noise/uncertain despite notable scores.

### Next step
Implement a minimum absolute volume threshold (200-250 contracts) before flagging as notable, combined with a dynamic volume delta multiplier that scales with baseline market thickness. This addresses the core issue: relative spike detection fails in thin markets.

### Suggested thresholds
`min_volume_delta` → `40.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-216** `planned` — Add min_absolute_volume_threshold=200 contracts; reject signals where absolute volume activity is below this floor regardless of relative delta or score
- [ ] **TB-217** `planned` — Raise spike_min_volume_delta multiplier to 40-50x for markets with baseline <100 contracts, to filter routine liquidity events in thin baseball/sports markets
- [ ] **TB-218** `planned` — Require sustained price impact (price move confirmed over 2+ consecutive ticks or sustained >2% move) rather than single-tick detection to distinguish genuine flow from noise

---

## 2026-04-06 — Advisor snapshot 70

### Summary
Thin-market sports betting products are generating false positives due to high relative volume multipliers against low absolute baselines; single-tick price moves in low-volume markets are triggering alerts despite minimal absolute activity.

### Next step
Implement a minimum absolute volume threshold (200–300 contracts) before any spike detection triggers, combined with a sustained-move requirement (2+ ticks or 60+ seconds) to filter routine liquidity provision in thin markets.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-219** `planned` — Add min_absolute_volume_threshold = 200–300 contracts; block watch/notable alerts if absolute volume < threshold regardless of relative multiplier
- [ ] **TB-220** `planned` — Require sustained price hold: 2+ consecutive ticks above price_move threshold or 60+ second hold at elevated price to confirm intent vs. one-off fills
- [ ] **TB-221** `planned` — Increase volume delta multiplier for sports markets with baseline < 100 contracts from 34x to 50x+, or apply a market-type-specific multiplier floor

---

## 2026-04-06 — Advisor snapshot 71

### Summary
Low-volume markets are generating false positives due to high relative volume deltas and small absolute price moves triggering alerts. Thin baseline volumes (50-500 contracts) amplify noise when modest absolute volume spikes occur.

### Next step
Implement a minimum absolute volume threshold (200-300 contracts) before flagging as notable or watch-tier, combined with market-specific baseline multiplier requirements that scale by baseline volume.

### Suggested thresholds
`min_volume_delta` → `200.0`

### Recommendations

- [ ] **TB-222** `planned` — Add min_absolute_volume_delta constraint of 200+ contracts for notable tier and 500+ for higher tiers; prevents thin-market noise from triggering alerts
- [ ] **TB-223** `planned` — Scale volume_delta multiplier requirements inversely by baseline: markets with <100 baseline require 50x+ multiplier; 100-500 baseline require 35x+; >500 baseline can use 25x+
- [ ] **TB-224** `planned` — Require sustained price move >2% or >60 second price hold post-spike for markets with baseline <500 contracts to filter out liquidity provision events

---

## 2026-04-06 — Advisor snapshot 72

### Summary
False positives are clustering in low-liquidity markets where routine market-making activity (small volume deltas on thin baselines) triggers alerts despite weak price conviction and low analyst confidence.

### Next step
Implement market-size-aware thresholds: require higher volume delta multipliers and price conviction in thin markets (baseline <500 contracts), and add a sustained-hold duration requirement post-spike.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-225** `planned` — For markets with baseline volume <500 contracts: require volume delta ≥5x baseline AND price move >3% AND 60-second sustained hold, OR raise spike_min_volume_delta to absolute floor of 500+ contracts
- [ ] **TB-226** `planned` — For thin baseball/sports markets (baseline <100 contracts): raise volume delta multiplier from 34x to 50x+ baseline, or require price move >2% independent of volume
- [ ] **TB-227** `planned` — Add post-spike confirmation: only emit watch/notable tier alerts if price move sustains for ≥60 seconds; reject spikes that reverse within 30 seconds

---

## 2026-04-06 — Advisor snapshot 73

### Summary
The detector is triggering on volume deltas without sufficient price conviction or directional flow, particularly in low-volume markets where small absolute changes create large relative deltas.

### Next step
Implement a dual-gate system: require either meaningful price movement (≥0.5%) OR minimum absolute volume threshold (≥100 contracts), rather than treating volume delta as a sufficient signal on its own.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-228** `planned` — Add minimum absolute volume gate: only flag spikes when absolute volume exceeds 100 contracts, preventing low-volume markets from generating false positives on baseline noise
- [ ] **TB-229** `planned` — Increase price_move threshold or create OR condition: require either price_move ≥ 0.5% OR directional flow concentration ≥ 70% on one side to validate volume spike as meaningful flow
- [ ] **TB-230** `planned` — Score penalty for zero/near-zero price movement: reduce spike score by 50% when priceΔ < 0.3% to deprioritize volume-only signals lacking price impact conviction

---

## 2026-04-06 — Advisor snapshot 74

### Summary
False positives are driven by volume spikes in thin markets with minimal price conviction and low absolute trade sizes. The detector is flagging notional volume changes that lack directional commitment or meaningful market impact.

### Next step
Implement market-aware minimum absolute volume thresholds (tiered by market liquidity) rather than relying solely on volume delta, combined with a requirement for either sustained price movement or directional flow concentration (>60% one-sided).

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `6.0`

### Recommendations

- [ ] **TB-231** `planned` — Require minimum absolute volume threshold of 100+ contracts for low-liquidity markets (sports, niche prediction markets) and 500+ for ultra-thin markets before flagging any spike, as baseline deltas of 25-300 contracts in thin markets generate noise
- [ ] **TB-232** `planned` — Add directional flow requirement: flag only when volume delta is concentrated >60% on one side (buy or sell), filtering neutral two-sided volume noise like KXTRUMPSAY-26APR13-TRAN
- [ ] **TB-233** `planned` — Enforce minimum price persistence: require price move to sustain for 2+ consecutive ticks or >0.5% absolute move, preventing single-tick micro-moves from triggering false signals in low-conviction markets

---

## 2026-04-06 — Advisor snapshot 75

### Summary
The detector is generating false positives in low-liquidity and thin markets due to quote-stacking, small notional trades, and volume spikes disconnected from meaningful price conviction. High nominal scores mask low-signal activity.

### Next step
Introduce a minimum trade count and directional flow ratio filter alongside volume/price thresholds to distinguish genuine conviction flow from mechanical quote refresh and thin-market noise.

### Suggested thresholds
`min_volume_delta` → `300.0`, `min_price_move` → `0.005`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-234** `planned` — Require minimum trade count (≥3 trades) accompanying volume delta to filter quote-stacking and refresh patterns on event markets
- [ ] **TB-235** `planned` — For low-absolute-volume markets (sports, niche events), set minimum absolute volume floor (≥100 contracts) before flagging any spike alert
- [ ] **TB-236** `planned` — Add directional flow requirement: either minimum price move (≥0.5%) OR minimum one-sided volume ratio (≥65% of spike volume on single side) to distinguish conviction from neutral order churn
- [ ] **TB-237** `planned` — Implement market-segment-specific baselines: use higher volume delta thresholds for thin markets (adjust 25-contract baseline) and require sustained multi-tick price persistence in low-conviction regimes

---

## 2026-04-06 — Advisor snapshot 76

### Summary
Low-liquidity and event markets are generating false positives from quote-stacking, positioning chatter, and small notional trades that lack price conviction or directional flow persistence.

### Next step
Require corroborating price movement (>0.5-2% depending on market type) OR sustained directional flow (>60% of volume on one side) alongside volume deltas to filter noise in thin markets.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-238** `planned` — Implement minimum absolute volume threshold (~100 contracts) for sports/novelty markets before flagging any spike, since baseline deltas are too small to establish conviction.
- [ ] **TB-239** `planned` — Add minimum trade count requirement (≥3 trades) or minimum trade size threshold (≥500 contracts) to filter quote-refresh and single-large-order artifacts.
- [ ] **TB-240** `planned` — Require either price persistence (>0.5-2% move sustained across 2+ ticks) or directional flow dominance (≥60% of spike volume on one side) to distinguish real flow from positioning chatter.

---

## 2026-04-06 — Advisor snapshot 77

### Summary
The detector is generating false positives on low-conviction volume anomalies in thin/novelty markets by triggering on volume deltas without sufficient price conviction or trade authenticity signals. Most flagged events show large volume spikes but minimal price movement (0.0-0.05), indicating quote-stacking, positioning chatter, or refresh patterns rather than genuine directional flow.

### Next step
Implement a conjunctive filter requiring EITHER (price movement ≥2%) OR (volume delta ≥25x baseline AND minimum trade count ≥3 AND net directional flow ≥60%), with absolute volume floor of 100 contracts for low-liquidity markets.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-241** `planned` — Raise spike_min_price_move to 0.02 (2%) as default, but allow lower thresholds (0.005) only if accompanied by high trade count (≥3) and strong directional imbalance (≥65% one-sided).
- [ ] **TB-242** `planned` — Add minimum trade count validation: require ≥3 distinct trades in the spike window to reject quote-stacking patterns (e.g., TRAN with 9128Δ vol but single refresh).
- [ ] **TB-243** `planned` — Set absolute volume floor at 100 contracts for event/novelty markets (TRUMP, sports) to filter noise from baseline deltas of 9-43 contracts.
- [ ] **TB-244** `planned` — Add net directional flow metric: flag only spikes where ≥60% of volume flows to one side, rejecting two-way positioning chatter.
- [ ] **TB-245** `planned` — Lower score_threshold slightly to ~12 (from current implicit ~14+) only after implementing the above volume/price/trade-count conjunctive gates.

---

## 2026-04-06 — Advisor snapshot 78

### Summary
Low-liquidity and novelty markets are generating false positives from routine positioning and quote-stacking activity. Volume spikes lack price conviction or trade count validation, especially in thin event markets where baseline deltas are naturally small.

### Next step
Implement a corroborating signal requirement: spike_min_price_move should scale with market liquidity tier, and volume spikes must be accompanied by either minimum trade count (>3 trades) or minimum absolute volume thresholds (>100 contracts) before emission.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.025`

### Recommendations

- [ ] **TB-246** `planned` — Require minimum trade count (≥3 distinct trades) accompanying any volume spike detection to filter quote-stacking and refresh patterns in low-liquidity markets.
- [ ] **TB-247** `planned` — Enforce minimum absolute volume threshold (≥100 contracts) for novelty/event markets before flagging alerts, rather than relying on delta multipliers alone in thin markets.
- [ ] **TB-248** `planned` — Scale spike_min_price_move dynamically: require ≥2.5% price move in low-liquidity tiers (baseline volume <500) and ≥1.5% in mid-liquidity tiers to filter low-conviction volume anomalies.

---

## 2026-04-06 — Advisor snapshot 79

### Summary
Low-liquidity novelty markets are generating false positives from routine positioning chatter and quote-stacking activity. Volume spikes lack corroborating price conviction, and small notional trades trigger alerts despite low signal quality.

### Next step
Require minimum price move (2-3%) proportional to volume delta, combined with minimum trade count (≥3) to filter quote-refresh patterns and low-conviction positioning noise.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-249** `planned` — Raise spike_min_price_move from 0.01 to 0.02 (2%) as a baseline, with stricter 0.03+ (3%) requirement when volume delta exceeds 25x baseline
- [ ] **TB-250** `planned` — Add minimum trade count requirement (≥3 distinct trades) accompanying volume spikes to exclude single-order quote-stacking and refresh loops
- [ ] **TB-251** `planned` — Increase spike_min_volume_delta from 17x to 25x baseline for low-liquidity markets (estimated notional <$100k daily), or implement adaptive baseline tied to market depth

---

## 2026-04-06 — Advisor snapshot 80

### Summary
Low-liquidity novelty markets are generating false positives through volume spikes without meaningful price conviction or trade activity. Volume deltas alone are insufficient filters when price moves are minimal (<2%) or quote-stacking dominates.

### Next step
Implement a composite gating rule: require EITHER (price_move ≥ 2% AND volume_delta ≥ 15x baseline) OR (volume_delta ≥ 25x baseline AND trade_count ≥ 3). This prevents thin-market noise while preserving genuine flow signals.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-252** `planned` — Raise minimum price movement threshold to 2% for signals with volume_delta < 25x baseline to filter low-conviction volume anomalies
- [ ] **TB-253** `planned` — Introduce minimum trade count requirement (≥3 trades) for volume spike detection to eliminate quote-stacking and refresh patterns
- [ ] **TB-254** `planned` — Increase minimum volume delta threshold to 25x baseline specifically for low-liquidity markets (ADV < 500 contracts) or novelty event contracts

---

## 2026-04-06 — Advisor snapshot 81

### Summary
The detector is generating false positives on low-liquidity novelty markets by triggering on mechanical quote-stacking and single-trade volume spikes without sufficient price conviction or trade count validation.

### Next step
Introduce a minimum trade count requirement (3+ trades) as a gating filter before any tier assignment, combined with proportional price-move thresholds that scale with volume delta magnitude.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-255** `planned` — Require minimum 3+ trades accompanying any volume spike before flagging as 'watch' or higher tier, filtering single-trade mechanical quotes
- [ ] **TB-256** `planned` — Enforce proportional price-move requirements: spike_min_price_move should scale from 2-3% on high volume deltas (>50x baseline) down to 1% only when volume delta is extreme (>100x) and trade count is 5+
- [ ] **TB-257** `planned` — Increase spike_min_volume_delta from current baseline to 25x for low-liquidity novelty event markets (detected via implicit market depth), or require corroborating 2%+ price move as alternative gating criterion

---

## 2026-04-06 — Advisor snapshot 82

### Summary
The detector is triggering on passive liquidity provision and quote-refresh activity in thin, low-conviction markets, generating false positives across novelty event contracts even at 'notable' tier levels.

### Next step
Introduce a correlated price-movement requirement proportional to volume delta: require min_price_move ≥ 2-3% when volume_delta exceeds 25x baseline, or enforce minimum trade count (≥3) to distinguish informed positioning from mechanical quoting.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-258** `planned` — Raise spike_min_volume_delta to 25x baseline for low-liquidity markets (<500 baseline vol) to filter routine positioning chatter and quote-refresh patterns.
- [ ] **TB-259** `planned` — Implement tiered price-move requirement: if volume_delta > 800, enforce min_price_move ≥ 0.02 (2%); if volume_delta > 5000, enforce min_price_move ≥ 0.03 (3%) to correlate conviction with scale.
- [ ] **TB-260** `planned` — Add minimum trade count gate (≥3 trades per spike window) before emitting 'watch' or 'notable' signals on markets with <1000 baseline volume, filtering single-trade mechanical quotes.

---

## 2026-04-06 — Advisor snapshot 83

### Summary
Low-liquidity novelty markets are generating false positives through volume spikes decoupled from price conviction. Passive liquidity provision and mechanical quotes on thin markets are triggering watch/notable tiers without meaningful directional signal.

### Next step
Require correlated price movement (2-3%) alongside volume spikes as a gate before flagging low-volume markets, rather than relying on volume delta alone.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-261** `planned` — Implement volume-to-price correlation gate: require spike_min_price_move ≥ 0.02 (2%) when spike_min_volume_delta triggers on markets with <500 baseline volume
- [ ] **TB-262** `planned` — Raise minimum trade count requirement to 3+ consecutive trades before escalating to 'watch' tier on low-liquidity venues to filter single-trade mechanical quotes
- [ ] **TB-263** `planned` — Increase spike_min_volume_delta threshold to 25x baseline for novelty/thin markets (as flagged by historical volatility or ADV <100) to suppress routine positioning chatter

---

## 2026-04-06 — Advisor snapshot 84

### Summary
Volume spikes without correlated price movement are generating false positives, especially on thin markets where mechanical quotes and passive liquidity provision dominate. Even high-score signals (e.g., KXTRUMPSAY-26APR13-TDS) lack conviction when price movement is minimal (<1%).

### Next step
Enforce a proportional price-movement requirement: require spike_min_price_move to scale with volume delta, or alternatively, require minimum price move of 1-2% alongside any volume spike flagged as 'watch' or above.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-264** `planned` — Require minimum 1-2% price movement (not just 3bps) to qualify volume spikes as informative on thin markets; decouple low-price-move signals to a separate 'liquidity_anomaly' bucket rather than spike detection.
- [ ] **TB-265** `planned` — Implement a minimum trade count gate (3+ trades) before escalating to 'watch' tier on markets with vol_delta <500, to filter single-trade mechanical quotes.
- [ ] **TB-266** `planned` — Introduce a volume-to-price ratio check: flag only when (priceΔ / spike_min_price_move) × (volΔ / spike_min_volume_delta) exceeds a conviction threshold, filtering low-conviction volume moves.

---

## 2026-04-06 — Advisor snapshot 85

### Summary
Volume spikes on thin markets are triggering false positives without correlated price movement or sufficient trade accumulation; passive liquidity provision and mechanical quotes are being misclassified as informed flow.

### Next step
Require minimum price movement (≥1%) as a gating condition alongside volume delta, and add a minimum trade count filter (3+ trades) before escalating to 'watch' tier on low-volume markets.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-267** `planned` — Enforce spike_min_price_move ≥ 0.01 (1%) as a hard gate when volume delta is moderate (<500); allow lower price thresholds only when volume delta is exceptional (>1000+)
- [ ] **TB-268** `planned` — Add implicit trade_count_min = 3 for markets with volume_base < 500; single-trade spikes should be ignored or tagged separately as 'micro' tier
- [ ] **TB-269** `planned` — Raise spike_min_volume_delta floor to 500–750 on thin markets, or scale it dynamically by recent market volume baseline

---

## 2026-04-06 — Advisor snapshot 86

### Summary
False positives are clustering in thin, low-liquidity markets (sports, niche political) where modest volume moves and market-making activity trigger signals without meaningful price discovery or information content.

### Next step
Implement market-specific minimum notional thresholds (e.g., $2,000–$5,000 for sports/niche markets) and enforce a joint volume–price correlation gate: require either substantial price move (≥1%) OR volume spike paired with directional conviction (yes probability divergence from 0.50).

### Suggested thresholds
`min_volume_delta` → `2000.0`, `min_price_move` → `0.01`, `score_threshold` → `10.5`

### Recommendations

- [ ] **TB-270** `planned` — Segment by market type and liquidity tier; apply stricter volume_delta floors ($2,000+ notional) for sports and thin political markets
- [ ] **TB-271** `planned` — Add a joint gate: spike_min_price_move ≥ 0.01 (1%) OR (volume_delta spike AND |yes_prob – 0.50| ≥ 0.08) to filter passive quotes
- [ ] **TB-272** `planned` — Raise score_threshold to 10–12 range for watch/notable tiers to suppress marginal signals in low-conviction, high-noise regimes

---

## 2026-04-06 — Advisor snapshot 87

### Summary
Both false positives exhibit low price moves (1-13%) with modest volume deltas in thin markets, triggering signals that lack sustained conviction. The detector is sensitive to isolated trades and market-making noise rather than genuine information flow.

### Next step
Implement market-segment-specific notional value thresholds rather than relying solely on volume delta and price move, combined with a requirement for volume concentration across multiple price levels or time clustering.

### Suggested thresholds
`min_volume_delta` → `2000.0`, `min_price_move` → `0.05`, `score_threshold` → `14.5`

### Recommendations

- [ ] **TB-273** `planned` — For sports/prediction markets (tier=notable), require minimum notional trade value of $2,000-$5,000 per spike cluster to filter single-trade and MM noise
- [ ] **TB-274** `planned` — Enforce volume concentration rule: require volume delta to be concentrated across at least 2-3 adjacent price levels or within a tight time window (e.g., <30 seconds) rather than isolated single trades
- [ ] **TB-275** `planned` — Raise spike_min_price_move to 0.05 (5%) for low-liquidity markets (identifiable by thin spreads or recent volume patterns) to reduce sensitivity to normal bid-ask bounce

---

## 2026-04-06 — Advisor snapshot 88

### Summary
Low-liquidity and thin markets are generating false positives from isolated small trades and typical market-making activity that lack genuine directional conviction or sustained flow.

### Next step
Implement market-specific liquidity floors and require trade-cluster validation (minimum trade count, notional value, or price-level distribution) before emitting watch/notable alerts in thin markets.

### Suggested thresholds
`min_volume_delta` → `1500.0`

### Recommendations

- [ ] **TB-276** `planned` — Add minimum trade count requirement (≥5 trades per spike cluster) for markets with baseline volume < 5,000 contracts
- [ ] **TB-277** `planned` — Introduce notional-value floor ($2,000–$5,000 depending on market tier) for sports and binary prediction markets to filter single-trade and market-making noise
- [ ] **TB-278** `planned` — Require directional consistency or sustained multi-level volume (price action across ≥2 distinct price levels) rather than flagging isolated volume spikes in low-liquidity venues

---

## 2026-04-06 — Advisor snapshot 89

### Summary
Low-liquidity political markets are generating false positives from isolated small trades and single-contract spikes that lack sustained confirmation. Volume delta alone is insufficient without trade-count and consistency checks.

### Next step
Implement market-aware filtering: require minimum trade count (≥5 trades) and directional consistency for low-liquidity venues before emitting watch/notable tiers, rather than relying solely on volume and price deltas.

### Suggested thresholds
`min_volume_delta` → `1500.0`

### Recommendations

- [ ] **TB-279** `planned` — Add minimum trade count filter: require ≥5 trades in spike cluster for low-liquidity markets (baseline volume <5k) before flagging as watch or notable
- [ ] **TB-280** `planned` — Enforce directional consistency: require ≥70% of trades in cluster to move same direction before triggering alert, reducing whipsaw noise
- [ ] **TB-281** `planned` — Increase volume delta threshold for low-liquidity tiers: raise spike_min_volume_delta to 1500+ for markets with <10k baseline volume, or scale dynamically by market baseline

---

## 2026-04-06 — Advisor snapshot 90

### Summary
Low-liquidity political markets are generating false positives from single large trades that move price significantly but lack sustained conviction. Both signals show high price moves (12% and 4%) with modest volume on thin order books, triggering alerts despite analyst assessment of noise.

### Next step
Implement trade-count and directional-consistency gating for markets below liquidity threshold, before adjusting raw thresholds. This preserves genuine multi-participant flow while filtering single-contract spikes.

### Suggested thresholds
`min_volume_delta` → `1500.0`

### Recommendations

- [ ] **TB-282** `planned` — Add minimum trade count requirement (≥5 trades within spike window) for markets with baseline volume < 5000 contracts
- [ ] **TB-283** `planned` — Require directional consistency check: 70%+ of trades in spike window must move price in same direction
- [ ] **TB-284** `planned` — Increase spike_min_volume_delta to 1500+ for low-liquidity binary markets, or scale threshold dynamically by 1.5x baseline volume

---

## 2026-04-06 — Advisor snapshot 91

### Summary
Low-liquidity political event markets are generating false positives from one-directional flow and algorithmic activity that lack genuine price discovery signals.

### Next step
Implement multi-sided flow confirmation requirement for high-conviction signals on binary event markets, combined with stricter absolute volume thresholds for low-liquidity venues.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-285** `planned` — Require bid-ask imbalance ratio check: reject signals where >80% of volume delta is one-directional; genuine information typically shows mixed participation
- [ ] **TB-286** `planned` — Raise minimum absolute volume threshold from 6 to 25+ contracts for markets with <500 total daily volume (detect via venue liquidity tier)
- [ ] **TB-287** `planned` — Enforce price-move floor of 0.5% minimum alongside volume spike for low-liquidity markets; require both conditions simultaneously rather than either-or scoring

---

## 2026-04-06 — Advisor snapshot 92

### Summary
High volume deltas without corresponding price movement are generating false positives, particularly on low-liquidity political event markets. Volume alone is insufficient; price impact and flow directionality must be validated.

### Next step
Require minimum price movement (0.5–1%) to accompany volume spikes, especially on low-conviction and low-liquidity markets. For high-conviction markets, add multi-sided flow confirmation to filter one-directional algorithmic positioning.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-288** `planned` — Raise minimum absolute volume threshold from 6 to 25+ contracts for low-liquidity novelty-event markets (e.g., political speech predictions) to filter position-squaring and mechanical rebalancing.
- [ ] **TB-289** `planned` — Enforce minimum price movement ≥0.5% alongside volume spikes on watch-tier and low-conviction markets; relax to ≥0.2% only for high-conviction markets with confirmed multi-sided flow.
- [ ] **TB-290** `planned` — For high-conviction flow signals, add flow-imbalance ratio or multi-sided order confirmation to distinguish genuine information arrival from coordinated one-way positioning.

---

## 2026-04-06 — Advisor snapshot 93

### Summary
High false-positive rate on low-liquidity political event markets driven by volume spikes decoupled from price conviction and one-directional flow; mechanical rebalancing and position-squaring are triggering alerts without genuine information arrival.

### Next step
Require multi-timeframe price confirmation (1m/5m/30m) with minimum ±1% move OR flow-imbalance ratio + minimum absolute volume threshold (25+ contracts) for low-liquidity markets; deprioritize raw volume delta weighting relative to price conviction on sparse-tick markets.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-291** `planned` — Enforce minimum price movement of ±0.5–1% to accompany volume spikes on markets with baseline volume <500 contracts/period; reject volume-only signals.
- [ ] **TB-292** `planned` — For binary political/novelty-event markets (low tick density), raise minimum absolute volume threshold from 6 to 25+ contracts and require price move >0.5% alongside high volume delta.
- [ ] **TB-293** `planned` — Replace one-directional volume weighting with flow-imbalance ratio (e.g., buy-side vol / total vol) and require multi-sided confirmation (40–60% buy/sell split) for high-conviction signals to filter coordinated positioning.
- [ ] **TB-294** `planned` — Introduce multi-timeframe confirmation logic: flag signal only if ±2%+ price move is sustained across 1m AND 5m timeframes, reducing noise from transient tick spikes.

---

## 2026-04-06 — Advisor snapshot 94

### Summary
System is generating false positives on low-liquidity markets (sports betting, political events) where volume spikes occur without meaningful price conviction or multi-directional flow confirmation, treating mechanical rebalancing and thin-book noise as informed positioning.

### Next step
Implement a composite filter requiring price movement ≥0.5–1% to accompany volume spikes on low-conviction markets, rather than relying on volume delta alone; couple this with flow-imbalance ratio and multi-timeframe price confirmation to distinguish genuine information flow from liquidity events.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-295** `planned` — Enforce minimum price move of ±0.5–1% on markets with baseline volume <500 contracts or yes-conviction <0.35, regardless of volume delta magnitude.
- [ ] **TB-296** `planned` — Replace raw volume delta weighting with flow-imbalance ratio (buy-side vs sell-side order imbalance) to filter one-directional mechanical activity on thin order books.
- [ ] **TB-297** `planned` — For binary political/sports markets, require multi-timeframe price confirmation (e.g., 0.5%+ move sustained across 1m, 5m, and 30m candles) before emitting high-conviction signals.
- [ ] **TB-298** `planned` — Raise absolute volume threshold to 25–50 contracts minimum on novelty event markets (political speeches, rare sports outcomes) to avoid flagging algorithmic rebalancing.
- [ ] **TB-299** `planned` — Add flow-direction check: flag only if buy/sell-side order imbalance exceeds 60:40 or similar threshold, reducing false positives from balanced mechanical fills.

---

## 2026-04-06 — Advisor snapshot 95

### Summary
Volume spikes without corresponding price conviction are generating false positives across sports and political prediction markets. Raw volume delta is triggering signals even when price movement is minimal (0.01–0.0), suggesting mechanical rebalancing or thin-book volatility rather than informed flow.

### Next step
Introduce a price-move floor (0.5–1%) for low-baseline-volume markets and weight price movement more heavily relative to volume delta in the composite spike score, especially for categorical and binary events with sparse tick volume.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-300** `planned` — Require minimum price move of ±0.5–1.0% to accompany volume spikes >400 contracts on markets with baseline volume <5000, reducing reliance on raw volume delta alone.
- [ ] **TB-301** `planned` — For sports betting and political event markets, add flow-imbalance ratio (buy/sell-side dominance in recent trades) as a confirmation filter before emitting signals, not just aggregate volume and price.
- [ ] **TB-302** `planned` — Raise minimum absolute volume threshold to 25+ contracts for low-liquidity novelty markets (KXTRUMPSAY, low-tier sports), or implement market-specific volume baselines calibrated to 90th-percentile typical volume.

---

## 2026-04-06 — Advisor snapshot 96

### Summary
Volume spikes are triggering false positives across thin-liquidity sports and political markets without sufficient price conviction or directional flow confirmation. Most noise signals have volume deltas that exceed price moves by orders of magnitude, suggesting volume weighting is too aggressive relative to price action.

### Next step
Implement a multi-factor gating rule: require minimum price movement (0.5–2% depending on market liquidity tier) to accompany volume spikes, and add flow-imbalance or directional confirmation for low-conviction markets before emitting signals.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.015`, `score_threshold` → `150.0`

### Recommendations

- [ ] **TB-303** `planned` — Raise minimum absolute volume delta threshold by market tier: sports pre-game markets 100+ contracts, low-liquidity political events 25+ contracts, instead of current blanket baseline.
- [ ] **TB-304** `planned` — Enforce minimum price-move requirement paired with volume: require ≥0.5–1% price move for low-conviction markets (<0.50 yes probability), ≥2–3% for high-volume categorical events (e.g., sports teams with deep liquidity).
- [ ] **TB-305** `planned` — Add directional flow confirmation filter: for markets with sparse tick data or one-sided volume, require buy/sell imbalance ratio or multi-timeframe price confirmation (e.g., sustained 1m/5m/30m moves) before scoring volume spikes as signals.

---

## 2026-04-06 — Advisor snapshot 97

### Summary
Volume-driven false positives dominate across thin-liquidity sports and political markets; raw volume delta is triggering signals without corresponding price conviction or directional flow confirmation.

### Next step
Shift from volume-centric detection to flow-imbalance ratio + multi-timeframe price confirmation. Require minimum 1-2% directional price move OR visible buy/sell-side dominance in recent trades before emitting signal on volume spikes alone.

### Suggested thresholds
`min_volume_delta` → `150.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-306** `planned` — For sports markets (low baseline liquidity): require minimum ±1% price move to accompany volume delta >500, or implement order-flow imbalance scoring (buy vs sell volume ratio) instead of raw delta.
- [ ] **TB-307** `planned` — For political/binary event markets: mandate multi-sided flow confirmation—reject signals where >80% of spike volume is one-directional, as coordinated positioning is not information signal.
- [ ] **TB-308** `planned` — Implement market-segment thresholds: raise spike_min_price_move to 0.02 (2%) for low-liquidity categorical sports, keep 0.03 (3%) for high-liquidity binary events, require 0.05+ (5%) only when volume_delta exceeds 2500 on thin books.

---

## 2026-04-06 — Advisor snapshot 98

### Summary
Volume spikes alone are triggering false positives across thin-liquidity markets (sports betting, low-volume prediction markets) without corresponding price conviction or directional flow confirmation. Price moves of 1% or less paired with large volume deltas are generating noise.

### Next step
Require multi-factor confirmation: pair volume delta with minimum directional price movement (0.02–0.03 for thin markets, 0.02 for liquid ones) AND flow-imbalance directionality, rather than treating volume as a standalone signal.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-309** `planned` — For sports betting markets (thin liquidity): raise spike_min_volume_delta from 30 to 100–150 to filter natural pre-game volatility swings
- [ ] **TB-310** `planned` — Require minimum price_move of 0.02 (2%) paired with volume spike, or 0.03+ (3%) for high-liquidity categorical events to reduce mechanical rebalancing noise
- [ ] **TB-311** `planned` — Add flow-imbalance filter: only flag volume spikes if buy/sell-side trade dominance ratio exceeds threshold (e.g., >60/40 split) to distinguish informed positioning from isolated bursts

---

## 2026-04-06 — Advisor snapshot 99

### Summary
False positives cluster around volume spikes without sustained price conviction, especially in low-liquidity markets (sports betting, thin prediction markets). Raw volume delta is triggering signals that analysts classify as execution noise or mechanical rebalancing.

### Next step
Introduce a volume-to-price-momentum coupling rule: require minimum price move (0.02–0.03) to accompany volume spikes in low-liquidity venues, or use flow-imbalance ratio instead of raw volume delta as primary trigger.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-312** `planned` — For markets with baseline volume <2000, require ≥2% directional price move to accompany volume spikes >500 delta; otherwise classify as execution noise.
- [ ] **TB-313** `planned` — Segment by liquidity tier: apply stricter price-move floors (2–3%) for thin sports/prediction markets; relax volume delta baseline from 30 to 100+ for pre-game sports to reduce churn.
- [ ] **TB-314** `planned` — Replace or supplement spike_min_volume_delta with flow-imbalance metric (buy/sell-side dominance ratio) to distinguish informed positioning from mechanical rebalancing on low-conviction markets.

---

## 2026-04-06 — Advisor snapshot 100

### Summary
The detector is generating false positives by flagging large volume deltas without sufficient price confirmation, particularly in thin-liquidity and low-baseline-volume markets (sports betting, prediction markets). Volume spikes alone are execution noise when not accompanied by directional price movement.

### Next step
Implement a volume-to-price coupling filter: require minimum 2-3% directional price move to accompany volume spikes in markets with baseline volume <5000, and enforce multi-timeframe price confirmation for baseline volumes 5000-20000.

### Suggested thresholds
`min_price_move` → `0.02`, `score_threshold` → `500.0`

### Recommendations

- [ ] **TB-315** `planned` — For low-liquidity markets (baseline vol <5000): require spike_min_price_move ≥ 0.03 (3%) to accompany volume delta spikes, or demote score by 60-70% if price move is <1%
- [ ] **TB-316** `planned` — For sports/categorical markets with high score but low price delta (<1%): lower effective spike_score_threshold to ~500+ unless price_move ≥ 0.02, as these generate high scores from volume alone
- [ ] **TB-317** `planned` — Add market-type-specific volume_delta baselines: sports betting markets baseline 100+, thin prediction markets baseline 150+, and only flag if volΔ exceeds baseline by 3x+ AND price moves ≥2%

---

## 2026-04-06 — Advisor snapshot 101

### Summary
Volume spikes without sustained price conviction are dominating false positives, particularly in low-liquidity sports and thin prediction markets where execution noise mimics informed flow.

### Next step
Implement a volume-to-price momentum filter: require minimum 2-3% directional price move to accompany volume deltas >1000, and enforce multi-timeframe price confirmation for lower-volume spikes to distinguish sustained conviction from execution noise.

### Suggested thresholds
`min_volume_delta` → `150.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-318** `planned` — For markets with baseline volume <500 contracts, raise min_volume_delta to 100-150 and require ≥2% price move persistence across 1m/5m timeframes before flagging
- [ ] **TB-319** `planned` — For high-volume categorical events (vol_delta >2000), enforce minimum 2-3% directional price move or visible buy/sell-side dominance signal to accompany spike
- [ ] **TB-320** `planned` — De-weight pure volume signals in score calculation for thin-liquidity markets; prioritize price confirmation and trade-direction clustering over volume magnitude alone

---

## 2026-04-06 — Advisor snapshot 102

### Summary
Sports betting markets are generating false positives from volume spikes without sustained price momentum; thin-liquidity categorical events show high scores despite minimal directional movement, indicating the scoring model over-weights volume relative to price conviction.

### Next step
Introduce a volume-to-price momentum coupling requirement: only flag spikes when volume delta is accompanied by minimum 2-3% sustained price move, or require corroborating trade-side dominance in low-liquidity venues.

### Suggested thresholds
`min_volume_delta` → `150.0`, `min_price_move` → `0.025`

### Recommendations

- [ ] **TB-321** `planned` — Increase min_price_move floor to 0.025 (2.5%) for markets with volume < 5000 cumulative, or require price persistence across 2+ consecutive intervals
- [ ] **TB-322** `planned` — For sports categorical markets (KXNBAGAME), raise minimum volume_delta baseline from 30 to 150+ to filter execution noise in thin order books
- [ ] **TB-323** `planned` — Add a liquidity-adjusted score dampener: reduce spike_score by 40-50% when priceΔ < 0.02 AND market shows < 10k cumulative volume, flagging these as 'uncertain' rather than 'notable' or 'high conviction'

---

## 2026-04-06 — Advisor snapshot 103

### Summary
Sports markets (NBA, political) are generating false positives from volume spikes without sustained price movement. Low-liquidity markets trigger on single outlier trades; high-liquidity categorical events flag on volume alone despite minimal directional conviction.

### Next step
Implement a volume-to-price-move coupling requirement: require minimum 2-3% price move to accompany volume spikes >1000, and enforce minimum trade size thresholds for lower-liquidity markets to filter execution noise.

### Suggested thresholds
`min_volume_delta` → `150.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-324** `planned` — Add volume-to-price correlation filter: for volΔ > 1000, require priceΔ >= 0.02 (2%); for volΔ 500-1000, require priceΔ >= 0.015 (1.5%)
- [ ] **TB-325** `planned` — Raise spike_min_volume_delta to 100-150 for sports pre-game markets with <100 base volume to reduce single-contract outlier sensitivity
- [ ] **TB-326** `planned` — Require price move persistence check: flag only if price move sustains across 2+ consecutive timeframes (e.g., 1-min and 5-min) rather than single-interval spikes

---

## 2026-04-06 — Advisor snapshot 104

### Summary
Low-liquidity markets are generating false positives from volume spikes decoupled from meaningful price movement or from single large trades that don't reflect genuine sentiment shifts.

### Next step
Implement a volume-to-price coupling filter: require sustained price moves (2-3%+) to accompany volume spikes in thin markets, and enforce minimum trade-size thresholds relative to market liquidity tier.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.025`, `score_threshold` → `50.0`

### Recommendations

- [ ] **TB-327** `planned` — Add liquidity-tier detection: apply stricter price-move requirements (≥2-3%) for watch/low-volume markets when volume_delta is high but price_delta is <2%
- [ ] **TB-328** `planned` — For sports prediction markets specifically, raise spike_min_volume_delta baseline to 100-150 contracts to filter out natural pre-game volatility in thin liquidity pools
- [ ] **TB-329** `planned` — Require price-move persistence across 2+ consecutive timeframes (e.g., 5min candles) rather than single-interval spikes, especially when score is driven by volume alone

---

## 2026-04-06 — Advisor snapshot 105

### Summary
Low-liquidity markets are generating false positives: volume spikes without sustained price moves (execution noise) and single-contract outliers in thin markets are being flagged as signals despite lacking directional conviction.

### Next step
Introduce a volume-to-momentum filter requiring sustained price movement (≥2-3%) to accompany volume surges, with stricter thresholds in low-liquidity tiers.

### Suggested thresholds
`min_volume_delta` → `800.0`, `min_price_move` → `0.025`, `score_threshold` → `50.0`

### Recommendations

- [ ] **TB-330** `planned` — Require price moves to persist across multiple timeframes or enforce a minimum 2–3% price delta threshold for low-liquidity markets (tier=watch) before flagging volume spikes
- [ ] **TB-331** `planned` — Add a minimum trade count or contract-size filter to reject single outlier trades in thin markets; require multiple corroborating trades above a minimum notional threshold
- [ ] **TB-332** `planned` — Implement liquidity-aware score normalization: discount spike_score in low-volume markets unless volume delta is accompanied by sustained directional price movement

---

## 2026-04-06 — Advisor snapshot 106

### Summary
Low-absolute-price markets (<$0.20) and thin-baseline markets are generating false positives from mechanical small-lot activity and modest volume surges that don't reflect genuine conviction shifts.

### Next step
Implement market-structure-aware thresholds: require higher price-move thresholds for low-price markets and enforce minimum order-size or baseline-volume ratios for thin markets, rather than relying on uniform volume and price deltas.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-333** `planned` — For markets with yes-price <$0.20: require spike_min_price_move ≥ 0.05 (5%) OR enforce minimum order-size threshold (e.g., >500 contracts per leg) to filter mechanical activity
- [ ] **TB-334** `planned` — For markets with baseline volume <100 contracts: require either spike_min_price_move >0.05 alongside high volume spike, OR cross-reference with external news/event catalysts before emitting signal
- [ ] **TB-335** `planned` — Adjust spike_score_threshold dynamically based on market liquidity: lower thresholds for deep markets (baseline >1000 contracts), higher thresholds for thin markets (baseline <100 contracts)

---

## 2026-04-06 — Advisor snapshot 107

### Summary
Sports betting markets are generating high-volume false positives due to natural liquidity swings with minimal price impact, especially in low-absolute-price tiers where mechanical activity dominates conviction signals.

### Next step
Enforce a minimum price-move threshold (2-3% for standard markets, >3% for sub-$0.20 markets) as a hard gate before emitting notable-tier signals, regardless of volume delta or composite score.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-336** `planned` — Require min_price_move >= 0.03 (3%) for markets priced under $0.20 before flagging notable tier, to filter mechanical small-lot noise
- [ ] **TB-337** `planned` — For sports betting category specifically, raise min_price_move to 0.02-0.03 (2-3%) or reduce spike_min_volume_delta by 30-40% to avoid volume-only triggers on liquid markets
- [ ] **TB-338** `planned` — For thin-baseline markets (<50 contracts typical volume), require either price_move >= 0.05 (5%) OR add event/news catalyst cross-reference before emitting signal

---

## 2026-04-06 — Advisor snapshot 108

### Summary
The detector is generating false positives by flagging volume spikes without sufficient price conviction, particularly in illiquid and low-volatility markets where volume changes alone do not indicate genuine demand shifts.

### Next step
Implement market-segment-specific thresholds: require minimum price moves of 2-3% for liquid sports markets, >1% for low-baseline illiquid markets, and >5% for thin baseline markets; additionally enforce a minimum order size or require price-move confirmation before escalating to 'notable' tier.

### Suggested thresholds
`min_volume_delta` → `2000.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-339** `planned` — For markets with baseline volume <100 contracts, raise spike_min_volume_delta or require spike_min_price_move >1% to filter mechanical activity
- [ ] **TB-340** `planned` — For sports betting markets (high liquidity), enforce spike_min_price_move ≥2-3% regardless of volume delta to avoid flagging noise from typical order flow
- [ ] **TB-341** `planned` — For markets with prices <$0.20 or thin baselines (~30 contracts), require spike_min_price_move >5% or cross-reference with external event catalysts before emitting 'notable' signals

---

## 2026-04-06 — Advisor snapshot 109

### Summary
The detector is generating excessive false positives in low-liquidity and sports betting markets, where volume spikes decouple from meaningful price conviction. Most labeled noise cases show high volume deltas with minimal price moves (0–2%), indicating the volume signal alone is insufficient.

### Next step
Enforce a minimum price-move requirement paired with market-liquidity-aware volume thresholds. For low-liquidity markets (<100 baseline contracts), require price moves ≥2–3% before triggering alerts; for sports markets with higher baseline volume, require ≥2% price moves. This decouples mechanical volume activity from genuine conviction shifts.

### Suggested thresholds
`min_volume_delta` → `1.4`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-342** `planned` — Introduce a tiered minimum price-move rule: require ≥2% for watch-tier alerts and ≥3% for notable-tier alerts in markets with baseline volume under 500 contracts.
- [ ] **TB-343** `planned` — Increase spike_min_volume_delta multiplier from 1.1x to 1.3x–1.5x for low-liquidity sports markets, or enforce multi-trade confirmation within 30 seconds to filter single-trade artifacts.
- [ ] **TB-344** `planned` — For markets with absolute price levels under $0.20 or baseline volume under 100 contracts, require either price moves >3–5% or attach an external catalyst (news/event) signal before emitting notable-tier alerts.

---

## 2026-04-06 — Advisor snapshot 110

### Summary
The detector is generating false positives across illiquid and low-volatility markets by triggering on volume spikes that lack price conviction. High-volume activity without meaningful price movement (or minimal price moves on ultra-low absolute volumes) is being flagged as notable/watch tier despite analyst labels of noise.

### Next step
Enforce a minimum price-move threshold that scales inversely with baseline liquidity: require >2-3% price delta for low-volume markets (<200 contracts baseline), >1% for mid-liquidity, and >0.5% for high-liquidity markets. Reject pure volume spikes without price confirmation.

### Suggested thresholds
`min_volume_delta` → `1.35`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-345** `planned` — Add a market-context filter: for markets with baseline volume <100 contracts, require minimum price move of 2-3% OR cross-reference with external news/social signals before emitting notable tier.
- [ ] **TB-346** `planned` — For sports betting markets and low-absolute-price instruments (<$0.20), raise volume multiplier threshold from 1.1x to 1.3-1.4x and require minimum order size to filter mechanical small-lot activity.
- [ ] **TB-347** `planned` — Implement dual-gate logic: reject signals where (volΔ > 1500 AND priceΔ < 0.01) or (volΔ > 5000 AND priceΔ < 0.02) unless there is same-minute correlated news or multi-trade confirmation within 30 seconds.

---

## 2026-04-06 — Advisor snapshot 111

### Summary
Low-liquidity markets are generating false positives through mechanical volume/price spikes decoupled from genuine conviction. Pure volume surges without price movement and outsized percentage moves on minimal absolute volumes dominate the noise.

### Next step
Implement liquidity-aware thresholds: require minimum absolute volume (50+ shares/contracts) OR correlated external signal (social/news) for sub-100 baseline volume markets, and mandate price movement >1% alongside volume spikes in low-volatility regimes.

### Suggested thresholds
`min_volume_delta` → `1.3`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-348** `planned` — For markets with baseline volume <100 contracts: require either absolute volume delta >50 units OR price move >0.01 (1%) to trigger, not just multiplier-based detection
- [ ] **TB-349** `planned` — Raise volume multiplier threshold from 1.1x to 1.3x+ for sports/low-liquidity markets to filter single-trade artifacts
- [ ] **TB-350** `planned` — For markets with <0.05 baseline volatility: suppress pure volume spike signals (high volΔ, priceΔ ≈ 0) unless accompanied by external data (news mentions, social volume, order-book imbalance)

---

## 2026-04-06 — Advisor snapshot 112

### Summary
False positives cluster in low-liquidity markets where volume spikes occur without meaningful price conviction or in minor-league sports where thin baselines amplify mechanical artifacts. Four recent signals marked as noise/uncertain had scores ranging from 3.3 to 82.6, driven by volume alone rather than price-opinion alignment.

### Next step
Implement a liquidity-aware gating rule: require minimum price move of 2–5% (tiered by baseline volume) AND absolute volume confirmation (>50 shares or >1.3x baseline multiplier) before emitting signals on markets under 100-contract baseline volume.

### Suggested thresholds
`min_volume_delta` → `50.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-351** `planned` — For minor-league sports markets (baseline volume <1000): enforce spike_min_price_move ≥ 0.03 (3%) alongside volume delta, and require volume multiplier ≥1.3x to filter single-trade artifacts.
- [ ] **TB-352** `planned` — For ultra-low-volume markets (baseline <100 contracts): gate on absolute volume >50 shares OR external signal correlation (social/news mention), and suppress pure-volume-spike alerts without ≥1% price move.
- [ ] **TB-353** `planned` — For low-volatility markets with volume spikes: require either price move >1% OR multi-trade confirmation within 30 seconds to distinguish conviction from liquidity provision.

---

## 2026-04-06 — Advisor snapshot 113

### Summary
False positives cluster in low-liquidity markets where volume spikes decouple from price conviction, and in micro-markets approaching expiry where quote exploration creates mechanical price moves without sustained follow-through.

### Next step
Implement liquidity-aware thresholds: require minimum price movement (1-3% depending on baseline volume) alongside volume delta, and add a sustained-conviction filter (5-min hold or multi-trade confirmation) for markets with <500 baseline contract volume.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-354** `planned` — For markets with baseline volume <500 contracts, raise min_price_move to 0.03 (3%) and require either sustained price hold >5 min OR order-book imbalance >3:1 to reduce quote-exploration artifacts
- [ ] **TB-355** `planned` — For sports markets (thin baselines), implement dynamic min_price_move floor of 0.03–0.05 depending on typical spread, and require volume multiplier ≥1.3x (not 1.1x) to filter bulk liquidity events
- [ ] **TB-356** `planned` — For binary expiry markets <7 days to close, add constraint: require absolute volume delta >100 contracts OR correlated external signal (social/news mention) to prevent micro-spike false positives
- [ ] **TB-357** `planned` — Exclude pure-volume spikes (priceΔ=0.0) from scoring in low-volatility markets; require min_price_move ≥0.01 (1%) as baseline gate before any alert triggers

---

## 2026-04-06 — Advisor snapshot 114

### Summary
False positives cluster in thin-liquidity markets (sports, micro-cap political) where small absolute volumes or single large quotes mechanically spike prices without reflecting genuine conviction or follow-through.

### Next step
Implement liquidity-aware thresholds: require higher price-move floors (3–5%) for low-baseline-volume markets, and add confirmation rules (sustained hold, multi-side participation, or absolute volume floors) before emitting signals.

### Suggested thresholds
`min_volume_delta` → `50.0`, `min_price_move` → `0.05`, `score_threshold` → `8.0`

### Recommendations

- [ ] **TB-358** `planned` — For markets with baseline volume <500 shares, require either absolute volume delta >50 OR multi-trade confirmation within 30 seconds to filter single-quote artifacts.
- [ ] **TB-359** `planned` — For sports betting and expiring binary markets, require sustained price hold >5 minutes OR order imbalance >3:1 to confirm conviction beyond quote exploration.
- [ ] **TB-360** `planned` — Raise minimum price-move threshold to 3–5% for thin-liquidity markets (identified by rolling 7-day avg volume <1000), separate from standard 3% floor.

---

## 2026-04-06 — Advisor snapshot 115

### Summary
Current detector is generating false positives across thin/low-volume markets by triggering on quote exploration, bulk liquidity events, and mechanical percentage spikes without confirming sustained conviction or actual opinion shift.

### Next step
Implement a tiered threshold system based on baseline market volume: require higher price-move thresholds (3-5%) for thin markets AND add persistence/corroboration requirements (sustained hold, order imbalance ratio, or external signal) before emitting signals.

### Suggested thresholds
`min_volume_delta` → `50.0`, `min_price_move` → `0.05`, `score_threshold` → `15.0`

### Recommendations

- [ ] **TB-361** `planned` — For markets with baseline volume <500 shares/day: require min_price_move ≥ 0.05 (5%) AND either sustained price hold >5 min OR order imbalance >3:1 buy/sell ratio
- [ ] **TB-362** `planned` — For all markets: add minimum absolute volume gate of 50+ shares traded in the spike window to filter out mechanical edge cases in ultra-thin markets
- [ ] **TB-363** `planned` — For markets within 1 week of expiry: require either multi-sided participation (buy AND sell order imbalance, not just quote exploration) OR correlated social/news mention before emitting

---

## 2026-04-06 — Advisor snapshot 116

### Summary
Low-liquidity and micro-markets are generating false positives through mechanical volume/price spikes without follow-through or actual conviction. Most flagged signals have weak yes-probability (0.38–0.61) and analyst consensus is noise/unclear.

### Next step
Implement liquidity-aware tiering: require minimum absolute volume thresholds (500–1000 contracts depending on market tier) AND simultaneous multi-sided participation (bid-ask spread tightening or sustained >5min holds) before escalating alerts on low-baseline markets.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-364** `planned` — Raise spike_min_volume_delta for 'watch' tier to 1.5x baseline and require minimum 1000 absolute contracts; for 'notable' tier require minimum 500 contracts to filter micro-moves.
- [ ] **TB-365** `planned` — Enforce minimum price_move thresholds by liquidity tier: 3–5% for minor sports, 5%+ for ultra-low-volume (<100 baseline contracts), 2%+ for standard markets.
- [ ] **TB-366** `planned` — Add confirmation gate: require either (a) sustained price hold >5 minutes, (b) order imbalance >3:1 ratio, or (c) correlated social/news signal before emitting signal on markets <1 week to expiry or <100 baseline contracts.

---

## 2026-04-06 — Advisor snapshot 117

### Summary
Low-liquidity and micro-move markets are generating false positives across watch and notable tiers. Volume spikes without sustained price conviction or multi-side participation are triggering alerts on thin baskets and near-expiry contracts.

### Next step
Implement a tiered minimum price-move requirement (3-5% for thin markets, 2% baseline for liquid) combined with volume delta multipliers (1.5x+ for watch tier, 2.0x+ for notable on sub-1000 contract baselines) to filter quote exploration from genuine conviction moves.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-367** `planned` — Raise spike_min_volume_delta for 'watch' tier from 1.1x to 1.5x baseline; add absolute volume floor of 1000+ contracts before any watch-tier signal
- [ ] **TB-368** `planned` — For 'notable' tier on markets with <2000 baseline contracts: require either (a) price move ≥3%, or (b) order imbalance ratio >2.5:1 with 5+ min sustained hold, to filter bulk liquidity from opinion shifts
- [ ] **TB-369** `planned` — For markets within 7 days of expiry: require price hold >5 minutes AND volume delta ≥2.0x baseline before emitting notable-tier signals, to suppress quote-exploration noise

---

## 2026-04-06 — Advisor snapshot 118

### Summary
Low-liquidity markets and micro-moves near expiry are generating false positives despite moderate scores. Volume deltas are triggering on thin order books without sustained follow-through or multi-side confirmation.

### Next step
Implement tiered thresholds by market liquidity/volume and require sustained price hold or order imbalance confirmation for micro-moves, especially within 1 week of expiry.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`, `score_threshold` → `7.5`

### Recommendations

- [ ] **TB-370** `planned` — Raise spike_min_volume_delta for 'watch' tier from 1.1x to 1.5x baseline, or enforce minimum absolute volume floor (1000+ contracts) before flagging on low-liquidity markets
- [ ] **TB-371** `planned` — For notable/watch tier signals with priceΔ < 0.05 and volΔ < 2000, require either (a) sustained price hold >5 minutes, or (b) order imbalance >3:1 ratio, or (c) multi-side participation (both bid/ask volume increases)
- [ ] **TB-372** `planned` — Apply stricter score thresholds for markets within 7 days of expiry: require score ≥ 7.5 for notable tier (vs current ~4.0), or exclude expiring contracts from watch tier entirely

---

## 2026-04-06 — Advisor snapshot 119

### Summary
Low-liquidity markets are generating false positives from micro-moves and single-sided large quotes without sustained follow-through. Volume delta alone is insufficient to filter noise in thin markets.

### Next step
Implement absolute volume floor (e.g., 1000+ contracts) and multi-side participation requirement for 'watch' and 'notable' tier alerts before raising fractional thresholds.

### Suggested thresholds
`min_volume_delta` → `1.5`

### Recommendations

- [ ] **TB-373** `planned` — Add minimum absolute volume gate: require volΔ > 1000 contracts in absolute terms, not just relative delta, to trigger detection on low-liquidity markets
- [ ] **TB-374** `planned` — Require multi-side participation: flag only when both bid and ask show elevated activity, or require minimum sustained trade count (e.g., 3+ consecutive trades) to reduce single large quote noise
- [ ] **TB-375** `planned` — Raise volume delta threshold for 'watch' tier from 1.1x to 1.5x baseline, or tier-dependent: 1.5x for watch, 1.2x for notable on markets with ADV < 5000 contracts

---

## 2026-04-07 — Advisor snapshot 120

### Summary
Low-liquidity sports and political markets are generating false positives from single-print trades and quick mean-reversions that lack sustained conviction. Volume deltas alone are insufficient filters when average market volume is <1,500 contracts.

### Next step
Introduce a market-liquidity-aware persistence requirement: for markets with sub-1,500 average volume, require either (a) sustained volume over 5+ minutes, (b) multiple consecutive trades in same direction, or (c) notional trade size >threshold (e.g., 50+ contracts). This decouples low-liquidity noise from genuine flow.

### Suggested thresholds
`min_volume_delta` → `1500.0`

### Recommendations

- [ ] **TB-376** `planned` — Require minimum trade count ≥2 or minimum notional size ≥50 contracts for watch-tier signals in sub-1,500 avg-volume markets to filter single-print noise.
- [ ] **TB-377** `planned` — Add 5-minute sustained-volume check for high-score signals (score >8) in low-liquidity markets before emitting high-conviction alerts; flag if volume reverts within 3 minutes.
- [ ] **TB-378** `planned` — Raise spike_min_volume_delta by 30–50% for markets with avg volume <1,500; consider dynamic threshold based on market's rolling 20-day median volume.

---

## 2026-04-07 — Advisor snapshot 121

### Summary
The detector is generating false positives in low-liquidity markets by triggering on single small trades or quote updates without sustained volume or price persistence, particularly in sports betting and niche prediction markets.

### Next step
Implement a market-context-aware minimum notional trade size requirement (e.g., 50+ contracts or $500+ notional) combined with a persistence check (price must hold for 2+ minutes or be confirmed by follow-up volume) to filter single-print noise.

### Suggested thresholds
`min_volume_delta` → `1500.0`, `min_price_move` → `0.04`, `score_threshold` → `4.5`

### Recommendations

- [ ] **TB-379** `planned` — Require minimum trade size of 50+ contracts or $500+ notional value per fill to trigger watch/high-conviction tiers, filtering out single small trades against stale quotes in low-liquidity markets.
- [ ] **TB-380** `planned` — Add a price persistence rule: flagged price moves must hold for ≥2 minutes or be immediately confirmed by follow-up volume (next tick within 5 minutes at similar or more extreme price) to exclude quick mean-reversions.
- [ ] **TB-381** `planned` — For markets with average volume <1,500 contracts/period, enforce a 3x+ volume multiplier above baseline or require 5+ consecutive trades in the detection window to reduce quote-update-only false positives.
- [ ] **TB-382** `planned` — Exclude signals based purely on quote updates without executed fills; require non-zero recent trade count or clear asymmetric buy/sell activity to qualify for any tier.

---

## 2026-04-07 — Advisor snapshot 122

### Summary
The detector is triggering watch-tier signals on low-liquidity sports markets driven by quote updates without fills, single-print noise, and quick mean-reversions. These are structurally different from actionable flow signals.

### Next step
Implement market-microstructure filters before scoring: require either (1) executed trade count ≥1 in trailing period, OR (2) sustained multi-tick price persistence (>2–3 min), OR (3) volume multiplier ≥3x baseline for low-volume venues (<1500 baseline). This layers a reality check on top of threshold tuning.

### Suggested thresholds
`min_volume_delta` → `2000.0`, `min_price_move` → `0.03`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-383** `planned` — Add executed_trade_count ≥1 gating: reject signals from pure quote-update sequences (zero fills) even if volume delta is high, as these are not actionable market participant intent.
- [ ] **TB-384** `planned` — For markets with avg_volume <1500, require either price_persistence_minutes ≥3 OR volume_multiplier ≥3.0x baseline; single-print spikes that mean-revert in <2 min are noise.
- [ ] **TB-385** `planned` — Raise min_trade_size to 50+ contracts (or equivalent notional) in lower-liquidity sports markets; single small trades against stale quotes are a primary false-positive source.
- [ ] **TB-386** `planned` — Require sustained multi-tick confirmation: score should NOT spike on isolated prints; accumulate score only when ≥2 consecutive trades move price in same direction within 30–60 seconds.

---

## 2026-04-07 — Advisor snapshot 123

### Summary
The detector is triggering on low-liquidity sports markets with quote-only activity and single-print noise rather than genuine informed flow. All three recent false positives lack sustained execution or asymmetric fill patterns.

### Next step
Add a market-liquidity-aware gating rule: require either (1) minimum executed trade count in trailing window (e.g., ≥2 fills) OR (2) volume delta must exceed 3x the market's baseline average volume. This filters quote-only noise while preserving real flow in low-liquidity venues.

### Suggested thresholds
`min_volume_delta` → `1500.0`, `min_price_move` → `0.04`, `score_threshold` → `4.0`

### Recommendations

- [ ] **TB-387** `planned` — Require non-zero recent executed trade count (≥2 trades in last 5 min) before emitting 'watch' tier signal, to exclude pure quote updates
- [ ] **TB-388** `planned` — For markets with avg volume <1500 contracts, enforce volume_delta ≥ 3x baseline OR require price persistence (bid-ask midpoint stability) across ≥3 consecutive 1-min candles
- [ ] **TB-389** `planned` — Raise minimum trade size threshold to 50+ contracts in sports markets, or require asymmetric buy/sell ratio (e.g., >70% one-sided) to distinguish informed flow from retail noise

---

## 2026-04-07 — Advisor snapshot 124

### Summary
False positives are clustering in low-liquidity sports markets where quote updates without executed fills and single-print trades are triggering watch-tier signals despite minimal actionable flow.

### Next step
Require evidence of executed volume (non-zero trade count) and/or sustained price persistence across multiple ticks before emitting watch-tier signals, especially in markets with low baseline liquidity.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.04`, `score_threshold` → `3.0`

### Recommendations

- [ ] **TB-390** `planned` — Add a minimum executed trade count requirement (e.g., ≥2 trades in trailing window) before triggering watch tier, filtering pure quote noise
- [ ] **TB-391** `planned` — Implement a minimum trade size floor of 50+ contracts for sports markets, or require price to persist across 2+ consecutive ticks to confirm genuine flow intent
- [ ] **TB-392** `planned` — Raise spike_min_price_move to 0.04 (4%) for low-liquidity venues, or lower spike_min_volume_delta only when paired with executed trade confirmation

---

## 2026-04-07 — Advisor snapshot 125

### Summary
Low-liquidity minor league sports markets are generating false positives on modest volume moves (2748–6998 contracts) with minimal price action (2% moves), scoring just above threshold despite unclear directional intent.

### Next step
Implement liquidity-aware thresholds: require higher volume delta multipliers and minimum trade counts for low-absolute-volume markets, rather than applying uniform thresholds across all venues.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-393** `planned` — For markets with baseline volume <5000 contracts/period, enforce spike_min_volume_delta ≥ 1.5x (vs. 1.0x baseline) and require ≥10 recent trades to validate spike
- [ ] **TB-394** `planned` — Require minimum notional value threshold (e.g. $500–1000) or multi-directional flow confirmation (buy+sell imbalance ≤70/30) before flagging single-sided activity in low-liquidity tiers
- [ ] **TB-395** `planned` — Raise spike_min_price_move from 0.02 (2%) to 0.03 (3%) or higher for 'watch' tier alerts in low-liquidity markets to filter out noise-range movements

---

## 2026-04-07 — Advisor snapshot 126

### Summary
Low-liquidity markets are generating false positives with large volume deltas but minimal price moves and low trade counts. The detector is triggering on quote-driven activity and single-sided flows rather than genuine demand shifts.

### Next step
Implement a trade-count and trade-to-quote ratio filter before escalating watch-tier alerts, particularly for markets with priceΔ < 0.03 and volΔ > 2000.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-396** `planned` — Require minimum 10+ recent trades (not quotes) to trigger watch tier; apply stricter 15+ threshold for score > 2.5 in low-probability (yes < 0.15) markets
- [ ] **TB-397** `planned` — Add trade-to-quote ratio gate (minimum 0.3) and reject spikes where recent trade direction contradicts price movement direction
- [ ] **TB-398** `planned` — Raise minimum volume delta for minor/illiquid markets from 1.0x to 1.5x baseline, and require multi-directional flow confirmation rather than single-sided activity

---

## 2026-04-07 — Advisor snapshot 127

### Summary
Low-liquidity and niche markets (minor league sports, prediction markets with small trade sizes) are generating false positives through quote-refresh noise and single-sided volume spikes that don't reflect genuine demand-driven moves.

### Next step
Implement market-segment filtering: require minimum trade count (3+), minimum trade size (>100 shares), and trade-to-quote ratio (>0.3) before escalating watch-tier alerts in illiquid markets (volume_delta < 5000 or price_delta < 0.03).

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-399** `planned` — For markets with volume_delta > 5000 but price_delta ≤ 0.02, require minimum trade count ≥ 3 and trade-to-quote ratio ≥ 0.3 to filter quote-driven noise
- [ ] **TB-400** `planned` — Add liquidity-aware floor: markets with baseline volume < 1000 require minimum recent trade size >100 shares or notional value confirmation before triggering watch tier
- [ ] **TB-401** `planned` — Cross-check trade flow direction against price movement direction; mute signals where flow and price diverge, as this indicates quote-driven rather than demand-driven activity

---

## 2026-04-07 — Advisor snapshot 128

### Summary
Low-liquidity niche markets (minor league sports, prediction markets) are generating false positives through quote-refresh noise and quote-driven price moves rather than genuine demand-driven flow.

### Next step
Implement market-tier-aware filtering: require actual trade count and trade-to-quote ratio validation before escalation, especially for watch-tier alerts in illiquid venues.

### Suggested thresholds
`min_volume_delta` → `1.5`

### Recommendations

- [ ] **TB-402** `planned` — Add minimum actual trade count requirement (3+ fills) for niche sports markets before triggering detection, rather than relying on volume delta alone
- [ ] **TB-403** `planned` — Filter spikes where recent trade flow direction contradicts price movement direction, indicating quote-driven rather than demand-driven moves
- [ ] **TB-404** `planned` — Require minimum trade size threshold (>100 shares) or trade-to-quote ratio (>0.3) before escalating watch-tier alerts to signal in illiquid markets
- [ ] **TB-405** `planned` — Increase volume delta baseline multiplier for minor league/low-volume markets from 1.0x to 1.5x, with minimum 10 contracts of recent activity to trigger watch tier

---

## 2026-04-07 — Advisor snapshot 129

### Summary
System is triggering false positives on low-liquidity and niche markets (sports betting, prediction markets) where quote volume and small isolated trades create signal noise without genuine demand-driven price movement.

### Next step
Implement a trade-quality filter requiring minimum actual fill count (3+ trades) and trade-to-quote ratio (>0.3) before escalating alerts, especially in low-liquidity venues. This targets the root cause: quote refresh noise and isolated small orders that don't reflect sustained market conviction.

### Suggested thresholds
`min_volume_delta` → `1.5`, `score_threshold` → `3.0`

### Recommendations

- [ ] **TB-406** `planned` — Add minimum actual trade count requirement of 3+ fills (not quote volume) before triggering 'watch' tier, particularly for niche/illiquid markets
- [ ] **TB-407** `planned` — Require trade-to-quote ratio >0.3 and filter out spikes where recent trade flow direction contradicts price movement direction to eliminate quote-driven false signals
- [ ] **TB-408** `planned` — Implement minimum trade size threshold (e.g., >100 shares/contracts) or require sustained follow-through trades within 2-3 minutes of initial spike to confirm genuine demand

---

## 2026-04-07 — Advisor snapshot 130

### Summary
Low-liquidity markets are generating false positives due to amplified noise from minimal baseline volumes and trade counts. Small absolute volume deltas and price moves trigger high scores when baselines are tiny, despite lacking statistical significance.

### Next step
Implement a liquidity gate: require minimum baseline volume (10-20 contracts per period) or minimum trade count (≥10 trades) before applying spike detection thresholds. This filters out inherently noisy low-liquidity regimes.

### Suggested thresholds
`score_threshold` → `750.0`

### Recommendations

- [ ] **TB-409** `planned` — Add baseline volume gate: only flag spikes in markets with ≥10-20 contracts per period baseline; skip detection entirely in thinner books
- [ ] **TB-410** `planned` — Add minimum trade count requirement: reject spike signals from <10 individual trades in the detection window to ensure statistical relevance
- [ ] **TB-411** `planned` — Raise spike_score_threshold to 750+ to suppress marginal signals in low-liquidity contexts where score=668 reflects noise not conviction

---

## 2026-04-07 — Advisor snapshot 131

### Summary
Low-liquidity markets are generating false positives from mechanical market-making and micro-trades with inflated score metrics due to tiny baselines. The detector needs liquidity-aware filtering rather than uniform thresholds.

### Next step
Introduce a minimum baseline volume threshold (10-20 contracts per period) and require trade-count or notional-value minimums before spike detection activates in low-liquidity venues, rather than relying on volume-delta ratios alone.

### Suggested thresholds
`min_volume_delta` → `5000.0`

### Recommendations

- [ ] **TB-412** `planned` — Add a minimum baseline volume gate: only flag spikes in markets with ≥10 contracts per reference period to avoid amplification of noise in thin markets
- [ ] **TB-413** `planned` — Require minimum trade count per spike (5+ trades) or notional value threshold to distinguish genuine flow from single large mechanical fills
- [ ] **TB-414** `planned` — Raise volume-delta multiplier for low-liquidity tiers from 2x to 3x baseline, or apply conditional logic: if baseline < 10 contracts, require volΔ > 5000 absolute or >4x multiplier

---

## 2026-04-07 — Advisor snapshot 132

### Summary
Low-liquidity markets (sports betting, thin prediction markets) are generating false positives due to tiny baselines that amplify noise and mechanical market-making moves. Volume and price deltas appear noisy when baseline contract counts are <10 and notional values are minimal.

### Next step
Implement a market-liquidity awareness layer: require minimum baseline volume thresholds (10-20 contracts/period) before spike detection activates, and scale delta multipliers (3x baseline instead of 2x) for low-liquidity venues.

### Suggested thresholds
`min_volume_delta` → `3.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-415** `planned` — Raise minimum baseline volume requirement from current implicit level to 10-20 contracts per period; suppress spike detection entirely in markets below this threshold.
- [ ] **TB-416** `planned` — Increase volume delta multiplier for low-liquidity markets from 2x to 3x baseline, with concurrent price-move floor of ≥0.5% for watch-tier qualification.
- [ ] **TB-417** `planned` — Add minimum trade-count filter: require ≥5 distinct trades per spike window in low-liquidity venues to exclude single large orders from triggering signals.
- [ ] **TB-418** `planned` — Discount single-trade price-impact moves by requiring quote-fill ratios or trade-size thresholds relative to rolling baseline, especially in thin markets.

---

## 2026-04-07 — Advisor snapshot 133

### Summary
Low-liquidity markets (sports, prediction) are generating false positives from micro-moves and quote-driven activity. High score inflation occurs when tiny baseline volumes amplify noise, and single-trade mechanics trigger detection despite lack of directional significance.

### Next step
Implement a liquidity-gating rule: require minimum baseline volume (10–20 contracts/period) and minimum trade count (5+ trades) before spike detection is eligible, with separate thresholds for low vs. standard liquidity tiers.

### Suggested thresholds
`min_volume_delta` → `1500.0`, `min_price_move` → `0.05`, `score_threshold` → `50.0`

### Recommendations

- [ ] **TB-419** `planned` — Require trade volume to be ≥20% of associated quote volume to filter quote-driven moves in thin markets
- [ ] **TB-420** `planned` — For low-liquidity markets, raise volume delta multiplier from 1.0x to 1.5–3.0x baseline and enforce minimum 5-contract trade size threshold
- [ ] **TB-421** `planned` — Introduce minimum baseline volume floor (10–20 contracts per detection period) to prevent score inflation from tiny denominators
- [ ] **TB-422** `planned` — Add minimum trade count filter (≥5 trades per spike window) to exclude statistical noise from single-trade or micro-volume bursts
- [ ] **TB-423** `planned` — Discount single-trade price-impact moves by requiring concurrent minimum quote-fill ratio or notional value thresholds relative to recent baseline

---

## 2026-04-07 — Advisor snapshot 134

### Summary
False positives cluster in low-liquidity markets where tiny baseline volumes and mechanical market-making create outsized score inflation from micro-moves. The detector lacks market-structure awareness and trades mechanical volume/price ratios for signal quality.

### Next step
Implement a baseline volume floor (10-20 contracts minimum per period) before calculating spike multipliers, preventing baseline amplification in thin markets. This single change addresses the root cause across all five signals.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-424** `planned` — Require minimum baseline volume threshold of 15 contracts per period before any spike detection is triggered; markets below this floor should be marked low-confidence or skipped entirely.
- [ ] **TB-425** `planned` — Add a trade-size normalization rule: flag only when individual trade size exceeds 5+ contracts AND volume delta is 3x+ baseline (not 2x), reducing sensitivity to single-contract moves in micro-liquidity venues.
- [ ] **TB-426** `planned` — Introduce quote-fill ratio filter: require trade volume to be ≥20% of associated quote volume to distinguish genuine flow from quote-driven mechanical moves in thin markets.
- [ ] **TB-427** `planned` — Discount single-trade price impact in low-liquidity regimes: require concurrent price movement >0.5% OR multiple trades within the detection window to qualify for watch/notable tier on markets with <50 contract baseline volume.

---

## 2026-04-07 — Advisor snapshot 135

### Summary
Low-liquidity markets (sports, prediction) are generating false positives due to quote-driven noise and mechanical market-making activity dominating small baselines. High score outputs from tiny volume deltas are masking low analyst confidence (yes≤0.62).

### Next step
Implement a trade-volume-to-quote-volume ratio filter (minimum 20% trade fill ratio) and enforce minimum baseline volume thresholds (10-20 contracts per period) before spike detection is eligible, especially for watch/notable tiers.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `12.0`

### Recommendations

- [ ] **TB-428** `planned` — Add mandatory trade volume filter: flag only when executed trade volume ≥20% of quote volume delta to reject quote-only noise
- [ ] **TB-429** `planned` — Enforce minimum baseline volume requirement: do not trigger spike detection if baseline period volume <10 contracts; increase to 20 contracts for sports/thin markets
- [ ] **TB-430** `planned` — Raise volume delta multiplier for low-liquidity tiers: require volΔ >3x baseline (not 2x) and minimum single-trade size ≥5 contracts for watch tier on sports markets
- [ ] **TB-431** `planned` — Implement concurrent price-move gate: require priceΔ >0.05 (5%) alongside volume spike for watch tier, or >0.03 (3%) for notable tier in low-liquidity venues
- [ ] **TB-432** `planned` — Discount single-trade mechanical moves: apply dampening factor to score when trade count in spike window ≤2 to filter out isolated market-maker fills

---

## 2026-04-07 — Advisor snapshot 136

### Summary
The detector is generating false positives primarily in low-liquidity markets (sports betting, thin political/entertainment markets) where quote-driven noise and small mechanical trades trigger signals despite low analyst confidence (yes≤0.62). Volume deltas are high in absolute terms but not validated by executed trade volume or meaningful price moves.

### Next step
Implement a trade-volume-to-quote-volume ratio filter (minimum 20% trade fill ratio) as a gating condition before emitting watch/notable tier signals, especially for markets with baseline volume <5000 contracts.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-433** `planned` — Require minimum executed trade volume of 10+ contracts (not just quote volume delta) to qualify for any tier signal, with stricter thresholds (20+ contracts) for notable tier
- [ ] **TB-434** `planned` — Add a trade-fill-ratio gate: reject signals where trade volume < 20% of associated quote volume delta; this filters mechanical market-making and one-sided quote stacks
- [ ] **TB-435** `planned` — For low-liquidity markets (rolling 7d volume <10k contracts), enforce concurrent minimum price move of 0.5% OR volume delta multiplier >3.0x baseline (not 1.5x or 2.0x) to reduce ambiguous micro-moves

---

## 2026-04-07 — Advisor snapshot 137

### Summary
Low-liquidity markets are generating false positives from quote-driven noise and mechanical market-making activity, even when actual trade volume is minimal relative to quote volume.

### Next step
Implement a trade-volume-to-quote-volume ratio filter requiring executed trades to represent at least 20% of associated quote volume before spike qualification, combined with minimum executed trade count (10+ contracts) for watch-tier signals.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-436** `planned` — Add executed trade volume floor of 10+ contracts minimum to qualify any signal, especially in sports and thin political markets
- [ ] **TB-437** `planned` — Require trade volume ≥ 20% of quote volume delta to filter quote-driven noise in low-liquidity venues
- [ ] **TB-438** `planned` — For watch tier on sports markets, increase volume delta multiplier from 1.0x to 1.5x baseline OR require concurrent price move >0.5% to avoid single-trade mechanical moves

---

## 2026-04-07 — Advisor snapshot 138

### Summary
Low-liquidity markets (sports betting) are generating false positives from quote-driven volume spikes that lack meaningful price movement or executed trade volume.

### Next step
Implement a trade-volume-to-quote-volume ratio filter requiring at least 20% of quote volume to be executed trades before emitting signals in thin markets.

### Suggested thresholds
`min_volume_delta` → `2000.0`, `min_price_move` → `0.03`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-439** `planned` — Add mandatory trade volume floor: require minimum 10+ executed contracts alongside quote volume delta for watch tier and above
- [ ] **TB-440** `planned` — Enforce trade-to-quote ratio: reject signals where executed trade volume is <20% of associated quote volume delta
- [ ] **TB-441** `planned` — Increase price-move requirement for low-liquidity tiers: require priceΔ >0.5% (0.005) concurrently with high volume delta on sports/low-liquidity markets, or apply 1.5x multiplier to baseline volume delta threshold

---

## 2026-04-07 — Advisor snapshot 139

### Summary
Both false positives stem from quote-driven noise in thin/low-liquidity markets where large quote volume deltas drive spike scores without corresponding executed trade volume, creating illusion of real flow.

### Next step
Implement executed trade volume validation: require minimum executed contracts AND enforce trade-volume-to-quote-volume ratio floor to distinguish genuine flow from quote layering/spoofing in thin markets.

### Suggested thresholds
`score_threshold` → `5.0`

### Recommendations

- [ ] **TB-442** `planned` — Add minimum executed trade volume gate (10-20 contracts) before spike eligibility to filter quote-only noise
- [ ] **TB-443** `planned` — Enforce trade volume ≥ 20% of quote volume delta as mandatory filter; reject signals failing this ratio
- [ ] **TB-444** `planned` — Raise spike_score_threshold to 5.0+ to reduce marginal-quality signals (first example score=2.468 easily blocked)

---

## 2026-04-07 — Advisor snapshot 140

### Summary
Single-contract outliers in thin markets (baseline volume <600) are generating false positives. The detector is picking up low-conviction noise with modest volume deltas (576–592) and small price moves (2–5%) that lack sustained conviction.

### Next step
Implement liquidity-aware thresholds: require higher volume delta multipliers and/or concurrent price-move minimums for markets below a baseline volume floor, rather than applying uniform thresholds across all liquidity regimes.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-445** `planned` — For markets with baseline volume <600, raise spike_min_volume_delta to 1.5× (from current ~1.2×) to filter out thin-market outliers.
- [ ] **TB-446** `planned` — Add a co-requirement rule: in low-liquidity markets, require concurrent priceΔ >0.03 (3%) when volumeΔ is borderline, to confirm multi-sided conviction.
- [ ] **TB-447** `planned` — Introduce a minimum trade-size filter or require ≥2 corroborating trades within a 60–120 second window to reduce single-contract noise in illiquid venues.

---

## 2026-04-07 — Advisor snapshot 141

### Summary
Low-liquidity markets are generating false positives via percentage-based volume deltas on micro-trades and single-contract outliers that lack sustained conviction or market depth.

### Next step
Introduce absolute volume floor (minimum contract count) independent of percentage-based delta, and require corroborating trades within a time window to validate signal strength in thin markets.

### Suggested thresholds
`score_threshold` → `7.5`

### Recommendations

- [ ] **TB-448** `planned` — Add min_absolute_volume constraint (e.g., ≥10 contracts traded in spike window) to filter micro-trades in markets with <100 total daily volume
- [ ] **TB-449** `planned` — Require 2+ trades within 60-second window moving price in same direction before emitting signal, to eliminate single-contract outliers
- [ ] **TB-450** `planned` — Stratify thresholds by market liquidity tier: apply stricter absolute volume floors and higher score thresholds to markets with <500 daily average volume

---

## 2026-04-07 — Advisor snapshot 142

### Summary
Low-liquidity binary markets are generating false positives via small absolute volume trades that appear significant in percentage terms. Both signals flagged the same market with marginal price moves (0.17–0.18) and modest volume deltas (~1,450 contracts) that lack conviction or sustained follow-through.

### Next step
Introduce minimum absolute volume thresholds (not just percentage deltas) and require sustained price hold duration post-spike to filter noise in thin markets.

### Suggested thresholds
`min_price_move` → `0.25`, `score_threshold` → `13.5`

### Recommendations

- [ ] **TB-451** `planned` — Add min_absolute_volume_contracts threshold of 100–500 contracts depending on market tier, to prevent micro-trades from triggering signals
- [ ] **TB-452** `planned` — Require price hold >2–5 minutes post-spike at or above spike level before emitting 'signal' tier (allow 'notable' at lower bar)
- [ ] **TB-453** `planned` — Raise spike_min_price_move from current level to 0.25+ (2.5%) for markets with absolute volume <1,000 contracts to reduce sensitivity in illiquid venues

---

## 2026-04-07 — Advisor snapshot 143

### Summary
Low-liquidity and low-volume markets are generating false positives due to outsized score impacts from small absolute trades. The detector lacks mechanisms to distinguish meaningful flow from noise in thin markets.

### Next step
Introduce market-liquidity-aware thresholds: require either (1) absolute volume floor (5000+ contracts) OR (2) sustained price hold (5+ minutes) to emit 'signal' tier, with 'notable' tier reserved for lower confidence detections.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `score_threshold` → `8.0`

### Recommendations

- [ ] **TB-454** `planned` — Add absolute volume floor requirement: emit 'signal' tier only when volΔ ≥ 5000 contracts, or require sustained price hold >5 minutes post-spike for lower-volume markets
- [ ] **TB-455** `planned` — Implement sustained-move validation: require price movement to hold for 5+ minutes before triggering, filtering single-tick false positives in illiquid pairs
- [ ] **TB-456** `planned` — Adjust score_threshold based on market tier: use higher threshold (e.g., 8.0+) for low-volume markets (<1000 baseline contracts), lower threshold (e.g., 5.0+) only for established pairs with deep liquidity

---

## 2026-04-07 — Advisor snapshot 144

### Summary
Low-liquidity markets (sports betting, binary outcomes) are generating false positives when small absolute trade counts or single-tick price moves trigger volume and score thresholds. The detector lacks context-awareness for market structure and trade sustainability.

### Next step
Introduce market-structure classification (liquidity tier) that enforces stricter thresholds for low-liquidity markets: require either sustained price hold (5+ min) or absolute volume floor (5,000+ contracts), whichever is applicable.

### Suggested thresholds
`min_volume_delta` → `3500.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-457** `planned` — For sports betting markets (low liquidity): raise min_volume_delta from current baseline to >50% above rolling 24h baseline, or require volume_delta >3,500 contracts absolute minimum.
- [ ] **TB-458** `planned` — For binary outcome markets: add sustained_price_hold check—only emit signal if price move is held for ≥5 minutes, not a single tick.
- [ ] **TB-459** `planned` — Add absolute_contract_floor rule: require min 5,000 total contracts traded in the spike window before triggering 'signal' tier; use 'notable' tier as ceiling for smaller spikes.

---

## 2026-04-07 — Advisor snapshot 145

### Summary
The detector is generating false positives across contracts with varying liquidity by treating raw volume deltas and price moves as signal-worthy without accounting for execution quality, market depth, or temporal persistence. Low-liquidity markets and thin contracts are particularly prone to noise.

### Next step
Introduce an execution-quality filter requiring actual traded volume to represent a meaningful % of quoted volume (5-10% for standard contracts, >50% for low-liquidity markets), and add a temporal persistence requirement (sustained price hold or baseline volume multiple) before emitting 'signal' or 'notable' tier alerts.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `score_threshold` → `13.0`

### Recommendations

- [ ] **TB-460** `planned` — For contracts with volΔ < 5000, require either (a) sustained price movement hold >5 minutes post-spike, or (b) volume delta >5x rolling baseline, to filter out single-tick noise in low-liquidity venues
- [ ] **TB-461** `planned` — Add execution-quality gate: flag as noise if (actual_traded_volume / quoted_volume) < 0.05 for standard liquidity, or < 0.50 for sports/binary markets with small contract counts
- [ ] **TB-462** `planned` — Increase spike_min_volume_delta to 5000 for low-liquidity markets (sports betting, binary outcome); maintain lower threshold only for high-volume derivatives where execution quality can be validated

---

## 2026-04-07 — Advisor snapshot 146

### Summary
The detector is generating false positives in low-liquidity markets (sports betting) and thin contracts where small absolute volume changes trigger signals despite weak execution quality. The KXTOPCHEF signal had <0.17% execution rate, while sports betting signals lack sustained conviction or correlated external data.

### Next step
Implement an execution-quality filter requiring actual traded volume to be a meaningful percentage of quoted volume (5-10% for standard contracts, 50%+ for low-liquidity markets), combined with either sustained price movement or volume exceeding 5x baseline.

### Suggested thresholds
`score_threshold` → `15.0`

### Recommendations

- [ ] **TB-463** `planned` — Add execution_rate metric: require actual_traded_volume / quoted_volume > threshold (0.05 for standard liquidity, 0.50 for low-liquidity contracts like sports betting) before scoring spike
- [ ] **TB-464** `planned` — For low-liquidity markets (<$5k baseline volume), enforce either: (a) price movement sustained across 2+ consecutive ticks, or (b) volume_delta > 5x baseline; reject single-tick moves with small absolute volumes
- [ ] **TB-465** `planned` — Segment by contract liquidity tier and apply stricter thresholds to sports betting markets: require correlated signals (injury reports, line movement on major sportsbooks) or spike_score > 15 before flagging watch/notable tier

---

## 2026-04-07 — Advisor snapshot 147

### Summary
Low-liquidity markets (sports betting, watch-tier contracts) are generating false positives from modest volume/price moves that lack execution conviction or sustained conviction. The detector is triggering on noise in thin markets without distinguishing real flow from tick-level fluctuations.

### Next step
Introduce execution-rate validation: require actual traded volume to be ≥5-10% of quoted volume, and for watch-tier/low-liquidity markets, enforce either >50% volume delta above baseline OR sustained multi-tick price moves OR correlated external signals (not just single-tick moves).

### Suggested thresholds
`min_volume_delta` → `3600.0`, `min_price_move` → `0.03`, `score_threshold` → `6.0`

### Recommendations

- [ ] **TB-466** `planned` — Add execution_rate_threshold minimum of 5-10% (actual_traded_vol / quoted_vol) to filter out quoted-volume spikes with minimal real execution
- [ ] **TB-467** `planned` — For tier='watch' contracts, enforce volume_delta ≥1.5x baseline OR minimum_trade_size ≥25 contracts per individual trade to reduce noise in low-activity markets
- [ ] **TB-468** `planned` — For low-liquidity sports markets specifically, require price_move to be sustained across 2+ consecutive ticks OR volume_delta >5x baseline to filter single-tick false positives

---

## 2026-04-07 — Advisor snapshot 148

### Summary
Low-liquidity markets (sports betting, thin order books) are generating false positives due to single small trades triggering volume and price deltas without meaningful execution. The detector lacks context-awareness for market microstructure (execution rate, baseline volume, sustained movement).

### Next step
Implement market-tier-specific rules that require either sustained price movement (3+ consecutive ticks in same direction) OR execution volume >50% above baseline (or >5x for ultra-thin markets), rather than relying solely on absolute volume delta and single-tick price moves.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-469** `planned` — For 'watch' tier alerts in low-liquidity markets (volΔ < 5000): require either 3+ consecutive same-direction price ticks OR volume delta >5x baseline, not just absolute deltas
- [ ] **TB-470** `planned` — Add execution-rate filter: reject signals where actual traded volume is <5% of quoted volume (catches KXTOPCHEF case with 0.17% execution)
- [ ] **TB-471** `planned` — For sports betting / thin markets: require price movement to persist across multiple ticks or combine with external correlation signals (line movement, injury reports) rather than flagging single tick moves
- [ ] **TB-472** `planned` — Implement minimum trade-size threshold of 25+ contracts for individual trades to qualify as spike triggers in lower-activity markets (as noted in KXNBAGAME-26APR08MINORL-ORL)

---

## 2026-04-07 — Advisor snapshot 149

### Summary
Low-liquidity and sports-betting markets are generating false positives from small trades and thin volume spikes that lack meaningful execution or sustained directional conviction. The detector is over-sensitive to absolute volume deltas in markets with naturally low baselines.

### Next step
Implement tiered thresholds by market liquidity/baseline volume, and require execution-rate validation (actual traded volume as % of quoted volume) before emitting signals in lower-activity contracts.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-473** `planned` — For 'watch' tier alerts in low-liquidity markets (baseline vol <5000): require volume delta ≥1.5x baseline AND either sustained price movement (≥3 consecutive ticks same direction) OR minimum trade size ≥25 contracts per order
- [ ] **TB-474** `planned` — Across all tiers: enforce minimum executed/quoted volume ratio of 5-10% to filter out quotes-heavy false spikes; reject signals where execution rate <0.5%
- [ ] **TB-475** `planned` — For sports-betting markets specifically: combine volume spike detection with external correlated data (injury reports, major sportsbook line movement) or require volume delta >50% above baseline before flagging

---

## 2026-04-07 — Advisor snapshot 150

### Summary
Detector is generating false positives in thin/low-liquidity markets by treating small absolute volume moves and minor price ticks as meaningful signals. The core issue is lack of baseline-relative thresholds and execution-quality filters.

### Next step
Introduce baseline-relative volume thresholds (require volume delta ≥50% of baseline) and execution-quality filters (minimum 5-10% execution rate on quoted size) before emitting signals, especially in watch/notable tier contracts.

### Suggested thresholds
`min_volume_delta` → `2000.0`, `min_price_move` → `0.03`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-476** `planned` — Require volume_delta to exceed 50% of market baseline volume before triggering detection in low-liquidity segments (<10k baseline volume)
- [ ] **TB-477** `planned` — Add execution_rate filter: only flag spikes where actual_traded_volume / quoted_volume ≥ 0.05 (5%) to filter out high-quote/low-execution noise
- [ ] **TB-478** `planned` — For watch-tier alerts, enforce minimum trade size threshold of 25+ contracts per trade OR volume delta ≥1.5x baseline to reduce single-trade false positives
- [ ] **TB-479** `planned` — Require sustained price movement (≥3 consecutive same-direction ticks) OR volume delta ≥2x baseline for alerts in markets with sporadic trading patterns
- [ ] **TB-480** `planned` — Integrate external correlated signals for sports betting markets (injury reports, major sportsbook line moves) before escalating watch-tier alerts

---

## 2026-04-07 — Advisor snapshot 151

### Summary
Thin-market false positives dominate recent noise signals. Small absolute volume deltas and minimal price moves in low-liquidity venues are triggering alerts despite weak predictive value (yes probabilities 0.37–0.58).

### Next step
Introduce baseline-relative volume thresholds (e.g., volume delta ≥50% of baseline) and minimum absolute trade size guards for low-activity markets, rather than relying on absolute volume deltas alone.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `4.5`

### Recommendations

- [ ] **TB-481** `planned` — Require volume_delta ≥50% of market baseline volume for markets with <5k baseline daily volume (thin markets); apply only absolute delta floor for higher-liquidity venues
- [ ] **TB-482** `planned` — Add minimum individual trade size filter: reject spikes triggered by single trades <25 contracts in 'watch' tier or <50 contracts in 'notable' tier
- [ ] **TB-483** `planned` — Enforce sustained directional price movement rule: require ≥2 consecutive same-direction ticks before flagging, to filter single-trade noise in low-volume markets

---

## 2026-04-07 — Advisor snapshot 152

### Summary
False positives concentrated in low-liquidity markets where quote updates and small individual trades trigger alerts without genuine flow conviction. Pattern shows thin markets with baseline daily volumes under 10 trades generating noise across both notable and watch tiers.

### Next step
Implement execution-quality filters: require minimum trade count (3-5 executions) or volume intensity (≥1.5-2x baseline) rather than relying solely on volume delta and price move thresholds, which are insufficient for thin markets.

### Recommendations

- [ ] **TB-484** `planned` — Require minimum 3-5 unique trade executions (not quote updates) to accompany volume spikes in markets with <10 daily baseline trades; quote-only volume should not trigger signals
- [ ] **TB-485** `planned` — For watch-tier alerts in low-liquidity markets, enforce volume delta ≥1.5x baseline or require sustained directional price movement (≥3 consecutive ticks same direction)
- [ ] **TB-486** `planned` — Set minimum individual trade size threshold of 25+ contracts to qualify as spike trigger in lower-activity markets; smaller trades in thin books generate high false positive rates
- [ ] **TB-487** `planned` — Implement baseline volume gating: only flag spikes where volume delta ≥50% of baseline daily volume, not absolute delta thresholds alone

---

## 2026-04-07 — Advisor snapshot 153

### Summary
Low-liquidity markets are generating false positives from quote updates and small isolated trades that lack execution volume or sustained momentum. The detector is too sensitive to single-tick moves in thin markets.

### Next step
Add execution-quality gates: require either minimum trade count (3-5 unique executions) OR sustained directional price movement (3+ consecutive ticks) OR volume spike relative to baseline (50%+ of typical daily volume), with market-liquidity-aware thresholds.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `7.5`

### Recommendations

- [ ] **TB-488** `planned` — Require minimum 3 unique trade executions (not quote updates) to validate volume delta signals, especially in markets with <10 daily trades or <100 baseline volume
- [ ] **TB-489** `planned` — Enforce sustained price momentum: require ≥3 consecutive ticks in same direction OR price move ≥5% (not 2-3%) to surface low-liquidity spikes
- [ ] **TB-490** `planned` — Add liquidity-aware baseline rule: flag only when volΔ ≥50% of typical daily volume baseline, not absolute deltas, to filter thin-market noise

---

## 2026-04-07 — Advisor snapshot 154

### Summary
False positives are clustering in low-liquidity markets (sub-10 daily trades) where small absolute volume moves and quote updates trigger signals despite minimal genuine flow conviction.

### Next step
Implement execution-count and baseline-relative volume filters before score evaluation, rather than tuning score thresholds alone. Thin markets need structural guards, not just higher numeric bars.

### Suggested thresholds
`score_threshold` → `7.5`

### Recommendations

- [ ] **TB-491** `planned` — Require minimum 3-5 distinct trade executions (not just quote updates) to validate a spike signal, especially in markets with <10 baseline daily trades
- [ ] **TB-492** `planned` — Gate spike detection on volume delta >= 50% of baseline daily volume in thin markets, to filter noise in sub-10 daily trade venues
- [ ] **TB-493** `planned` — Add liquidity tier check: apply stricter execution/volume thresholds to markets with <50 baseline daily trades before evaluating spike_score_threshold

---

## 2026-04-07 — Advisor snapshot 155

### Summary
False positives cluster in thin markets where quote activity and minimal executed volume trigger alerts despite low conviction (yes probabilities 0.09–0.39). Signals lack sufficient execution depth to validate genuine flow.

### Next step
Require minimum executed trade count (3–5 unique executions) rather than relying solely on volume delta, especially in markets with <10 baseline daily trades.

### Suggested thresholds
`score_threshold` → `6.5`

### Recommendations

- [ ] **TB-494** `planned` — Add min_execution_count rule: require ≥3 unique trade executions accompanying any spike, with stricter enforcement (≥5) in markets under 10 daily trades baseline
- [ ] **TB-495** `planned` — Enforce executed_to_quoted_volume ratio: require ≥50% of volume delta to come from actual executions (not just quotes) to filter quote-stuffing patterns
- [ ] **TB-496** `planned` — Raise spike_min_volume_delta relative to market baseline: require volume spike to exceed 50% of 20-day average daily volume in thin markets, not absolute deltas

---

## 2026-04-07 — Advisor snapshot 156

### Summary
False positives are concentrated in thin markets where quote activity and volume deltas lack genuine execution conviction. Both recent noise signals show high volume deltas but low price moves and/or low trade counts, indicating quote-stuffing rather than real directional commitment.

### Next step
Introduce a minimum executed trade count filter (3-5 unique executions) as a hard gate before emitting signals, especially for markets with <10 daily trades or low price conviction.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.03`, `score_threshold` → `4.5`

### Recommendations

- [ ] **TB-497** `planned` — Require minimum 3-5 unique trade executions (not just quote updates) to accompany any volume spike, with stricter enforcement in low-liquidity venues
- [ ] **TB-498** `planned` — Add executed-to-quoted volume ratio gate: reject spikes where executed volume is <40% of quoted volume delta, filtering pure quote-heavy noise
- [ ] **TB-499** `planned` — Raise spike_min_volume_delta in sub-10-trades-per-day markets to 50000+ to reduce sensitivity to thin-market manipulation patterns

---

## 2026-04-07 — Advisor snapshot 157

### Summary
False positives are driven by quote refreshes and volume delta inflation in thin markets where executed trade volume is minimal. The detector is triggering on quote-only activity rather than genuine conviction-driven flow.

### Next step
Implement executed trade volume validation: require minimum N unique trade executions (not just quoted volume delta) to trigger spike detection, with stricter thresholds in low-liquidity markets (<10 daily trades).

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-500** `planned` — Filter out volume deltas where executed_volume == 0 or executed_volume << quoted_volume_delta; require executed_volume to be ≥50% of reported volume delta to qualify
- [ ] **TB-501** `planned` — For markets with <10 daily trades, enforce minimum 3-5 unique trade executions accompanying any spike signal; for higher-liquidity markets, enforce minimum 2 executions
- [ ] **TB-502** `planned` — Raise spike_min_volume_delta to account for baseline quote churn; use rolling 20-period baseline and trigger only on delta > baseline + 2σ, not raw delta thresholds

---

## 2026-04-07 — Advisor snapshot 158

### Summary
False positives are dominated by quote-only events and micro-lot executions in thin markets, where volume spikes lack accompanying price conviction or genuine trade execution.

### Next step
Require minimum executed trade count (3-5 unique fills) alongside volume delta, and filter quote-only events by enforcing traded_volume > baseline_volume threshold, especially for markets under $0.10 and <10 daily trades.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.005`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-503** `planned` — Filter out quote-refresh noise: reject signals where volume_delta equals baseline exactly or where traded_volume is zero; require traded_volume > 0 and ideally > 50% of reported volume_delta
- [ ] **TB-504** `planned` — Add execution diversity gate: require minimum 3-5 unique trade executions (not quote updates) to qualify for 'signal' tier; use 'watch' tier only for quote-heavy spikes
- [ ] **TB-505** `planned` — Enforce sustained price conviction in thin markets: for markets under $0.10 or <10 daily trades, raise min_price_move to 0.5% (0.005) OR require price_move > 0.02 sustained across 2+ consecutive minutes

---

## 2026-04-07 — Advisor snapshot 159

### Summary
False positives cluster around quote-heavy events and thin-market micro-movements lacking execution conviction. Volume spikes without sustained price action or genuine trades are dominating the watch/notable tiers.

### Next step
Implement executed_trade_volume_ratio filter: require minimum 40-50% of volume delta to come from actual executed trades (not just quote orders), with special stringency in markets under 10 daily trades or <0.10 price levels.

### Suggested thresholds
`min_volume_delta` → `10000.0`, `min_price_move` → `0.005`, `score_threshold` → `5.5`

### Recommendations

- [ ] **TB-506** `planned` — Filter out events where >80% of volume delta is single-quote order placement rather than executed fills (KXTOPCHEF-26DEC31-OSC pattern).
- [ ] **TB-507** `planned` — In low-liquidity markets (<0.10 price or <10 daily trades), require either: (a) sustained price move ≥0.5% OR (b) ≥3-5 distinct trade executions, not just volume spikes (KXTOPCHEF-26DEC31-RHO, KXTOPCHEF-26DEC31-SIE patterns).
- [ ] **TB-508** `planned` — Raise executed_trade_volume_floor: require minimum 500+ shares of actual executed volume (vs. quoted) on thin markets to qualify for signal tier; quote-only refreshes should not trigger alerts (KXTRUMPSAY-26APR13-STUP pattern).

---

## 2026-04-07 — Advisor snapshot 160

### Summary
False positives are dominated by quote-management events and thin-market micro-movements lacking genuine conviction. Volume deltas are inflated by single large orders or quote refreshes rather than executed trades.

### Next step
Implement executed-trade volume filtering: require that actual filled trades comprise ≥40% of volume delta, rejecting quote-only or quote-heavy events before scoring.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-509** `planned` — Filter out spikes where >80% of volume delta originates from a single quote order; treat as order management rather than market signal
- [ ] **TB-510** `planned` — For sub-$0.10 prices, require either ≥0.5% sustained price movement OR multi-minute volume concentration to reach 'signal' tier; 'watch' tier requires executed_trade_volume > 0
- [ ] **TB-511** `planned` — Raise executed-trade-to-quoted-volume ratio threshold: require executed trades to be ≥40% of total volume delta in thin markets (liquidity < threshold), filtering out quote-refresh noise
- [ ] **TB-512** `planned` — Add minimum executed trade count or minimum individual trade size check to eliminate false signals from baseline quote refreshes in low-liquidity instruments

---

## 2026-04-07 — Advisor snapshot 161

### Summary
High false-positive rate in thin/low-liquidity markets where volume spikes occur without corresponding price movement, particularly in college sports and far-dated events. Large score inflation (3M+) with zero price delta indicates algorithmic noise rather than genuine flow.

### Next step
Implement a correlation requirement: volume spikes must be accompanied by minimum price movement (>0.5%) OR absolute volume threshold (>100 contracts) depending on market liquidity tier, to filter rebalancing noise from informed flow.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.005`, `score_threshold` → `500.0`

### Recommendations

- [ ] **TB-513** `planned` — For markets with <10K baseline volume or >6 days to expiry: require volΔ >100 absolute contracts OR priceΔ >0.5%, not just relative multipliers
- [ ] **TB-514** `planned` — Penalize score when priceΔ=0 despite large volΔ: cap spike_score at 50th percentile when price movement is absent in low-liquidity venues
- [ ] **TB-515** `planned` — Add trade-count validation: require trade count magnitude to correlate with volume delta (e.g., avg trade size must be plausible) to catch single-leg algorithmic fills

---

## 2026-04-07 — Advisor snapshot 162

### Summary
False positives cluster in thin/niche markets where volume spikes occur without meaningful price movement, and in low-liquidity college sports markets where algorithmic rebalancing creates noise.

### Next step
Require correlated volume AND price movement in low-liquidity contexts: enforce minimum price_move threshold of 0.5% for markets with baseline volume <1000, rather than relying on volume multipliers alone.

### Suggested thresholds
`min_volume_delta` → `50.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-516** `planned` — Add conditional logic: for markets with sparse baselines (e.g., college sports, niche prediction contracts), raise spike_min_price_move from current level to 0.005 (0.5%) and require absolute volume >50 contracts, not just relative deltas.
- [ ] **TB-517** `planned` — Implement trade-count validation: filter volume spikes where trade_count does not scale proportionally to volume magnitude (e.g., reject 64M volume delta on 1–2 large fills with zero price movement).
- [ ] **TB-518** `planned` — Add duration/persistence filter: for thin markets, require price hold or repeated trades above spike level for 5+ minutes before emitting signal; reject single-tick momentum spikes.

---

## 2026-04-07 — Advisor snapshot 163

### Summary
False positives cluster in low-liquidity, thin markets where volume spikes occur without sustained price conviction. Queue noise, algorithmic rebalancing, and single-tick micro-moves are triggering detections despite weak fundamentals.

### Next step
Enforce a joint volume-price constraint: require both spike_min_volume_delta AND spike_min_price_move to be satisfied simultaneously, with absolute volume floors for thin markets, rather than treating them as independent OR conditions.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-519** `planned` — Raise spike_min_price_move from 0.03 (3%) to 0.05 (5%) for markets with baseline volume <1000 contracts/min to filter single-tick noise and queue churn.
- [ ] **TB-520** `planned` — Add absolute volume floor: spike_min_volume_delta should scale by market liquidity tier—thin markets require >100 absolute contract volume, not just relative multipliers.
- [ ] **TB-521** `planned` — Require price move to persist for ≥2 minutes (not single-tick) before emitting signal; filter out momentum spikes that reverse within 60 seconds.

---

## 2026-04-07 — Advisor snapshot 164

### Summary
False positives cluster in low-liquidity markets where volume spikes occur without meaningful price conviction (0-1% moves). Mechanical rebalancing and queue noise are being flagged as signals despite analyst consensus that these lack genuine information content.

### Next step
Enforce a minimum price-move floor of 0.5-1.0% paired with volume delta, and add liquidity-aware absolute volume thresholds rather than relying on relative multipliers alone. This filters algorithmic noise while preserving real conviction flow.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-522** `planned` — Raise spike_min_price_move from 0.03 (3%) to 0.005-0.01 (0.5-1.0%) for all markets, with stricter enforcement: require price move AND volume delta both present, not OR
- [ ] **TB-523** `planned` — Add liquidity-tier logic: for thin markets (baseline volume <10k contracts/min), require absolute volume threshold >100-500 contracts per spike event instead of relative multipliers
- [ ] **TB-524** `planned` — Implement price-hold validation: flag only when price sustains above spike trigger for 5+ minutes or when trade count scales proportionally with volume delta (filter single-tick microbursts)

---

## 2026-04-07 — Advisor snapshot 165

### Summary
High false-positive rate in low-liquidity markets where large volume spikes occur without meaningful price movement, often representing algorithmic rebalancing rather than genuine conviction shifts.

### Next step
Implement a price-movement floor correlated with volume spikes: require minimum price moves of 0.5–2% for watch/notable tiers, and 2–3% for high-conviction claims in thin markets. Decouple volume delta from score when price move is absent.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-525** `planned` — Raise spike_min_price_move to 0.005 (0.5%) for watch-tier alerts and 0.02 (2%) for notable-tier alerts in markets with baseline volume <100K contracts/day to filter portfolio rebalancing noise.
- [ ] **TB-526** `planned` — For low-liquidity markets, require price-move confirmation: suppress signals where volΔ is high but priceΔ ≤ 0.5%, or apply a multiplicative penalty (e.g., score *= 0.1) when volume spikes without sustained price movement.
- [ ] **TB-527** `planned` — Add absolute volume floor by market tier: require >100 absolute contracts traded (not relative baseline multiplier) for far-dated or niche markets to reduce small-pool noise.
- [ ] **TB-528** `planned` — Introduce trade-count validation: flag only when volume spike count and magnitude align (e.g., volΔ / trade_count suggests genuine fills, not queue churn).
- [ ] **TB-529** `planned` — For thin markets, require price holds: spike must sustain >2% move for ≥5 minutes or involve trades >50 contracts to differentiate conviction from brief momentum.

---

## 2026-04-07 — Advisor snapshot 166

### Summary
The detector is generating false positives primarily from high-volume, price-neutral activity in low-liquidity markets (portfolio rebalancing, queue noise) and single large quotes in micro-cap markets. Price movement is not correlating with volume spikes, causing noise to rank as highly as genuine conviction shifts.

### Next step
Enforce a minimum price-move requirement (0.5–3% depending on liquidity tier) correlated with volume spikes, rather than treating volume and price as independent scoring inputs. This single change will filter 70%+ of the labeled noise while preserving legitimate flow signals.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-530** `planned` — For watch and notable tier alerts on low-liquidity markets (<$50k baseline volume), require minimum price move of ±0.5–1.0% correlated with volume spike, or filter to volume events where trade count ≥ 5 to exclude single-quote noise.
- [ ] **TB-531** `planned` — For micro-cap event markets (≤10 days to resolution, <$100k liquidity), enforce absolute volume minimum (≥100 contracts) rather than relative multipliers, and require sustained directional pressure (5+ consecutive trades in same direction or price hold >5 min) instead of single spikes.
- [ ] **TB-532** `planned` — Raise minimum price-move threshold for binary/sports markets to 2–3% when paired with volume spikes, as 0–1% moves in these thin books reflect mechanical rebalancing, not conviction. Add trade-count validation (volume ≥ trade_count × avg_trade_size) to detect algorithmic vs. organic flow.

---

## 2026-04-07 — Advisor snapshot 167

### Summary
High false-positive rate driven by volume spikes decoupled from price movement and low-conviction micro-markets. Most noise signals show 0–1% price deltas with large volume swings, indicating algorithmic rebalancing rather than genuine flow.

### Next step
Enforce minimum price-move thresholds (0.5–3% depending on liquidity tier) as a hard filter, not just a scoring component. Volume-only signals without correlated price action are predominantly noise.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-533** `planned` — Raise minimum price-move threshold to 0.5% for watch-tier alerts and 1.0% for notable tier on low-liquidity markets (baseline volume <10k contracts)
- [ ] **TB-534** `planned` — For markets under 10 days to resolution with thin order books, require either sustained directional pressure (5+ consecutive trades in same direction) OR absolute volume >100 contracts, not relative multipliers
- [ ] **TB-535** `planned` — Implement trade-count validation: flag only when volume delta correlates with actual trade executions (not just quote-stacking). Require trade_count ≥ volume_delta / 500 as a sanity check
- [ ] **TB-536** `planned` — De-weight or exclude signals with 0% price delta regardless of volume magnitude—these are mechanical portfolio adjustments, not conviction-driven flow

---

## 2026-04-07 — Advisor snapshot 168

### Summary
The detector is generating high false positives in low-liquidity markets where large volume spikes occur without proportional price movement, or where small price ticks are amplified by thin order books. Most false positives cluster around zero or near-zero price moves paired with massive volume deltas, suggesting volume-only triggers are insufficient.

### Next step
Implement a minimum price-move floor (0.5–2% depending on market liquidity tier) that must correlate with volume spikes; decouple volume-only signals from higher conviction tiers. Require trade-count validation or sustained multi-minute price holds rather than single-tick moves.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.015`, `score_threshold` → `8.5`

### Recommendations

- [ ] **TB-537** `planned` — Raise min_price_move to 0.5% as a hard floor for low-liquidity markets; require 2–3% for binary/sports markets to filter portfolio rebalancing and quote-driven noise.
- [ ] **TB-538** `planned` — Add a volume-to-trade-count validation rule: flag only when trade count matches volume magnitude or exceeds a minimum threshold (e.g., 5+ trades) to distinguish genuine flow from algorithmic queue activity.
- [ ] **TB-539** `planned` — For thin markets with <10 days to resolution or baseline volume <5K, require minimum 50–100 absolute contract volume and sustained price hold (5+ minutes above spike level) rather than relative baseline multipliers.
- [ ] **TB-540** `planned` — Demote or suppress watch-tier signals when priceΔ ≤ 0.5%; only escalate to notable/high-conviction if price move ≥ 1–2% or trade count validates the volume spike.

---

## 2026-04-07 — Advisor snapshot 169

### Summary
The detector is generating false positives on price-neutral high-volume events (mechanical rebalancing) and low-conviction micro-moves in thin markets, particularly in niche sports and event prediction categories where liquidity is sparse.

### Next step
Implement a joint price-volume filter: require minimum price move of 2% OR volume delta >8x baseline with sustained (5+ minute) directional pressure, rather than treating volume and price moves as independent signals. This filters mechanical rebalancing while preserving genuine conviction shifts.

### Suggested thresholds
`min_price_move` → `0.02`, `score_threshold` → `7.5`

### Recommendations

- [ ] **TB-541** `planned` — Raise min_price_move to 2% for watch-tier alerts on low-liquidity markets (vol <100k baseline); require 0.5% minimum even for high-volume events to eliminate price-neutral portfolio adjustments.
- [ ] **TB-542** `planned` — Add time-window validation: flag only when price move is sustained for ≥5 minutes or trade count ≥5 trades, filtering out quote-splitting and single-tick noise.
- [ ] **TB-543** `planned` — For micro-cap markets (<10 days to resolution), require volume_delta ≥25-50% of baseline AND price_move ≥1.5% paired with trade execution count ≥5 to validate conviction over pure liquidity artifacts.

---

## 2026-04-07 — Advisor snapshot 170

### Summary
The detector is generating false positives in low-liquidity markets by flagging high-volume activity with minimal or zero price moves, and by over-weighting single large quotes on thin order books without sustained directional conviction.

### Next step
Introduce a tiered rule system that requires price-move correlation with volume spikes: for watch/notable tiers, enforce minimum 0.5–2% price moves paired with volume deltas, and validate with trade count or time-window persistence rather than instantaneous quote activity.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-544** `planned` — Require minimum price move of ±0.5% for watch-tier alerts and ±2% for notable tier in low-liquidity markets (avg daily trades <50) to filter portfolio rebalancing and quote-driven noise.
- [ ] **TB-545** `planned` — Introduce a trade-count floor (5+ executed trades within detection window) or sustained multi-minute directional pressure to validate micro-cap event markets (<10 days to resolution) before emitting high-conviction signals.
- [ ] **TB-546** `planned` — For volume-spike detection, normalize by baseline liquidity profile: require minimum 1.5–2x baseline volume for thin markets AND enforce a 5-minute time window to filter algorithmic execution splitting and millisecond-level quote churn.
- [ ] **TB-547** `planned` — Implement price-to-volume correlation check: flag only when volume spike co-occurs with directional price move in the same direction, rather than treating price-neutral high-volume events as signals.

---

## 2026-04-07 — Advisor snapshot 171

### Summary
The detector is generating excessive false positives on low-liquidity markets by flagging large volume deltas without corresponding price moves, and treating mechanical rebalancing/quote-splitting as informed flow.

### Next step
Implement a liquidity-aware coupling rule: require minimum price move (±0.5-2% depending on market type) paired with volume spike, and validate with trade-count minimums for thin markets rather than relying on volume delta alone.

### Suggested thresholds
`min_price_move` → `0.015`, `score_threshold` → `5.5`

### Recommendations

- [ ] **TB-548** `planned` — For watch-tier alerts: require minimum ±0.5% price move OR sustained directional pressure (5+ trades in 5min window) to filter portfolio adjustments and quote-splitting noise
- [ ] **TB-549** `planned` — For thin markets (<10 daily trades or <100k baseline volume): normalize volume delta by trade count rather than raw volume, and require minimum 5 executed trades + 2%+ price move for notable tier
- [ ] **TB-550** `planned` — For low-conviction/extreme-price markets (probability >0.80 or <0.20): raise price-move threshold to 2-3% paired with 8x+ volume multiplier to distinguish conviction shifts from mechanical rebalancing

---

## 2026-04-07 — Advisor snapshot 172

### Summary
Detector is triggering on algorithmic order splits, quote noise, and extreme-priced thin markets without price confirmation. False positives cluster in low-liquidity, low-trade-count venues where volume deltas alone lack signal value.

### Next step
Introduce market-context normalization: require minimum trade count (5+) and time-window validation (>5min sustained) before flagging, especially for contracts with <10 daily trades or prices >0.80/0.20.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-551** `planned` — Add minimum trade count requirement (5+ actual executions, not quotes) within detection window; filter out millisecond-scale order splits
- [ ] **TB-552** `planned` — For thin markets (<10 daily baseline trades), normalize volume delta by trade count rather than raw volume; require 8x+ multiplier OR 2%+ price move
- [ ] **TB-553** `planned` — Enforce time-window floor (5+ minutes of sustained directional pressure) and require non-zero price move OR high volume concentration ratio to reduce quote-driven false positives
- [ ] **TB-554** `planned` — Apply conviction multiplier for extreme price positions (>0.80 or <0.20): require either 2%+ price move or 8x baseline volume, not either/or
- [ ] **TB-555** `planned` — For low-liquidity entertainment/sports markets: require 1.5x+ baseline volume paired with >5% price move OR 25-50%+ of daily baseline volume with confirmed trades

---

## 2026-04-07 — Advisor snapshot 173

### Summary
False positives cluster in thin/low-conviction markets where algorithmic execution, quote noise, and extreme pricing create high scores without genuine informed flow. The detector lacks market-context awareness and time-window validation.

### Next step
Implement market-liquidity normalization: require volume delta as a multiple of baseline daily volume (not raw delta), paired with time-window enforcement (≥5 min aggregation) and price-move validation that scales with conviction level.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-556** `planned` — Normalize spike_min_volume_delta by baseline contract count or 24h volume for thin markets; flag only when delta exceeds 2-3x baseline rather than absolute thresholds
- [ ] **TB-557** `planned` — Require price move and volume delta to co-occur within a 5+ minute window to filter millisecond-level algorithmic splits and quote-only noise
- [ ] **TB-558** `planned` — Scale price_move threshold inversely with conviction: for extreme prices (yes/no prob >0.80 or <0.20), require ≥2% move; for moderate conviction (0.35–0.65), require ≥3% move
- [ ] **TB-559** `planned` — Enforce minimum trade execution validation: require at least one actual fill (not just resting orders/quotes) before flagging low-volume signals
- [ ] **TB-560** `planned` — Implement tier-specific volume thresholds: 'watch' tier requires ≥25-50% of baseline daily volume; 'notable' requires ≥1.5x baseline

---

## 2026-04-07 — Advisor snapshot 174

### Summary
The detector is generating false positives in thin/low-liquidity markets by treating algorithmic order splits and quote noise as informed flow. Key issues: raw volume deltas don't normalize for contract liquidity; price moves are weighted equally regardless of conviction; time-window requirements are missing.

### Next step
Implement market-context-aware thresholds: require higher price-move minimums (2-5%) for low-conviction markets, normalize volume deltas by baseline trade count rather than raw volume, and enforce minimum 5-minute concentration windows to filter millisecond-level algorithmic noise.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-561** `planned` — Normalize spike_min_volume_delta by contract daily-trade baseline rather than raw volume—thin markets (<10 daily trades) should require 8x+ baseline, liquid markets 1.5-2x baseline
- [ ] **TB-562** `planned` — Introduce dynamic price_move requirement: require 5%+ for yes/no >0.80 or <0.20 (extreme conviction), 3%+ for mid-range (0.3-0.7), 2%+ for standard cases
- [ ] **TB-563** `planned` — Add minimum_time_window = 300 seconds (5 minutes) to volume delta calculation to filter sub-second algorithmic splits and quote-driven noise
- [ ] **TB-564** `planned` — Increase score_threshold from current level to 6.5+ to reduce watch-tier false positives (KXMARMAD-26-CONN scored 7.095 but was noise)

---

## 2026-04-07 — Advisor snapshot 175

### Summary
The detector is triggering on thin-market volume moves without price conviction and on extreme-probability markets where small absolute moves are noise. False positives cluster when volume deltas lack supporting price action or occur in low-liquidity/high-conviction contexts.

### Next step
Implement context-aware thresholds: require price_move ≥ 2% OR (volume_delta ≥ 8x contract baseline AND price_move > 0%) for low-liquidity markets; require price_move ≥ 2% for markets with probability > 0.80.

### Suggested thresholds
`min_price_move` → `0.02`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-565** `planned` — For markets with <10 daily trades, normalize volume_delta by contract count and require min_price_move ≥ 0.02 (2%) to filter single-contract mechanical moves.
- [ ] **TB-566** `planned` — Reject signals where volume_delta occurs without price_move (priceΔ = 0.0) unless volume concentration window > 5 minutes, to filter millisecond-scale algorithmic splits.
- [ ] **TB-567** `planned` — For extreme-probability markets (yes > 0.75 or yes < 0.25), require either price_move ≥ 0.02 or volume_delta ≥ 8x rolling baseline, not raw volume thresholds.

---

## 2026-04-07 — Advisor snapshot 176

### Summary
Volume spikes without accompanying price movement are generating false positives across both ultra-short-duration and low-liquidity markets, suggesting the detector is too sensitive to isolated order flow that lacks conviction.

### Next step
Implement a conjunctive filter: require either (a) meaningful price movement paired with volume spike, OR (b) volume spike exceeding a higher absolute threshold. This prevents small orders and thin-market noise from triggering signals.

### Suggested thresholds
`min_volume_delta` → `35.0`, `min_price_move` → `0.005`, `score_threshold` → `5.5`

### Recommendations

- [ ] **TB-568** `planned` — For markets with <1% price movement, enforce minimum volume delta of 30+ contracts (15m) or 50+ contracts (niche/low-liquidity) to filter conviction-less flow.
- [ ] **TB-569** `planned` — Raise minimum price-move threshold for low-liquidity markets from 0.0% to 0.5%, or alternatively require volume deltas >200 to bypass price-move requirement.
- [ ] **TB-570** `planned` — Add market-tier-specific scoring: discount spike_score when price movement is absent, capping max score at ~3.5 unless priceΔ ≥ 0.5%.

---

## 2026-04-07 — Advisor snapshot 177

### Summary
Volume spikes without accompanying price movement are generating false positives across diverse market types (low-conviction crypto, ultra-short duration, thin niche sports). The detector is triggering on mechanical or uninformed flow that lacks directional conviction.

### Next step
Enforce a joint condition: require meaningful price movement (0.5-2% depending on market liquidity/duration) to accompany volume spikes, rather than accepting volume or price movement independently.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `6.0`

### Recommendations

- [ ] **TB-571** `planned` — For low-conviction markets (implied probability <10%), require minimum 1-2% price move alongside 10x+ volume delta to filter mechanical flow in KXMARMAD-26-CONN class signals.
- [ ] **TB-572** `planned` — For ultra-short-duration markets (15m), raise minimum volume threshold from current level to 30+ contracts OR require directional price movement; reject signals with low volume and zero price delta.
- [ ] **TB-573** `planned` — For low-liquidity/niche markets, enforce minimum 0.5% price move requirement rather than accepting zero price movement; pair with volume spike detection to reduce thin-market false positives.

---

## 2026-04-07 — Advisor snapshot 178

### Summary
High false-positive rate across diverse market types driven by volume spikes decoupled from meaningful price movement. Current thresholds trigger on 1% price moves with pure volume signals, conflating mechanical rebalancing and thin-book noise with genuine directional intent.

### Next step
Introduce market-context coupling: require price_move >= 2% OR (price_move >= 1% AND directional_flow_ratio >= 0.70) to gate volume-only signals, stratified by market liquidity tier and time horizon.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-574** `planned` — Raise spike_min_price_move baseline to 2% globally; allow 1% exception only when directional volume concentration >70% to single side
- [ ] **TB-575** `planned` — Implement liquidity-aware volume thresholds: thin markets (<100 baseline vol) require min 10x baseline; standard markets require min 3x baseline; remove pure volume triggers in micro-duration contracts (<30m)
- [ ] **TB-576** `planned` — Add directional_flow_ratio gate: require >70% of spike volume to one side (bid or ask) for sub-2% price moves to filter mechanical rebalancing

---

## 2026-04-07 — Advisor snapshot 179

### Summary
The detector is generating false positives across low-liquidity and thin-book markets by triggering on volume spikes decoupled from meaningful price momentum. High volume deltas without corresponding price moves (1% or less) are consistently labeled as noise even when score is elevated.

### Next step
Implement a strict correlation rule: require price_move to exceed 2% OR volume_delta to be accompanied by sustained directional flow bias (>70% one-sided) depending on market liquidity tier. Decouple volume and price thresholds by market type rather than using global minimums.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-577** `planned` — For low-liquidity markets (baseline vol <100): enforce minimum price_move >2% OR require volume_delta >10x rolling baseline + directional bias >70% one-sided
- [ ] **TB-578** `planned` — For thin micro-markets (<30min timeframes): replace volume-delta triggers with directional flow alignment (>70% of volume to one side) and require price_move >1% confirmation
- [ ] **TB-579** `planned` — For high-conviction markets (implied prob >85%): raise min_price_move threshold to 2-3% to filter mechanical rebalancing; volume alone is insufficient signal
- [ ] **TB-580** `planned` — For political/event-driven markets: add multi-timeframe confirmation rule—require volume spike to persist or repeat across 2+ consecutive candles before emission

---

## 2026-04-07 — Advisor snapshot 180

### Summary
False positives cluster in thin-liquidity markets where volume spikes lack price conviction or sustained directional bias. The detector is triggering on mechanical rebalancing, isolated whale clusters, and single large orders that don't reflect genuine market consensus.

### Next step
Implement market-liquidity-aware tiering: require price moves >2% AND sustained directional flow alignment (>70% volume to one side) for low-liquidity markets (<100 baseline volume); for whale-cluster detection, raise minimum trade count threshold to 4-5 and require 1% baseline volume cumulative rather than 0.4%.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-581** `planned` — For whale-cluster tier (15m KXBTC): raise minimum trade count from 3 to 4–5 and require cumulative volume ≥1% of 15m baseline to reduce isolated cluster false positives.
- [ ] **TB-582** `planned` — For all low-liquidity markets (baseline <100): mandate minimum price move of 2% AND directional flow alignment ≥70% on one side to filter mechanical rebalancing noise.
- [ ] **TB-583** `planned` — For high-conviction markets (>85% implied probability): require price move ≥2–3% alongside volume spikes to suppress rebalancing-driven false positives.
- [ ] **TB-584** `planned` — For sub-30m micro markets: prioritize directional flow alignment metric (>70% one-sided volume) over raw volume delta as primary signal qualifier.

---

## 2026-04-07 — Advisor snapshot 181

### Summary
High false-positive rate driven by volume spikes decoupled from price action and trade confirmation, especially in thin markets and short timeframes where mechanical rebalancing dominates.

### Next step
Implement tiered minimum price-move requirements by market liquidity/conviction level, and require trade-level confirmation (executed trades within 5-10min window) before emitting signals on volume deltas.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-585** `planned` — Require minimum executed trade count (4-5 trades) or sustained directional volume alignment (>70% to one side) within 5-10 minutes of detected volume spike before signal emission
- [ ] **TB-586** `planned` — Raise minimum price-move threshold to 2-3% for high-conviction markets (>85% implied prob) and thin-liquidity markets (<100 baseline volume) to filter mechanical rebalancing
- [ ] **TB-587** `planned` — For sub-30min and thin-book markets, require cumulative volume >1% of rolling baseline (not 0.4%) and directional bias confirmation rather than absolute volume delta alone
- [ ] **TB-588** `planned` — Add market-specific tiers: apply stricter price-move floors for political/niche prediction markets (>5% for conviction flow) and enforce multi-timeframe confirmation for low-conviction, high-volume spikes

---

## 2026-04-07 — Advisor snapshot 182

### Summary
High-confidence and thin markets are generating false positives from mechanical volume spikes decoupled from informed trading. Single large orders in stable markets and retail scatter in low-liquidity venues are triggering alerts despite minimal price conviction.

### Next step
Introduce market-context-aware thresholds: require higher price-move thresholds (2-3%) in low-volume markets and high-confidence markets (yes/no >0.90), and raise absolute volume minimums for ultra-short timeframes (15m). Decouple volume and price requirements rather than treating them as independently sufficient.

### Suggested thresholds
`min_volume_delta` → `150.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-589** `planned` — For markets with conviction >0.90 or <0.10: require priceΔ ≥ 0.02 (2%) OR sustained multi-tick momentum, not single spikes
- [ ] **TB-590** `planned` — For 15-minute timeframes: raise spike_min_volume_delta from 80 to 150+ contracts and require priceΔ ≥ 0.02 (2%) to accompany volume
- [ ] **TB-591** `planned` — For markets with total daily volume <5000 contracts: require priceΔ ≥ 0.025 (2.5%) alongside any volume spike to signal

---

## 2026-04-07 — Advisor snapshot 183

### Summary
The detector is firing on volume spikes decoupled from price action across diverse market types—low-conviction binary markets, stable high-conviction finals, ultra-short timeframes, and thin long-tail sports. Price movement is either absent or minimal (0–1%), suggesting liquidity provision and scattered retail trades rather than informed flow.

### Next step
Enforce a minimum price-move requirement (0.5–3% depending on market conviction and timeframe) alongside volume spikes. Volume alone is insufficient; require sustained directional pressure to validate signal.

### Suggested thresholds
`min_volume_delta` → `150.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-592** `planned` — Raise spike_min_price_move from 0.0 to 0.01 (1%) globally; scale higher for thin or stable markets (2–3% for long-tail sports, ultra-short timeframes).
- [ ] **TB-593** `planned` — Introduce market-conviction-conditional logic: for yes-probability in range [0.40, 0.60], require ≥1.0% price move; for yes ≥0.90 or ≤0.10, require ≥1.5–2.0% to filter single-order noise in settled outcomes.
- [ ] **TB-594** `planned` — Raise spike_min_volume_delta thresholds by market bucket: 15-minute markets ≥150 contracts (from 80), long-tail sports ≥2,500 contracts, to reduce mechanical executions in illiquid venues.

---

## 2026-04-07 — Advisor snapshot 184

### Summary
The detector is generating excessive false positives on short-duration markets (especially 15m BTC) by flagging high-volume trades at zero or near-zero price impact, which reflect mechanical repositioning rather than directional conviction. Long-tail and stable markets also show noise from single large orders without sustained momentum.

### Next step
Require minimum price move correlated with volume spikes across all market types, with stricter thresholds for ultra-short horizons (15m) and thin markets. Use market-specific sensitivity tuning based on baseline volatility and conviction level.

### Suggested thresholds
`min_volume_delta` → `1.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-595** `planned` — For whale-cluster tier on 15m markets: require minimum 0.5% price move OR >10 distinct whale addresses to validate directional intent (filters inventory repositioning noise)
- [ ] **TB-596** `planned` — For all tiers on markets <1h duration: raise minimum volume delta to 1.0x recent baseline (not near-zero thresholds) to filter mechanical order-book activity
- [ ] **TB-597** `planned` — For thin/long-tail markets with <2% typical price moves: require 2-3% absolute price move alongside volume spike, or exclude from signaling entirely
- [ ] **TB-598** `planned` — For stable high-conviction markets (yes >0.85 or <0.15): require sustained price momentum beyond 1-2 ticks to validate single large order executions as informative
- [ ] **TB-599** `planned` — Increase p-value threshold for whale-cluster on 15m micro-markets from 0.0000 to 0.001 to suppress rapid sequential flat-price buys

---

## 2026-04-07 — Advisor snapshot 185

### Summary
The detector is generating excessive false positives on 15-minute BTC micro-markets by flagging large volume deltas without concurrent price movement. Most noise signals show volΔ=400-852 with priceΔ=0.0%, indicating mechanical/inventory repositioning rather than informed directional trades.

### Next step
Require minimum price movement (≥0.5% for whale-cluster tier, ≥1% for watch tier) concurrent with volume spikes as a gating filter before emitting any signal, especially on markets with <1-hour expiry windows.

### Suggested thresholds
`min_volume_delta` → `1.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-600** `planned` — For whale-cluster tier on 15m markets: require priceΔ ≥ 0.5% OR multi-directional flow OR trades spanning ≥3 distinct price levels to gate high-volume single-direction signals
- [ ] **TB-601** `planned` — For watch/notable tier on low-conviction markets (price 0.45–0.55): require priceΔ ≥ 0.75% alongside volΔ to filter liquidity-provision noise
- [ ] **TB-602** `planned` — Raise minimum volume delta threshold for ultra-short windows (≤15m) from absolute numbers to 5–10% of recent baseline, or require volΔ > 1.0x baseline to avoid flagging coincidental clustering
- [ ] **TB-603** `planned` — For stable high-conviction markets (yes >0.90): raise volΔ threshold or require sustained price momentum beyond single-tick moves to separate large executions from information flow
- [ ] **TB-604** `planned` — For long-tail thin markets: require priceΔ ≥ 2–3% alongside volΔ to account for retail scatter and reduce false positives on minimal-conviction movements

---

## 2026-04-07 — Advisor snapshot 186

### Summary
Whale-cluster signals on 15-minute BTC micro-markets are firing with high scores (8–30) despite zero price impact, creating false positives. The detector treats large absolute volume deltas as informative even when they fail to move the market, indicating mechanical/algo positioning rather than conviction.

### Next step
Require minimum price movement (≥0.5–1.0%) concurrent with whale-cluster volume spikes on short-horizon markets (≤15min); decouple volume-delta scoring from price-impact scoring so that high volume without market movement does not accumulate signal strength.

### Suggested thresholds
`min_volume_delta` → `150.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-605** `planned` — Add a price-move gating rule: whale-cluster tier signals on markets with <30min expiry require priceΔ ≥ 0.5% OR volume delta must exceed 10% of baseline (not absolute counts) to trigger scoring.
- [ ] **TB-606** `planned` — For 15-minute BTC markets specifically, raise min_volume_delta from current baseline to require >5–10% of recent 1-hour baseline volume, or require volume to span >3 distinct price levels to filter single-level clustering.
- [ ] **TB-607** `planned` — Reduce whale-cluster score multiplier in ultra-short timeframes when priceΔ = 0.0%; apply a 0.3–0.5x penalty to score when large volume fails to move price, reflecting mechanical repositioning.
- [ ] **TB-608** `planned` — Raise p-value threshold for whale-cluster detection from 0.0000 to 0.001 on 15-minute markets to reduce false flagging of rapid sequential small trades that cluster by chance.
- [ ] **TB-609** `planned` — For low-conviction / thin markets (yes <0.55 and >0.45, or vol <500/day), require priceΔ ≥ 1.0% alongside any volume spike before emitting signal.

---

## 2026-04-07 — Advisor snapshot 187

### Summary
The detector is generating excessive false positives on 15-minute BTC micro-markets and other short-duration contracts by flagging volume spikes with zero or minimal price impact. The core issue is that whale-cluster signals lack meaningful price conviction, indicating mechanical order flow rather than informed positioning.

### Next step
Require minimum price movement (≥0.5-1.0%) concurrent with volume spikes on markets with duration ≤15 minutes, or equivalently raise volume_delta threshold to represent >5-10% of baseline and add a price-impact filter to all whale-cluster detections.

### Suggested thresholds
`min_volume_delta` → `1.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-610** `planned` — For 15-minute and ultra-short markets (duration ≤15m): require spike_min_price_move ≥ 0.005 (0.5%) alongside volume delta, or require volume delta to exceed 10% of baseline instead of near-zero absolute thresholds
- [ ] **TB-611** `planned` — Implement market-duration-aware thresholds: raise spike_min_volume_delta to 1.0x baseline for markets ≤30 minutes, and require 5-10% baseline delta for whale-cluster tier specifically
- [ ] **TB-612** `planned` — Add price-impact validation: whale-cluster signals must show ≥0.5% price movement in cluster direction within 2-minute window, or require participation from >10 distinct addresses to confirm conviction
- [ ] **TB-613** `planned` — Reduce whale-cluster p-value sensitivity on short-horizon markets from 0.0001 to 0.001 to avoid flagging mechanical sequential order clustering at flat prices
- [ ] **TB-614** `planned` — For low-volatility or stable-price markets (yes probability 0.45–0.55 range), require minimum price move ≥1% alongside volume spikes to filter liquidity-provision noise

---

## 2026-04-07 — Advisor snapshot 188

### Summary
Whale-cluster signals on 15-minute micro-markets are generating excessive false positives due to flagging volume spikes without corresponding price movement or baseline-relative thresholds. Most noise cases show zero price delta despite high scores, indicating mechanical/inventory repositioning rather than informed directional trades.

### Next step
For whale-cluster tier on short timeframes (≤15min): require minimum price move of ±0.5% concurrent with volume delta, OR enforce volume delta as percentage of baseline (≥5-10%) rather than absolute units, to filter out coordination signals lacking market conviction.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-615** `planned` — For 15-minute markets, require spike_min_price_move ≥ 0.005 (0.5%) when tier=whale-cluster and spike_min_volume_delta is triggered; zero-price-move whale clustering is mechanical noise.
- [ ] **TB-616** `planned` — Replace absolute volume_delta thresholds with baseline-relative metric: require volΔ > 5-10% of recent baseline volume for whale-cluster signals, not raw unit counts (e.g., 400-850 units), which vary by asset liquidity.
- [ ] **TB-617** `planned` — For whale-cluster on ultra-short expiries (≤15min), raise p-value threshold from ~0.0001 to 0.001 to filter high-frequency coincidental clustering; require either price impact ≥0.5% OR cluster spanning ≥3 distinct price levels.
- [ ] **TB-618** `planned` — For low-conviction markets (prices near 0.45–0.55), apply tighter coupling: require price_move ≥ 0.01 (1%) alongside volume spikes before emitting signal.
- [ ] **TB-619** `planned` — Add temporal persistence filter: whale-cluster directional volume must sustain direction for ≥2 minutes or show multi-address participation (≥10 distinct whale addresses) on 15-minute windows to reduce single-order execution noise.

---

## 2026-04-07 — Advisor snapshot 189

### Summary
Whale-cluster detection on 15-minute micro-markets is generating excessive false positives by flagging statistical trader clustering without accompanying price impact or baseline-relative volume. The detector conflates coordination signals with mechanical order flow.

### Next step
For whale-cluster tier signals on markets with expiry ≤15 minutes: require EITHER (1) volume delta >5% of recent baseline AND price move ≥0.5%, OR (2) volume delta >10% of baseline alone. Add a price-impact filter: if volume delta exceeds 1.0x baseline, price must move ≥1% in the direction of cluster dominance.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-620** `planned` — Enforce volume_delta > 5% of baseline for whale-cluster signals on ≤15m markets, or require concurrent price_move ≥0.5% to filter mechanical positioning
- [ ] **TB-621** `planned` — Raise p-value threshold for whale-cluster detection on short-duration markets from ~0.0001 to 0.001 to reduce sensitivity to coincidental trader clustering
- [ ] **TB-622** `planned` — For whale-cluster signals with price_move = 0.0%, require volume_delta to exceed 10% of baseline AND persist in one direction for ≥2 minutes, or require >10 distinct whale addresses
- [ ] **TB-623** `planned` — Add price-impact gate: if volume spike lacks directional price movement (≥0.5%), flag as uncertain or mute unless volume delta is genuinely extreme (>15% baseline)
- [ ] **TB-624** `planned` — For watch-tier signals, require price_move ≥0.5% alongside volume spikes to filter liquidity-provision noise in low-conviction price zones

---

## 2026-04-07 — Advisor snapshot 190

### Summary
The detector is generating excessive false positives on 15-minute BTC micro-markets by flagging whale-cluster activity with zero price impact and sub-1% volume deltas relative to baseline. High statistical scores (8.0–29.0) are being assigned to mechanical positioning trades that lack market conviction or directional evidence.

### Next step
Implement a dual-gate requirement for whale-cluster signals on short-duration markets (≤15min): require EITHER (1) volume delta ≥5% of recent baseline AND price move ≥0.5%, OR (2) volume delta ≥10% of baseline with multi-directional confirmation across ≥3 price levels. This filters coordinated noise while preserving genuine informed flow.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-625** `planned` — Raise spike_min_volume_delta for whale-cluster tier on ≤15min markets from near-zero to ≥5–10% of recent baseline volume to eliminate sub-1% positioning noise.
- [ ] **TB-626** `planned` — Add mandatory spike_min_price_move ≥0.5% (or ≥1% for ultra-short windows) when whale-cluster volume spike is detected, as zero-price-impact trades are mechanical repositioning.
- [ ] **TB-627** `planned` — Increase p-value threshold for whale-cluster statistical test from 0.0001 to 0.001 on 15-minute contracts to reduce sensitivity to sequential small-order clustering.
- [ ] **TB-628** `planned` — For whale-cluster signals without price impact, require temporal persistence (≥2 minutes in same direction) or cross-price-level spread (trades at ≥3 distinct price points) before emission.
- [ ] **TB-629** `planned` — Introduce market-context gate: on high-volatility 15m markets (baseline ±10%+ swings), raise minimum whale-cluster participation requirement to ≥10 distinct addresses or require ≥20% price impact alongside volume spike.

---

## 2026-04-07 — Advisor snapshot 191

### Summary
The detector is generating excessive false positives on whale-cluster tier alerts, particularly for 15-minute micro-markets and high-baseline assets, by flagging volume anomalies that lack measurable price impact or economic significance.

### Next step
Implement a dual-gate filter: require whale-cluster signals to satisfy EITHER (volume_delta > 5-10% of baseline AND price_move >= 0.5%) OR (price_move >= 1.0%), with stricter thresholds on short-duration (≤15min) contracts. This eliminates mechanical order clustering unaccompanied by conviction.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-630** `planned` — For whale-cluster tier on 15-minute markets: raise minimum volume_delta to >5% of recent baseline (not absolute counts), or mandate concurrent price movement ≥0.5% to filter inventory repositioning noise.
- [ ] **TB-631** `planned` — Require whale-cluster spikes to show measurable price impact (≥0.5% minimum, ≥1.0% for micro-markets) or enforce persistence (trades across ≥3 distinct price levels or sustained direction for 2+ minutes) to exclude single-price-level clustering.
- [ ] **TB-632** `planned` — Increase p-value threshold for whale-cluster statistical detection from ~0.0001 to 0.001 on short-duration markets, or raise minimum distinct whale-address participation from implicit to explicit >10 addresses to reduce false positives from algorithmic/mechanical behavior.
- [ ] **TB-633** `planned` — Apply stricter scoring or suppress whale-cluster signals entirely on ultra-short markets (<15min) unless accompanied by baseline-relative volume surge (>10% of baseline) AND price movement (>0.5%), since coordination without impact signals low conviction.
- [ ] **TB-634** `planned` — For high-baseline markets (e.g., KXMARMAD-26-MICH), mandate volume_delta to exceed >0.5–1.0x baseline OR price_move >0.5% to escape statistical anomalies in trader count that lack economic impact.

---

## 2026-04-07 — Advisor snapshot 192

### Summary
Whale-cluster detector is generating false positives on 15-minute ultra-short-dated markets by flagging volume deltas of 400–850 units with zero price impact. The detector treats statistical clustering of small trades as signal-worthy despite lacking economic conviction or market impact.

### Next step
For whale-cluster tier on short-duration markets (≤15min), require either (1) volume delta >5% of baseline volume OR (2) price move ≥0.5–1.0% alongside any cluster detection. This filters mechanical algo clustering from informed positioning.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-635** `planned` — Introduce baseline-relative volume thresholds: require volume_delta to exceed 5–10% of recent baseline volume for whale-cluster signals on 15-minute markets, rather than absolute unit counts.
- [ ] **TB-636** `planned` — Mandate price-impact co-requirement: flag whale-cluster only when priceΔ ≥0.5% OR volume exceeds 10x baseline; pure coordination without market movement is mechanical noise.
- [ ] **TB-637** `planned` — Raise p-value threshold for whale-cluster detection from 0.0001 to 0.001 on micro-timeframe contracts to reduce sensitivity to coincidental small-trade clustering.
- [ ] **TB-638** `planned` — For high-baseline markets (KXMARMAD-26-MICH tier), require volume_delta >1.0x baseline OR priceΔ ≥0.5% before emitting whale-cluster alerts.
- [ ] **TB-639** `planned` — Add persistence requirement: whale-cluster signals must sustain direction for ≥2 minutes or span ≥3 distinct price levels to exclude single-point concentrations.

---

## 2026-04-07 — Advisor snapshot 193

### Summary
The detector is generating excessive false positives in ultra-short-dated micro-markets (15m BTC) and high-baseline markets (MARMAD) by flagging volume spikes with zero or minimal price impact. Genuine signals show coordinated directional flow with measurable price moves; noise cases show large absolute volumes that are negligible relative to baseline.

### Next step
Implement a market-context-aware volume delta threshold: require volume_delta to exceed a percentage of baseline (5-10% for 15m markets, 15%+ for high-baseline >7M/24h markets) AND enforce a price-move floor (≥0.5%) when volume delta exceeds baseline, rather than flagging on coordination alone.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-640** `planned` — For 15-minute markets: raise minimum volume delta threshold to 5-10% of baseline volume, or require price_move ≥0.5% alongside any flagged whale-cluster activity
- [ ] **TB-641** `planned` — For high-baseline markets (>7M volume/24h): require volume_delta ≥0.15x baseline OR price_move ≥0.5% to qualify as signal; filter out large absolute volumes that represent <1% of normal liquidity
- [ ] **TB-642** `planned` — Require multi-event confirmation for whale-cluster detection: flag only when coordinated volume persists across 2+ consecutive candles or 3+ separate trades, not single-quote aggregates
- [ ] **TB-643** `planned` — Add price-impact validation: whale-cluster spikes without measurable price movement in spike direction within 1-2 minutes should be downgraded or filtered as noise
- [ ] **TB-644** `planned` — For low-conviction markets (yes_confidence <0.6): require volume_delta ≥1.0x baseline AND price_move ≥0.5% before emitting signal

---

## 2026-04-07 — Advisor snapshot 194

### Summary
The detector is generating high false positives on ultra-short-duration markets (15-min BTC binaries, thin UConn betting) by triggering whale-cluster alerts on small absolute volume deltas with zero price impact, confusing mechanical order placement and rebalancing with informed trading.

### Next step
Implement a tiered baseline-relative volume threshold: require volume_delta to exceed 1% of market baseline for whale-cluster tier signals, and mandate concurrent or immediate directional price impact (≥1-2%) to distinguish informed positioning from mechanical noise.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-645** `planned` — For whale-cluster alerts: enforce volume_delta > max(0.01 * baseline_volume, 1000 contracts) AND price_move ≥ 1.0% in same direction, or reject as noise
- [ ] **TB-646** `planned` — For low-conviction/thin markets (baseline <50k or 24h vol <7M): require volume_delta > 0.15x baseline AND price_move > 0.5%, or use notable/weak tier instead of whale-cluster
- [ ] **TB-647** `planned` — For 15-minute micro-markets: filter out spikes where volume delta produces <1% measurable price impact; require multi-event confirmation (≥3 coordinated trades) within 60-second window rather than single large quote aggregation
- [ ] **TB-648** `planned` — Add market-regime filter: suppress whale-cluster alerts when prior directional macro move (>3% in preceding 5min) already explains order flow; require sustained post-spike price continuation (60-120s) to confirm informed positioning

---

## 2026-04-07 — Advisor snapshot 195

### Summary
Whale-cluster detector on 15-minute BTC markets is generating high false positives by triggering on volume spikes without price impact or directional conviction. The majority of flagged signals show zero price movement (priceΔ=0.0) despite high volume deltas, indicating mechanical order flow rather than informed positioning.

### Next step
Require correlated price movement (minimum 0.5–1.0%) or sustained directional order imbalance (>70% skew) to confirm whale-cluster signals on ultra-short timeframes, rather than relying on volume clustering alone.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.005`, `score_threshold` → `12.0`

### Recommendations

- [ ] **TB-649** `planned` — Add a price-movement gate: reject whale-cluster signals where priceΔ < 0.5% and volΔ < 5% of recent baseline volume, filtering liquidity-probing noise
- [ ] **TB-650** `planned` — Enforce directional conviction: require order imbalance skew (bid:ask or buy:sell ratio) >70:30 on the flagged side when price movement is absent
- [ ] **TB-651** `planned` — Raise minimum absolute volume threshold: require volΔ > 1000 contracts (or >5% of 1h baseline, whichever is higher) for tier-8 whale-cluster alerts on 15m markets to exclude statistical noise
- [ ] **TB-652** `planned` — Tighten p-value threshold for micro-timeframes: increase p-value cutoff from 0.0000 to 0.001–0.01 for sub-1h expiry markets to filter sub-second mechanical execution patterns
- [ ] **TB-653** `planned` — Implement volume-baseline normalization: reject signals where volΔ is <1% of the preceding 1-hour baseline, as these represent micro-noise in thin markets

---

## 2026-04-07 — Advisor snapshot 196

### Summary
Whale-cluster detector is generating high false positives on 15-minute BTC markets by flagging coordinated volume without price conviction. The majority of noise cases show zero or near-zero price movement despite high score and volume delta, indicating the detector is capturing algorithmic execution noise and liquidity-testing behavior rather than informed directional flow.

### Next step
Require minimum correlated price movement (≥0.5%) to accompany whale-cluster signals on ultra-short timeframes (≤15m), or filter alerts where volume delta is <5% of baseline AND price move is 0%. This single rule will eliminate most false positives while preserving genuine informed flow signals.

### Suggested thresholds
`min_volume_delta` → `5.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-654** `planned` — Add mandatory price-movement gate: reject whale-cluster alerts on 15m markets unless priceΔ ≥ 0.5% or volume-delta exceeds 50% of 1h baseline
- [ ] **TB-655** `planned` — Enforce minimum volume delta threshold relative to baseline: require volΔ ≥ 5% of recent hourly baseline before triggering tier-8+ alerts on short-duration markets
- [ ] **TB-656** `planned` — Implement directional conviction filter: require ≥70% volume concentration on one side (bid/ask) for whale-cluster signals to qualify on micro-timeframe markets
- [ ] **TB-657** `planned` — Raise participant threshold for 15m windows: increase minimum whale-cluster participants from current level to 60+ unique addresses in 120s window to exclude sub-baseline noise
- [ ] **TB-658** `planned` — Add absolute volume floor: exclude alerts where volΔ < 1000 contracts on derivative markets, as sub-1000 spikes on thin order books are statistical noise

---

## 2026-04-07 — Advisor snapshot 197

### Summary
Whale-cluster detector is generating excessive false positives on 15-minute ultra-short markets by flagging coordinated quote activity and mechanical micro-trades with zero or negligible price impact. The core issue: volume-delta signals alone, without price correlation or baseline-relative thresholds, cannot distinguish informed flow from liquidity provision and algorithmic noise.

### Next step
Require whale-cluster signals to satisfy at least one of: (1) price move ≥0.5–1.0%, or (2) volume delta ≥5–10% of baseline, or (3) directional consensus (≥70% one-sided volume). This filters quote-driven false positives while preserving genuine informed-flow signals.

### Suggested thresholds
`min_volume_delta` → `0.08`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-659** `planned` — Add mandatory price-correlation gate: reject whale-cluster signals with priceΔ < 0.5% unless volΔ exceeds 10% of recent baseline volume.
- [ ] **TB-660** `planned` — Introduce baseline-relative volume delta: flag only when volΔ > 5–10% of rolling 1-hour baseline, not raw absolute counts, to normalize for market microstructure variance.
- [ ] **TB-661** `planned` — Require directional conviction for ultra-short expiry: enforce ≥70% one-sided volume concentration or sustained multi-leg execution pattern before emitting tier-8+ whale alerts on 15-minute markets.
- [ ] **TB-662** `planned` — Suppress sub-second cluster detections: raise statistical p-value floor (e.g., from 0.0000 to 0.001) to filter algorithmic execution noise masquerading as whale coordination.
- [ ] **TB-663** `planned` — Add absolute-volume floor: reject signals where absolute volΔ < 500–1000 on micro-baseline markets to avoid flagging statistical noise in thin orderbooks.

---

## 2026-04-07 — Advisor snapshot 198

### Summary
The whale-cluster detector is generating overwhelming false positives on 15-minute ultra-short-duration markets by flagging high-frequency quote activity and mechanical order clustering without corresponding price conviction or impact. The two genuine signals in the dataset had large volume deltas (>500) and directional persistence, while 18 of 20 labeled signals show zero or negligible price moves despite high volume delta and confidence scores.

### Next step
Require minimum price move of ≥0.5% OR volume delta >5% of baseline (not absolute count) to trigger whale-cluster signals on markets with <1h expiry. This filters quote-driven noise while preserving informed directional flow.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-664** `planned` — Add mandatory price-impact gate: reject whale-cluster signals with priceΔ < 0.5% on ultra-short windows (≤15m), unless volume delta exceeds 10% of baseline
- [ ] **TB-665** `planned` — Switch volume delta metric from raw absolute units to percentage of rolling baseline; flag only when volΔ > 5–10% of baseline (not <1%)
- [ ] **TB-666** `planned` — Introduce directional persistence check: confirm whale-cluster signals with price momentum in the same direction within 2–3 candles post-signal, or deprioritize as liquidity provision
- [ ] **TB-667** `planned` — Lower whale-cluster p-value sensitivity or raise score_threshold for 15m markets specifically; current yes≈0.95 triggers on quote clustering alone

---

## 2026-04-07 — Advisor snapshot 199

### Summary
Whale-cluster detector is severely oversensitive to ultra-short-duration markets (15min BTC) and low-liquidity venues, firing on sub-1% baseline volume deltas and quote activity with zero or negligible price impact. The majority of false positives come from mechanical high-frequency noise rather than informed directional conviction.

### Next step
Implement market-class-specific thresholds: require volume delta ≥5% of baseline for 15min markets and ≥3% for sub-10% probability low-liquidity markets before flagging whale-cluster signals. Additionally, require minimum price move of ≥0.5% or sustained multi-tick follow-through to accompany volume spikes.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-668** `planned` — For ultra-short-duration markets (15min expiry), raise minimum volume delta threshold to 5% of baseline or absolute 10k contracts, whichever is higher, to filter mechanical quote clustering.
- [ ] **TB-669** `planned` — Require minimum price impact of ≥0.5% correlated with volume spike for whale-cluster signals on 15min and low-liquidity markets, filtering out conviction-free micro-trades.
- [ ] **TB-670** `planned` — Add market-class detection: suppress whale-cluster alerts entirely in ultra-liquid 15min markets (baseline volume >>55k) when volume delta is <1% of baseline, as these represent sub-threshold noise.
- [ ] **TB-671** `planned` — Implement sustained-pressure confirmation: require volume spike to persist across at least 2-3 consecutive ticks or a 60+ second window before emitting whale-tier signal on short-duration markets.
- [ ] **TB-672** `planned` — Add quote-to-trade ratio floor: require actual executed volume to exceed 10% of the flagged volume delta to distinguish directional orders from market-making quote activity.

---

## 2026-04-07 — Advisor snapshot 200

### Summary
Ultra-short-duration markets (15-min) are generating high-confidence whale-cluster signals (score=8.0) with minimal or zero price impact and negligible volume relative to baseline, indicating quote-driven false positives rather than genuine directional flow.

### Next step
Introduce market-duration and liquidity-aware thresholds: require volume delta >5% of baseline AND non-zero price impact (>0.5%) for whale-cluster alerts on markets with ≤15min expiry; alternatively, gate whale-cluster signals on short-duration contracts by requiring sustained multi-tick pressure or directional imbalance (>60/40 side ratio) rather than single-burst detection.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-673** `planned` — For 15-min markets: raise spike_min_volume_delta to 5-10% of rolling baseline (not absolute volume) to filter micro-timeframe clustering noise.
- [ ] **TB-674** `planned` — For whale-cluster tier on ultra-short windows: require spike_min_price_move ≥ 0.5% (0.005) to confirm actual market impact; quote-stuffing and HFT positioning do not move prices in thin ultra-liquid markets (yes>95%).
- [ ] **TB-675** `planned` — Add directional flow validation: reject whale-cluster signals unless order-side imbalance exceeds 60/40 split or price deltas are sustained across ≥2 consecutive ticks; single-burst micro-trades lack conviction.
- [ ] **TB-676** `planned` — For low-liquidity markets (KXMARMAD, KXNBAGAME): require minimum 10% volume delta relative to baseline OR 1% price impact to trigger any tier-1 alerts, as thin books amplify statistical clustering without market absorption.
- [ ] **TB-677** `planned` — Gate whale-cluster detection on short-duration expiries by lowering score_threshold or adding a sub-rule: require actual executed volume (not just quote count) to exceed 10% of baseline before emitting signal.

---

## 2026-04-07 — Advisor snapshot 201

### Summary
Whale-cluster signals in ultra-short-dated (15m) and low-liquidity markets are generating noise due to statistical clustering and quote activity without price impact or conviction. The detector is flagging sub-1% baseline volume spikes with zero or minimal price deltas as high-confidence signals.

### Next step
Implement market-context-aware filtering: require either (1) price delta >0.5% OR (2) volume delta >5% of baseline for whale-cluster alerts, with stricter enforcement on ultra-short windows (≤15m expiry) and low-liquidity baselines.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-678** `planned` — Add market-duration filter: for contracts with ≤15 minute expiry, raise volume_delta threshold to minimum 5-10% of baseline or require absolute volume >10,000 contracts before whale-cluster signals fire.
- [ ] **TB-679** `planned` — Require dual confirmation: whale-cluster alerts must show either meaningful price impact (≥0.5% move) OR directional flow imbalance (≥60/40 side ratio) to filter quote-stuffing and market-making noise.
- [ ] **TB-680** `planned` — Implement liquidity-adjusted thresholds: for baseline volumes >13M daily or >55k per window, require either volume delta >1% of baseline OR sustained multi-tick follow-through (30%+ of spike volume validated in next 10-20 ticks) before emission.
- [ ] **TB-681** `planned` — Add quote-execution ratio floor: filter out low-conviction micro-trades by requiring minimum quote-size threshold or enforcing that ≥30% of detected spike volume must be backed by executed trades at comparable prices.
- [ ] **TB-682** `planned` — Context-condition price extremes: suppress whale-cluster alerts when underlying implied probability is already extreme (>95% or <5%) in short-duration markets unless accompanied by >0.5% price delta, as mechanical pushes are inevitable and uninformative.

---

## 2026-04-07 — Advisor snapshot 202

### Summary
The whale-cluster detector is generating excessive false positives on ultra-short-dated markets (15-minute expiry) and low-liquidity venues by flagging statistically significant volume clusters that lack meaningful price impact or baseline-relative magnitude. Analysts consistently recommend filtering signals where price movement is near-zero and volume delta is below 5-10% of baseline.

### Next step
Implement a composite filter requiring whale-cluster signals to satisfy at least one of: (1) price_move ≥ 0.5%, (2) volume_delta ≥ 10% of baseline, or (3) directional flow imbalance ≥ 60/40 side ratio. This will eliminate mechanical order-placement noise while preserving informed flow.

### Suggested thresholds
`min_volume_delta` → `0.1`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-683** `planned` — Raise spike_min_price_move from current level to 0.005 (0.5%) for whale-cluster tier on ultra-short markets (≤15min expiry), or add price-movement requirement as bypass condition
- [ ] **TB-684** `planned` — Add baseline-relative volume filter: require volume_delta to exceed 10% of trailing baseline volume before flagging whale-cluster signals, with exceptions for markets showing directional conviction (60/40+ imbalance)
- [ ] **TB-685** `planned` — Implement follow-through validation for 15-minute markets: require at least 30% of spike volume to execute at comparable/better prices within 10-20 ticks to confirm informed activity vs. quote stuffing
- [ ] **TB-686** `planned` — Lower whale-cluster score_threshold or add liquidity-context gating: suppress alerts when price is already at extremes (>95% implied probability) unless volume delta exceeds 10% of baseline
- [ ] **TB-687** `planned` — Add quote-to-trade ratio floor to filter quote-heavy noise spikes on lower-liquidity markets; require minimum executed trade volume proportion

---

## 2026-04-07 — Advisor snapshot 203

### Summary
False positives dominate in whale-cluster signals across ultra-short-dated low-volume markets (e.g., KXBTC15M) and high-baseline markets (e.g., KXMARMAD), where small volume deltas, near-zero price moves, and routine market-making trigger alerts without predictive impact.

### Next step
Require minimum price move >0.005 (0.5%) AND volume delta >5% of baseline for all whale-cluster tiers to filter noise.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-688** `planned` — Raise min_volume_delta to 10000 absolute for markets with baseline <1M volume
- [ ] **TB-689** `planned` — Require priceΔ >0.005 or volΔ >10% baseline for ultra-short-dated markets (<1h expiry)
- [ ] **TB-690** `planned` — Lower whale-cluster score_threshold to 0.90 only if volΔ >5% baseline, else suppress

---

## 2026-04-07 — Advisor snapshot 204

### Summary
Whale-cluster signals are generating excessive false positives in ultra-short-dated, high-baseline-volume markets like KXBTC15M and KXMARMAD, where small volume deltas (<1% of baseline) with minimal or zero price impact reflect quote activity, clustering artifacts, or routine market-making rather than informed flow.

### Next step
Require volume delta to exceed 5% of baseline volume before triggering whale-cluster alerts, with market-specific baselines dynamically computed over recent windows.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.005`, `score_threshold` → `8.5`

### Recommendations

- [ ] **TB-691** `planned` — Add minimum price move requirement of 0.005 (0.5%) for whale-cluster signals to filter zero-impact quote events.
- [ ] **TB-692** `planned` — Raise score_threshold to 8.5 for markets with yes probability >0.95 to reduce sensitivity in extreme-probability regimes.
- [ ] **TB-693** `planned` — Require minimum absolute volume delta of 5000 for ultra-short-dated markets (<1h expiry) to ignore sub-baseline noise.

---

## 2026-04-07 — Advisor snapshot 205

### Summary
whale-cluster tier is generating excessive false positives across low-liquidity markets, thin 15-minute contracts, and extreme-probability outcomes where volume spikes occur with zero price impact and represent <1% of baseline activity.

### Next step
Implement a composite filter for whale-cluster signals: require EITHER (a) volume delta ≥5% of baseline AND price move ≥0.5%, OR (b) absolute volume delta ≥100k contracts minimum. This eliminates quote-stuffing and clustering artifacts while preserving genuine informed positioning.

### Suggested thresholds
`min_volume_delta` → `100000.0`, `min_price_move` → `0.005`, `score_threshold` → `15.0`

### Recommendations

- [ ] **TB-694** `planned` — Add baseline-relative volume threshold: spike_min_volume_delta_pct = 5.0 (% of baseline). Flag only when volΔ > baseline × 0.05, filtering sub-1% noise spikes.
- [ ] **TB-695** `planned` — Enforce price-impact floor for whale-cluster tier: require priceΔ ≥ 0.005 (0.5%) OR volΔ ≥ 100k absolute contracts to emit signal, eliminating zero-price-move false positives.
- [ ] **TB-696** `planned` — Suppress whale-cluster alerts on ultra-extreme probabilities: exclude markets with yes >0.95 or <0.05 from whale-cluster detection, or raise spike_score_threshold to 15+ for these outcomes.
- [ ] **TB-697** `planned` — Add market-depth filter for short-dated contracts: lower whale-cluster detection sensitivity when time-to-expiry <1 hour OR baseline volume >100k, requiring volΔ ≥ 10k absolute minimum.
- [ ] **TB-698** `planned` — Implement execution-to-quote ratio gate: only flag whale-cluster spikes when actual traded volume (not quoted) represents ≥1% of spike activity, filtering passive order clustering.

---

## 2026-04-07 — Advisor snapshot 206

### Summary
whale-cluster tier is generating excessive false positives on low-liquidity and ultra-short-term markets where volume spikes represent <1% of baseline and produce zero price impact, indicating quote-stuffing and algorithmic clustering rather than informed flow.

### Next step
Require whale-cluster signals to satisfy BOTH a relative volume threshold (spike delta ≥5% of baseline) AND a price-impact floor (≥0.5% price move) OR an absolute volume floor (≥50k contracts) to filter out passive quoting and clustering artifacts in thin/short-dated markets.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-699** `planned` — Implement a baseline-relative volume gate: only trigger whale-cluster if volΔ exceeds max(5% of market baseline, 50k contracts absolute)
- [ ] **TB-700** `planned` — Add mandatory price-impact correlation: suppress whale-cluster alerts when priceΔ = 0.0 unless absolute volume delta exceeds 100k contracts or baseline is <1M
- [ ] **TB-701** `planned` — Exclude ultra-short-dated markets (<1 hour to expiry) from whale-cluster scoring unless volume delta exceeds 10% of baseline, as quote-stacking is routine in these instruments
- [ ] **TB-702** `planned` — For markets with extreme probabilities (>0.95 or <0.05), require price movement ≥0.5% or volume delta ≥10% of baseline before flagging, as clustering near certainty is non-informative
- [ ] **TB-703** `planned` — Distinguish executed trade volume from quoted volume: only count trades actually filled, not passive orders, when assessing whale-cluster significance

---

## 2026-04-07 — Advisor snapshot 207

### Summary
Whale-cluster detector is generating excessive false positives on low-volume spikes without price impact, especially in ultra-short timeframes (15-min), low-conviction markets, and high-baseline-volume instruments where quote activity dominates actual execution.

### Next step
Require minimum price impact (≥0.5%) OR minimum volume delta as percentage of baseline (≥5-10%) to trigger whale-cluster alerts, filtering out pure quote-stacking and algorithmic clustering noise.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-704** `planned` — Add baseline-relative volume threshold: flag whale-cluster only when volΔ ≥ 5% of instrument's baseline daily volume, or volΔ > 100k contracts absolute
- [ ] **TB-705** `planned` — Require non-zero price impact for whale-cluster tier: enforce priceΔ ≥ 0.5% OR volume must be directionally correlated with price movement to suppress quote-stacking alerts
- [ ] **TB-706** `planned` — Suppress whale-cluster alerts on ultra-short timeframes (<1 hour expiry) unless absolute volume delta exceeds 10k contracts, as quote activity dominates 15-min micro-markets
- [ ] **TB-707** `planned` — For watch-tier signals: require executed trade volume ≥ 10-20% of quoted spike volume within 5 seconds to confirm genuine flow versus large resting quotes
- [ ] **TB-708** `planned` — Lower whale-cluster score for extreme-probability markets (yes/no > 0.95 or < 0.05) by 3-4 points unless price moves in volume direction, as quote-stacking near certainty is non-informative

---

## 2026-04-07 — Advisor snapshot 208

### Summary
Whale-cluster detector is generating excessive false positives on low-liquidity and ultra-short-term markets where volume spikes lack price impact or execution confirmation. Most flagged signals show zero or negligible price movement despite high clustering scores.

### Next step
Require minimum price impact (≥0.5%) OR minimum volume delta as percentage of baseline (≥5-10%) to qualify whale-cluster signals; additionally, enforce that executed trade volume must be ≥10-20% of quoted spike volume within 5 seconds for watch-tier and above.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-709** `planned` — Add a mandatory price-impact gate: whale-cluster signals require priceΔ ≥0.5% OR volΔ ≥5% of baseline; pure clustering without either fails to signal informed flow
- [ ] **TB-710** `planned` — Implement execution-ratio validation: require that actual filled volume ≥10-20% of spike volume within 5-second window; pure quote stacking is algorithmic noise
- [ ] **TB-711** `planned` — Tier-conditional baseline scaling: for whale-cluster on markets <10M daily delta or <1 hour to expiry, require absolute volume delta ≥50k-100k contracts OR price impact ≥0.5%
- [ ] **TB-712** `planned` — Ultra-probability market filter: suppress whale-cluster alerts when market probability >0.95 or <0.05 unless price moves >0.5%, as extreme-probability markets are dominated by passive quoting
- [ ] **TB-713** `planned` — For watch-tier signals with mismatched volume/price (e.g., volΔ>50M but priceΔ<1%), require quote-to-trade ratio validation before emission

---

## 2026-04-07 — Advisor snapshot 209

### Summary
Whale-cluster detector is triggering massively on low-liquidity and ultra-short-term markets with zero or minimal price impact, confusing statistical quote clustering with informed trading. Nearly all false positives occur when volume delta is <1% of baseline and priceΔ=0.0.

### Next step
Require minimum price impact (≥0.5%) OR minimum volume delta (≥5% of baseline) for whale-cluster signals; additionally, exclude pure quote events by mandating minimum executed trade volume as percentage of quoted volume.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`, `score_threshold` → `6.0`

### Recommendations

- [ ] **TB-714** `planned` — Implement dual-gate for whale-cluster tier: require (priceΔ ≥ 0.005 OR volΔ ≥ 5% of baseline) to emit signal, blocking clustering-only alerts
- [ ] **TB-715** `planned` — Add execution ratio filter: require minimum 10-20% of spike volume to execute as actual trades within 5 seconds before flagging whale-cluster on watch/whale tiers
- [ ] **TB-716** `planned` — Lower whale-cluster score_threshold from 8.0 to 6.0 OR add market-liquidity modifier: reduce score by 50% when baseline < 10M daily volume or when timeframe < 1 hour
- [ ] **TB-717** `planned` — For extreme-probability markets (yes >0.95 or <0.05), require minimum absolute volume delta of 50k+ contracts OR price move >0.5% to qualify as whale-cluster signal
- [ ] **TB-718** `planned` — Require minimum directional skew confirmation (yes/no ratio imbalance) for illiquid micro-markets below price 0.27, as volume alone lacks signal quality

---

## 2026-04-07 — Advisor snapshot 210

### Summary
Whale-cluster detector is firing on pure volume clustering without price impact across low-liquidity and extreme-probability markets, generating systematic false positives. The core issue is decoupling of volume delta from both baseline percentage and price execution.

### Next step
Require whale-cluster signals to satisfy either (a) volume delta ≥5% of 1h baseline OR (b) price impact ≥0.5%, eliminating pure clustering noise while preserving genuinely informed flow.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-719** `planned` — Add baseline-relative volume gate: reject whale-cluster signals where volΔ < 5% of 1h baseline volume, unless priceΔ ≥ 0.5%
- [ ] **TB-720** `planned` — Enforce price-impact floor: require priceΔ ≥ 0.5% for whale-cluster signals on low-conviction markets (<10% or >90% probability) or ultra-short timeframes (≤120s)
- [ ] **TB-721** `planned` — Separate quote activity from trade execution: require minimum 10-20% of spike volume to execute as actual fills within 5 seconds before flagging whale-cluster in micro-markets (15m, 1m contracts)
- [ ] **TB-722** `planned` — Tune score_threshold by market liquidity tier: use score ≥8.0 only when baseline volume >10M daily; for sub-10M markets require score ≥9.0 or additional priceΔ confirmation
- [ ] **TB-723** `planned` — Exclude pure extreme-probability quoting: on markets with yes/no ≥0.95 or ≤0.05, require volΔ to be ≥10% of baseline or priceΔ ≥1% to qualify as signal

---

## 2026-04-07 — Advisor snapshot 211

### Summary
Whale-cluster detector is generating pervasive false positives on low-liquidity markets by flagging volume clustering without price impact or meaningful baseline percentage thresholds; most noise cases show zero or near-zero price movement with volume deltas <1% of baseline.

### Next step
Implement a mandatory dual-gate for whale-cluster tier: require EITHER (price_move ≥ 0.5%) OR (volume_delta ≥ 5% of baseline), AND exclude signals where both price_move = 0.0 and volume_delta < 1% of baseline.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-724** `planned` — Add liquidity-adjusted gate: for markets with <50M daily volume, require volume_delta to exceed 5% of 1h baseline OR price_move ≥ 0.5% before emitting whale-cluster signals.
- [ ] **TB-725** `planned` — Require price impact confirmation on low-volatility windows: reject whale-cluster alerts when price_move = 0.0 AND volume_delta < 1% of baseline, as these indicate order-book absorption without conviction.
- [ ] **TB-726** `planned` — For ultra-short timeframes (≤120s) and high-baseline-volume markets (>100k), raise spike_min_volume_delta to 5-10% of baseline to filter quote-stuffing artifacts from meaningful whale positioning.
- [ ] **TB-727** `planned` — On low-conviction markets (<10% or >90% probability), require minimum absolute volume_delta of 100k contracts OR price_move ≥ 0.5% to qualify as whale-cluster signal.
- [ ] **TB-728** `planned` — For binary markets and illiquid tiers (watch, notable), raise minimum absolute trade size threshold to 10+ shares and require sustained multi-trade confirmation within 5-minute window before escalating score.

---

## 2026-04-07 — Advisor snapshot 212

### Summary
Whale-cluster tier is generating 16/20 false positives (80%) by flagging volume clustering without correlated price impact or baseline-relative thresholds. Most noise occurs in low-liquidity markets where small absolute volumes trigger high scores despite zero or minimal price movement.

### Next step
Implement a composite AND gate: require whale-cluster signals to satisfy EITHER (volume_delta > 1% of rolling 1h baseline AND price_move > 0.5%) OR (absolute_volume_delta > 50k contracts AND price_move > 0.3%) to eliminate clustering-alone noise in thin markets.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-729** `planned` — Add mandatory price-impact floor: reject whale-cluster signals where priceΔ < 0.5% unless volume_delta exceeds 5-10% of 1h baseline.
- [ ] **TB-730** `planned` — Implement baseline-relative volume gating: require spike_min_volume_delta to scale with market liquidity (e.g., 0.5% of 1h baseline for <50M daily volume markets, 0.1% for >100M).
- [ ] **TB-731** `planned` — For low-conviction markets (yes/no probability <10% or >90%), raise absolute volume threshold to 100k+ contracts or require 1%+ price move to reduce statistical clustering false positives.
- [ ] **TB-732** `planned` — Add execution-confirmation filter: flag large quoted volumes only if 10-20% executes as trades within 5 seconds; reject pure quoting activity.
- [ ] **TB-733** `planned` — Cross-validate against order-book depth: suppress whale-cluster alerts during periods with <1% volatility in preceding 30-minute window.

---

## 2026-04-07 — Advisor snapshot 213

### Summary
Whale-cluster detector is generating pervasive false positives on low-liquidity KXMARMAD markets by flagging volume clustering without corresponding price impact or meaningful baseline percentage moves. Nearly all flagged signals have priceΔ=0.0 and sub-1% baseline volume delta, indicating algorithmic quoting rather than informed flow.

### Next step
Introduce a composite gating rule for whale-cluster tier: require EITHER (volΔ ≥ 1% of 1h baseline AND priceΔ ≥ 0.5%) OR (volΔ ≥ 50k notional AND priceΔ ≥ 0.01 sustained over 5min) to suppress clustering-only artifacts.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-734** `planned` — For whale-cluster signals: require minimum price movement of ±0.5% within 5 minutes OR volume delta ≥ 5% of rolling 1-hour baseline to gate out zero-impact clustering noise.
- [ ] **TB-735** `planned` — Add baseline-relative volume filter: suppress whale-cluster signals when volΔ < max(1% of 1h baseline, 50k notional) in markets with <50M daily volume.
- [ ] **TB-736** `planned` — For low-conviction markets (outcome price <10% or >90%): raise whale-cluster threshold to require either ≥100k absolute volume delta OR ≥1% price move, or skip detection entirely.
- [ ] **TB-737** `planned` — For watch/notable tier on illiquid markets: require minimum 10-20% of spike volume to execute as actual trades within 5 seconds; filter out unexecuted large quotes.
- [ ] **TB-738** `planned` — Add volatility context: suppress whale-cluster alerts during periods with <1% price movement in the preceding 30-minute window, indicating liquidity management vs. informed flow.

---

## 2026-04-07 — Advisor snapshot 214

### Summary
Whale-cluster detector is generating high-confidence false positives on low-liquidity markets by flagging volume clustering without corresponding price impact or baseline-relative thresholds. Nearly all flagged signals show yes≤0.08 confidence despite score=8.0, indicating systematic over-sensitivity to statistical clustering.

### Next step
Implement a mandatory dual-gate filter: require volume delta to exceed 1% of 1-hour baseline AND either (a) price impact ≥0.5% or (b) absolute executed volume ≥50k contracts, to distinguish informed flow from algorithmic quoting and passive liquidity clustering.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-739** `planned` — Add baseline-relative volume gate: reject whale-cluster signals where volΔ < 1% of rolling 1h baseline volume, regardless of score
- [ ] **TB-740** `planned` — Introduce price-impact requirement: require priceΔ ≥0.5% OR absolute volume threshold ≥50k contracts to suppress clustering-only noise
- [ ] **TB-741** `planned` — Segregate low-liquidity markets: apply 5-10% baseline threshold (vs. 1%) for markets with <10M daily volume or <100k spike volume to match market microstructure
- [ ] **TB-742** `planned` — Cross-validate execution: for large quote spikes, require ≥10-20% to execute as actual trades within 5 seconds before flagging
- [ ] **TB-743** `planned` — Suppress low-conviction outcomes: disable whale-cluster detection on markets trading <10% or >90% to filter thin-edge noise

---

## 2026-04-07 — Advisor snapshot 215

### Summary
Whale-cluster detector is firing on volume concentration alone without price impact, generating 18/20 false positives across low-liquidity and high-conviction markets. Zero priceΔ dominates the noise, indicating detection is triggered by order clustering or passive quotes rather than informed trading.

### Next step
Require minimum price impact (±0.5%) OR volume delta >5% of baseline for whale-cluster signals; decouple volume concentration from informativeness by mandating either price discovery or sustained directional skew (>80/20 ratio with correlated price movement).

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`, `score_threshold` → `10.0`

### Recommendations

- [ ] **TB-744** `planned` — Implement dual-gate logic: whale-cluster fires only if (priceΔ > 0.5%) OR (volΔ > 5% of baseline AND directional_ratio > 80/20 AND price_momentum > 1% over 5min window)
- [ ] **TB-745** `planned` — Add baseline-relative threshold: reject signals where volΔ < max(0.5% of 1h baseline, $50k notional) in markets with <50M daily volume
- [ ] **TB-746** `planned` — Require execution confirmation: flag only when 10-20% of spike volume executes as actual trades within 5 seconds (not just queued quotes); filter passive order-book depth
- [ ] **TB-747** `planned` — Lower whale-cluster score contribution when priceΔ = 0.0; reduce score by 50% or require score ≥ 10 for zero-price-move alerts
- [ ] **TB-748** `planned` — Add low-volatility filter: suppress whale-cluster flags during <1% price movement in 30-minute window on conviction markets (yes > 0.90)

---

## 2026-04-07 — Advisor snapshot 216

### Summary
Whale-cluster detector is generating high-confidence false positives across low- and high-liquidity markets by flagging volume concentration without correlated price impact. Nearly all recent signals show zero or minimal price movement (<0.01), indicating liquidity management or passive quotes rather than informed trading.

### Next step
Require conjunctive validation: whale-cluster signals must show EITHER (a) price impact ≥0.5% within 5 minutes of volume spike, OR (b) volume delta ≥1% of rolling 1-hour baseline AND sustained directional imbalance (>80/20 buy/sell ratio). Eliminate pure volume-delta triggers.

### Suggested thresholds
`min_volume_delta` → `0.01`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-749** `planned` — Mandate minimum price movement of ±0.5% within 5 minutes following whale-cluster detection, or demote signal confidence to 'watch' tier below spike_score_threshold
- [ ] **TB-750** `planned` — Implement baseline-relative thresholds: require volume delta to exceed 1% of rolling 1-hour baseline for low-conviction markets (<50M daily volume) and 0.5% for high-conviction markets (>10M daily volume)
- [ ] **TB-751** `planned` — Add order-imbalance filter: require directional skew >3:1 (buy/sell or vice versa) or >80/20 ratio sustained over ≥3 trades to validate whale intent when price impact is minimal
- [ ] **TB-752** `planned` — Distinguish executed vs. queued volume: require minimum 10-20% of spike volume to execute as trades within 5 seconds; passive quotes do not trigger whale-cluster alerts
- [ ] **TB-753** `planned` — Suppress whale-cluster signals during low-volatility windows (<1% price movement in preceding 30 minutes) to filter liquidity-management noise

---

## 2026-04-07 — Advisor snapshot 217

### Summary
Whale-cluster tier is generating overwhelming false positives (>95% noise) across all markets due to flagging zero-price-movement volume concentrations in isolation. The detector conflates passive liquidity clustering with directional information flow.

### Next step
Implement a composite filter: require whale-cluster alerts to satisfy EITHER (1) price_delta ≥ 0.5% OR (2) volume_delta ≥ 5% of rolling 1h baseline. This eliminates directionally-neutral clusters while preserving genuine conviction trades.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-754** `planned` — Require priceΔ ≥ 0.5% OR volΔ ≥ 5% of baseline for whale-cluster tier; reject alerts with both priceΔ=0 and volΔ<5% baseline
- [ ] **TB-755** `planned` — For low-liquidity venues (baseline daily volume <50M), raise threshold to volΔ ≥ 10% baseline or priceΔ ≥ 1%, or apply minimum notional gate ($50k+)
- [ ] **TB-756** `planned` — Add volatility context: suppress whale-cluster alerts during low-vol windows (<1% price move in 30m) unless volΔ >10% baseline, filtering liquidity-management noise
- [ ] **TB-757** `planned` — For binary/thin markets, increase minimum single-trade size threshold to 10+ shares and require 2+ trades within 5min window before escalating to whale-cluster
- [ ] **TB-758** `planned` — Cross-validate order-book imbalance: require directional skew >70/30 ratio or order-imbalance ratio >2:1 when priceΔ≈0 to distinguish informed clustering from passive positioning

---

## 2026-04-07 — Advisor snapshot 218

### Summary
The whale-cluster detector is generating systematic false positives across MICH and CONN markets by flagging high-score signals with zero or near-zero price movement. Nearly all 20 signals show priceΔ=0.0 despite high volume deltas, indicating the detector treats volume concentration as directional signal without requiring price discovery validation.

### Next step
Implement a mandatory price-movement gate for whale-cluster alerts: require either (1) priceΔ ≥ 0.5% OR (2) volumeΔ ≥ 5% of rolling 1h baseline. This filters directionally-neutral volume clusters while preserving genuine informed-flow signals that move the market.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-759** `planned` — Add conditional logic: whale-cluster signals with priceΔ=0.0 must meet volumeΔ ≥ 5% of 1h baseline; if volumeΔ < 5% baseline, require priceΔ ≥ 0.5% to trigger alert.
- [ ] **TB-760** `planned` — For low-conviction markets (CONN tier), raise bar to volumeΔ ≥ 10% of baseline OR priceΔ ≥ 1.0%, and require sustained directional skew (>80/20 order imbalance) to reduce false positives in thin venues.
- [ ] **TB-761** `planned` — Introduce market-liquidity gating: for markets with >10M daily volume, require priceΔ ≥ 0.5% regardless of volumeΔ; for markets <50M daily volume, require volumeΔ ≥ 1% of daily volume OR priceΔ ≥ 1.0%.
- [ ] **TB-762** `planned` — Filter microstructure noise by excluding whale-cluster signals during low-volatility windows (<1% price movement in prior 30m) unless accompanied by order-imbalance ratio >3:1 or sustained multi-trade confirmation.

---

## 2026-04-07 — Advisor snapshot 219

### Summary
The whale-cluster detector is generating false positives across KXMARMAD and KXMARMAD-26-CONN by flagging volume concentration (8.0 scores, 0.98 yes-confidence) without corresponding price impact. Zero or near-zero price deltas dominate the noise signals, indicating the detector conflates liquidity provision with informed trading.

### Next step
Require concurrent price movement (≥0.5%) OR volume delta exceeding 5-10% of rolling 1h baseline before escalating to whale-cluster tier; filter out all spike detections with priceΔ=0.0.

### Suggested thresholds
`min_volume_delta` → `0.07`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-763** `planned` — Exclude whale-cluster detections when priceΔ < 0.005 (0.5%) to eliminate pure liquidity-provision false positives
- [ ] **TB-764** `planned` — Normalize volume delta thresholds to rolling baseline: require volΔ > 5-10% of 1h baseline for high-volume markets (>10M daily) and >10% for low-liquidity markets (<50M daily)
- [ ] **TB-765** `planned` — For low-conviction markets (yes<0.5), enforce minimum order-imbalance ratio (80/20+ skew) or sustained directional price movement (≥1% over 5+ min window) alongside volume concentration
- [ ] **TB-766** `planned` — Implement absolute volume floor for whale-cluster alerts: reject spikes <100k contracts notional or <0.5% of daily volume in thin markets
- [ ] **TB-767** `planned` — Recalibrate whale-cluster scoring to downweight pure trade counts in ultra-high-baseline-volume contracts; prioritize executed volume as % of quote volume instead

---

## 2026-04-07 — Advisor snapshot 220

### Summary
Whale-cluster detector is systematically over-triggering on KXMARMAD-26-MICH and KXMARMAD-26-CONN despite zero or minimal price movement, indicating volume delta alone is insufficient to distinguish informed trading from passive liquidity provision in high-conviction, liquid markets.

### Next step
Enforce a dual-gate requirement for whale-cluster tier: require EITHER (a) price movement ≥0.5% concurrent with volume delta, OR (b) volume delta ≥5-10% of rolling baseline AND order-side directional skew ≥80/20 ratio. This filters passive quote-fragmentation while preserving true informed flow.

### Suggested thresholds
`min_volume_delta` → `0.075`, `min_price_move` → `0.005`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-768** `planned` — Exclude whale-cluster signals with priceΔ=0.0 or priceΔ<0.005 in markets with >5M baseline volume; require minimum 0.5% price impact to validate conviction.
- [ ] **TB-769** `planned` — Normalize volume delta as percentage of rolling 1-hour baseline; flag only when volΔ ≥5-10% of baseline (tiered by market liquidity tier) to distinguish signal from microstructure noise.
- [ ] **TB-770** `planned` — Add directional-bias filter: require >80/20 buy/sell ratio or sustained >3 minutes of unidirectional clustering before escalating to whale-cluster tier in low-price-movement contexts.
- [ ] **TB-771** `planned` — For far-dated or illiquid contracts (baseline <5M or expiry >6 months), require either minimum trade count >10 or sustained price move >3% before emitting any signal.
- [ ] **TB-772** `planned` — Recalibrate whale-cluster scoring function to weight price impact (50%) and directional volume skew (30%) more heavily than absolute volume delta (20%) in high-baseline-volume markets.

---

## 2026-04-07 — Advisor snapshot 221

### Summary
Whale-cluster tier is generating excessive false positives in high-baseline-volume markets (KXMARMAD-26-MICH) where volume spikes lack price impact. The detector conflates volume concentration with informed trading, missing that absolute deltas become meaningless without correlated price movement in deep-liquidity markets.

### Next step
Implement a mandatory price-impact gate for whale-cluster signals: require either spike_min_price_move ≥ 0.5% OR volume delta ≥ 5% of rolling 1h baseline (whichever is stricter). Exclude signals with zero price movement entirely.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-773** `planned` — For whale-cluster tier: require spike_min_price_move ≥ 0.5% OR (volume_delta_pct_of_1h_baseline ≥ 5.0%) to filter volume-only noise in high-conviction, high-baseline markets
- [ ] **TB-774** `planned` — Add market-context filter: suppress whale-cluster alerts on markets with baseline_daily_volume > 10M unless price_move ≥ 0.5% or volume_delta_pct ≥ 10%, since absolute volume deltas are poor quality signals in ultra-liquid markets
- [ ] **TB-775** `planned` — Exclude all signals where priceΔ = 0.0 from whale-cluster tier; require minimum price movement of 0.01 (1 bp) as a baseline floor, with 0.5% required for high-volume markets
- [ ] **TB-776** `planned` — For low-liquidity markets (baseline < 5M): require volume_delta_pct_of_baseline ≥ 5% OR sustained_directional_bias (>80/20 side ratio) to avoid microstructure noise
- [ ] **TB-777** `planned` — Replace absolute volume_delta thresholds with percentage-of-baseline model: normalize spikes against rolling 1h baseline to handle markets with 1000x+ baseline variance

---

## 2026-04-07 — Advisor snapshot 222

### Summary
The whale-cluster detector is generating false positives on high-conviction, high-baseline-volume markets (KXMARMAD-26-MICH) by triggering on volume spikes without corresponding price movement. Nearly all flagged signals show priceΔ=0.0 or <0.01 despite high scores, indicating volume concentration alone is insufficient signal quality.

### Next step
Implement a mandatory price-impact floor for whale-cluster alerts: require minimum priceΔ ≥0.5% OR volume delta ≥5-10% of baseline, whichever is stricter. This filters out liquidity-provision noise while preserving true informed-trading signals.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-778** `planned` — Add hard constraint: exclude whale-cluster signals when priceΔ = 0.0 unless volΔ exceeds 10% of market's 1-hour baseline volume
- [ ] **TB-779** `planned` — For markets with >10M daily baseline volume, require either priceΔ ≥0.5% OR order-imbalance ratio >70/30 directional skew to emit whale-cluster tier alerts
- [ ] **TB-780** `planned` — Normalize volume delta as percentage of baseline rather than absolute values; flag only when volΔ_pct >5-10% depending on market liquidity tier
- [ ] **TB-781** `planned` — For low-conviction or low-probability markets (yes <0.10), require sustained directional bias (>80/20 volume ratio) OR priceΔ ≥1.0% alongside whale-cluster volume signals
- [ ] **TB-782** `planned` — Filter out signals from zero-tick trades and quote-fragmentation patterns; require minimum trade count (e.g., 5+ distinct fills) or minimum executed size (5k+ shares) within cluster window

---

## 2026-04-07 — Advisor snapshot 223

### Summary
Predominantly whale-cluster false positives in high-liquidity, high-conviction markets (yes >0.95) with low price impact (often 0%) and small volume deltas relative to baseline, driven by noise from market makers and quote fragmentation.

### Next step
Require minimum price movement of 0.5% OR volume delta >5% of baseline for whale-cluster signals in high-liquidity markets.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-783** `planned` — Require min price move >0.005 (0.5%) or vol delta >5% baseline for whale-cluster tier
- [ ] **TB-784** `planned` — Raise min volume delta to 20k absolute in ultra-high prob markets (>0.95 yes)
- [ ] **TB-785** `planned` — Filter whale-cluster if priceΔ=0 and no sustained directional bias

---

## 2026-04-07 — Advisor snapshot 224

### Summary
The whale-cluster detector is generating overwhelming false positives on KXMARMAD-26-MICH (and similar high-conviction, high-liquidity markets) by triggering on tiny absolute volume deltas (7k–75k contracts) with zero or near-zero price impact. The detector conflates trade fragmentation and quote-level noise with informed whale activity.

### Next step
Require whale-cluster signals to meet BOTH a relative volume threshold (≥5% of baseline) AND an absolute price-impact floor (≥0.5% move) or minimum absolute volume (≥100k contracts). This eliminates low-conviction microstructure noise while preserving genuine directional accumulation.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-786** `planned` — For whale-cluster tier: require volume delta to exceed 5% of the 1h baseline volume before scoring. Absolute thresholds alone fail in high-liquidity markets.
- [ ] **TB-787** `planned` — Add a price-impact gate: exclude whale-cluster signals where priceΔ = 0.00 unless absolute volume delta exceeds 100k+ contracts, or require priceΔ ≥ 0.5% (50 bps) for all whale-cluster alerts.
- [ ] **TB-788** `planned` — For extreme-conviction markets (yes > 0.90 or price <0.05 / >0.95): require either (a) ≥1% price move or (b) ≥10% volume delta + ≥80/20 directional skew to suppress quote-spam false positives.
- [ ] **TB-789** `planned` — Add minimum absolute trade count or cumulative contract threshold (e.g., >10 trades or >5k contracts within window) to filter microstructure noise from market-maker quoting in ultra-liquid venues.
- [ ] **TB-790** `planned` — For far-dated or illiquid markets (e.g., 2031 expirations, <5M baseline volume): require sustained price movement (>3–5%) or >10 trade minimum before escalating to watch/alert tier.

---

## 2026-04-07 — Advisor snapshot 225

### Summary
False positives dominate in whale-cluster signals on high-conviction (yes>0.95 or <0.05), high-liquidity, or low-liquidity markets with minimal or no price movement despite volume spikes, often due to quote noise, market maker activity, or poor baseline normalization.

### Next step
Require minimum price move ≥0.5% OR volume delta ≥5% of baseline for all whale-cluster signals, with dynamic baseline adjustment by market liquidity and price extremes.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-791** `planned` — Filter whale-cluster in extreme price markets (>0.95 or <0.05) unless priceΔ ≥0.5% or volΔ >10% baseline
- [ ] **TB-792** `planned` — Raise min volume delta to 5% of 1h baseline in high-liquidity markets (>10M daily vol)
- [ ] **TB-793** `planned` — Require directional trade skew (>80/20) or multi-sig clusters in low-liquidity markets

---

## 2026-04-07 — Advisor snapshot 226

### Summary
The whale-cluster detector is generating excessive false positives on KXMARMAD-26-MICH (extreme-conviction market at >0.95 probability) by triggering on zero-price-impact volume clusters that lack market significance. All 19 labeled signals are noise despite high score/confidence, driven by quote-refresh mechanics and liquidity provision in illiquid extreme-price regimes.

### Next step
Enforce a hard price-impact floor for whale-cluster tier: require either minimum absolute price movement (±0.5%) OR volume delta ≥2% of baseline, whichever is stricter. This eliminates zero-tick trades while preserving signals with real market conviction.

### Suggested thresholds
`min_volume_delta` → `0.02`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-794** `planned` — Add hard filter: exclude whale-cluster signals where priceΔ=0.0 and volΔ <2% of market baseline volume, as these are mechanical quote activity without conviction.
- [ ] **TB-795** `planned` — For markets trading >0.95 or <0.05 probability: require minimum volume delta of 2-5% of baseline (scaled by baseline size) instead of absolute thresholds, since micro-moves in extreme markets are naturally noisy.
- [ ] **TB-796** `planned` — Introduce price-impact weighting into spike_score calculation: downweight or null signals where volume spike produces zero price dislocation, as they indicate liquidity provision rather than informed flow.
- [ ] **TB-797** `planned` — Require minimum consecutive trade count (e.g., ≥3 trades from distinct clusters with directional alignment) in extreme-conviction markets before triggering whale-cluster tier, not just temporal clustering.
- [ ] **TB-798** `planned` — For ultra-high-baseline markets (>10M daily delta): set spike_min_volume_delta floor at 1% of baseline or 50k contracts absolute, whichever is higher.

---

## 2026-04-07 — Advisor snapshot 227

### Summary
The whale-cluster detector is generating high-confidence false positives (score=8.0, yes≈0.99) in extreme-probability markets (>0.95 or <0.05) where volume spikes occur without meaningful price movement, driven by quote-refresh mechanics and liquidity provision rather than informed trading.

### Next step
Implement a price-impact filter: require minimum price_move ≥ 0.5% OR volume_delta ≥ 1-2% of baseline before triggering whale-cluster alerts, with stricter thresholds in extreme-probability regimes (>0.95 or <0.05 price).

### Suggested thresholds
`min_volume_delta` → `0.015`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-799** `planned` — Add conditional logic: in markets with price >0.95 or <0.05, require volume_delta to exceed 2% of baseline OR absolute_price_move ≥ 0.5% to reduce quote-spam false positives.
- [ ] **TB-800** `planned` — Normalize volume detection by baseline volume percentile rather than absolute delta—sub-1% baseline spikes in high-liquidity markets (>10M daily) should require either price impact or trade-count consistency to validate conviction.
- [ ] **TB-801** `planned` — Exclude whale-cluster signals when price_move is 0 or negligible (<0.01) across the spike window, as volume clustering without price dislocation typically indicates hedging or liquidity provision.
- [ ] **TB-802** `planned` — For ultra-high-baseline markets (>10M daily volume), raise the minimum volume delta threshold to 1-2% of baseline or require minimum absolute volume (e.g., >100k contracts) to filter micro-clustering noise.
- [ ] **TB-803** `planned` — Incorporate directional consistency check: require consecutive multi-signature trades from distinct wallet clusters showing aligned directional bias rather than fragmented quote patterns to distinguish informed flow from market-maker activity.

---

## 2026-04-07 — Advisor snapshot 228

### Summary
The whale-cluster detector is generating systematic false positives on KXMARMAD-26-MICH (extreme probability >0.95 market) by flagging volume clustering without price impact, confusing quote-refresh mechanics and market-maker noise for informational flow.

### Next step
Implement a conditional rule: for markets with prices >0.95 or <0.05, require EITHER minimum price move ≥0.5% OR volume delta ≥1% of rolling 24h baseline before triggering whale-cluster signals, regardless of clustering score.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-804** `planned` — Add price-regime filter: disable or heavily suppress whale-cluster alerts when price ∈ (0.05, 0.95) is false (i.e., at extremes), unless priceΔ ≥ 0.5% or volΔ ≥ 1% of baseline
- [ ] **TB-805** `planned` — Normalize volume delta calculation to account for baseline liquidity: require volΔ as percentage of recent baseline (e.g., 24h rolling sum) rather than absolute delta, especially for ultra-liquid markets (baseline >10M daily volume)
- [ ] **TB-806** `planned` — Add price-impact weighting to whale-cluster scoring: trades that move price <0.1% despite volume clustering should decay the score by 50%+ or require directional consistency with prior trend to remain actionable
- [ ] **TB-807** `planned` — For far-dated or low-liquidity markets (baseline <5M), raise minimum trade count threshold: require ≥5 distinct transactions in the cluster window rather than fragmented quotes to avoid order-book microstructure noise
- [ ] **TB-808** `planned` — Implement baseline-relative volume thresholds: set spike_min_volume_delta dynamically as 1–5% of the prior 24h baseline, scaled by market conviction (price extremity) and absolute daily volume

---

## 2026-04-07 — Advisor snapshot 229

### Summary
The detector is generating high-confidence false positives on KXMARMAD-26-MICH (extreme probability market >0.95) by triggering on quote-level noise and trivial volume clustering with zero or minimal price impact. All 17 signals on this market are labeled noise despite high score/confidence, indicating the detector conflates liquidity provision with informed flow.

### Next step
Implement price-impact weighting: require minimum absolute price move (≥0.5%) OR volume delta exceeding 1-2% of rolling baseline for whale-cluster tier signals. For markets with prices >0.95 or <0.05, apply stricter thresholds independent of score.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-809** `planned` — For whale-cluster signals in markets with probability >0.95 or <0.05: require priceΔ ≥ 0.5% OR volΔ ≥ 1% of 24h baseline before emitting; otherwise suppress or deprioritize.
- [ ] **TB-810** `planned` — Exclude whale-cluster signals where volΔ results in zero or <0.01 price movement; add price-impact filtering to distinguish liquidity provision from conviction.
- [ ] **TB-811** `planned` — For ultra-high-baseline markets (>10M daily volume), raise minimum volume delta threshold to absolute 50k+ contracts or 1-2% of baseline, not relative clustering alone.
- [ ] **TB-812** `planned` — For watch/lower-tier signals in illiquid or far-dated markets: require minimum trade count (>5-10 distinct trades) or sustained multi-candle directional bias, not single-spike volume events.
- [ ] **TB-813** `planned` — Add market-regime detection: suppress or re-weight whale-cluster signals on locked/extreme-pricing markets where quote-refresh mechanics naturally cluster volume without conviction.

---

## 2026-04-07 — Advisor snapshot 230

### Summary
All recent whale-cluster signals are false positives labeled as noise/unclear/high in ultra-high-conviction markets (yes=0.99, prices >0.95), featuring high scores but no price movement (mostly priceΔ=0.0) and volume deltas that are trivial relative to high baselines.

### Next step
Require minimum 0.5% price move OR volume delta >1% of 24h baseline for whale-cluster alerts in markets with implied probability >0.95.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-814** `planned` — Raise spike_min_price_move to 0.005 for markets with yes >=0.95
- [ ] **TB-815** `planned` — Dynamically adjust spike_min_volume_delta to 1% of market's 24h baseline volume
- [ ] **TB-816** `planned` — Require directional trade-side asymmetry or order book depletion alongside volume spikes

---

## 2026-04-07 — Advisor snapshot 231

### Summary
Whale-cluster detector is firing on stationary-price, high-conviction markets (>0.95 probability) with large volume deltas but zero price impact. All 14 recent signals are labeled noise/unclear/no, indicating the detector conflates liquidity provision and mechanical order execution with informed positioning.

### Next step
Implement a conjunction gate: require EITHER minimum 0.5% price movement OR volume delta exceeding 1-2% of rolling baseline volume to trigger whale-cluster alerts in markets with prices >0.90 or <0.10. This preserves signal on genuine informed flow while muting quote-clustering noise at pinned extremes.

### Suggested thresholds
`min_volume_delta` → `0.01`, `min_price_move` → `0.005`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-817** `planned` — Add price-move gate: require priceΔ ≥ 0.005 (0.5%) for whale-cluster tier, or suppress signal entirely if priceΔ = 0.0 in markets with implied probability >0.90
- [ ] **TB-818** `planned` — Implement baseline-relative volume threshold: reject whale-cluster signals unless volΔ > 1% of rolling 24h baseline volume, especially for markets with baseline >5M
- [ ] **TB-819** `planned` — Deprioritize or exclude ultra-extreme markets: reduce spike_score_threshold by 3–5 points (or set separate rule) for markets at >0.95 or <0.05 probability where directional saturation is structural
- [ ] **TB-820** `planned` — Add quote-vs-trade asymmetry check: suppress whale-cluster alerts when quote volume vastly exceeds executed trade volume at identical prices
- [ ] **TB-821** `planned` — Lower spike_score_threshold for whale-cluster tier only when price movement is present; keep original threshold only when price move ≥0.5% is observed

---

## 2026-04-07 — Advisor snapshot 232

### Summary
Whale-cluster detector is generating false positives on extreme-probability markets (>95% yes) where large volume spikes occur with zero price movement. The market structure (pinned prices, thin liquidity regions, mechanical flow) absorbs directional volume without repricing, making pure volume clustering non-informative.

### Next step
Implement a price-movement gate for whale-cluster signals in extreme-probability markets (yes > 0.95 or yes < 0.05): require either ≥0.5% price movement OR order-book depletion before flagging. This single rule eliminates ~19 false positives in the KXMARMAD-26-MICH set while preserving the one genuine signal (volΔ=35000 with extreme bid-ask spread context).

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-822** `planned` — Add market-state conditional logic: for implied probabilities >95% or <5%, require spike_min_price_move ≥ 0.005 (0.5%) OR alternative signal (e.g., order-book impact, bid-ask tightening) before emitting whale-cluster tier alerts.
- [ ] **TB-823** `planned` — Introduce baseline-volume normalization: require volume delta to exceed 1% of 24h baseline volume OR represent >0.1% notional trade size per whale participant to filter mechanical execution.
- [ ] **TB-824** `planned` — Implement temporal persistence requirement: extend whale-cluster detection window from 120s to 300s (5min) or require price-level diversity across multiple ticks, since coordinated activity at single price point in saturated markets is typically non-informative.

---

## 2026-04-07 — Advisor snapshot 233

### Summary
The whale-cluster detector is generating excessive false positives on KXMARMAD-26-MICH (yes=0.99, extreme probability market) by flagging large volume deltas without accompanying price movement. In saturated-probability markets, consensus pricing absorbs directional volume mechanically, making pure volume clustering non-informative.

### Next step
Implement a price-movement gate for markets with implied probabilities >95% or <5%: require minimum 0.5% price move OR spike must represent >1% of 24h baseline volume to qualify as actionable signal. This single rule eliminates ~95% of observed false positives.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-825** `planned` — For whale-cluster tier: add conditional logic—if market yes-price >0.95 or <0.05, enforce spike_min_price_move ≥0.005 (0.5%) OR require volume delta >1% of 24h baseline volume before emitting signal.
- [ ] **TB-826** `planned` — Increase whale-cluster minimum concentration threshold from 37 to 100+ whales when baseline daily volume exceeds 15M, and apply this stricter gate especially to extreme-probability markets.
- [ ] **TB-827** `planned` — Add elasticity check: if price delta remains 0.0 across all detected whale cluster activity, require either (a) order-book depletion metric, (b) multi-price-level trades, or (c) sustained clustering >180s instead of 120s to confirm informed flow vs. mechanical execution.
- [ ] **TB-828** `planned` — For small-market sports contracts (tier=watch), raise spike_min_price_move from 0% to 0.01 (1.0%) to filter stationary-price volume spikes that lack price discovery.

---

## 2026-04-07 — Advisor snapshot 234

### Summary
The whale-cluster detector is generating systematic false positives on KXMARMAD-26-MICH (yes=0.99) by flagging large volume deltas with zero price movement. Extreme-probability markets exhibit price inelasticity, making volume clustering alone non-predictive without accompanying repricing.

### Next step
Implement a price-movement gate for markets with extreme implied probabilities (>95% or <5%): require minimum 0.5% price delta OR reject the spike entirely. This single rule eliminates ~90% of observed false positives while preserving the one genuine whale-coordination signal.

### Suggested thresholds
`min_volume_delta` → `1.3`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-829** `planned` — Add conditional logic: if yes_price > 0.95 or yes_price < 0.05, require spike_min_price_move >= 0.005 (0.5%) for whale-cluster tier, regardless of volume_delta magnitude.
- [ ] **TB-830** `planned` — Require minimum notional trade size >0.1% of 24h baseline volume per participating whale, or exclude single-price-level clustering from whale-cluster alerts in extreme-probability regimes.
- [ ] **TB-831** `planned` — For non-extreme markets, raise spike_min_volume_delta multiplier from 1.1x to 1.3x and require minimum 5+ distinct trades in the spike window to filter quote-driven noise on small sports contracts.
- [ ] **TB-832** `planned` — For whale-cluster detections on markets with bid-ask spread >0.98, lower p-value threshold to distinguish liquidity provision from coordination (keep the one genuine signal at volΔ=35000).
- [ ] **TB-833** `planned` — Replace 120s clustering window with requirement for multi-minute persistence (e.g., 5min) or multi-price-level trades to avoid mechanical stationary-price coordination.

---

## 2026-04-07 — Advisor snapshot 235

### Summary
The detector is generating high false-positive rates on whale-cluster alerts in extreme-probability markets (>95% or <5%) where large volume deltas occur with zero price impact. These are mechanical liquidity flows, not informational signals.

### Next step
Implement a market-context filter: require minimum 0.5% price movement to trigger whale-cluster alerts when implied probability exceeds 0.95 or is below 0.05. This single rule eliminates ~90% of false positives while preserving the one genuine signal (35k volume delta with coordinated activity).

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-834** `planned` — Add conditional logic: if yes_price > 0.95 OR yes_price < 0.05, enforce spike_min_price_move >= 0.005 (0.5%) for whale-cluster tier alerts; otherwise use standard 0.0% threshold.
- [ ] **TB-835** `planned` — Raise minimum whale-cluster concentration threshold from 37 to 100+ whales for markets with >15M baseline daily volume, to filter statistical noise in high-liquidity venues.
- [ ] **TB-836** `planned` — For watch-tier alerts on small markets (baseline volume <5M), increase volume delta multiplier sensitivity requirement from 1.1x to 1.3x+ and require minimum trade count of 5+ distinct trades within clustering window.
- [ ] **TB-837** `planned` — Add price-elasticity check: suppress whale-cluster alerts if volume delta >20k but price impact remains <0.1%, indicating one-sided mechanical activity rather than informed flow.
- [ ] **TB-838** `planned` — Require multi-price-level confirmation for whale-cluster alerts: volume must span at least 2 distinct price levels or demonstrate 5+ minute persistence (not 120s) to qualify as signal-worthy.

---

## 2026-04-07 — Advisor snapshot 236

### Summary
Whale-cluster detector is triggering heavily on extreme-probability markets (>95% yes) with large volume deltas but zero price movement, generating 15+ false positives. Volume clustering alone at pinned prices is mechanical liquidity provision, not informational flow.

### Next step
Require minimum price movement (≥0.5%) concurrent with whale-cluster detection on markets with implied probability >95% or <5%, or filter out whale-cluster alerts entirely when priceΔ=0.0 and baseline probability is extreme.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-839** `planned` — Add conditional rule: if yes_price > 0.95 or yes_price < 0.05, require spike_min_price_move ≥ 0.005 (0.5%) to trigger whale-cluster tier alerts, regardless of volume delta or score
- [ ] **TB-840** `planned` — Implement liquidity-relative volume filtering: exclude whale-cluster signals where volΔ < 0.1% of 24h baseline volume, or require minimum 100+ whales (not 37) for markets with >15M baseline daily volume
- [ ] **TB-841** `planned` — Add price-elasticity check: suppress whale-cluster alerts when priceΔ = 0.0 and market baseline probability is extreme (>95% or <5%), as coordinated volume at locked prices is non-predictive
- [ ] **TB-842** `planned` — Raise minimum price move threshold from 0% to 0.5-1.0% for watch-tier sports contracts (low absolute volume markets) to filter quote-driven noise
- [ ] **TB-843** `planned` — For whale-cluster tier specifically: require either (a) ≥0.5% price movement, OR (b) multi-price-level trades within 120s window, OR (c) >40 whale concentration—not volume delta alone

---

## 2026-04-07 — Advisor snapshot 237

### Summary
Whale-cluster detector is generating high false-positive rates on extreme-probability markets (>95% or <5%) where large volume spikes occur without corresponding price movement, indicating mechanical liquidity provision rather than informed trading.

### Next step
Introduce probability-aware price-movement requirement: for markets with implied probability >0.95 or <0.05, require minimum price move of ≥0.5% to trigger whale-cluster alerts; for all other markets, require ≥0.1% price move alongside volume clustering.

### Suggested thresholds
`min_price_move` → `0.001`

### Recommendations

- [ ] **TB-844** `planned` — Add conditional min_price_move rule: if market probability ∈ (0.95, 1.0) ∪ (0.0, 0.05), enforce spike_min_price_move ≥ 0.005 (0.5%); else enforce ≥ 0.001 (0.1%)
- [ ] **TB-845** `planned` — For whale-cluster tier specifically, require either (a) price impact ≥ threshold OR (b) multi-level trading activity (trades at 2+ distinct price points within window), to exclude single-price mechanical activity
- [ ] **TB-846** `planned` — Raise minimum cluster size threshold from 37 to 60+ whales for markets with baseline daily volume >15M and probability >0.90, reducing sensitivity to routine position management
- [ ] **TB-847** `planned` — Filter whale-cluster alerts where volume delta <0.5% of baseline 24h volume in extreme-probability markets, as micro-trades in tail regions generate statistical noise
- [ ] **TB-848** `planned` — For 'watch' tier (lower severity), increase volume delta multiplier from 1.1x to 1.3x+ and require minimum 5+ trades in recent flow window to reduce quote-driven false positives

---

## 2026-04-07 — Advisor snapshot 238

### Summary
The detector is generating massive false positives on whale-cluster signals in extreme-probability markets (>95% yes) where large volumes produce zero price movement. These are routine liquidity/rebalancing trades, not informational flow.

### Next step
Require minimum 0.5% price movement concurrent with whale-cluster activity in markets with implied probability >95% or <5%, OR filter out whale-cluster spikes entirely when priceΔ=0.0 and conviction is extreme.

### Suggested thresholds
`min_volume_delta` → `0.01`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-849** `planned` — Add conviction-gated price-move requirement: if yes_prob > 0.95 or < 0.05, require spike_min_price_move ≥ 0.005 (0.5%), else require ≥ 0.001 (0.1%)
- [ ] **TB-850** `planned` — Implement liquidity-adjusted volume thresholds: require volume_delta to be ≥ 1% of baseline daily volume in extreme-probability markets before triggering whale-cluster tier
- [ ] **TB-851** `planned` — Exclude zero-impact whale-cluster signals: filter out spikes where priceΔ = 0.0 and both directional sides show no counter-trading (one-way flow = mechanical, not informational)
- [ ] **TB-852** `planned` — Raise minimum whale-cluster size for high-baseline markets: increase from 37 to 100+ whales for markets with >15M baseline daily volume
- [ ] **TB-853** `planned` — Require multi-minute persistence on extreme-conviction markets: extend clustering window from 120s to 300s+ on yes_prob >0.95 to distinguish noise from sustained informed activity

---

## 2026-04-07 — Advisor snapshot 239

### Summary
Whale-cluster detector is generating false positives on extreme-probability markets (>95% or <5%) where large volumes produce zero price impact, indicating rebalancing noise rather than informed flow. Price movement is the critical missing filter.

### Next step
Implement market-regime-aware price-impact requirement: require minimum 0.5% price movement for whale-cluster signals in markets with implied probability >95% or <5%, and require volume delta ≥1% of baseline in these extreme-conviction regimes.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-854** `planned` — Add conditional rule: if (yes_price > 0.95 OR yes_price < 0.05) AND priceΔ == 0, reject whale-cluster signal regardless of volume or score
- [ ] **TB-855** `planned` — Introduce baseline-relative volume filter: require volΔ ≥ max(1% of baseline, 50k absolute) for whale-cluster detection in high-conviction markets
- [ ] **TB-856** `planned` — For non-extreme markets, raise minimum price move threshold from 0% to 0.5-1.0% to enforce price discovery requirement before tier-1 alerts
- [ ] **TB-857** `planned` — Add liquidity-adjusted scoring: discount whale-cluster scores by (volΔ / baseline_volume) ratio; flag only when ratio >0.01 (1%) or price moves ≥0.5%
- [ ] **TB-858** `planned` — Increase minimum whale-cluster size threshold from 37 to 75+ for markets with >15M baseline volume to reduce statistical noise in liquid pools

---

## 2026-04-07 — Advisor snapshot 240

### Summary
Whale-cluster detector is generating false positives on extreme-probability markets (>95% yes/no) where large volume spikes occur with zero price movement, indicating rebalancing or quote noise rather than informed flow. The detector conflates statistical significance of absolute volume with predictive signal value.

### Next step
Require minimum price movement (≥0.5%) concurrent with whale-cluster volume spikes on markets with implied probabilities >95% or <5%, since consensus pricing in extreme regimes absorbs large directional volume without repricing.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-859** `planned` — Add market-regime filter: for markets with yes-price >0.95 or <0.05, enforce spike_min_price_move ≥0.005 (0.5%) or require sustained directional imbalance (>80/20 side split over 5+ minutes) to trigger whale-cluster alerts.
- [ ] **TB-860** `planned` — Introduce liquidity-adjusted volume thresholds: require volume_delta ≥ max(5% of baseline_volume, 0.5x baseline_daily_volume) for whale-cluster signals, and raise minimum cluster size to 100+ accounts in high-liquidity markets (>15M baseline).
- [ ] **TB-861** `planned` — Add price-impact requirement for extreme-conviction markets: exclude whale-cluster flags where priceΔ=0 across all timeframes and yes-price ∉ [0.25, 0.75], as these represent routine position management without signal value.
- [ ] **TB-862** `planned` — Filter quote-only noise: require minimum trade-count (5+ executed trades) or bid-ask spread normalization before triggering watch/whale-cluster tiers on micro-volume spikes in thin markets.

---

## 2026-04-07 — Advisor snapshot 241

### Summary
Whale-cluster detector is firing on extreme-conviction markets (>95% yes) with large volume deltas but zero price movement, generating systematic false positives. The tier is conflating quote accumulation and rebalancing with informed flow.

### Next step
Enforce a universal minimum price movement gate (≥0.5%) for whale-cluster signals, with additional context-specific filters for extreme probabilities (>95% or <5%) and thin baselines.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-863** `planned` — Add mandatory price_move ≥ 0.5% correlation check for all whale-cluster tier alerts; reject signals where priceΔ = 0.0 regardless of volume or score.
- [ ] **TB-864** `planned` — For markets with yes-probability >0.95 or <0.05, raise the effective spike_min_volume_delta threshold to 0.5% of baseline or require sustained directional imbalance (>80/20 side split over 5+ minutes) instead of raw volume.
- [ ] **TB-865** `planned` — Implement liquidity-adjustment factor: scale volume_delta threshold inversely to baseline volume; for baselines <1M, require volΔ ≥ 5-10% of baseline; for baselines >15M, allow tighter absolute thresholds but reject micro-trades (<0.1% of baseline).
- [ ] **TB-866** `planned` — For ultra-low-probability markets (<2% yes), require minimum 1 basis point price movement before flagging whale-cluster, as true informed activity on thin conviction should move price even with small absolute volumes.
- [ ] **TB-867** `planned` — Exclude whale-cluster spikes where trade count is low or per-trade sizes are uniform/mechanical (suggesting rebalancing), even if volume delta exceeds thresholds.

---

## 2026-04-07 — Advisor snapshot 242

### Summary
Whale-cluster detector is generating false positives on high-conviction markets (>95% yes probability) where large volume deltas occur with zero price movement, suggesting quote noise and rebalancing rather than informed flow.

### Next step
Require concurrent minimum price movement (≥0.5%) OR enforce market-context gates: exclude whale-cluster signals when price is static AND market probability is extreme (>95% or <5%) AND volume delta is <0.5% of baseline.

### Suggested thresholds
`min_volume_delta` → `0.005`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-868** `planned` — Add mandatory price-movement gate: spike_min_price_move ≥ 0.5% for whale-cluster tier in markets with yes-probability >0.95 or <0.05
- [ ] **TB-869** `planned` — Implement baseline-volume ratio filter: exclude whale-cluster signals when volΔ < 0.5% of 1h baseline volume in extreme-conviction markets (>95%)
- [ ] **TB-870** `planned` — Raise minimum cluster size or absolute volume threshold for high-baseline markets: require volΔ ≥ 0.1% of daily baseline or ≥100 whale accounts (vs. 37) when baseline >15M
- [ ] **TB-871** `planned` — Add execution-confirmation check: require minimum trade count (5+) or price-level crossing to distinguish quote noise from real informed activity
- [ ] **TB-872** `planned` — Lower whale-cluster score_threshold or tier on ultra-low-probability markets (<2%): require concurrent price movement (>0.5%) before flagging, as thin order books generate mechanical spikes

---

## 2026-04-07 — Advisor snapshot 243

### Summary
Whale-cluster tier is generating systematic false positives on high-conviction markets (>95% implied probability) where large volume deltas produce zero price impact, indicating mechanical rebalancing rather than informed flow.

### Next step
Implement a mandatory price-movement gate for whale-cluster signals: require minimum price move of ±0.5% OR sustained directional imbalance (>80/20 split) concurrent with volume spike, regardless of score. This filters quote noise while preserving genuine informed activity.

### Suggested thresholds
`min_volume_delta` → `0.01`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-873** `planned` — Add liquidity-adjusted volume threshold: require volΔ to exceed 1% of market baseline volume (or 0.5% for ultra-liquid markets >15M baseline) before whale-cluster tier qualifies, to exclude mechanical noise in deep-liquidity pools.
- [ ] **TB-874** `planned` — Implement conviction-zone filter: for markets with implied probability >95% or <5%, enforce minimum ±0.5% price movement or 5+ minute directional imbalance (>80/20) to trigger whale-cluster signals, as quote clustering in tail zones is primarily rebalancing.
- [ ] **TB-875** `planned` — Raise minimum cluster size threshold from 37 to 100+ whales for markets with >15M baseline daily volume, reducing sensitivity on high-liquidity venues where nominal whale counts are statistically inflated.
- [ ] **TB-876** `planned` — Add price-elasticity requirement for ultra-low conviction markets (<2%): require ≥1bp price movement before flagging whale clusters, since true informed activity on thin markets should move price measurably.
- [ ] **TB-877** `planned` — Increase volume delta multiplier threshold from 1.1x to 1.3x+ and require minimum trade count (5+ trades in recent window) for watch tier to reduce quote-driven false positives.

---

## 2026-04-07 — Advisor snapshot 244

### Summary
All 20 false positives are whale-cluster signals (score=8.0) with zero price movement on high-conviction markets (KXMARMAD-26-MICH mostly at yes=0.99). The detector is triggering on pure quote activity and mechanical rebalancing without price impact.

### Next step
Require concurrent price movement (≥0.5%) as a mandatory confirmation gate for whale-cluster signals, especially in markets with extreme probabilities (>95% or <5%). This single rule eliminates all 20 false positives while preserving signals where whales actually move price.

### Suggested thresholds
`min_volume_delta` → `0.005`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-878** `planned` — Add hard constraint: whale-cluster tier signals require priceΔ ≥ 0.5% OR enforce that priceΔ=0.0 automatically downgrades/suppresses the signal regardless of volume delta or cluster size.
- [ ] **TB-879** `planned` — For whale-cluster in markets with yes >0.95 or <0.05, raise minimum volume delta threshold to ≥0.5% of baseline (not ≥1% of absolute volume) and require price movement ≥0.5% to confirm.
- [ ] **TB-880** `planned` — Reduce whale-cluster score weighting when price is completely static; cap score at 3.0–4.0 (vs current 8.0) for zero-price-impact signals, making them advisory/watch-tier only rather than high-confidence alerts.
- [ ] **TB-881** `planned` — For ultra-high-conviction markets (>95% implied), require minimum trade count (5+ trades) and directional imbalance confirmation (>80/20 side split sustained >5min) before flagging, to distinguish informed flow from rebalancing.
- [ ] **TB-882** `planned` — Implement liquidity-adjusted volume delta: volume_delta must exceed max(1% of baseline, 0.5% of baseline) depending on baseline size; exclude spikes <0.1% of baseline in markets >15M daily volume.

---

## 2026-04-07 — Advisor snapshot 245

### Summary
Whale-cluster tier is generating systematic false positives on KXMARMAD-26-MICH and similar markets due to zero price impact despite large volume deltas. The detector flags quote clustering and rebalancing activity as signal without requiring concurrent price movement or baseline-relative volume thresholds.

### Next step
Require minimum price movement (≥0.5%) OR minimum volume delta as percentage of baseline (≥1%) as a mandatory AND gate for whale-cluster signals, especially in extreme-conviction markets (price >0.95 or <0.05).

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-883** `planned` — Add price-movement correlation gate: suppress whale-cluster signals when priceΔ=0.0 across all timeframes, or require priceΔ ≥0.5% to confirm signal validity.
- [ ] **TB-884** `planned` — Implement baseline-relative volume filter: flag whale-cluster only when volΔ ≥ max(1% of 1h baseline volume, 25000 absolute delta) to filter mechanical quote noise in deep-liquidity markets.
- [ ] **TB-885** `planned` — Adjust conviction-zone logic: for markets with implied probability >0.95 or <0.05, enforce stricter gates—require either price move ≥0.5% or directional side imbalance >80/20 sustained over 5+ minutes before emitting tier-1 alert.
- [ ] **TB-886** `planned` — Lower whale-cluster weighting in score calculation when baseline volume >10M, since absolute volume significance becomes misleading relative to pool depth.
- [ ] **TB-887** `planned` — For ultra-low probability markets (<2%), require minimum 1bp price elasticity before triggering, as true informed flow typically moves price even on small absolute volumes.

---

## 2026-04-07 — Advisor snapshot 246

### Summary
All 20 signals from KXMARMAD-26 are whale-cluster false positives with zero price movement (priceΔ=0.0) despite high volume deltas and perfect confidence scores. The detector is triggering on mechanical quote activity and one-sided order accumulation in extreme-probability markets without any price discovery.

### Next step
Require minimum price movement (≥0.5%) as a mandatory gate for whale-cluster detection in all markets, especially those with prices >0.95 or <0.05. This single rule eliminates all 20 false positives while preserving informed signal detection.

### Suggested thresholds
`min_volume_delta` → `0.005`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-888** `planned` — Add hard constraint: whale-cluster signals must include priceΔ ≥0.5% (or ≥1.0% for extreme-probability markets >98% or <2%) to filter mechanical quote activity
- [ ] **TB-889** `planned` — Implement volume-delta scaling by baseline: require volΔ ≥0.5% of 24h baseline for markets with baseline >10M, and ≥1% for markets with baseline <1M, to reduce false positives on pure quote clustering
- [ ] **TB-890** `planned` — Gate whale-cluster on directional conviction: reject signals where all flow concentrates on a single side with zero slippage; require either mixed directionality (≥20/80 side split) or price movement to validate informed positioning
- [ ] **TB-891** `planned` — For extreme-probability markets (>95% or <5%), raise spike_min_price_move requirement from detector baseline to ≥0.5-1.0% and enforce that volume anomalies correlate with realized volatility to avoid rebalancing noise

---

## 2026-04-07 — Advisor snapshot 247

### Summary
False positives cluster around extreme-probability markets and volume spikes decoupled from meaningful price movement. The detector is triggering on liquidity-seeking behavior and technical noise rather than informative flow.

### Next step
Implement conditional thresholds based on market probability regime and require volume-price coherence: high-conviction markets (>90% or <10%) need 15x+ volume multipliers; low-conviction markets (<5%) need 2.5%+ price moves or directional agreement; short-duration markets need >0.5% price moves to validate volume spikes.

### Suggested thresholds
`min_price_move` → `0.025`

### Recommendations

- [ ] **TB-892** `planned` — For markets with yes probability >90% or <10%, increase volume delta multiplier threshold to 15x baseline to filter liquidity clustering at consensus prices
- [ ] **TB-893** `planned` — For markets with yes probability <5%, enforce minimum 2.5% price move requirement OR require directional agreement between volume and price trend before emitting spike alerts
- [ ] **TB-894** `planned` — For short-duration markets (15m windows), require minimum 0.5-3% price move accompanying any volume spike; reject 1000x+ volume multiples without corresponding price impact as liquidity noise

---

## 2026-04-07 — Advisor snapshot 248

### Summary
High false-positive rate in whale-cluster and watch-tier detections on illiquid/extreme-probability markets where large volume spikes occur without meaningful price impact, indicating mechanical order-book activity rather than informed flow.

### Next step
Implement conditional price-move requirements: require minimum 0.5–2.5% price correlation for whale-cluster signals on markets with baseline volume <5M or probability extremes (>90%/<10%), and 2–3% for watch-tier on short-duration instruments. Decouple volume-only signals from true spike detection.

### Suggested thresholds
`min_price_move` → `0.015`

### Recommendations

- [ ] **TB-895** `planned` — For whale-cluster tier on low-liquidity markets (baseline vol <5M): require priceΔ ≥0.005 (0.5%) OR asymmetric execution prices (not uniform ladder fills)
- [ ] **TB-896** `planned` — For notable/watch tiers on extreme-probability markets (yes >0.90 or <0.10): increase volume-delta multiplier threshold from 10x to 15x baseline to filter consensus-price liquidity seeking
- [ ] **TB-897** `planned` — For watch-tier on short-duration markets (15m): enforce priceΔ ≥0.02–0.03 (2–3%) when volΔ multiplier exceeds 1000x, or suppress alert if priceΔ ≈0.0
- [ ] **TB-898** `planned` — For low-conviction markets (implied probability <5%): raise min_price_move from 0.01 to 0.025 (2.5%) and require directional agreement between volume delta sign and price delta sign

---

## 2026-04-07 — Advisor snapshot 249

### Summary
Whale-cluster and watch-tier alerts are firing on volume spikes without corresponding price movement, particularly in illiquid and extreme-probability markets where large volumes represent normal market-making rather than informative flow.

### Next step
Enforce a mandatory price-movement floor (≥0.5% for whale-cluster on illiquid markets, ≥2.5% for low-conviction tail markets) correlated with volume delta, and apply dynamic volume-delta multipliers based on baseline liquidity and probability extremity rather than fixed scoring.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-899** `planned` — Require priceΔ ≥ 0.5% alongside volΔ for whale-cluster tier signals on markets with baseline volume <5M or tail probability (<5% or >95%); suppress signals with priceΔ = 0.0.
- [ ] **TB-900** `planned` — Increase volume-delta multiplier threshold from 10x to 15x for markets at consensus extremes (>90% or <10% implied probability) to filter liquidity-seeking activity that naturally congregates.
- [ ] **TB-901** `planned` — For watch-tier and short-duration markets (15m), require minimum priceΔ ≥ 2.5% to accompany 1000x+ volume multiples; suppress alerts with priceΔ = 0.0.
- [ ] **TB-902** `planned` — For low-conviction markets (sub-5% implied probability), increase minimum price-move threshold from 1.0% to 2.5% or require directional agreement between volume and price trend before emitting signal.
- [ ] **TB-903** `planned` — Add a liquidity-adjusted sensitivity gate: if baseline_volume < 5M or market_probability in [0.01, 0.05] ∪ [0.95, 0.99], require priceΔ correlation before scoring spike as actionable.

---

## 2026-04-07 — Advisor snapshot 250

### Summary
Whale-cluster detector is generating false positives on low-liquidity, low-conviction markets by triggering on large absolute volumes without price impact or sustained directional flow. Most noise cases show priceΔ=0.0 or <0.5%, indicating mechanical execution rather than information flow.

### Next step
Require minimum price movement (≥0.5%) correlation with volume spikes for whale-cluster tier on illiquid markets, and increase baseline volume multiplier thresholds (250x+) for markets below $10M daily volume to filter routine block trades.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-904** `planned` — Add mandatory price-move floor of ≥0.5% for whale-cluster signals on markets with <$10M daily volume or implied probability <10% or >90%.
- [ ] **TB-905** `planned` — Increase whale-cluster baseline multiplier threshold from 194.6x to 250x+ for low-liquidity markets, and enforce notional per-order minimum of $5,000+ to filter single mechanical trades.
- [ ] **TB-906** `planned` — For watch-tier alerts on short-duration markets (15m), require ≥2-3% price move to accompany 1000x+ volume multiples; suppress alerts with priceΔ=0.0.
- [ ] **TB-907** `planned` — Raise minimum price move threshold for sub-5% implied probability markets from 1.0% to 2.5%, or require directional agreement between volume trend and price trend.

---

## 2026-04-07 — Advisor snapshot 251

### Summary
Whale-cluster and notable tiers are generating excessive false positives on low-liquidity markets (sub-$10M daily volume, extreme skew >90% or <10% probability) where large volume deltas occur without meaningful price impact. Volume-only detection is triggering on routine block trades and market-making activity rather than informative flow.

### Next step
Require minimum price-move correlation (≥0.5%) for whale-cluster alerts on illiquid markets, and raise volume-delta multiplier thresholds for extreme-skew markets (>90% or <10% probability) from current baselines to 250x+ to filter mechanical execution.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-908** `planned` — For whale-cluster tier on markets with baseline volume <$10M or daily volume <5M: require priceΔ ≥0.5% OR asymmetric order-level pricing (multi-tick execution) to emit signal; pure volume spikes at uniform price levels are noise.
- [ ] **TB-909** `planned` — For markets with implied probability >90% or <10%: increase volume-delta multiplier threshold to 250x baseline (from 194.6x) and require minimum absolute notional trade size >$5,000 per order to filter liquidity-seeking congregation.
- [ ] **TB-910** `planned` — For notable tier on sub-5% conviction markets: raise minimum priceΔ threshold from 1.0% to 2.5%, or require quote-to-trade conversion >0.8 ratio plus ≥20 executed trades before flagging.
- [ ] **TB-911** `planned` — For short-duration markets (15m candles): require priceΔ ≥0.5-1.0% to accompany volume spikes >1000x multiplier; unexecuted quotes and mechanical rebalancing trigger false watch-tier alerts.
- [ ] **TB-912** `planned` — Lower volume-delta sensitivity for baseline <1 absolute volume: require minimum 20+ trade count before notable classification, or apply absolute volume thresholds rather than ratio-based multipliers.

---

## 2026-04-07 — Advisor snapshot 252

### Summary
whale-cluster tier is generating systematic false positives on KXMARMAD-26-CONN and similar markets: high volume concentration without price impact is being flagged as signal-worthy despite analyst consensus that zero price movement indicates mechanical execution, not informed flow.

### Next step
Require non-zero price movement (≥0.5%) OR price-impact correlation as a mandatory gate before whale-cluster signals qualify, rather than relying on volume clustering and score alone.

### Suggested thresholds
`min_volume_delta` → `5000000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-913** `planned` — Add hard filter: reject whale-cluster signals when priceΔ = 0.0 unless volume delta exceeds 5% of baseline daily delta AND whale concentration exceeds 30 accounts in 120s window
- [ ] **TB-914** `planned` — Introduce market-depth adjustment: for markets with baseline daily delta >4M, require minimum 0.5% price movement or sustained multi-tick directional pressure to emit whale-cluster alerts
- [ ] **TB-915** `planned` — Implement order-pattern discrimination: flag identical trade sizes executing at identical prices with zero impact as 'mechanical' and suppress; require asymmetric order sizes or multi-price participation for signal qualification
- [ ] **TB-916** `planned` — Lower spike_score_threshold for whale-cluster tier from 8.0 to require additional confirmation signal (price movement OR directional flow asymmetry) before emission

---

## 2026-04-07 — Advisor snapshot 253

### Summary
Whale-cluster detector is triggering heavily on zero-price-impact volume spikes in low-conviction markets, flagging mechanical/liquidity-driven execution as informed flow. Nearly all false positives share priceΔ=0.0 with yes-probability <0.1, indicating noise rather than directional conviction.

### Next step
Require non-zero price impact (≥0.5%) OR minimum volume delta as % of baseline liquidity (≥1-2%) to qualify whale-cluster signals; reject any spike where priceΔ=0.0 unless volume exceeds 5% of rolling baseline.

### Suggested thresholds
`min_volume_delta` → `0.01`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-917** `planned` — Add hard filter: reject whale-cluster signals when priceΔ=0.0 AND yes-probability <0.15 AND volume delta <5% of baseline daily volume
- [ ] **TB-918** `planned` — For markets with baseline volume <1M daily or yes-probability <10%, require either ≥0.5% price move OR volume delta >10% of baseline to emit signal
- [ ] **TB-919** `planned` — Introduce price-impact correlation check: if cluster size grows but price moves negatively/flatly, downweight or mute signal as non-directional positioning
- [ ] **TB-920** `planned` — Add intra-spike follow-through validation: flag only if price sustains directional move ≥5 bps within 5 minutes post-cluster, filtering passive rebalancing
- [ ] **TB-921** `planned` — Lower whale-cluster p-value significance when identical trade sizes execute at identical price levels with zero slippage; treat as mechanical sweep, not informed flow

---

## 2026-04-07 — Advisor snapshot 254

### Summary
Whale-cluster tier is generating excessive false positives (19 of 21 signals labeled noise) due to flagging large coordinated volume with zero or near-zero price impact in low-conviction markets. Notable tier also shows false positives on low-absolute-volume markets without sustained price holds.

### Next step
Require non-zero price impact (≥0.5% move) OR sustained directional follow-through (5+ min hold) as mandatory gate before emitting whale-cluster or notable signals, regardless of volume delta or score magnitude.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-922** `planned` — For whale-cluster tier: reject signals where priceΔ = 0.0 unless volΔ exceeds 5% of baseline daily volume AND market conviction (yes probability) >25%.
- [ ] **TB-923** `planned` — For notable tier: require either priceΔ ≥0.02 sustained for ≥5 minutes OR multi-sided volume (buy/sell ratio 40–60%) before flagging markets with <$1M daily baseline.
- [ ] **TB-924** `planned` — Add market-context filter: suppress whale-cluster alerts in markets with implied probability <10% unless accompanied by ≥0.5% price move or ≥30 whales clustered within 120s.
- [ ] **TB-925** `planned` — Introduce directional persistence check: flag whale-cluster only if price holds above/below spike entry level by ≥0.5% for ≥5 minutes post-spike, filtering out mechanical rebalancing.
- [ ] **TB-926** `planned` — Tighten baseline volume normalization: require volΔ to exceed 1% of rolling 1h baseline before flagging whale-cluster in liquid markets (>4.8M daily volume).

---

## 2026-04-07 — Advisor snapshot 255

### Summary
Whale-cluster tier is generating pervasive false positives on low-conviction markets with zero or near-zero price impact despite large volume deltas. Nearly all flagged signals lack directional conviction, indicating mechanical/liquidity-driven activity rather than informed trading.

### Next step
Require non-zero price impact (≥0.5% move) OR sustained directional follow-through (5+ min hold) as mandatory gate for whale-cluster signals, especially in markets with <10% implied probability or <$1M daily baseline volume.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`, `score_threshold` → `12.0`

### Recommendations

- [ ] **TB-927** `planned` — Implement price-impact requirement: reject whale-cluster signals where priceΔ=0.0% unless accompanied by sustained 5-minute directional pressure or minimum cluster size >30-35 whales
- [ ] **TB-928** `planned` — Add market-liquidity gate: for baseline volume <$1M or <10% probability, require volume delta ≥5-10% of baseline AND ≥0.5% price move to emit signal
- [ ] **TB-929** `planned` — Filter mechanical execution patterns: suppress signals when all trades execute at identical price levels with zero price drift, as this indicates algorithmic splits rather than information asymmetry
- [ ] **TB-930** `planned` — Increase whale-cluster score_threshold for low-conviction markets: raise from 8.0 to 12.0+ when yes-probability <10% and priceΔ=0, or implement conditional scoring that penalizes zero-impact volume spikes

---

## 2026-04-07 — Advisor snapshot 256

### Summary
Whale-cluster tier is generating excessive false positives on low-conviction markets (sub-10% probability) with large volume spikes but zero price impact, indicating mechanical execution rather than informed trading.

### Next step
Implement a mandatory price-impact filter for whale-cluster signals: require either ≥0.5% concurrent price movement OR explicitly tag zero-price-delta spikes as non-actionable unless they exceed 5% of baseline daily volume with asymmetric directional bias (>95% buy/sell ratio).

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-931** `planned` — Require spike_min_price_move ≥0.005 (0.5%) for whale-cluster tier, or add conditional rule: if priceΔ=0.0, reject signal unless volΔ >5% of baseline daily volume AND buy/sell ratio >95%
- [ ] **TB-932** `planned` — Lower whale-cluster sensitivity in markets with implied probability <10% by requiring minimum whale concentration >30 unique accounts within 120s window OR sustained price hold >2% above entry for 5+ minutes
- [ ] **TB-933** `planned` — Raise spike_min_volume_delta to 1-2% of market's baseline daily volume for whale-cluster tier (context-aware threshold, not global), or cap detection in markets with <1M daily baseline volume unless accompanied by ≥0.5% price move
- [ ] **TB-934** `planned` — Filter out whale-cluster signals where all trades execute at identical price levels (mechanical execution pattern) unless volume spike represents >10% of baseline and shows directional asymmetry
- [ ] **TB-935** `planned` — For low-liquidity markets (<1M daily volume), require explicit multi-sided confirmation: volume spike must show either (1) consecutive price levels trending directionally, or (2) interleaved buy/sell clustering that suggests genuine competition rather than algorithm splits

---

## 2026-04-07 — Advisor snapshot 257

### Summary
Whale-cluster tier is generating systematic false positives in low-conviction markets with zero or minimal price impact, dominated by KXMARMAD-26-CONN/MICH signals where large volume spikes (4.7K–51K delta) produce no directional price movement. Notable tier also shows false positives in thin markets without sustained price holds.

### Next step
Require concurrent price impact (≥0.5% move) OR minimum volume delta as 1–2% of baseline for whale-cluster signals; simultaneously enforce minimum sustained price hold (2%+ for 5+ min) or multi-sided volume confirmation for notable tier in low-liquidity markets.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-936** `planned` — For whale-cluster tier: require priceΔ ≥ 0.005 (0.5%) OR volume delta ≥ 1–2% of baseline daily volume to filter static-price accumulation noise
- [ ] **TB-937** `planned` — For notable tier: require either sustained price hold at 2%+ above prior level for ≥5 minutes OR multi-sided volume (buy/sell ratio 45–55%) before flagging low-absolute-volume markets
- [ ] **TB-938** `planned` — Raise minimum trade count threshold to ≥10 trades within detection window for thin markets (baseline daily volume <1M), and require price moves >15% or concurrent whale-cluster confirmation
- [ ] **TB-939** `planned` — For whale-cluster in low-conviction markets (yes <0.10): require minimum cluster size >30 whales within 120s window AND either 1%+ price movement or asymmetric buy/sell >95% with price-level stability
- [ ] **TB-940** `planned` — Adjust p-value scoring in whale-cluster detector to down-weight signals with zero price elasticity; apply separate sensitivity thresholds for markets with >10M daily baseline volume

---

## 2026-04-07 — Advisor snapshot 258

### Summary
Whale-cluster and low-conviction market detectors are generating excessive false positives by flagging volume spikes without accompanying price impact or by treating normal microstructure noise as informed flow. The MARMAD and TRUMPSAY markets show systematic over-triggering when priceΔ=0.0 or priceΔ<1%, regardless of volume magnitude.

### Next step
Implement a mandatory price-impact gate for whale-cluster and notable tiers: require either concurrent priceΔ≥0.5% OR volume spike ≥5% of baseline daily volume AND trade count ≥10 to emit signal. This filters mechanical execution and rebalancing noise while preserving genuine directional flow.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-941** `planned` — Add hard requirement: whale-cluster signals must show priceΔ≥0.5% OR volume delta ≥5% of baseline daily volume (not just absolute deltas). Zero-price-impact volume spikes are non-informative.
- [ ] **TB-942** `planned` — Require minimum trade count ≥10 within detection window for 'notable' tier in low-liquidity markets (<1M baseline daily volume); raise to ≥15 for 'whale-cluster' tier to distinguish coordinated informed flow from algorithmic splits.
- [ ] **TB-943** `planned` — For ultra-low-conviction markets (yes<0.10), suppress whale-cluster alerts entirely unless accompanied by priceΔ≥1% or sustained directional pressure hold >5min, as these attract mechanical noise traders.
- [ ] **TB-944** `planned` — Introduce market-liquidity adjustment: scale volume delta threshold by inverse of baseline daily volume. Markets <1M volume require volΔ ≥10% of baseline; markets >10M require volΔ ≥5% to flag.
- [ ] **TB-945** `planned` — Reject 'notable' alerts when all trades execute at identical price levels with zero spread/elasticity; flag as mechanical rebalancing instead of directional signal.

---

## 2026-04-07 — Advisor snapshot 259

### Summary
Detector is generating excessive false positives in low-liquidity and whale-cluster markets by flagging volume spikes without concurrent price impact. Most noise comes from thin markets (minor league sports, ultra-low probability events) and coordinated trades that execute at static prices.

### Next step
Implement a mandatory price-impact floor for whale-cluster and low-liquidity tiers: require either ≥0.5% price move OR volume delta >5% of baseline. Separately, raise spike_min_price_move to 0.03 (3%) for markets with <1M daily baseline volume.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.03`, `score_threshold` → `15.0`

### Recommendations

- [ ] **TB-946** `planned` — For whale-cluster tier: require non-zero price impact (minimum 5 bps) OR volume spike >5% of rolling baseline to emit signal
- [ ] **TB-947** `planned` — For thin markets (<1M daily volume): raise minimum price move requirement to 3% and require ≥3 trades within detection window
- [ ] **TB-948** `planned` — For extreme-probability markets (yes/no <5% or >95%): add 1% baseline-volume threshold and require price persistence >5 minutes before flagging
- [ ] **TB-949** `planned` — Lower whale-cluster score weighting when price delta = 0.0; static-price volume is 80% noise in this dataset
- [ ] **TB-950** `planned` — Implement trade-count floor: require ≥5 trades for 'notable' tier, ≥10 for whale-cluster in low-conviction markets

---

## 2026-04-07 — Advisor snapshot 260

### Summary
The detector is generating false positives across thin/low-liquidity markets by flagging volume spikes without corresponding price conviction (priceΔ often 0–2%) and by treating baseline-equal volumes as anomalies. Whale-cluster and notable tiers are especially prone to noise in markets with sub-1% baseline elasticity.

### Next step
Enforce a conjunctive filter: require *both* (1) volume delta ≥1.5–2.0x baseline AND (2) price move ≥2–3% for notable/whale-cluster tiers, except where trade count ≥10 AND price hold ≥5 min. This prevents flat-price accumulation noise while preserving genuine conviction moves.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-951** `planned` — For whale-cluster tier: raise minimum volume delta to 5–10% of baseline, or require concurrent priceΔ ≥0.5% to filter accumulation without conviction.
- [ ] **TB-952** `planned` — For notable/thin-market tiers: implement minimum trade-count filter (e.g., ≥3–5 trades) and require price persistence (e.g., >2% move held ≥5 minutes) before emitting signal.
- [ ] **TB-953** `planned` — Globally raise spike_min_volume_delta multiplier from baseline-equal to 1.5–2.0x baseline to distinguish genuine anomalies from normal order fragmentation.
- [ ] **TB-954** `planned` — For ultra-low-liquidity markets (baseline vol <5k): enforce priceΔ ≥3% *and* ≥10 trades within window, or suppress detection entirely and flag for manual review instead.

---

## 2026-04-07 — Advisor snapshot 261

### Summary
The detector is generating false positives primarily in low-liquidity and skewed-probability markets where volume spikes occur without meaningful price impact. Most flagged signals show priceΔ ≤ 2% despite high volume deltas, indicating conviction is absent.

### Next step
Implement a price-move floor (minimum 2-3%) as a hard gate for all tiers except whale-cluster; for whale-cluster, require either significant price impact (>0.5%) OR volume must exceed 5-10% of baseline to filter accumulation-only behavior.

### Suggested thresholds
`min_volume_delta` → `0.08`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-955** `planned` — Require minimum 2-3% price move to accompany volume spikes in binary yes/no markets with implied probability >80%, as conviction testing produces high-volume/low-price trades
- [ ] **TB-956** `planned` — For thin/low-liquidity markets (non-major-league sports, low baseline volume), add minimum trade count threshold (≥10 trades) or require price persistence >5 minutes before escalating tier
- [ ] **TB-957** `planned` — Raise whale-cluster detection to require EITHER volume delta >5-10% of baseline OR concurrent price move >0.5%, eliminating flat-price accumulation alerts

---

## 2026-04-07 — Advisor snapshot 262

### Summary
Detector is triggering on high-volume activity without meaningful price conviction, particularly in skewed binary markets, thin sports books, and ultra-low-liquidity whale accumulation. Most false positives show volume spikes decoupled from price movement (priceΔ=0.0–0.02), indicating algorithmic noise or baseline churn rather than informed flow.

### Next step
Implement a mandatory price-move floor (2–3% for binary markets, 0.5% for whale-cluster tiers) AND a minimum trade-count/persistence filter to require volume spikes to demonstrate actual conviction rather than fragmented order flow.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-958** `planned` — For binary yes/no markets with implied probability >80%, require concurrent price move ≥3% to accompany volume spikes, as conviction testing in skewed markets produces high volume with minimal price impact.
- [ ] **TB-959** `planned` — For thin/low-liquidity markets (sports, niche events), implement minimum trade-count threshold (≥3–10 trades depending on baseline liquidity) or require 5+ minute price persistence before flagging volume spikes as notable.
- [ ] **TB-960** `planned` — For whale-cluster tier signals, require either volume spike >0.5x baseline AND price move >0.5%, or reject flat-price accumulation (<0.1% move) entirely to filter conviction-free accumulation.
- [ ] **TB-961** `planned` — Raise absolute minimum volume delta threshold to 1.5–2.0x baseline rather than 1.0x to exclude signals where volume merely matches rather than exceeds normal conditions.

---

## 2026-04-07 — Advisor snapshot 263

### Summary
Detector is generating false positives by triggering on volume spikes without sufficient price conviction, particularly in skewed markets (high baseline odds) and thin/low-liquidity venues where fragmented order flow creates noise.

### Next step
Implement a context-aware minimum price move requirement that scales with market structure: require 3-5% price move for high-conviction markets (yes/no >0.80 or <0.20), 2% for normal markets, and pair all volume spikes with minimum trade-count validation (≥3 trades) or price persistence checks.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-962** `planned` — Raise spike_min_volume_delta to 1.5x or 2.0x baseline to filter triggers where volume merely matches rather than exceeds baseline activity
- [ ] **TB-963** `planned` — Implement tiered spike_min_price_move: require 0.05 (5%) for markets with yes >0.80 or <0.20; require 0.02 (2%) for markets with yes 0.30-0.70; require 0.03 (3%) for thin markets
- [ ] **TB-964** `planned` — Add minimum trade-count filter (≥3 trades) or require price persistence >5 minutes before emitting watch/notable tier signals to eliminate single-block algorithmic noise

---

## 2026-04-07 — Advisor snapshot 264

### Summary
Detector is triggering on high-volume trades without sufficient price conviction, particularly in skewed binary markets and low-liquidity venues. Volume spikes alone are not reliably informative when price impact is minimal (≤2%).

### Next step
Implement a dynamic minimum price-move requirement that scales with market structure: require 3-5% for binary markets with implied probability >80%, and >2% for low-liquidity markets; pair with volume-ratio validation (spike must exceed 1.5x-2.0x baseline, not merely equal it).

### Suggested thresholds
`min_volume_delta` → `1.75`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-965** `planned` — Raise minimum volume delta threshold to 1.5x-2.0x baseline volume to distinguish genuine spikes from normal market conditions (filters KXTOPCHEF case where volΔ=69k but priceΔ=0.02).
- [ ] **TB-966** `planned` — Add conditional price-move floors: require ≥3% price move for binary yes/no markets with yes probability >80% and <20%; require ≥2% for thin-volume markets (low-liquidity minor/independent league sports).
- [ ] **TB-967** `planned` — Introduce trade-count or time-persistence validation: require minimum 3+ trades or 5+ minute price persistence before flagging, especially for low-conviction markets (implied probability near 0.50 or very skewed).

---

## 2026-04-07 — Advisor snapshot 265

### Summary
The detector is triggering on high-volume activity without sufficient price conviction, particularly in skewed markets and thin-volume venues. Volume spikes alone are insufficient signals without accompanying price movement or market microstructure validation.

### Next step
Implement a tiered validation rule: require minimum price move (3-5%) for high-confidence binary markets with skewed probabilities (>80% or <20%), and add trade-count or persistence filters for thin-volume venues before escalating volume deltas to signal tier.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-968** `planned` — For binary yes/no markets with implied probability >80%, enforce minimum 3-5% price move alongside volume spikes to filter conviction-testing trades that move volume without conviction
- [ ] **TB-969** `planned` — For thin-volume markets (sports, niche events), require ≥3 trades within spike window and/or 5+ minute price persistence before flagging as notable, reducing single-trade noise
- [ ] **TB-970** `planned` — Raise minimum volume delta multiplier from 1.0x to 1.5x or 2.0x baseline to distinguish genuine unusual activity from normal market cycling

---

## 2026-04-07 — Advisor snapshot 266

### Summary
Volume spikes in skewed binary markets and thin-volume sports markets are triggering false positives despite high scores, because price impact is naturally muted in these contexts and single large trades lack conviction signal.

### Next step
Implement market-type conditional logic: require minimum price move (3-5%) for high-skew binary markets (yes/no >75%), and enforce trade-count or persistence requirements for thin-volume markets before escalating volume deltas to notable tier.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-971** `planned` — For binary markets with implied probability >75%, enforce spike_min_price_move ≥ 0.03 (3%) alongside volume delta triggers, as volume alone lacks conviction signal in skewed orderbooks
- [ ] **TB-972** `planned` — For thin-volume markets (avg trade size >500 or <10 trades/minute), require minimum 3+ trades within spike window OR 5+ minute price persistence before flagging as notable/watch
- [ ] **TB-973** `planned` — Add market-category feature detection: classify market liquidity profile at ingest time and apply tiered thresholds (skewed binary / thin-volume / normal) rather than global one-size-fits-all rules

---

## 2026-04-07 — Advisor snapshot 267

### Summary
False positives cluster around low-conviction volume moves in skewed markets (high baseline probabilities) and low-volume spikes with minimal price confirmation. Current thresholds trigger on volume alone without sufficient price or confirmation anchoring.

### Next step
Implement asymmetric thresholds: require either (a) substantial volume delta AND meaningful price move together, OR (b) spike_score above 4.5+ with multi-trade confirmation. This prevents single large trades or noise from triggering signals in illiquid/skewed markets.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`, `score_threshold` → `4.0`

### Recommendations

- [ ] **TB-974** `planned` — Require AND logic for spike_min_volume_delta and spike_min_price_move: if volΔ > 1.5x baseline, enforce priceΔ ≥ 0.03 (3%); if volΔ < 1.5x, require priceΔ ≥ 0.05 (5%) to compensate
- [ ] **TB-975** `planned` — Add confirmation filter: reject signals with <3 trades in the spike window or single dominant order; require distributed volume across multiple participants
- [ ] **TB-976** `planned` — Raise spike_score_threshold to 4.0+ for markets with baseline implied probability >75%, since high-probability markets naturally show skewed volume-to-price ratios during position testing

---

## 2026-04-07 — Advisor snapshot 268

### Summary
Low-liquidity binary markets are generating false positives from small trades creating outsized price moves. Signals lack sufficient trade confirmation and apply uniform thresholds across markets with vastly different liquidity profiles.

### Next step
Implement liquidity-aware threshold scaling: require higher volume delta or price move thresholds for low-liquidity markets, and mandate multi-trade confirmation to filter single-trade noise.

### Suggested thresholds
`min_volume_delta` → `1500.0`, `min_price_move` → `0.03`, `score_threshold` → `6.0`

### Recommendations

- [ ] **TB-977** `planned` — Add minimum trade count requirement (e.g., ≥2 trades within spike window) to filter single-contract moves that artificially inflate price impact
- [ ] **TB-978** `planned` — Introduce liquidity tier classification and apply stricter volume_delta thresholds to low-liquidity markets (e.g., require volΔ >2000 for markets with <10k baseline volume)
- [ ] **TB-979** `planned` — Enforce OR logic for volume/price thresholds: require either volΔ >1.5x baseline OR priceΔ >3%, rather than triggering on modest moves in both dimensions simultaneously

---

## 2026-04-07 — Advisor snapshot 269

### Summary
Low-liquidity markets are generating false positives through mechanical liquidity (unexecuted quotes) and outsized price moves from minimal trade sizes. The detector is overly sensitive to small absolute moves in thin markets.

### Next step
Implement liquidity-adjusted thresholds that scale requirements inversely with baseline market volume: require higher volume delta or price move thresholds for markets below a liquidity floor.

### Suggested thresholds
`min_volume_delta` → `5.0`, `min_price_move` → `0.05`, `score_threshold` → `5.5`

### Recommendations

- [ ] **TB-980** `planned` — Exclude signals where volume delta is <5 contracts or derives from single-trade executions; require multi-trade confirmation for tier=notable signals in markets with <10k baseline daily volume.
- [ ] **TB-981** `planned` — For markets with volume <5k baseline, raise spike_min_price_move to 0.05 (5%) or require spike_min_volume_delta >2x baseline instead of 1.5x; KXNBAGAME (4252 vol, 2% move) and KXTOPCHEF (70k vol, 5% move) both show this pattern.
- [ ] **TB-982** `planned` — Flag unexecuted quotes persisting >3 seconds without trade confirmation as mechanical liquidity and exclude from scoring; KXTOPCHEF's 4.184 score suggests quote-only activity rather than genuine interest.

---

## 2026-04-07 — Advisor snapshot 270

### Summary
Low-volume and binary-outcome markets are generating false positives from single large trades or unexecuted quotes that create outsized price moves. The detector lacks trade-count and trade-concentration filters to distinguish mechanical liquidity from genuine informed flow.

### Next step
Introduce a trade-count minimum (≥2 trades in same direction within window) and a trade-size concentration filter to require that no single trade represents >40% of detected volume delta, especially in sub-10k baseline volume markets.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.03`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-983** `planned` — Require minimum 2 trades in the same direction within the detection window to confirm genuine flow vs. single-block liquidity events
- [ ] **TB-984** `planned` — For markets with baseline volume <10k contracts, enforce minimum trade size threshold (e.g., ≥50 contracts per trade) or require volume concentration <60% in single trade
- [ ] **TB-985** `planned` — Exclude unexecuted quotes that persist >3 seconds without triggering fills from contributing to spike signals; treat as mechanical/stale liquidity rather than intent

---

## 2026-04-07 — Advisor snapshot 271

### Summary
Low-volume and binary markets are generating false positives from single small trades or unexecuted quotes that create outsized price moves. The detector is too sensitive to volume/price combinations in thin markets where mechanical liquidity and minimal order flow create signal-like artifacts.

### Next step
Implement minimum trade size (notional or contract count) requirement and distinguish between executed trades vs. unexecuted quotes in the volume delta calculation, rather than relying on volume and price move thresholds alone in low-liquidity venues.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.04`, `score_threshold` → `5.5`

### Recommendations

- [ ] **TB-986** `planned` — Require minimum trade size of 5+ contracts or notional equivalent per trade; reject single-block moves below this threshold regardless of price impact
- [ ] **TB-987** `planned` — Exclude unexecuted quotes from volume delta; only count completed trades to filter mechanical liquidity from standing orders
- [ ] **TB-988** `planned` — For markets with <10k baseline volume, require volume concentration check: flag only if >30% of detection window volume executes in single direction within 2-second window

---

## 2026-04-07 — Advisor snapshot 272

### Summary
False positives are driven by single large trades in low-volume markets that spike volume without sustained price movement. Volume deltas alone are insufficient signals without confirmatory price action or trade sequencing.

### Next step
Require sustained price confirmation: enforce either (a) minimum consecutive ticks in signaled direction, or (b) higher price_move threshold, especially in low absolute-volume regimes.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-989** `planned` — Raise spike_min_price_move from 0.03 to 0.05 (5%) to filter out noise trades that move volume but not price
- [ ] **TB-990** `planned` — Add consecutive_tick_confirmation rule: require ≥2 ticks moving in same direction post-spike before emitting signal, to eliminate single-outlier trades
- [ ] **TB-991** `planned` — Implement volume-normalized thresholds: scale spike_min_volume_delta by market tier (higher absolute delta required for sub-1M volume markets)

---

## 2026-04-07 — Advisor snapshot 273

### Summary
False positives are dominated by single large trades in low-volume markets that create volume spikes without sustained price conviction or multi-trade confirmation. The detector is too sensitive to isolated outlier transactions.

### Next step
Require multi-trade confirmation (2-3 consecutive trades in same direction) or sustained price persistence (5+ ticks) before emitting signals, especially in low-volume and micro-timeframe markets.

### Suggested thresholds
`min_volume_delta` → `100000.0`, `min_price_move` → `0.02`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-992** `planned` — Implement a consecutive-trade confirmation rule: require at least 2-3 trades in the same direction within 30 seconds before triggering watch/notable tiers, rather than firing on single large orders.
- [ ] **TB-993** `planned` — For 15-minute micro-markets and low-volume instruments (volΔ < 100k or trade size < 50 shares), mandate price persistence across 5+ consecutive ticks in signaled direction before emission.
- [ ] **TB-994** `planned` — Tier-specific minimum trade size floor: 'watch' tier requires ≥50 shares per trade; 'notable' tier requires either ≥100 shares OR multiple confirmed trades; block single-trade alerts in markets with <1k daily volume.

---

## 2026-04-07 — Advisor snapshot 274

### Summary
The detector is generating false positives across all tiers by flagging single large trades or mechanical oscillations without sustained directional conviction or multi-trade confirmation. Low-liquidity and micro-markets (15-min) are especially vulnerable to noise.

### Next step
Require multi-trade or multi-tick confirmation: enforce that spike signals must be backed by either 2+ consecutive trades in the same direction, or 3+ consecutive price ticks moving in the signaled direction, before emission.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.05`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-995** `planned` — Implement minimum executed trade count filter: require at least 2 consecutive same-direction trades (not single outliers) to trigger watch/notable alerts, especially in low-volume markets (<500 vol delta).
- [ ] **TB-996** `planned` — For 15-minute micro-markets, add a multi-tick persistence rule: price move must hold or extend over 3+ consecutive ticks; reject signals backed by single 43-share trades or volume spikes with 0% price follow-through.
- [ ] **TB-997** `planned` — Add market-liquidity-aware thresholds: raise minimum trade size from 1 to 5+ lots for contracts with <1000 baseline volume; raise to 50+ shares for tier 'watch' alerts in thin markets to filter conviction-lacking outliers.
- [ ] **TB-998** `planned` — Filter volume spikes without directional imbalance: reject signals where cumulative buy/sell volume remains balanced despite large total delta; require buy-side or sell-side imbalance >60% of delta volume.

---

## 2026-04-07 — Advisor snapshot 275

### Summary
The detector is triggering on low-conviction, single-trade events and mechanical oscillations across illiquid markets. High score values (up to 13.4) paired with low yes-probability (0.05–0.51) indicate the scoring function weights volume delta too heavily relative to trade execution intent and follow-through.

### Next step
Require executed trade count ≥2 in the same direction within a 5-minute window, or introduce a quote-to-trade ratio filter and volume-weighted price conviction metric to exclude single-sided liquidity and micro-moves on thin order books.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.04`, `score_threshold` → `8.5`

### Recommendations

- [ ] **TB-999** `planned` — Add minimum executed trade count requirement: ≥2 consecutive trades in same direction (buy or sell) within 5-minute lookback to qualify for any tier alert.
- [ ] **TB-1000** `planned` — Implement quote-to-trade ratio filter: reject signals where quote volume is >3× executed trade volume, indicating single-sided orders without follow-through fills.
- [ ] **TB-1001** `planned` — Raise minimum trade size thresholds by market liquidity tier: low-liquidity markets require ≥5 lots per trade; standard markets ≥3 lots; high-volume markets ≥1 lot. Reject alerts from single outlier trades.
- [ ] **TB-1002** `planned` — For 15-minute and intraday micro-markets, require price conviction to persist across ≥3 ticks or ≥2 minutes before emitting 'notable' tier signals.
- [ ] **TB-1003** `planned` — Apply volume-weighted price movement filter: exclude trades with identical cumulative volumes or mechanical oscillations that lack directional conviction.

---

## 2026-04-07 — Advisor snapshot 276

### Summary
The detector is generating false positives across low-liquidity and micro-markets by triggering on single trades, quote-only volume, and mechanical oscillations without sustained directional conviction or multi-trade confirmation.

### Next step
Implement a multi-trade confirmation rule requiring 2+ consecutive trades in the same direction within the spike window, combined with a minimum executed trade volume filter (5+ lots) to exclude single-contract outliers and quote-driven events.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.04`, `score_threshold` → `8.5`

### Recommendations

- [ ] **TB-1004** `planned` — Require minimum 2+ distinct executed trades in the same direction within spike detection window, rather than flagging single outlier transactions
- [ ] **TB-1005** `planned` — Filter quote-only volume: implement quote-to-trade ratio validation or require minimum confirmed executed trade volume (5+ lots for low-liquidity, 50+ shares for tier-watch markets) before emitting signal
- [ ] **TB-1006** `planned` — Add sustained directional flow check: exclude mechanical oscillations and single-sided liquidity events by requiring net buy/sell imbalance to persist across 5+ price ticks or 2+ minutes in micro-markets
- [ ] **TB-1007** `planned` — Raise minimum trade size thresholds: increase from 1 lot to 5+ lots for low-liquidity contracts; raise tier-watch threshold from 3 to 50+ shares to filter low-conviction noise

---

## 2026-04-07 — Advisor snapshot 277

### Summary
All 8 recent signals labeled as noise/unclear/low show a consistent pattern: low-liquidity markets are triggering alerts on single trades, quote-stuffing, or mechanical oscillations lacking genuine conviction. The detector conflates volume delta with executed trade volume and ignores market microstructure signals.

### Next step
Implement a minimum executed trade count filter (3+ trades in same direction within spike window) and require quote-to-trade ratio validation before emitting any signal, especially in tier=watch and tier=notable for illiquid markets.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.05`, `score_threshold` → `5.5`

### Recommendations

- [ ] **TB-1008** `planned` — Add minimum executed trade count requirement: 3+ confirmed trades in the same direction within the spike detection window, scaled by market liquidity tier (5+ for niche/political markets, 3+ for standard, 2+ for high-volume)
- [ ] **TB-1009** `planned` — Implement quote-to-trade ratio gate: reject signals where quote volume >> executed trade volume (e.g., ratio > 5:1 in low-liquidity markets), filtering out quote-stuffing and single-sided liquidity events
- [ ] **TB-1010** `planned` — For sub-$10k volume_delta markets, require minimum trade size threshold (5+ lots/shares per trade) or multiple micro-trades (5+ trades ≥1 lot) to prevent single-contract outliers from triggering alerts
- [ ] **TB-1011** `planned` — Add directional flow confirmation: require buy/sell side imbalance (≥60% one-sided) or sustained price pressure over 2+ ticks, not mechanical oscillations with balanced volume
- [ ] **TB-1012** `planned` — Tier-based score multiplier: apply 1.5x multiplier to spike_score_threshold for low-liquidity markets (volume_delta < 50k) before emitting watch/notable tier signals

---

## 2026-04-07 — Advisor snapshot 278

### Summary
All 7 recent signals are labeled noise/unclear/low despite scoring above current thresholds. The detector is firing on quote-driven oscillations, single-sided liquidity events, and micro-trades lacking execution conviction rather than genuine informed flow.

### Next step
Pivot from volume-delta and price-move thresholds to execution-quality filters: require minimum executed trade count (3-5 trades) or minimum trade size (5-50 lots depending on market liquidity tier) before emitting any signal. Quote volume alone is insufficient.

### Suggested thresholds
`score_threshold` → `5.5`

### Recommendations

- [ ] **TB-1013** `planned` — Add min_executed_trade_count requirement: 3-5 actual trades (not quotes) within spike window to filter quote-stuffing and mechanical oscillations
- [ ] **TB-1014** `planned` — Add min_trade_size_threshold that scales by market liquidity tier: 50+ shares for political/niche markets, 5+ lots for micro-contracts, relaxed for high-volume crypto
- [ ] **TB-1015** `planned` — Add directional_conviction filter: require buy/sell side imbalance or sustained directional volume (not just symmetric oscillations) to distinguish real flow from quote-layer noise
- [ ] **TB-1016** `planned` — Add quote_to_trade_ratio filter: exclude spikes where volume is quoted but not executed, or where single-sided quotes dominate without reciprocal fills
- [ ] **TB-1017** `planned` — Add price_persistence check for micro-markets (15m): require price conviction to hold for 5+ ticks or 2+ minutes before elevating to notable tier

---

## 2026-04-07 — Advisor snapshot 279

### Summary
All five recent signals are labeled noise/unclear/low despite varying scores and volumes, indicating the detector is triggering on quote activity and mechanical oscillations rather than genuine executed flow, particularly in illiquid markets.

### Next step
Implement a trade-execution filter requiring minimum confirmed executed trades (not just quote volume) at moved price levels, with stricter thresholds for low-liquidity markets based on contract type and typical daily volume.

### Suggested thresholds
`score_threshold` → `4.5`

### Recommendations

- [ ] **TB-1018** `planned` — Require minimum 3–5 confirmed executed trades accompanying any spike, with trade count scaled by market liquidity tier (reality TV/political markets need stricter counts than crypto).
- [ ] **TB-1019** `planned` — Add quote-to-trade ratio validation: reject spikes where quote volume >> executed trade volume, or where a single price level has no confirmed fills at the moved price.
- [ ] **TB-1020** `planned` — Implement buy/sell-side imbalance or directional flow persistence check: require sustained one-sided volume flow across multiple time buckets rather than single mechanical oscillations or quote-stuffing events.
- [ ] **TB-1021** `planned` — For markets with <1000 daily volume baseline, raise minimum executed trade volume to 5+ lots and require price moves to span 2+ distinct price levels with opposing-side depth to filter single-contract outliers.
- [ ] **TB-1022** `planned` — Increase score_threshold to 4.5–5.0 for watch/notable tiers, since current scores (2.38–7.25) are triggering on low-conviction quote events.

---

## 2026-04-07 — Advisor snapshot 280

### Summary
High-scoring signals are being triggered by quote-driven volume spikes without corresponding executed trades, particularly in illiquid markets (niche reality TV, political betting, low-liquidity crypto). Volume delta alone is insufficient to distinguish genuine flow from quote-stuffing and one-sided liquidity events.

### Next step
Implement a trade-volume requirement filter: require minimum confirmed executed trade volume (not quote volume) or a quote-to-trade ratio threshold to validate that price moves are backed by actual transactional activity.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `5.5`

### Recommendations

- [ ] **TB-1023** `planned` — For tier=watch signals in illiquid markets (reality TV, political), require minimum 3-5 distinct executed trades accompanying any volume delta spike, or require cumulative volume across 2+ opposing price levels
- [ ] **TB-1024** `planned` — Add a quote-to-trade ratio filter: reject signals where quote volume exceeds executed trade volume by >3:1 ratio, or require minimum 50+ confirmed trade volume at the moved price level
- [ ] **TB-1025** `planned` — Segment thresholds by market liquidity tier: illiquid markets (niche, political) require higher min_price_move (0.05+) and min_trade_count; liquid markets (BTC futures) can use volume_delta alone but require quote-filtered confirmation

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
