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

---

## 2026-04-05 — Advisor snapshot F

### Summary
Low-liquidity political markets are generating false positives on small price moves with modest volume deltas. Both signals had low yes-probability (0.2–0.38) and were labeled noise despite crossing current thresholds.

### Next step
Introduce an absolute minimum volume threshold (e.g., 1000+ contracts traded) for niche/low-liquidity markets before any spike detection, rather than relying solely on volume delta or relative baseline changes.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.05`

### Recommendations

---

## 2026-04-05 — Advisor snapshot G

### Summary
Low-liquidity markets (cabinet, political) are generating false positives with small absolute volumes and modest price moves. The detector is triggering on single trades or micro-moves that lack meaningful market conviction.

### Next step
Introduce an absolute minimum volume threshold (e.g., 1000+ contracts) as a hard floor, independent of baseline comparisons, to filter out niche/low-liquidity spike noise before score evaluation.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.05`

### Recommendations

---

## 2026-04-05 — Advisor snapshot H

### Summary
Low-liquidity markets are generating false positives from single large trades or minimal sustained volume. Both recent signals show modest volume deltas (692–108k) and small price moves (3–4%) that lack confirmation via trade count or multi-candle persistence.

### Next step
Introduce a trade-count or volume-persistence filter: require either sustained volume across ≥2 consecutive 1m candles OR minimum recent trade count (e.g., ≥3 trades in lookback window) before emitting a signal in low-liquidity venues.

### Suggested thresholds
`min_volume_delta` → `150000.0`, `score_threshold` → `3.5`

### Recommendations

---

## 2026-04-05 — Advisor snapshot I

### Summary
Low-liquidity markets are generating false positives from single large trades or routine algorithmic activity that move price minimally. The detector lacks filters for market depth and trade persistence.

### Next step
Implement a baseline-relative volume delta rule (e.g., require volΔ > 1.5x recent 5m average) and enforce multi-candle price persistence before signaling in markets with <1000 baseline volume.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `3.5`

### Recommendations

---

## 2026-04-05 — Advisor snapshot J

### Summary
Low-liquidity markets are generating false positives from single large trades and routine algorithmic activity. Both signals have low analyst confidence (yes=0.26 and yes=0.16) despite crossing current thresholds, indicating thresholds are too permissive for thin markets.

### Next step
Implement market-aware thresholds that scale by baseline liquidity: require percentage-based volume deltas (5-10% of recent baseline) and sustained multi-candle confirmation rather than single-spike detection in low-volume instruments.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `3.0`

### Recommendations

---

## 2026-04-05 — Advisor snapshot K

### Summary
Quote-only volume accumulation in low-liquidity markets is inflating spike scores without genuine executed trades, causing false positives on both notable and watch-tier signals.

### Next step
Implement a minimum executed trade volume filter (50+ contracts per side) before any volume delta contributes to spike score calculation, effectively decoupling quote activity from signal generation.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `9.0`

### Recommendations

---

## 2026-04-05 — Advisor snapshot L

### Summary
Quote-only activity in low-liquidity prediction markets is generating false positives across political and niche markets. Volume deltas are being inflated by quote accumulation without corresponding executed trades.

### Next step
Distinguish between quote volume and executed trade volume; require minimum executed trade volume (e.g., >20 shares/contracts per side) before any volume delta contributes to spike scoring.

### Suggested thresholds
`min_volume_delta` → `200.0`, `min_price_move` → `0.05`, `score_threshold` → `7.0`

### Recommendations

---

## 2026-04-05 — Advisor snapshot M

### Summary
Quote-only volume activity in low-liquidity political markets is generating false positives with misleading high scores despite low executed trade volume and weak price conviction (yes=0.07-0.63).

### Next step
Implement a minimum executed trade volume filter (e.g., >20 shares) that must be met before quote volume counts toward spike detection, rather than relying on quote volume deltas alone.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `5.0`

### Recommendations

---

## 2026-04-05 — Advisor snapshot N

### Summary
False positives are concentrated in low-liquidity political markets where quote-only movements and minimal actual trades trigger signals despite low conviction. Price moves alone (2%) are insufficient filters without volume validation.

### Next step
Implement trade-count validation and tiered volume thresholds by liquidity/conviction level rather than a single global volume delta threshold.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `2.5`

### Recommendations

---

## 2026-04-05 — Advisor snapshot O

### Summary
High-scoring signals with minimal price impact (1-2%) and no executed trade confirmation are generating false positives, particularly in thin/political markets where order book activity doesn't translate to real price discovery.

### Next step
Require minimum executed trade volume confirmation alongside order book delta, and enforce a price-move floor that scales with market liquidity tier.

### Suggested thresholds
`min_price_move` → `0.025`

### Recommendations

---

## 2026-04-05 — Advisor snapshot P

### Summary
False positives stem from quote-only volume spikes without sustained trade follow-through, and high scores driven by volume deltas that don't correlate with genuine price conviction or informed positioning.

### Next step
Introduce a trade-volume confirmation gate: require a minimum percentage of the volume delta to be represented by actual executed trades (not just quote/bid-ask activity) before emitting a signal.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.04`

### Recommendations

---

## 2026-04-05 — Advisor snapshot Q

### Summary
False positives are driven by thin-market noise: high relative volume deltas on low absolute baselines (SDUF) and high conviction scores disconnected from actual price impact (KXCABOUT-26APR-TGAB with 9% move but only 3% underlying probability).

### Next step
Introduce liquidity-aware thresholds that scale requirements based on baseline volume and market depth. For markets with baseline volume <20, enforce stricter absolute volume deltas and require price-volume correlation.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-05 — Advisor snapshot R

### Summary
Thin markets and low-liquidity contracts are generating false positives through amplified price moves and inflated scores on minimal volume. The spike detector lacks safeguards for markets with low absolute liquidity or microprice conditions.

### Next step
Introduce a minimum absolute volume threshold (e.g., 10,000+ contracts in market) and exclude or dampen signals from contracts priced below 0.05 before applying spike detection logic.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.05`, `score_threshold` → `100.0`

### Recommendations

---

## 2026-04-05 — Advisor snapshot S

### Summary
Low-liquidity nickname markets are generating false positives from single-trade outliers and mechanical quote-flush events that lack sustained flow conviction.

### Next step
Implement a liquidity-tier-based minimum trade size requirement: require multi-contract spikes or sustained order flow on markets with typical trade sizes below 20 contracts, rather than relying on single outlier trades.

### Suggested thresholds
`min_volume_delta` → `1500.0`, `min_price_move` → `0.05`, `score_threshold` → `6.5`

### Recommendations

---

## 2026-04-05 — Advisor snapshot T

### Summary
Low-liquidity niche markets (TRUMP nickname contracts) are generating false positives from thin order books where small single trades cause outsized price moves without reflecting genuine market consensus.

### Next step
Implement liquidity-tier-aware thresholds that require higher volume deltas and minimum trade sizes for low-liquidity markets, rather than applying uniform global thresholds.

### Suggested thresholds
`min_volume_delta` → `1.3`, `min_price_move` → `0.08`

### Recommendations

---

## 2026-04-05 — Advisor snapshot U

### Summary
Low-liquidity niche markets (like nickname contracts) are generating false positives from small absolute volumes and single large trades that create outsized price moves without reflecting genuine market consensus.

### Next step
Implement market-liquidity-aware thresholds: apply stricter volume delta multipliers (1.3x+) and minimum contract size filters for low-liquidity tiers, rather than using uniform global thresholds.

### Suggested thresholds
`min_volume_delta` → `1.3`

### Recommendations

---

## 2026-04-05 — Advisor snapshot V

### Summary
Micro-probability markets with large volume deltas but minimal price moves are generating false positives; the detector is triggering on mechanical quote clustering and passive liquidity provision rather than directional conviction.

### Next step
Implement a composite gating rule: require either (a) price move ≥2% OR (b) directional flow consensus ≥70% for at least 2 consecutive seconds, before emitting a signal in markets with yes-probability <0.10.

### Suggested thresholds
`min_price_move` → `0.02`, `score_threshold` → `7.5`

### Recommendations

---

## 2026-04-05 — Advisor snapshot W

### Summary
Detector is triggering on volume spikes without sustained price conviction, particularly in micro-probability and near-expiry markets where mechanical order clustering creates false positives.

### Next step
Implement a multi-factor gate: require either (1) price move >0.5% sustained over 5min, OR (2) directional order-flow imbalance >70% over >15sec, OR (3) price move >2% for ultra-low probability markets (<5% implied prob) within 24h of expiry. This separates passive quote updates from genuine informed flow.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `12.0`

### Recommendations

---

## 2026-04-05 — Advisor snapshot X

### Summary
The detector is generating false positives in ultra-low-probability micro-markets near expiration, where mechanical order clustering and quote updates trigger volume spikes without genuine directional conviction or meaningful price movement.

### Next step
Implement a composite filter requiring either (a) price movement >2% OR (b) sustained directional order-side imbalance (>70% one-side over >5 seconds) for markets with base probability <0.10 within 24h of expiry, rather than relying on volume delta alone.

### Suggested thresholds
`min_volume_delta` → `150000.0`, `min_price_move` → `0.02`, `score_threshold` → `12.0`

### Recommendations

---

## 2026-04-05 — Advisor snapshot Y

### Summary
High false-positive rate in micro-probability markets (yes <0.06) with volume spikes but minimal or zero price movement. Volume delta alone is insufficient; price action and order-flow persistence are needed to distinguish signal from noise.

### Next step
Require either meaningful price movement (≥0.5%) OR sustained directional order-flow persistence (≥15 seconds) for markets within 24h of expiry with base probability <0.10, to filter passive quote updates.

### Suggested thresholds
`min_volume_delta` → `100000.0`, `min_price_move` → `0.005`, `score_threshold` → `12.0`

### Recommendations

---

## 2026-04-05 — Advisor snapshot Z

### Summary
Low-conviction micro-markets near expiry are generating noise signals with weak price moves and small base probabilities. The first signal (score=5.525, priceΔ=0.04, yes=0.02) is clearly false positive; the second (score=17.831, priceΔ=0.0) suggests volume alone without sustained price action is insufficient.

### Next step
Require minimum base probability threshold (yes ≥ 0.05) AND sustained price movement or order-imbalance persistence for markets within 24h of expiry to filter micro-market noise.

### Suggested thresholds
`min_volume_delta` → `150000.0`, `min_price_move` → `0.005`, `score_threshold` → `12.0`

### Recommendations

---

## 2026-04-05 — Advisor snapshot 27

### Summary
False positives are clustering in low-conviction micro-markets (base probability <0.05) and quote-driven volume spikes lacking executed trade confirmation, particularly in short-duration expiry windows where noise dominates signal.

### Next step
Implement a two-tier filter: (1) exclude or deprioritize markets with base probability <0.05, and (2) require minimum executed trade size (not just volume delta from quotes) to validate spike legitimacy before emitting watch/notable tier alerts.

### Suggested thresholds
`min_volume_delta` → `150000.0`, `min_price_move` → `0.035`, `score_threshold` → `12.0`

### Recommendations

---

## 2026-04-05 — Advisor snapshot 28

### Summary
False positives are concentrated in low-conviction micro-markets with quote-driven volume spikes that lack substantive executed trades, particularly when base probability is very low (<5%).

### Next step
Require minimum executed trade size (not just volume delta from quotes) and enforce base probability floor to filter noise in low-liquidity prediction markets.

### Suggested thresholds
`min_volume_delta` → `150000.0`, `min_price_move` → `0.04`, `score_threshold` → `5.5`

### Recommendations

---

## 2026-04-05 — Advisor snapshot 29

### Summary
Both signals on the same market near expiration show legitimate activity (medium confidence labels) but low price moves (0.04% and 0.0%), indicating the detector is correctly identifying flow but baseline thresholds are too rigid for end-of-life market dynamics.

### Next step
Implement time-to-expiration (TTX) bucketing: apply relaxed volume_delta thresholds for markets within 48h of resolution, since mechanical rebalancing and informed positioning naturally produce elevated volume on lower price impact.

### Recommendations

---

## 2026-04-05 — Advisor snapshot 30

### Summary
Near-expiration micro-event markets are generating medium-confidence signals with low price moves (0–4%) but moderate volume spikes, driven by mechanical rebalancing and quote-rebounding rather than informed positioning.

### Next step
Introduce time-to-expiration (TTX) and quote-to-trade ratio buckets to dynamically adjust volume-delta thresholds and filter mechanical noise in final 48 hours.

### Suggested thresholds
`min_price_move` → `0.02`, `score_threshold` → `8.0`

### Recommendations

---

## 2026-04-05 — Advisor snapshot 31

### Summary
Near-expiration micro-event markets are generating medium-confidence signals with modest price moves (1-4%) on moderate volume deltas, suggesting the detector is catching genuine flow but needs context-aware tuning to separate informed trading from mechanical rebalancing.

### Next step
Implement time-to-expiration and market-liquidity bucketing: lower volume_delta thresholds for sub-24h markets while adding quote-to-trade ratio and baseline volatility filters to distinguish informed flow from post-quote mechanical moves.

### Suggested thresholds
`min_volume_delta` → `105000.0`, `min_price_move` → `0.02`, `score_threshold` → `3.8`

### Recommendations

---

## 2026-04-05 — Advisor snapshot 32

### Summary
False positives are driven by quote-side volume spikes without corresponding executed trade follow-through or price impact, particularly on ultra-low-liquidity markets where large quotes fail to materialize into actual fills.

### Next step
Require post-spike trade confirmation: signal only after observing ≥3 consecutive executed trades in the same direction within a tight time window post-quote, rather than flagging on quote delta alone.

### Suggested thresholds
`min_volume_delta` → `250000.0`, `min_price_move` → `0.03`, `score_threshold` → `12.0`

### Recommendations

---

## 2026-04-05 — Advisor snapshot 33

### Summary
Low-liquidity, near-expiry markets (KXTRUMPSAY-26APR06) are generating false positives from quote-driven volume spikes without real directional trade follow-through or meaningful price impact.

### Next step
Introduce liquidity-aware filtering: require minimum trade-to-quote ratio and consecutive directional trade confirmation before emitting signals in markets below a liquidity threshold.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `5.0`

### Recommendations

---

## 2026-04-05 — Advisor snapshot 34

### Summary
Large volume deltas without corresponding price movement or genuine trade execution are triggering false positives, particularly in low-liquidity near-expiry markets dominated by quote refreshes rather than filled trades.

### Next step
Introduce a trade-to-quote ratio filter requiring minimum 10-15% of quoted volume to be actually filled before flagging volume spikes, combined with a mandatory price-movement floor of 1% for volume-only signals.

### Suggested thresholds
`min_price_move` → `0.01`, `score_threshold` → `3.5`

### Recommendations

---

## 2026-04-05 — Advisor snapshot 35

### Summary
Detector is firing on thin markets with negligible absolute volume and quote-dominated activity lacking real price impact. Three false positives share low liquidity, near-expiry conditions, and minimal or absent price moves despite high nominal volume deltas.

### Next step
Implement a multi-factor gating rule: require both (1) volume delta as % of baseline daily volume ≥2%, AND (2) price move ≥1% OR confirmed multi-party trade volume ≥10% of quoted delta, before emitting watch-tier signals.

### Suggested thresholds
`min_price_move` → `0.01`, `score_threshold` → `5.0`

### Recommendations

---

## 2026-04-05 — Advisor snapshot 36

### Summary
Detector is triggering on noise in thin micro-cap markets: either trivial volume deltas relative to baseline daily volume, or large volume moves without accompanying price pressure indicating genuine information flow.

### Next step
Implement relative volume delta (as % of baseline daily volume) rather than absolute volume delta, and require minimum price movement (≥1%) for watch-tier signals unless volume originates from multiple counterparties.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

---

## 2026-04-05 — Advisor snapshot 37

### Summary
Ultra-thin markets with low baseline volume and extreme probability distributions are generating false positives: small absolute volumes create outsized percentage moves, and volume spikes without meaningful price movement are being incorrectly flagged as informative signals.

### Next step
Implement a market-liquidity-adjusted volume threshold that scales minimum volume delta by baseline daily volume and probability tier, rather than using a fixed absolute threshold across all markets.

### Suggested thresholds
`min_price_move` → `0.01`, `score_threshold` → `3.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 38

### Summary
Ultra-thin micro-cap markets are generating false positives: tiny absolute volumes trigger outsized percentage price moves, creating high-scoring signals that lack genuine information content.

### Next step
Introduce a volume-relative threshold: require spike_min_volume_delta to be a minimum percentage of the market's baseline daily volume (e.g., 2-5%) rather than an absolute number. This filters noise in thin markets while preserving sensitivity in liquid ones.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `2.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 39

### Summary
Detector is triggering on low-conviction, thin-market microbursts—high volume deltas without price persistence, single-tick moves in ultra-low-probability markets, and negligible absolute volumes. These are noise spikes, not genuine flow signals.

### Next step
Require price persistence (5+ minute hold) or multi-sided order book activity before emitting watch-tier signals; this filters one-directional dumps that reverse immediately.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `5.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 40

### Summary
Low-probability markets are generating high false-positive rates due to outsized percentage moves on small absolute volumes, and volume spikes without price persistence are being flagged despite lacking genuine directional conviction.

### Next step
Require multi-tick price persistence (≥2 consecutive ticks holding direction) or bilateral order activity, rather than relying on single-tick moves or one-directional absorption patterns.

### Suggested thresholds
`min_volume_delta` → `120000.0`, `min_price_move` → `0.015`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 41

### Summary
Detector is triggering on quote-driven volume without executed trades and one-directional price spikes that fail to persist, generating noise on low-conviction moves.

### Next step
Add execution quality filters: require minimum trade count (25+ executed trades) and price persistence (5+ minute hold) before emitting spike signals, rather than relying on volume and price deltas alone.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `6.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 42

### Summary
Large volume spikes in micro-cap/illiquid markets are triggering false positives despite zero or negligible price impact, indicating volume alone is insufficient for signal quality.

### Next step
Require minimum price movement alongside volume delta in low-liquidity markets, or filter signals where volume delta exceeds executed notional by a wide margin (quote refresh artifact).

### Suggested thresholds
`min_price_move` → `0.01`, `score_threshold` → `10.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 43

### Summary
Both signals fired on micro-cap markets with high volume deltas but minimal or zero price impact, indicating the detector is triggering on liquidity noise rather than genuine directional conviction.

### Next step
Require minimum price move sustained alongside volume spike in micro-cap markets; add notional volume floor (~$500k) for tail-event contracts to filter out thin-book noise.

### Suggested thresholds
`min_volume_delta` → `200000.0`, `min_price_move` → `0.03`, `score_threshold` → `12.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 44

### Summary
Ultra-low-price markets (<5¢) are generating false positives due to algorithmic order splitting and micro-market noise, with scores well below typical quality thresholds yet still triggering detection.

### Next step
Introduce market-tier-specific thresholds: require either sustained multi-minute price holds above spike level OR minimum per-trade size filters for markets with notional values <$500k, combined with a price-move floor of 5% for low-probability tail events.

### Suggested thresholds
`min_volume_delta` → `500000.0`, `min_price_move` → `0.05`, `score_threshold` → `3.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 45

### Summary
Both recent false positives occur in ultra-low-price markets with large volume deltas but minimal sustained price impact, suggesting the detector is picking up liquidity noise and algorithmic order fragmentation rather than informed flow.

### Next step
Implement a price-hold duration filter: require detected price moves to persist for at least 2-3 minutes before emitting a signal, or add minimum per-trade size enforcement for markets under 5¢ to filter algorithmic splitting.

### Suggested thresholds
`min_volume_delta` → `150000.0`, `min_price_move` → `0.05`, `score_threshold` → `6.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 46

### Summary
Detector is triggering on passive liquidity events and expired/settled markets where volume deltas lack genuine repricing signals, creating false positives despite moderate scores.

### Next step
Add market-state validation: exclude or heavily downweight signals from markets where resolution_date <= current_date, and implement quote/trade volume decomposition to filter passive liquidity masquerading as informative flow.

### Suggested thresholds
`min_price_move` → `0.02`, `score_threshold` → `4.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 47

### Summary
Detector is flagging low-conviction signals in ultra-low-probability markets where passive liquidity provision mimics genuine repricing. The first signal shows technical artifacts at extreme price levels, the second shows volume movement without actual price discovery.

### Next step
Implement price-range filtering (exclude price <= $0.00 or >= $0.95) and volume-side discrimination for markets with implied probability < 5%, separating quote-side passive liquidity from trade-side active repricing.

### Suggested thresholds
`min_price_move` → `0.01`, `score_threshold` → `3.8`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 48

### Summary
Watch-tier alerts are triggering on ultra-low-probability political markets with minimal price moves (0.00–0.03) and ambiguous volume signals that lack sustained directional bias or meaningful trade-side activity. The detector is conflating passive liquidity provision with genuine repricing.

### Next step
Implement dual-volume tracking (quote-side vs. trade-side) and enforce minimum contract thresholds for ultra-low-probability markets (<5% implied probability) before emitting watch-tier signals.

### Suggested thresholds
`min_volume_delta` → `300000.0`, `min_price_move` → `0.02`, `score_threshold` → `4.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 49

### Summary
Low-probability political speech markets are generating watch-tier alerts on minimal volume and price moves (2-3% moves on <0.05 contracts), creating noise that drowns out genuine signal.

### Next step
Implement market-depth-aware thresholds: require either absolute minimum trade size (50+ contracts) OR sustained directional bias across multiple minutes for sub-$0.05 markets, rather than relying on volume delta and price move percentages alone.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 50

### Summary
Ultra-low-probability political markets (<5%) are generating watch-tier false positives from small absolute trades creating outsized percentage moves without genuine conviction. The detector is too sensitive to price moves in illiquid markets with minimal volume anchors.

### Next step
Implement market-context-aware thresholds: require minimum absolute trade volume (50+ contracts) and filter edge-case price ranges ($0.00, >$0.95) before applying percentage-based move detection on low-probability events.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `3.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 51

### Summary
All five recent watch-tier signals are labeled as false positives. The detector is triggering on mechanical/trivial activity in ultra-low-probability political markets (<5% implied), where small absolute volumes create outsized percentage moves without genuine conviction.

### Next step
Implement a minimum absolute trade volume threshold (50–100 contracts) for watch-tier alerts on markets with yes-price <$0.05, combined with a baseline volume delta filter (5–10% of rolling baseline) to distinguish real flow from market-making noise.

### Suggested thresholds
`score_threshold` → `4.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 52

### Summary
Watch-tier alerts are triggering on mechanical micro-moves in ultra-low-probability political markets (<5%) with insufficient conviction signals. Volume deltas appear large in absolute terms but represent trivial percentages of baseline liquidity, while price moves of 2-3% lack substantive market conviction.

### Next step
Implement tier-specific thresholds: require volume delta to exceed 5-10% of baseline liquidity for watch-tier alerts, and enforce minimum absolute trade size (50+ contracts) or price-move floors (>5%) for sub-$0.05 binary event markets.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `4.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 53

### Summary
Watch-tier alerts are triggering on mechanical micro-movements in low-liquidity markets. Volume deltas are too small relative to baseline, and price moves lack conviction even when absolute volume numbers appear large.

### Next step
Implement volume-delta as a percentage of baseline rather than absolute units, with market-liquidity-aware thresholds. Require minimum 5-10% baseline volume delta for low-liquidity watch-tier markets.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `4.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 54

### Summary
Watch-tier alerts are triggering on mechanical micro-moves in low-liquidity markets: tiny absolute volume shifts and sub-3% price moves in ultra-low-probability contracts are generating noise without conviction.

### Next step
Introduce liquidity-aware thresholds: require volume delta as a percentage of baseline volume (not absolute delta), and enforce minimum absolute trade size for sub-5% probability markets to filter out trivial fills.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `4.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 55

### Summary
False positives are driven by two distinct failure modes: (1) low-baseline volume amplification turning small absolute trades into extreme spike scores, and (2) quote-management noise in high-volume markets being flagged as meaningful price signals despite minimal fractional moves.

### Next step
Implement a minimum baseline volume gate before computing volume multiples, combined with a relative volume delta threshold that scales with market size. This prevents both extreme-score amplification on thin books and noise-flagging on liquid markets.

### Suggested thresholds
`min_price_move` → `0.04`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 56

### Summary
The detector is generating false positives on thin/expiring markets and low-baseline contracts. Expiration-driven liquidations, quote management noise, and extreme volume multiples on tiny baselines are being flagged as genuine signals.

### Next step
Implement a baseline volume floor (500+ contracts) before computing spike scores, and apply a time-decay multiplier that attenuates signals within 24 hours of market expiration.

### Suggested thresholds
`min_volume_delta` → `0.05`, `score_threshold` → `50.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 57

### Summary
Detector is generating false positives on thin/expiring markets by treating small absolute volumes and deadline-driven liquidations as informative flow signals. Extreme spike scores on low-baseline markets and quote management noise on high-volume markets are also inflating false alerts.

### Next step
Introduce market-context filters before spike scoring: require minimum baseline volume threshold (~500 contracts), apply expiration-proximity decay (down-weight <24h to expiry), and enforce directional-flow validation (>70% one-sided over 30+ trades) for ultra-low-probability markets.

### Suggested thresholds
`score_threshold` → `5.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 58

### Summary
False positives are driven by thin order books amplifying small absolute volumes into high spike scores, and by deadline/liquidation effects in low-probability markets near expiration. Quote-adjustment noise on sub-1% price moves is triggering watch/notable tiers inappropriately.

### Next step
Implement a baseline volume floor (500+ contracts) and context-aware penalties: require either (a) price move >5% for low-liquidity markets, (b) sustained directional flow (>70% one-sided) for ultra-low-probability markets, or (c) score suppression for markets within 24 hours of expiration.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 59

### Summary
The detector is generating high-scoring false positives on thin markets, low-liquidity pairs, and markets near expiration by amplifying small absolute volumes into inflated spike scores. Quote-management activity and settlement positioning are being misclassified as informed flow.

### Next step
Implement a baseline volume floor (500+ contracts minimum) and require contextual filters (time-to-expiration, one-sidedness duration, baseline liquidity %) before scoring volume multiples, rather than relying on raw deltas and price moves alone.

### Suggested thresholds
`min_volume_delta` → `500.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 60

### Summary
System is emitting high-confidence scores on low-signal activity: quote-adjustment noise on thin books, deadline-driven liquidations in near-expiration markets, and single-sided market-maker volume that lacks follow-on aggression or sustained directional flow.

### Next step
Implement market-context filters (baseline volume percentage, time-to-expiration discount, directional persistence check) before relying on raw volume and price deltas, rather than raising thresholds uniformly.

### Suggested thresholds
`score_threshold` → `5.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 61

### Summary
False positives cluster around thin/low-liquidity markets, single-sided market-maker quotes, ultra-low-probability instruments, and expiration-driven liquidations. Current thresholds trigger on volume and price moves that lack genuine informed flow signals.

### Next step
Implement context-aware filtering: require sustained directional flow (>70% one-sided over 30+ trades) for ultra-low-probability markets (<5%), add liquidity-relative thresholds (5-10% of baseline volume), apply expiration decay (downweight signals <24h to expiry), and explicitly filter single-sided quotes >2M without follow-on aggression.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `6.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 62

### Summary
False positives are driven by market-maker quote adjustments and thin-book noise rather than informed flow. Large single-sided volume spikes without sustained price action or directional aggression are being incorrectly flagged as signals.

### Next step
Introduce a sustained directional flow requirement (>70% one-sided volume over a rolling window) as a gating filter before emitting signals, especially in low-liquidity or ultra-low-probability markets.

### Suggested thresholds
`min_volume_delta` → `500000.0`, `min_price_move` → `0.05`, `score_threshold` → `2.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 63

### Summary
System is generating false positives in low-liquidity and ultra-low-probability markets by flagging quote-driven noise and single large unexecuted orders as informed flow. Volume spikes lack confirmation through sustained directional trade execution.

### Next step
Implement executed-to-quoted volume ratio filter (require >5-10% of flagged volume to be actual executed trades) before emitting signals, especially for markets with implied probability <5% or baseline volume <500k.

### Suggested thresholds
`min_volume_delta` → `500000.0`, `min_price_move` → `0.05`, `score_threshold` → `3.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 64

### Summary
The detector is triggering on quote-driven noise rather than executed trades, particularly in low-liquidity markets where large unexecuted orders and single-sided quotes create false signals despite weak price conviction.

### Next step
Introduce an executed-to-quoted volume ratio filter (minimum 5-10% of flagged volume must be actual executed trades) to distinguish real conviction from quote noise, especially in markets with implied probability <5%.

### Suggested thresholds
`min_volume_delta` → `500000.0`, `min_price_move` → `0.04`, `score_threshold` → `3.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 65

### Summary
Current detector is generating false positives in low-liquidity, low-probability markets by triggering on large unexecuted quote volume without distinguishing real conviction (executed trades) from quote-driven noise.

### Next step
Implement a mandatory executed-to-quoted volume ratio filter (5-10% minimum) before any signal emission, regardless of score or volume delta magnitude.

### Suggested thresholds
`score_threshold` → `4.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 66

### Summary
Two consecutive false positives driven by thin-market volume spikes without meaningful price movement or informed flow signals. The detector is over-weighting volume deltas in low-liquidity venues and ignoring the absence of price action as a disqualifier.

### Next step
Implement a minimum absolute volume floor (not just multiplier-based delta) and require price movement as a gating condition rather than a weak contributor to scoring, especially in thin markets.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.01`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 67

### Summary
Low-absolute-volume markets are generating false positives through high multiplier ratios on routine trades. The detector is conflating relative volatility (high % moves on tiny baselines) with informed flow.

### Next step
Introduce a minimum absolute volume floor (e.g., 500+ shares/hour baseline) independent of multiplier-based scoring, to prevent thin markets from triggering alerts on statistically normal small trades.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 68

### Summary
Both signals are noisy detections in thin sports-betting markets where small absolute volumes trigger alerts despite marginal price moves. The issue is reliance on volume delta ratios without minimum absolute volume guards.

### Next step
Introduce a minimum absolute volume threshold (e.g., 200–300 contracts) before any signal qualifies as 'notable', regardless of delta ratio or score.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `45.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 69

### Summary
The detector is generating false positives in thin sports betting markets by flagging routine liquidity provision and small absolute volumes that trigger high relative deltas. All three recent notable-tier signals were labeled noise/uncertain despite notable scores.

### Next step
Implement a minimum absolute volume threshold (200-250 contracts) before flagging as notable, combined with a dynamic volume delta multiplier that scales with baseline market thickness. This addresses the core issue: relative spike detection fails in thin markets.

### Suggested thresholds
`min_volume_delta` → `40.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 70

### Summary
Thin-market sports betting products are generating false positives due to high relative volume multipliers against low absolute baselines; single-tick price moves in low-volume markets are triggering alerts despite minimal absolute activity.

### Next step
Implement a minimum absolute volume threshold (200–300 contracts) before any spike detection triggers, combined with a sustained-move requirement (2+ ticks or 60+ seconds) to filter routine liquidity provision in thin markets.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 71

### Summary
Low-volume markets are generating false positives due to high relative volume deltas and small absolute price moves triggering alerts. Thin baseline volumes (50-500 contracts) amplify noise when modest absolute volume spikes occur.

### Next step
Implement a minimum absolute volume threshold (200-300 contracts) before flagging as notable or watch-tier, combined with market-specific baseline multiplier requirements that scale by baseline volume.

### Suggested thresholds
`min_volume_delta` → `200.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 72

### Summary
False positives are clustering in low-liquidity markets where routine market-making activity (small volume deltas on thin baselines) triggers alerts despite weak price conviction and low analyst confidence.

### Next step
Implement market-size-aware thresholds: require higher volume delta multipliers and price conviction in thin markets (baseline <500 contracts), and add a sustained-hold duration requirement post-spike.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.04`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 73

### Summary
The detector is triggering on volume deltas without sufficient price conviction or directional flow, particularly in low-volume markets where small absolute changes create large relative deltas.

### Next step
Implement a dual-gate system: require either meaningful price movement (≥0.5%) OR minimum absolute volume threshold (≥100 contracts), rather than treating volume delta as a sufficient signal on its own.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 74

### Summary
False positives are driven by volume spikes in thin markets with minimal price conviction and low absolute trade sizes. The detector is flagging notional volume changes that lack directional commitment or meaningful market impact.

### Next step
Implement market-aware minimum absolute volume thresholds (tiered by market liquidity) rather than relying solely on volume delta, combined with a requirement for either sustained price movement or directional flow concentration (>60% one-sided).

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `6.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 75

### Summary
The detector is generating false positives in low-liquidity and thin markets due to quote-stacking, small notional trades, and volume spikes disconnected from meaningful price conviction. High nominal scores mask low-signal activity.

### Next step
Introduce a minimum trade count and directional flow ratio filter alongside volume/price thresholds to distinguish genuine conviction flow from mechanical quote refresh and thin-market noise.

### Suggested thresholds
`min_volume_delta` → `300.0`, `min_price_move` → `0.005`, `score_threshold` → `6.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 76

### Summary
Low-liquidity and event markets are generating false positives from quote-stacking, positioning chatter, and small notional trades that lack price conviction or directional flow persistence.

### Next step
Require corroborating price movement (>0.5-2% depending on market type) OR sustained directional flow (>60% of volume on one side) alongside volume deltas to filter noise in thin markets.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 77

### Summary
The detector is generating false positives on low-conviction volume anomalies in thin/novelty markets by triggering on volume deltas without sufficient price conviction or trade authenticity signals. Most flagged events show large volume spikes but minimal price movement (0.0-0.05), indicating quote-stacking, positioning chatter, or refresh patterns rather than genuine directional flow.

### Next step
Implement a conjunctive filter requiring EITHER (price movement ≥2%) OR (volume delta ≥25x baseline AND minimum trade count ≥3 AND net directional flow ≥60%), with absolute volume floor of 100 contracts for low-liquidity markets.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 78

### Summary
Low-liquidity and novelty markets are generating false positives from routine positioning and quote-stacking activity. Volume spikes lack price conviction or trade count validation, especially in thin event markets where baseline deltas are naturally small.

### Next step
Implement a corroborating signal requirement: spike_min_price_move should scale with market liquidity tier, and volume spikes must be accompanied by either minimum trade count (>3 trades) or minimum absolute volume thresholds (>100 contracts) before emission.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.025`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 79

### Summary
Low-liquidity novelty markets are generating false positives from routine positioning chatter and quote-stacking activity. Volume spikes lack corroborating price conviction, and small notional trades trigger alerts despite low signal quality.

### Next step
Require minimum price move (2-3%) proportional to volume delta, combined with minimum trade count (≥3) to filter quote-refresh patterns and low-conviction positioning noise.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 80

### Summary
Low-liquidity novelty markets are generating false positives through volume spikes without meaningful price conviction or trade activity. Volume deltas alone are insufficient filters when price moves are minimal (<2%) or quote-stacking dominates.

### Next step
Implement a composite gating rule: require EITHER (price_move ≥ 2% AND volume_delta ≥ 15x baseline) OR (volume_delta ≥ 25x baseline AND trade_count ≥ 3). This prevents thin-market noise while preserving genuine flow signals.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 81

### Summary
The detector is generating false positives on low-liquidity novelty markets by triggering on mechanical quote-stacking and single-trade volume spikes without sufficient price conviction or trade count validation.

### Next step
Introduce a minimum trade count requirement (3+ trades) as a gating filter before any tier assignment, combined with proportional price-move thresholds that scale with volume delta magnitude.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 82

### Summary
The detector is triggering on passive liquidity provision and quote-refresh activity in thin, low-conviction markets, generating false positives across novelty event contracts even at 'notable' tier levels.

### Next step
Introduce a correlated price-movement requirement proportional to volume delta: require min_price_move ≥ 2-3% when volume_delta exceeds 25x baseline, or enforce minimum trade count (≥3) to distinguish informed positioning from mechanical quoting.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 83

### Summary
Low-liquidity novelty markets are generating false positives through volume spikes decoupled from price conviction. Passive liquidity provision and mechanical quotes on thin markets are triggering watch/notable tiers without meaningful directional signal.

### Next step
Require correlated price movement (2-3%) alongside volume spikes as a gate before flagging low-volume markets, rather than relying on volume delta alone.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 84

### Summary
Volume spikes without correlated price movement are generating false positives, especially on thin markets where mechanical quotes and passive liquidity provision dominate. Even high-score signals (e.g., KXTRUMPSAY-26APR13-TDS) lack conviction when price movement is minimal (<1%).

### Next step
Enforce a proportional price-movement requirement: require spike_min_price_move to scale with volume delta, or alternatively, require minimum price move of 1-2% alongside any volume spike flagged as 'watch' or above.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 85

### Summary
Volume spikes on thin markets are triggering false positives without correlated price movement or sufficient trade accumulation; passive liquidity provision and mechanical quotes are being misclassified as informed flow.

### Next step
Require minimum price movement (≥1%) as a gating condition alongside volume delta, and add a minimum trade count filter (3+ trades) before escalating to 'watch' tier on low-volume markets.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.01`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 86

### Summary
False positives are clustering in thin, low-liquidity markets (sports, niche political) where modest volume moves and market-making activity trigger signals without meaningful price discovery or information content.

### Next step
Implement market-specific minimum notional thresholds (e.g., $2,000–$5,000 for sports/niche markets) and enforce a joint volume–price correlation gate: require either substantial price move (≥1%) OR volume spike paired with directional conviction (yes probability divergence from 0.50).

### Suggested thresholds
`min_volume_delta` → `2000.0`, `min_price_move` → `0.01`, `score_threshold` → `10.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 87

### Summary
Both false positives exhibit low price moves (1-13%) with modest volume deltas in thin markets, triggering signals that lack sustained conviction. The detector is sensitive to isolated trades and market-making noise rather than genuine information flow.

### Next step
Implement market-segment-specific notional value thresholds rather than relying solely on volume delta and price move, combined with a requirement for volume concentration across multiple price levels or time clustering.

### Suggested thresholds
`min_volume_delta` → `2000.0`, `min_price_move` → `0.05`, `score_threshold` → `14.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 88

### Summary
Low-liquidity and thin markets are generating false positives from isolated small trades and typical market-making activity that lack genuine directional conviction or sustained flow.

### Next step
Implement market-specific liquidity floors and require trade-cluster validation (minimum trade count, notional value, or price-level distribution) before emitting watch/notable alerts in thin markets.

### Suggested thresholds
`min_volume_delta` → `1500.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 89

### Summary
Low-liquidity political markets are generating false positives from isolated small trades and single-contract spikes that lack sustained confirmation. Volume delta alone is insufficient without trade-count and consistency checks.

### Next step
Implement market-aware filtering: require minimum trade count (≥5 trades) and directional consistency for low-liquidity venues before emitting watch/notable tiers, rather than relying solely on volume and price deltas.

### Suggested thresholds
`min_volume_delta` → `1500.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 90

### Summary
Low-liquidity political markets are generating false positives from single large trades that move price significantly but lack sustained conviction. Both signals show high price moves (12% and 4%) with modest volume on thin order books, triggering alerts despite analyst assessment of noise.

### Next step
Implement trade-count and directional-consistency gating for markets below liquidity threshold, before adjusting raw thresholds. This preserves genuine multi-participant flow while filtering single-contract spikes.

### Suggested thresholds
`min_volume_delta` → `1500.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 91

### Summary
Low-liquidity political event markets are generating false positives from one-directional flow and algorithmic activity that lack genuine price discovery signals.

### Next step
Implement multi-sided flow confirmation requirement for high-conviction signals on binary event markets, combined with stricter absolute volume thresholds for low-liquidity venues.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 92

### Summary
High volume deltas without corresponding price movement are generating false positives, particularly on low-liquidity political event markets. Volume alone is insufficient; price impact and flow directionality must be validated.

### Next step
Require minimum price movement (0.5–1%) to accompany volume spikes, especially on low-conviction and low-liquidity markets. For high-conviction markets, add multi-sided flow confirmation to filter one-directional algorithmic positioning.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 93

### Summary
High false-positive rate on low-liquidity political event markets driven by volume spikes decoupled from price conviction and one-directional flow; mechanical rebalancing and position-squaring are triggering alerts without genuine information arrival.

### Next step
Require multi-timeframe price confirmation (1m/5m/30m) with minimum ±1% move OR flow-imbalance ratio + minimum absolute volume threshold (25+ contracts) for low-liquidity markets; deprioritize raw volume delta weighting relative to price conviction on sparse-tick markets.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.01`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 94

### Summary
System is generating false positives on low-liquidity markets (sports betting, political events) where volume spikes occur without meaningful price conviction or multi-directional flow confirmation, treating mechanical rebalancing and thin-book noise as informed positioning.

### Next step
Implement a composite filter requiring price movement ≥0.5–1% to accompany volume spikes on low-conviction markets, rather than relying on volume delta alone; couple this with flow-imbalance ratio and multi-timeframe price confirmation to distinguish genuine information flow from liquidity events.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.01`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 95

### Summary
Volume spikes without corresponding price conviction are generating false positives across sports and political prediction markets. Raw volume delta is triggering signals even when price movement is minimal (0.01–0.0), suggesting mechanical rebalancing or thin-book volatility rather than informed flow.

### Next step
Introduce a price-move floor (0.5–1%) for low-baseline-volume markets and weight price movement more heavily relative to volume delta in the composite spike score, especially for categorical and binary events with sparse tick volume.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.01`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 96

### Summary
Volume spikes are triggering false positives across thin-liquidity sports and political markets without sufficient price conviction or directional flow confirmation. Most noise signals have volume deltas that exceed price moves by orders of magnitude, suggesting volume weighting is too aggressive relative to price action.

### Next step
Implement a multi-factor gating rule: require minimum price movement (0.5–2% depending on market liquidity tier) to accompany volume spikes, and add flow-imbalance or directional confirmation for low-conviction markets before emitting signals.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.015`, `score_threshold` → `150.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 97

### Summary
Volume-driven false positives dominate across thin-liquidity sports and political markets; raw volume delta is triggering signals without corresponding price conviction or directional flow confirmation.

### Next step
Shift from volume-centric detection to flow-imbalance ratio + multi-timeframe price confirmation. Require minimum 1-2% directional price move OR visible buy/sell-side dominance in recent trades before emitting signal on volume spikes alone.

### Suggested thresholds
`min_volume_delta` → `150.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 98

### Summary
Volume spikes alone are triggering false positives across thin-liquidity markets (sports betting, low-volume prediction markets) without corresponding price conviction or directional flow confirmation. Price moves of 1% or less paired with large volume deltas are generating noise.

### Next step
Require multi-factor confirmation: pair volume delta with minimum directional price movement (0.02–0.03 for thin markets, 0.02 for liquid ones) AND flow-imbalance directionality, rather than treating volume as a standalone signal.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 99

### Summary
False positives cluster around volume spikes without sustained price conviction, especially in low-liquidity markets (sports betting, thin prediction markets). Raw volume delta is triggering signals that analysts classify as execution noise or mechanical rebalancing.

### Next step
Introduce a volume-to-price-momentum coupling rule: require minimum price move (0.02–0.03) to accompany volume spikes in low-liquidity venues, or use flow-imbalance ratio instead of raw volume delta as primary trigger.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 100

### Summary
The detector is generating false positives by flagging large volume deltas without sufficient price confirmation, particularly in thin-liquidity and low-baseline-volume markets (sports betting, prediction markets). Volume spikes alone are execution noise when not accompanied by directional price movement.

### Next step
Implement a volume-to-price coupling filter: require minimum 2-3% directional price move to accompany volume spikes in markets with baseline volume <5000, and enforce multi-timeframe price confirmation for baseline volumes 5000-20000.

### Suggested thresholds
`min_price_move` → `0.02`, `score_threshold` → `500.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 101

### Summary
Volume spikes without sustained price conviction are dominating false positives, particularly in low-liquidity sports and thin prediction markets where execution noise mimics informed flow.

### Next step
Implement a volume-to-price momentum filter: require minimum 2-3% directional price move to accompany volume deltas >1000, and enforce multi-timeframe price confirmation for lower-volume spikes to distinguish sustained conviction from execution noise.

### Suggested thresholds
`min_volume_delta` → `150.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 102

### Summary
Sports betting markets are generating false positives from volume spikes without sustained price momentum; thin-liquidity categorical events show high scores despite minimal directional movement, indicating the scoring model over-weights volume relative to price conviction.

### Next step
Introduce a volume-to-price momentum coupling requirement: only flag spikes when volume delta is accompanied by minimum 2-3% sustained price move, or require corroborating trade-side dominance in low-liquidity venues.

### Suggested thresholds
`min_volume_delta` → `150.0`, `min_price_move` → `0.025`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 103

### Summary
Sports markets (NBA, political) are generating false positives from volume spikes without sustained price movement. Low-liquidity markets trigger on single outlier trades; high-liquidity categorical events flag on volume alone despite minimal directional conviction.

### Next step
Implement a volume-to-price-move coupling requirement: require minimum 2-3% price move to accompany volume spikes >1000, and enforce minimum trade size thresholds for lower-liquidity markets to filter execution noise.

### Suggested thresholds
`min_volume_delta` → `150.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 104

### Summary
Low-liquidity markets are generating false positives from volume spikes decoupled from meaningful price movement or from single large trades that don't reflect genuine sentiment shifts.

### Next step
Implement a volume-to-price coupling filter: require sustained price moves (2-3%+) to accompany volume spikes in thin markets, and enforce minimum trade-size thresholds relative to market liquidity tier.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.025`, `score_threshold` → `50.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 105

### Summary
Low-liquidity markets are generating false positives: volume spikes without sustained price moves (execution noise) and single-contract outliers in thin markets are being flagged as signals despite lacking directional conviction.

### Next step
Introduce a volume-to-momentum filter requiring sustained price movement (≥2-3%) to accompany volume surges, with stricter thresholds in low-liquidity tiers.

### Suggested thresholds
`min_volume_delta` → `800.0`, `min_price_move` → `0.025`, `score_threshold` → `50.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 106

### Summary
Low-absolute-price markets (<$0.20) and thin-baseline markets are generating false positives from mechanical small-lot activity and modest volume surges that don't reflect genuine conviction shifts.

### Next step
Implement market-structure-aware thresholds: require higher price-move thresholds for low-price markets and enforce minimum order-size or baseline-volume ratios for thin markets, rather than relying on uniform volume and price deltas.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 107

### Summary
Sports betting markets are generating high-volume false positives due to natural liquidity swings with minimal price impact, especially in low-absolute-price tiers where mechanical activity dominates conviction signals.

### Next step
Enforce a minimum price-move threshold (2-3% for standard markets, >3% for sub-$0.20 markets) as a hard gate before emitting notable-tier signals, regardless of volume delta or composite score.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 108

### Summary
The detector is generating false positives by flagging volume spikes without sufficient price conviction, particularly in illiquid and low-volatility markets where volume changes alone do not indicate genuine demand shifts.

### Next step
Implement market-segment-specific thresholds: require minimum price moves of 2-3% for liquid sports markets, >1% for low-baseline illiquid markets, and >5% for thin baseline markets; additionally enforce a minimum order size or require price-move confirmation before escalating to 'notable' tier.

### Suggested thresholds
`min_volume_delta` → `2000.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 109

### Summary
The detector is generating excessive false positives in low-liquidity and sports betting markets, where volume spikes decouple from meaningful price conviction. Most labeled noise cases show high volume deltas with minimal price moves (0–2%), indicating the volume signal alone is insufficient.

### Next step
Enforce a minimum price-move requirement paired with market-liquidity-aware volume thresholds. For low-liquidity markets (<100 baseline contracts), require price moves ≥2–3% before triggering alerts; for sports markets with higher baseline volume, require ≥2% price moves. This decouples mechanical volume activity from genuine conviction shifts.

### Suggested thresholds
`min_volume_delta` → `1.4`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 110

### Summary
The detector is generating false positives across illiquid and low-volatility markets by triggering on volume spikes that lack price conviction. High-volume activity without meaningful price movement (or minimal price moves on ultra-low absolute volumes) is being flagged as notable/watch tier despite analyst labels of noise.

### Next step
Enforce a minimum price-move threshold that scales inversely with baseline liquidity: require >2-3% price delta for low-volume markets (<200 contracts baseline), >1% for mid-liquidity, and >0.5% for high-liquidity markets. Reject pure volume spikes without price confirmation.

### Suggested thresholds
`min_volume_delta` → `1.35`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 111

### Summary
Low-liquidity markets are generating false positives through mechanical volume/price spikes decoupled from genuine conviction. Pure volume surges without price movement and outsized percentage moves on minimal absolute volumes dominate the noise.

### Next step
Implement liquidity-aware thresholds: require minimum absolute volume (50+ shares/contracts) OR correlated external signal (social/news) for sub-100 baseline volume markets, and mandate price movement >1% alongside volume spikes in low-volatility regimes.

### Suggested thresholds
`min_volume_delta` → `1.3`, `min_price_move` → `0.01`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 112

### Summary
False positives cluster in low-liquidity markets where volume spikes occur without meaningful price conviction or in minor-league sports where thin baselines amplify mechanical artifacts. Four recent signals marked as noise/uncertain had scores ranging from 3.3 to 82.6, driven by volume alone rather than price-opinion alignment.

### Next step
Implement a liquidity-aware gating rule: require minimum price move of 2–5% (tiered by baseline volume) AND absolute volume confirmation (>50 shares or >1.3x baseline multiplier) before emitting signals on markets under 100-contract baseline volume.

### Suggested thresholds
`min_volume_delta` → `50.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 113

### Summary
False positives cluster in low-liquidity markets where volume spikes decouple from price conviction, and in micro-markets approaching expiry where quote exploration creates mechanical price moves without sustained follow-through.

### Next step
Implement liquidity-aware thresholds: require minimum price movement (1-3% depending on baseline volume) alongside volume delta, and add a sustained-conviction filter (5-min hold or multi-trade confirmation) for markets with <500 baseline contract volume.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.03`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 114

### Summary
False positives cluster in thin-liquidity markets (sports, micro-cap political) where small absolute volumes or single large quotes mechanically spike prices without reflecting genuine conviction or follow-through.

### Next step
Implement liquidity-aware thresholds: require higher price-move floors (3–5%) for low-baseline-volume markets, and add confirmation rules (sustained hold, multi-side participation, or absolute volume floors) before emitting signals.

### Suggested thresholds
`min_volume_delta` → `50.0`, `min_price_move` → `0.05`, `score_threshold` → `8.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 115

### Summary
Current detector is generating false positives across thin/low-volume markets by triggering on quote exploration, bulk liquidity events, and mechanical percentage spikes without confirming sustained conviction or actual opinion shift.

### Next step
Implement a tiered threshold system based on baseline market volume: require higher price-move thresholds (3-5%) for thin markets AND add persistence/corroboration requirements (sustained hold, order imbalance ratio, or external signal) before emitting signals.

### Suggested thresholds
`min_volume_delta` → `50.0`, `min_price_move` → `0.05`, `score_threshold` → `15.0`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 116

### Summary
Low-liquidity and micro-markets are generating false positives through mechanical volume/price spikes without follow-through or actual conviction. Most flagged signals have weak yes-probability (0.38–0.61) and analyst consensus is noise/unclear.

### Next step
Implement liquidity-aware tiering: require minimum absolute volume thresholds (500–1000 contracts depending on market tier) AND simultaneous multi-sided participation (bid-ask spread tightening or sustained >5min holds) before escalating alerts on low-baseline markets.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 117

### Summary
Low-liquidity and micro-move markets are generating false positives across watch and notable tiers. Volume spikes without sustained price conviction or multi-side participation are triggering alerts on thin baskets and near-expiry contracts.

### Next step
Implement a tiered minimum price-move requirement (3-5% for thin markets, 2% baseline for liquid) combined with volume delta multipliers (1.5x+ for watch tier, 2.0x+ for notable on sub-1000 contract baselines) to filter quote exploration from genuine conviction moves.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 118

### Summary
Low-liquidity markets and micro-moves near expiry are generating false positives despite moderate scores. Volume deltas are triggering on thin order books without sustained follow-through or multi-side confirmation.

### Next step
Implement tiered thresholds by market liquidity/volume and require sustained price hold or order imbalance confirmation for micro-moves, especially within 1 week of expiry.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`, `score_threshold` → `7.5`

### Recommendations

---

## 2026-04-06 — Advisor snapshot 119

### Summary
Low-liquidity markets are generating false positives from micro-moves and single-sided large quotes without sustained follow-through. Volume delta alone is insufficient to filter noise in thin markets.

### Next step
Implement absolute volume floor (e.g., 1000+ contracts) and multi-side participation requirement for 'watch' and 'notable' tier alerts before raising fractional thresholds.

### Suggested thresholds
`min_volume_delta` → `1.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 120

### Summary
Low-liquidity sports and political markets are generating false positives from single-print trades and quick mean-reversions that lack sustained conviction. Volume deltas alone are insufficient filters when average market volume is <1,500 contracts.

### Next step
Introduce a market-liquidity-aware persistence requirement: for markets with sub-1,500 average volume, require either (a) sustained volume over 5+ minutes, (b) multiple consecutive trades in same direction, or (c) notional trade size >threshold (e.g., 50+ contracts). This decouples low-liquidity noise from genuine flow.

### Suggested thresholds
`min_volume_delta` → `1500.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 121

### Summary
The detector is generating false positives in low-liquidity markets by triggering on single small trades or quote updates without sustained volume or price persistence, particularly in sports betting and niche prediction markets.

### Next step
Implement a market-context-aware minimum notional trade size requirement (e.g., 50+ contracts or $500+ notional) combined with a persistence check (price must hold for 2+ minutes or be confirmed by follow-up volume) to filter single-print noise.

### Suggested thresholds
`min_volume_delta` → `1500.0`, `min_price_move` → `0.04`, `score_threshold` → `4.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 122

### Summary
The detector is triggering watch-tier signals on low-liquidity sports markets driven by quote updates without fills, single-print noise, and quick mean-reversions. These are structurally different from actionable flow signals.

### Next step
Implement market-microstructure filters before scoring: require either (1) executed trade count ≥1 in trailing period, OR (2) sustained multi-tick price persistence (>2–3 min), OR (3) volume multiplier ≥3x baseline for low-volume venues (<1500 baseline). This layers a reality check on top of threshold tuning.

### Suggested thresholds
`min_volume_delta` → `2000.0`, `min_price_move` → `0.03`, `score_threshold` → `3.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 123

### Summary
The detector is triggering on low-liquidity sports markets with quote-only activity and single-print noise rather than genuine informed flow. All three recent false positives lack sustained execution or asymmetric fill patterns.

### Next step
Add a market-liquidity-aware gating rule: require either (1) minimum executed trade count in trailing window (e.g., ≥2 fills) OR (2) volume delta must exceed 3x the market's baseline average volume. This filters quote-only noise while preserving real flow in low-liquidity venues.

### Suggested thresholds
`min_volume_delta` → `1500.0`, `min_price_move` → `0.04`, `score_threshold` → `4.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 124

### Summary
False positives are clustering in low-liquidity sports markets where quote updates without executed fills and single-print trades are triggering watch-tier signals despite minimal actionable flow.

### Next step
Require evidence of executed volume (non-zero trade count) and/or sustained price persistence across multiple ticks before emitting watch-tier signals, especially in markets with low baseline liquidity.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.04`, `score_threshold` → `3.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 125

### Summary
Low-liquidity minor league sports markets are generating false positives on modest volume moves (2748–6998 contracts) with minimal price action (2% moves), scoring just above threshold despite unclear directional intent.

### Next step
Implement liquidity-aware thresholds: require higher volume delta multipliers and minimum trade counts for low-absolute-volume markets, rather than applying uniform thresholds across all venues.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 126

### Summary
Low-liquidity markets are generating false positives with large volume deltas but minimal price moves and low trade counts. The detector is triggering on quote-driven activity and single-sided flows rather than genuine demand shifts.

### Next step
Implement a trade-count and trade-to-quote ratio filter before escalating watch-tier alerts, particularly for markets with priceΔ < 0.03 and volΔ > 2000.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 127

### Summary
Low-liquidity and niche markets (minor league sports, prediction markets with small trade sizes) are generating false positives through quote-refresh noise and single-sided volume spikes that don't reflect genuine demand-driven moves.

### Next step
Implement market-segment filtering: require minimum trade count (3+), minimum trade size (>100 shares), and trade-to-quote ratio (>0.3) before escalating watch-tier alerts in illiquid markets (volume_delta < 5000 or price_delta < 0.03).

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 128

### Summary
Low-liquidity niche markets (minor league sports, prediction markets) are generating false positives through quote-refresh noise and quote-driven price moves rather than genuine demand-driven flow.

### Next step
Implement market-tier-aware filtering: require actual trade count and trade-to-quote ratio validation before escalation, especially for watch-tier alerts in illiquid venues.

### Suggested thresholds
`min_volume_delta` → `1.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 129

### Summary
System is triggering false positives on low-liquidity and niche markets (sports betting, prediction markets) where quote volume and small isolated trades create signal noise without genuine demand-driven price movement.

### Next step
Implement a trade-quality filter requiring minimum actual fill count (3+ trades) and trade-to-quote ratio (>0.3) before escalating alerts, especially in low-liquidity venues. This targets the root cause: quote refresh noise and isolated small orders that don't reflect sustained market conviction.

### Suggested thresholds
`min_volume_delta` → `1.5`, `score_threshold` → `3.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 130

### Summary
Low-liquidity markets are generating false positives due to amplified noise from minimal baseline volumes and trade counts. Small absolute volume deltas and price moves trigger high scores when baselines are tiny, despite lacking statistical significance.

### Next step
Implement a liquidity gate: require minimum baseline volume (10-20 contracts per period) or minimum trade count (≥10 trades) before applying spike detection thresholds. This filters out inherently noisy low-liquidity regimes.

### Suggested thresholds
`score_threshold` → `750.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 131

### Summary
Low-liquidity markets are generating false positives from mechanical market-making and micro-trades with inflated score metrics due to tiny baselines. The detector needs liquidity-aware filtering rather than uniform thresholds.

### Next step
Introduce a minimum baseline volume threshold (10-20 contracts per period) and require trade-count or notional-value minimums before spike detection activates in low-liquidity venues, rather than relying on volume-delta ratios alone.

### Suggested thresholds
`min_volume_delta` → `5000.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 132

### Summary
Low-liquidity markets (sports betting, thin prediction markets) are generating false positives due to tiny baselines that amplify noise and mechanical market-making moves. Volume and price deltas appear noisy when baseline contract counts are <10 and notional values are minimal.

### Next step
Implement a market-liquidity awareness layer: require minimum baseline volume thresholds (10-20 contracts/period) before spike detection activates, and scale delta multipliers (3x baseline instead of 2x) for low-liquidity venues.

### Suggested thresholds
`min_volume_delta` → `3.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 133

### Summary
Low-liquidity markets (sports, prediction) are generating false positives from micro-moves and quote-driven activity. High score inflation occurs when tiny baseline volumes amplify noise, and single-trade mechanics trigger detection despite lack of directional significance.

### Next step
Implement a liquidity-gating rule: require minimum baseline volume (10–20 contracts/period) and minimum trade count (5+ trades) before spike detection is eligible, with separate thresholds for low vs. standard liquidity tiers.

### Suggested thresholds
`min_volume_delta` → `1500.0`, `min_price_move` → `0.05`, `score_threshold` → `50.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 134

### Summary
False positives cluster in low-liquidity markets where tiny baseline volumes and mechanical market-making create outsized score inflation from micro-moves. The detector lacks market-structure awareness and trades mechanical volume/price ratios for signal quality.

### Next step
Implement a baseline volume floor (10-20 contracts minimum per period) before calculating spike multipliers, preventing baseline amplification in thin markets. This single change addresses the root cause across all five signals.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `5.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 135

### Summary
Low-liquidity markets (sports, prediction) are generating false positives due to quote-driven noise and mechanical market-making activity dominating small baselines. High score outputs from tiny volume deltas are masking low analyst confidence (yes≤0.62).

### Next step
Implement a trade-volume-to-quote-volume ratio filter (minimum 20% trade fill ratio) and enforce minimum baseline volume thresholds (10-20 contracts per period) before spike detection is eligible, especially for watch/notable tiers.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `12.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 136

### Summary
The detector is generating false positives primarily in low-liquidity markets (sports betting, thin political/entertainment markets) where quote-driven noise and small mechanical trades trigger signals despite low analyst confidence (yes≤0.62). Volume deltas are high in absolute terms but not validated by executed trade volume or meaningful price moves.

### Next step
Implement a trade-volume-to-quote-volume ratio filter (minimum 20% trade fill ratio) as a gating condition before emitting watch/notable tier signals, especially for markets with baseline volume <5000 contracts.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `6.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 137

### Summary
Low-liquidity markets are generating false positives from quote-driven noise and mechanical market-making activity, even when actual trade volume is minimal relative to quote volume.

### Next step
Implement a trade-volume-to-quote-volume ratio filter requiring executed trades to represent at least 20% of associated quote volume before spike qualification, combined with minimum executed trade count (10+ contracts) for watch-tier signals.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `3.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 138

### Summary
Low-liquidity markets (sports betting) are generating false positives from quote-driven volume spikes that lack meaningful price movement or executed trade volume.

### Next step
Implement a trade-volume-to-quote-volume ratio filter requiring at least 20% of quote volume to be executed trades before emitting signals in thin markets.

### Suggested thresholds
`min_volume_delta` → `2000.0`, `min_price_move` → `0.03`, `score_threshold` → `5.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 139

### Summary
Both false positives stem from quote-driven noise in thin/low-liquidity markets where large quote volume deltas drive spike scores without corresponding executed trade volume, creating illusion of real flow.

### Next step
Implement executed trade volume validation: require minimum executed contracts AND enforce trade-volume-to-quote-volume ratio floor to distinguish genuine flow from quote layering/spoofing in thin markets.

### Suggested thresholds
`score_threshold` → `5.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 140

### Summary
Single-contract outliers in thin markets (baseline volume <600) are generating false positives. The detector is picking up low-conviction noise with modest volume deltas (576–592) and small price moves (2–5%) that lack sustained conviction.

### Next step
Implement liquidity-aware thresholds: require higher volume delta multipliers and/or concurrent price-move minimums for markets below a baseline volume floor, rather than applying uniform thresholds across all liquidity regimes.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 141

### Summary
Low-liquidity markets are generating false positives via percentage-based volume deltas on micro-trades and single-contract outliers that lack sustained conviction or market depth.

### Next step
Introduce absolute volume floor (minimum contract count) independent of percentage-based delta, and require corroborating trades within a time window to validate signal strength in thin markets.

### Suggested thresholds
`score_threshold` → `7.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 142

### Summary
Low-liquidity binary markets are generating false positives via small absolute volume trades that appear significant in percentage terms. Both signals flagged the same market with marginal price moves (0.17–0.18) and modest volume deltas (~1,450 contracts) that lack conviction or sustained follow-through.

### Next step
Introduce minimum absolute volume thresholds (not just percentage deltas) and require sustained price hold duration post-spike to filter noise in thin markets.

### Suggested thresholds
`min_price_move` → `0.25`, `score_threshold` → `13.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 143

### Summary
Low-liquidity and low-volume markets are generating false positives due to outsized score impacts from small absolute trades. The detector lacks mechanisms to distinguish meaningful flow from noise in thin markets.

### Next step
Introduce market-liquidity-aware thresholds: require either (1) absolute volume floor (5000+ contracts) OR (2) sustained price hold (5+ minutes) to emit 'signal' tier, with 'notable' tier reserved for lower confidence detections.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `score_threshold` → `8.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 144

### Summary
Low-liquidity markets (sports betting, binary outcomes) are generating false positives when small absolute trade counts or single-tick price moves trigger volume and score thresholds. The detector lacks context-awareness for market structure and trade sustainability.

### Next step
Introduce market-structure classification (liquidity tier) that enforces stricter thresholds for low-liquidity markets: require either sustained price hold (5+ min) or absolute volume floor (5,000+ contracts), whichever is applicable.

### Suggested thresholds
`min_volume_delta` → `3500.0`, `min_price_move` → `0.03`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 145

### Summary
The detector is generating false positives across contracts with varying liquidity by treating raw volume deltas and price moves as signal-worthy without accounting for execution quality, market depth, or temporal persistence. Low-liquidity markets and thin contracts are particularly prone to noise.

### Next step
Introduce an execution-quality filter requiring actual traded volume to represent a meaningful % of quoted volume (5-10% for standard contracts, >50% for low-liquidity markets), and add a temporal persistence requirement (sustained price hold or baseline volume multiple) before emitting 'signal' or 'notable' tier alerts.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `score_threshold` → `13.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 146

### Summary
The detector is generating false positives in low-liquidity markets (sports betting) and thin contracts where small absolute volume changes trigger signals despite weak execution quality. The KXTOPCHEF signal had <0.17% execution rate, while sports betting signals lack sustained conviction or correlated external data.

### Next step
Implement an execution-quality filter requiring actual traded volume to be a meaningful percentage of quoted volume (5-10% for standard contracts, 50%+ for low-liquidity markets), combined with either sustained price movement or volume exceeding 5x baseline.

### Suggested thresholds
`score_threshold` → `15.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 147

### Summary
Low-liquidity markets (sports betting, watch-tier contracts) are generating false positives from modest volume/price moves that lack execution conviction or sustained conviction. The detector is triggering on noise in thin markets without distinguishing real flow from tick-level fluctuations.

### Next step
Introduce execution-rate validation: require actual traded volume to be ≥5-10% of quoted volume, and for watch-tier/low-liquidity markets, enforce either >50% volume delta above baseline OR sustained multi-tick price moves OR correlated external signals (not just single-tick moves).

### Suggested thresholds
`min_volume_delta` → `3600.0`, `min_price_move` → `0.03`, `score_threshold` → `6.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 148

### Summary
Low-liquidity markets (sports betting, thin order books) are generating false positives due to single small trades triggering volume and price deltas without meaningful execution. The detector lacks context-awareness for market microstructure (execution rate, baseline volume, sustained movement).

### Next step
Implement market-tier-specific rules that require either sustained price movement (3+ consecutive ticks in same direction) OR execution volume >50% above baseline (or >5x for ultra-thin markets), rather than relying solely on absolute volume delta and single-tick price moves.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `3.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 149

### Summary
Low-liquidity and sports-betting markets are generating false positives from small trades and thin volume spikes that lack meaningful execution or sustained directional conviction. The detector is over-sensitive to absolute volume deltas in markets with naturally low baselines.

### Next step
Implement tiered thresholds by market liquidity/baseline volume, and require execution-rate validation (actual traded volume as % of quoted volume) before emitting signals in lower-activity contracts.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 150

### Summary
Detector is generating false positives in thin/low-liquidity markets by treating small absolute volume moves and minor price ticks as meaningful signals. The core issue is lack of baseline-relative thresholds and execution-quality filters.

### Next step
Introduce baseline-relative volume thresholds (require volume delta ≥50% of baseline) and execution-quality filters (minimum 5-10% execution rate on quoted size) before emitting signals, especially in watch/notable tier contracts.

### Suggested thresholds
`min_volume_delta` → `2000.0`, `min_price_move` → `0.03`, `score_threshold` → `5.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 151

### Summary
Thin-market false positives dominate recent noise signals. Small absolute volume deltas and minimal price moves in low-liquidity venues are triggering alerts despite weak predictive value (yes probabilities 0.37–0.58).

### Next step
Introduce baseline-relative volume thresholds (e.g., volume delta ≥50% of baseline) and minimum absolute trade size guards for low-activity markets, rather than relying on absolute volume deltas alone.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `4.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 152

### Summary
False positives concentrated in low-liquidity markets where quote updates and small individual trades trigger alerts without genuine flow conviction. Pattern shows thin markets with baseline daily volumes under 10 trades generating noise across both notable and watch tiers.

### Next step
Implement execution-quality filters: require minimum trade count (3-5 executions) or volume intensity (≥1.5-2x baseline) rather than relying solely on volume delta and price move thresholds, which are insufficient for thin markets.

### Recommendations

---

## 2026-04-07 — Advisor snapshot 153

### Summary
Low-liquidity markets are generating false positives from quote updates and small isolated trades that lack execution volume or sustained momentum. The detector is too sensitive to single-tick moves in thin markets.

### Next step
Add execution-quality gates: require either minimum trade count (3-5 unique executions) OR sustained directional price movement (3+ consecutive ticks) OR volume spike relative to baseline (50%+ of typical daily volume), with market-liquidity-aware thresholds.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `7.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 154

### Summary
False positives are clustering in low-liquidity markets (sub-10 daily trades) where small absolute volume moves and quote updates trigger signals despite minimal genuine flow conviction.

### Next step
Implement execution-count and baseline-relative volume filters before score evaluation, rather than tuning score thresholds alone. Thin markets need structural guards, not just higher numeric bars.

### Suggested thresholds
`score_threshold` → `7.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 155

### Summary
False positives cluster in thin markets where quote activity and minimal executed volume trigger alerts despite low conviction (yes probabilities 0.09–0.39). Signals lack sufficient execution depth to validate genuine flow.

### Next step
Require minimum executed trade count (3–5 unique executions) rather than relying solely on volume delta, especially in markets with <10 baseline daily trades.

### Suggested thresholds
`score_threshold` → `6.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 156

### Summary
False positives are concentrated in thin markets where quote activity and volume deltas lack genuine execution conviction. Both recent noise signals show high volume deltas but low price moves and/or low trade counts, indicating quote-stuffing rather than real directional commitment.

### Next step
Introduce a minimum executed trade count filter (3-5 unique executions) as a hard gate before emitting signals, especially for markets with <10 daily trades or low price conviction.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.03`, `score_threshold` → `4.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 157

### Summary
False positives are driven by quote refreshes and volume delta inflation in thin markets where executed trade volume is minimal. The detector is triggering on quote-only activity rather than genuine conviction-driven flow.

### Next step
Implement executed trade volume validation: require minimum N unique trade executions (not just quoted volume delta) to trigger spike detection, with stricter thresholds in low-liquidity markets (<10 daily trades).

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `3.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 158

### Summary
False positives are dominated by quote-only events and micro-lot executions in thin markets, where volume spikes lack accompanying price conviction or genuine trade execution.

### Next step
Require minimum executed trade count (3-5 unique fills) alongside volume delta, and filter quote-only events by enforcing traded_volume > baseline_volume threshold, especially for markets under $0.10 and <10 daily trades.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.005`, `score_threshold` → `6.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 159

### Summary
False positives cluster around quote-heavy events and thin-market micro-movements lacking execution conviction. Volume spikes without sustained price action or genuine trades are dominating the watch/notable tiers.

### Next step
Implement executed_trade_volume_ratio filter: require minimum 40-50% of volume delta to come from actual executed trades (not just quote orders), with special stringency in markets under 10 daily trades or <0.10 price levels.

### Suggested thresholds
`min_volume_delta` → `10000.0`, `min_price_move` → `0.005`, `score_threshold` → `5.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 160

### Summary
False positives are dominated by quote-management events and thin-market micro-movements lacking genuine conviction. Volume deltas are inflated by single large orders or quote refreshes rather than executed trades.

### Next step
Implement executed-trade volume filtering: require that actual filled trades comprise ≥40% of volume delta, rejecting quote-only or quote-heavy events before scoring.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `3.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 161

### Summary
High false-positive rate in thin/low-liquidity markets where volume spikes occur without corresponding price movement, particularly in college sports and far-dated events. Large score inflation (3M+) with zero price delta indicates algorithmic noise rather than genuine flow.

### Next step
Implement a correlation requirement: volume spikes must be accompanied by minimum price movement (>0.5%) OR absolute volume threshold (>100 contracts) depending on market liquidity tier, to filter rebalancing noise from informed flow.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.005`, `score_threshold` → `500.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 162

### Summary
False positives cluster in thin/niche markets where volume spikes occur without meaningful price movement, and in low-liquidity college sports markets where algorithmic rebalancing creates noise.

### Next step
Require correlated volume AND price movement in low-liquidity contexts: enforce minimum price_move threshold of 0.5% for markets with baseline volume <1000, rather than relying on volume multipliers alone.

### Suggested thresholds
`min_volume_delta` → `50.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 163

### Summary
False positives cluster in low-liquidity, thin markets where volume spikes occur without sustained price conviction. Queue noise, algorithmic rebalancing, and single-tick micro-moves are triggering detections despite weak fundamentals.

### Next step
Enforce a joint volume-price constraint: require both spike_min_volume_delta AND spike_min_price_move to be satisfied simultaneously, with absolute volume floors for thin markets, rather than treating them as independent OR conditions.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.05`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 164

### Summary
False positives cluster in low-liquidity markets where volume spikes occur without meaningful price conviction (0-1% moves). Mechanical rebalancing and queue noise are being flagged as signals despite analyst consensus that these lack genuine information content.

### Next step
Enforce a minimum price-move floor of 0.5-1.0% paired with volume delta, and add liquidity-aware absolute volume thresholds rather than relying on relative multipliers alone. This filters algorithmic noise while preserving real conviction flow.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 165

### Summary
High false-positive rate in low-liquidity markets where large volume spikes occur without meaningful price movement, often representing algorithmic rebalancing rather than genuine conviction shifts.

### Next step
Implement a price-movement floor correlated with volume spikes: require minimum price moves of 0.5–2% for watch/notable tiers, and 2–3% for high-conviction claims in thin markets. Decouple volume delta from score when price move is absent.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 166

### Summary
The detector is generating false positives primarily from high-volume, price-neutral activity in low-liquidity markets (portfolio rebalancing, queue noise) and single large quotes in micro-cap markets. Price movement is not correlating with volume spikes, causing noise to rank as highly as genuine conviction shifts.

### Next step
Enforce a minimum price-move requirement (0.5–3% depending on liquidity tier) correlated with volume spikes, rather than treating volume and price as independent scoring inputs. This single change will filter 70%+ of the labeled noise while preserving legitimate flow signals.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.01`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 167

### Summary
High false-positive rate driven by volume spikes decoupled from price movement and low-conviction micro-markets. Most noise signals show 0–1% price deltas with large volume swings, indicating algorithmic rebalancing rather than genuine flow.

### Next step
Enforce minimum price-move thresholds (0.5–3% depending on liquidity tier) as a hard filter, not just a scoring component. Volume-only signals without correlated price action are predominantly noise.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 168

### Summary
The detector is generating high false positives in low-liquidity markets where large volume spikes occur without proportional price movement, or where small price ticks are amplified by thin order books. Most false positives cluster around zero or near-zero price moves paired with massive volume deltas, suggesting volume-only triggers are insufficient.

### Next step
Implement a minimum price-move floor (0.5–2% depending on market liquidity tier) that must correlate with volume spikes; decouple volume-only signals from higher conviction tiers. Require trade-count validation or sustained multi-minute price holds rather than single-tick moves.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.015`, `score_threshold` → `8.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 169

### Summary
The detector is generating false positives on price-neutral high-volume events (mechanical rebalancing) and low-conviction micro-moves in thin markets, particularly in niche sports and event prediction categories where liquidity is sparse.

### Next step
Implement a joint price-volume filter: require minimum price move of 2% OR volume delta >8x baseline with sustained (5+ minute) directional pressure, rather than treating volume and price moves as independent signals. This filters mechanical rebalancing while preserving genuine conviction shifts.

### Suggested thresholds
`min_price_move` → `0.02`, `score_threshold` → `7.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 170

### Summary
The detector is generating false positives in low-liquidity markets by flagging high-volume activity with minimal or zero price moves, and by over-weighting single large quotes on thin order books without sustained directional conviction.

### Next step
Introduce a tiered rule system that requires price-move correlation with volume spikes: for watch/notable tiers, enforce minimum 0.5–2% price moves paired with volume deltas, and validate with trade count or time-window persistence rather than instantaneous quote activity.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 171

### Summary
The detector is generating excessive false positives on low-liquidity markets by flagging large volume deltas without corresponding price moves, and treating mechanical rebalancing/quote-splitting as informed flow.

### Next step
Implement a liquidity-aware coupling rule: require minimum price move (±0.5-2% depending on market type) paired with volume spike, and validate with trade-count minimums for thin markets rather than relying on volume delta alone.

### Suggested thresholds
`min_price_move` → `0.015`, `score_threshold` → `5.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 172

### Summary
Detector is triggering on algorithmic order splits, quote noise, and extreme-priced thin markets without price confirmation. False positives cluster in low-liquidity, low-trade-count venues where volume deltas alone lack signal value.

### Next step
Introduce market-context normalization: require minimum trade count (5+) and time-window validation (>5min sustained) before flagging, especially for contracts with <10 daily trades or prices >0.80/0.20.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `6.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 173

### Summary
False positives cluster in thin/low-conviction markets where algorithmic execution, quote noise, and extreme pricing create high scores without genuine informed flow. The detector lacks market-context awareness and time-window validation.

### Next step
Implement market-liquidity normalization: require volume delta as a multiple of baseline daily volume (not raw delta), paired with time-window enforcement (≥5 min aggregation) and price-move validation that scales with conviction level.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `6.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 174

### Summary
The detector is generating false positives in thin/low-liquidity markets by treating algorithmic order splits and quote noise as informed flow. Key issues: raw volume deltas don't normalize for contract liquidity; price moves are weighted equally regardless of conviction; time-window requirements are missing.

### Next step
Implement market-context-aware thresholds: require higher price-move minimums (2-5%) for low-conviction markets, normalize volume deltas by baseline trade count rather than raw volume, and enforce minimum 5-minute concentration windows to filter millisecond-level algorithmic noise.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `6.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 175

### Summary
The detector is triggering on thin-market volume moves without price conviction and on extreme-probability markets where small absolute moves are noise. False positives cluster when volume deltas lack supporting price action or occur in low-liquidity/high-conviction contexts.

### Next step
Implement context-aware thresholds: require price_move ≥ 2% OR (volume_delta ≥ 8x contract baseline AND price_move > 0%) for low-liquidity markets; require price_move ≥ 2% for markets with probability > 0.80.

### Suggested thresholds
`min_price_move` → `0.02`, `score_threshold` → `6.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 176

### Summary
Volume spikes without accompanying price movement are generating false positives across both ultra-short-duration and low-liquidity markets, suggesting the detector is too sensitive to isolated order flow that lacks conviction.

### Next step
Implement a conjunctive filter: require either (a) meaningful price movement paired with volume spike, OR (b) volume spike exceeding a higher absolute threshold. This prevents small orders and thin-market noise from triggering signals.

### Suggested thresholds
`min_volume_delta` → `35.0`, `min_price_move` → `0.005`, `score_threshold` → `5.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 177

### Summary
Volume spikes without accompanying price movement are generating false positives across diverse market types (low-conviction crypto, ultra-short duration, thin niche sports). The detector is triggering on mechanical or uninformed flow that lacks directional conviction.

### Next step
Enforce a joint condition: require meaningful price movement (0.5-2% depending on market liquidity/duration) to accompany volume spikes, rather than accepting volume or price movement independently.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `6.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 178

### Summary
High false-positive rate across diverse market types driven by volume spikes decoupled from meaningful price movement. Current thresholds trigger on 1% price moves with pure volume signals, conflating mechanical rebalancing and thin-book noise with genuine directional intent.

### Next step
Introduce market-context coupling: require price_move >= 2% OR (price_move >= 1% AND directional_flow_ratio >= 0.70) to gate volume-only signals, stratified by market liquidity tier and time horizon.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 179

### Summary
The detector is generating false positives across low-liquidity and thin-book markets by triggering on volume spikes decoupled from meaningful price momentum. High volume deltas without corresponding price moves (1% or less) are consistently labeled as noise even when score is elevated.

### Next step
Implement a strict correlation rule: require price_move to exceed 2% OR volume_delta to be accompanied by sustained directional flow bias (>70% one-sided) depending on market liquidity tier. Decouple volume and price thresholds by market type rather than using global minimums.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 180

### Summary
False positives cluster in thin-liquidity markets where volume spikes lack price conviction or sustained directional bias. The detector is triggering on mechanical rebalancing, isolated whale clusters, and single large orders that don't reflect genuine market consensus.

### Next step
Implement market-liquidity-aware tiering: require price moves >2% AND sustained directional flow alignment (>70% volume to one side) for low-liquidity markets (<100 baseline volume); for whale-cluster detection, raise minimum trade count threshold to 4-5 and require 1% baseline volume cumulative rather than 0.4%.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 181

### Summary
High false-positive rate driven by volume spikes decoupled from price action and trade confirmation, especially in thin markets and short timeframes where mechanical rebalancing dominates.

### Next step
Implement tiered minimum price-move requirements by market liquidity/conviction level, and require trade-level confirmation (executed trades within 5-10min window) before emitting signals on volume deltas.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 182

### Summary
High-confidence and thin markets are generating false positives from mechanical volume spikes decoupled from informed trading. Single large orders in stable markets and retail scatter in low-liquidity venues are triggering alerts despite minimal price conviction.

### Next step
Introduce market-context-aware thresholds: require higher price-move thresholds (2-3%) in low-volume markets and high-confidence markets (yes/no >0.90), and raise absolute volume minimums for ultra-short timeframes (15m). Decouple volume and price requirements rather than treating them as independently sufficient.

### Suggested thresholds
`min_volume_delta` → `150.0`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 183

### Summary
The detector is firing on volume spikes decoupled from price action across diverse market types—low-conviction binary markets, stable high-conviction finals, ultra-short timeframes, and thin long-tail sports. Price movement is either absent or minimal (0–1%), suggesting liquidity provision and scattered retail trades rather than informed flow.

### Next step
Enforce a minimum price-move requirement (0.5–3% depending on market conviction and timeframe) alongside volume spikes. Volume alone is insufficient; require sustained directional pressure to validate signal.

### Suggested thresholds
`min_volume_delta` → `150.0`, `min_price_move` → `0.01`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 184

### Summary
The detector is generating excessive false positives on short-duration markets (especially 15m BTC) by flagging high-volume trades at zero or near-zero price impact, which reflect mechanical repositioning rather than directional conviction. Long-tail and stable markets also show noise from single large orders without sustained momentum.

### Next step
Require minimum price move correlated with volume spikes across all market types, with stricter thresholds for ultra-short horizons (15m) and thin markets. Use market-specific sensitivity tuning based on baseline volatility and conviction level.

### Suggested thresholds
`min_volume_delta` → `1.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 185

### Summary
The detector is generating excessive false positives on 15-minute BTC micro-markets by flagging large volume deltas without concurrent price movement. Most noise signals show volΔ=400-852 with priceΔ=0.0%, indicating mechanical/inventory repositioning rather than informed directional trades.

### Next step
Require minimum price movement (≥0.5% for whale-cluster tier, ≥1% for watch tier) concurrent with volume spikes as a gating filter before emitting any signal, especially on markets with <1-hour expiry windows.

### Suggested thresholds
`min_volume_delta` → `1.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 186

### Summary
Whale-cluster signals on 15-minute BTC micro-markets are firing with high scores (8–30) despite zero price impact, creating false positives. The detector treats large absolute volume deltas as informative even when they fail to move the market, indicating mechanical/algo positioning rather than conviction.

### Next step
Require minimum price movement (≥0.5–1.0%) concurrent with whale-cluster volume spikes on short-horizon markets (≤15min); decouple volume-delta scoring from price-impact scoring so that high volume without market movement does not accumulate signal strength.

### Suggested thresholds
`min_volume_delta` → `150.0`, `min_price_move` → `0.01`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 187

### Summary
The detector is generating excessive false positives on 15-minute BTC micro-markets and other short-duration contracts by flagging volume spikes with zero or minimal price impact. The core issue is that whale-cluster signals lack meaningful price conviction, indicating mechanical order flow rather than informed positioning.

### Next step
Require minimum price movement (≥0.5-1.0%) concurrent with volume spikes on markets with duration ≤15 minutes, or equivalently raise volume_delta threshold to represent >5-10% of baseline and add a price-impact filter to all whale-cluster detections.

### Suggested thresholds
`min_volume_delta` → `1.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 188

### Summary
Whale-cluster signals on 15-minute micro-markets are generating excessive false positives due to flagging volume spikes without corresponding price movement or baseline-relative thresholds. Most noise cases show zero price delta despite high scores, indicating mechanical/inventory repositioning rather than informed directional trades.

### Next step
For whale-cluster tier on short timeframes (≤15min): require minimum price move of ±0.5% concurrent with volume delta, OR enforce volume delta as percentage of baseline (≥5-10%) rather than absolute units, to filter out coordination signals lacking market conviction.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 189

### Summary
Whale-cluster detection on 15-minute micro-markets is generating excessive false positives by flagging statistical trader clustering without accompanying price impact or baseline-relative volume. The detector conflates coordination signals with mechanical order flow.

### Next step
For whale-cluster tier signals on markets with expiry ≤15 minutes: require EITHER (1) volume delta >5% of recent baseline AND price move ≥0.5%, OR (2) volume delta >10% of baseline alone. Add a price-impact filter: if volume delta exceeds 1.0x baseline, price must move ≥1% in the direction of cluster dominance.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 190

### Summary
The detector is generating excessive false positives on 15-minute BTC micro-markets by flagging whale-cluster activity with zero price impact and sub-1% volume deltas relative to baseline. High statistical scores (8.0–29.0) are being assigned to mechanical positioning trades that lack market conviction or directional evidence.

### Next step
Implement a dual-gate requirement for whale-cluster signals on short-duration markets (≤15min): require EITHER (1) volume delta ≥5% of recent baseline AND price move ≥0.5%, OR (2) volume delta ≥10% of baseline with multi-directional confirmation across ≥3 price levels. This filters coordinated noise while preserving genuine informed flow.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 191

### Summary
The detector is generating excessive false positives on whale-cluster tier alerts, particularly for 15-minute micro-markets and high-baseline assets, by flagging volume anomalies that lack measurable price impact or economic significance.

### Next step
Implement a dual-gate filter: require whale-cluster signals to satisfy EITHER (volume_delta > 5-10% of baseline AND price_move >= 0.5%) OR (price_move >= 1.0%), with stricter thresholds on short-duration (≤15min) contracts. This eliminates mechanical order clustering unaccompanied by conviction.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 192

### Summary
Whale-cluster detector is generating false positives on 15-minute ultra-short-dated markets by flagging volume deltas of 400–850 units with zero price impact. The detector treats statistical clustering of small trades as signal-worthy despite lacking economic conviction or market impact.

### Next step
For whale-cluster tier on short-duration markets (≤15min), require either (1) volume delta >5% of baseline volume OR (2) price move ≥0.5–1.0% alongside any cluster detection. This filters mechanical algo clustering from informed positioning.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 193

### Summary
The detector is generating excessive false positives in ultra-short-dated micro-markets (15m BTC) and high-baseline markets (MARMAD) by flagging volume spikes with zero or minimal price impact. Genuine signals show coordinated directional flow with measurable price moves; noise cases show large absolute volumes that are negligible relative to baseline.

### Next step
Implement a market-context-aware volume delta threshold: require volume_delta to exceed a percentage of baseline (5-10% for 15m markets, 15%+ for high-baseline >7M/24h markets) AND enforce a price-move floor (≥0.5%) when volume delta exceeds baseline, rather than flagging on coordination alone.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 194

### Summary
The detector is generating high false positives on ultra-short-duration markets (15-min BTC binaries, thin UConn betting) by triggering whale-cluster alerts on small absolute volume deltas with zero price impact, confusing mechanical order placement and rebalancing with informed trading.

### Next step
Implement a tiered baseline-relative volume threshold: require volume_delta to exceed 1% of market baseline for whale-cluster tier signals, and mandate concurrent or immediate directional price impact (≥1-2%) to distinguish informed positioning from mechanical noise.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 195

### Summary
Whale-cluster detector on 15-minute BTC markets is generating high false positives by triggering on volume spikes without price impact or directional conviction. The majority of flagged signals show zero price movement (priceΔ=0.0) despite high volume deltas, indicating mechanical order flow rather than informed positioning.

### Next step
Require correlated price movement (minimum 0.5–1.0%) or sustained directional order imbalance (>70% skew) to confirm whale-cluster signals on ultra-short timeframes, rather than relying on volume clustering alone.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.005`, `score_threshold` → `12.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 196

### Summary
Whale-cluster detector is generating high false positives on 15-minute BTC markets by flagging coordinated volume without price conviction. The majority of noise cases show zero or near-zero price movement despite high score and volume delta, indicating the detector is capturing algorithmic execution noise and liquidity-testing behavior rather than informed directional flow.

### Next step
Require minimum correlated price movement (≥0.5%) to accompany whale-cluster signals on ultra-short timeframes (≤15m), or filter alerts where volume delta is <5% of baseline AND price move is 0%. This single rule will eliminate most false positives while preserving genuine informed flow signals.

### Suggested thresholds
`min_volume_delta` → `5.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 197

### Summary
Whale-cluster detector is generating excessive false positives on 15-minute ultra-short markets by flagging coordinated quote activity and mechanical micro-trades with zero or negligible price impact. The core issue: volume-delta signals alone, without price correlation or baseline-relative thresholds, cannot distinguish informed flow from liquidity provision and algorithmic noise.

### Next step
Require whale-cluster signals to satisfy at least one of: (1) price move ≥0.5–1.0%, or (2) volume delta ≥5–10% of baseline, or (3) directional consensus (≥70% one-sided volume). This filters quote-driven false positives while preserving genuine informed-flow signals.

### Suggested thresholds
`min_volume_delta` → `0.08`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 198

### Summary
The whale-cluster detector is generating overwhelming false positives on 15-minute ultra-short-duration markets by flagging high-frequency quote activity and mechanical order clustering without corresponding price conviction or impact. The two genuine signals in the dataset had large volume deltas (>500) and directional persistence, while 18 of 20 labeled signals show zero or negligible price moves despite high volume delta and confidence scores.

### Next step
Require minimum price move of ≥0.5% OR volume delta >5% of baseline (not absolute count) to trigger whale-cluster signals on markets with <1h expiry. This filters quote-driven noise while preserving informed directional flow.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 199

### Summary
Whale-cluster detector is severely oversensitive to ultra-short-duration markets (15min BTC) and low-liquidity venues, firing on sub-1% baseline volume deltas and quote activity with zero or negligible price impact. The majority of false positives come from mechanical high-frequency noise rather than informed directional conviction.

### Next step
Implement market-class-specific thresholds: require volume delta ≥5% of baseline for 15min markets and ≥3% for sub-10% probability low-liquidity markets before flagging whale-cluster signals. Additionally, require minimum price move of ≥0.5% or sustained multi-tick follow-through to accompany volume spikes.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 200

### Summary
Ultra-short-duration markets (15-min) are generating high-confidence whale-cluster signals (score=8.0) with minimal or zero price impact and negligible volume relative to baseline, indicating quote-driven false positives rather than genuine directional flow.

### Next step
Introduce market-duration and liquidity-aware thresholds: require volume delta >5% of baseline AND non-zero price impact (>0.5%) for whale-cluster alerts on markets with ≤15min expiry; alternatively, gate whale-cluster signals on short-duration contracts by requiring sustained multi-tick pressure or directional imbalance (>60/40 side ratio) rather than single-burst detection.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 201

### Summary
Whale-cluster signals in ultra-short-dated (15m) and low-liquidity markets are generating noise due to statistical clustering and quote activity without price impact or conviction. The detector is flagging sub-1% baseline volume spikes with zero or minimal price deltas as high-confidence signals.

### Next step
Implement market-context-aware filtering: require either (1) price delta >0.5% OR (2) volume delta >5% of baseline for whale-cluster alerts, with stricter enforcement on ultra-short windows (≤15m expiry) and low-liquidity baselines.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 202

### Summary
The whale-cluster detector is generating excessive false positives on ultra-short-dated markets (15-minute expiry) and low-liquidity venues by flagging statistically significant volume clusters that lack meaningful price impact or baseline-relative magnitude. Analysts consistently recommend filtering signals where price movement is near-zero and volume delta is below 5-10% of baseline.

### Next step
Implement a composite filter requiring whale-cluster signals to satisfy at least one of: (1) price_move ≥ 0.5%, (2) volume_delta ≥ 10% of baseline, or (3) directional flow imbalance ≥ 60/40 side ratio. This will eliminate mechanical order-placement noise while preserving informed flow.

### Suggested thresholds
`min_volume_delta` → `0.1`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 203

### Summary
False positives dominate in whale-cluster signals across ultra-short-dated low-volume markets (e.g., KXBTC15M) and high-baseline markets (e.g., KXMARMAD), where small volume deltas, near-zero price moves, and routine market-making trigger alerts without predictive impact.

### Next step
Require minimum price move >0.005 (0.5%) AND volume delta >5% of baseline for all whale-cluster tiers to filter noise.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 204

### Summary
Whale-cluster signals are generating excessive false positives in ultra-short-dated, high-baseline-volume markets like KXBTC15M and KXMARMAD, where small volume deltas (<1% of baseline) with minimal or zero price impact reflect quote activity, clustering artifacts, or routine market-making rather than informed flow.

### Next step
Require volume delta to exceed 5% of baseline volume before triggering whale-cluster alerts, with market-specific baselines dynamically computed over recent windows.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.005`, `score_threshold` → `8.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 205

### Summary
whale-cluster tier is generating excessive false positives across low-liquidity markets, thin 15-minute contracts, and extreme-probability outcomes where volume spikes occur with zero price impact and represent <1% of baseline activity.

### Next step
Implement a composite filter for whale-cluster signals: require EITHER (a) volume delta ≥5% of baseline AND price move ≥0.5%, OR (b) absolute volume delta ≥100k contracts minimum. This eliminates quote-stuffing and clustering artifacts while preserving genuine informed positioning.

### Suggested thresholds
`min_volume_delta` → `100000.0`, `min_price_move` → `0.005`, `score_threshold` → `15.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 206

### Summary
whale-cluster tier is generating excessive false positives on low-liquidity and ultra-short-term markets where volume spikes represent <1% of baseline and produce zero price impact, indicating quote-stuffing and algorithmic clustering rather than informed flow.

### Next step
Require whale-cluster signals to satisfy BOTH a relative volume threshold (spike delta ≥5% of baseline) AND a price-impact floor (≥0.5% price move) OR an absolute volume floor (≥50k contracts) to filter out passive quoting and clustering artifacts in thin/short-dated markets.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 207

### Summary
Whale-cluster detector is generating excessive false positives on low-volume spikes without price impact, especially in ultra-short timeframes (15-min), low-conviction markets, and high-baseline-volume instruments where quote activity dominates actual execution.

### Next step
Require minimum price impact (≥0.5%) OR minimum volume delta as percentage of baseline (≥5-10%) to trigger whale-cluster alerts, filtering out pure quote-stacking and algorithmic clustering noise.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 208

### Summary
Whale-cluster detector is generating excessive false positives on low-liquidity and ultra-short-term markets where volume spikes lack price impact or execution confirmation. Most flagged signals show zero or negligible price movement despite high clustering scores.

### Next step
Require minimum price impact (≥0.5%) OR minimum volume delta as percentage of baseline (≥5-10%) to qualify whale-cluster signals; additionally, enforce that executed trade volume must be ≥10-20% of quoted spike volume within 5 seconds for watch-tier and above.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 209

### Summary
Whale-cluster detector is triggering massively on low-liquidity and ultra-short-term markets with zero or minimal price impact, confusing statistical quote clustering with informed trading. Nearly all false positives occur when volume delta is <1% of baseline and priceΔ=0.0.

### Next step
Require minimum price impact (≥0.5%) OR minimum volume delta (≥5% of baseline) for whale-cluster signals; additionally, exclude pure quote events by mandating minimum executed trade volume as percentage of quoted volume.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`, `score_threshold` → `6.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 210

### Summary
Whale-cluster detector is firing on pure volume clustering without price impact across low-liquidity and extreme-probability markets, generating systematic false positives. The core issue is decoupling of volume delta from both baseline percentage and price execution.

### Next step
Require whale-cluster signals to satisfy either (a) volume delta ≥5% of 1h baseline OR (b) price impact ≥0.5%, eliminating pure clustering noise while preserving genuinely informed flow.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 211

### Summary
Whale-cluster detector is generating pervasive false positives on low-liquidity markets by flagging volume clustering without price impact or meaningful baseline percentage thresholds; most noise cases show zero or near-zero price movement with volume deltas <1% of baseline.

### Next step
Implement a mandatory dual-gate for whale-cluster tier: require EITHER (price_move ≥ 0.5%) OR (volume_delta ≥ 5% of baseline), AND exclude signals where both price_move = 0.0 and volume_delta < 1% of baseline.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 212

### Summary
Whale-cluster tier is generating 16/20 false positives (80%) by flagging volume clustering without correlated price impact or baseline-relative thresholds. Most noise occurs in low-liquidity markets where small absolute volumes trigger high scores despite zero or minimal price movement.

### Next step
Implement a composite AND gate: require whale-cluster signals to satisfy EITHER (volume_delta > 1% of rolling 1h baseline AND price_move > 0.5%) OR (absolute_volume_delta > 50k contracts AND price_move > 0.3%) to eliminate clustering-alone noise in thin markets.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 213

### Summary
Whale-cluster detector is generating pervasive false positives on low-liquidity KXMARMAD markets by flagging volume clustering without corresponding price impact or meaningful baseline percentage moves. Nearly all flagged signals have priceΔ=0.0 and sub-1% baseline volume delta, indicating algorithmic quoting rather than informed flow.

### Next step
Introduce a composite gating rule for whale-cluster tier: require EITHER (volΔ ≥ 1% of 1h baseline AND priceΔ ≥ 0.5%) OR (volΔ ≥ 50k notional AND priceΔ ≥ 0.01 sustained over 5min) to suppress clustering-only artifacts.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 214

### Summary
Whale-cluster detector is generating high-confidence false positives on low-liquidity markets by flagging volume clustering without corresponding price impact or baseline-relative thresholds. Nearly all flagged signals show yes≤0.08 confidence despite score=8.0, indicating systematic over-sensitivity to statistical clustering.

### Next step
Implement a mandatory dual-gate filter: require volume delta to exceed 1% of 1-hour baseline AND either (a) price impact ≥0.5% or (b) absolute executed volume ≥50k contracts, to distinguish informed flow from algorithmic quoting and passive liquidity clustering.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 215

### Summary
Whale-cluster detector is firing on volume concentration alone without price impact, generating 18/20 false positives across low-liquidity and high-conviction markets. Zero priceΔ dominates the noise, indicating detection is triggered by order clustering or passive quotes rather than informed trading.

### Next step
Require minimum price impact (±0.5%) OR volume delta >5% of baseline for whale-cluster signals; decouple volume concentration from informativeness by mandating either price discovery or sustained directional skew (>80/20 ratio with correlated price movement).

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`, `score_threshold` → `10.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 216

### Summary
Whale-cluster detector is generating high-confidence false positives across low- and high-liquidity markets by flagging volume concentration without correlated price impact. Nearly all recent signals show zero or minimal price movement (<0.01), indicating liquidity management or passive quotes rather than informed trading.

### Next step
Require conjunctive validation: whale-cluster signals must show EITHER (a) price impact ≥0.5% within 5 minutes of volume spike, OR (b) volume delta ≥1% of rolling 1-hour baseline AND sustained directional imbalance (>80/20 buy/sell ratio). Eliminate pure volume-delta triggers.

### Suggested thresholds
`min_volume_delta` → `0.01`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 217

### Summary
Whale-cluster tier is generating overwhelming false positives (>95% noise) across all markets due to flagging zero-price-movement volume concentrations in isolation. The detector conflates passive liquidity clustering with directional information flow.

### Next step
Implement a composite filter: require whale-cluster alerts to satisfy EITHER (1) price_delta ≥ 0.5% OR (2) volume_delta ≥ 5% of rolling 1h baseline. This eliminates directionally-neutral clusters while preserving genuine conviction trades.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 218

### Summary
The whale-cluster detector is generating systematic false positives across MICH and CONN markets by flagging high-score signals with zero or near-zero price movement. Nearly all 20 signals show priceΔ=0.0 despite high volume deltas, indicating the detector treats volume concentration as directional signal without requiring price discovery validation.

### Next step
Implement a mandatory price-movement gate for whale-cluster alerts: require either (1) priceΔ ≥ 0.5% OR (2) volumeΔ ≥ 5% of rolling 1h baseline. This filters directionally-neutral volume clusters while preserving genuine informed-flow signals that move the market.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 219

### Summary
The whale-cluster detector is generating false positives across KXMARMAD and KXMARMAD-26-CONN by flagging volume concentration (8.0 scores, 0.98 yes-confidence) without corresponding price impact. Zero or near-zero price deltas dominate the noise signals, indicating the detector conflates liquidity provision with informed trading.

### Next step
Require concurrent price movement (≥0.5%) OR volume delta exceeding 5-10% of rolling 1h baseline before escalating to whale-cluster tier; filter out all spike detections with priceΔ=0.0.

### Suggested thresholds
`min_volume_delta` → `0.07`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 220

### Summary
Whale-cluster detector is systematically over-triggering on KXMARMAD-26-MICH and KXMARMAD-26-CONN despite zero or minimal price movement, indicating volume delta alone is insufficient to distinguish informed trading from passive liquidity provision in high-conviction, liquid markets.

### Next step
Enforce a dual-gate requirement for whale-cluster tier: require EITHER (a) price movement ≥0.5% concurrent with volume delta, OR (b) volume delta ≥5-10% of rolling baseline AND order-side directional skew ≥80/20 ratio. This filters passive quote-fragmentation while preserving true informed flow.

### Suggested thresholds
`min_volume_delta` → `0.075`, `min_price_move` → `0.005`, `score_threshold` → `6.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 221

### Summary
Whale-cluster tier is generating excessive false positives in high-baseline-volume markets (KXMARMAD-26-MICH) where volume spikes lack price impact. The detector conflates volume concentration with informed trading, missing that absolute deltas become meaningless without correlated price movement in deep-liquidity markets.

### Next step
Implement a mandatory price-impact gate for whale-cluster signals: require either spike_min_price_move ≥ 0.5% OR volume delta ≥ 5% of rolling 1h baseline (whichever is stricter). Exclude signals with zero price movement entirely.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 222

### Summary
The whale-cluster detector is generating false positives on high-conviction, high-baseline-volume markets (KXMARMAD-26-MICH) by triggering on volume spikes without corresponding price movement. Nearly all flagged signals show priceΔ=0.0 or <0.01 despite high scores, indicating volume concentration alone is insufficient signal quality.

### Next step
Implement a mandatory price-impact floor for whale-cluster alerts: require minimum priceΔ ≥0.5% OR volume delta ≥5-10% of baseline, whichever is stricter. This filters out liquidity-provision noise while preserving true informed-trading signals.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 223

### Summary
Predominantly whale-cluster false positives in high-liquidity, high-conviction markets (yes >0.95) with low price impact (often 0%) and small volume deltas relative to baseline, driven by noise from market makers and quote fragmentation.

### Next step
Require minimum price movement of 0.5% OR volume delta >5% of baseline for whale-cluster signals in high-liquidity markets.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 224

### Summary
The whale-cluster detector is generating overwhelming false positives on KXMARMAD-26-MICH (and similar high-conviction, high-liquidity markets) by triggering on tiny absolute volume deltas (7k–75k contracts) with zero or near-zero price impact. The detector conflates trade fragmentation and quote-level noise with informed whale activity.

### Next step
Require whale-cluster signals to meet BOTH a relative volume threshold (≥5% of baseline) AND an absolute price-impact floor (≥0.5% move) or minimum absolute volume (≥100k contracts). This eliminates low-conviction microstructure noise while preserving genuine directional accumulation.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 225

### Summary
False positives dominate in whale-cluster signals on high-conviction (yes>0.95 or <0.05), high-liquidity, or low-liquidity markets with minimal or no price movement despite volume spikes, often due to quote noise, market maker activity, or poor baseline normalization.

### Next step
Require minimum price move ≥0.5% OR volume delta ≥5% of baseline for all whale-cluster signals, with dynamic baseline adjustment by market liquidity and price extremes.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 226

### Summary
The whale-cluster detector is generating excessive false positives on KXMARMAD-26-MICH (extreme-conviction market at >0.95 probability) by triggering on zero-price-impact volume clusters that lack market significance. All 19 labeled signals are noise despite high score/confidence, driven by quote-refresh mechanics and liquidity provision in illiquid extreme-price regimes.

### Next step
Enforce a hard price-impact floor for whale-cluster tier: require either minimum absolute price movement (±0.5%) OR volume delta ≥2% of baseline, whichever is stricter. This eliminates zero-tick trades while preserving signals with real market conviction.

### Suggested thresholds
`min_volume_delta` → `0.02`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 227

### Summary
The whale-cluster detector is generating high-confidence false positives (score=8.0, yes≈0.99) in extreme-probability markets (>0.95 or <0.05) where volume spikes occur without meaningful price movement, driven by quote-refresh mechanics and liquidity provision rather than informed trading.

### Next step
Implement a price-impact filter: require minimum price_move ≥ 0.5% OR volume_delta ≥ 1-2% of baseline before triggering whale-cluster alerts, with stricter thresholds in extreme-probability regimes (>0.95 or <0.05 price).

### Suggested thresholds
`min_volume_delta` → `0.015`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 228

### Summary
The whale-cluster detector is generating systematic false positives on KXMARMAD-26-MICH (extreme probability >0.95 market) by flagging volume clustering without price impact, confusing quote-refresh mechanics and market-maker noise for informational flow.

### Next step
Implement a conditional rule: for markets with prices >0.95 or <0.05, require EITHER minimum price move ≥0.5% OR volume delta ≥1% of rolling 24h baseline before triggering whale-cluster signals, regardless of clustering score.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 229

### Summary
The detector is generating high-confidence false positives on KXMARMAD-26-MICH (extreme probability market >0.95) by triggering on quote-level noise and trivial volume clustering with zero or minimal price impact. All 17 signals on this market are labeled noise despite high score/confidence, indicating the detector conflates liquidity provision with informed flow.

### Next step
Implement price-impact weighting: require minimum absolute price move (≥0.5%) OR volume delta exceeding 1-2% of rolling baseline for whale-cluster tier signals. For markets with prices >0.95 or <0.05, apply stricter thresholds independent of score.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 230

### Summary
All recent whale-cluster signals are false positives labeled as noise/unclear/high in ultra-high-conviction markets (yes=0.99, prices >0.95), featuring high scores but no price movement (mostly priceΔ=0.0) and volume deltas that are trivial relative to high baselines.

### Next step
Require minimum 0.5% price move OR volume delta >1% of 24h baseline for whale-cluster alerts in markets with implied probability >0.95.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 231

### Summary
Whale-cluster detector is firing on stationary-price, high-conviction markets (>0.95 probability) with large volume deltas but zero price impact. All 14 recent signals are labeled noise/unclear/no, indicating the detector conflates liquidity provision and mechanical order execution with informed positioning.

### Next step
Implement a conjunction gate: require EITHER minimum 0.5% price movement OR volume delta exceeding 1-2% of rolling baseline volume to trigger whale-cluster alerts in markets with prices >0.90 or <0.10. This preserves signal on genuine informed flow while muting quote-clustering noise at pinned extremes.

### Suggested thresholds
`min_volume_delta` → `0.01`, `min_price_move` → `0.005`, `score_threshold` → `5.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 232

### Summary
Whale-cluster detector is generating false positives on extreme-probability markets (>95% yes) where large volume spikes occur with zero price movement. The market structure (pinned prices, thin liquidity regions, mechanical flow) absorbs directional volume without repricing, making pure volume clustering non-informative.

### Next step
Implement a price-movement gate for whale-cluster signals in extreme-probability markets (yes > 0.95 or yes < 0.05): require either ≥0.5% price movement OR order-book depletion before flagging. This single rule eliminates ~19 false positives in the KXMARMAD-26-MICH set while preserving the one genuine signal (volΔ=35000 with extreme bid-ask spread context).

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 233

### Summary
The whale-cluster detector is generating excessive false positives on KXMARMAD-26-MICH (yes=0.99, extreme probability market) by flagging large volume deltas without accompanying price movement. In saturated-probability markets, consensus pricing absorbs directional volume mechanically, making pure volume clustering non-informative.

### Next step
Implement a price-movement gate for markets with implied probabilities >95% or <5%: require minimum 0.5% price move OR spike must represent >1% of 24h baseline volume to qualify as actionable signal. This single rule eliminates ~95% of observed false positives.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 234

### Summary
The whale-cluster detector is generating systematic false positives on KXMARMAD-26-MICH (yes=0.99) by flagging large volume deltas with zero price movement. Extreme-probability markets exhibit price inelasticity, making volume clustering alone non-predictive without accompanying repricing.

### Next step
Implement a price-movement gate for markets with extreme implied probabilities (>95% or <5%): require minimum 0.5% price delta OR reject the spike entirely. This single rule eliminates ~90% of observed false positives while preserving the one genuine whale-coordination signal.

### Suggested thresholds
`min_volume_delta` → `1.3`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 235

### Summary
The detector is generating high false-positive rates on whale-cluster alerts in extreme-probability markets (>95% or <5%) where large volume deltas occur with zero price impact. These are mechanical liquidity flows, not informational signals.

### Next step
Implement a market-context filter: require minimum 0.5% price movement to trigger whale-cluster alerts when implied probability exceeds 0.95 or is below 0.05. This single rule eliminates ~90% of false positives while preserving the one genuine signal (35k volume delta with coordinated activity).

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 236

### Summary
Whale-cluster detector is triggering heavily on extreme-probability markets (>95% yes) with large volume deltas but zero price movement, generating 15+ false positives. Volume clustering alone at pinned prices is mechanical liquidity provision, not informational flow.

### Next step
Require minimum price movement (≥0.5%) concurrent with whale-cluster detection on markets with implied probability >95% or <5%, or filter out whale-cluster alerts entirely when priceΔ=0.0 and baseline probability is extreme.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 237

### Summary
Whale-cluster detector is generating high false-positive rates on extreme-probability markets (>95% or <5%) where large volume spikes occur without corresponding price movement, indicating mechanical liquidity provision rather than informed trading.

### Next step
Introduce probability-aware price-movement requirement: for markets with implied probability >0.95 or <0.05, require minimum price move of ≥0.5% to trigger whale-cluster alerts; for all other markets, require ≥0.1% price move alongside volume clustering.

### Suggested thresholds
`min_price_move` → `0.001`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 238

### Summary
The detector is generating massive false positives on whale-cluster signals in extreme-probability markets (>95% yes) where large volumes produce zero price movement. These are routine liquidity/rebalancing trades, not informational flow.

### Next step
Require minimum 0.5% price movement concurrent with whale-cluster activity in markets with implied probability >95% or <5%, OR filter out whale-cluster spikes entirely when priceΔ=0.0 and conviction is extreme.

### Suggested thresholds
`min_volume_delta` → `0.01`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 239

### Summary
Whale-cluster detector is generating false positives on extreme-probability markets (>95% or <5%) where large volumes produce zero price impact, indicating rebalancing noise rather than informed flow. Price movement is the critical missing filter.

### Next step
Implement market-regime-aware price-impact requirement: require minimum 0.5% price movement for whale-cluster signals in markets with implied probability >95% or <5%, and require volume delta ≥1% of baseline in these extreme-conviction regimes.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 240

### Summary
Whale-cluster detector is generating false positives on extreme-probability markets (>95% yes/no) where large volume spikes occur with zero price movement, indicating rebalancing or quote noise rather than informed flow. The detector conflates statistical significance of absolute volume with predictive signal value.

### Next step
Require minimum price movement (≥0.5%) concurrent with whale-cluster volume spikes on markets with implied probabilities >95% or <5%, since consensus pricing in extreme regimes absorbs large directional volume without repricing.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 241

### Summary
Whale-cluster detector is firing on extreme-conviction markets (>95% yes) with large volume deltas but zero price movement, generating systematic false positives. The tier is conflating quote accumulation and rebalancing with informed flow.

### Next step
Enforce a universal minimum price movement gate (≥0.5%) for whale-cluster signals, with additional context-specific filters for extreme probabilities (>95% or <5%) and thin baselines.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 242

### Summary
Whale-cluster detector is generating false positives on high-conviction markets (>95% yes probability) where large volume deltas occur with zero price movement, suggesting quote noise and rebalancing rather than informed flow.

### Next step
Require concurrent minimum price movement (≥0.5%) OR enforce market-context gates: exclude whale-cluster signals when price is static AND market probability is extreme (>95% or <5%) AND volume delta is <0.5% of baseline.

### Suggested thresholds
`min_volume_delta` → `0.005`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 243

### Summary
Whale-cluster tier is generating systematic false positives on high-conviction markets (>95% implied probability) where large volume deltas produce zero price impact, indicating mechanical rebalancing rather than informed flow.

### Next step
Implement a mandatory price-movement gate for whale-cluster signals: require minimum price move of ±0.5% OR sustained directional imbalance (>80/20 split) concurrent with volume spike, regardless of score. This filters quote noise while preserving genuine informed activity.

### Suggested thresholds
`min_volume_delta` → `0.01`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 244

### Summary
All 20 false positives are whale-cluster signals (score=8.0) with zero price movement on high-conviction markets (KXMARMAD-26-MICH mostly at yes=0.99). The detector is triggering on pure quote activity and mechanical rebalancing without price impact.

### Next step
Require concurrent price movement (≥0.5%) as a mandatory confirmation gate for whale-cluster signals, especially in markets with extreme probabilities (>95% or <5%). This single rule eliminates all 20 false positives while preserving signals where whales actually move price.

### Suggested thresholds
`min_volume_delta` → `0.005`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 245

### Summary
Whale-cluster tier is generating systematic false positives on KXMARMAD-26-MICH and similar markets due to zero price impact despite large volume deltas. The detector flags quote clustering and rebalancing activity as signal without requiring concurrent price movement or baseline-relative volume thresholds.

### Next step
Require minimum price movement (≥0.5%) OR minimum volume delta as percentage of baseline (≥1%) as a mandatory AND gate for whale-cluster signals, especially in extreme-conviction markets (price >0.95 or <0.05).

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 246

### Summary
All 20 signals from KXMARMAD-26 are whale-cluster false positives with zero price movement (priceΔ=0.0) despite high volume deltas and perfect confidence scores. The detector is triggering on mechanical quote activity and one-sided order accumulation in extreme-probability markets without any price discovery.

### Next step
Require minimum price movement (≥0.5%) as a mandatory gate for whale-cluster detection in all markets, especially those with prices >0.95 or <0.05. This single rule eliminates all 20 false positives while preserving informed signal detection.

### Suggested thresholds
`min_volume_delta` → `0.005`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 247

### Summary
False positives cluster around extreme-probability markets and volume spikes decoupled from meaningful price movement. The detector is triggering on liquidity-seeking behavior and technical noise rather than informative flow.

### Next step
Implement conditional thresholds based on market probability regime and require volume-price coherence: high-conviction markets (>90% or <10%) need 15x+ volume multipliers; low-conviction markets (<5%) need 2.5%+ price moves or directional agreement; short-duration markets need >0.5% price moves to validate volume spikes.

### Suggested thresholds
`min_price_move` → `0.025`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 248

### Summary
High false-positive rate in whale-cluster and watch-tier detections on illiquid/extreme-probability markets where large volume spikes occur without meaningful price impact, indicating mechanical order-book activity rather than informed flow.

### Next step
Implement conditional price-move requirements: require minimum 0.5–2.5% price correlation for whale-cluster signals on markets with baseline volume <5M or probability extremes (>90%/<10%), and 2–3% for watch-tier on short-duration instruments. Decouple volume-only signals from true spike detection.

### Suggested thresholds
`min_price_move` → `0.015`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 249

### Summary
Whale-cluster and watch-tier alerts are firing on volume spikes without corresponding price movement, particularly in illiquid and extreme-probability markets where large volumes represent normal market-making rather than informative flow.

### Next step
Enforce a mandatory price-movement floor (≥0.5% for whale-cluster on illiquid markets, ≥2.5% for low-conviction tail markets) correlated with volume delta, and apply dynamic volume-delta multipliers based on baseline liquidity and probability extremity rather than fixed scoring.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 250

### Summary
Whale-cluster detector is generating false positives on low-liquidity, low-conviction markets by triggering on large absolute volumes without price impact or sustained directional flow. Most noise cases show priceΔ=0.0 or <0.5%, indicating mechanical execution rather than information flow.

### Next step
Require minimum price movement (≥0.5%) correlation with volume spikes for whale-cluster tier on illiquid markets, and increase baseline volume multiplier thresholds (250x+) for markets below $10M daily volume to filter routine block trades.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 251

### Summary
Whale-cluster and notable tiers are generating excessive false positives on low-liquidity markets (sub-$10M daily volume, extreme skew >90% or <10% probability) where large volume deltas occur without meaningful price impact. Volume-only detection is triggering on routine block trades and market-making activity rather than informative flow.

### Next step
Require minimum price-move correlation (≥0.5%) for whale-cluster alerts on illiquid markets, and raise volume-delta multiplier thresholds for extreme-skew markets (>90% or <10% probability) from current baselines to 250x+ to filter mechanical execution.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 252

### Summary
whale-cluster tier is generating systematic false positives on KXMARMAD-26-CONN and similar markets: high volume concentration without price impact is being flagged as signal-worthy despite analyst consensus that zero price movement indicates mechanical execution, not informed flow.

### Next step
Require non-zero price movement (≥0.5%) OR price-impact correlation as a mandatory gate before whale-cluster signals qualify, rather than relying on volume clustering and score alone.

### Suggested thresholds
`min_volume_delta` → `5000000.0`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 253

### Summary
Whale-cluster detector is triggering heavily on zero-price-impact volume spikes in low-conviction markets, flagging mechanical/liquidity-driven execution as informed flow. Nearly all false positives share priceΔ=0.0 with yes-probability <0.1, indicating noise rather than directional conviction.

### Next step
Require non-zero price impact (≥0.5%) OR minimum volume delta as % of baseline liquidity (≥1-2%) to qualify whale-cluster signals; reject any spike where priceΔ=0.0 unless volume exceeds 5% of rolling baseline.

### Suggested thresholds
`min_volume_delta` → `0.01`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 254

### Summary
Whale-cluster tier is generating excessive false positives (19 of 21 signals labeled noise) due to flagging large coordinated volume with zero or near-zero price impact in low-conviction markets. Notable tier also shows false positives on low-absolute-volume markets without sustained price holds.

### Next step
Require non-zero price impact (≥0.5% move) OR sustained directional follow-through (5+ min hold) as mandatory gate before emitting whale-cluster or notable signals, regardless of volume delta or score magnitude.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 255

### Summary
Whale-cluster tier is generating pervasive false positives on low-conviction markets with zero or near-zero price impact despite large volume deltas. Nearly all flagged signals lack directional conviction, indicating mechanical/liquidity-driven activity rather than informed trading.

### Next step
Require non-zero price impact (≥0.5% move) OR sustained directional follow-through (5+ min hold) as mandatory gate for whale-cluster signals, especially in markets with <10% implied probability or <$1M daily baseline volume.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`, `score_threshold` → `12.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 256

### Summary
Whale-cluster tier is generating excessive false positives on low-conviction markets (sub-10% probability) with large volume spikes but zero price impact, indicating mechanical execution rather than informed trading.

### Next step
Implement a mandatory price-impact filter for whale-cluster signals: require either ≥0.5% concurrent price movement OR explicitly tag zero-price-delta spikes as non-actionable unless they exceed 5% of baseline daily volume with asymmetric directional bias (>95% buy/sell ratio).

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 257

### Summary
Whale-cluster tier is generating systematic false positives in low-conviction markets with zero or minimal price impact, dominated by KXMARMAD-26-CONN/MICH signals where large volume spikes (4.7K–51K delta) produce no directional price movement. Notable tier also shows false positives in thin markets without sustained price holds.

### Next step
Require concurrent price impact (≥0.5% move) OR minimum volume delta as 1–2% of baseline for whale-cluster signals; simultaneously enforce minimum sustained price hold (2%+ for 5+ min) or multi-sided volume confirmation for notable tier in low-liquidity markets.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 258

### Summary
Whale-cluster and low-conviction market detectors are generating excessive false positives by flagging volume spikes without accompanying price impact or by treating normal microstructure noise as informed flow. The MARMAD and TRUMPSAY markets show systematic over-triggering when priceΔ=0.0 or priceΔ<1%, regardless of volume magnitude.

### Next step
Implement a mandatory price-impact gate for whale-cluster and notable tiers: require either concurrent priceΔ≥0.5% OR volume spike ≥5% of baseline daily volume AND trade count ≥10 to emit signal. This filters mechanical execution and rebalancing noise while preserving genuine directional flow.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.005`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 259

### Summary
Detector is generating excessive false positives in low-liquidity and whale-cluster markets by flagging volume spikes without concurrent price impact. Most noise comes from thin markets (minor league sports, ultra-low probability events) and coordinated trades that execute at static prices.

### Next step
Implement a mandatory price-impact floor for whale-cluster and low-liquidity tiers: require either ≥0.5% price move OR volume delta >5% of baseline. Separately, raise spike_min_price_move to 0.03 (3%) for markets with <1M daily baseline volume.

### Suggested thresholds
`min_volume_delta` → `0.05`, `min_price_move` → `0.03`, `score_threshold` → `15.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 260

### Summary
The detector is generating false positives across thin/low-liquidity markets by flagging volume spikes without corresponding price conviction (priceΔ often 0–2%) and by treating baseline-equal volumes as anomalies. Whale-cluster and notable tiers are especially prone to noise in markets with sub-1% baseline elasticity.

### Next step
Enforce a conjunctive filter: require *both* (1) volume delta ≥1.5–2.0x baseline AND (2) price move ≥2–3% for notable/whale-cluster tiers, except where trade count ≥10 AND price hold ≥5 min. This prevents flat-price accumulation noise while preserving genuine conviction moves.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 261

### Summary
The detector is generating false positives primarily in low-liquidity and skewed-probability markets where volume spikes occur without meaningful price impact. Most flagged signals show priceΔ ≤ 2% despite high volume deltas, indicating conviction is absent.

### Next step
Implement a price-move floor (minimum 2-3%) as a hard gate for all tiers except whale-cluster; for whale-cluster, require either significant price impact (>0.5%) OR volume must exceed 5-10% of baseline to filter accumulation-only behavior.

### Suggested thresholds
`min_volume_delta` → `0.08`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 262

### Summary
Detector is triggering on high-volume activity without meaningful price conviction, particularly in skewed binary markets, thin sports books, and ultra-low-liquidity whale accumulation. Most false positives show volume spikes decoupled from price movement (priceΔ=0.0–0.02), indicating algorithmic noise or baseline churn rather than informed flow.

### Next step
Implement a mandatory price-move floor (2–3% for binary markets, 0.5% for whale-cluster tiers) AND a minimum trade-count/persistence filter to require volume spikes to demonstrate actual conviction rather than fragmented order flow.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 263

### Summary
Detector is generating false positives by triggering on volume spikes without sufficient price conviction, particularly in skewed markets (high baseline odds) and thin/low-liquidity venues where fragmented order flow creates noise.

### Next step
Implement a context-aware minimum price move requirement that scales with market structure: require 3-5% price move for high-conviction markets (yes/no >0.80 or <0.20), 2% for normal markets, and pair all volume spikes with minimum trade-count validation (≥3 trades) or price persistence checks.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 264

### Summary
Detector is triggering on high-volume trades without sufficient price conviction, particularly in skewed binary markets and low-liquidity venues. Volume spikes alone are not reliably informative when price impact is minimal (≤2%).

### Next step
Implement a dynamic minimum price-move requirement that scales with market structure: require 3-5% for binary markets with implied probability >80%, and >2% for low-liquidity markets; pair with volume-ratio validation (spike must exceed 1.5x-2.0x baseline, not merely equal it).

### Suggested thresholds
`min_volume_delta` → `1.75`, `min_price_move` → `0.02`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 265

### Summary
The detector is triggering on high-volume activity without sufficient price conviction, particularly in skewed markets and thin-volume venues. Volume spikes alone are insufficient signals without accompanying price movement or market microstructure validation.

### Next step
Implement a tiered validation rule: require minimum price move (3-5%) for high-confidence binary markets with skewed probabilities (>80% or <20%), and add trade-count or persistence filters for thin-volume venues before escalating volume deltas to signal tier.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 266

### Summary
Volume spikes in skewed binary markets and thin-volume sports markets are triggering false positives despite high scores, because price impact is naturally muted in these contexts and single large trades lack conviction signal.

### Next step
Implement market-type conditional logic: require minimum price move (3-5%) for high-skew binary markets (yes/no >75%), and enforce trade-count or persistence requirements for thin-volume markets before escalating volume deltas to notable tier.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 267

### Summary
False positives cluster around low-conviction volume moves in skewed markets (high baseline probabilities) and low-volume spikes with minimal price confirmation. Current thresholds trigger on volume alone without sufficient price or confirmation anchoring.

### Next step
Implement asymmetric thresholds: require either (a) substantial volume delta AND meaningful price move together, OR (b) spike_score above 4.5+ with multi-trade confirmation. This prevents single large trades or noise from triggering signals in illiquid/skewed markets.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`, `score_threshold` → `4.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 268

### Summary
Low-liquidity binary markets are generating false positives from small trades creating outsized price moves. Signals lack sufficient trade confirmation and apply uniform thresholds across markets with vastly different liquidity profiles.

### Next step
Implement liquidity-aware threshold scaling: require higher volume delta or price move thresholds for low-liquidity markets, and mandate multi-trade confirmation to filter single-trade noise.

### Suggested thresholds
`min_volume_delta` → `1500.0`, `min_price_move` → `0.03`, `score_threshold` → `6.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 269

### Summary
Low-liquidity markets are generating false positives through mechanical liquidity (unexecuted quotes) and outsized price moves from minimal trade sizes. The detector is overly sensitive to small absolute moves in thin markets.

### Next step
Implement liquidity-adjusted thresholds that scale requirements inversely with baseline market volume: require higher volume delta or price move thresholds for markets below a liquidity floor.

### Suggested thresholds
`min_volume_delta` → `5.0`, `min_price_move` → `0.05`, `score_threshold` → `5.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 270

### Summary
Low-volume and binary-outcome markets are generating false positives from single large trades or unexecuted quotes that create outsized price moves. The detector lacks trade-count and trade-concentration filters to distinguish mechanical liquidity from genuine informed flow.

### Next step
Introduce a trade-count minimum (≥2 trades in same direction within window) and a trade-size concentration filter to require that no single trade represents >40% of detected volume delta, especially in sub-10k baseline volume markets.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.03`, `score_threshold` → `5.0`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 271

### Summary
Low-volume and binary markets are generating false positives from single small trades or unexecuted quotes that create outsized price moves. The detector is too sensitive to volume/price combinations in thin markets where mechanical liquidity and minimal order flow create signal-like artifacts.

### Next step
Implement minimum trade size (notional or contract count) requirement and distinguish between executed trades vs. unexecuted quotes in the volume delta calculation, rather than relying on volume and price move thresholds alone in low-liquidity venues.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.04`, `score_threshold` → `5.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 272

### Summary
False positives are driven by single large trades in low-volume markets that spike volume without sustained price movement. Volume deltas alone are insufficient signals without confirmatory price action or trade sequencing.

### Next step
Require sustained price confirmation: enforce either (a) minimum consecutive ticks in signaled direction, or (b) higher price_move threshold, especially in low absolute-volume regimes.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 273

### Summary
False positives are dominated by single large trades in low-volume markets that create volume spikes without sustained price conviction or multi-trade confirmation. The detector is too sensitive to isolated outlier transactions.

### Next step
Require multi-trade confirmation (2-3 consecutive trades in same direction) or sustained price persistence (5+ ticks) before emitting signals, especially in low-volume and micro-timeframe markets.

### Suggested thresholds
`min_volume_delta` → `100000.0`, `min_price_move` → `0.02`, `score_threshold` → `6.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 274

### Summary
The detector is generating false positives across all tiers by flagging single large trades or mechanical oscillations without sustained directional conviction or multi-trade confirmation. Low-liquidity and micro-markets (15-min) are especially vulnerable to noise.

### Next step
Require multi-trade or multi-tick confirmation: enforce that spike signals must be backed by either 2+ consecutive trades in the same direction, or 3+ consecutive price ticks moving in the signaled direction, before emission.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.05`, `score_threshold` → `6.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 275

### Summary
The detector is triggering on low-conviction, single-trade events and mechanical oscillations across illiquid markets. High score values (up to 13.4) paired with low yes-probability (0.05–0.51) indicate the scoring function weights volume delta too heavily relative to trade execution intent and follow-through.

### Next step
Require executed trade count ≥2 in the same direction within a 5-minute window, or introduce a quote-to-trade ratio filter and volume-weighted price conviction metric to exclude single-sided liquidity and micro-moves on thin order books.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.04`, `score_threshold` → `8.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 276

### Summary
The detector is generating false positives across low-liquidity and micro-markets by triggering on single trades, quote-only volume, and mechanical oscillations without sustained directional conviction or multi-trade confirmation.

### Next step
Implement a multi-trade confirmation rule requiring 2+ consecutive trades in the same direction within the spike window, combined with a minimum executed trade volume filter (5+ lots) to exclude single-contract outliers and quote-driven events.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.04`, `score_threshold` → `8.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 277

### Summary
All 8 recent signals labeled as noise/unclear/low show a consistent pattern: low-liquidity markets are triggering alerts on single trades, quote-stuffing, or mechanical oscillations lacking genuine conviction. The detector conflates volume delta with executed trade volume and ignores market microstructure signals.

### Next step
Implement a minimum executed trade count filter (3+ trades in same direction within spike window) and require quote-to-trade ratio validation before emitting any signal, especially in tier=watch and tier=notable for illiquid markets.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.05`, `score_threshold` → `5.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 278

### Summary
All 7 recent signals are labeled noise/unclear/low despite scoring above current thresholds. The detector is firing on quote-driven oscillations, single-sided liquidity events, and micro-trades lacking execution conviction rather than genuine informed flow.

### Next step
Pivot from volume-delta and price-move thresholds to execution-quality filters: require minimum executed trade count (3-5 trades) or minimum trade size (5-50 lots depending on market liquidity tier) before emitting any signal. Quote volume alone is insufficient.

### Suggested thresholds
`score_threshold` → `5.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 279

### Summary
All five recent signals are labeled noise/unclear/low despite varying scores and volumes, indicating the detector is triggering on quote activity and mechanical oscillations rather than genuine executed flow, particularly in illiquid markets.

### Next step
Implement a trade-execution filter requiring minimum confirmed executed trades (not just quote volume) at moved price levels, with stricter thresholds for low-liquidity markets based on contract type and typical daily volume.

### Suggested thresholds
`score_threshold` → `4.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 280

### Summary
High-scoring signals are being triggered by quote-driven volume spikes without corresponding executed trades, particularly in illiquid markets (niche reality TV, political betting, low-liquidity crypto). Volume delta alone is insufficient to distinguish genuine flow from quote-stuffing and one-sided liquidity events.

### Next step
Implement a trade-volume requirement filter: require minimum confirmed executed trade volume (not quote volume) or a quote-to-trade ratio threshold to validate that price moves are backed by actual transactional activity.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `5.5`

### Recommendations

---

## 2026-04-07 — Advisor snapshot 281

### Summary
Low-liquidity event markets and ultra-short-duration contracts are generating false positives due to routine rebalancing trades and micro-volatility triggering signals on minimal price moves (1-2%) with modest volume deltas.

### Next step
Implement market-type-specific thresholds: require 5%+ price moves for binary event markets and 8-10x volume multipliers for sub-30min duration contracts, while raising the global score threshold to filter marginal signals.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-015** `rejected` — For binary political/event markets (KXTRUMPSAY-*): require min_price_move ≥ 0.05 (5%) alongside volume spike to filter rebalancing noise in thin order books
  - **Governor rejection**: TB-011 explicitly sets spike_min_price_move = 0.04 (4%), which was established as a durable constraint. The proposed tweak raises min_price_move to 0.05 (5%) globally. While market-type-specific thresholds (5%+ for event markets, 8-10x multipliers for sub-30min contracts) are not inherently conflicting, the global score_threshold increase to 5.0 combined with raising the baseline price move requirement risks relaxing TB-003 and TB-006 constraints for liquid markets where 2-3% moves were previously accepted. Additionally, the proposal lacks specification of how market-type and duration-based overrides will be implemented and enforced, creating ambiguity about whether TB-003 (2% requirement for low liquidity) and TB-013 (liquidity-aware thresholds) will be properly preserved for their respective scenarios.
- [ ] **TB-016** `rejected` — For ultra-short-duration markets (<30 min): increase volume delta multiplier from 5.6x to 8-10x baseline to account for inherent micro-volatility
  - **Governor rejection**: TB-011 explicitly sets spike_min_price_move = 0.04 (4%), which was established as a durable constraint. The proposed tweak raises min_price_move to 0.05 (5%) globally. While market-type-specific thresholds (5%+ for event markets, 8-10x multipliers for sub-30min contracts) are not inherently conflicting, the global score_threshold increase to 5.0 combined with raising the baseline price move requirement risks relaxing TB-003 and TB-006 constraints for liquid markets where 2-3% moves were previously accepted. Additionally, the proposal lacks specification of how market-type and duration-based overrides will be implemented and enforced, creating ambiguity about whether TB-003 (2% requirement for low liquidity) and TB-013 (liquidity-aware thresholds) will be properly preserved for their respective scenarios.
- [ ] **TB-017** `rejected` — Raise global spike_score_threshold to 5.0+ to mute low-conviction signals (currently score=2.156 and 4.86 passed despite analyst=noise labels)
  - **Governor rejection**: TB-011 explicitly sets spike_min_price_move = 0.04 (4%), which was established as a durable constraint. The proposed tweak raises min_price_move to 0.05 (5%) globally. While market-type-specific thresholds (5%+ for event markets, 8-10x multipliers for sub-30min contracts) are not inherently conflicting, the global score_threshold increase to 5.0 combined with raising the baseline price move requirement risks relaxing TB-003 and TB-006 constraints for liquid markets where 2-3% moves were previously accepted. Additionally, the proposal lacks specification of how market-type and duration-based overrides will be implemented and enforced, creating ambiguity about whether TB-003 (2% requirement for low liquidity) and TB-013 (liquidity-aware thresholds) will be properly preserved for their respective scenarios.

---

## 2026-04-07 — Advisor snapshot 282

### Summary
High false-positive rate across short-duration and low-liquidity markets. Signals are firing on mechanical liquidity moves, single small trades, and routine rebalancing rather than genuine directional flow.

### Next step
Implement market-type-specific thresholds and require sustained multi-order confirmation rather than single large quotes, especially for ultra-short-duration and binary event markets.

### Suggested thresholds
`min_volume_delta` → `8.5`, `min_price_move` → `0.05`, `score_threshold` → `6.0`

### Recommendations

- [ ] **TB-018** `rejected` — For ultra-short-duration markets (<30 min): raise volume delta multiplier threshold from 5.6x to 8-10x baseline to filter micro-volatility noise
  - **Governor rejection**: Proposed min_volume_delta of 8.5 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with 15–20% multiplier on thin markets, 10% on deep markets. The proposed value of 8.5 is orders of magnitude below the established floor and would bypass the liquidity-aware multiplier framework that was explicitly designed to prevent false positives on thin markets. Additionally, proposed min_price_move of 0.05 (5%) conflicts with TB-011 (spike_min_price_move = 0.04) and TB-013 liquidity-aware thresholds by creating a one-size-fits-all rule that ignores market depth context (TB-013 permits 2% for >100k baseline liquidity). The proposed score_threshold of 6.0 lacks granular tier definition and risks circumventing TB-008's alert escalation logic that distinguishes watch-tier (volΔ > 3x) from notable-tier conditions.
- [ ] **TB-019** `rejected` — For low-liquidity event/binary markets: require minimum 5%+ price movement alongside volume spikes, or enforce sustained directional trades (>50 contracts) before flagging
  - **Governor rejection**: Proposed min_volume_delta of 8.5 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with 15–20% multiplier on thin markets, 10% on deep markets. The proposed value of 8.5 is orders of magnitude below the established floor and would bypass the liquidity-aware multiplier framework that was explicitly designed to prevent false positives on thin markets. Additionally, proposed min_price_move of 0.05 (5%) conflicts with TB-011 (spike_min_price_move = 0.04) and TB-013 liquidity-aware thresholds by creating a one-size-fits-all rule that ignores market depth context (TB-013 permits 2% for >100k baseline liquidity). The proposed score_threshold of 6.0 lacks granular tier definition and risks circumventing TB-008's alert escalation logic that distinguishes watch-tier (volΔ > 3x) from notable-tier conditions.
- [ ] **TB-020** `rejected` — For all markets: replace single-order detection with multi-order confirmation rule—require at least 2 independent orders at similar prices or >50 contract sustained flow to validate signal authenticity
  - **Governor rejection**: Proposed min_volume_delta of 8.5 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with 15–20% multiplier on thin markets, 10% on deep markets. The proposed value of 8.5 is orders of magnitude below the established floor and would bypass the liquidity-aware multiplier framework that was explicitly designed to prevent false positives on thin markets. Additionally, proposed min_price_move of 0.05 (5%) conflicts with TB-011 (spike_min_price_move = 0.04) and TB-013 liquidity-aware thresholds by creating a one-size-fits-all rule that ignores market depth context (TB-013 permits 2% for >100k baseline liquidity). The proposed score_threshold of 6.0 lacks granular tier definition and risks circumventing TB-008's alert escalation logic that distinguishes watch-tier (volΔ > 3x) from notable-tier conditions.

---

## 2026-04-07 — Advisor snapshot 283

### Summary
System is generating watch/notable tier false positives on low-liquidity event markets and ultra-short-duration instruments, primarily triggered by isolated small trades or mechanical liquidity moves rather than genuine conviction-driven flow.

### Next step
Implement market-type-specific threshold tiers: raise price_move floor to 5% for binary event markets and 3% for ultra-short duration (<30min) instruments, while increasing volume_delta multiplier for short-duration markets from 5.6x to 8-10x baseline.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [x] **TB-021** `applied` — For binary political event markets (KXTRUMPSAY*): require min_price_move >= 0.05 (5%) combined with sustained directional volume (>50 contracts in same direction) to filter routine micro-trades
- [x] **TB-022** `applied` — For ultra-short-duration markets (<30min): increase volume_delta multiplier threshold to 8-10x baseline and require priceΔ >= 0.03 (3%) to reduce noise from mechanical rebalancing
- [x] **TB-023** `applied` — Implement minimum trade-size floor per market liquidity tier: for low-liquidity event markets, exclude signals triggered by single-contract or sub-100-contract isolated trades unless accompanied by follow-on volume

---

## 2026-04-07 — Advisor snapshot 284

### Summary
False positives are driven by quote-heavy volume (not executed trades), single small trades on low-conviction events, and micro-movements in ultra-short-duration markets. Current thresholds lack market-structure and temporal context.

### Next step
Implement a trades-to-quotes ratio filter (require >40% of volume delta to be executed trades, not just quotes) and market-duration multiplier (8-10x volume delta requirement for <30min markets). This addresses the root cause across all six signals.

### Suggested thresholds
`min_volume_delta` → `30000.0`, `min_price_move` → `0.04`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-024** `rejected` — Add trades-to-quotes ratio filter: reject signals where executed trade volume is <40% of total volume delta, to exclude quote-driven mechanical moves
  - **Governor rejection**: Proposed min_volume_delta of 30000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 30000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <300k baseline volume. Additionally, the proposal lacks implementation specification for the trades-to-quotes ratio filter (>40% executed trades) and market-duration multiplier (8–10x for <30min markets), creating ambiguity about whether TB-003 (2% requirement for illiquid markets), TB-004 (ultra-thin market volume rule), TB-013 (liquidity-aware price thresholds), and TB-014 (multiplier framework) will be properly preserved. The suggested score_threshold of 3.5 also risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the ratio/duration overrides are not explicitly coded to respect those conditions.
- [ ] **TB-025** `rejected` — Introduce market-duration multiplier: for markets with <30 minutes to expiry, multiply spike_min_volume_delta requirement by 8-10x to suppress inherent micro-volatility noise
  - **Governor rejection**: Proposed min_volume_delta of 30000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 30000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <300k baseline volume. Additionally, the proposal lacks implementation specification for the trades-to-quotes ratio filter (>40% executed trades) and market-duration multiplier (8–10x for <30min markets), creating ambiguity about whether TB-003 (2% requirement for illiquid markets), TB-004 (ultra-thin market volume rule), TB-013 (liquidity-aware price thresholds), and TB-014 (multiplier framework) will be properly preserved. The suggested score_threshold of 3.5 also risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the ratio/duration overrides are not explicitly coded to respect those conditions.
- [ ] **TB-026** `rejected` — Require sustained multi-tick directional conviction: for watch-tier and below, demand ≥3 consecutive trades in same direction at progressive prices, not single outlier transactions
  - **Governor rejection**: Proposed min_volume_delta of 30000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 30000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <300k baseline volume. Additionally, the proposal lacks implementation specification for the trades-to-quotes ratio filter (>40% executed trades) and market-duration multiplier (8–10x for <30min markets), creating ambiguity about whether TB-003 (2% requirement for illiquid markets), TB-004 (ultra-thin market volume rule), TB-013 (liquidity-aware price thresholds), and TB-014 (multiplier framework) will be properly preserved. The suggested score_threshold of 3.5 also risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the ratio/duration overrides are not explicitly coded to respect those conditions.
- [ ] **TB-027** `rejected` — Raise price-move threshold for low-liquidity event markets (political/binary outcomes): require priceΔ ≥0.05 (5%) alongside volume spike to trigger notable tier
  - **Governor rejection**: Proposed min_volume_delta of 30000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 30000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <300k baseline volume. Additionally, the proposal lacks implementation specification for the trades-to-quotes ratio filter (>40% executed trades) and market-duration multiplier (8–10x for <30min markets), creating ambiguity about whether TB-003 (2% requirement for illiquid markets), TB-004 (ultra-thin market volume rule), TB-013 (liquidity-aware price thresholds), and TB-014 (multiplier framework) will be properly preserved. The suggested score_threshold of 3.5 also risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the ratio/duration overrides are not explicitly coded to respect those conditions.
- [ ] **TB-028** `rejected` — Implement minimum trade size floor: filter out single-contract or sub-50-contract trades unless part of sustained order sequence
  - **Governor rejection**: Proposed min_volume_delta of 30000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 30000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <300k baseline volume. Additionally, the proposal lacks implementation specification for the trades-to-quotes ratio filter (>40% executed trades) and market-duration multiplier (8–10x for <30min markets), creating ambiguity about whether TB-003 (2% requirement for illiquid markets), TB-004 (ultra-thin market volume rule), TB-013 (liquidity-aware price thresholds), and TB-014 (multiplier framework) will be properly preserved. The suggested score_threshold of 3.5 also risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the ratio/duration overrides are not explicitly coded to respect those conditions.

---

## 2026-04-07 — Advisor snapshot 285

### Summary
False positives cluster around low-liquidity event markets where quote volume, single large trades, and mechanical rebalancing trigger alerts despite minimal genuine conviction (yes% ≤0.5). Short-duration and binary political markets are particularly vulnerable.

### Next step
Implement a trades-to-quotes ratio filter requiring executed trade volume to exceed 60% of total volume delta, combined with a minimum sustained order size requirement (>50 contracts per trade) to distinguish genuine flow from quote-driven mechanical moves.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.03`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-029** `rejected` — Raise spike_min_volume_delta to 15000 for watch-tier alerts and 200000 for notable-tier on low-liquidity markets (<100k daily volume) to filter micro-event noise
  - **Governor rejection**: Proposed min_volume_delta of 15000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 15000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <150k baseline volume. Additionally, the trades-to-quotes ratio filter (>60% executed trades) and minimum sustained order size (>50 contracts) lack explicit implementation specification and risk circumventing TB-004 (ultra-thin market volume rule), TB-007 (directional trade-flow confirmation), and TB-010 (2+ consecutive trades requirement) if not properly integrated with existing coherence and flow-validation gates. Finally, score_threshold of 3.5 lacks granular tier definition and risks conflicting with TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the ratio/order-size overrides are not explicitly coded to preserve those conditions.
- [ ] **TB-030** `rejected` — Add minimum sustained trade size requirement: reject signals where largest single trade is <50 contracts, or require ≥3 independent trades within 2-tick price window
  - **Governor rejection**: Proposed min_volume_delta of 15000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 15000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <150k baseline volume. Additionally, the trades-to-quotes ratio filter (>60% executed trades) and minimum sustained order size (>50 contracts) lack explicit implementation specification and risk circumventing TB-004 (ultra-thin market volume rule), TB-007 (directional trade-flow confirmation), and TB-010 (2+ consecutive trades requirement) if not properly integrated with existing coherence and flow-validation gates. Finally, score_threshold of 3.5 lacks granular tier definition and risks conflicting with TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the ratio/order-size overrides are not explicitly coded to preserve those conditions.
- [ ] **TB-031** `rejected` — Increase spike_min_price_move to 0.05 (5%) for binary political event markets and short-duration contracts; require 0.03+ (3%) for all others to raise conviction bar
  - **Governor rejection**: Proposed min_volume_delta of 15000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 15000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <150k baseline volume. Additionally, the trades-to-quotes ratio filter (>60% executed trades) and minimum sustained order size (>50 contracts) lack explicit implementation specification and risk circumventing TB-004 (ultra-thin market volume rule), TB-007 (directional trade-flow confirmation), and TB-010 (2+ consecutive trades requirement) if not properly integrated with existing coherence and flow-validation gates. Finally, score_threshold of 3.5 lacks granular tier definition and risks conflicting with TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the ratio/order-size overrides are not explicitly coded to preserve those conditions.

---

## 2026-04-07 — Advisor snapshot 286

### Summary
System is generating false positives on low-conviction tactical order flow and quote-heavy activity, particularly on short-duration and micro-event markets where single large orders or quote imbalances trigger alerts without corresponding price conviction or sustained directional intent.

### Next step
Implement a dual-gate requirement: require BOTH meaningful price confirmation (>1–3% depending on market duration/type) AND sustained multi-order directional flow, rather than triggering on volume delta alone. This filters mechanical liquidity moves while preserving genuine conviction signals.

### Suggested thresholds
`min_volume_delta` → `200000.0`, `min_price_move` → `0.015`, `score_threshold` → `8.0`

### Recommendations

- [ ] **TB-032** `rejected` — For short-duration markets (15M binaries): raise spike_min_price_move to 0.01–0.02 (1–2%) and require multiple independent orders in same direction within the detection window, not single large quotes.
  - **Governor rejection**: Proposed min_volume_delta of 200000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 200000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with baseline volume <2M contracts. Additionally, proposed min_price_move of 0.015 (1.5%) conflicts with TB-011 (spike_min_price_move = 0.04 or 4%), TB-013 (liquidity-aware thresholds permitting 2–5% depending on market depth), and TB-021/TB-022 (which establish higher minimums for event and short-duration markets). Finally, proposed score_threshold of 8.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) and TB-007's directional trade-flow confirmation (>60% dominant recent trade-side share) if the dual-gate override is not explicitly coded to preserve those conditions.
- [ ] **TB-033** `rejected` — Introduce trades-to-quotes ratio filter: exclude alerts where quote volume >> executed trade volume, signaling mechanical order placement rather than actual fills.
  - **Governor rejection**: Proposed min_volume_delta of 200000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 200000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with baseline volume <2M contracts. Additionally, proposed min_price_move of 0.015 (1.5%) conflicts with TB-011 (spike_min_price_move = 0.04 or 4%), TB-013 (liquidity-aware thresholds permitting 2–5% depending on market depth), and TB-021/TB-022 (which establish higher minimums for event and short-duration markets). Finally, proposed score_threshold of 8.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) and TB-007's directional trade-flow confirmation (>60% dominant recent trade-side share) if the dual-gate override is not explicitly coded to preserve those conditions.
- [ ] **TB-034** `rejected` — For micro-event/low-volume markets: set a minimum sustained trade size (e.g., >50 contracts per order or >5 orders) and require price move >0.03 (3%) before escalating from watch to notable tier.
  - **Governor rejection**: Proposed min_volume_delta of 200000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 200000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with baseline volume <2M contracts. Additionally, proposed min_price_move of 0.015 (1.5%) conflicts with TB-011 (spike_min_price_move = 0.04 or 4%), TB-013 (liquidity-aware thresholds permitting 2–5% depending on market depth), and TB-021/TB-022 (which establish higher minimums for event and short-duration markets). Finally, proposed score_threshold of 8.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) and TB-007's directional trade-flow confirmation (>60% dominant recent trade-side share) if the dual-gate override is not explicitly coded to preserve those conditions.
- [ ] **TB-035** `rejected` — Raise spike_min_volume_delta floor by market liquidity tier: baseline ~10k for micro-cap, ~200k for mid-cap, ~400k+ for high-volume markets like KXBTC, to filter single-contract and small-lot noise.
  - **Governor rejection**: Proposed min_volume_delta of 200000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 200000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with baseline volume <2M contracts. Additionally, proposed min_price_move of 0.015 (1.5%) conflicts with TB-011 (spike_min_price_move = 0.04 or 4%), TB-013 (liquidity-aware thresholds permitting 2–5% depending on market depth), and TB-021/TB-022 (which establish higher minimums for event and short-duration markets). Finally, proposed score_threshold of 8.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) and TB-007's directional trade-flow confirmation (>60% dominant recent trade-side share) if the dual-gate override is not explicitly coded to preserve those conditions.

---

## 2026-04-07 — Advisor snapshot 287

### Summary
False positives dominated by small volume deltas (<25k) with sub-3% price moves in thin markets, particularly on short-duration and low-conviction event contracts. Pure volume spikes without price confirmation are triggering watch-tier noise.

### Next step
Require price-move confirmation (>1–3% depending on market duration) alongside volume deltas to filter mechanical/liquidity-driven false signals. Decouple binary event markets from short-duration (15m) markets with separate thresholds.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-036** `rejected` — Raise spike_min_volume_delta to 50000 for standard markets and 250000 for 15-minute duration markets to filter single large quotes and mechanical order-book activity
  - **Governor rejection**: Proposed min_volume_delta of 50000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 50000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <500k baseline volume. Additionally, proposed min_price_move of 0.03 (3%) conflicts with TB-011 (spike_min_price_move = 0.04 or 4%) by relaxing the established price-move floor, and conflicts with TB-013 (liquidity-aware price thresholds permitting 2% for >100k baseline liquidity) and TB-021/TB-022 (which establish 5% for event markets and 3% for short-duration markets, respectively). Finally, the proposal lacks specification of how duration-based and market-type overrides will be implemented and enforced, creating ambiguity about whether TB-003 (2% requirement for illiquid markets), TB-004 (ultra-thin market volume rule), and TB-008 (watch-tier escalation logic) will be properly preserved.
- [ ] **TB-037** `rejected` — Enforce minimum price_move of 0.03 (3%) for watch tier and 0.05 (5%) for notable tier to require directional conviction alongside volume
  - **Governor rejection**: Proposed min_volume_delta of 50000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 50000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <500k baseline volume. Additionally, proposed min_price_move of 0.03 (3%) conflicts with TB-011 (spike_min_price_move = 0.04 or 4%) by relaxing the established price-move floor, and conflicts with TB-013 (liquidity-aware price thresholds permitting 2% for >100k baseline liquidity) and TB-021/TB-022 (which establish 5% for event markets and 3% for short-duration markets, respectively). Finally, the proposal lacks specification of how duration-based and market-type overrides will be implemented and enforced, creating ambiguity about whether TB-003 (2% requirement for illiquid markets), TB-004 (ultra-thin market volume rule), and TB-008 (watch-tier escalation logic) will be properly preserved.
- [ ] **TB-038** `rejected` — Implement a trades-to-quotes ratio filter: require executed trade volume ≥60% of reported volume delta to exclude quote-stuffing and liquidity-booking noise
  - **Governor rejection**: Proposed min_volume_delta of 50000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 50000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <500k baseline volume. Additionally, proposed min_price_move of 0.03 (3%) conflicts with TB-011 (spike_min_price_move = 0.04 or 4%) by relaxing the established price-move floor, and conflicts with TB-013 (liquidity-aware price thresholds permitting 2% for >100k baseline liquidity) and TB-021/TB-022 (which establish 5% for event markets and 3% for short-duration markets, respectively). Finally, the proposal lacks specification of how duration-based and market-type overrides will be implemented and enforced, creating ambiguity about whether TB-003 (2% requirement for illiquid markets), TB-004 (ultra-thin market volume rule), and TB-008 (watch-tier escalation logic) will be properly preserved.

---

## 2026-04-07 — Advisor snapshot 288

### Summary
The detector is triggering heavily on quote-driven volume spikes and single-sided order flow without price confirmation or sustained follow-through, particularly in thin prediction markets and short-duration binary contracts. Most false positives lack fundamental conviction (low yes probability, isolated trades).

### Next step
Implement a multi-factor confirmation gate: require either (1) price move >2% + volume delta >10k, OR (2) sustained directional trades (≥50 contracts in same direction within 5 min window) regardless of price move. This filters mechanical/liquidity-driven noise while preserving genuine conviction flow.

### Suggested thresholds
`min_volume_delta` → `12000.0`, `min_price_move` → `0.015`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-039** `rejected` — Add trades-to-quotes ratio filter: reject signals where quote volume >80% of total volume delta, to exclude pure market-making quote layering
  - **Governor rejection**: Proposed min_price_move of 0.015 (1.5%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal relaxes this floor by 62.5%, reintroducing the marginal-move noise that TB-011 was designed to suppress. Additionally, proposed min_volume_delta of 12000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 12000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <120k baseline volume. Finally, proposed score_threshold of 3.5 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the sustained-directional-trades override is not explicitly coded to preserve those conditions. The multi-factor confirmation gate (price >2% + volume >10k OR sustained directional flow ≥50 contracts) is architecturally sound, but must preserve TB-011's 4% price-move floor and TB-014's liquidity-aware multiplier framework, not replace them with lower fixed thresholds.
- [ ] **TB-040** `rejected` — Require minimum follow-through volume: only emit watch-tier signals if ≥50 contracts execute in spike direction within 5-minute window after initial spike detection
  - **Governor rejection**: Proposed min_price_move of 0.015 (1.5%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal relaxes this floor by 62.5%, reintroducing the marginal-move noise that TB-011 was designed to suppress. Additionally, proposed min_volume_delta of 12000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 12000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <120k baseline volume. Finally, proposed score_threshold of 3.5 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the sustained-directional-trades override is not explicitly coded to preserve those conditions. The multi-factor confirmation gate (price >2% + volume >10k OR sustained directional flow ≥50 contracts) is architecturally sound, but must preserve TB-011's 4% price-move floor and TB-014's liquidity-aware multiplier framework, not replace them with lower fixed thresholds.
- [ ] **TB-041** `rejected` — Implement price-confirmation gate by market type: for binary/15-min markets, require >1.5% price move to trigger notable-tier; for longer-duration prediction markets, require >3% for notable-tier
  - **Governor rejection**: Proposed min_price_move of 0.015 (1.5%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal relaxes this floor by 62.5%, reintroducing the marginal-move noise that TB-011 was designed to suppress. Additionally, proposed min_volume_delta of 12000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 12000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <120k baseline volume. Finally, proposed score_threshold of 3.5 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the sustained-directional-trades override is not explicitly coded to preserve those conditions. The multi-factor confirmation gate (price >2% + volume >10k OR sustained directional flow ≥50 contracts) is architecturally sound, but must preserve TB-011's 4% price-move floor and TB-014's liquidity-aware multiplier framework, not replace them with lower fixed thresholds.
- [ ] **TB-042** `rejected` — Lower single-trade minimum size: filter out isolated sub-5-contract trades before computing volume delta, since these are noise in thin markets
  - **Governor rejection**: Proposed min_price_move of 0.015 (1.5%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal relaxes this floor by 62.5%, reintroducing the marginal-move noise that TB-011 was designed to suppress. Additionally, proposed min_volume_delta of 12000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 12000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <120k baseline volume. Finally, proposed score_threshold of 3.5 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the sustained-directional-trades override is not explicitly coded to preserve those conditions. The multi-factor confirmation gate (price >2% + volume >10k OR sustained directional flow ≥50 contracts) is architecturally sound, but must preserve TB-011's 4% price-move floor and TB-014's liquidity-aware multiplier framework, not replace them with lower fixed thresholds.
- [ ] **TB-043** `rejected` — Add conviction filter: reduce score weight (or suppress entirely) for signals where market yes-probability is <0.15, indicating low belief in the spike direction
  - **Governor rejection**: Proposed min_price_move of 0.015 (1.5%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal relaxes this floor by 62.5%, reintroducing the marginal-move noise that TB-011 was designed to suppress. Additionally, proposed min_volume_delta of 12000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 12000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <120k baseline volume. Finally, proposed score_threshold of 3.5 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the sustained-directional-trades override is not explicitly coded to preserve those conditions. The multi-factor confirmation gate (price >2% + volume >10k OR sustained directional flow ≥50 contracts) is architecturally sound, but must preserve TB-011's 4% price-move floor and TB-014's liquidity-aware multiplier framework, not replace them with lower fixed thresholds.

---

## 2026-04-07 — Advisor snapshot 289

### Summary
The detector is triggering on quote-driven and mechanical order flow without fundamental conviction, particularly in thin markets and short-duration binaries. Most false positives show volume spikes decoupled from price movement or multi-tick conviction.

### Next step
Implement a price-confirmation requirement (minimum 1-2% move) paired with a follow-through volume filter (50+ matching contracts within 5 minutes) to distinguish conviction-driven flow from tactical/liquidity-driven spikes.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.01`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-044** `rejected` — For watch-tier signals in sub-5% price moves, require minimum volume delta of 20,000+ contracts to filter market-making noise in thin markets.
  - **Governor rejection**: Proposed min_price_move of 0.01 (1%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal relaxes this floor by 75%, reintroducing the marginal-move noise that TB-011 was designed to suppress. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 5.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the follow-through volume filter is not explicitly coded to preserve those conditions. The follow-through conviction gate (50+ matching contracts within 5 minutes) is architecturally sound and compatible with TB-005 (order-flow coherence) and TB-007 (directional trade-flow confirmation >60%), but must preserve TB-011's 4% price-move floor and TB-014's liquidity-aware multiplier framework rather than replace them with lower fixed thresholds.
- [ ] **TB-045** `rejected` — Add a trades-to-quotes ratio filter: reject signals where quote volume exceeds executed trade volume by >2:1 ratio, or where single-contract trades dominate the spike.
  - **Governor rejection**: Proposed min_price_move of 0.01 (1%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal relaxes this floor by 75%, reintroducing the marginal-move noise that TB-011 was designed to suppress. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 5.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the follow-through volume filter is not explicitly coded to preserve those conditions. The follow-through conviction gate (50+ matching contracts within 5 minutes) is architecturally sound and compatible with TB-005 (order-flow coherence) and TB-007 (directional trade-flow confirmation >60%), but must preserve TB-011's 4% price-move floor and TB-014's liquidity-aware multiplier framework rather than replace them with lower fixed thresholds.
- [ ] **TB-046** `rejected` — For 15-minute binary markets specifically, raise the baseline price-move requirement to 1%+ or require multi-order confirmation at similar price levels rather than single large quotes.
  - **Governor rejection**: Proposed min_price_move of 0.01 (1%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal relaxes this floor by 75%, reintroducing the marginal-move noise that TB-011 was designed to suppress. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 5.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the follow-through volume filter is not explicitly coded to preserve those conditions. The follow-through conviction gate (50+ matching contracts within 5 minutes) is architecturally sound and compatible with TB-005 (order-flow coherence) and TB-007 (directional trade-flow confirmation >60%), but must preserve TB-011's 4% price-move floor and TB-014's liquidity-aware multiplier framework rather than replace them with lower fixed thresholds.
- [ ] **TB-047** `rejected` — Implement 5-minute follow-through validation: spike triggers only emit signal if ≥50 contracts execute in the same direction within 5 minutes, filtering isolated outlier transactions.
  - **Governor rejection**: Proposed min_price_move of 0.01 (1%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal relaxes this floor by 75%, reintroducing the marginal-move noise that TB-011 was designed to suppress. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 5.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the follow-through volume filter is not explicitly coded to preserve those conditions. The follow-through conviction gate (50+ matching contracts within 5 minutes) is architecturally sound and compatible with TB-005 (order-flow coherence) and TB-007 (directional trade-flow confirmation >60%), but must preserve TB-011's 4% price-move floor and TB-014's liquidity-aware multiplier framework rather than replace them with lower fixed thresholds.

---

## 2026-04-07 — Advisor snapshot 290

### Summary
The detector is generating false positives primarily from quote-side volume spikes without sustained trade follow-through, and from tactical order flow in thin markets that lacks fundamental conviction. Most noise occurs at watch tier with low yes-probability and minimal price confirmation.

### Next step
Implement a trades-to-quotes ratio filter and require minimum price confirmation (1-2%) alongside volume spikes to distinguish tactical positioning from genuine conviction flow.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.01`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-048** `rejected` — Add executed trades-to-quotes ratio requirement (minimum 0.5) to filter quote-stuffing and unexecuted order book inflation
  - **Governor rejection**: Proposed min_price_move of 0.01 (1%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal relaxes this floor by 75%, reintroducing the marginal-move noise that TB-011 was designed to suppress. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 5.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the trades-to-quotes ratio filter is not explicitly coded to preserve those conditions. The trades-to-quotes ratio filter itself is architecturally sound and compatible with TB-004 (ultra-thin market volume rule) and TB-005 (order-flow coherence), but must preserve TB-011's 4% price-move floor and TB-014's liquidity-aware multiplier framework rather than replace them with lower fixed thresholds.
- [ ] **TB-049** `rejected` — For watch tier: require minimum 1% price move alongside volume delta, or implement 5-minute follow-through filter requiring 50+ contracts in spike direction
  - **Governor rejection**: Proposed min_price_move of 0.01 (1%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal relaxes this floor by 75%, reintroducing the marginal-move noise that TB-011 was designed to suppress. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 5.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the trades-to-quotes ratio filter is not explicitly coded to preserve those conditions. The trades-to-quotes ratio filter itself is architecturally sound and compatible with TB-004 (ultra-thin market volume rule) and TB-005 (order-flow coherence), but must preserve TB-011's 4% price-move floor and TB-014's liquidity-aware multiplier framework rather than replace them with lower fixed thresholds.
- [ ] **TB-050** `rejected` — Raise spike_min_volume_delta to 15000 for watch tier and implement market-volatility-adjusted thresholds, as thin markets naturally generate high volume_delta ratios from small order sizes
  - **Governor rejection**: Proposed min_price_move of 0.01 (1%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal relaxes this floor by 75%, reintroducing the marginal-move noise that TB-011 was designed to suppress. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 5.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the trades-to-quotes ratio filter is not explicitly coded to preserve those conditions. The trades-to-quotes ratio filter itself is architecturally sound and compatible with TB-004 (ultra-thin market volume rule) and TB-005 (order-flow coherence), but must preserve TB-011's 4% price-move floor and TB-014's liquidity-aware multiplier framework rather than replace them with lower fixed thresholds.
- [ ] **TB-051** `rejected` — For binary/short-duration markets (15M, events <30 days out): increase baseline score threshold by 20-30% or require sustained multi-tick price movement rather than isolated outliers
  - **Governor rejection**: Proposed min_price_move of 0.01 (1%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal relaxes this floor by 75%, reintroducing the marginal-move noise that TB-011 was designed to suppress. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores liquidity-aware context and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 5.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the trades-to-quotes ratio filter is not explicitly coded to preserve those conditions. The trades-to-quotes ratio filter itself is architecturally sound and compatible with TB-004 (ultra-thin market volume rule) and TB-005 (order-flow coherence), but must preserve TB-011's 4% price-move floor and TB-014's liquidity-aware multiplier framework rather than replace them with lower fixed thresholds.

---

## 2026-04-07 — Advisor snapshot 291

### Summary
Most signals are noise driven by quote-only spikes, single-sided order book activity, and small price moves in thin markets without sustained follow-through. The detector is too sensitive to tactical order flow lacking fundamental conviction.

### Next step
Require minimum executed trade volume (not quotes alone) as a gating filter before scoring, and enforce price-move confirmation (>1–2%) alongside volume spikes to reduce false positives in low-liquidity prediction markets.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-052** `rejected` — Filter out quote-only events (side='-') and unexecuted orders from volume delta calculations; count only actual executed trades.
  - **Governor rejection**: Proposed min_price_move of 0.05 (5%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal raises this floor by 25%, which contradicts the historical tightening decision. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 5.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if not explicitly coded to preserve those conditions. The recommendation to require executed trade volume and price-move confirmation is architecturally sound and compatible with TB-004 (ultra-thin market volume rule), TB-005 (order-flow coherence), and TB-007 (directional trade-flow confirmation >60%), but must be implemented as additive gates that preserve TB-011's 4% floor and TB-014's liquidity-aware multiplier framework rather than replacing them with higher fixed thresholds.
- [ ] **TB-053** `rejected` — Require a trades-to-quotes ratio (e.g., ≥30% of flagged volume must be executed trades) or minimum follow-through volume of 50+ contracts in the same direction within 5 minutes to validate conviction.
  - **Governor rejection**: Proposed min_price_move of 0.05 (5%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal raises this floor by 25%, which contradicts the historical tightening decision. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 5.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if not explicitly coded to preserve those conditions. The recommendation to require executed trade volume and price-move confirmation is architecturally sound and compatible with TB-004 (ultra-thin market volume rule), TB-005 (order-flow coherence), and TB-007 (directional trade-flow confirmation >60%), but must be implemented as additive gates that preserve TB-011's 4% floor and TB-014's liquidity-aware multiplier framework rather than replacing them with higher fixed thresholds.
- [ ] **TB-054** `rejected` — Raise minimum price-move requirement to 3–5% for watch tier and 5%+ for notable tier to exclude market-making noise in thin markets.
  - **Governor rejection**: Proposed min_price_move of 0.05 (5%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal raises this floor by 25%, which contradicts the historical tightening decision. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 5.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if not explicitly coded to preserve those conditions. The recommendation to require executed trade volume and price-move confirmation is architecturally sound and compatible with TB-004 (ultra-thin market volume rule), TB-005 (order-flow coherence), and TB-007 (directional trade-flow confirmation >60%), but must be implemented as additive gates that preserve TB-011's 4% floor and TB-014's liquidity-aware multiplier framework rather than replacing them with higher fixed thresholds.
- [ ] **TB-055** `rejected` — For 15-minute binary markets, require ≥1% price confirmation alongside volume spikes, or raise baseline score thresholds to filter tactical order flow.
  - **Governor rejection**: Proposed min_price_move of 0.05 (5%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal raises this floor by 25%, which contradicts the historical tightening decision. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 5.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if not explicitly coded to preserve those conditions. The recommendation to require executed trade volume and price-move confirmation is architecturally sound and compatible with TB-004 (ultra-thin market volume rule), TB-005 (order-flow coherence), and TB-007 (directional trade-flow confirmation >60%), but must be implemented as additive gates that preserve TB-011's 4% floor and TB-014's liquidity-aware multiplier framework rather than replacing them with higher fixed thresholds.
- [ ] **TB-056** `rejected` — Implement a minimum trade size filter (e.g., exclude single-contract trades) and require sustained multi-tick movement rather than isolated outlier transactions.
  - **Governor rejection**: Proposed min_price_move of 0.05 (5%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal raises this floor by 25%, which contradicts the historical tightening decision. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 5.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if not explicitly coded to preserve those conditions. The recommendation to require executed trade volume and price-move confirmation is architecturally sound and compatible with TB-004 (ultra-thin market volume rule), TB-005 (order-flow coherence), and TB-007 (directional trade-flow confirmation >60%), but must be implemented as additive gates that preserve TB-011's 4% floor and TB-014's liquidity-aware multiplier framework rather than replacing them with higher fixed thresholds.

---

## 2026-04-07 — Advisor snapshot 292

### Summary
The detector is generating watch/notable signals on quote-heavy, thin-liquidity events with minimal price conviction. Most false positives lack either sustained trade follow-through or meaningful price moves (>3%), indicating the system is too sensitive to quote-only volume spikes.

### Next step
Implement a trades-to-quotes filter: require that ≥50% of flagged volume delta consists of executed trades (not quotes), and raise the minimum price move threshold to 0.04 (4%) for watch tier and 0.06 (6%) for notable tier to filter out market-making noise.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.04`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-057** `rejected` — Exclude quote-only events (side='-') and require minimum 50% executed trade ratio within the spike window to reduce false positives in low-liquidity markets.
  - **Governor rejection**: Proposed min_volume_delta of 15000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 15000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <150k baseline volume. Additionally, proposed min_price_move of 0.04 (4%) matches TB-011's established floor but proposed notable-tier threshold of 0.06 (6%) lacks specification for how it will be enforced relative to TB-001 (notable requires ≥0.5%), TB-013 (liquidity-aware thresholds permitting 2% for >100k baseline), and TB-021/TB-022 (which establish 5% for event markets and 3% for short-duration markets). Finally, proposed score_threshold of 5.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the trades-to-quotes filter is not explicitly coded as an additive gate that preserves tier-specific conditions. The trades-to-quotes ratio filter itself (≥50% executed trades) is architecturally sound and compatible with TB-004, TB-005, and TB-007, but must preserve TB-014's liquidity-aware multiplier framework rather than replace it with a fixed floor.
- [ ] **TB-058** `rejected` — Raise spike_min_price_move to 0.04 for watch tier and 0.06 for notable tier; sub-4% moves on modest volume are typical market-making activity in prediction markets.
  - **Governor rejection**: Proposed min_volume_delta of 15000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 15000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <150k baseline volume. Additionally, proposed min_price_move of 0.04 (4%) matches TB-011's established floor but proposed notable-tier threshold of 0.06 (6%) lacks specification for how it will be enforced relative to TB-001 (notable requires ≥0.5%), TB-013 (liquidity-aware thresholds permitting 2% for >100k baseline), and TB-021/TB-022 (which establish 5% for event markets and 3% for short-duration markets). Finally, proposed score_threshold of 5.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the trades-to-quotes filter is not explicitly coded as an additive gate that preserves tier-specific conditions. The trades-to-quotes ratio filter itself (≥50% executed trades) is architecturally sound and compatible with TB-004, TB-005, and TB-007, but must preserve TB-014's liquidity-aware multiplier framework rather than replace it with a fixed floor.
- [ ] **TB-059** `rejected` — Introduce a follow-through volume requirement: for single-sided spikes, require ≥50 contracts of matching directional trades within 5 minutes post-spike to confirm conviction.
  - **Governor rejection**: Proposed min_volume_delta of 15000.0 directly conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets). A fixed 15000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <150k baseline volume. Additionally, proposed min_price_move of 0.04 (4%) matches TB-011's established floor but proposed notable-tier threshold of 0.06 (6%) lacks specification for how it will be enforced relative to TB-001 (notable requires ≥0.5%), TB-013 (liquidity-aware thresholds permitting 2% for >100k baseline), and TB-021/TB-022 (which establish 5% for event markets and 3% for short-duration markets). Finally, proposed score_threshold of 5.0 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the trades-to-quotes filter is not explicitly coded as an additive gate that preserves tier-specific conditions. The trades-to-quotes ratio filter itself (≥50% executed trades) is architecturally sound and compatible with TB-004, TB-005, and TB-007, but must preserve TB-014's liquidity-aware multiplier framework rather than replace it with a fixed floor.

---

## 2026-04-07 — Advisor snapshot 293

### Summary
False positives are driven by quote-only volume spikes, single-sided order imbalances without follow-through trades, and low-conviction price moves in thin markets. The detector is triggering on market-making activity and tactical positioning rather than fundamental flow.

### Next step
Require minimum executed trade volume (not just quote delta) and enforce price-move confirmation thresholds that scale by market liquidity tier, filtering out quote-only and unconfirmed order imbalances.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`, `score_threshold` → `5.5`

### Recommendations

- [ ] **TB-060** `rejected` — Exclude quote-only events (side='-') from volume delta calculations, or require ≥10% of flagged volume to be executed trades rather than working quotes
  - **Governor rejection**: Proposed min_price_move of 0.05 (5%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal raises this floor by 25%, contradicting the historical tightening decision. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 5.5 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if not explicitly coded to preserve those conditions. The recommendation to require executed trade volume and price-move confirmation is architecturally sound and compatible with TB-004 (ultra-thin market volume rule), TB-005 (order-flow coherence), and TB-007 (directional trade-flow confirmation >60%), but must be implemented as additive gates that preserve TB-011's 4% floor and TB-014's liquidity-aware multiplier framework rather than replacing them with higher fixed thresholds.
- [ ] **TB-061** `rejected` — For watch-tier signals, require priceΔ ≥0.05 (5%) in thin markets, or enforce 50+ contract follow-through volume within 5 minutes matching spike direction to confirm conviction
  - **Governor rejection**: Proposed min_price_move of 0.05 (5%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal raises this floor by 25%, contradicting the historical tightening decision. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 5.5 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if not explicitly coded to preserve those conditions. The recommendation to require executed trade volume and price-move confirmation is architecturally sound and compatible with TB-004 (ultra-thin market volume rule), TB-005 (order-flow coherence), and TB-007 (directional trade-flow confirmation >60%), but must be implemented as additive gates that preserve TB-011's 4% floor and TB-014's liquidity-aware multiplier framework rather than replacing them with higher fixed thresholds.
- [ ] **TB-062** `rejected` — For 15-minute binary markets, require priceΔ ≥0.01 (1%) alongside volume spike to filter tactical order flow; consider raising baseline score threshold by 20–30% for sub-1% price moves
  - **Governor rejection**: Proposed min_price_move of 0.05 (5%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal raises this floor by 25%, contradicting the historical tightening decision. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 5.5 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if not explicitly coded to preserve those conditions. The recommendation to require executed trade volume and price-move confirmation is architecturally sound and compatible with TB-004 (ultra-thin market volume rule), TB-005 (order-flow coherence), and TB-007 (directional trade-flow confirmation >60%), but must be implemented as additive gates that preserve TB-011's 4% floor and TB-014's liquidity-aware multiplier framework rather than replacing them with higher fixed thresholds.

---

## 2026-04-07 — Advisor snapshot 294

### Summary
Three consecutive false positives reveal that quote-only activity, single-sided spikes without follow-through, and low-liquidity market-making are triggering signals on thin volume and modest price moves.

### Next step
Implement a follow-through validation rule: require minimum 50+ contracts of matching-direction trades within 5 minutes of initial spike to confirm genuine flow, rather than relying on volume delta and price move alone.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-063** `rejected` — Exclude quote-only events (side='-') from volume_delta calculations, or require ≥10% of flagged volume to consist of executed trades rather than quotes.
  - **Governor rejection**: Proposed min_price_move of 0.05 (5%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal raises this floor by 25%, contradicting the historical tightening decision. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 3.5 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the follow-through volume filter is not explicitly coded as an additive gate that preserves tier-specific conditions. The follow-through conviction gate (50+ matching contracts within 5 minutes) is architecturally sound and compatible with TB-005 (order-flow coherence) and TB-007 (directional trade-flow confirmation >60%), but must preserve TB-011's 4% price-move floor and TB-014's liquidity-aware multiplier framework rather than replace them with higher fixed thresholds.
- [ ] **TB-064** `rejected` — Add follow-through volume gate: spike must be accompanied by ≥50 contracts of same-direction trades within 5-minute window to avoid single-sided quote spikes.
  - **Governor rejection**: Proposed min_price_move of 0.05 (5%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal raises this floor by 25%, contradicting the historical tightening decision. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 3.5 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the follow-through volume filter is not explicitly coded as an additive gate that preserves tier-specific conditions. The follow-through conviction gate (50+ matching contracts within 5 minutes) is architecturally sound and compatible with TB-005 (order-flow coherence) and TB-007 (directional trade-flow confirmation >60%), but must preserve TB-011's 4% price-move floor and TB-014's liquidity-aware multiplier framework rather than replace them with higher fixed thresholds.
- [ ] **TB-065** `rejected` — Raise min_price_move threshold to 0.05 (5%) for watch tier in sub-50k volume delta markets, since sub-5% moves on small deltas are typical thin-market making.
  - **Governor rejection**: Proposed min_price_move of 0.05 (5%) directly conflicts with TB-011, which explicitly sets spike_min_price_move = 0.04 (4%) as a durable constraint to filter marginal moves in low-liquidity pairs. The proposal raises this floor by 25%, contradicting the historical tightening decision. Additionally, proposed min_volume_delta of 15000 conflicts with TB-014, which establishes spike_min_volume_delta floor of 800–1000 contracts with percentage-of-baseline multipliers (15–20% on thin markets, 10% on deep markets); a fixed 15000-contract floor ignores the liquidity-aware multiplier framework and would suppress legitimate signals on markets with <150k baseline volume. Finally, proposed score_threshold of 3.5 lacks granular tier definition and risks circumventing TB-008's watch-tier escalation logic (volΔ > 3x or volΔ > 1.5x paired with priceΔ > 1%) if the follow-through volume filter is not explicitly coded as an additive gate that preserves tier-specific conditions. The follow-through conviction gate (50+ matching contracts within 5 minutes) is architecturally sound and compatible with TB-005 (order-flow coherence) and TB-007 (directional trade-flow confirmation >60%), but must preserve TB-011's 4% price-move floor and TB-014's liquidity-aware multiplier framework rather than replace them with higher fixed thresholds.

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
