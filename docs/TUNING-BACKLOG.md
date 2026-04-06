# Tuning Backlog

Last updated: 2026-04-06

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
