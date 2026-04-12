
## 2026-04-12 — Advisor snapshot A

### Summary
Whale-cluster signals on high-frequency 15m BTC markets trigger frequently with low price moves (mostly 0%), leading to many false positives labeled as noise/no/high or signal/no/high/medium, even at moderate volumes like 400. True positives are rare and often have higher volumes or slight price moves.

### Next step
Require minimum price move >0% for whale-cluster tier in 15m BTC markets to filter noise without muting volume spikes.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.01`, `score_threshold` → `8.5`

### Recommendations

- [x] **TB-001** `applied` — Raise whale-cluster volume delta threshold to 1000 for 15m BTC to catch only stronger signals.
- [x] **TB-002** `applied` — Increase spike_score_threshold to 8.5 to reduce low-confidence triggers.
- [x] **TB-003** `applied` — Raise whale-cluster whale count threshold to 50 in 120s and λ to 0.01 for 15m BTC markets.

---

## 2026-04-12 — Advisor snapshot B

### Summary
Whale-cluster signals on high-frequency BTC 15m markets trigger frequently with score=8.0 and volΔ ≥400 despite minimal or zero price moves, resulting in high false positives (many 'signal/no/high') even at yes probabilities 0.65-0.85, while true signals are inconsistent.

### Next step
For BTC 15m markets, raise whale-cluster thresholds to filter noise from high baseline volume and rapid counter-flows.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-004** `planned` — Raise whale-cluster threshold to 50 whales in 120s for high-frequency BTC 15m markets.
- [ ] **TB-005** `planned` — Raise whale-cluster λ threshold to 0.01 for 15-min BTC markets.
- [ ] **TB-006** `planned` — Require min_price_move ≥0.02 for whale-cluster tier in BTC 15m to ensure price impact.

---

## 2026-04-12 — Advisor snapshot C

### Summary
Whale-cluster signals on low-volume 15m BTC markets trigger frequently with high scores and volΔ around 400 despite no price movement, leading to many false positives labeled as noise/no, while higher volΔ instances are mixed and some genuine signals are missed.

### Next step
Require volume delta >0.5x baseline and raise whale-cluster threshold to 50 whales in 120s for 15m BTC markets.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-007** `planned` — Adjust whale-cluster detector to require volume delta >0.5x baseline to filter low-volume clusters.
- [ ] **TB-008** `planned` — Raise whale-cluster threshold to 50 whales in 120s for high-frequency BTC 15m markets.
- [ ] **TB-009** `planned` — Increase whale-cluster λ threshold to 0.01 to reduce noise from rapid counter-flow reversals.

---

## 2026-04-12 — Advisor snapshot D

### Summary
High whale-cluster signals on low-volume 15m BTC markets trigger many false positives despite high scores and yes probabilities, especially with zero price moves and insufficient relative volume spikes.

### Next step
Require volume delta >0.5x baseline for whale-cluster in 15m BTC markets and raise cluster threshold to 50 whales in 120s.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-010** `planned` — Raise whale-cluster λ threshold to 0.01 for 15-min BTC markets
- [ ] **TB-011** `planned` — Require minimum price move >0.005 (0.5%) for zero-price-delta signals
- [ ] **TB-012** `planned` — Increase spike_score_threshold to 8.5 for whale-cluster tier in low-volume markets

---

## 2026-04-12 — Advisor snapshot E

### Summary
The whale-cluster detector is generating high-confidence signals (score=8.0) with strong probability mass (yes=0.65–0.76) but lacks price confirmation; 10 of 20 signals are labeled false positives despite elevated volume deltas, indicating the detector conflates whale clustering activity with predictive edge.

### Next step
Require concurrent price movement (priceΔ ≥ 0.01) as a gate condition for whale-cluster signals in 15-minute BTC markets, reducing noise from coordinated but non-directional order flow.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-013** `planned` — Enforce spike_min_price_move ≥ 0.01 (1%) for whale-cluster tier signals—all true-positive labels in your set include priceΔ > 0, whereas false positives cluster around priceΔ = 0.0
- [ ] **TB-014** `planned` — Raise whale-cluster volume threshold to >500 units (not absolute baseline-relative, but observed signal magnitude) to filter low-conviction clusters that analysts marked noise/unclear
- [ ] **TB-015** `planned` — Add a temporal persistence filter: require volume delta to sustain for ≥2 consecutive 15-minute bars before emitting signal, as single-bar whale clusters without follow-through lack informative value

---

## 2026-04-12 — Advisor snapshot F

### Summary
All signals are whale-cluster detections on low-volume 15m BTC markets with high scores (8.0) but zero or minimal price moves, resulting in many false positives labeled as signal/no or noise despite varying volume deltas from 320-1250.

### Next step
Require minimum price move >0.005 (0.5%) for whale-cluster signals on 15m BTC markets to filter out detections without directional impact.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-016** `planned` — Raise spike_min_price_move to 0.005 to eliminate zero-price-move false positives.
- [ ] **TB-017** `planned` — Increase spike_min_volume_delta to 500 for 15m low-volume markets per analyst feedback on baseline clustering.
- [ ] **TB-018** `planned` — Tier score_threshold by market: raise to 8.5 for high-frequency BTC 15m to reduce noise.

---

## 2026-04-12 — Advisor snapshot G

### Summary
Whale-cluster signals on low-volume 15m BTC markets trigger frequent false positives due to isolated clustering without price movement or sufficient volume delta relative to baseline, despite consistent high scores around 8.0.

### Next step
Require whale-cluster signals to have volΔ >0.5x baseline AND (priceΔ >0.01 in cluster direction OR volΔ >5% baseline) to filter noise while preserving true spikes.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-019** `planned` — Raise whale-cluster volume delta requirement to >0.5x baseline for 15m BTC markets
- [ ] **TB-020** `planned` — Require minimum priceΔ >0.01 or directional momentum >1% within spike window for whale-clusters
- [ ] **TB-021** `planned` — Increase whale-cluster threshold to 50 whales in 120s and λ >0.01 for high-frequency markets

---

## 2026-04-12 — Advisor snapshot H

### Summary
Whale-cluster signals trigger frequent false positives on low volume deltas (200-400) and negligible price moves (0-0.1%), often labeled as noise from normal flow, rebalancing, or micro-orders despite high scores, while true signals show higher volumes (800+) or analyst confirmation.

### Next step
Raise whale-cluster min volume delta to at least 5% of baseline volume and require price delta >0.01 or sustained directional agreement >80%.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.01`, `score_threshold` → `10.0`

### Recommendations

- [ ] **TB-022** `planned` — Set min_volume_delta to 5% of baseline to filter sub-baseline micro-spikes.
- [ ] **TB-023** `planned` — Require min_price_move >0.01 to ignore zero-impact clusters.
- [ ] **TB-024** `planned` — Raise score_threshold to 10.0 for whale-cluster tier to reduce low-confidence triggers.

---

## 2026-04-12 — Advisor snapshot I

### Summary
High false positives in whale-cluster detections for ultra-short 15M BTC markets due to routine microstructure noise with low price moves (≤0.001) and modest volume deltas, despite high scores; watch tier signals also trigger noise in low-liquidity markets.

### Next step
Require volume delta to exceed 5-10% of baseline volume before triggering whale-cluster alerts in ≤15min markets to filter routine execution patterns.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-025** `planned` — Raise min_volume_delta to 500+ for 15M crypto markets or tier it by baseline liquidity.
- [ ] **TB-026** `planned` — Increase min_price_move to 0.005 (0.5%) to ignore signals with negligible price impact.
- [ ] **TB-027** `planned` — For low-liquidity markets (e.g. sports props), set volΔ threshold to 1-2% of baseline.

---

## 2026-04-12 — Advisor snapshot J

### Summary
False positives dominate in low-volume 15-minute BTC markets due to whale-cluster detections on modest absolute volume deltas (200-700) against very low baselines (~50), lacking price moves and often reflecting routine or mechanical flow rather than informed trading.

### Next step
Raise min_volume_delta to 5% of 1-hour baseline volume for 15-min markets and increase whale-cluster threshold to 50 whales in 120s.

### Suggested thresholds
`min_volume_delta` → `250.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-028** `planned` — Set min_volume_delta >= 5% of baseline to filter sub-baseline routine spikes.
- [ ] **TB-029** `planned` — Require whale-cluster >=50 whales in 120s for thin 15-min BTC markets.
- [ ] **TB-030** `planned` — Raise min_price_move to 0.005 (0.5%) to ensure directional informativeness.

---

## 2026-04-12 — Advisor snapshot K

### Summary
Whale-cluster signals on 15-minute BTC markets trigger frequent false positives due to low volume-delta thresholds capturing quote-spam, thin order-book noise, and routine algorithmic activity despite high model confidence scores.

### Next step
Raise spike_min_volume_delta to require at least 5x baseline volume (e.g., 250+ assuming baseline ~50) for whale-cluster tier in 15-min markets.

### Suggested thresholds
`min_volume_delta` → `250.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-031** `planned` — Increase min_volume_delta threshold to 5-10x baseline to filter sub-baseline spikes.
- [ ] **TB-032** `planned` — Require minimum priceΔ of 0.005 (0.5%) alongside volume spikes.
- [ ] **TB-033** `planned` — Add tier-specific rule for whale-cluster: min 50 whales in 120s window.

---

## 2026-04-12 — Advisor snapshot L

### Summary
False positives dominate in whale-cluster signals for 15-minute BTC markets, especially with zero price movement despite high volume deltas, due to mechanical liquidity noise, quote-spam, and thin order books in near-1.0 priced contracts.

### Next step
Require minimum price move >0.0 and raise whale-cluster threshold to 50 whales in 120s for 15-min BTC markets.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.003`

### Recommendations

- [ ] **TB-034** `planned` — Raise min_volume_delta to 5-10x baseline volume multiplier.
- [ ] **TB-035** `planned` — Set min_price_move to 0.003 (0.3%) to filter no-price-impact noise.
- [ ] **TB-036** `planned` — Increase whale-cluster size threshold to 50+ whales in 120s.

---

## 2026-04-12 — Advisor snapshot M

### Summary
False positives dominate in whale-cluster signals on high-liquidity BTC 15M markets with near-1.0 yes prices, driven by mechanical liquidity noise, quote spam, and low price impact despite high volume deltas; the single notable-tier signal was noise due to insufficient volume relative to baseline.

### Next step
Raise minimum volume delta threshold to 30x baseline for 15-minute BTC markets and increase whale-cluster threshold to 50 whales in 120s for near-1.0 priced contracts.

### Suggested thresholds
`min_volume_delta` → `30.0`

### Recommendations

- [ ] **TB-037** `planned` — Require volume delta >30x baseline for all 15M BTC spike detections to filter liquidity-driven noise.
- [ ] **TB-038** `planned` — For whale-cluster tier, raise threshold to 50+ whales in 120s in high-liquidity endgame markets.
- [ ] **TB-039** `planned` — Add min absolute volume multiplier (e.g., 5-10x baseline) for thin/low-liquidity markets to avoid negligible volume false positives.

---

## 2026-04-12 — Advisor snapshot N

### Summary
Recent signals show false positives from high volume spikes without meaningful price movement, as in KXBTC15M with volΔ=48418.98 but priceΔ=0.0, despite high score and analyst confirmation as medium signal.

### Next step
Require minimum price move to filter volume-only spikes.

### Suggested thresholds
`min_volume_delta` → `100000.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-040** `planned` — Increase min_price_move to 0.02 to exclude zero-price-change triggers
- [ ] **TB-041** `planned` — Raise min_volume_delta to 100000 for stricter volume filtering
- [ ] **TB-042** `planned` — Add rule: emit only if priceΔ >= 0.01 AND score > 100

---

## 2026-04-12 — Advisor snapshot O

### Summary
Recent signals are all labeled as true positives (signal/yes), but two exhibit very low price moves (0.01 and 0.0) despite high volume deltas, indicating a pattern where volume spikes alone trigger detections for events with minimal price impact.

### Next step
Raise min_price_move threshold to filter out low-impact volume-only spikes.

### Suggested thresholds
`min_volume_delta` → `100000.0`, `min_price_move` → `0.015`, `score_threshold` → `10000.0`

### Recommendations

- [ ] **TB-043** `planned` — Increase spike_min_price_move from 0.01 to 0.015 to require more substantial price changes.
- [ ] **TB-044** `planned` — Raise spike_min_volume_delta to 100000 to focus on larger volume surges.
- [ ] **TB-045** `planned` — Increase spike_score_threshold to 10000 to prioritize higher-confidence signals.

---

## 2026-04-12 — Advisor snapshot P

### Summary
False positives are driven by whale-cluster and watch tier signals in high-liquidity BTC markets with no price movement despite volume spikes, labeled as noise or requiring tier-specific filtering.

### Next step
Require minimum price move >0 for whale-cluster and watch tiers in high-liquidity markets like 15-min BTC.

### Suggested thresholds
`min_price_move` → `0.01`, `score_threshold` → `10.0`

### Recommendations

- [ ] **TB-046** `planned` — Increase whale-cluster threshold to 5 whales in 120s for 15-min BTC markets.
- [ ] **TB-047** `planned` — Add tier-specific rules: require priceΔ >0.01 for watch and whale-cluster tiers.
- [ ] **TB-048** `planned` — Raise score_threshold to 10.0 to filter low-significance volume-only spikes.

---

## 2026-04-12 — Advisor snapshot Q

### Summary
Your detector is generating false positives in whale-cluster tiers on high-liquidity markets (BTC) where volume spikes lack corresponding price movement, while missing context-dependent signals in niche markets where volume and price both move meaningfully.

### Next step
Implement a price-movement requirement for whale-cluster tier signals: require priceΔ ≥ 0.01 (1%) when volΔ exceeds baseline, or escalate the whale-cluster threshold to 5+ whales in 120 seconds to filter low-volume clusters in high-liquidity pairs.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-049** `planned` — For whale-cluster tier: adopt the analyst suggestion of requiring 5 whales in 120s window for 15-min BTC markets to eliminate noise from dispersed small trades masquerading as coordinated activity
- [ ] **TB-050** `planned` — Enforce a coupling rule: signals with volΔ > 200k but priceΔ = 0.0 should be downweighted or filtered unless the market is known to have structural illiquidity
- [ ] **TB-051** `planned` — For notable tier: maintain current sensitivity but add a confidence floor—yes probability ≥ 0.50 to emit—to catch medium-confidence signals like KXNBAGAME-NOP (yes=0.33) before they reach production

---

## 2026-04-12 — Advisor snapshot R

### Summary
False positives occur in high-liquidity markets like 15-min BTC where small volume deltas and zero price moves trigger watch and whale-cluster signals, while sports bets need price move tolerance due to lower liquidity. Genuine signals cluster in notable tiers with high scores and volume.

### Next step
Raise min_price_move to filter zero-move noise in liquid markets and refine whale-cluster to require 5+ whales in 120s for 15-min BTC.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-052** `planned` — Set min_price_move to 0.01 minimum to eliminate zero price delta triggers.
- [ ] **TB-053** `planned` — Increase whale-cluster threshold to 5 whales in 120s for high-liquidity 15-min BTC markets.
- [ ] **TB-054** `planned` — Raise score_threshold to 10 for watch tier in liquid markets to prioritize notables.

---

## 2026-04-12 — Advisor snapshot S

### Summary
False positives are prominent in high-liquidity markets like 15-min BTC, where whale-clusters trigger on low price moves (0.0) and moderate volume despite high baseline liquidity; signals with priceΔ >=0.01 and significant volΔ are consistently high/medium conviction.

### Next step
Require minimum price move >0.0 and tailor volume thresholds by market liquidity (e.g., higher for BTC).

### Suggested thresholds
`min_price_move` → `0.01`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-055** `planned` — Increase whale-cluster threshold to 5 whales in 120s for 15-min BTC markets.
- [ ] **TB-056** `planned` — Set min_price_move to 0.01 to filter zero-price-move triggers.
- [ ] **TB-057** `planned` — Raise spike_score_threshold to 5.0 for watch-tier signals.

---

## 2026-04-12 — Advisor snapshot T

### Summary
Multiple whale-cluster signals on high-liquidity BTC 15M markets trigger with high scores but no price move and low volume deltas, labeled as noise, while NBA game signals with price moves are valid despite modest deltas.

### Next step
Require minimum price move for whale-cluster tier in high-liquidity markets like BTC.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-058** `planned` — Increase whale-cluster threshold to 5 whales in 120s for 15-min BTC markets
- [ ] **TB-059** `planned` — Set min_price_move to 0.02 globally to filter zero-price-move signals
- [ ] **TB-060** `planned` — Raise spike_score_threshold to 10.0 for whale-cluster tier

---

## 2026-04-12 — Advisor snapshot U

### Summary
Whale-cluster signals on high-liquidity BTC 15M markets show high false positives with low price moves (0.0%) and modest volume deltas, while notable/high conviction flows on other markets with price moves are true signals.

### Next step
Require minimum price move for whale-cluster tier in high-liquidity markets like BTC.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-061** `planned` — Increase whale-cluster threshold to 5 whales in 120s for 15-min BTC markets
- [ ] **TB-062** `planned` — Raise min_volume_delta to 1000 for BTC markets to filter low-volume clusters
- [ ] **TB-063** `planned` — Add tier-specific min_price_move: 0.01 for whale-cluster, 0.0 for notable/high conviction

---

## 2026-04-12 — Advisor snapshot V

### Summary
False positives are prominent in high-liquidity BTC markets from whale-cluster detections with high volume deltas but no price movement, triggering despite baseline noise. Other tiers like watch and notable show fewer issues, mostly validated as signals.

### Next step
Require minimum price move >0 for whale-cluster tier in high-liquidity markets like BTC.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-064** `planned` — Increase whale-cluster threshold to 5 whales in 120s for 15-min BTC markets as noted by analyst.
- [ ] **TB-065** `planned` — Raise min_volume_delta to 1000+ for BTC to filter low-significance clusters.
- [ ] **TB-066** `planned` — Add tier-specific score thresholds: 9.0+ for whale-cluster, lower for notable/watch.

---

## 2026-04-12 — Advisor snapshot W

### Summary
False positives in whale-cluster signals for high-liquidity 15-min BTC markets due to low volume deltas relative to baseline, despite high scores and no price movement.

### Next step
Raise whale-cluster volume delta threshold to 5x baseline and require minimum 5 whales in 120s for 15-min BTC markets.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-067** `planned` — Require min_price_move > 0.01 for whale-cluster tier in BTC markets
- [ ] **TB-068** `planned` — Increase spike_score_threshold to 9.0 for whale-cluster signals with priceΔ=0
- [ ] **TB-069** `planned` — Set tier-specific min_volume_delta: 5000 for BTC15M whale-cluster

---

## 2026-04-12 — Advisor snapshot X

### Summary
BTC 15-minute whale-cluster signals are generating false positives despite high scores (8.0), driven by low volume deltas (321-558) that lack institutional conviction in high-liquidity markets. Simultaneously, genuinely informative signals in sports betting (NBA games) and political prediction markets show much higher volume deltas and mixed yes-probabilities, suggesting tier-based threshold tuning is needed.

### Next step
Implement tier-specific volume delta thresholds: raise whale-cluster minimum to 2,000+ for BTC 15-min markets, while relaxing constraints for high-conviction flow (143 vol delta with 8% price move is valid signal) and notable sports/political markets (100k+ vol deltas are legitimate).

### Suggested thresholds
`min_volume_delta` → `2000.0`

### Recommendations

- [ ] **TB-070** `planned` — Raise spike_min_volume_delta to 2,000 for whale-cluster tier on 15-min BTC markets; current 500 threshold is generating noise in high-liquidity environments as noted by multiple analyst reviews.
- [ ] **TB-071** `planned` — Create a price-move amplifier: lower score_threshold for signals with priceΔ ≥ 0.05 (e.g., KXTRUMPSAY at 0.08 priceΔ should pass at lower volume) since price conviction is an orthogonal signal to volume clustering.
- [ ] **TB-072** `planned` — Segregate tier-based thresholds: notable/watch tiers with volΔ > 100k should use different rules than whale-cluster micro-movements; the NBA game signals (volΔ 132k–405k) are legitimate despite lower yes-probability variance.

---

## 2026-04-12 — Advisor snapshot Y

### Summary
Multiple whale-cluster signals on KXBTC15M-26APR121515-15 with low volume deltas (321-558) are triggering false positives labeled as noise/no, despite high scores around 8.0 and no price movement, while high-volume NBA game signals are correctly labeled as signal/yes.

### Next step
Raise spike_min_volume_delta threshold for 15-min BTC markets to filter low-volume whale-clusters in high-liquidity environments.

### Suggested thresholds
`min_volume_delta` → `2000.0`

### Recommendations

- [ ] **TB-073** `planned` — Increase min_volume_delta from 500 to 2000+ for BTC15M whale-cluster tier to exclude micro-clusters.
- [ ] **TB-074** `planned` — Require volΔ at least 5x baseline volume for whale-cluster in high-liquidity markets like BTC.
- [ ] **TB-075** `planned` — Raise whale-cluster rule to minimum 5 whales in 120s for 15-min BTC to ensure conviction size.

---

## 2026-04-12 — Advisor snapshot Z

### Summary
Whale-cluster signals on high-liquidity 15M BTC markets show false positives at low volume deltas (300-500) despite high scores, while larger volumes (1000+) and price moves are reliably informative; other tiers like high conviction flow perform well even with modest volumes.

### Next step
Raise whale-cluster min_volume_delta to 2000 for 15M BTC markets to filter micro-clusters.

### Suggested thresholds
`min_volume_delta` → `2000.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-076** `planned` — For whale-cluster tier on KXBTC15M, set min_volume_delta=2000 to eliminate low-conviction noise.
- [ ] **TB-077** `planned` — Require min_price_move=0.01 for whale-cluster signals with volΔ<1000.
- [ ] **TB-078** `planned` — Raise score_threshold to 10 for whale-cluster in high-liquidity markets.

---

## 2026-04-12 — Advisor snapshot 27

### Summary
The detector is generating excessive low-conviction whale-cluster signals (score=8.0, yes=0.60–0.75) with zero or minimal price moves (priceΔ=0.0), driven by moderate volume deltas (261–558) that do not represent actionable flow. Analyst feedback consistently recommends raising volume delta thresholds to filter micro-clusters in high-liquidity BTC markets.

### Next step
Raise spike_min_volume_delta for whale-cluster tier to 1,000–1,250 for 15-minute BTC markets to eliminate low-signal-to-noise clusters, while preserving high-conviction signals (score≥9.0 or yes≥0.80 with volΔ≥400).

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-079** `planned` — Increase whale-cluster volume delta threshold to 1,000+ to filter out 261–558 vol-delta signals that analysts mark as noise or low-conviction despite passing current thresholds.
- [ ] **TB-080** `planned` — Apply a price-move floor for whale-cluster detection: require priceΔ≥0.005 (0.5%) when volΔ<1,000 to exclude volume spikes decoupled from market impact.
- [ ] **TB-081** `planned` — Implement a composite gate: emit whale-cluster signals only when (score>8.5 OR yes>0.80) AND volΔ>1,000, or (score≥12 AND volΔ≥400) to preserve genuine institutional conviction while muting repetitive base-score-8.0 clusters.

---

## 2026-04-12 — Advisor snapshot 28

### Summary
Your detector is generating high-confidence whale-cluster signals (score 8.0+) on short-duration crypto markets with minimal or zero price movement, creating false positives despite elevated volume. The core issue is that volume concentration alone—without price conviction or sustained hold duration—does not reliably distinguish informed positioning from momentum-chasing or mechanical activity.

### Next step
Introduce a **price-move floor relative to recent volatility** (2–3% above trailing 15-min volatility) or require **5-minute hold confirmation** at spike price before emitting whale-cluster signals on sub-hourly timeframes. This aligns with research showing that prediction markets reward sustained informed positioning over transient clustering.

### Suggested thresholds
`min_volume_delta` → `5.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-082** `planned` — For whale-cluster tier on 15-minute markets: require minimum price move of 0.02 (2%) OR sustained signal presence across two non-overlapping 5-minute windows to filter 120-second momentum artifacts.
- [ ] **TB-083** `planned` — For political/long-dated markets (KXTRUMPSAY pattern): increase volume_delta multiplier threshold from 2.7x to 5.0x baseline to suppress single-quote mechanical spikes in low-liquidity venues.
- [ ] **TB-084** `planned` — For crypto 15-minute markets: raise minimum absolute volume floor to 5,000+ contracts on whale-cluster alerts to eliminate sub-2% baseline spikes lacking market conviction.
- [ ] **TB-085** `planned` — Add hold-duration gate: require spike price to persist for at least 5 minutes before classifying as signal-tier to separate informed flow from short-burst clustering.

---

## 2026-04-12 — Advisor snapshot 29

### Summary
The whale-cluster detector is generating high-confidence signals (score 8.0) with large volume deltas but zero or minimal price movement, creating false positives in liquid 15-minute crypto markets. Analyst feedback consistently flags volume-only spikes as noise unless accompanied by meaningful price correlation or duration confirmation.

### Next step
Implement a price-movement floor for whale-cluster signals: require minimum 2–3% price move OR sustained 5-minute hold duration at spike price before emitting signal-tier alert. This directly addresses the decoupling between volume and price that characterizes most false positives.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.02`, `score_threshold` → `10.0`

### Recommendations

- [ ] **TB-086** `planned` — Add mandatory price correlation: whale-cluster signals with priceΔ=0.0 should be downgraded to noise tier unless volume delta exceeds 1000+ contracts AND score exceeds 10.0.
- [ ] **TB-087** `planned` — Require duration confirmation: on 15-minute markets, enforce 5-minute minimum hold at spike price before classifying as genuine signal; reject 120-second clusters as momentum-chasing artifacts.
- [ ] **TB-088** `planned` — Convert volume delta to percentage-of-baseline: replace absolute thresholds with >5% of rolling 1-hour baseline volume for high-liquidity crypto pairs to normalize across market regimes.
- [ ] **TB-089** `planned` — Raise minimum absolute volume for crypto tiers: enforce 5,000+ contract minimum for whale-cluster alerts on KXBTC and similar liquid instruments to filter sub-2% baseline moves.
- [ ] **TB-090** `planned` — For political/speech markets (low liquidity, long-dated): increase volume-delta multiplier from 2.7x to 5x baseline to suppress mechanical single-quote activity.

---

## 2026-04-12 — Advisor snapshot 30

### Summary
Whale-cluster signals on low-volume 15m crypto markets like KXBTC frequently trigger false positives due to micro-spikes with no or minimal price movement, despite high scores and volume deltas around 400-1250.

### Next step
Require minimum absolute volume threshold (e.g., ≥2000 shares) or 24h baseline volume >50,000 for thin markets to filter illiquid noise.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-091** `planned` — Raise spike_min_volume_delta to 1000 to exclude sub-baseline micro-spikes.
- [ ] **TB-092** `planned` — Require volΔ ≥25% of 1h baseline volume for whale-cluster in 15m markets.
- [ ] **TB-093** `planned` — Lower whale-cluster p-value threshold to <0.001 and enforce minimum directional consensus.

---

## 2026-04-12 — Advisor snapshot 31

### Summary
Whale-cluster signals on low-volume 15m crypto markets trigger frequent false positives despite high scores, often lacking price movement, flow confirmation, or sufficient absolute volume, while true signals show higher 'yes' probabilities and occasional price deltas.

### Next step
Require minimum absolute volume threshold of 2000 shares and volΔ ≥25% of 1h baseline to filter micro-spikes in thin markets.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-094** `planned` — Require recent trade flow alignment with price direction for actionable signals, filtering one-sided whale clusters.
- [ ] **TB-095** `planned` — Raise min_price_move to 0.01 (1%) to exclude zero or negligible price change spikes.
- [ ] **TB-096** `planned` — Lower whale-cluster p-value threshold to p<0.001 and require directional consensus >80% to reduce algorithmic noise.

---

## 2026-04-12 — Advisor snapshot 32

### Summary
High false positives in whale-cluster signals on low-volume 15m crypto markets, especially with no price movement despite volume spikes and lacking trade flow confirmation.

### Next step
Require minimum absolute volume threshold ≥1000 and price move ≥0.01, plus flow confirmation aligning with price direction.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-097** `planned` — Require volume delta ≥25% of 1h baseline or absolute volume ≥5000 shares.
- [ ] **TB-098** `planned` — Lower whale-cluster p-value threshold to p<0.001 and require directional consensus >80%.
- [ ] **TB-099** `planned` — Filter signals without confirming trade flow in price direction.

---

## 2026-04-12 — Advisor snapshot 33

### Summary
Whale-cluster signals on low-volume 15m KXBTC markets trigger frequently with high scores but low price moves (often 0%), leading to many false positives labeled as signal/no or noise, especially when volume deltas are modest (400-800) and yes probabilities below 0.8.

### Next step
Require minimum absolute volume threshold (e.g., ≥2000 shares) or volume delta ≥25% of 1h baseline to filter micro-spikes in thin markets.

### Suggested thresholds
`min_volume_delta` → `600.0`, `min_price_move` → `0.005`, `score_threshold` → `9.0`

### Recommendations

- [ ] **TB-100** `planned` — Require flow confirmation: flag spikes only when recent trade flow aligns with price direction.
- [ ] **TB-101** `planned` — Raise spike_score_threshold to 9.0 to filter low-yes-probability signals (<0.8).
- [ ] **TB-102** `planned` — Require minimum price move of 0.005 (0.5%) or whitelist markets with 24h volume >50k shares.

---

## 2026-04-12 — Advisor snapshot 34

### Summary
False positives dominate in low-price-move whale-cluster signals on thin 15m markets, particularly with zero or minimal priceΔ (<0.01), low yes probabilities (<0.75), and volume deltas under 1000, despite high scores; analysts flag noise from micro-structure, illiquidity, and lack of flow confirmation.

### Next step
Require minimum price move >0.005 and volume delta ≥500 to filter micro-spikes without muting high-confidence flow.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-103** `planned` — Raise min_volume_delta to 500 to exclude sub-baseline events in thin markets
- [ ] **TB-104** `planned` — Set min_price_move to 0.005 to confirm directional impact beyond noise
- [ ] **TB-105** `planned` — Require yes≥0.75 or flow alignment (post-spike trade direction matching whale bias) for emission

---

## 2026-04-12 — Advisor snapshot 35

### Summary
High-score whale-cluster signals on thin 15m markets generate frequent false positives, especially with low price moves (priceΔ ≤0.001), no directional price change, or insufficient volume deltas relative to baseline, despite high 'yes' probabilities.

### Next step
Require minimum price move confirmation and relative volume threshold to filter micro-spikes lacking directional flow.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-106** `planned` — Increase min_price_move to 0.005 to eliminate signals with negligible price change.
- [ ] **TB-107** `planned` — Raise min_volume_delta to 1000.0 to filter sub-baseline whale clusters.
- [ ] **TB-108** `planned` — Add flow confirmation rule: flag only if recent trade flow aligns with whale direction.

---

## 2026-04-12 — Advisor snapshot 36

### Summary
Your detector is generating high-confidence signals (score=8.0, yes≥0.95) that analysts frequently reject as false positives, particularly when volume spikes occur without corresponding price movement. The pattern suggests whale-cluster activity is being flagged as predictive when it often represents noise or one-sided positioning that fails to move the market.

### Next step
Implement flow-confirmation filtering: require that volume spikes be accompanied by minimum price movement (0.3–0.5%) or validated by subsequent opposing-tier flow direction to distinguish genuine information from positioning noise. This directly addresses the analyst note on lines 14–15 about filtering one-sided whale clusters followed by opposing flow.

### Suggested thresholds
`min_volume_delta` → `25.0`, `min_price_move` → `0.004`

### Recommendations

- [ ] **TB-109** `planned` — Raise spike_min_price_move from 0.0 to 0.003–0.005 (0.3–0.5%) when tier=whale-cluster and score=8.0. Analyst data shows 7 rejections with priceΔ=0.0 and high yes-scores; requiring price confirmation would eliminate these without cutting true signals (which correlate volume+price).
- [ ] **TB-110** `planned` — Add volume-baseline normalization: require spike_min_volume_delta ≥25% of the 1-hour rolling baseline or absolute volume ≥5,000 units per event window, per analyst note on line 20. This filters sub-baseline micro-spikes in thin 15m markets that lack real market impact.
- [ ] **TB-111** `planned` — Introduce a flow-tier cross-check: flag signals as actionable only when whale-cluster volume is followed (within 1–3 bars) by aligned smart-money or retail flow direction, or when price movement persists. This directly implements the reflexivity insight—large positions can move prices, but lack of follow-through flow suggests the signal lacks conviction.

---

## 2026-04-12 — Advisor snapshot 37

### Summary
False positives occur in low-volume whale clusters with minimal price moves (priceΔ ≤0.001) and absolute volΔ as low as 239-400, especially in low-liquidity 15m markets; even some higher volΔ signals lack confirming price impact or flow alignment.

### Next step
Switch min_volume_delta to relative threshold (e.g., spike vol >5% of 1h baseline) and require min_price_move >0.002 with flow confirmation.

### Suggested thresholds
`min_volume_delta` → `800.0`, `min_price_move` → `0.002`

### Recommendations

- [ ] **TB-112** `planned` — Increase min_price_move from 0.001+ to 0.002+ to filter tiny/no price impact spikes.
- [ ] **TB-113** `planned` — Require volΔ >1000 absolute or >5% of recent 1h baseline volume.
- [ ] **TB-114** `planned` — Add flow confirmation: require trade flow direction to align with price move post-spike.

---

## 2026-04-12 — Advisor snapshot 38

### Summary
False positives in whale-cluster signals on 15-min BTC markets are driven by low volume deltas (often <500) and zero or minimal price moves (≤0.001), especially mechanical liquidity provision near 99%+ prices; genuine signals typically have higher volumes and some price impact.

### Next step
For 15-min BTC markets, raise whale-cluster threshold to 60 whales in 120s and require volΔ >5% of 1h baseline or min priceΔ=0.002.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.002`

### Recommendations

- [ ] **TB-115** `planned` — Raise min_volume_delta to 500 for 15-min markets to filter low-volume noise.
- [ ] **TB-116** `planned` — Require minimum priceΔ=0.002 to ensure impact beyond mechanical quotes.
- [ ] **TB-117** `planned` — Dynamically set volΔ threshold to 5% of 1h baseline volume.

---

## 2026-04-12 — Advisor snapshot 39

### Summary
Whale-cluster signals on 15-minute BTC markets produce many false positives labeled as noise/high or noise/no, often due to small whale counts, mechanical liquidity provision near 99%+ prices, low liquidity, and lack of volume or price movement alignment, despite high scores.

### Next step
For 15-minute BTC markets, raise whale-cluster threshold to 30+ whales in 120s AND require volume delta to exceed 5% of 1h rolling baseline.

### Suggested thresholds
`min_price_move` → `0.003`

### Recommendations

- [ ] **TB-118** `planned` — Raise whale-cluster threshold to 60 whales in 120s for ultra-short-dated BTC markets to filter mechanical liquidity and small coordinated buys.
- [ ] **TB-119** `planned` — Require minimum volume delta as 5% of 1h baseline (instead of absolute count) to reduce false positives in low-liquidity periods.
- [ ] **TB-120** `planned` — Add min_price_move requirement of 0.003 for whale-cluster tier to ensure signals align with actual price impact.

---

## 2026-04-12 — Advisor snapshot 40

### Summary
Excessive false positives in whale-cluster signals for 15-minute BTC markets, where statistical clustering triggers alerts without meaningful volume impact or price movement, despite high yes probabilities (>0.98).

### Next step
Require minimum volume delta of 5-10% relative to baseline for whale-cluster tier in ultra-short-duration markets.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-121** `planned` — Raise whale-cluster threshold to 20-30 whales in 120s for 15-min BTC markets.
- [ ] **TB-122** `planned` — Filter whale-cluster alerts with priceΔ < 0.01 and volΔ < 5% baseline.
- [ ] **TB-123** `planned` — Increase spike_min_volume_delta to 500+ for high-frequency low-liquidity markets.

---

## 2026-04-12 — Advisor snapshot 41

### Summary
Whale-cluster signals in 15-min BTC prediction markets near 99%+ prices generate frequent false positives due to routine pinning noise, statistical clustering in thin/low-liquidity markets, and low volume deltas relative to baseline without sustained price impact or predictive flow.

### Next step
Require volume delta ≥5% of baseline volume for whale-cluster signals in 15-min BTC markets, and raise whale-cluster threshold to 20-25+ whales in 120s.

### Suggested thresholds
`min_volume_delta` → `400.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-124** `planned` — Require volume delta ≥5% of baseline before flagging whale-cluster signals to filter economically insignificant activity.
- [ ] **TB-125** `planned` — Raise whale-cluster threshold to 20+ whales in 120s for high-frequency 15-min BTC markets to exclude routine pinning.
- [ ] **TB-126** `planned` — Filter whale-cluster alerts where price move <0.01 (1%) and yes probability >0.995 unless volume delta ≥10% of baseline.

---

## 2026-04-12 — Advisor snapshot 42

### Summary
Whale-cluster signals in low-liquidity 15-min BTC prediction markets trigger frequent false positives with low volume deltas (<500) and minimal/no price moves, often labeled as noise/unclear/low despite high scores and yes probabilities near 0.999, due to microstructure events like pinning without predictive impact.

### Next step
Raise whale-cluster min volume delta to 5-10% of 1h baseline and require min price move >0.003 or sustained flow.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-127** `planned` — Set spike_min_volume_delta to 500 absolute or 5% of 1h baseline to filter low-impact clusters.
- [ ] **TB-128** `planned` — Increase spike_min_price_move to 0.005 to exclude no-response events.
- [ ] **TB-129** `planned` — For whale-cluster tier, require 20+ whales in 120s and volume delta >=10% baseline.

---

## 2026-04-12 — Advisor snapshot 43

### Summary
Whale-cluster signals in 15-min BTC markets generate frequent false positives due to low volume deltas (<1000) and minimal/no price moves (often 0-0.003) in thin, high-probability (>0.99) markets, despite consistent 8.0 scores; genuine signals show higher volume and price response.

### Next step
Require volume delta >=5% of 1h baseline AND price move >=0.005 for whale-cluster in 15-min BTC markets.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-130** `planned` — Raise min_volume_delta to 1000 for whale-cluster tier in low-liquidity 15-min markets
- [ ] **TB-131** `planned` — Increase min_price_move to 0.005 to filter microstructure noise without price impact
- [ ] **TB-132** `planned` — Tier-specific: whale-cluster requires 20+ whales in 120s for BTC 15m contracts

---

## 2026-04-12 — Advisor snapshot 44

### Summary
False positives dominate in short-duration crypto markets like 15M BTC contracts, particularly from whale-cluster detections with low volume deltas relative to baseline and no price response, alongside volume spikes from unexecuted orders.

### Next step
Require volume delta to exceed 5% of 1h baseline AND minimum price move of 0.01 for all signals in 15M BTC markets.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-133** `planned` — Raise whale-cluster min volume delta to 5-10% of 1h baseline to filter microstructure noise.
- [ ] **TB-134** `planned` — For volume spikes, enforce executed trade volume / quote volume ratio > 0.5 or sustained price move > 1%.
- [ ] **TB-135** `planned` — Increase whale-cluster threshold to 25+ whales in 120s for 15M BTC near 99%+ prices.

---

## 2026-04-12 — Advisor snapshot 45

### Summary
False positives dominate in high-volume markets like sports and short-duration crypto (e.g., 15-min BTC), where tiny trades, unexecuted orders, and low-liquidity microstructure events trigger alerts without price response or sustained flow, despite high scores near extreme prices (0.99+ yes).

### Next step
Require volume delta >5% of baseline volume across all tiers and markets to filter microstructure noise while preserving high-volume genuine signals.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-136** `planned` — Raise min_volume_delta to 5-10% of 1h baseline for crypto and whale-cluster detections.
- [ ] **TB-137** `planned` — Require priceΔ >=0.005 (0.5%) or sustained unidirectional flow over 3min for watch/notable tiers.
- [ ] **TB-138** `planned` — For whale-cluster, increase threshold to 25+ whales in 120s and volΔ >5% baseline.

---

## 2026-04-12 — Advisor snapshot 46

### Summary
False positives dominate in high-volume markets like sports and short-duration crypto, and low-liquidity whale-clusters near extreme prices (e.g., 99%+ yes), where volume spikes lack sustained price response or predictive value.

### Next step
Require volume delta >0.5x baseline volume and pair with minimum price move or whale count thresholds tailored to market type.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-139** `planned` — Raise min_volume_delta to >0.5x baseline for high-volume markets (e.g., sports) to filter tiny trades.
- [ ] **TB-140** `planned` — For 15-min BTC markets, require volΔ >1% of 1h baseline or whale-clusters >25 in 120s near 99%+ prices.
- [ ] **TB-141** `planned` — Add rule: sustained priceΔ >=0.01 alongside vol spikes for short-duration crypto to exclude order noise.

---

## 2026-04-12 — Advisor snapshot 47

### Summary
False positives dominate in high-volume markets like sports and short-duration crypto, as well as low-liquidity whale-clusters near extreme prices, where volume spikes lack sustained price response or predictive value.

### Next step
Require volume delta >0.5x baseline volume and minimum price move >0.01 alongside current thresholds to filter microstructure noise across market types.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-142** `planned` — Raise min_volume_delta to 0.5x baseline for high-volume markets (e.g., sports) to exclude tiny trades.
- [ ] **TB-143** `planned` — For 15-min crypto markets, require volΔ >1% of 1h baseline or priceΔ >0.01 for whale-cluster signals.
- [ ] **TB-144** `planned` — Increase whale-cluster threshold to 25+ whales in 120s at yes prices >0.99.

---

## 2026-04-12 — Advisor snapshot 48

### Summary
False positives dominate in high-volume markets like sports and short-duration crypto, and low-liquidity whale-clusters without price response, due to insufficient relative volume scaling, missing price confirmation, and fixed absolute thresholds.

### Next step
Scale volume delta thresholds relative to market baseline (e.g., >0.5x 1h baseline) and require minimum price move or volume-to-quote ratio for all signals.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-145** `planned` — Raise volume delta to >0.5x baseline volume for high-volume markets like sports to filter tiny trades.
- [ ] **TB-146** `planned` — Require sustained price move >0.01 or executed volume >20% of quote volume for crypto 15m markets.
- [ ] **TB-147** `planned` — Increase whale-cluster min volume delta to 5-10% of 1h baseline and threshold to 25+ whales in 120s near 99%+ prices.

---

## 2026-04-12 — Advisor snapshot 49

### Summary
False positives occur in high-volume markets like sports and short-duration crypto due to volume spikes without meaningful price movement, and in low-liquidity whale-clusters lacking sustained volume relative to baseline.

### Next step
Require volume delta >0.5x baseline volume and pair with minimum price movement or executed-to-quote volume ratio.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-148** `planned` — Raise min_volume_delta to >0.5x baseline for high-volume markets (e.g., sports) to filter tiny trades.
- [ ] **TB-149** `planned` — For crypto short-duration markets, require sustained priceΔ or executed volume / quote volume > threshold.
- [ ] **TB-150** `planned` — Increase whale-cluster min_volume_delta to 5-10% of 1h baseline to avoid microstructure noise.

---

## 2026-04-12 — Advisor snapshot 50

### Summary
False positives dominate in high-volume markets like sports and short-duration crypto, where volume spikes from tiny trades or unexecuted orders occur without meaningful price movement; low-liquidity microstructure events also trigger noise.

### Next step
Require volume delta >0.5x baseline volume and pair with minimum price movement to filter noise in high-volume/illiquid contexts.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-151** `planned` — Raise volume delta threshold relative to baseline (e.g., >0.5x) for high-volume markets like sports to filter tiny trades.
- [ ] **TB-152** `planned` — For short-duration crypto, require sustained price move or executed trade volume / quote volume ratio alongside volume spikes.
- [ ] **TB-153** `planned` — Increase whale-cluster min volume delta to 5-10% of 1h baseline for low-liquidity events without price response.

---

## 2026-04-12 — Advisor snapshot 51

### Summary
False positives occur in high-volume markets like sports and short-duration crypto from isolated volume spikes without sustained price movement or relative to baseline activity.

### Next step
Require volume delta >0.5x baseline volume and pair with minimum price move for all markets.

### Suggested thresholds
`min_price_move` → `0.015`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-154** `planned` — Raise volume delta threshold relative to baseline (e.g., >0.5x) for high-volume markets like sports to filter tiny trades.
- [ ] **TB-155** `planned` — For short-duration crypto, require sustained price movement (>=0.01) alongside volume spikes or executed trade volume ratio.
- [ ] **TB-156** `planned` — Increase score_threshold to 5.0 to filter low-price-move signals regardless of volume.

---

## 2026-04-12 — Advisor snapshot 52

### Summary
False positives arise from volume spikes driven by tiny trades in high-volume markets like sports events and unexecuted order noise in short-duration crypto markets, despite insufficient price movement.

### Next step
Introduce market-type-specific volume delta thresholds relative to baseline volume (e.g., >0.5x baseline) and require minimum executed trade volume to quote volume ratio.

### Suggested thresholds
`min_price_move` → `0.01`, `score_threshold` → `2.0`

### Recommendations

- [ ] **TB-157** `planned` — Raise volume delta threshold to >0.5x baseline volume for high-volume markets like sports to filter tiny trades.
- [ ] **TB-158** `planned` — For short-duration crypto markets, require sustained price movement (>0.01) with volume spikes or minimum executed/quote volume ratio.
- [ ] **TB-159** `planned` — Increase spike_score_threshold to 2.0 to suppress low-score signals with weak price delta.

---

## 2026-04-12 — Advisor snapshot 53

### Summary
False positives are driven by mechanical quotes, HFT noise, and tiny trades in low-liquidity long-dated markets, short-duration crypto, and high-volume sports events, where volume spikes occur without meaningful or sustained price moves.

### Next step
Introduce market-type specific volume multipliers relative to baseline (e.g., 2.5x for low-liquidity speech, 15x for BTC 15m) and require sustained price moves >5% over 5m or >0.5% with minimum executed trade ratio.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-160** `planned` — Raise volume delta multiplier to 2.5x baseline for low-liquidity, long-dated markets and require >5% price move sustained over 5m.
- [ ] **TB-161** `planned` — Set volume multiplier to 15x baseline for 15-min BTC markets and require >0.5% price move for watch tier.
- [ ] **TB-162** `planned` — Require volume delta >0.5x baseline in high-volume markets like sports and add minimum executed trade volume to quote volume ratio.

---

## 2026-04-12 — Advisor snapshot 54

### Summary
False positives dominate in low-liquidity long-dated markets, short-duration crypto/HFT, and high-volume sports events due to mechanical quotes, unexecuted orders, and tiny trades triggering without sustained informative moves.

### Next step
Introduce market-specific volume multipliers relative to baseline liquidity and require sustained price moves (>5% over 5m for low-liq, >0.5% for crypto) to filter mechanical noise.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-163** `planned` — Raise volume delta multiplier to 2.5x baseline and price move >5% sustained over 5m for low-liquidity, long-dated speech markets.
- [ ] **TB-164** `planned` — Set volume multiplier to 15x baseline and price move >0.5% for 15-min BTC/crypto watch tier to block HFT noise.
- [ ] **TB-165** `planned` — Require volume delta >0.5x baseline for high-volume markets like sports to ignore tiny trades.

---

## 2026-04-12 — Advisor snapshot 55

### Summary
False positives dominate in short-duration BTC markets and low-liquidity events due to mechanical HFT noise, balanced order flow, and unexecuted quotes without sustained directional movement; one notable signal shows value in political markets with larger price moves.

### Next step
Require net directional flow >50% of volume and sustained price move >3% over 5 minutes for all markets to filter mechanical activity.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-166** `planned` — Raise volume multiplier to 5x baseline for 15m BTC markets
- [ ] **TB-167** `planned` — Require price move >5% sustained over 5m for low-liquidity speech markets
- [ ] **TB-168** `planned` — Add minimum executed trade volume to quote volume ratio >0.5 for short-duration crypto

---

## 2026-04-12 — Advisor snapshot 56

### Summary
False positives dominate in high-frequency BTC markets and low-liquidity events due to mechanical HFT noise, balanced trades, and tiny volumes without sustained directional price moves, while notable signals like TRUMPSAY show genuine spikes.

### Next step
Introduce market-specific volume multipliers (e.g., 5-15x baseline for BTC 15m) and require net directional flow >50% of volume alongside sustained price moves.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-169** `planned` — Raise volume multiplier to 5x baseline for 15m BTC markets and require net flow >50%
- [ ] **TB-170** `planned` — Require price move >5% sustained over 5m for low-liquidity speech/event markets
- [ ] **TB-171** `planned` — Set relative volume delta >0.5x baseline for high-volume markets like sports to filter tiny trades

---

## 2026-04-12 — Advisor snapshot 57

### Summary
False positives dominate in high-volume BTC 15-minute markets from balanced mechanical/HFT activity despite minimal price moves, while low-liquidity speech markets trigger on large mechanical quotes without sustained direction.

### Next step
Introduce market-type rules: for BTC 15m, require volume >5x baseline AND net directional flow >50% AND price move >0.5%; for low-liquidity speech, require price move >5% sustained over 5m.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-172** `planned` — Raise BTC 15m volume multiplier to 5-15x baseline based on tier
- [ ] **TB-173** `planned` — Require net directional flow >50% of volume to filter balanced activity
- [ ] **TB-174** `planned` — Mandate sustained price move >0.5-5% over 5m for watch tier, tiered by liquidity

---

## 2026-04-12 — Advisor snapshot 58

### Summary
False positives dominate in 15-minute BTC markets and low-liquidity speech markets due to high volume spikes from mechanical HFT or balanced activity with minimal price moves (0.01-0.03), while the single notable signal had stronger price movement (6%).

### Next step
Require minimum 2% price move for watch tier in high-frequency crypto markets and low-liquidity events to filter mechanical noise.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-175** `planned` — Raise volume multiplier to 6x baseline for 15m BTC markets
- [ ] **TB-176** `planned` — Require net directional flow >50% of volume for watch tier signals
- [ ] **TB-177** `planned` — Set price move >5% sustained over 5m for low-liquidity long-dated markets

---

## 2026-04-12 — Advisor snapshot 59

### Summary
Your detector is generating false positives on low-liquidity and short-timeframe markets by triggering on mechanical volume activity and minor price movements that lack directional conviction. The pattern shows multiple noise signals with high volume deltas but minimal price moves (0.01-0.03) and low analyst confidence scores.

### Next step
Implement market-specific dynamic thresholds that adjust based on liquidity profile and typical spreads, rather than applying uniform thresholds across crypto spot (KXBTC) and prediction markets (KXTRUMPSAY). Require either sustained directional price moves OR significant volume concentration, not volume alone.

### Suggested thresholds
`min_volume_delta` → `5.5`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-178** `planned` — For 15-minute crypto markets (KXBTC): Raise spike_min_volume_delta from baseline 4x to 5-6x multiplier, OR require spike_min_price_move >= 2% (from current 1%) to qualify for watch tier
- [ ] **TB-179** `planned` — For low-liquidity, long-dated prediction markets (KXTRUMPSAY): Implement dual-gate requirement—volume delta must exceed 2.5x baseline AND price move must sustain >= 5% over 5-minute window to filter mechanical quotes
- [ ] **TB-180** `planned` — Add directional flow filter for 15-minute markets: require net directional volume concentration > 50% of total volume delta to distinguish genuine flow from balanced mechanical activity

---

## 2026-04-12 — Advisor snapshot 60

### Summary
Your detector is triggering on low-confidence noise in crypto markets with minimal price moves (1%) but elevated volume deltas, while missing genuine signals in event-driven markets. The watch-tier signals on KXBTC show conflicting weak conviction (yes=0.35-0.42) despite moderate scores, indicating threshold misalignment.

### Next step
Implement asymmetric thresholds by market type: require 2% minimum price move for crypto 15M markets, and raise volume-delta multiplier to 5-6x baseline to filter mechanical activity. For event markets like KXTRUMPSAY, lower price-move requirements but require directional conviction (yes probability >0.15) to surface genuine signal.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-181** `planned` — Increase spike_min_price_move from 1% to 2% for 15-minute cryptocurrency markets (KXBTC style) to filter low-conviction moves
- [ ] **TB-182** `planned` — Raise spike_min_volume_delta multiplier to 5x baseline for crypto, or add net directional flow >50% requirement to distinguish informed flow from balanced mechanical activity
- [ ] **TB-183** `planned` — For event-driven markets (KXTRUMPSAY), create a separate rule that accepts lower price moves (0.05-0.06) when analyst conviction (yes probability) exceeds 0.15, rather than applying uniform thresholds

---

## 2026-04-12 — Advisor snapshot 61

### Summary
Recent signals show false positives driven by isolated short-term volume spikes and small price moves in golf prop and 15m crypto markets, often due to quote noise or balanced mechanical activity, while one Trump-related signal appears genuine.

### Next step
Require sustained price move over 5 minutes and net directional flow >50% of volume to filter transient noise across markets.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-184** `planned` — For golf prop markets, raise price move persistence threshold to require sustained change over 5m+ instead of 1m spikes.
- [ ] **TB-185** `planned` — For 15m crypto markets, increase volume delta multiplier from 4x to 6x baseline and require min 2% price move.
- [ ] **TB-186** `planned` — Add net directional flow >50% of volume requirement for watch-tier signals in high-spread markets.

---

## 2026-04-12 — Advisor snapshot 62

### Summary
Recent false positives stem from isolated 1m price spikes and quote-driven noise in golf props, plus low price moves with high volume but balanced activity in 15m crypto markets.

### Next step
Require sustained price move over 5m and net directional flow >50% of volume to filter noise.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-187** `planned` — Raise price move persistence threshold to require sustained change over 5m+ for golf prop markets
- [ ] **TB-188** `planned` — Increase volume delta multiplier to 6x baseline and min price move to 0.02 for 15m crypto markets
- [ ] **TB-189** `planned` — Require net directional flow >50% of volume for watch tier signals in BTC markets

---

## 2026-04-12 — Advisor snapshot 63

### Summary
False positives stem from isolated short-term spikes and quote-driven noise in niche markets like golf props and crypto, where low price persistence and insufficient volume multipliers trigger alerts despite unclear informational value.

### Next step
Require price move persistence over 5+ minutes and market-specific dynamic volume thresholds to filter transient noise.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-190** `planned` — For golf prop markets, enforce sustained price change over 5m+ instead of 1m isolated spikes.
- [ ] **TB-191** `planned` — For 15m crypto markets, raise volume delta to 6x baseline or min 2% price move given wide spreads.
- [ ] **TB-192** `planned` — Implement dynamic thresholds using recent baselines like EWMA for volume and volatility-adjusted price.

---

## 2026-04-12 — Advisor snapshot 64

### Summary
False positives in low-volume crypto and niche prop markets stem from small-lot accumulation, isolated 1m spikes, and insufficient price persistence despite low price moves.

### Next step
Add market-specific filters: minimum notional USD volume and sustained price move over 5m for low-liquidity or prop markets.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-193** `planned` — For 15m crypto markets, add minimum notional trade size filter (e.g., $10k USD equivalent) to ignore small-lot noise.
- [ ] **TB-194** `planned` — Raise price move persistence to require 5m+ sustained change instead of 1m spikes, especially for golf props.
- [ ] **TB-195** `planned` — Increase min price move to 0.02 for watch tier in wide-spread crypto markets and volume delta multiplier to 6x baseline.

---

## 2026-04-12 — Advisor snapshot 65

### Summary
False positives arise from low-conviction signals in thin markets like low-volume crypto and quote-driven props, where isolated volume spikes or small price moves lack persistence or notional size.

### Next step
Add market-specific filters: minimum notional USD volume and price move persistence over 5m.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-196** `planned` — For 15m crypto markets, add minimum notional trade size filter (e.g., USD equivalent > $10k) to filter small-lot accumulation.
- [ ] **TB-197** `planned` — For golf prop markets, require price move persistence over 5m+ instead of isolated 1m spikes.
- [ ] **TB-198** `planned` — Incorporate dynamic baselines using EWMA for volume/price to normalize low-liquidity assets.

---

## 2026-04-12 — Advisor snapshot 66

### Summary
Your detector is generating false positives in low-liquidity markets (15m crypto, prop markets) where volume spikes lack corresponding price conviction, and isolated quote-driven noise is being treated as meaningful flow.

### Next step
Implement a price-move persistence requirement: signals must show sustained price deviation over multiple candles (5+ ticks) rather than isolated 1-minute spikes, reducing noise while preserving genuine informative flow.

### Suggested thresholds
`min_volume_delta` → `300000.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-199** `rejected` — Add a minimum notional trade size filter (USD equivalent) for crypto 15m markets to eliminate false positives from small-lot accumulation that lacks institutional conviction.
  - **Governor rejection**: TB-001 applied raised whale-cluster volume delta threshold to 1000 for 15m BTC, but the proposed tweak sets min_volume_delta to 300000.0, which relaxes the previously tightened threshold and risks reintroducing the noise that TB-001 was implemented to fix.
- [ ] **TB-200** `rejected` — Increase the volume-to-price-move ratio threshold; require that high volume deltas are accompanied by proportional price moves (e.g., volΔ > 200k USD should correlate with priceΔ ≥ 0.02).
  - **Governor rejection**: TB-001 applied raised whale-cluster volume delta threshold to 1000 for 15m BTC, but the proposed tweak sets min_volume_delta to 300000.0, which relaxes the previously tightened threshold and risks reintroducing the noise that TB-001 was implemented to fix.
- [ ] **TB-201** `rejected` — For lower-liquidity asset classes (props, alts), enforce 5-minute price persistence: the detected price move must hold or expand over the next 5 candles, filtering out transient quote-driven noise.
  - **Governor rejection**: TB-001 applied raised whale-cluster volume delta threshold to 1000 for 15m BTC, but the proposed tweak sets min_volume_delta to 300000.0, which relaxes the previously tightened threshold and risks reintroducing the noise that TB-001 was implemented to fix.

---

## 2026-04-12 — Advisor snapshot 67

### Summary
False positives dominate in low-liquidity, high-frequency crypto markets (e.g., BTC 15m) and niche props (e.g., golf), where high volume with minimal or transient price moves triggers signals lacking conviction or persistence.

### Next step
Add a price move persistence filter requiring sustained deviation over 5 ticks or 5m, plus a minimum notional volume threshold (e.g., USD equivalent) for low-liquidity markets.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-202** `rejected` — Raise volume-to-price-move ratio threshold to filter high-volume/low-price-change noise in BTC 15m markets.
  - **Governor rejection**: The proposed tweak directly violates TB-199 (rejected: no minimum notional trade size filter for crypto 15m markets) and TB-200 (rejected: no volume-to-price-move ratio threshold). The recommendation to add a 'minimum notional volume threshold for low-liquidity markets' reintroduces the exact constraint that TB-199 explicitly rejected. Additionally, the price move persistence filter (sustained deviation over 5 ticks or 5m) mirrors TB-201 (rejected: no 5-minute price persistence for lower-liquidity assets), which was previously determined to be an unsuitable approach. These constraints were rejected through prior governance decisions and should not be reintroduced without documented evidence that the original rejection rationale no longer applies.
- [ ] **TB-203** `rejected` — Require minimum sustained price deviation over 5 ticks or 5m for all notable-tier signals.
  - **Governor rejection**: The proposed tweak directly violates TB-199 (rejected: no minimum notional trade size filter for crypto 15m markets) and TB-200 (rejected: no volume-to-price-move ratio threshold). The recommendation to add a 'minimum notional volume threshold for low-liquidity markets' reintroduces the exact constraint that TB-199 explicitly rejected. Additionally, the price move persistence filter (sustained deviation over 5 ticks or 5m) mirrors TB-201 (rejected: no 5-minute price persistence for lower-liquidity assets), which was previously determined to be an unsuitable approach. These constraints were rejected through prior governance decisions and should not be reintroduced without documented evidence that the original rejection rationale no longer applies.
- [ ] **TB-204** `rejected` — Add minimum notional trade size filter (USD equivalent) for crypto markets with low absolute volumes.
  - **Governor rejection**: The proposed tweak directly violates TB-199 (rejected: no minimum notional trade size filter for crypto 15m markets) and TB-200 (rejected: no volume-to-price-move ratio threshold). The recommendation to add a 'minimum notional volume threshold for low-liquidity markets' reintroduces the exact constraint that TB-199 explicitly rejected. Additionally, the price move persistence filter (sustained deviation over 5 ticks or 5m) mirrors TB-201 (rejected: no 5-minute price persistence for lower-liquidity assets), which was previously determined to be an unsuitable approach. These constraints were rejected through prior governance decisions and should not be reintroduced without documented evidence that the original rejection rationale no longer applies.

---

## 2026-04-12 — Advisor snapshot 68

### Summary
False positives are driven by high-volume low-price-move spikes in low-liquidity, high-frequency BTC 15m markets, where small-lot accumulation lacks conviction despite large volΔ.

### Next step
Introduce a volume-to-price-move ratio threshold (e.g., volΔ / priceΔ > 10000 triggers review) to filter noise in thin markets.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-205** `rejected` — Require minimum sustained price deviation over 5 ticks for notable tier signals.
  - **Governor rejection**: The proposed tweak introduces a volume-to-price-move ratio threshold, which directly conflicts with TB-200 rejected (no volume-to-price-move ratio threshold) and TB-202 rejected (no raised volume-to-price-move ratio threshold for BTC 15m high-volume/low-price-change noise). These rejections explicitly block such filters to avoid restricting spike detection in those scenarios.
- [ ] **TB-206** `rejected` — Add minimum notional trade size filter (e.g., USD 10k equivalent) for low-volume crypto markets.
  - **Governor rejection**: The proposed tweak introduces a volume-to-price-move ratio threshold, which directly conflicts with TB-200 rejected (no volume-to-price-move ratio threshold) and TB-202 rejected (no raised volume-to-price-move ratio threshold for BTC 15m high-volume/low-price-change noise). These rejections explicitly block such filters to avoid restricting spike detection in those scenarios.
- [ ] **TB-207** `rejected` — Raise score_threshold for BTC 15m markets to prioritize conviction over raw volume.
  - **Governor rejection**: The proposed tweak introduces a volume-to-price-move ratio threshold, which directly conflicts with TB-200 rejected (no volume-to-price-move ratio threshold) and TB-202 rejected (no raised volume-to-price-move ratio threshold for BTC 15m high-volume/low-price-change noise). These rejections explicitly block such filters to avoid restricting spike detection in those scenarios.

---

## 2026-04-12 — Advisor snapshot 69

### Summary
False positives occur in low-liquidity, high-frequency markets like BTC 15m where high volume deltas with minimal price moves (e.g., 1%) generate signals labeled as noise/unclear, while notable-tier markets with extreme price moves (81%) are valid medium signals.

### Next step
Introduce a volume-to-price-move ratio threshold or require minimum sustained price deviation over 5 ticks to filter noise in low-liquidity high-frequency markets.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-208** `rejected` — Raise volume-to-price-move ratio threshold (e.g., require volΔ/priceΔ > 1000 for low-liquidity markets)
  - **Governor rejection**: The proposed tweak introduces a volume-to-price-move ratio threshold or minimum sustained price deviation over 5 ticks, which directly conflicts with multiple rejected historical constraints: TB-200 rejected 'no volume-to-price-move ratio threshold (e.g., volΔ >200k USD w/ priceΔ ≥0.02)', TB-201 rejected 'no 5-minute price persistence for lower-liquidity assets', TB-202 rejected 'no raised volume-to-price-move ratio threshold for BTC 15m high-vol/low-price noise', TB-203 rejected 'no minimum sustained price deviation over 5 ticks/5m for notable-tier signals', and TB-205 rejected 'no minimum sustained price deviation over 5 ticks for notable-tier signals'. These rejections explicitly block adding such price-related filters to address noise in low-liquidity or BTC 15m contexts.
- [ ] **TB-209** `rejected` — Require minimum sustained price deviation over 5 ticks
  - **Governor rejection**: The proposed tweak introduces a volume-to-price-move ratio threshold or minimum sustained price deviation over 5 ticks, which directly conflicts with multiple rejected historical constraints: TB-200 rejected 'no volume-to-price-move ratio threshold (e.g., volΔ >200k USD w/ priceΔ ≥0.02)', TB-201 rejected 'no 5-minute price persistence for lower-liquidity assets', TB-202 rejected 'no raised volume-to-price-move ratio threshold for BTC 15m high-vol/low-price noise', TB-203 rejected 'no minimum sustained price deviation over 5 ticks/5m for notable-tier signals', and TB-205 rejected 'no minimum sustained price deviation over 5 ticks for notable-tier signals'. These rejections explicitly block adding such price-related filters to address noise in low-liquidity or BTC 15m contexts.
- [ ] **TB-210** `rejected` — Increase spike_min_price_move to 0.03 for high-frequency markets like BTC 15m
  - **Governor rejection**: The proposed tweak introduces a volume-to-price-move ratio threshold or minimum sustained price deviation over 5 ticks, which directly conflicts with multiple rejected historical constraints: TB-200 rejected 'no volume-to-price-move ratio threshold (e.g., volΔ >200k USD w/ priceΔ ≥0.02)', TB-201 rejected 'no 5-minute price persistence for lower-liquidity assets', TB-202 rejected 'no raised volume-to-price-move ratio threshold for BTC 15m high-vol/low-price noise', TB-203 rejected 'no minimum sustained price deviation over 5 ticks/5m for notable-tier signals', and TB-205 rejected 'no minimum sustained price deviation over 5 ticks for notable-tier signals'. These rejections explicitly block adding such price-related filters to address noise in low-liquidity or BTC 15m contexts.

---

## 2026-04-12 — Advisor snapshot 70

### Summary
False positives occur in low-liquidity, high-frequency markets like BTC 15m from large volume spikes (e.g., 191k and 55k deltas) with minimal price moves (1%), likely due to large quote placements not leading to sustained directional trades.

### Next step
Introduce a minimum volume-to-price-move ratio threshold (e.g., require volΔ / priceΔ > 10000) to filter noise from disproportionate volume without price confirmation.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-211** `rejected` — Raise volume-to-price-move ratio threshold to reduce false positives from large quote placements.
  - **Governor rejection**: The proposed tweak introduces a minimum volume-to-price-move ratio threshold (volΔ / priceΔ > 10000), which directly conflicts with TB-200 rejected (no volume-to-price-move ratio threshold, e.g., volΔ>200k USD w/ priceΔ≥0.02) and TB-208 rejected (no volΔ/priceΔ ratio threshold, e.g., >1000 for low-liquidity). These explicitly rejected adding such ratio-based filters to avoid overly restrictive criteria, particularly in low-volume or BTC 15m contexts matching the proposal.
- [ ] **TB-212** `rejected` — Require minimum sustained price deviation over 5 ticks for low-liquidity markets.
  - **Governor rejection**: The proposed tweak introduces a minimum volume-to-price-move ratio threshold (volΔ / priceΔ > 10000), which directly conflicts with TB-200 rejected (no volume-to-price-move ratio threshold, e.g., volΔ>200k USD w/ priceΔ≥0.02) and TB-208 rejected (no volΔ/priceΔ ratio threshold, e.g., >1000 for low-liquidity). These explicitly rejected adding such ratio-based filters to avoid overly restrictive criteria, particularly in low-volume or BTC 15m contexts matching the proposal.
- [ ] **TB-213** `rejected` — Increase spike_min_price_move to 0.02 for high-frequency markets like BTC 15m.
  - **Governor rejection**: The proposed tweak introduces a minimum volume-to-price-move ratio threshold (volΔ / priceΔ > 10000), which directly conflicts with TB-200 rejected (no volume-to-price-move ratio threshold, e.g., volΔ>200k USD w/ priceΔ≥0.02) and TB-208 rejected (no volΔ/priceΔ ratio threshold, e.g., >1000 for low-liquidity). These explicitly rejected adding such ratio-based filters to avoid overly restrictive criteria, particularly in low-volume or BTC 15m contexts matching the proposal.

---

## 2026-04-12 — Advisor snapshot 71

### Summary
False positives occur in high-volume, low-price-move scenarios like large quote placements in BTC markets that fail to sustain directionally, while genuine high-conviction signals show both large volume deltas and significant price moves.

### Next step
Introduce a minimum volume-to-price-move ratio threshold (e.g., volΔ / priceΔ > 10000) to filter noise from high-volume, low-impact trades.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-214** `rejected` — Raise the volume-to-price-move ratio threshold to reduce false positives from large quote placements.
  - **Governor rejection**: The proposed tweak introduces a volume-to-price-move ratio threshold (volΔ / priceΔ > 10000), which directly conflicts with multiple historical rejections including TB-200 rejected (no volume-to-price-move ratio threshold e.g., volΔ >200k USD with priceΔ ≥0.02), TB-202 rejected (no raised volume-to-price-move ratio threshold for BTC 15m), TB-208 rejected (no volume-to-price-move ratio threshold e.g., volΔ/priceΔ >1000), and TB-211 rejected (no volume-to-price-move ratio threshold to reduce false positives from large quote placements). These explicitly rejected similar filters to avoid over-filtering genuine signals.
- [ ] **TB-215** `rejected` — Require minimum sustained price deviation over 5 ticks for low-liquidity markets.
  - **Governor rejection**: The proposed tweak introduces a volume-to-price-move ratio threshold (volΔ / priceΔ > 10000), which directly conflicts with multiple historical rejections including TB-200 rejected (no volume-to-price-move ratio threshold e.g., volΔ >200k USD with priceΔ ≥0.02), TB-202 rejected (no raised volume-to-price-move ratio threshold for BTC 15m), TB-208 rejected (no volume-to-price-move ratio threshold e.g., volΔ/priceΔ >1000), and TB-211 rejected (no volume-to-price-move ratio threshold to reduce false positives from large quote placements). These explicitly rejected similar filters to avoid over-filtering genuine signals.
- [ ] **TB-216** `rejected` — Increase spike_min_price_move to 0.05 to ensure material price impact.
  - **Governor rejection**: The proposed tweak introduces a volume-to-price-move ratio threshold (volΔ / priceΔ > 10000), which directly conflicts with multiple historical rejections including TB-200 rejected (no volume-to-price-move ratio threshold e.g., volΔ >200k USD with priceΔ ≥0.02), TB-202 rejected (no raised volume-to-price-move ratio threshold for BTC 15m), TB-208 rejected (no volume-to-price-move ratio threshold e.g., volΔ/priceΔ >1000), and TB-211 rejected (no volume-to-price-move ratio threshold to reduce false positives from large quote placements). These explicitly rejected similar filters to avoid over-filtering genuine signals.

---

## 2026-04-12 — Advisor snapshot 72

### Summary
False positives are prevalent in low-liquidity markets like pre-game sports and high-frequency BTC due to mechanical quote-trades and large volume spikes without sustained price moves, while high-conviction signals in other markets perform well.

### Next step
Introduce a volume-to-price-move ratio threshold (e.g., require priceΔ > 0.02 * volΔ normalization) and baseline-normalized volume delta for low-liquidity markets.

### Suggested thresholds
`min_price_move` → `0.02`, `score_threshold` → `10.0`

### Recommendations

- [ ] **TB-217** `rejected` — Raise min_volume_delta to 1-2% of baseline volume for low-liquidity or pre-game markets.
  - **Governor rejection**: The proposed tweak introduces a volume-to-price-move ratio threshold (e.g., priceΔ > 0.02 * volΔ normalization) and sets min_price_move: 0.02, which directly conflicts with multiple rejected historical constraints: TB-200 rejected (no volume-to-price-move ratio threshold, e.g., volΔ >200k USD with priceΔ ≥0.02), TB-202 rejected (no raised volume-to-price-move ratio threshold for BTC 15m), TB-208 rejected (no volume-to-price-move ratio threshold, e.g., volΔ/priceΔ >1000), TB-210 rejected (no spike_min_price_move increased to 0.03 for BTC 15m), and TB-213 rejected (no spike_min_price_move increased to 0.02 for BTC 15m). These reintroduce explicitly rejected filters for low-liquidity and high-frequency BTC markets.
- [ ] **TB-218** `rejected` — Require minimum price move of 0.02 (2%) or sustained deviation over 5 ticks.
  - **Governor rejection**: The proposed tweak introduces a volume-to-price-move ratio threshold (e.g., priceΔ > 0.02 * volΔ normalization) and sets min_price_move: 0.02, which directly conflicts with multiple rejected historical constraints: TB-200 rejected (no volume-to-price-move ratio threshold, e.g., volΔ >200k USD with priceΔ ≥0.02), TB-202 rejected (no raised volume-to-price-move ratio threshold for BTC 15m), TB-208 rejected (no volume-to-price-move ratio threshold, e.g., volΔ/priceΔ >1000), TB-210 rejected (no spike_min_price_move increased to 0.03 for BTC 15m), and TB-213 rejected (no spike_min_price_move increased to 0.02 for BTC 15m). These reintroduce explicitly rejected filters for low-liquidity and high-frequency BTC markets.
- [ ] **TB-219** `rejected` — Increase score_threshold to 10 for markets with volΔ > 10000 and priceΔ < 0.05.
  - **Governor rejection**: The proposed tweak introduces a volume-to-price-move ratio threshold (e.g., priceΔ > 0.02 * volΔ normalization) and sets min_price_move: 0.02, which directly conflicts with multiple rejected historical constraints: TB-200 rejected (no volume-to-price-move ratio threshold, e.g., volΔ >200k USD with priceΔ ≥0.02), TB-202 rejected (no raised volume-to-price-move ratio threshold for BTC 15m), TB-208 rejected (no volume-to-price-move ratio threshold, e.g., volΔ/priceΔ >1000), TB-210 rejected (no spike_min_price_move increased to 0.03 for BTC 15m), and TB-213 rejected (no spike_min_price_move increased to 0.02 for BTC 15m). These reintroduce explicitly rejected filters for low-liquidity and high-frequency BTC markets.

---

## 2026-04-12 — Advisor snapshot 73

### Summary
False positives are prevalent in low-liquidity markets like golf props, pre-game sports, and high-frequency BTC due to mechanical quote spikes and large quote placements without sustained price moves.

### Next step
Introduce market-type-specific volume delta multipliers (e.g., 2x baseline for golf props and low-liquidity events) and a minimum sustained price deviation requirement over 5 ticks.

### Recommendations

- [ ] **TB-220** `rejected` — Raise volume delta multiplier to 2x baseline for golf prop markets to filter mechanical spikes.
  - **Governor rejection**: The proposed 'minimum sustained price deviation requirement over 5 ticks' directly conflicts with multiple rejected historical constraints, including TB-201 (no 5-minute price persistence for lower-liquidity assets), TB-203 (no minimum sustained price deviation over 5 ticks/5m for notable-tier signals), TB-205 (no minimum sustained price deviation over 5 ticks for notable-tier signals), TB-209 (no minimum sustained price deviation over 5 ticks), and TB-212 (no minimum sustained price deviation over 5 ticks for low-liquidity markets). These were explicitly rejected, indicating a prior decision against implementing sustained price deviation filters, particularly over 5 ticks or equivalent time periods.
- [ ] **TB-221** `rejected` — Require minimum volume delta of 1-2% of baseline for low-liquidity or pre-game markets.
  - **Governor rejection**: The proposed 'minimum sustained price deviation requirement over 5 ticks' directly conflicts with multiple rejected historical constraints, including TB-201 (no 5-minute price persistence for lower-liquidity assets), TB-203 (no minimum sustained price deviation over 5 ticks/5m for notable-tier signals), TB-205 (no minimum sustained price deviation over 5 ticks for notable-tier signals), TB-209 (no minimum sustained price deviation over 5 ticks), and TB-212 (no minimum sustained price deviation over 5 ticks for low-liquidity markets). These were explicitly rejected, indicating a prior decision against implementing sustained price deviation filters, particularly over 5 ticks or equivalent time periods.
- [ ] **TB-222** `rejected` — Add volume-to-price-move ratio threshold or 5-tick sustained price deviation for high-frequency BTC markets.
  - **Governor rejection**: The proposed 'minimum sustained price deviation requirement over 5 ticks' directly conflicts with multiple rejected historical constraints, including TB-201 (no 5-minute price persistence for lower-liquidity assets), TB-203 (no minimum sustained price deviation over 5 ticks/5m for notable-tier signals), TB-205 (no minimum sustained price deviation over 5 ticks for notable-tier signals), TB-209 (no minimum sustained price deviation over 5 ticks), and TB-212 (no minimum sustained price deviation over 5 ticks for low-liquidity markets). These were explicitly rejected, indicating a prior decision against implementing sustained price deviation filters, particularly over 5 ticks or equivalent time periods.

---

## 2026-04-12 — Advisor snapshot 74

### Summary
Your detector is generating false positives primarily in low-liquidity markets (golf props, pre-game NBA, crypto quote placements) where mechanical quote activity and thin order books trigger alerts despite lacking genuine information asymmetry. True signals show either substantial price moves (>0.35) with conviction scoring or genuine information gaps (Trump windmill case) that market prices underestimate.

### Next step
Implement asset-class and liquidity-tier multipliers: apply stricter volume-delta thresholds (2.0x baseline) for low-liquidity markets (golf, pre-game sports) and a volume-to-price-move ratio gate to filter quote spam in high-volume, low-move cases like crypto 15m.

### Suggested thresholds
`min_volume_delta` → `2.0`

### Recommendations

- [ ] **TB-223** `planned` — For golf and low-liquidity prop markets, raise spike_min_volume_delta multiplier from 1.3x to 2.0x baseline to suppress mechanical quote spikes
- [ ] **TB-224** `planned` — Add a volume-to-price-move ratio threshold (e.g., volΔ/priceΔ < 500k for tier=notable) to catch cases like KXBTC15M where 191k volume moved price only 1%
- [ ] **TB-225** `planned` — Lower score_threshold for high-conviction tier signals with strong price moves (>0.35 priceΔ) even if volume is moderate, to surface genuine moves like KXPGAROUNDSCORE-THAT71 (score=51.6, priceΔ=0.81)

---

## 2026-04-12 — Advisor snapshot 75

### Summary
False positives dominate in ultra-short-dated crypto derivatives, low-liquidity golf props, and pre-game markets due to sub-second trade bursts, mechanical quote spikes, and unsustained price moves that mimic informed flow.

### Next step
Require sustained price moves >1% over 60+ seconds and raise volume delta multiplier to 2x baseline for low-liquidity markets.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-226** `planned` — Raise volume-delta threshold or volume-to-price-move ratio to filter execution noise and quote placements.
- [ ] **TB-227** `planned` — Increase min volume delta to 1-2% of baseline for low-liquidity/pre-game markets.
- [ ] **TB-228** `planned` — Raise volume delta multiplier from 1.3x to 2x for golf prop markets.

---

## 2026-04-12 — Advisor snapshot 76

### Summary
False positives dominate in low-liquidity markets (e.g., golf props, pre-game sports, ultra-short crypto derivatives) due to mechanical quote spikes, sub-second trade bursts, and large quote placements without sustained price moves.

### Next step
Require sustained price moves >1% over 60+ seconds AND raise volume delta multiplier to 2x baseline for low-liquidity markets.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-229** `planned` — Raise volume-delta threshold to 1-2% of baseline for low-liquidity/pre-game markets
- [ ] **TB-230** `planned` — Raise volume delta multiplier from 1.3x to 2x for golf prop markets
- [ ] **TB-231** `planned` — Add volume-to-price-move ratio threshold to filter large quotes without directional trades

---

## 2026-04-12 — Advisor snapshot 77

### Summary
False positives dominate in low-liquidity markets like NBA winners, ultra-short-dated crypto derivatives, and golf props due to mechanical quote adjustments, small trades, and sub-second bursts that trigger on low volume deltas and minor price moves despite low scores.

### Next step
Introduce market-type-specific volume delta multipliers (e.g., 5-10x baseline for NBA, 2x for golf) and require sustained price moves >1% over 60s for crypto shorts.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-232** `rejected` — Raise volume delta threshold to 5-10x baseline for NBA winner markets.
  - **Governor rejection**: The proposed tweak violates TB-199,204,206 (no minimum notional trade size filter for crypto 15m/low-volume/low-liquidity markets, interpreted as blocking volume-based filters) by introducing market-type-specific **volume delta multipliers** (e.g., 5-10x baseline), which act as a volume delta filter. It also violates TB-210,213,216,217,218,219 (no spike_min_price_move increases for BTC 15m/high-frequency markets) by setting **min_price_move: 0.01** (>0), and TB-201,203,205,209,212,215,220,221,222 (no 5-minute/5-tick price persistence or sustained price deviation for lower-liquidity assets) by requiring **sustained price moves >1% over 60s** for crypto shorts.
- [ ] **TB-233** `rejected` — Require sustained price move >1% over 60+ seconds for ultra-short-dated crypto.
  - **Governor rejection**: The proposed tweak violates TB-199,204,206 (no minimum notional trade size filter for crypto 15m/low-volume/low-liquidity markets, interpreted as blocking volume-based filters) by introducing market-type-specific **volume delta multipliers** (e.g., 5-10x baseline), which act as a volume delta filter. It also violates TB-210,213,216,217,218,219 (no spike_min_price_move increases for BTC 15m/high-frequency markets) by setting **min_price_move: 0.01** (>0), and TB-201,203,205,209,212,215,220,221,222 (no 5-minute/5-tick price persistence or sustained price deviation for lower-liquidity assets) by requiring **sustained price moves >1% over 60s** for crypto shorts.
- [ ] **TB-234** `rejected` — Increase volume delta multiplier to 2x baseline for golf prop markets.
  - **Governor rejection**: The proposed tweak violates TB-199,204,206 (no minimum notional trade size filter for crypto 15m/low-volume/low-liquidity markets, interpreted as blocking volume-based filters) by introducing market-type-specific **volume delta multipliers** (e.g., 5-10x baseline), which act as a volume delta filter. It also violates TB-210,213,216,217,218,219 (no spike_min_price_move increases for BTC 15m/high-frequency markets) by setting **min_price_move: 0.01** (>0), and TB-201,203,205,209,212,215,220,221,222 (no 5-minute/5-tick price persistence or sustained price deviation for lower-liquidity assets) by requiring **sustained price moves >1% over 60s** for crypto shorts.

---

## 2026-04-12 — Advisor snapshot 78

### Summary
False positives dominate in low-liquidity markets like sports (NBA, golf), crypto shorts, and pre-game events due to routine quoting noise, micro-volume spikes, and unsustained bursts, while genuine signals appear in Trump-related and select golf props with high scores and clear info asymmetry.

### Next step
Introduce dynamic volume delta thresholds scaled by market type and baseline liquidity (e.g., 2-10x for sports/crypto, higher for low-liq props) to filter noise without muting high-conviction flow.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-235** `rejected` — Raise volume delta multiplier to 2x baseline minimum for sports winner markets (NBA, etc.)
  - **Governor rejection**: The proposed tweak directly violates TB-200, TB-202, TB-208, TB-211, and TB-214 (all explicitly rejected). These constraints rejected volume-to-price-move ratio thresholds and volume delta multipliers for crypto 15m/low-liquidity/high-frequency markets. The recommendation to introduce 'dynamic volume delta thresholds scaled by market type' (e.g., 2-10x for crypto) is functionally equivalent to the rejected multiplier-based approach. Additionally, setting min_price_move to 0.01 conflicts with TB-210, TB-213, and TB-216-219, which rejected all spike_min_price_move increases for BTC 15m/high-frequency markets. The proposal attempts to reintroduce filtering mechanisms (volume/price scaling and price move minimums) that were systematically rejected to preserve high-frequency signal detection in these market segments.
- [ ] **TB-236** `rejected` — Require sustained price moves >1% over 60s or volume-to-price ratio check for crypto shorts
  - **Governor rejection**: The proposed tweak directly violates TB-200, TB-202, TB-208, TB-211, and TB-214 (all explicitly rejected). These constraints rejected volume-to-price-move ratio thresholds and volume delta multipliers for crypto 15m/low-liquidity/high-frequency markets. The recommendation to introduce 'dynamic volume delta thresholds scaled by market type' (e.g., 2-10x for crypto) is functionally equivalent to the rejected multiplier-based approach. Additionally, setting min_price_move to 0.01 conflicts with TB-210, TB-213, and TB-216-219, which rejected all spike_min_price_move increases for BTC 15m/high-frequency markets. The proposal attempts to reintroduce filtering mechanisms (volume/price scaling and price move minimums) that were systematically rejected to preserve high-frequency signal detection in these market segments.
- [ ] **TB-237** `rejected` — Set category-specific min volume delta (e.g., 1-2% baseline for low-liq/pre-game, 2x for golf props)
  - **Governor rejection**: The proposed tweak directly violates TB-200, TB-202, TB-208, TB-211, and TB-214 (all explicitly rejected). These constraints rejected volume-to-price-move ratio thresholds and volume delta multipliers for crypto 15m/low-liquidity/high-frequency markets. The recommendation to introduce 'dynamic volume delta thresholds scaled by market type' (e.g., 2-10x for crypto) is functionally equivalent to the rejected multiplier-based approach. Additionally, setting min_price_move to 0.01 conflicts with TB-210, TB-213, and TB-216-219, which rejected all spike_min_price_move increases for BTC 15m/high-frequency markets. The proposal attempts to reintroduce filtering mechanisms (volume/price scaling and price move minimums) that were systematically rejected to preserve high-frequency signal detection in these market segments.

---

## 2026-04-12 — Advisor snapshot 79

### Summary
False positives dominate in low-liquidity markets like pre-game NBA, golf props, and short-dated crypto due to mechanical quote adjustments, small trade bursts, and sub-second noise despite large volume deltas but tiny price moves (<0.04). Genuine signals appear in high-conviction flow or clear information asymmetry like political props.

### Next step
Introduce market-type-specific volume delta multipliers (e.g., 5-10x baseline for NBA, 2x for sports winners, 2x for golf props) and require sustained price moves >0.03 over 60s.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-238** `rejected` — Raise volume delta threshold to 5-10x baseline for pre-game NBA and low-liquidity winner markets to filter micro-spikes.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introduces **market-type-specific volume delta multipliers** (e.g., 5-10x baseline for NBA, 2x for sports winners/golf props), explicitly rejected in TB-220,221,232,234,235,237 for low-liquidity/pre-game/golf props/NBA/sports winner markets. (2) Requires **sustained price moves >0.03 over 60s**, conflicting with rejections of sustained price moves >1% over 60s (TB-233,236 for ultra-short-dated crypto/crypto shorts) and 5-minute/5-tick price persistence or sustained price deviation (TB-201,203,205,209,212,215,220-222 for lower-liquidity/high-frequency/BTC 15m/crypto shorts), as well as no spike_min_price_move increases (e.g., to 0.02/0.03/0.05; TB-210,213,216-219 for BTC 15m/high-frequency markets).
- [ ] **TB-239** `rejected` — Require minimum price move of 0.03 (3%) or sustained >1% over 60s for crypto and high-freq markets.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introduces **market-type-specific volume delta multipliers** (e.g., 5-10x baseline for NBA, 2x for sports winners/golf props), explicitly rejected in TB-220,221,232,234,235,237 for low-liquidity/pre-game/golf props/NBA/sports winner markets. (2) Requires **sustained price moves >0.03 over 60s**, conflicting with rejections of sustained price moves >1% over 60s (TB-233,236 for ultra-short-dated crypto/crypto shorts) and 5-minute/5-tick price persistence or sustained price deviation (TB-201,203,205,209,212,215,220-222 for lower-liquidity/high-frequency/BTC 15m/crypto shorts), as well as no spike_min_price_move increases (e.g., to 0.02/0.03/0.05; TB-210,213,216-219 for BTC 15m/high-frequency markets).
- [ ] **TB-240** `rejected` — Increase volume-to-price ratio threshold and golf prop multiplier from 1.3x to 2x baseline.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introduces **market-type-specific volume delta multipliers** (e.g., 5-10x baseline for NBA, 2x for sports winners/golf props), explicitly rejected in TB-220,221,232,234,235,237 for low-liquidity/pre-game/golf props/NBA/sports winner markets. (2) Requires **sustained price moves >0.03 over 60s**, conflicting with rejections of sustained price moves >1% over 60s (TB-233,236 for ultra-short-dated crypto/crypto shorts) and 5-minute/5-tick price persistence or sustained price deviation (TB-201,203,205,209,212,215,220-222 for lower-liquidity/high-frequency/BTC 15m/crypto shorts), as well as no spike_min_price_move increases (e.g., to 0.02/0.03/0.05; TB-210,213,216-219 for BTC 15m/high-frequency markets).

---

## 2026-04-12 — Advisor snapshot 80

### Summary
False positives dominate in low-liquidity markets like pre-game NBA, golf props, and ultra-short-dated crypto, driven by routine quoting noise, small trade bursts, and mechanical quote spikes despite high volume deltas; genuine signals appear in whale clusters and high-conviction flow with asymmetric info.

### Next step
Introduce market-type-specific volume delta multipliers (e.g., 5-10x baseline for NBA/golf, 2x for sports winners) and require sustained price moves >1% over 60s for crypto.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-241** `planned` — Raise volume delta threshold to 5-10x baseline for pre-game NBA and low-liquidity markets to filter quote noise.
- [ ] **TB-242** `planned` — Require minimum price move of 0.03+ or sustained >1% over 60s, especially for crypto derivatives.
- [ ] **TB-243** `planned` — Increase score_threshold to 5.0+ and add volume-to-price ratio check to suppress large-volume/low-move noise.

---

## 2026-04-12 — Advisor snapshot 81

### Summary
Your detector is generating false positives in low-liquidity markets (BTC 15M, NBA pre-game, golf props) by treating mechanical quote adjustments and thin-market trade bursts as informed flow. True signals are being correctly identified but are buried among noise.

### Next step
Implement market-segment-specific volume delta thresholds rather than a single global threshold. Crypto derivatives and sports pre-game markets require 5-10x baseline elevation; golf props need 2x; general sports need 2x minimum.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-244** `rejected` — For BTC 15M (ultra-short-dated crypto): Raise spike_min_volume_delta to 10x baseline or require sustained price moves >1% over 60+ seconds to filter execution noise and sub-second trade bursts.
  - **Governor rejection**: The proposed tweak violates Rejected (TB-220+): no market-type-specific volume delta multipliers (e.g., 1-10x/1-2% baseline) for low-liq/pre-game/golf props/NBA/sports winners. The recommendation explicitly introduces 5-10x baseline elevation for crypto derivatives (including BTC 15M), 2x for golf props, and 2x for general sports (including NBA pre-game), which are market-segment-specific volume delta multipliers directly conflicting with this rejected constraint.
- [ ] **TB-245** `rejected` — For NBA pre-game and low-activity periods: Raise spike_min_volume_delta to 5-10x baseline to eliminate mechanical quote-trades and small cluster activity.
  - **Governor rejection**: The proposed tweak violates Rejected (TB-220+): no market-type-specific volume delta multipliers (e.g., 1-10x/1-2% baseline) for low-liq/pre-game/golf props/NBA/sports winners. The recommendation explicitly introduces 5-10x baseline elevation for crypto derivatives (including BTC 15M), 2x for golf props, and 2x for general sports (including NBA pre-game), which are market-segment-specific volume delta multipliers directly conflicting with this rejected constraint.
- [ ] **TB-246** `rejected` — For golf props and low-liquidity events: Raise volume delta multiplier from 1.3x to 2x baseline to filter quote spike noise.
  - **Governor rejection**: The proposed tweak violates Rejected (TB-220+): no market-type-specific volume delta multipliers (e.g., 1-10x/1-2% baseline) for low-liq/pre-game/golf props/NBA/sports winners. The recommendation explicitly introduces 5-10x baseline elevation for crypto derivatives (including BTC 15M), 2x for golf props, and 2x for general sports (including NBA pre-game), which are market-segment-specific volume delta multipliers directly conflicting with this rejected constraint.
- [ ] **TB-247** `rejected` — For general sports markets: Raise spike_min_volume_delta to at least 2x baseline to suppress routine quoting noise during low-activity periods.
  - **Governor rejection**: The proposed tweak violates Rejected (TB-220+): no market-type-specific volume delta multipliers (e.g., 1-10x/1-2% baseline) for low-liq/pre-game/golf props/NBA/sports winners. The recommendation explicitly introduces 5-10x baseline elevation for crypto derivatives (including BTC 15M), 2x for golf props, and 2x for general sports (including NBA pre-game), which are market-segment-specific volume delta multipliers directly conflicting with this rejected constraint.
- [ ] **TB-248** `rejected` — Implement a price-move floor: Require spike_min_price_move ≥ 0.01 (1%) for ultra-short-dated instruments to distinguish informed flow from execution artifacts.
  - **Governor rejection**: The proposed tweak violates Rejected (TB-220+): no market-type-specific volume delta multipliers (e.g., 1-10x/1-2% baseline) for low-liq/pre-game/golf props/NBA/sports winners. The recommendation explicitly introduces 5-10x baseline elevation for crypto derivatives (including BTC 15M), 2x for golf props, and 2x for general sports (including NBA pre-game), which are market-segment-specific volume delta multipliers directly conflicting with this rejected constraint.

---

## 2026-04-12 — Advisor snapshot 82

### Summary
False positives dominate in low-liquidity markets like 15-min BTC, pre-game NBA, golf props, and sports winners due to thin liquidity spikes, quote adjustments, and small trade bursts without meaningful price moves, while true signals like whale-clusters with priceΔ>0 or high-confidence events like TRUMPSAY persist.

### Next step
Require min_price_move >0.01 alongside volume delta to filter execution noise and quote spikes in low-liquidity markets.

### Suggested thresholds
`min_price_move` → `0.01`, `score_threshold` → `10.0`

### Recommendations

- [ ] **TB-249** `rejected` — Raise spike_min_volume_delta to 10x baseline for 15-min BTC and crypto derivatives
  - **Governor rejection**: The proposed tweak directly violates TB-210, TB-213, and TB-216-219, which explicitly rejected spike_min_price_move increases (including 0.01 thresholds) for BTC 15m/high-freq markets. The proposal to require min_price_move > 0.01 alongside volume delta reintroduces a rejected constraint for the exact market conditions (15-min BTC, high-frequency) where these rejections were applied. This represents a regression that contradicts the historical decision to avoid price-move filtering in these markets.
- [ ] **TB-250** `rejected` — Set market-type thresholds: 5-10x baseline for pre-game NBA/golf props, 2x for sports winners
  - **Governor rejection**: The proposed tweak directly violates TB-210, TB-213, and TB-216-219, which explicitly rejected spike_min_price_move increases (including 0.01 thresholds) for BTC 15m/high-freq markets. The proposal to require min_price_move > 0.01 alongside volume delta reintroduces a rejected constraint for the exact market conditions (15-min BTC, high-frequency) where these rejections were applied. This represents a regression that contradicts the historical decision to avoid price-move filtering in these markets.
- [ ] **TB-251** `rejected` — Increase score_threshold to 10+ for tier=watch/notable to prioritize whale-cluster and high-confidence signals
  - **Governor rejection**: The proposed tweak directly violates TB-210, TB-213, and TB-216-219, which explicitly rejected spike_min_price_move increases (including 0.01 thresholds) for BTC 15m/high-freq markets. The proposal to require min_price_move > 0.01 alongside volume delta reintroduces a rejected constraint for the exact market conditions (15-min BTC, high-frequency) where these rejections were applied. This represents a regression that contradicts the historical decision to avoid price-move filtering in these markets.

---

## 2026-04-12 — Advisor snapshot 83

### Summary
False positives dominate in low-liquidity markets like golf props, NBA pre-game, and short-dated BTC/crypto derivatives, often from small volume spikes, quote noise, or single large trades without sustained directional flow, while true signals appear in high-info asymmetry cases like political props.

### Next step
Introduce market-type-specific dynamic volume delta multipliers (e.g., 5-10x baseline for sports/crypto props, 2x for liquid politics) and require sustained price move >0.02 or directional bias over 2+ events.

### Suggested thresholds
`min_volume_delta` → `2000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-252** `planned` — Raise min_volume_delta multiplier to 2-10x baseline by market tier (low-liq: 5-10x, sports: 2-5x) to filter quote noise and thin liquidity spikes.
- [ ] **TB-253** `planned` — Increase min_price_move to 0.03 for watch/notable tiers and require >60s sustained move for crypto shorts.
- [ ] **TB-254** `planned` — Add rule: sustained flow check (consistent yes/no bias over 2+ consecutive signals) before emitting on round/game-specific markets.

---

## 2026-04-12 — Advisor snapshot 84

### Summary
False positives dominate in low-liquidity 15-minute BTC markets from whale-cluster and watch tiers, where high volume deltas occur without price movement, often due to noise, layering, or thin-book activity; sports and round markets also show noise from small bursts.

### Next step
Require priceΔ >0.02 OR volΔ >1000 for whale-cluster tier on 15-min BTC markets to filter zero-impact volume spikes.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-255** `rejected` — For 15-min BTC whale-cluster: require volΔ >0.5x baseline AND (priceΔ >0.02 OR yes≠0.5).
  - **Governor rejection**: The proposed tweak violates TB-200,202,208,211,214 (no volume-to-price-move ratio threshold, e.g., volΔ>200k USD w/ priceΔ≥0.02; volΔ/priceΔ>1000/10000) by introducing a combined priceΔ >0.02 OR volΔ >1000 requirement for whale-cluster tier on 15m BTC, which enforces a volume-to-price-move filter to exclude zero-price-impact volume spikes, directly conflicting with the explicit rejection of such ratio-based thresholds in low-liquidity/high-freq BTC 15m markets.
- [ ] **TB-256** `rejected` — Raise min_volume_delta to 1000+ for thin markets (15-min BTC, NBA pre-game) to cut micro-spikes.
  - **Governor rejection**: The proposed tweak violates TB-200,202,208,211,214 (no volume-to-price-move ratio threshold, e.g., volΔ>200k USD w/ priceΔ≥0.02; volΔ/priceΔ>1000/10000) by introducing a combined priceΔ >0.02 OR volΔ >1000 requirement for whale-cluster tier on 15m BTC, which enforces a volume-to-price-move filter to exclude zero-price-impact volume spikes, directly conflicting with the explicit rejection of such ratio-based thresholds in low-liquidity/high-freq BTC 15m markets.
- [ ] **TB-257** `rejected` — Add filter: exclude spikes with priceΔ=0.0 unless volΔ >50x baseline or sustained over 60s.
  - **Governor rejection**: The proposed tweak violates TB-200,202,208,211,214 (no volume-to-price-move ratio threshold, e.g., volΔ>200k USD w/ priceΔ≥0.02; volΔ/priceΔ>1000/10000) by introducing a combined priceΔ >0.02 OR volΔ >1000 requirement for whale-cluster tier on 15m BTC, which enforces a volume-to-price-move filter to exclude zero-price-impact volume spikes, directly conflicting with the explicit rejection of such ratio-based thresholds in low-liquidity/high-freq BTC 15m markets.

---

## 2026-04-12 — Advisor snapshot 85

### Summary
High false positives in whale-cluster signals on low-liquidity 15-minute BTC markets with zero or minimal price movement despite moderate volume deltas, and watch-tier signals on sports markets from routine quoting noise.

### Next step
Require minimum price movement >2% OR volume delta >25x baseline for whale-cluster tier on 15-min markets; raise volume delta threshold to 5-10x baseline for watch tier.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-258** `planned` — For whale-cluster: filter spikes with priceΔ=0 and yes~0.5 at midprice to exclude layering/coordination.
- [ ] **TB-259** `planned` — Raise min_volume_delta to 0.5x-1x baseline specifically for 15-min BTC markets.
- [ ] **TB-260** `planned` — Require sustained directional flow or >2% price move for watch-tier sports/round markets.

---

## 2026-04-12 — Advisor snapshot 86

### Summary
Your detector is generating false positives on whale-cluster spikes in 15-minute BTC markets where large volume deltas occur without corresponding price movement, suggesting coordination or layering rather than genuine price discovery. The critical issue is that volume alone is insufficient; price impact must be required to distinguish signal from noise.

### Next step
Implement a price-impact filter: require whale-cluster spikes to show either >2.0% price movement OR volume delta >25x baseline; reject spikes where priceΔ=0.0 even with high volΔ, as these indicate price-neutral accumulation or potential market manipulation rather than informative flow.

### Suggested thresholds
`min_volume_delta` → `750.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-261** `planned` — For whale-cluster tier on 15-min BTC markets: reject signals where priceΔ=0.0 and volΔ<7500 (25x baseline), as these are coordination signals without conviction
- [ ] **TB-262** `planned` — For whale-cluster tier: raise volume delta threshold to 0.5x baseline (approximately 500–750 depending on contract liquidity) or require >2.0% price movement to separate layering from real conviction flow
- [ ] **TB-263** `planned` — For watch and notable tiers on thin 15-min markets: require sustained directional bias (multiple consecutive same-side events) or volΔ >10x baseline before emitting signals, as single large trades in low-activity windows generate statistical noise
- [ ] **TB-264** `planned` — Add explicit filter: flag and suppress spikes where volume_delta is high but price_delta is zero AND midprice participation is detected (yes probability ~0.50), as these patterns match layering behavior documented in prediction market microstructure

---

## 2026-04-12 — Advisor snapshot 87

### Summary
Whale-cluster signals on low-liquidity 15-minute BTC markets trigger frequent false positives due to high volume deltas without price movement, often labeled as noise or no-signal despite scores of 8.0+.

### Next step
Require minimum 2% price movement or volume delta >25% of baseline for whale-cluster tier on 15-min markets to filter noise.

### Suggested thresholds
`min_volume_delta` → `750.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-265** `rejected` — Raise whale-cluster min_volume_delta to 0.5x baseline for 15-min BTC markets
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: **No minimum notional trade size filter** (TB-199,204,206 rejected) by introducing min_volume_delta: 750.0 as a filter; **No volume-to-price-move ratio threshold** (TB-200,202,208,211,214 rejected) by requiring volume delta >25% of baseline tied to price movement; **No 5-minute/5-tick price persistence or sustained price deviation** (TB-201,203,205,209,212,215,220-222 rejected), extended to **No spike_min_price_move increases** (TB-210,213,216-219 rejected) by setting min_price_move: 0.02 (2%) for BTC 15m low-liquidity whale-cluster markets; and **No combined priceΔ/volΔ filters** (TB-255,257 rejected) by mandating minimum 2% price movement OR volume delta >25% of baseline.
- [ ] **TB-266** `rejected` — Filter spikes at yes=0.50 with zero price impact as potential layering
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: **No minimum notional trade size filter** (TB-199,204,206 rejected) by introducing min_volume_delta: 750.0 as a filter; **No volume-to-price-move ratio threshold** (TB-200,202,208,211,214 rejected) by requiring volume delta >25% of baseline tied to price movement; **No 5-minute/5-tick price persistence or sustained price deviation** (TB-201,203,205,209,212,215,220-222 rejected), extended to **No spike_min_price_move increases** (TB-210,213,216-219 rejected) by setting min_price_move: 0.02 (2%) for BTC 15m low-liquidity whale-cluster markets; and **No combined priceΔ/volΔ filters** (TB-255,257 rejected) by mandating minimum 2% price movement OR volume delta >25% of baseline.
- [ ] **TB-267** `rejected` — Require >2.0% price move for whale-cluster signals without sustained volume
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: **No minimum notional trade size filter** (TB-199,204,206 rejected) by introducing min_volume_delta: 750.0 as a filter; **No volume-to-price-move ratio threshold** (TB-200,202,208,211,214 rejected) by requiring volume delta >25% of baseline tied to price movement; **No 5-minute/5-tick price persistence or sustained price deviation** (TB-201,203,205,209,212,215,220-222 rejected), extended to **No spike_min_price_move increases** (TB-210,213,216-219 rejected) by setting min_price_move: 0.02 (2%) for BTC 15m low-liquidity whale-cluster markets; and **No combined priceΔ/volΔ filters** (TB-255,257 rejected) by mandating minimum 2% price movement OR volume delta >25% of baseline.

---

## 2026-04-12 — Advisor snapshot 88

### Summary
The detector is generating numerous false positives on 15-minute BTC markets where whale-cluster volume spikes occur without accompanying price movement. Analysts consistently flag signals with zero or minimal price delta (priceΔ=0.0) as non-signals, indicating the system conflates high-volume activity with informative flow.

### Next step
Implement a price-impact filter: require whale-cluster spikes to demonstrate measurable price movement (>1.0% for 15-minute windows) or reject them as coordination/layering noise rather than conviction-driven flow. This directly addresses the analyst consensus that volume-only signals lack predictive value.

### Suggested thresholds
`min_volume_delta` → `750.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-268** `rejected` — Add a mandatory price-movement constraint for whale-cluster tier: priceΔ ≥ 0.01 (1%) for 15-minute contracts, or reclassify as potential coordination rather than market signal
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: **TB-210,213,216-219 rejected** explicitly prohibit 'No spike_min_price_move increases (e.g. to 0.02/0.03/0.05/0.01) for BTC 15m/high-freq markets', and the suggested min_price_move: 0.01 matches one of the rejected examples (0.01). Additionally, it conflicts with **TB-201,203,205,209,212,215,220-222 rejected** ('No 5-min/5-tick price persistence or sustained price deviation' for BTC 15m), **TB-255,256,257 rejected** ('No combined priceΔ/volΔ filters (e.g. priceΔ>0.02 OR volΔ>1000...)' for 15m BTC whale-cluster), and **TB-200,202,208,211,214 rejected** ('No volume-to-price-move ratio threshold'). This introduces a price movement requirement previously rejected to avoid filtering out valid volume-only whale signals.
- [ ] **TB-269** `rejected` — Raise whale-cluster volume_delta baseline multiplier to 0.5x (approximately 750+ units based on observed signals) to filter low-volume coordinations; alternatively, require 25% of rolling baseline volume per analyst feedback
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: **TB-210,213,216-219 rejected** explicitly prohibit 'No spike_min_price_move increases (e.g. to 0.02/0.03/0.05/0.01) for BTC 15m/high-freq markets', and the suggested min_price_move: 0.01 matches one of the rejected examples (0.01). Additionally, it conflicts with **TB-201,203,205,209,212,215,220-222 rejected** ('No 5-min/5-tick price persistence or sustained price deviation' for BTC 15m), **TB-255,256,257 rejected** ('No combined priceΔ/volΔ filters (e.g. priceΔ>0.02 OR volΔ>1000...)' for 15m BTC whale-cluster), and **TB-200,202,208,211,214 rejected** ('No volume-to-price-move ratio threshold'). This introduces a price movement requirement previously rejected to avoid filtering out valid volume-only whale signals.
- [ ] **TB-270** `rejected` — Implement directional-flow persistence check: flag only when sustained side bias (consistent buy/sell imbalance) occurs over 2+ consecutive detection windows, reducing false positives from single large orders at midprice (yes≈0.50)
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: **TB-210,213,216-219 rejected** explicitly prohibit 'No spike_min_price_move increases (e.g. to 0.02/0.03/0.05/0.01) for BTC 15m/high-freq markets', and the suggested min_price_move: 0.01 matches one of the rejected examples (0.01). Additionally, it conflicts with **TB-201,203,205,209,212,215,220-222 rejected** ('No 5-min/5-tick price persistence or sustained price deviation' for BTC 15m), **TB-255,256,257 rejected** ('No combined priceΔ/volΔ filters (e.g. priceΔ>0.02 OR volΔ>1000...)' for 15m BTC whale-cluster), and **TB-200,202,208,211,214 rejected** ('No volume-to-price-move ratio threshold'). This introduces a price movement requirement previously rejected to avoid filtering out valid volume-only whale signals.

---

## 2026-04-12 — Advisor snapshot 89

### Summary
Whale-cluster signals on low-volume 15-minute BTC markets trigger frequently with high scores and volume deltas around 400-900 but zero or minimal price movement, leading to many false positives labeled as noise or no-signal despite some yes labels.

### Next step
Require minimum price movement >0.01 or volume delta >1000x baseline for whale-cluster tier on 15-min markets to filter price-neutral noise.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-271** `rejected` — Raise spike_min_volume_delta to 1000 for 15-minute BTC contracts
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-001 applied** requires whale-cluster volume delta threshold ≥1000 for 15m BTC, but the proposal sets min_volume_delta: 1000.0 (exact match, not a relaxation but redundant with existing); critically, it introduces min_price_move: 0.02, conflicting with **No spike_min_price_move increases** (TB-210,213,216-219,248-251,265-270 rejected) which explicitly blocks min_price_move increases (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets; (2) **No minimum notional trade size filter** (TB-199,204,206,265-267 rejected) and **No combined priceΔ/volΔ filters** (TB-255,256,257,265-267 rejected) block adding price movement requirements or combined volΔ/priceΔ conditions for 15m BTC whale-cluster/low-volume markets, as this is a price-neutral noise filter using OR logic (price>0.01 OR vol>1000x baseline).
- [ ] **TB-272** `rejected` — Set spike_min_price_move to 0.02 for whale-cluster tier
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-001 applied** requires whale-cluster volume delta threshold ≥1000 for 15m BTC, but the proposal sets min_volume_delta: 1000.0 (exact match, not a relaxation but redundant with existing); critically, it introduces min_price_move: 0.02, conflicting with **No spike_min_price_move increases** (TB-210,213,216-219,248-251,265-270 rejected) which explicitly blocks min_price_move increases (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets; (2) **No minimum notional trade size filter** (TB-199,204,206,265-267 rejected) and **No combined priceΔ/volΔ filters** (TB-255,256,257,265-267 rejected) block adding price movement requirements or combined volΔ/priceΔ conditions for 15m BTC whale-cluster/low-volume markets, as this is a price-neutral noise filter using OR logic (price>0.01 OR vol>1000x baseline).
- [ ] **TB-273** `rejected` — Filter out spikes at yes=0.50 with priceΔ=0.00 as likely layering
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-001 applied** requires whale-cluster volume delta threshold ≥1000 for 15m BTC, but the proposal sets min_volume_delta: 1000.0 (exact match, not a relaxation but redundant with existing); critically, it introduces min_price_move: 0.02, conflicting with **No spike_min_price_move increases** (TB-210,213,216-219,248-251,265-270 rejected) which explicitly blocks min_price_move increases (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets; (2) **No minimum notional trade size filter** (TB-199,204,206,265-267 rejected) and **No combined priceΔ/volΔ filters** (TB-255,256,257,265-267 rejected) block adding price movement requirements or combined volΔ/priceΔ conditions for 15m BTC whale-cluster/low-volume markets, as this is a price-neutral noise filter using OR logic (price>0.01 OR vol>1000x baseline).

---

## 2026-04-12 — Advisor snapshot 90

### Summary
The detector is generating high-volume false positives on 15-minute BTC markets where large volume deltas occur with zero or minimal price movement, suggesting coordination or layering rather than conviction-driven flow. Watch-tier and whale-cluster signals consistently lack price discovery despite triggering on volume alone.

### Next step
Implement a price-movement coupling requirement: for whale-cluster tier, require either priceΔ >2.0% OR volΔ >25x baseline volume; for watch-tier on short-dated markets, add a notional-value minimum ($500+) and require volΔ to exceed 2.5x baseline.

### Suggested thresholds
`min_volume_delta` → `0.5`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-274** `rejected` — Add a price-impact filter for whale-cluster spikes: flag only signals where volume delta correlates with >1.0% price move, or require volΔ to exceed 50x baseline to capture genuine conviction without noise.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-255,256,257,265-267,271-273 rejected**: Introduces a combined priceΔ/volΔ filter ('priceΔ >2.0% OR volΔ >25x baseline volume') for 15m BTC whale-cluster, explicitly rejected. (2) **TB-210,213,216-219,248-251,265-270 rejected**: Sets min_price_move: 0.02, constituting a spike_min_price_move increase for BTC 15m markets. (3) **TB-220,221,232,234,235,237,244-247 rejected**: Adds market-type-specific volume delta multipliers (25x baseline for whale-cluster, 2.5x for watch-tier short-dated) for crypto/BTC 15m markets.
- [ ] **TB-275** `rejected` — For 15-minute BTC markets specifically, raise whale-cluster volume delta threshold to 0.5x baseline and reject signals where volume hits midprice (yes≈0.50) with zero subsequent price impact.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-255,256,257,265-267,271-273 rejected**: Introduces a combined priceΔ/volΔ filter ('priceΔ >2.0% OR volΔ >25x baseline volume') for 15m BTC whale-cluster, explicitly rejected. (2) **TB-210,213,216-219,248-251,265-270 rejected**: Sets min_price_move: 0.02, constituting a spike_min_price_move increase for BTC 15m markets. (3) **TB-220,221,232,234,235,237,244-247 rejected**: Adds market-type-specific volume delta multipliers (25x baseline for whale-cluster, 2.5x for watch-tier short-dated) for crypto/BTC 15m markets.
- [ ] **TB-276** `rejected` — For watch-tier low-liquidity markets, enforce a minimum notional trade size ($500+) and require sustained directional flow (consistent side bias over 2+ consecutive events) before emitting signals.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-255,256,257,265-267,271-273 rejected**: Introduces a combined priceΔ/volΔ filter ('priceΔ >2.0% OR volΔ >25x baseline volume') for 15m BTC whale-cluster, explicitly rejected. (2) **TB-210,213,216-219,248-251,265-270 rejected**: Sets min_price_move: 0.02, constituting a spike_min_price_move increase for BTC 15m markets. (3) **TB-220,221,232,234,235,237,244-247 rejected**: Adds market-type-specific volume delta multipliers (25x baseline for whale-cluster, 2.5x for watch-tier short-dated) for crypto/BTC 15m markets.
- [ ] **TB-277** `rejected` — Separate price-moving volume (signal) from price-neutral accumulation (noise) by conditioning whale-cluster detections on priceΔ >0.0% or requiring volΔ deltas to exceed 10x the baseline for thin order-book activity.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-255,256,257,265-267,271-273 rejected**: Introduces a combined priceΔ/volΔ filter ('priceΔ >2.0% OR volΔ >25x baseline volume') for 15m BTC whale-cluster, explicitly rejected. (2) **TB-210,213,216-219,248-251,265-270 rejected**: Sets min_price_move: 0.02, constituting a spike_min_price_move increase for BTC 15m markets. (3) **TB-220,221,232,234,235,237,244-247 rejected**: Adds market-type-specific volume delta multipliers (25x baseline for whale-cluster, 2.5x for watch-tier short-dated) for crypto/BTC 15m markets.

---

## 2026-04-12 — Advisor snapshot 91

### Summary
False positives dominate in low-liquidity, short-dated markets like 15-min BTC and sports events, where routine volume noise, zero-price-impact whale clusters, and small absolute trades trigger signals without predictive content.

### Next step
Add market-specific filters: raise volume delta to 1.5x baseline for sports, require >0.02 price move or 0.5x baseline volume for 15-min BTC whale-clusters, and enforce $500 notional minimum for low-liq short-dated markets.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-278** `rejected` — Raise volume delta multiplier to 1.5x baseline for sports winner markets
  - **Governor rejection**: The proposed tweak conflicts with multiple historical constraints: (1) 'No minimum notional trade size filter (USD equiv.) for crypto 15m/low-volume/low-liquidity markets (TB-199,204,206,265-267 rejected)' - violates by enforcing $500 notional minimum for low-liq short-dated markets including 15m crypto; (2) 'No spike_min_price_move increases (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets (TB-210,213,216-219,248-251,265-270 rejected)' - violates by requiring >0.02 price move for 15-min BTC whale-clusters; (3) 'No market-type-specific volume delta multipliers (e.g., 1-10x/1-2% baseline) for low-liq/.../sports.../crypto (TB-220,221,232,234,235,237,244-247 rejected)' - violates by raising volume delta to 1.5x baseline for sports.
- [ ] **TB-279** `rejected` — Require whale-cluster spikes to show >0.02 price move or >25% baseline volume in 15-min markets
  - **Governor rejection**: The proposed tweak conflicts with multiple historical constraints: (1) 'No minimum notional trade size filter (USD equiv.) for crypto 15m/low-volume/low-liquidity markets (TB-199,204,206,265-267 rejected)' - violates by enforcing $500 notional minimum for low-liq short-dated markets including 15m crypto; (2) 'No spike_min_price_move increases (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets (TB-210,213,216-219,248-251,265-270 rejected)' - violates by requiring >0.02 price move for 15-min BTC whale-clusters; (3) 'No market-type-specific volume delta multipliers (e.g., 1-10x/1-2% baseline) for low-liq/.../sports.../crypto (TB-220,221,232,234,235,237,244-247 rejected)' - violates by raising volume delta to 1.5x baseline for sports.
- [ ] **TB-280** `rejected` — Filter out price-neutral spikes at midprice (0.50) and add $500 notional-value minimum for watch-tier signals
  - **Governor rejection**: The proposed tweak conflicts with multiple historical constraints: (1) 'No minimum notional trade size filter (USD equiv.) for crypto 15m/low-volume/low-liquidity markets (TB-199,204,206,265-267 rejected)' - violates by enforcing $500 notional minimum for low-liq short-dated markets including 15m crypto; (2) 'No spike_min_price_move increases (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets (TB-210,213,216-219,248-251,265-270 rejected)' - violates by requiring >0.02 price move for 15-min BTC whale-clusters; (3) 'No market-type-specific volume delta multipliers (e.g., 1-10x/1-2% baseline) for low-liq/.../sports.../crypto (TB-220,221,232,234,235,237,244-247 rejected)' - violates by raising volume delta to 1.5x baseline for sports.

---

## 2026-04-12 — Advisor snapshot 92

### Summary
Whale-cluster signals on low-liquidity 15-minute BTC markets generate frequent false positives due to volume spikes without price movement or predictive content, while watch-tier signals in sports and short-dated markets trigger on routine liquidity noise.

### Next step
Require minimum price movement >0.0% or volume delta >1.5x baseline for whale-cluster tier, and add notional-value minimum ($500+) for low-liquidity markets.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-281** `rejected` — Raise whale-cluster volume delta threshold to 0.5x-1.5x baseline and require >2% price move or 25%+ of baseline volume for 15-min BTC markets.
  - **Governor rejection**: The proposed tweak sets min_price_move: 0.02, which directly conflicts with 'No spike_min_price_move increases (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets (TB-210,213,216-219,248-251,265-270 rejected)'. This introduces a minimum price movement requirement that was explicitly rejected to avoid restricting whale-cluster detection in low-liquidity BTC 15m markets. Additionally, the 'notional-value minimum ($500+)' for low-liquidity markets conflicts with 'No minimum notional trade size filter (USD equiv.) for crypto 15m/low-volume/low-liquidity markets (TB-199,204,206,265-267 rejected)'.
- [ ] **TB-282** `rejected` — For sports winner and round-specific markets, increase volume delta multiplier to 1.5x baseline and require sustained directional flow.
  - **Governor rejection**: The proposed tweak sets min_price_move: 0.02, which directly conflicts with 'No spike_min_price_move increases (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets (TB-210,213,216-219,248-251,265-270 rejected)'. This introduces a minimum price movement requirement that was explicitly rejected to avoid restricting whale-cluster detection in low-liquidity BTC 15m markets. Additionally, the 'notional-value minimum ($500+)' for low-liquidity markets conflicts with 'No minimum notional trade size filter (USD equiv.) for crypto 15m/low-volume/low-liquidity markets (TB-199,204,206,265-267 rejected)'.
- [ ] **TB-283** `rejected` — Filter spikes at midprice (yes~0.5) with zero price impact, and add $500+ notional-value minimum for watch-tier short-dated markets.
  - **Governor rejection**: The proposed tweak sets min_price_move: 0.02, which directly conflicts with 'No spike_min_price_move increases (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets (TB-210,213,216-219,248-251,265-270 rejected)'. This introduces a minimum price movement requirement that was explicitly rejected to avoid restricting whale-cluster detection in low-liquidity BTC 15m markets. Additionally, the 'notional-value minimum ($500+)' for low-liquidity markets conflicts with 'No minimum notional trade size filter (USD equiv.) for crypto 15m/low-volume/low-liquidity markets (TB-199,204,206,265-267 rejected)'.

---

## 2026-04-12 — Advisor snapshot 93

### Summary
False positives dominate in low-liquidity, short-dated markets like 15-min BTC contracts and sports/resolution markets, where high volΔ triggers without price movement or predictive content, often labeled as noise/unclear/no due to routine liquidity, coordination, or layering.

### Next step
Require priceΔ > 0.02 for all whale-cluster and watch-tier signals unless volΔ exceeds 50x baseline, to filter price-neutral accumulation.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-284** `rejected` — Raise whale-cluster volΔ threshold to 0.5x baseline for 15-min BTC markets.
  - **Governor rejection**: The proposed tweak requires priceΔ > 0.02 for whale-cluster signals (unless volΔ >50x baseline), which directly conflicts with multiple historical constraints explicitly rejecting minimum price move requirements, including 'No spike_min_price_move increases (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets (TB-210,213,216-219,248-251,265-270,271-273,274-277,278-283 rejected)' and 'No 5-minute/5-tick price persistence or sustained price deviation for lower-liquidity/high-freq/BTC 15m/crypto shorts/assets (TB-201,203,205,209,212,215,220-222 rejected)'. This introduces a price movement filter previously rejected to avoid filtering valid volume-based spikes in low-liquidity BTC 15m markets.
- [ ] **TB-285** `rejected` — For sports winner markets, increase volΔ multiplier to 1.5x baseline.
  - **Governor rejection**: The proposed tweak requires priceΔ > 0.02 for whale-cluster signals (unless volΔ >50x baseline), which directly conflicts with multiple historical constraints explicitly rejecting minimum price move requirements, including 'No spike_min_price_move increases (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets (TB-210,213,216-219,248-251,265-270,271-273,274-277,278-283 rejected)' and 'No 5-minute/5-tick price persistence or sustained price deviation for lower-liquidity/high-freq/BTC 15m/crypto shorts/assets (TB-201,203,205,209,212,215,220-222 rejected)'. This introduces a price movement filter previously rejected to avoid filtering valid volume-based spikes in low-liquidity BTC 15m markets.
- [ ] **TB-286** `rejected` — Add notional-value minimum ($500+) or 2.5x baseline volΔ for low-liquidity, short-dated watch-tier signals.
  - **Governor rejection**: The proposed tweak requires priceΔ > 0.02 for whale-cluster signals (unless volΔ >50x baseline), which directly conflicts with multiple historical constraints explicitly rejecting minimum price move requirements, including 'No spike_min_price_move increases (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets (TB-210,213,216-219,248-251,265-270,271-273,274-277,278-283 rejected)' and 'No 5-minute/5-tick price persistence or sustained price deviation for lower-liquidity/high-freq/BTC 15m/crypto shorts/assets (TB-201,203,205,209,212,215,220-222 rejected)'. This introduces a price movement filter previously rejected to avoid filtering valid volume-based spikes in low-liquidity BTC 15m markets.

---

## 2026-04-12 — Advisor snapshot 94

### Summary
False positives dominate in low-price-move whale-cluster signals on 15-min BTC markets and routine volume spikes in sports markets, often lacking price impact or predictive content despite high scores.

### Next step
Require minimum price move >0.01 for all whale-cluster signals and raise volume delta multiplier to 1.5x baseline for sports markets.

### Suggested thresholds
`min_price_move` → `0.015`

### Recommendations

- [ ] **TB-287** `rejected` — Raise whale-cluster volume delta threshold to 0.5x baseline for 15-min BTC markets.
  - **Governor rejection**: The proposed tweak requires a minimum price move >0.01 (specifically min_price_move: 0.015) for whale-cluster signals on 15m BTC markets, which directly conflicts with historical constraint '**No spike_min_price_move increases** (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets (TB-210,213,216-219,248-251,265-270,271-273,274-277,278-283,284-286 rejected)'. This is an explicit rejection of raising the minimum price move threshold.
- [ ] **TB-288** `rejected` — Require volume >25% baseline or price move >0.02 for 15-min markets.
  - **Governor rejection**: The proposed tweak requires a minimum price move >0.01 (specifically min_price_move: 0.015) for whale-cluster signals on 15m BTC markets, which directly conflicts with historical constraint '**No spike_min_price_move increases** (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets (TB-210,213,216-219,248-251,265-270,271-273,274-277,278-283,284-286 rejected)'. This is an explicit rejection of raising the minimum price move threshold.
- [ ] **TB-289** `rejected` — Add notional-value minimum ($500+) for low-liquidity, short-dated watch-tier signals.
  - **Governor rejection**: The proposed tweak requires a minimum price move >0.01 (specifically min_price_move: 0.015) for whale-cluster signals on 15m BTC markets, which directly conflicts with historical constraint '**No spike_min_price_move increases** (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets (TB-210,213,216-219,248-251,265-270,271-273,274-277,278-283,284-286 rejected)'. This is an explicit rejection of raising the minimum price move threshold.

---

## 2026-04-12 — Advisor snapshot 95

### Summary
False positives dominate in whale-cluster signals on low-volume 15-minute BTC markets with high volΔ but zero or minimal price moves, and in watch-tier sports/politics markets where routine liquidity or small trades trigger alerts without predictive impact.

### Next step
Require minimum price movement >0.01 for all tiers and raise volume delta thresholds tier/market-specifically to filter price-neutral noise.

### Suggested thresholds
`min_price_move` → `0.015`

### Recommendations

- [ ] **TB-290** `rejected` — For whale-cluster on 15-min BTC: require priceΔ >0.02 or volΔ >0.25x baseline, and filter midprice (yes~0.5) spikes with zero price impact
  - **Governor rejection**: The proposed tweak violates multiple historical constraints by introducing a minimum price movement requirement (>0.01 or 0.015) that was explicitly rejected: 'No spike_min_price_move increases (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets (TB-210,213,216-219,248-251,265-270,271-273,274-277,278-283,284-286 rejected)' and 'No 5-minute/5-tick price persistence or sustained price deviation for lower-liquidity/high-freq/BTC 15m/crypto shorts/assets (TB-201,203,205,209,212,215,220-222 rejected)'. This adds a price move filter to address false positives in low-volume 15m BTC markets, directly conflicting with prior rejections aimed at preserving sensitivity without price thresholds.
- [ ] **TB-291** `rejected` — For watch-tier sports winner markets: volΔ multiplier >=1.5x baseline
  - **Governor rejection**: The proposed tweak violates multiple historical constraints by introducing a minimum price movement requirement (>0.01 or 0.015) that was explicitly rejected: 'No spike_min_price_move increases (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets (TB-210,213,216-219,248-251,265-270,271-273,274-277,278-283,284-286 rejected)' and 'No 5-minute/5-tick price persistence or sustained price deviation for lower-liquidity/high-freq/BTC 15m/crypto shorts/assets (TB-201,203,205,209,212,215,220-222 rejected)'. This adds a price move filter to address false positives in low-volume 15m BTC markets, directly conflicting with prior rejections aimed at preserving sensitivity without price thresholds.
- [ ] **TB-292** `rejected` — For low-liquidity short-dated watch markets: add $500 notional minimum or volΔ >2.5x baseline
  - **Governor rejection**: The proposed tweak violates multiple historical constraints by introducing a minimum price movement requirement (>0.01 or 0.015) that was explicitly rejected: 'No spike_min_price_move increases (e.g., to 0.01/0.02/0.03/0.05) for BTC 15m/high-freq markets (TB-210,213,216-219,248-251,265-270,271-273,274-277,278-283,284-286 rejected)' and 'No 5-minute/5-tick price persistence or sustained price deviation for lower-liquidity/high-freq/BTC 15m/crypto shorts/assets (TB-201,203,205,209,212,215,220-222 rejected)'. This adds a price move filter to address false positives in low-volume 15m BTC markets, directly conflicting with prior rejections aimed at preserving sensitivity without price thresholds.

---

## 2026-04-12 — Advisor snapshot 96

### Summary
Your detector is generating high-volume false positives on whale-cluster tier signals with zero or minimal price moves (priceΔ=0.0), despite moderate-to-high conviction scores. Volume alone is insufficient to confirm genuine informed flow when price impact is absent.

### Next step
Implement a price-move floor for whale-cluster signals: require priceΔ ≥ 0.01 (1%) minimum, or add a joint constraint that ties score threshold to price impact (higher score requirement when priceΔ is near zero).

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-293** `rejected` — For whale-cluster tier: reject signals where priceΔ = 0.0 unless score exceeds 15.0, filtering the 8.0-score cluster noise while preserving genuine whale repositioning that moves price.
  - **Governor rejection**: The proposed tweak violates the historical constraint '**No spike_min_price_move increases** (e.g. to 0.01/0.02/0.03/0.05/0.015) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-270,271-273,274-277,278-283,284-286,287-290 rejected)'. Setting min_price_move: 0.01 directly implements a price-move floor of 1% for whale-cluster signals, which was explicitly rejected multiple times to avoid restricting detections in these markets.
- [ ] **TB-294** `rejected` — For watch-tier short-dated/low-liquidity markets (KXTRUMPSAY, KXNBAGAME): enforce notional-value minimum of $500+ or require volΔ ≥ 2.5x baseline to exclude routine small trades misidentified as spikes.
  - **Governor rejection**: The proposed tweak violates the historical constraint '**No spike_min_price_move increases** (e.g. to 0.01/0.02/0.03/0.05/0.015) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-270,271-273,274-277,278-283,284-286,287-290 rejected)'. Setting min_price_move: 0.01 directly implements a price-move floor of 1% for whale-cluster signals, which was explicitly rejected multiple times to avoid restricting detections in these markets.
- [ ] **TB-295** `rejected` — Add market-specific volume-delta multipliers: sports winner markets (KXNBAGAME) require 1.5x baseline; crypto 15-min bars tolerate 1.0x; apply conservatively to low-notional contracts approaching expiry.
  - **Governor rejection**: The proposed tweak violates the historical constraint '**No spike_min_price_move increases** (e.g. to 0.01/0.02/0.03/0.05/0.015) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-270,271-273,274-277,278-283,284-286,287-290 rejected)'. Setting min_price_move: 0.01 directly implements a price-move floor of 1% for whale-cluster signals, which was explicitly rejected multiple times to avoid restricting detections in these markets.

---

## 2026-04-12 — Advisor snapshot 97

### Summary
Multiple whale-cluster signals on KXBTC15M with low or no price moves (0.0-0.01) are mixed (some true signals, many false), while watch-tier signals in sports and low-liquidity markets trigger false positives from routine volume or small trades despite notes suggesting category-specific filters.

### Next step
Introduce tier-specific or market-category volume multipliers (e.g., 1.5x for sports, 2.5x for low-liquidity short-dated) to filter noise without global threshold hikes.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-296** `rejected` — Require priceΔ >= 0.02 for whale-cluster tier to eliminate no-move false positives.
  - **Governor rejection**: The proposed tweak introduces market-category or tier-specific volume multipliers (1.5x for sports, 2.5x for low-liquidity), which directly violates the historical constraint: 'No market-type-specific volume delta multipliers (e.g. 1-10x/1-2%/0.5x/1.5x/2x/2.5x/5-10x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m (TB-220,221,232,234,235,237,244-247,250,278,285,291,295 rejected).' The recommendation explicitly proposes category-specific multipliers that were previously rejected across 15+ test batches (TB-220, TB-221, TB-232, TB-234, TB-235, TB-237, TB-244–247, TB-250, TB-278, TB-285, TB-291, TB-295). Additionally, the proposed min_price_move of 0.02 for BTC 15m whale-cluster markets conflicts with: 'No spike_min_price_move increases (e.g. to 0.01/0.015/0.02/0.03/0.05) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295 rejected),' which explicitly rejects 0.02 threshold increases for this asset class and signal tier.
- [ ] **TB-297** `rejected` — Add notional-value minimum ($500+) for watch-tier low-liquidity markets.
  - **Governor rejection**: The proposed tweak introduces market-category or tier-specific volume multipliers (1.5x for sports, 2.5x for low-liquidity), which directly violates the historical constraint: 'No market-type-specific volume delta multipliers (e.g. 1-10x/1-2%/0.5x/1.5x/2x/2.5x/5-10x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m (TB-220,221,232,234,235,237,244-247,250,278,285,291,295 rejected).' The recommendation explicitly proposes category-specific multipliers that were previously rejected across 15+ test batches (TB-220, TB-221, TB-232, TB-234, TB-235, TB-237, TB-244–247, TB-250, TB-278, TB-285, TB-291, TB-295). Additionally, the proposed min_price_move of 0.02 for BTC 15m whale-cluster markets conflicts with: 'No spike_min_price_move increases (e.g. to 0.01/0.015/0.02/0.03/0.05) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295 rejected),' which explicitly rejects 0.02 threshold increases for this asset class and signal tier.
- [ ] **TB-298** `rejected` — Raise volΔ multiplier to 1.5x baseline for sports winner markets like KXNBAGAME.
  - **Governor rejection**: The proposed tweak introduces market-category or tier-specific volume multipliers (1.5x for sports, 2.5x for low-liquidity), which directly violates the historical constraint: 'No market-type-specific volume delta multipliers (e.g. 1-10x/1-2%/0.5x/1.5x/2x/2.5x/5-10x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m (TB-220,221,232,234,235,237,244-247,250,278,285,291,295 rejected).' The recommendation explicitly proposes category-specific multipliers that were previously rejected across 15+ test batches (TB-220, TB-221, TB-232, TB-234, TB-235, TB-237, TB-244–247, TB-250, TB-278, TB-285, TB-291, TB-295). Additionally, the proposed min_price_move of 0.02 for BTC 15m whale-cluster markets conflicts with: 'No spike_min_price_move increases (e.g. to 0.01/0.015/0.02/0.03/0.05) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295 rejected),' which explicitly rejects 0.02 threshold increases for this asset class and signal tier.

---

## 2026-04-12 — Advisor snapshot 98

### Summary
False positives dominate in thin golf props, sports winner markets, low-liquidity short-dated events, and BTC whale-clusters with minimal or no price moves despite volume deltas; genuine signals show stronger price moves and high conviction.

### Next step
Raise volume delta multiplier to 1.5x+ baseline globally and require price move >=0.03 for watch-tier signals.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-299** `planned` — For thin golf prop markets: volume delta >=1.5x baseline + >=5 trades in window
- [ ] **TB-300** `planned` — For sports winner markets: volume delta >=1.5x baseline
- [ ] **TB-301** `planned` — For low-liquidity short-dated markets: add $500+ notional value min or 2.5x volume baseline
- [ ] **TB-302** `planned` — For whale-cluster BTC: require priceΔ >=0.02

---

## 2026-04-12 — Advisor snapshot 99

### Summary
False positives are prevalent in thin/illiquid markets (golf props, sports winners, low-liq short-dated) from routine positioning or small trades causing % spikes, and in whale-clusters with no price move; true signals show stronger price moves and high conviction.

### Next step
Raise volume delta multiplier to 1.5x+ for watch-tier/thin markets and add min trades (5+) requirement.

### Suggested thresholds
`min_price_move` → `0.02`

### Recommendations

- [ ] **TB-303** `rejected` — For thin golf prop/sports winner markets: volume delta 1.5x baseline + 5+ trades in window.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **No spike_min_price_move increases** (TB-210,213,216-219,248-251,265-273,274-295,296 rejected) by adding min_price_move: 0.02, which is an explicit increase rejected for BTC 15m/high-freq/whale-cluster markets; (2) **No market-type-specific volume delta multipliers** (e.g. 1.5x) for thin/low-liq/crypto/BTC 15m markets (TB-220,221,232,234,235,237,244-247,250,278,285,291,295-298 rejected) by raising volume delta multiplier to 1.5x+ specifically for watch-tier/thin markets; (3) Introduces 'min trades (5+)' requirement, conflicting with **No minimum notional trade size filter** (TB-199,204,206,265-267,276-283,286,289,294,297,280 rejected) and **No combined priceΔ/volΔ filters** (TB-255,256,257) patterns for low-volume/thin/15m BTC markets.
- [ ] **TB-304** `rejected` — For whale-cluster: require priceΔ >= 0.02 to filter no-move false positives.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **No spike_min_price_move increases** (TB-210,213,216-219,248-251,265-273,274-295,296 rejected) by adding min_price_move: 0.02, which is an explicit increase rejected for BTC 15m/high-freq/whale-cluster markets; (2) **No market-type-specific volume delta multipliers** (e.g. 1.5x) for thin/low-liq/crypto/BTC 15m markets (TB-220,221,232,234,235,237,244-247,250,278,285,291,295-298 rejected) by raising volume delta multiplier to 1.5x+ specifically for watch-tier/thin markets; (3) Introduces 'min trades (5+)' requirement, conflicting with **No minimum notional trade size filter** (TB-199,204,206,265-267,276-283,286,289,294,297,280 rejected) and **No combined priceΔ/volΔ filters** (TB-255,256,257) patterns for low-volume/thin/15m BTC markets.
- [ ] **TB-305** `rejected` — For low-liq short-dated: add $500+ notional min or 2.5x volume baseline.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **No spike_min_price_move increases** (TB-210,213,216-219,248-251,265-273,274-295,296 rejected) by adding min_price_move: 0.02, which is an explicit increase rejected for BTC 15m/high-freq/whale-cluster markets; (2) **No market-type-specific volume delta multipliers** (e.g. 1.5x) for thin/low-liq/crypto/BTC 15m markets (TB-220,221,232,234,235,237,244-247,250,278,285,291,295-298 rejected) by raising volume delta multiplier to 1.5x+ specifically for watch-tier/thin markets; (3) Introduces 'min trades (5+)' requirement, conflicting with **No minimum notional trade size filter** (TB-199,204,206,265-267,276-283,286,289,294,297,280 rejected) and **No combined priceΔ/volΔ filters** (TB-255,256,257) patterns for low-volume/thin/15m BTC markets.

---

## 2026-04-12 — Advisor snapshot 100

### Summary
False positives dominate in thin sports props (e.g., golf rounds, NBA games) and low-liquidity short-dated markets from routine positioning or small trades causing percentage spikes without predictive power; BTC whale-clusters trigger reliably on score/volume but lack price movement confirmation.

### Next step
Introduce market-type tiered volume multipliers (e.g., 1.5x+ for sports props/watch tier) and minimum trade count (5+ in window) to filter noise while preserving high-conviction flow.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-306** `planned` — Raise volume delta multiplier to 1.5x baseline for sports winner/prop markets (golf, NBA) to cut pre-event positioning noise.
- [ ] **TB-307** `planned` — Require minimum 5 trades in recent window for watch-tier signals in thin markets.
- [ ] **TB-308** `planned` — Add notional-value minimum ($500+) or 2.5x volume baseline for low-liquidity short-dated markets approaching resolution.
- [ ] **TB-309** `planned` — Enforce min_price_move 0.03+ for whale-cluster signals without price delta confirmation.

---

## 2026-04-12 — Advisor snapshot 101

### Summary
False positives dominate in thin golf prop markets and sports winner markets from routine pre-event positioning and liquidity noise, despite low price moves (~0.02); whale-cluster BTC signals trigger frequently without price movement and are mostly noise.

### Next step
Raise volume delta multiplier to 1.5x+ for thin/low-liquidity markets (e.g., golf props, sports winners) and require minimum 5 trades in detection window.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-310** `rejected` — For golf prop and sports winner markets: increase volΔ multiplier from 1.2x/1.0x to 1.5x baseline.
  - **Governor rejection**: The proposed tweak raises the volume delta multiplier to 1.5x+ for thin/low-liquidity markets (e.g., golf props, sports winners), which directly conflicts with historical constraint 'No market-type-specific volume delta multipliers (e.g., 1-10x/1-2%/0.5x/1.5x/2x/2.5x/5-10x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m (TB-220,221,232,234,235,237,244-247,250,278,285,291,295-298,303,305 rejected)'. This introduces a market-specific multiplier explicitly rejected in prior tuning decisions.
- [ ] **TB-311** `rejected` — Require at least 5 trades in recent window for watch-tier signals to filter pre-event noise.
  - **Governor rejection**: The proposed tweak raises the volume delta multiplier to 1.5x+ for thin/low-liquidity markets (e.g., golf props, sports winners), which directly conflicts with historical constraint 'No market-type-specific volume delta multipliers (e.g., 1-10x/1-2%/0.5x/1.5x/2x/2.5x/5-10x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m (TB-220,221,232,234,235,237,244-247,250,278,285,291,295-298,303,305 rejected)'. This introduces a market-specific multiplier explicitly rejected in prior tuning decisions.
- [ ] **TB-312** `rejected` — Raise min_price_move to 0.03 for whale-cluster signals with volΔ <1000 to mute no-move triggers.
  - **Governor rejection**: The proposed tweak raises the volume delta multiplier to 1.5x+ for thin/low-liquidity markets (e.g., golf props, sports winners), which directly conflicts with historical constraint 'No market-type-specific volume delta multipliers (e.g., 1-10x/1-2%/0.5x/1.5x/2x/2.5x/5-10x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m (TB-220,221,232,234,235,237,244-247,250,278,285,291,295-298,303,305 rejected)'. This introduces a market-specific multiplier explicitly rejected in prior tuning decisions.

---

## 2026-04-12 — Advisor snapshot 102

### Summary
Your detector is generating false positives in low-liquidity markets (thin golf props, BTC 15m clusters) where volume spikes occur without meaningful price movement or genuine information flow. Whale positioning and pre-event activity are triggering signals that analysts label as false despite high scores.

### Next step
Implement a price-move floor that scales inversely with market liquidity tier: require minimum 0.03 (3%) price delta for watch-tier thin markets, 0.02 for whale-cluster tiers. Decouple volume signals from conviction scoring when price movement is absent or negligible.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-313** `planned` — For watch-tier thin markets (golf props): raise spike_min_volume_delta multiplier from 1.2x to 1.5x and enforce minimum 5+ trades in recent window before emitting signal, as noted in analyst feedback on KXPGAROUNDSCORE-MAST26R4-XSCH70.
- [ ] **TB-314** `planned` — For whale-cluster tiers (BTC 15m): filter out signals where priceΔ ≤ 0.01 regardless of volume or score; all four BTC whale signals show zero or negligible price movement despite high scores (8.0–18.66), indicating positioning noise rather than directional conviction.
- [ ] **TB-315** `planned` — Require price-movement confirmation for low-conviction markets: set a rule that score ≥ 6.0 demands priceΔ ≥ 0.03, and score < 6.0 demands either priceΔ ≥ 0.02 OR yes-probability ≥ 0.40 to reduce false positives in uncertain tiers.

---

## 2026-04-12 — Advisor snapshot 103

### Summary
False positives dominate in thin golf prop markets from normal pre-event volume spikes despite small price moves, and in whale-cluster detections on BTC markets with zero price change despite volume delta.

### Next step
Raise volume delta multiplier to 1.5x+ for thin prop markets and require 5+ trades in detection window; globally require minimum price move >0.01 for whale-cluster tiers.

### Suggested thresholds
`min_price_move` → `0.01`, `score_threshold` → `3.0`

### Recommendations

- [ ] **TB-316** `rejected` — For golf/thin prop markets: increase spike_min_volume_delta multiplier from 1.2x to 1.5x and add min_trades=5 filter
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) 'No spike_min_price_move increases (e.g., to 0.01/0.015/0.02/0.03/0.05) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305 rejected)' by globally requiring minimum price move >0.01 (min_price_move: 0.01) for whale-cluster tiers, which directly conflicts with explicitly rejected increases to 0.01 for BTC 15m/whale-cluster; (2) 'No market-type-specific volume delta multipliers (e.g., 1-10x/1-2%/0.5x/1.5x/2x/2.5x/5-10x baseline) for low-liq/pre-game/golf props/.../BTC 15m/thin markets (TB-220,221,232,234,235,237,244-247,250,278,285,291,295-298,303,305,310 rejected)' by raising volume delta multiplier to 1.5x+ specifically for thin prop markets (e.g., golf), which is an explicitly rejected market-type-specific multiplier.
- [ ] **TB-317** `rejected` — For whale-cluster signals: set spike_min_price_move >=0.01 to filter zero-move false positives
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) 'No spike_min_price_move increases (e.g., to 0.01/0.015/0.02/0.03/0.05) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305 rejected)' by globally requiring minimum price move >0.01 (min_price_move: 0.01) for whale-cluster tiers, which directly conflicts with explicitly rejected increases to 0.01 for BTC 15m/whale-cluster; (2) 'No market-type-specific volume delta multipliers (e.g., 1-10x/1-2%/0.5x/1.5x/2x/2.5x/5-10x baseline) for low-liq/pre-game/golf props/.../BTC 15m/thin markets (TB-220,221,232,234,235,237,244-247,250,278,285,291,295-298,303,305,310 rejected)' by raising volume delta multiplier to 1.5x+ specifically for thin prop markets (e.g., golf), which is an explicitly rejected market-type-specific multiplier.
- [ ] **TB-318** `rejected` — Raise spike_score_threshold to 3.0 to suppress low-score watch-tier signals unless high conviction
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) 'No spike_min_price_move increases (e.g., to 0.01/0.015/0.02/0.03/0.05) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305 rejected)' by globally requiring minimum price move >0.01 (min_price_move: 0.01) for whale-cluster tiers, which directly conflicts with explicitly rejected increases to 0.01 for BTC 15m/whale-cluster; (2) 'No market-type-specific volume delta multipliers (e.g., 1-10x/1-2%/0.5x/1.5x/2x/2.5x/5-10x baseline) for low-liq/pre-game/golf props/.../BTC 15m/thin markets (TB-220,221,232,234,235,237,244-247,250,278,285,291,295-298,303,305,310 rejected)' by raising volume delta multiplier to 1.5x+ specifically for thin prop markets (e.g., golf), which is an explicitly rejected market-type-specific multiplier.

---

## 2026-04-12 — Advisor snapshot 104

### Summary
False positives are prominent in thin markets like golf props from normal pre-event positioning despite low price moves, and whale-clusters trigger signals without price changes. Genuine signals show stronger price moves and high conviction flow.

### Next step
Require minimum trades in recent window and raise volume delta multiplier for thin/low-liquidity markets.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-319** `rejected` — For thin golf prop markets, raise volume delta multiplier from 1.2x to 1.5x+ and require 5+ trades in window.
  - **Governor rejection**: The proposed tweak raises min_price_move to 0.03, which directly conflicts with the historical constraint 'No spike_min_price_move increases (e.g., to 0.01/0.015/0.02/0.03/0.05) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-318 rejected)'. This is an explicit rejection of increasing the minimum price move threshold, including to 0.03, for relevant markets like BTC 15m and whale-clusters.
- [ ] **TB-320** `rejected` — Increase min_price_move threshold to filter zero-change whale-clusters.
  - **Governor rejection**: The proposed tweak raises min_price_move to 0.03, which directly conflicts with the historical constraint 'No spike_min_price_move increases (e.g., to 0.01/0.015/0.02/0.03/0.05) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-318 rejected)'. This is an explicit rejection of increasing the minimum price move threshold, including to 0.03, for relevant markets like BTC 15m and whale-clusters.
- [ ] **TB-321** `rejected` — Tier score_threshold by market type, higher for watch/tier=watch.
  - **Governor rejection**: The proposed tweak raises min_price_move to 0.03, which directly conflicts with the historical constraint 'No spike_min_price_move increases (e.g., to 0.01/0.015/0.02/0.03/0.05) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-318 rejected)'. This is an explicit rejection of increasing the minimum price move threshold, including to 0.03, for relevant markets like BTC 15m and whale-clusters.

---

## 2026-04-12 — Advisor snapshot 105

### Summary
Your detector is generating false positives in thin markets (golf props) where normal pre-event positioning mimics spike behavior, and also flagging whale-cluster activity with zero price movement as signals despite lacking directional conviction.

### Next step
Implement market-structure-aware thresholds: require synchronized volume + price movement (not either/or), and add a minimum trade-count filter for low-liquidity markets to distinguish genuine flow from positioning noise.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-322** `rejected` — For thin markets (golf props, niche events): raise spike_min_volume_delta multiplier to 1.5x+ and enforce minimum 5+ trades in detection window, as analyst noted this reduces false positives from normal pre-event activity
  - **Governor rejection**: The proposed tweak requires synchronized volume + price movement (min_price_move: 0.02), which directly conflicts with historical constraints TB-001, TB-002, TB-210 (applied) that maintain separate volume delta and score thresholds without mandating price movement for BTC 15m/whale-cluster markets, and rejected proposals TB-200,202,208,211,214,255-257,265-267,271-273,274-277,278-283,284-286,287-290,293-295,296-298 (no volume-to-price-move ratio threshold) and incomplete TB-XXX (no combined priceΔ/volΔ filters). It also introduces a market-type-specific filter (min trade-count for low-liquidity markets like golf props), violating rejected TB-220,221,232,234,235,237,244-247,250,278,285,291,295-298,303,305,310,316-319 (no market-type-specific volume delta multipliers or similar adjustments).
- [ ] **TB-323** `rejected` — Decouple volume and price signals: require BOTH volΔ > threshold AND priceΔ > threshold to emit a signal (reject the whale-cluster BTC signals where priceΔ=0.0 despite high volume)
  - **Governor rejection**: The proposed tweak requires synchronized volume + price movement (min_price_move: 0.02), which directly conflicts with historical constraints TB-001, TB-002, TB-210 (applied) that maintain separate volume delta and score thresholds without mandating price movement for BTC 15m/whale-cluster markets, and rejected proposals TB-200,202,208,211,214,255-257,265-267,271-273,274-277,278-283,284-286,287-290,293-295,296-298 (no volume-to-price-move ratio threshold) and incomplete TB-XXX (no combined priceΔ/volΔ filters). It also introduces a market-type-specific filter (min trade-count for low-liquidity markets like golf props), violating rejected TB-220,221,232,234,235,237,244-247,250,278,285,291,295-298,303,305,310,316-319 (no market-type-specific volume delta multipliers or similar adjustments).
- [ ] **TB-324** `rejected` — Add market-tier adjustment: apply stricter thresholds to 'watch' tier (0.02 price moves in thin props) while allowing 'high conviction flow' tier slightly lower thresholds if price movement is confirmed
  - **Governor rejection**: The proposed tweak requires synchronized volume + price movement (min_price_move: 0.02), which directly conflicts with historical constraints TB-001, TB-002, TB-210 (applied) that maintain separate volume delta and score thresholds without mandating price movement for BTC 15m/whale-cluster markets, and rejected proposals TB-200,202,208,211,214,255-257,265-267,271-273,274-277,278-283,284-286,287-290,293-295,296-298 (no volume-to-price-move ratio threshold) and incomplete TB-XXX (no combined priceΔ/volΔ filters). It also introduces a market-type-specific filter (min trade-count for low-liquidity markets like golf props), violating rejected TB-220,221,232,234,235,237,244-247,250,278,285,291,295-298,303,305,310,316-319 (no market-type-specific volume delta multipliers or similar adjustments).

---

## 2026-04-12 — Advisor snapshot 106

### Summary
Recent signals show false positives in high-frequency BTC 15-minute markets from routine small-account activity (volΔ=14.86x) and thin golf prop markets from normal pre-event positioning (volΔ=8046x), while high conviction flow like TRUMP remains a true signal.

### Next step
Introduce market-type specific volume delta multipliers (e.g., higher for high-frequency and thin markets) to filter noise without impacting genuine flow.

### Recommendations

- [ ] **TB-325** `rejected` — Raise volume delta multiplier from 14.9x to 25x for high-frequency BTC 15-minute markets.
  - **Governor rejection**: The proposed tweak introduces market-type-specific volume delta multipliers (e.g., higher for high-frequency and thin markets), which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers (e.g., 1-10x/0.5x/1-2%/1.5x/2x/2.5x/5-10x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m/thin markets (TB-220,221,232,234,235...' as it explicitly rejects such multipliers for the exact market types mentioned in the proposal (high-frequency BTC 15m and thin golf prop markets).
- [ ] **TB-326** `rejected` — For thin golf prop markets, raise volume delta multiplier from 1.2x to 1.5x+ and require 5+ trades in recent window.
  - **Governor rejection**: The proposed tweak introduces market-type-specific volume delta multipliers (e.g., higher for high-frequency and thin markets), which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers (e.g., 1-10x/0.5x/1-2%/1.5x/2x/2.5x/5-10x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m/thin markets (TB-220,221,232,234,235...' as it explicitly rejects such multipliers for the exact market types mentioned in the proposal (high-frequency BTC 15m and thin golf prop markets).
- [ ] **TB-327** `rejected` — Monitor priceΔ consistency with volΔ for high conviction signals to avoid muting medium/high impact events.
  - **Governor rejection**: The proposed tweak introduces market-type-specific volume delta multipliers (e.g., higher for high-frequency and thin markets), which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers (e.g., 1-10x/0.5x/1-2%/1.5x/2x/2.5x/5-10x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m/thin markets (TB-220,221,232,234,235...' as it explicitly rejects such multipliers for the exact market types mentioned in the proposal (high-frequency BTC 15m and thin golf prop markets).

---

## 2026-04-12 — Advisor snapshot 107

### Summary
False positives are occurring in high-frequency BTC 15-minute markets and thin golf prop markets due to routine small-account activity and normal pre-event positioning, despite low price moves (1-2%) and moderate scores.

### Next step
Introduce market-type-specific volume delta multipliers (e.g., higher for high-frequency BTC and thin prop markets) to filter noise without impacting high-conviction flow.

### Recommendations

- [ ] **TB-328** `rejected` — Raise volume delta multiplier from 14.9x to 25x for high-frequency BTC 15-minute markets.
  - **Governor rejection**: The proposed tweak introduces market-type-specific volume delta multipliers (e.g., higher for high-frequency BTC and thin prop markets), which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers (e.g., 1-10x/0.5x/1-2%/1.5x/2x/2.5x/5-10x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m/thin markets (TB-220,221,232,234,235,237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-327 rejected)'. This was explicitly rejected multiple times to prevent regressions.
- [ ] **TB-329** `rejected` — For thin golf prop markets, raise volume delta multiplier from 1.2x to 1.5x+ and require 5+ trades in recent window.
  - **Governor rejection**: The proposed tweak introduces market-type-specific volume delta multipliers (e.g., higher for high-frequency BTC and thin prop markets), which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers (e.g., 1-10x/0.5x/1-2%/1.5x/2x/2.5x/5-10x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m/thin markets (TB-220,221,232,234,235,237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-327 rejected)'. This was explicitly rejected multiple times to prevent regressions.
- [ ] **TB-330** `rejected` — Consider minimum trades threshold globally for low-price-move detections (under 3%).
  - **Governor rejection**: The proposed tweak introduces market-type-specific volume delta multipliers (e.g., higher for high-frequency BTC and thin prop markets), which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers (e.g., 1-10x/0.5x/1-2%/1.5x/2x/2.5x/5-10x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m/thin markets (TB-220,221,232,234,235,237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-327 rejected)'. This was explicitly rejected multiple times to prevent regressions.

---

## 2026-04-12 — Advisor snapshot 108

### Summary
Your detector is generating false positives in thin markets (golf props, high-frequency BTC) where normal positioning and small-account activity trigger signals despite low genuine alpha. Meanwhile, genuinely informative flow (high conviction TRUMP signal with 5% price move) is being captured correctly.

### Next step
Implement market-segment-specific thresholds: require higher volume delta multipliers for thin/illiquid markets (1.5x–25x depending on typical liquidity) and minimum trade-count filters to distinguish algorithmic noise from intentional flow.

### Recommendations

- [ ] **TB-331** `planned` — For high-frequency BTC 15m markets: raise volume delta multiplier threshold to 25x (from 14.9x) to filter routine small-account activity, as noted in analyst feedback
- [ ] **TB-332** `planned` — For thin prop markets (golf, niche political): raise volume delta multiplier to 1.5x–2.0x and require minimum 5+ trades in recent window before emitting signal
- [ ] **TB-333** `planned` — Segment detectors by market liquidity tier: apply stricter thresholds to low-liquidity markets and looser thresholds to high-volume markets to reduce false positives without muting alpha

---

## 2026-04-12 — Advisor snapshot 109

### Summary
False positives are prominent in high-frequency BTC 15-minute markets from routine small-account activity and thin golf prop markets due to low volume delta multipliers and insufficient trade requirements, while genuine signals occur with higher volume deltas and price moves.

### Next step
Introduce market-type specific volume delta multipliers: 25x for high-frequency BTC markets and 1.5x+ for thin prop markets.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-334** `rejected` — Raise volume delta multiplier threshold from 14.9x to 25x for high-frequency BTC 15-minute markets.
  - **Governor rejection**: The proposed tweak violates TB-220, TB-221, TB-232-TB-237, TB-244-TB-247, TB-250, TB-278, TB-285, TB-291, TB-295-TB-298, which explicitly rejected market-type-specific volume delta multipliers (including the proposed 25x for high-frequency BTC markets and 1.5x+ for thin prop markets). The historical constraint states: 'No market-type-specific volume delta multipliers (e.g., 0.5x/1-10x/1-2%/1.5x/2x/2.5x/5-10x/14.9x→25x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m/thin markets.' The proposed 25x multiplier for BTC 15m and 1.5x+ for golf props directly contradicts this blanket rejection across all listed market categories and multiplier ranges.
- [ ] **TB-335** `rejected` — For thin golf prop markets, raise volume delta multiplier from 1.2x to 1.5x+ and require at least 5 trades in the recent window.
  - **Governor rejection**: The proposed tweak violates TB-220, TB-221, TB-232-TB-237, TB-244-TB-247, TB-250, TB-278, TB-285, TB-291, TB-295-TB-298, which explicitly rejected market-type-specific volume delta multipliers (including the proposed 25x for high-frequency BTC markets and 1.5x+ for thin prop markets). The historical constraint states: 'No market-type-specific volume delta multipliers (e.g., 0.5x/1-10x/1-2%/1.5x/2x/2.5x/5-10x/14.9x→25x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m/thin markets.' The proposed 25x multiplier for BTC 15m and 1.5x+ for golf props directly contradicts this blanket rejection across all listed market categories and multiplier ranges.
- [ ] **TB-336** `rejected` — Consider tier-specific score thresholds to filter watch-tier signals with low price moves.
  - **Governor rejection**: The proposed tweak violates TB-220, TB-221, TB-232-TB-237, TB-244-TB-247, TB-250, TB-278, TB-285, TB-291, TB-295-TB-298, which explicitly rejected market-type-specific volume delta multipliers (including the proposed 25x for high-frequency BTC markets and 1.5x+ for thin prop markets). The historical constraint states: 'No market-type-specific volume delta multipliers (e.g., 0.5x/1-10x/1-2%/1.5x/2x/2.5x/5-10x/14.9x→25x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m/thin markets.' The proposed 25x multiplier for BTC 15m and 1.5x+ for golf props directly contradicts this blanket rejection across all listed market categories and multiplier ranges.

---

## 2026-04-12 — Advisor snapshot 110

### Summary
Your detector is flagging high-volume moves with minimal price action as signals, particularly in thin markets (golf props, BTC 15M). Volume alone without price confirmation creates false positives, especially when large single accounts can move prediction market prices through concentrated positions.

### Next step
Implement market-structure-aware thresholds: require price move confirmation (minimum 2-3%) for high-volume signals in thin markets, and add a trades-count requirement to distinguish genuine flow from single-account positioning.

### Suggested thresholds
`min_price_move` → `0.02`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-337** `rejected` — For BTC 15M markets: raise volume delta multiplier threshold to 25x as noted, filtering routine small-account activity
  - **Governor rejection**: The proposed tweak sets min_price_move: 0.02, which directly conflicts with historical constraint 'No spike_min_price_move increases (e.g., to 0.01/0.015/0.02/0.03/0.05) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322 rejected)'. This introduces a minimum price move threshold of 0.02 that was explicitly rejected multiple times to avoid tightening filters in these markets. Additionally, it conflicts with 'No 5-minute/5-tick price persistence or sustained price deviation for lower-liquidity/high-freq/BTC 15m/crypto shorts/assets (TB-201,203,205,209,212,215,220-222 rejected)' and 'No combined priceΔ/volΔ filters' constraints, as it adds price move confirmation (2%) for high-volume signals in thin markets including BTC 15m.
- [ ] **TB-338** `rejected` — For thin prop markets (golf, similar): require volΔ × priceΔ joint confirmation—e.g., volΔ ≥ 5000 AND priceΔ ≥ 0.02 simultaneously, plus minimum 5+ trades in window
  - **Governor rejection**: The proposed tweak sets min_price_move: 0.02, which directly conflicts with historical constraint 'No spike_min_price_move increases (e.g., to 0.01/0.015/0.02/0.03/0.05) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322 rejected)'. This introduces a minimum price move threshold of 0.02 that was explicitly rejected multiple times to avoid tightening filters in these markets. Additionally, it conflicts with 'No 5-minute/5-tick price persistence or sustained price deviation for lower-liquidity/high-freq/BTC 15m/crypto shorts/assets (TB-201,203,205,209,212,215,220-222 rejected)' and 'No combined priceΔ/volΔ filters' constraints, as it adds price move confirmation (2%) for high-volume signals in thin markets including BTC 15m.
- [ ] **TB-339** `rejected` — Add insider-positioning risk flag: when volΔ is high but priceΔ is near-zero, lower signal tier or require external cross-market confirmation before emitting, as concentrated positions can artificially move thin markets without genuine information flow
  - **Governor rejection**: The proposed tweak sets min_price_move: 0.02, which directly conflicts with historical constraint 'No spike_min_price_move increases (e.g., to 0.01/0.015/0.02/0.03/0.05) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322 rejected)'. This introduces a minimum price move threshold of 0.02 that was explicitly rejected multiple times to avoid tightening filters in these markets. Additionally, it conflicts with 'No 5-minute/5-tick price persistence or sustained price deviation for lower-liquidity/high-freq/BTC 15m/crypto shorts/assets (TB-201,203,205,209,212,215,220-222 rejected)' and 'No combined priceΔ/volΔ filters' constraints, as it adds price move confirmation (2%) for high-volume signals in thin markets including BTC 15m.

---

## 2026-04-12 — Advisor snapshot 111

### Summary
High-frequency BTC 15-minute markets generate false positives from routine small-account activity despite low price moves, while other markets like TRUMPSAY and PGAROUNDSCORE produce true signals with moderate volume and price deltas.

### Next step
Introduce market-type specific volume delta multipliers, raising it to 25x for high-frequency BTC 15-minute markets.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `3.0`

### Recommendations

- [ ] **TB-340** `rejected` — Raise volume delta multiplier threshold from 14.9x to 25x for high-frequency BTC markets per analyst note.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume delta multipliers** (25x for high-frequency BTC 15-minute markets), which directly conflicts with the historical constraint 'No market-type-specific volΔ multipliers (e.g., .../25x baseline) for .../BTC 15m/... (TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336 rejected)'. This was explicitly rejected previously.
- [ ] **TB-341** `rejected` — Increase min_price_move to 0.03 to filter signals with minimal price impact like BTC cases.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume delta multipliers** (25x for high-frequency BTC 15-minute markets), which directly conflicts with the historical constraint 'No market-type-specific volΔ multipliers (e.g., .../25x baseline) for .../BTC 15m/... (TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336 rejected)'. This was explicitly rejected previously.
- [ ] **TB-342** `rejected` — Raise score_threshold to 3.0 to suppress low-score watch-tier signals unless accompanied by strong price move.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume delta multipliers** (25x for high-frequency BTC 15-minute markets), which directly conflicts with the historical constraint 'No market-type-specific volΔ multipliers (e.g., .../25x baseline) for .../BTC 15m/... (TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336 rejected)'. This was explicitly rejected previously.

---

## 2026-04-12 — Advisor snapshot 112

### Summary
False positives occur in low-liquidity golf markets with small price moves (2%) despite volume spikes, and in high-frequency BTC markets with routine small-account activity even at low volume deltas.

### Next step
Introduce market-type rules: higher price move threshold (>5%) for low-liquidity golf markets and volume delta multiplier >25x for high-frequency BTC markets.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-343** `rejected` — For final-round golf markets, require priceΔ >0.05 and weight volΔ by total liquidity.
  - **Governor rejection**: The proposed tweak violates TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339 rejected (No spike_min_price_move increases, e.g., to 0.01/0.015/0.02/0.03/0.05) for BTC 15m/high-freq/whale-cluster markets by setting min_price_move: 0.03 (a disallowed increase). It also violates No market-type-specific volume delta multipliers (e.g., .../14.9x→25x/...) for low-liq/pre-gam by introducing >25x multiplier for high-frequency BTC markets.
- [ ] **TB-344** `rejected` — Raise volume delta multiplier from 14.9x to 25x for BTC 15M markets.
  - **Governor rejection**: The proposed tweak violates TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339 rejected (No spike_min_price_move increases, e.g., to 0.01/0.015/0.02/0.03/0.05) for BTC 15m/high-freq/whale-cluster markets by setting min_price_move: 0.03 (a disallowed increase). It also violates No market-type-specific volume delta multipliers (e.g., .../14.9x→25x/...) for low-liq/pre-gam by introducing >25x multiplier for high-frequency BTC markets.
- [ ] **TB-345** `rejected` — Increase min_price_move to 0.03 globally to filter 2% moves.
  - **Governor rejection**: The proposed tweak violates TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339 rejected (No spike_min_price_move increases, e.g., to 0.01/0.015/0.02/0.03/0.05) for BTC 15m/high-freq/whale-cluster markets by setting min_price_move: 0.03 (a disallowed increase). It also violates No market-type-specific volume delta multipliers (e.g., .../14.9x→25x/...) for low-liq/pre-gam by introducing >25x multiplier for high-frequency BTC markets.

---

## 2026-04-12 — Advisor snapshot 113

### Summary
False positives occur in low-liquidity markets like final-round golf with small samples and minimal price moves (2%), despite volume spikes; zero price moves also trigger invalid signals.

### Next step
Weight volume spikes by total market liquidity and raise price move threshold to >5% for watch-tier alerts.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `2.5`

### Recommendations

- [ ] **TB-346** `rejected` — Require priceΔ > 0.05 (5%) to filter small moves in low-liquidity markets
  - **Governor rejection**: The proposed tweak raises min_price_move to 0.05 (5%), which directly conflicts with 'No spike_min_price_move increases (e.g. to 0.01/0.015/0.02/0.03/0.05; priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345 rejected)'. This is an explicit rejection of increasing the price move threshold to 0.05 or similar values.
- [ ] **TB-347** `rejected` — Incorporate market liquidity normalization for volΔ significance
  - **Governor rejection**: The proposed tweak raises min_price_move to 0.05 (5%), which directly conflicts with 'No spike_min_price_move increases (e.g. to 0.01/0.015/0.02/0.03/0.05; priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345 rejected)'. This is an explicit rejection of increasing the price move threshold to 0.05 or similar values.
- [ ] **TB-348** `rejected` — Raise score_threshold to 2.5+ to suppress borderline signals like score=2.033
  - **Governor rejection**: The proposed tweak raises min_price_move to 0.05 (5%), which directly conflicts with 'No spike_min_price_move increases (e.g. to 0.01/0.015/0.02/0.03/0.05; priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345 rejected)'. This is an explicit rejection of increasing the price move threshold to 0.05 or similar values.

---

## 2026-04-12 — Advisor snapshot 114

### Summary
Your detector is generating false positives on ultra-short-duration markets (15-min) and low-liquidity niche markets (golf, political) where volume spikes occur without meaningful price moves or genuine informational flow. The primary issue is that spike_min_price_move is too permissive for these asset classes.

### Next step
Implement asset-class or market-duration-specific price-move thresholds rather than a single global minimum. Ultra-short markets (≤15min) and low-liquidity niche markets require substantially higher price-move requirements (0.5%+ and 5%+ respectively) to filter noise.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-349** `rejected` — For 15-minute duration markets, raise spike_min_price_move to ≥0.5% to eliminate signals where volume spikes but price remains flat or near-flat (see KXBTC15M signals with priceΔ=0.0).
  - **Governor rejection**: The proposed tweak violates multiple historical constraints explicitly rejecting market-type-specific or duration-specific increases to **spike_min_price_move**, including: TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348 (no **spike_min_price_move increases** e.g., ≥0.01/0.015/0.02/0.03/0.05/priceΔ>0% for BTC 15m/high-freq/whale-cluster markets) and TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336,340,343-344 (no **market-type-specific volume delta multipliers** which parallels the rejected asset-class-specific adjustments here for ultra-short/15-min and low-liq niche markets like golf/political, proposing 0.5%+ and 5%+ **min_price_move** thresholds, directly conflicting with the preserved permissive global **spike_min_price_move**).
- [ ] **TB-350** `rejected` — For low-liquidity niche markets (golf, political events), require spike_min_price_move ≥5% and normalize volume_delta thresholds by market liquidity percentile to distinguish genuine information flow from thin-market noise.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints explicitly rejecting market-type-specific or duration-specific increases to **spike_min_price_move**, including: TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348 (no **spike_min_price_move increases** e.g., ≥0.01/0.015/0.02/0.03/0.05/priceΔ>0% for BTC 15m/high-freq/whale-cluster markets) and TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336,340,343-344 (no **market-type-specific volume delta multipliers** which parallels the rejected asset-class-specific adjustments here for ultra-short/15-min and low-liq niche markets like golf/political, proposing 0.5%+ and 5%+ **min_price_move** thresholds, directly conflicting with the preserved permissive global **spike_min_price_move**).
- [ ] **TB-351** `rejected` — For 'watch' tier signals specifically, consider a composite rule: reject signals where (priceΔ < asset_class_minimum AND yes_probability < 0.5), as these indicate analyst doubt paired with insufficient price conviction.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints explicitly rejecting market-type-specific or duration-specific increases to **spike_min_price_move**, including: TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348 (no **spike_min_price_move increases** e.g., ≥0.01/0.015/0.02/0.03/0.05/priceΔ>0% for BTC 15m/high-freq/whale-cluster markets) and TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336,340,343-344 (no **market-type-specific volume delta multipliers** which parallels the rejected asset-class-specific adjustments here for ultra-short/15-min and low-liq niche markets like golf/political, proposing 0.5%+ and 5%+ **min_price_move** thresholds, directly conflicting with the preserved permissive global **spike_min_price_move**).

---

## 2026-04-12 — Advisor snapshot 115

### Summary
False positives are prevalent in ultra-short-duration markets (e.g., 15M) with no price move and in final-round golf markets with small samples and modest price changes, despite volume spikes.

### Next step
Introduce market-specific price move requirements: >0.5% for 15M markets and >5% for final-round golf markets.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `3.7`

### Recommendations

- [ ] **TB-352** `rejected` — Require priceΔ >0.5% for 'watch' tier alerts on 15M markets to filter noise.
  - **Governor rejection**: The proposed tweak introduces a **min_price_move** threshold of 0.005 (>0.5%) for 15M markets, which directly conflicts with **TB-210,213,216-219,248-251,265-270,271-273,274-277,278-283,284-286,287-290,293-295,296-298,303-305,316-322,337-339,341,343-345,346-348,349-351 rejected** constraints explicitly rejecting any increases to spike_min_price_move (e.g., ≥0.01/0.015/0.02/0.03/0.05/0.5%/5%/priceΔ>0%) for BTC 15m/high-freq/whale-cluster scenarios. This sets a non-zero price move requirement previously rejected to avoid filtering valid volume spikes.
- [ ] **TB-353** `rejected` — For final-round golf markets, require priceΔ >0.05 and weight volΔ by total market liquidity.
  - **Governor rejection**: The proposed tweak introduces a **min_price_move** threshold of 0.005 (>0.5%) for 15M markets, which directly conflicts with **TB-210,213,216-219,248-251,265-270,271-273,274-277,278-283,284-286,287-290,293-295,296-298,303-305,316-322,337-339,341,343-345,346-348,349-351 rejected** constraints explicitly rejecting any increases to spike_min_price_move (e.g., ≥0.01/0.015/0.02/0.03/0.05/0.5%/5%/priceΔ>0%) for BTC 15m/high-freq/whale-cluster scenarios. This sets a non-zero price move requirement previously rejected to avoid filtering valid volume spikes.
- [ ] **TB-354** `rejected` — Raise spike_score_threshold to 3.7 to cull low-score watch signals.
  - **Governor rejection**: The proposed tweak introduces a **min_price_move** threshold of 0.005 (>0.5%) for 15M markets, which directly conflicts with **TB-210,213,216-219,248-251,265-270,271-273,274-277,278-283,284-286,287-290,293-295,296-298,303-305,316-322,337-339,341,343-345,346-348,349-351 rejected** constraints explicitly rejecting any increases to spike_min_price_move (e.g., ≥0.01/0.015/0.02/0.03/0.05/0.5%/5%/priceΔ>0%) for BTC 15m/high-freq/whale-cluster scenarios. This sets a non-zero price move requirement previously rejected to avoid filtering valid volume spikes.

---

## 2026-04-12 — Advisor snapshot 116

### Summary
False positives are prevalent in ultra-short-duration markets (e.g., 15M BTC) due to volume spikes without price movement and in low-liquidity final-round golf markets with insufficient price moves relative to small samples.

### Next step
Introduce market-specific dynamic thresholds: for 15M markets, require priceΔ >0.5%; for final-round golf, scale min_price_move to >5% or 2x total liquidity-adjusted volume significance.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `3.7`

### Recommendations

- [ ] **TB-355** `rejected` — Increase spike_min_price_move to 0.005 (0.5%) for all 'watch' tier alerts on 15M or ultra-short markets
  - **Governor rejection**: The proposed tweak introduces a min_price_move of 0.005 (0.5%) for 15M markets, which directly conflicts with historical constraint 'No spike_min_price_move increases (e.g., to 0.01/0.015/0.02/0.03/0.05/0.5%/5%; priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352 rejected)'. This sets a non-zero minimum price move threshold where previous tweaks to increase it were explicitly rejected. Additionally, the score_threshold of 3.7 likely relaxes the applied TB-002 constraint of spike_score_threshold ≥8.5.
- [ ] **TB-356** `rejected` — For low-liquidity markets (e.g., golf finals), weight volume delta by total market liquidity and require priceΔ >0.05
  - **Governor rejection**: The proposed tweak introduces a min_price_move of 0.005 (0.5%) for 15M markets, which directly conflicts with historical constraint 'No spike_min_price_move increases (e.g., to 0.01/0.015/0.02/0.03/0.05/0.5%/5%; priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352 rejected)'. This sets a non-zero minimum price move threshold where previous tweaks to increase it were explicitly rejected. Additionally, the score_threshold of 3.7 likely relaxes the applied TB-002 constraint of spike_score_threshold ≥8.5.
- [ ] **TB-357** `rejected` — Raise spike_score_threshold to 3.7 to filter low-price-move signals like BTC15M cases
  - **Governor rejection**: The proposed tweak introduces a min_price_move of 0.005 (0.5%) for 15M markets, which directly conflicts with historical constraint 'No spike_min_price_move increases (e.g., to 0.01/0.015/0.02/0.03/0.05/0.5%/5%; priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352 rejected)'. This sets a non-zero minimum price move threshold where previous tweaks to increase it were explicitly rejected. Additionally, the score_threshold of 3.7 likely relaxes the applied TB-002 constraint of spike_score_threshold ≥8.5.

---

## 2026-04-12 — Advisor snapshot 117

### Summary
False positives dominate in thin 15-minute crypto markets due to low baseline volumes amplifying minor trades and zero price moves, and in low-liquidity golf markets with insufficient price thresholds; genuine signals appear in some watch-tier events with moderate volume and price changes.

### Next step
Add market-specific minimum absolute volume thresholds (e.g., >100 contracts for crypto 15M, scaled by liquidity for others) and increase price move requirements for watch tier in thin markets.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-358** `rejected` — Require minimum absolute volume >100 contracts for 15M crypto to filter thin-market noise.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introduces 'market-specific minimum absolute volume thresholds (e.g., >100 contracts for crypto 15M)', conflicting with 'No minimum notional trade size filter (USD equiv., e.g., $500/$10k; TB-199,204,206,265-267,276-283,286,289,294,297,280 rejected)' and 'No market-type-specific volume delta multipliers (e.g., ... crypto/BTC 15m ...; TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336,340,343-344 rejected)' by adding market-specific volume filters previously rejected. (2) Sets 'min_price_move: 0.005', conflicting with 'No spike_min_price_move increases (e.g., ≥0.005/0.01/.../priceΔ>0%; TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected)' by raising the price move requirement, which was explicitly rejected to avoid tightening filters.
- [ ] **TB-359** `rejected` — Raise min_price_move to 0.005 for watch tier in 15M markets.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introduces 'market-specific minimum absolute volume thresholds (e.g., >100 contracts for crypto 15M)', conflicting with 'No minimum notional trade size filter (USD equiv., e.g., $500/$10k; TB-199,204,206,265-267,276-283,286,289,294,297,280 rejected)' and 'No market-type-specific volume delta multipliers (e.g., ... crypto/BTC 15m ...; TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336,340,343-344 rejected)' by adding market-specific volume filters previously rejected. (2) Sets 'min_price_move: 0.005', conflicting with 'No spike_min_price_move increases (e.g., ≥0.005/0.01/.../priceΔ>0%; TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected)' by raising the price move requirement, which was explicitly rejected to avoid tightening filters.
- [ ] **TB-360** `rejected` — For final-round golf markets, weight volΔ by total liquidity and require priceΔ >0.05.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introduces 'market-specific minimum absolute volume thresholds (e.g., >100 contracts for crypto 15M)', conflicting with 'No minimum notional trade size filter (USD equiv., e.g., $500/$10k; TB-199,204,206,265-267,276-283,286,289,294,297,280 rejected)' and 'No market-type-specific volume delta multipliers (e.g., ... crypto/BTC 15m ...; TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336,340,343-344 rejected)' by adding market-specific volume filters previously rejected. (2) Sets 'min_price_move: 0.005', conflicting with 'No spike_min_price_move increases (e.g., ≥0.005/0.01/.../priceΔ>0%; TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected)' by raising the price move requirement, which was explicitly rejected to avoid tightening filters.

---

## 2026-04-12 — Advisor snapshot 118

### Summary
False positives dominate in thin, short-duration markets like 15M crypto and final-round golf, where low baselines amplify minor volume and small price moves trigger alerts despite lacking informative signals.

### Next step
Add market-specific adjustments: require minimum absolute volume (>100 contracts) and higher price moves (>0.5% for 15M, >5% for low-liquidity final rounds).

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-361** `rejected` — Increase baseline volume calculation window to reduce amplification in thin markets.
  - **Governor rejection**: The proposed tweak sets min_price_move: 0.005 (equivalent to 0.5%), which directly conflicts with historical constraint 'No spike_min_price_move increases (e.g. to 0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected)'. This explicitly rejects increasing the minimum price move threshold to 0.005 or similar values for 15m BTC/crypto markets. Additionally, the minimum absolute volume (>100 contracts) conflicts with 'No minimum notional trade size filter (USD equiv., e.g. $500/$10k) for crypto 15m/low-volume/low-liquidity markets (TB-199,204,206,265-267,276-283,286,289,294,297,280,294,297 rejected)'.
- [ ] **TB-362** `rejected` — Raise min_price_move to 0.005 for watch-tier in 15M markets.
  - **Governor rejection**: The proposed tweak sets min_price_move: 0.005 (equivalent to 0.5%), which directly conflicts with historical constraint 'No spike_min_price_move increases (e.g. to 0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected)'. This explicitly rejects increasing the minimum price move threshold to 0.005 or similar values for 15m BTC/crypto markets. Additionally, the minimum absolute volume (>100 contracts) conflicts with 'No minimum notional trade size filter (USD equiv., e.g. $500/$10k) for crypto 15m/low-volume/low-liquidity markets (TB-199,204,206,265-267,276-283,286,289,294,297,280,294,297 rejected)'.
- [ ] **TB-363** `rejected` — Weight volume spikes by total market liquidity and require >0.05 price move in low-sample markets like golf.
  - **Governor rejection**: The proposed tweak sets min_price_move: 0.005 (equivalent to 0.5%), which directly conflicts with historical constraint 'No spike_min_price_move increases (e.g. to 0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected)'. This explicitly rejects increasing the minimum price move threshold to 0.005 or similar values for 15m BTC/crypto markets. Additionally, the minimum absolute volume (>100 contracts) conflicts with 'No minimum notional trade size filter (USD equiv., e.g. $500/$10k) for crypto 15m/low-volume/low-liquidity markets (TB-199,204,206,265-267,276-283,286,289,294,297,280,294,297 rejected)'.

---

## 2026-04-12 — Advisor snapshot 119

### Summary
False positives are concentrated in thin, short-duration markets (15-min crypto, long-dated Trump speech, final-round golf) where low baseline volumes and mechanical quotes amplify minor trades into inflated spike scores despite minimal price movement or low conviction.

### Next step
Implement liquidity-aware thresholds that scale minimum volume delta and price-move requirements inversely with market liquidity and duration. Thin markets should require higher fractional price moves (≥0.5–5%) and volume thresholds normalized to absolute contract counts rather than raw deltas.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-364** `rejected` — For markets with baseline volume <100 contracts (15-min crypto, low-liquidity Trump speech), require minimum absolute volume >100 contracts to trigger detection, and increase spike_min_price_move to 0.5–1.0%.
  - **Governor rejection**: The proposed tweak sets min_price_move: 0.01, which violates multiple historical constraints explicitly rejecting increases to spike_min_price_move (e.g., TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected ≥0.005/0.01/etc.) for BTC 15m/high-freq/whale-cluster markets. Additionally, introducing liquidity-aware scaling of minimum volume delta and price-move requirements inversely with liquidity conflicts with TB-001 applied (whale-cluster volume delta threshold ≥1000 for 15m BTC, no relaxation) and TB-002 applied (spike_score_threshold ≥8.5, no reductions), as it risks relaxing thresholds below protected minima in thin/15m BTC/crypto markets.
- [ ] **TB-365** `rejected` — For ultra-short-duration markets (≤15 min) and final-round niche markets (golf), raise spike_min_price_move threshold to 0.5–5% respectively; require price conviction before volume spikes register as signals.
  - **Governor rejection**: The proposed tweak sets min_price_move: 0.01, which violates multiple historical constraints explicitly rejecting increases to spike_min_price_move (e.g., TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected ≥0.005/0.01/etc.) for BTC 15m/high-freq/whale-cluster markets. Additionally, introducing liquidity-aware scaling of minimum volume delta and price-move requirements inversely with liquidity conflicts with TB-001 applied (whale-cluster volume delta threshold ≥1000 for 15m BTC, no relaxation) and TB-002 applied (spike_score_threshold ≥8.5, no reductions), as it risks relaxing thresholds below protected minima in thin/15m BTC/crypto markets.
- [ ] **TB-366** `rejected` — Introduce a liquidity-normalized volume delta multiplier: multiply spike_min_volume_delta by 2–3x for markets in bottom quartile of total liquidity, or use dynamic baseline windows (e.g., 5–10 min rolling average for 15-min candles instead of fixed baseline).
  - **Governor rejection**: The proposed tweak sets min_price_move: 0.01, which violates multiple historical constraints explicitly rejecting increases to spike_min_price_move (e.g., TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected ≥0.005/0.01/etc.) for BTC 15m/high-freq/whale-cluster markets. Additionally, introducing liquidity-aware scaling of minimum volume delta and price-move requirements inversely with liquidity conflicts with TB-001 applied (whale-cluster volume delta threshold ≥1000 for 15m BTC, no relaxation) and TB-002 applied (spike_score_threshold ≥8.5, no reductions), as it risks relaxing thresholds below protected minima in thin/15m BTC/crypto markets.

---

## 2026-04-12 — Advisor snapshot 120

### Summary
Recent signals show false positives from mechanical quotes in low-liquidity long-dated markets, amplified volume deltas in thin short-duration crypto markets, and negligible price moves in ultra-short markets, while one sports score market was a genuine signal.

### Next step
Introduce market-specific filters: 3x volume multiplier for low-liquidity/long-dated markets and minimum absolute volume (>100 contracts) plus extended baseline window for short-duration crypto.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-367** `rejected` — Raise volume delta multiplier to 3x baseline for low-liquidity, long-dated markets like Trump speeches.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introducing min_price_move: 0.005 directly conflicts with TB-210, TB-213, TB-216-219, TB-248-251, TB-265-273, TB-274-295, TB-296, TB-303-305, TB-316-322, TB-337-339, TB-341, TB-343-345, TB-346-348, TB-349-351, TB-352-355 (all explicitly rejected 'No spike_min_price_move increases' for BTC 15m/high-freq/whale-cluster markets). (2) The proposed '3x volume multiplier for low-liquidity/long-dated markets' conflicts with TB-200, TB-202, TB-208, TB-211, TB-214, TB-255-257, TB-265-267, TB-271-273, TB-274-277, TB-278-283, TB-284-286, TB-287-290, TB-293-295, TB-296-298 (all explicitly rejected 'No market-type-specific volume delta multipliers'). The recommendation to introduce market-specific filters with volume multipliers and minimum absolute volume thresholds systematically re-introduces filtering mechanisms that were previously rejected as causing regressions.
- [ ] **TB-368** `rejected` — Require minimum absolute volume >100 contracts and longer baseline window for thin 15-min crypto markets.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introducing min_price_move: 0.005 directly conflicts with TB-210, TB-213, TB-216-219, TB-248-251, TB-265-273, TB-274-295, TB-296, TB-303-305, TB-316-322, TB-337-339, TB-341, TB-343-345, TB-346-348, TB-349-351, TB-352-355 (all explicitly rejected 'No spike_min_price_move increases' for BTC 15m/high-freq/whale-cluster markets). (2) The proposed '3x volume multiplier for low-liquidity/long-dated markets' conflicts with TB-200, TB-202, TB-208, TB-211, TB-214, TB-255-257, TB-265-267, TB-271-273, TB-274-277, TB-278-283, TB-284-286, TB-287-290, TB-293-295, TB-296-298 (all explicitly rejected 'No market-type-specific volume delta multipliers'). The recommendation to introduce market-specific filters with volume multipliers and minimum absolute volume thresholds systematically re-introduces filtering mechanisms that were previously rejected as causing regressions.
- [ ] **TB-369** `rejected` — Increase min price move to >0.005 (0.5%) for watch-tier ultra-short-duration markets.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introducing min_price_move: 0.005 directly conflicts with TB-210, TB-213, TB-216-219, TB-248-251, TB-265-273, TB-274-295, TB-296, TB-303-305, TB-316-322, TB-337-339, TB-341, TB-343-345, TB-346-348, TB-349-351, TB-352-355 (all explicitly rejected 'No spike_min_price_move increases' for BTC 15m/high-freq/whale-cluster markets). (2) The proposed '3x volume multiplier for low-liquidity/long-dated markets' conflicts with TB-200, TB-202, TB-208, TB-211, TB-214, TB-255-257, TB-265-267, TB-271-273, TB-274-277, TB-278-283, TB-284-286, TB-287-290, TB-293-295, TB-296-298 (all explicitly rejected 'No market-type-specific volume delta multipliers'). The recommendation to introduce market-specific filters with volume multipliers and minimum absolute volume thresholds systematically re-introduces filtering mechanisms that were previously rejected as causing regressions.

---

## 2026-04-12 — Advisor snapshot 121

### Summary
Your spike detector is generating false positives across illiquid and short-duration markets by treating mechanical order flow and thin-market noise as meaningful price signals. The core issue is that volume deltas and score thresholds lack market-structure awareness, causing low-baseline markets to trigger on proportionally minor trades.

### Next step
Implement market-structure-aware thresholds: apply liquidity-adjusted volume multipliers (3x for low-liquidity markets), enforce minimum absolute volume floors (>100 contracts), and increase price-move requirements for ultra-short timeframes (>0.5% for 15-min markets).

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-370** `rejected` — For low-liquidity, long-dated markets (like KXTRUMPSAY-26APR13-TRAN): raise the volume delta multiplier to 3x baseline to filter mechanical quotes.
  - **Governor rejection**: The proposed tweak conflicts with multiple historical constraints: (1) Introduces 'liquidity-adjusted volume multipliers (3x for low-liquidity markets)', violating 'No market-type-specific volume delta multipliers... for low-liq.../crypto/BTC 15m/thin markets (TB-220,221,232-237,244...)'; (2) Adds 'minimum absolute volume floors (>100 contracts)', violating 'No minimum notional trade size filter... for crypto 15m/low-volume/low-liquidity markets (TB-199,204,206,265-267,276-283,286,289,294,297,280,297,358-360 rejected)'; (3) Sets 'min_price_move: 0.005' which is an increase, violating 'No spike_min_price_move increases (e.g. to 0.005/0.01...) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected)'.
- [ ] **TB-371** `rejected` — For thin crypto markets (like KXBTC15M): require minimum absolute volume thresholds (e.g., >100 contracts) and increase baseline volume calculation windows to dampen minor-trade amplification.
  - **Governor rejection**: The proposed tweak conflicts with multiple historical constraints: (1) Introduces 'liquidity-adjusted volume multipliers (3x for low-liquidity markets)', violating 'No market-type-specific volume delta multipliers... for low-liq.../crypto/BTC 15m/thin markets (TB-220,221,232-237,244...)'; (2) Adds 'minimum absolute volume floors (>100 contracts)', violating 'No minimum notional trade size filter... for crypto 15m/low-volume/low-liquidity markets (TB-199,204,206,265-267,276-283,286,289,294,297,280,297,358-360 rejected)'; (3) Sets 'min_price_move: 0.005' which is an increase, violating 'No spike_min_price_move increases (e.g. to 0.005/0.01...) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected)'.
- [ ] **TB-372** `rejected` — For ultra-short-duration markets (15-min buckets): increase price-move requirement for 'watch' and 'notable' tiers to >0.5% minimum, since these timeframes are noise-prone and rarely move meaningfully without underlying information.
  - **Governor rejection**: The proposed tweak conflicts with multiple historical constraints: (1) Introduces 'liquidity-adjusted volume multipliers (3x for low-liquidity markets)', violating 'No market-type-specific volume delta multipliers... for low-liq.../crypto/BTC 15m/thin markets (TB-220,221,232-237,244...)'; (2) Adds 'minimum absolute volume floors (>100 contracts)', violating 'No minimum notional trade size filter... for crypto 15m/low-volume/low-liquidity markets (TB-199,204,206,265-267,276-283,286,289,294,297,280,297,358-360 rejected)'; (3) Sets 'min_price_move: 0.005' which is an increase, violating 'No spike_min_price_move increases (e.g. to 0.005/0.01...) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected)'.

---

## 2026-04-12 — Advisor snapshot 122

### Summary
False positives are driven by mechanical liquidity bursts and low baselines in high-liquidity short-horizon BTC markets and low-liquidity long-dated event markets, amplified by insufficient absolute volume or price move filters.

### Next step
Introduce market-specific volume multipliers and minimum absolute volume thresholds, with higher price move requirements for ultra-short markets.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-373** `rejected` — Raise volume multiplier to 15x baseline for 15-min BTC markets
  - **Governor rejection**: The proposed tweak introduces 'market-specific volume multipliers' which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers (e.g. 0.5x/1-10x/1-2%/1.5x/2x/2.5x/3x/5-10x/14.9x→25x baseline) for low-liq/pre-game/golf props/NBA/sports winner' (explicitly rejected in TB-200,202,208,211,214,255-257,265-267,271-273,274-277,278-283,284-286,287-290,293-295,296-298). Additionally, it introduces 'minimum absolute volume thresholds', conflicting with 'No minimum notional trade size filter (USD equiv., e.g. $500/$10k) for crypto 15m/low-volume/low-liquidity markets' (TB-199,204,206,265-267,276-283,286,289,294,297,280,297,358-360,364-366,370-372 rejected). Finally, 'min_price_move: 0.005' conflicts with 'No spike_min_price_move increases (e.g. to 0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets' (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected).
- [ ] **TB-374** `rejected` — Set volume multiplier to 3x baseline for low-liquidity long-dated markets like Trump speech
  - **Governor rejection**: The proposed tweak introduces 'market-specific volume multipliers' which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers (e.g. 0.5x/1-10x/1-2%/1.5x/2x/2.5x/3x/5-10x/14.9x→25x baseline) for low-liq/pre-game/golf props/NBA/sports winner' (explicitly rejected in TB-200,202,208,211,214,255-257,265-267,271-273,274-277,278-283,284-286,287-290,293-295,296-298). Additionally, it introduces 'minimum absolute volume thresholds', conflicting with 'No minimum notional trade size filter (USD equiv., e.g. $500/$10k) for crypto 15m/low-volume/low-liquidity markets' (TB-199,204,206,265-267,276-283,286,289,294,297,280,297,358-360,364-366,370-372 rejected). Finally, 'min_price_move: 0.005' conflicts with 'No spike_min_price_move increases (e.g. to 0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets' (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected).
- [ ] **TB-375** `rejected` — Require minimum absolute volume >100 contracts and extend baseline window for thin markets
  - **Governor rejection**: The proposed tweak introduces 'market-specific volume multipliers' which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers (e.g. 0.5x/1-10x/1-2%/1.5x/2x/2.5x/3x/5-10x/14.9x→25x baseline) for low-liq/pre-game/golf props/NBA/sports winner' (explicitly rejected in TB-200,202,208,211,214,255-257,265-267,271-273,274-277,278-283,284-286,287-290,293-295,296-298). Additionally, it introduces 'minimum absolute volume thresholds', conflicting with 'No minimum notional trade size filter (USD equiv., e.g. $500/$10k) for crypto 15m/low-volume/low-liquidity markets' (TB-199,204,206,265-267,276-283,286,289,294,297,280,297,358-360,364-366,370-372 rejected). Finally, 'min_price_move: 0.005' conflicts with 'No spike_min_price_move increases (e.g. to 0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets' (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected).
- [ ] **TB-376** `rejected` — Increase min price move to >0.005 for watch tier in 15-min markets
  - **Governor rejection**: The proposed tweak introduces 'market-specific volume multipliers' which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers (e.g. 0.5x/1-10x/1-2%/1.5x/2x/2.5x/3x/5-10x/14.9x→25x baseline) for low-liq/pre-game/golf props/NBA/sports winner' (explicitly rejected in TB-200,202,208,211,214,255-257,265-267,271-273,274-277,278-283,284-286,287-290,293-295,296-298). Additionally, it introduces 'minimum absolute volume thresholds', conflicting with 'No minimum notional trade size filter (USD equiv., e.g. $500/$10k) for crypto 15m/low-volume/low-liquidity markets' (TB-199,204,206,265-267,276-283,286,289,294,297,280,297,358-360,364-366,370-372 rejected). Finally, 'min_price_move: 0.005' conflicts with 'No spike_min_price_move increases (e.g. to 0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets' (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected).

---

## 2026-04-12 — Advisor snapshot 123

### Summary
False positives are driven by mechanical liquidity bursts in high-liquidity short-horizon BTC markets, thin baselines amplifying minor trades in crypto, and noise in ultra-short or low-liquidity markets, despite varying price moves and scores.

### Next step
Introduce market-specific volume multipliers and minimum absolute volume thresholds to filter mechanical noise without uniform global changes.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-377** `rejected` — Raise volume multiplier threshold to 15x baseline for 15-min BTC markets.
  - **Governor rejection**: The proposed tweak introduces min_price_move: 0.005, which directly violates the historical constraint 'No spike_min_price_move increases' (TB-210, 213, 216-219, 248-251, 265-273, 274-295, 296, 303-305, 316-322, 337-339, 341, 343-345, 346-348, 349-351, 352-355 rejected) for BTC 15m/high-freq/whale-cluster markets. This constraint was explicitly applied to prevent regression, and the proposed minimum price move threshold of 0.005 represents exactly the type of spike_min_price_move increase that has been systematically rejected across 40+ prior test batches. This relaxes the detector's sensitivity in the exact market context (BTC 15m whale-cluster) where the constraint was hardened.
- [ ] **TB-378** `rejected` — Require minimum absolute volume >100 contracts for thin markets.
  - **Governor rejection**: The proposed tweak introduces min_price_move: 0.005, which directly violates the historical constraint 'No spike_min_price_move increases' (TB-210, 213, 216-219, 248-251, 265-273, 274-295, 296, 303-305, 316-322, 337-339, 341, 343-345, 346-348, 349-351, 352-355 rejected) for BTC 15m/high-freq/whale-cluster markets. This constraint was explicitly applied to prevent regression, and the proposed minimum price move threshold of 0.005 represents exactly the type of spike_min_price_move increase that has been systematically rejected across 40+ prior test batches. This relaxes the detector's sensitivity in the exact market context (BTC 15m whale-cluster) where the constraint was hardened.
- [ ] **TB-379** `rejected` — Increase price-move requirement to >0.5% for ultra-short-duration (15 min) watch-tier alerts.
  - **Governor rejection**: The proposed tweak introduces min_price_move: 0.005, which directly violates the historical constraint 'No spike_min_price_move increases' (TB-210, 213, 216-219, 248-251, 265-273, 274-295, 296, 303-305, 316-322, 337-339, 341, 343-345, 346-348, 349-351, 352-355 rejected) for BTC 15m/high-freq/whale-cluster markets. This constraint was explicitly applied to prevent regression, and the proposed minimum price move threshold of 0.005 represents exactly the type of spike_min_price_move increase that has been systematically rejected across 40+ prior test batches. This relaxes the detector's sensitivity in the exact market context (BTC 15m whale-cluster) where the constraint was hardened.

---

## 2026-04-12 — Advisor snapshot 124

### Summary
False positives are driven by mechanical liquidity bursts in high-liquidity short-horizon BTC markets and amplified signals in low-liquidity or thin markets, despite varying price moves and scores.

### Next step
Introduce market-specific volume multipliers and minimum absolute volume thresholds to filter noise without uniform changes.

### Recommendations

- [ ] **TB-380** `planned` — Raise volume multiplier threshold to 15x baseline for 15-min BTC markets.
- [ ] **TB-381** `planned` — Increase volume delta multiplier to 3x baseline for low-liquidity long-dated markets like Trump speeches.
- [ ] **TB-382** `planned` — Require minimum absolute volume >100 contracts and extend baseline volume window for thin markets.

---

## 2026-04-12 — Advisor snapshot 125

### Summary
False positives are driven by mechanical moves like single large bets, liquidity bursts, and thin baselines amplifying minor trades in low-liquidity or short-horizon markets such as golf props, BTC 15-min, and Trump speeches.

### Next step
Introduce market-type specific volume multipliers and minimum trade requirements to filter mechanical noise without globally raising thresholds.

### Recommendations

- [ ] **TB-383** `rejected` — Raise volume delta multiplier to 1.5x baseline and require 2+ recent trades for golf prop markets.
  - **Governor rejection**: The proposed tweak directly violates the historical constraint 'No market-type-specific volume delta multipliers' (rejected TB-199, 204, 206, 265-267, 276-283, 286, 289, 294, 297, 358-360, 364-366, 370-372, 378). The recommendation to 'introduce market-type specific volume multipliers' is explicitly contradicted by this constraint, which rejected numerous similar proposals across multiple test batches. The constraint was established to prevent differential treatment of markets by volume multipliers (0.5x, 1-10x, 1.5x, 2x, etc.), and the current proposal attempts to circumvent this by introducing exactly such multipliers for 'golf props, BTC 15-min, and Trump speeches.'
- [ ] **TB-384** `rejected` — Set volume multiplier to 15x baseline for 15-min BTC markets.
  - **Governor rejection**: The proposed tweak directly violates the historical constraint 'No market-type-specific volume delta multipliers' (rejected TB-199, 204, 206, 265-267, 276-283, 286, 289, 294, 297, 358-360, 364-366, 370-372, 378). The recommendation to 'introduce market-type specific volume multipliers' is explicitly contradicted by this constraint, which rejected numerous similar proposals across multiple test batches. The constraint was established to prevent differential treatment of markets by volume multipliers (0.5x, 1-10x, 1.5x, 2x, etc.), and the current proposal attempts to circumvent this by introducing exactly such multipliers for 'golf props, BTC 15-min, and Trump speeches.'
- [ ] **TB-385** `rejected` — Raise volume delta multiplier to 3x baseline for low-liquidity long-dated Trump speech markets; add min absolute volume >100 contracts.
  - **Governor rejection**: The proposed tweak directly violates the historical constraint 'No market-type-specific volume delta multipliers' (rejected TB-199, 204, 206, 265-267, 276-283, 286, 289, 294, 297, 358-360, 364-366, 370-372, 378). The recommendation to 'introduce market-type specific volume multipliers' is explicitly contradicted by this constraint, which rejected numerous similar proposals across multiple test batches. The constraint was established to prevent differential treatment of markets by volume multipliers (0.5x, 1-10x, 1.5x, 2x, etc.), and the current proposal attempts to circumvent this by introducing exactly such multipliers for 'golf props, BTC 15-min, and Trump speeches.'

---

## 2026-04-12 — Advisor snapshot 126

### Summary
False positives dominate in low-liquidity long-dated word markets (e.g., Trump speech), golf props, and thin short-horizon crypto markets (e.g., 15-min BTC), driven by mechanical quoting, single bets, or low baselines amplifying minor trades despite low price moves.

### Next step
Introduce market-type-specific volume multipliers and minimum absolute volume/trade requirements, with baseline window adjustments for thin markets.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-386** `rejected` — Set volume multiplier to 3x baseline and price move >0.05 for low-liquidity, long-dated word markets.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume multipliers** and **minimum absolute volume/trade requirements**, which directly conflicts with the historical constraint '**No market-type-specific volume delta multipliers** (e.g. 0.5' (incomplete but clear intent from rejected TBs). Additionally, for 15m BTC (explicitly mentioned), it suggests **min_price_move: 0.05**, violating '**No spike_min_price_move increases** (e.g. to 0.005/0.01/.../0.05...) for BTC 15m/... markets' (TB-210,213,... rejected), as this raises the minimum price move threshold.
- [ ] **TB-387** `rejected` — Require 1.5x volume multiplier and >=2 recent trades for golf prop markets.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume multipliers** and **minimum absolute volume/trade requirements**, which directly conflicts with the historical constraint '**No market-type-specific volume delta multipliers** (e.g. 0.5' (incomplete but clear intent from rejected TBs). Additionally, for 15m BTC (explicitly mentioned), it suggests **min_price_move: 0.05**, violating '**No spike_min_price_move increases** (e.g. to 0.005/0.01/.../0.05...) for BTC 15m/... markets' (TB-210,213,... rejected), as this raises the minimum price move threshold.
- [ ] **TB-388** `rejected` — Raise volume multiplier to 15x baseline for high-liquidity short-horizon crypto; add min absolute volume >100 contracts and longer baseline window for thin crypto.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume multipliers** and **minimum absolute volume/trade requirements**, which directly conflicts with the historical constraint '**No market-type-specific volume delta multipliers** (e.g. 0.5' (incomplete but clear intent from rejected TBs). Additionally, for 15m BTC (explicitly mentioned), it suggests **min_price_move: 0.05**, violating '**No spike_min_price_move increases** (e.g. to 0.005/0.01/.../0.05...) for BTC 15m/... markets' (TB-210,213,... rejected), as this raises the minimum price move threshold.

---

## 2026-04-12 — Advisor snapshot 127

### Summary
False positives dominate in low-liquidity, long-dated word markets (e.g., Trump speech) and specific props (e.g., golf scores) due to mechanical quoting and single-bet bursts, despite moderate volume deltas and small price moves; high-liquidity short-horizon BTC also triggers on liquidity bursts.

### Next step
Introduce market-category dynamic multipliers for volume threshold (e.g., 3x baseline for low-liq long-dated, 1.5x for golf props, 15x for BTC 15m) combined with minimum price move and trade count requirements.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-389** `rejected` — Raise volume multiplier to 3x baseline and require >5% price move for watch tier in low-liquidity, long-dated word markets.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume delta multipliers** (e.g., 3x for low-liq long-dated, 1.5x for golf props, 15x for BTC 15m), which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers' (rejected TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336,340,343-344,367-375,38). It also adds **minimum price move** requirements (min_price_move: 0.05), conflicting with 'No spike_min_price_move increases' (rejected TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379).
- [ ] **TB-390** `rejected` — Require 1.5x volume delta baseline plus at least 2 recent trades for golf prop markets.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume delta multipliers** (e.g., 3x for low-liq long-dated, 1.5x for golf props, 15x for BTC 15m), which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers' (rejected TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336,340,343-344,367-375,38). It also adds **minimum price move** requirements (min_price_move: 0.05), conflicting with 'No spike_min_price_move increases' (rejected TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379).
- [ ] **TB-391** `rejected` — Raise volume multiplier to 15x baseline for 15-min BTC markets.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume delta multipliers** (e.g., 3x for low-liq long-dated, 1.5x for golf props, 15x for BTC 15m), which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers' (rejected TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336,340,343-344,367-375,38). It also adds **minimum price move** requirements (min_price_move: 0.05), conflicting with 'No spike_min_price_move increases' (rejected TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379).

---

## 2026-04-12 — Advisor snapshot 128

### Summary
False positives are prevalent in low-liquidity markets like golf props and long-dated Trump speech markets, and high-liquidity short-horizon BTC markets, driven by mechanical quoting, single-bet moves, and liquidity bursts despite varying price moves.

### Next step
Introduce market-type specific volume multipliers (e.g., 2-3x baseline for low-liq props, 15x for BTC) and require confirmed trade flow or multiple recent trades alongside price move >5%.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-392** `rejected` — Raise volume multiplier to 2.0x baseline and price move >0.05 for golf prop markets
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume multipliers** (e.g., 2-3x baseline for low-liq props, 15x for BTC), which directly conflicts with the historical constraint '**No market-type-specific volume delta multipliers** (e.g. 0.5x/1-10x/1-2%/1.5x/2x/2.5x/3x/5-10x/14.9x→25x/15x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC' (explicitly rejected in multiple TBs). Additionally, it sets **min_price_move: 0.05**, which violates '**No spike_min_price_move increases** (e.g. to 0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets' (rejected in TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379).
- [ ] **TB-393** `rejected` — Require volume multiplier >3x baseline and price move >0.05 for low-liquidity long-dated word markets
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume multipliers** (e.g., 2-3x baseline for low-liq props, 15x for BTC), which directly conflicts with the historical constraint '**No market-type-specific volume delta multipliers** (e.g. 0.5x/1-10x/1-2%/1.5x/2x/2.5x/3x/5-10x/14.9x→25x/15x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC' (explicitly rejected in multiple TBs). Additionally, it sets **min_price_move: 0.05**, which violates '**No spike_min_price_move increases** (e.g. to 0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets' (rejected in TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379).
- [ ] **TB-394** `rejected` — Raise volume multiplier to 15x baseline for 15-min BTC markets; add min 2 recent trades for golf props
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume multipliers** (e.g., 2-3x baseline for low-liq props, 15x for BTC), which directly conflicts with the historical constraint '**No market-type-specific volume delta multipliers** (e.g. 0.5x/1-10x/1-2%/1.5x/2x/2.5x/3x/5-10x/14.9x→25x/15x baseline) for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC' (explicitly rejected in multiple TBs). Additionally, it sets **min_price_move: 0.05**, which violates '**No spike_min_price_move increases** (e.g. to 0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets' (rejected in TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379).

---

## 2026-04-12 — Advisor snapshot 129

### Summary
False positives are driven by mechanical quoting and single-bet adjustments in low-liquidity golf prop markets, long-dated word markets, and high-liquidity short-horizon BTC contracts, often with small price moves (<5%) despite high volume deltas.

### Next step
Introduce market-type specific volume multipliers (e.g., 2x baseline for golf props, 3x for low-liquidity word markets, 15x for BTC 15m) and require confirmed multi-trade flow.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-395** `rejected` — Raise min_price_move to 0.05 globally and require >2 recent trades to filter single-bet mechanical moves.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume multipliers** (e.g., 2x for golf props, 3x for low-liquidity word markets, 15x for BTC 15m), which directly conflicts with the historical constraint '**No market-type-specific volume delta multipliers** (e.g. 0.5x/1-10x/1-2%/1.5x/2x/2.5x/', as previously rejected in multiple TBs.
- [ ] **TB-396** `rejected` — Set tier-specific thresholds: watch tier needs 3x volume multiplier + >5% price move for low-liquidity markets.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume multipliers** (e.g., 2x for golf props, 3x for low-liquidity word markets, 15x for BTC 15m), which directly conflicts with the historical constraint '**No market-type-specific volume delta multipliers** (e.g. 0.5x/1-10x/1-2%/1.5x/2x/2.5x/', as previously rejected in multiple TBs.
- [ ] **TB-397** `rejected` — For golf props and BTC short-horizon, enforce 1.5-15x volume baseline multipliers based on liquidity and horizon.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume multipliers** (e.g., 2x for golf props, 3x for low-liquidity word markets, 15x for BTC 15m), which directly conflicts with the historical constraint '**No market-type-specific volume delta multipliers** (e.g. 0.5x/1-10x/1-2%/1.5x/2x/2.5x/', as previously rejected in multiple TBs.

---

## 2026-04-12 — Advisor snapshot 130

### Summary
False positives are driven by mechanical quoting and single-bet moves in golf prop markets, low-liquidity word markets, and high-liquidity short-horizon BTC contracts, despite notable volume deltas and price moves.

### Next step
Introduce market-type specific volume multipliers (e.g., 2x baseline for golf props, 3x for low-liq word markets, 15x for 15m BTC) and require confirmed trade flow or multiple recent trades.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-398** `planned` — Raise volume multiplier to 2.0x baseline and price move >5% for golf prop markets.
- [ ] **TB-399** `planned` — Require >5% price move and 3x volume multiplier for watch tier in low-liquidity long-dated word markets.
- [ ] **TB-400** `planned` — Raise volume multiplier to 15x baseline for 15-min BTC markets and add 1.5x baseline with 2+ recent trades filter for golf props.

---

## 2026-04-12 — Advisor snapshot 131

### Summary
Your detector is generating false positives in specialty markets (golf props, long-dated word markets) and high-liquidity short-horizon contracts (15-min BTC) due to mechanical quote adjustments and liquidity bursts rather than genuine price discovery. Meanwhile, you're missing some genuine signals in medium-liquidity contracts.

### Next step
Implement market-specific thresholds rather than global ones: require higher volume multipliers (1.5x–15x baseline depending on contract type and liquidity profile) and price-move minimums (>5% for specialty/low-liquidity markets) to filter mechanical moves while preserving signal detection in genuine flow.

### Recommendations

- [ ] **TB-401** `rejected` — For golf prop markets (PGAROUNDSCORE): raise volume_delta multiplier to 1.5x–2.0x baseline and require price_move >5% with confirmed multi-trade flow to filter single-bet mechanical adjustments
  - **Governor rejection**: The proposed tweak violates multiple historical constraints by introducing market-type-specific volume delta multipliers (e.g., 1.5x–15x baseline depending on contract type and liquidity profile), explicitly rejected in TB-XXX (e.g., TB-200,202, etc.); increases spike_min_price_move (e.g., >5% for specialty/low-liquidity markets), rejected in TB-210,213, etc.; and implements market-specific thresholds, conflicting with the applied no market-type-specific multipliers rule.
- [ ] **TB-402** `rejected` — For long-dated, low-liquidity word markets (TRUMPSAY, etc.): raise volume_delta multiplier to 3x baseline and enforce price_move >5% minimum to suppress algorithmic quoting noise
  - **Governor rejection**: The proposed tweak violates multiple historical constraints by introducing market-type-specific volume delta multipliers (e.g., 1.5x–15x baseline depending on contract type and liquidity profile), explicitly rejected in TB-XXX (e.g., TB-200,202, etc.); increases spike_min_price_move (e.g., >5% for specialty/low-liquidity markets), rejected in TB-210,213, etc.; and implements market-specific thresholds, conflicting with the applied no market-type-specific multipliers rule.
- [ ] **TB-403** `rejected` — For 15-min high-liquidity BTC (KXBTC15M): raise volume_delta multiplier to 15x baseline to filter high-frequency mechanical liquidity bursts while retaining genuine momentum signals
  - **Governor rejection**: The proposed tweak violates multiple historical constraints by introducing market-type-specific volume delta multipliers (e.g., 1.5x–15x baseline depending on contract type and liquidity profile), explicitly rejected in TB-XXX (e.g., TB-200,202, etc.); increases spike_min_price_move (e.g., >5% for specialty/low-liquidity markets), rejected in TB-210,213, etc.; and implements market-specific thresholds, conflicting with the applied no market-type-specific multipliers rule.

---

## 2026-04-12 — Advisor snapshot 132

### Summary
False positives are driven by mechanical quoting and single-bet moves in low-liquidity markets like golf props, long-dated words, and short-horizon BTC, where high volume deltas occur with small price moves (<5%) and low yes prices (~0.05). True signals show larger price moves or lag pricing despite small deltas.

### Next step
Require minimum price move of 0.05 and at least 2 recent trades globally to filter mechanical adjustments.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-404** `rejected` — Raise volume multiplier to 2.0x baseline and price move >0.05 for golf prop markets.
  - **Governor rejection**: The proposed tweak directly violates the historical constraint 'No spike_min_price_move increases' (rejected TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-403). The recommendation to 'Require minimum price move of 0.05' is explicitly a spike_min_price_move increase, which has been rejected across 40+ previous tuning proposals. This constraint was tightened to prevent over-filtering of legitimate signals and should not be relaxed without documented evidence that prior rejections were in error.
- [ ] **TB-405** `rejected` — Raise volume multiplier to 3x baseline and price move >0.05 for low-liquidity long-dated word markets.
  - **Governor rejection**: The proposed tweak directly violates the historical constraint 'No spike_min_price_move increases' (rejected TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-403). The recommendation to 'Require minimum price move of 0.05' is explicitly a spike_min_price_move increase, which has been rejected across 40+ previous tuning proposals. This constraint was tightened to prevent over-filtering of legitimate signals and should not be relaxed without documented evidence that prior rejections were in error.
- [ ] **TB-406** `rejected` — Raise volume multiplier to 15x baseline for 15-min BTC markets.
  - **Governor rejection**: The proposed tweak directly violates the historical constraint 'No spike_min_price_move increases' (rejected TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-403). The recommendation to 'Require minimum price move of 0.05' is explicitly a spike_min_price_move increase, which has been rejected across 40+ previous tuning proposals. This constraint was tightened to prevent over-filtering of legitimate signals and should not be relaxed without documented evidence that prior rejections were in error.

---

## 2026-04-12 — Advisor snapshot 133

### Summary
False positives are prevalent in low-liquidity markets like golf props and long-dated word markets, triggered by mechanical quoting or single-bet moves despite small price changes (<5%) and low yes prices (~0.05), while genuine signals show high volume deltas even with modest price moves.

### Next step
Raise min_price_move to 0.05 and add market-type rules: 2.0x volume multiplier for golf props, 3.0x for low-liquidity word markets.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `3.0`

### Recommendations

- [ ] **TB-407** `rejected` — Require price move >5% for watch tier in low-liquidity and golf prop markets.
  - **Governor rejection**: The proposed tweak raises **min_price_move to 0.05**, which directly conflicts with **TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-403,404-406 rejected**: **No spike_min_price_move increases** (e.g. to 0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets. Additionally, it introduces **market-type-specific volume delta multipliers** (2.0x for golf props, 3.0x for low-liquidity word markets), violating **No market-type-specific volume delta multipliers** (e.g. 0.5x/1-10x/1-2%/1.5x/2x/2.5x/3x/5-10x/14.9x→25x/15x baseline) for low-liq/.../crypto/BTC 15.
- [ ] **TB-408** `rejected` — Increase volume multiplier threshold to 2.0x baseline for golf props with at least 2 recent trades.
  - **Governor rejection**: The proposed tweak raises **min_price_move to 0.05**, which directly conflicts with **TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-403,404-406 rejected**: **No spike_min_price_move increases** (e.g. to 0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets. Additionally, it introduces **market-type-specific volume delta multipliers** (2.0x for golf props, 3.0x for low-liquidity word markets), violating **No market-type-specific volume delta multipliers** (e.g. 0.5x/1-10x/1-2%/1.5x/2x/2.5x/3x/5-10x/14.9x→25x/15x baseline) for low-liq/.../crypto/BTC 15.
- [ ] **TB-409** `rejected` — Require price move >3% globally and score >3.0 to filter mechanical quoting.
  - **Governor rejection**: The proposed tweak raises **min_price_move to 0.05**, which directly conflicts with **TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-403,404-406 rejected**: **No spike_min_price_move increases** (e.g. to 0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets. Additionally, it introduces **market-type-specific volume delta multipliers** (2.0x for golf props, 3.0x for low-liquidity word markets), violating **No market-type-specific volume delta multipliers** (e.g. 0.5x/1-10x/1-2%/1.5x/2x/2.5x/3x/5-10x/14.9x→25x/15x baseline) for low-liq/.../crypto/BTC 15.

---

## 2026-04-12 — Advisor snapshot 134

### Summary
False positives are triggered by mechanical quoting or single-bet moves in low-liquidity markets like golf props and long-dated word markets, despite low price moves (<5%) and watch-tier scores (~2.7), while true signals show significant volume with smaller price deltas due to pricing lags.

### Next step
Require minimum price move >0.05 and recent confirmed trade flow across all markets to filter mechanical adjustments.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-410** `rejected` — Raise volume multiplier to 2.0x baseline for golf prop markets
  - **Governor rejection**: The proposed tweak requires a **minimum price move >0.05**, which directly conflicts with historical constraint 'No spike_min_price_move increases' (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-403,404-406 rejected; e.g., no ≥0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%). These TBs explicitly rejected increasing the minimum price move threshold, including to 0.05, to avoid missing true spikes with smaller price deltas.
- [ ] **TB-411** `rejected` — Require >5% price move and 3x volume multiplier for watch tier in low-liquidity word markets
  - **Governor rejection**: The proposed tweak requires a **minimum price move >0.05**, which directly conflicts with historical constraint 'No spike_min_price_move increases' (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-403,404-406 rejected; e.g., no ≥0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%). These TBs explicitly rejected increasing the minimum price move threshold, including to 0.05, to avoid missing true spikes with smaller price deltas.
- [ ] **TB-412** `rejected` — Add filter for at least 2 recent trades in prop markets to exclude single-bet spikes
  - **Governor rejection**: The proposed tweak requires a **minimum price move >0.05**, which directly conflicts with historical constraint 'No spike_min_price_move increases' (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-403,404-406 rejected; e.g., no ≥0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%). These TBs explicitly rejected increasing the minimum price move threshold, including to 0.05, to avoid missing true spikes with smaller price deltas.

---

## 2026-04-12 — Advisor snapshot 135

### Summary
False positives cluster in low-liquidity, long-dated Trump speech markets and golf prop markets, triggered by mechanical quoting or small trades despite low price moves, while genuine high-signal events like KXBTC15M are correctly detected.

### Next step
Introduce market-type rules: raise volume multiplier to 2-3x baseline and price move to 5-10% for low-liquidity/long-dated props and golf markets.

### Recommendations

- [ ] **TB-413** `planned` — Raise volume delta multiplier to 2x baseline and price move to 10% for low-liquidity, long-dated Trump speech markets.
- [ ] **TB-414** `planned` — Require volume multiplier >=2.0x baseline, price move >5%, and >=2 recent trades for golf prop markets.
- [ ] **TB-415** `planned` — Raise volume multiplier to 3x baseline and price move >5% for watch-tier low-liquidity word markets.

---

## 2026-04-12 — Advisor snapshot 136

### Summary
False positives dominate in low-liquidity markets like Trump speech props and golf bets, triggered by passive liquidity provision, mechanical quote adjustments, or single unexecuted quotes without meaningful price moves or confirmed trades.

### Next step
Introduce market-type specific multipliers (e.g., 2-3x volume baseline for low-liquidity props) and require confirmed executed trades in volume delta calculations.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-416** `rejected` — Raise volume delta multiplier to 2x baseline for low-liquidity/long-dated markets and exclude unexecuted quotes.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume delta multipliers** (e.g., 2-3x volume baseline for low-liquidity props), which directly conflicts with the historical constraint '**No market-type-specific volume delta multipliers** (e.g., n' that explicitly rejected such changes. Additionally, it sets **min_price_move: 0.05**, violating the '**No spike_min_price_move increases** (e.g., no ≥0.005/0.01/.../0.05)' rule for relevant markets.
- [ ] **TB-417** `rejected` — Require minimum 5% price move and at least 2 recent confirmed trades for watch tier.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume delta multipliers** (e.g., 2-3x volume baseline for low-liquidity props), which directly conflicts with the historical constraint '**No market-type-specific volume delta multipliers** (e.g., n' that explicitly rejected such changes. Additionally, it sets **min_price_move: 0.05**, violating the '**No spike_min_price_move increases** (e.g., no ≥0.005/0.01/.../0.05)' rule for relevant markets.
- [ ] **TB-418** `rejected` — Differentiate thresholds by market tier: golf props need 2x volume + 5% price; BTC needs higher volume-to-trade ratio.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume delta multipliers** (e.g., 2-3x volume baseline for low-liquidity props), which directly conflicts with the historical constraint '**No market-type-specific volume delta multipliers** (e.g., n' that explicitly rejected such changes. Additionally, it sets **min_price_move: 0.05**, violating the '**No spike_min_price_move increases** (e.g., no ≥0.005/0.01/.../0.05)' rule for relevant markets.

---

## 2026-04-12 — Advisor snapshot 137

### Summary
False positives dominate in low-liquidity markets like Trump speech and golf props due to mechanical quoting, passive liquidity, and unexecuted volume spikes without meaningful price moves, while true signals show high volume with substantial price changes.

### Next step
Require minimum price move >0.03 AND volume multiplier >2x baseline, excluding unexecuted quotes from volume delta.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-419** `rejected` — Raise volume multiplier threshold to 2-3x baseline for low-liquidity and long-dated markets
  - **Governor rejection**: The proposed tweak requires a **minimum price move >0.03**, which directly conflicts with the historical constraint '**No spike_min_price_move increases** (e.g., ≥0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets' (rejected TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418). This introduces a price move threshold explicitly rejected multiple times to prevent restricting spike detection.
- [ ] **TB-420** `rejected` — Mandate price move >5% for watch tier in prop/event markets with mechanical quoting
  - **Governor rejection**: The proposed tweak requires a **minimum price move >0.03**, which directly conflicts with the historical constraint '**No spike_min_price_move increases** (e.g., ≥0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets' (rejected TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418). This introduces a price move threshold explicitly rejected multiple times to prevent restricting spike detection.
- [ ] **TB-421** `rejected` — Filter volume delta to include only executed trades, ignoring passive liquidity provision
  - **Governor rejection**: The proposed tweak requires a **minimum price move >0.03**, which directly conflicts with the historical constraint '**No spike_min_price_move increases** (e.g., ≥0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets' (rejected TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418). This introduces a price move threshold explicitly rejected multiple times to prevent restricting spike detection.

---

## 2026-04-12 — Advisor snapshot 138

### Summary
False positives are driven by quote-only noise, mechanical quoting, and unexecuted large quotes in low-liquidity markets like golf props and long-dated Trump speech markets, triggering on high volume deltas without real trade flow or sufficient price moves.

### Next step
Raise volume delta multiplier to 2.0x baseline globally and add a minimum trades filter (>5 recent trades) to exclude quote-only noise.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-422** `rejected` — Require >5 recent trades for all watch-tier signals to filter quote-only volume spikes.
  - **Governor rejection**: The proposed tweak violates the historical constraint 'No market-type-specific volume delta multipliers (e.g. 0.5x/1-10x/1-2%/1.5x/2x/2.5x/3x/5-10x/14.', which explicitly rejects introducing multipliers like the proposed 2.0x baseline globally. Although described as 'global', it directly matches the rejected 2.0x example and conflicts with the no-multipliers rule established to prevent such adjustments.
- [ ] **TB-423** `rejected` — For golf prop markets, enforce 2.0x volume delta, >5% price move, and confirmed trade flow.
  - **Governor rejection**: The proposed tweak violates the historical constraint 'No market-type-specific volume delta multipliers (e.g. 0.5x/1-10x/1-2%/1.5x/2x/2.5x/3x/5-10x/14.', which explicitly rejects introducing multipliers like the proposed 2.0x baseline globally. Although described as 'global', it directly matches the rejected 2.0x example and conflicts with the no-multipliers rule established to prevent such adjustments.
- [ ] **TB-424** `rejected` — For low-liquidity long-dated markets (e.g., Trump speech), raise to 3x volume delta and 5-10% price move.
  - **Governor rejection**: The proposed tweak violates the historical constraint 'No market-type-specific volume delta multipliers (e.g. 0.5x/1-10x/1-2%/1.5x/2x/2.5x/3x/5-10x/14.', which explicitly rejects introducing multipliers like the proposed 2.0x baseline globally. Although described as 'global', it directly matches the rejected 2.0x example and conflicts with the no-multipliers rule established to prevent such adjustments.

---

## 2026-04-12 — Advisor snapshot 139

### Summary
False positives are driven by quote-only noise, unexecuted large quotes, and mechanical adjustments in low-liquidity markets like golf props and long-dated Trump speeches, triggering on high volume deltas without real trade flow or sufficient price moves.

### Next step
Raise volume delta multiplier to 2.0x baseline globally and add market-type rules requiring >5 recent trades and excluding unexecuted quotes.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-425** `planned` — Require >5 recent trades and 2.0x volume delta multiplier for golf prop markets to filter quote-only noise.
- [ ] **TB-426** `planned` — Exclude large unexecuted quotes from volume delta calculations or increase volume-to-trade ratio threshold.
- [ ] **TB-427** `planned` — For low-liquidity long-dated markets like Trump speeches, require 10% price move and 2x volume multiplier.

---

## 2026-04-12 — Advisor snapshot 140

### Summary
Your detector is generating false positives primarily from liquidity-driven volume spikes in low-liquidity markets (golf props, long-dated events) and passive quote adjustments that lack genuine price discovery. True signals are being obscured by noise because volume delta alone is triggering alerts without sufficient price confirmation.

### Next step
Implement a liquidity-adjusted volume threshold that scales by market baseline and requires minimum price move confirmation (>3-5%) before emitting watch-tier alerts, with stricter rules for markets identified as low-liquidity or quote-heavy.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-428** `planned` — For golf prop and long-dated markets (KXPGAROUNDSCORE*, KXTRUMPSAY*): Raise spike_min_volume_delta multiplier to 2.0x baseline and require spike_min_price_move ≥ 0.05 (5%) to filter liquidity-driven noise.
- [ ] **TB-429** `planned` — For crypto/high-frequency markets (KXBTC*): Exclude unexecuted quotes or passive liquidity from volume delta calculations; use trade-count confirmation (minimum 5+ executed trades) before escalating to watch tier.
- [ ] **TB-430** `planned` — Add a trade-execution ratio filter: require volume delta to correlate with actual executed trade count, not just quoted size, to prevent passive market-maker activity from triggering false signals.

---

## 2026-04-12 — Advisor snapshot 141

### Summary
False positives are prevalent in low-liquidity markets like golf props and long-dated events, driven by liquidity swings, quote-only noise, and passive orders without meaningful price moves or executed trades.

### Next step
Introduce market-type rules raising volume delta to 2x baseline and price move to 0.05+ for low-liquidity categories (golf props, long-dated speeches); filter out unexecuted quotes.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-431** `rejected` — Raise volume delta multiplier to 2.0x baseline for golf prop markets
  - **Governor rejection**: The proposed tweak introduces min_price_move: 0.05 for low-liquidity markets (golf props, long-dated events), which directly violates the historical constraint: 'No spike_min_price_move increases (e.g. ≥0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected)'. Although the proposal targets low-liquidity categories rather than BTC 15m specifically, the precedent of rejecting price move thresholds at or above 0.05 (TB-248-251, TB-265-273, TB-274-295) indicates a systematic rejection of this parameter adjustment across market types. Introducing this threshold would conflict with the established pattern of rejections and risks reintroducing the noise regression that these prior rejections were designed to prevent.
- [ ] **TB-432** `rejected` — Require price move >0.05 and >5 recent trades for low-liquidity/long-dated markets
  - **Governor rejection**: The proposed tweak introduces min_price_move: 0.05 for low-liquidity markets (golf props, long-dated events), which directly violates the historical constraint: 'No spike_min_price_move increases (e.g. ≥0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected)'. Although the proposal targets low-liquidity categories rather than BTC 15m specifically, the precedent of rejecting price move thresholds at or above 0.05 (TB-248-251, TB-265-273, TB-274-295) indicates a systematic rejection of this parameter adjustment across market types. Introducing this threshold would conflict with the established pattern of rejections and risks reintroducing the noise regression that these prior rejections were designed to prevent.
- [ ] **TB-433** `rejected` — Exclude large unexecuted quotes from volume delta in all markets
  - **Governor rejection**: The proposed tweak introduces min_price_move: 0.05 for low-liquidity markets (golf props, long-dated events), which directly violates the historical constraint: 'No spike_min_price_move increases (e.g. ≥0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected)'. Although the proposal targets low-liquidity categories rather than BTC 15m specifically, the precedent of rejecting price move thresholds at or above 0.05 (TB-248-251, TB-265-273, TB-274-295) indicates a systematic rejection of this parameter adjustment across market types. Introducing this threshold would conflict with the established pattern of rejections and risks reintroducing the noise regression that these prior rejections were designed to prevent.

---

## 2026-04-12 — Advisor snapshot 142

### Summary
Your detector is generating false positives from quote-driven volume spikes and low-liquidity market noise, particularly in BTC 15M and golf prop markets, while missing or underweighting genuine signals that lack immediate price confirmation.

### Next step
Implement a trade-execution filter: require that volume delta spikes be accompanied by a minimum ratio of executed trade volume to total quoted volume (e.g., >60% execution rate) to distinguish real order flow from passive liquidity provision.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-434** `rejected` — For BTC 15M markets: raise spike_min_volume_delta multiplier from 6x to 8x baseline, and exclude unmatched quotes from volume calculations.
  - **Governor rejection**: The proposed tweak sets min_price_move: 0.05, which violates the historical constraint 'No spike_min_price_move increases (e.g., no ≥0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected)'. This explicitly rejects increasing the minimum price move threshold to 0.05% or similar values, as previously tightened to prevent missing genuine signals.
- [ ] **TB-435** `rejected` — For low-liquidity prop markets (golf, Trump speech): implement a dual gate—require both volume_delta ≥ 2x baseline AND minimum 5 recent executed trades, plus spike_min_price_move ≥ 0.05 (5%) for Trump speech markets.
  - **Governor rejection**: The proposed tweak sets min_price_move: 0.05, which violates the historical constraint 'No spike_min_price_move increases (e.g., no ≥0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected)'. This explicitly rejects increasing the minimum price move threshold to 0.05% or similar values, as previously tightened to prevent missing genuine signals.
- [ ] **TB-436** `rejected` — Decouple price-move requirements from signal validity: KXTRUMPSAY-26APR13-STUP demonstrates that genuine signals in illiquid markets may have zero immediate price confirmation due to public event lag; consider a secondary 'event-validated' tier that triggers alerts when volume + trade frequency exceed thresholds even if priceΔ = 0.
  - **Governor rejection**: The proposed tweak sets min_price_move: 0.05, which violates the historical constraint 'No spike_min_price_move increases (e.g., no ≥0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%) for BTC 15m/high-freq/whale-cluster markets (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355 rejected)'. This explicitly rejects increasing the minimum price move threshold to 0.05% or similar values, as previously tightened to prevent missing genuine signals.

---

## 2026-04-12 — Advisor snapshot 143

### Summary
False positives are prevalent in low-liquidity markets (Trump speech, golf props) from small trades or quote-driven volume without follow-on trades, and in high-frequency BTC 15M markets from large unexecuted quotes or short-term volatility artifacts, while genuine signals occur with substantial price moves or confirmed event lags.

### Next step
Introduce market-type rules: raise volume multiplier to 2x baseline and price move to 0.10 for low-liquidity/long-dated markets; exclude unmatched quotes from volume delta and require >5 recent trades for BTC 15M.

### Suggested thresholds
`min_price_move` → `0.1`

### Recommendations

- [ ] **TB-437** `rejected` — Raise volume delta multiplier to 2x baseline for golf props and Trump speech markets
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume delta multipliers** (2x baseline for low-liquidity/long-dated markets), which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers (0.5x/1-10x/1-2%/1.5x/2x/2.5x/3x/5-10x/14.9x→15x/25x baseline; low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m/thin/high-freq/ultra-short', explicitly rejected previously. It also raises **spike_min_price_move** to 0.10, conflicting with 'No spike_min_price_move increases (≥0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%; [multiple TBs rejected]'. Additionally, for BTC 15M, requiring >5 recent trades adds a **minimum notional trade size/count filter**, violating 'No minimum notional trade size/USD equivalent filter (USD 500/10k/abs vol >100 contracts; [multiple TBs rejected]'.
- [ ] **TB-438** `rejected` — Require minimum 5 recent trades and exclude large unexecuted quotes from volume delta in BTC 15M markets
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume delta multipliers** (2x baseline for low-liquidity/long-dated markets), which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers (0.5x/1-10x/1-2%/1.5x/2x/2.5x/3x/5-10x/14.9x→15x/25x baseline; low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m/thin/high-freq/ultra-short', explicitly rejected previously. It also raises **spike_min_price_move** to 0.10, conflicting with 'No spike_min_price_move increases (≥0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%; [multiple TBs rejected]'. Additionally, for BTC 15M, requiring >5 recent trades adds a **minimum notional trade size/count filter**, violating 'No minimum notional trade size/USD equivalent filter (USD 500/10k/abs vol >100 contracts; [multiple TBs rejected]'.
- [ ] **TB-439** `rejected` — Increase min_price_move to 0.10 for markets with baseline yes price <0.10
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume delta multipliers** (2x baseline for low-liquidity/long-dated markets), which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers (0.5x/1-10x/1-2%/1.5x/2x/2.5x/3x/5-10x/14.9x→15x/25x baseline; low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m/thin/high-freq/ultra-short', explicitly rejected previously. It also raises **spike_min_price_move** to 0.10, conflicting with 'No spike_min_price_move increases (≥0.005/0.01/0.015/0.02/0.03/0.05/priceΔ>0%; [multiple TBs rejected]'. Additionally, for BTC 15M, requiring >5 recent trades adds a **minimum notional trade size/count filter**, violating 'No minimum notional trade size/USD equivalent filter (USD 500/10k/abs vol >100 contracts; [multiple TBs rejected]'.

---

## 2026-04-12 — Advisor snapshot 144

### Summary
Your detector is generating false positives from quote-driven volume artifacts and liquidity swings in low-volume markets, while missing or under-weighting genuine signals that precede real price movements. Market-specific tuning is needed.

### Next step
Implement market-class segmentation with distinct thresholds: require 8x baseline volume + executed trade confirmation for short-term crypto; 2x baseline + minimum trade count for illiquid props; 2x baseline + 10% price move for long-dated, low-liquidity events. This mirrors the Penalized Spike Accuracy approach—align sensitivity to empirical spike rates per market segment rather than applying uniform thresholds.

### Recommendations

- [ ] **TB-440** `rejected` — For 15-minute crypto (KXBTC15M): Raise volume multiplier to 8x baseline and filter out unmatched quotes; require follow-on executed trade volume to validate spike signals and reduce quote-only noise.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) TB-001 applied (whale-cluster min_volume_delta ≥1000 for 15m BTC) by introducing market-class segmentation with lower multipliers like 2x baseline for illiquid props, relaxing the strict minimum to avoid noise reintroduction; (2) TB-002 applied (spike_score_threshold ≥8.5) by suggesting market-specific adjustments that could reduce thresholds below 8.5 to align sensitivity per segment; (3) TB-003 applied (whale-cluster whale count ≥50 in 120s AND λ=0.01 for 15m BTC) through segmentation that permits looser criteria like 2x baseline + minimum trade count instead of strict whale counts; (4) No market-type-specific volume delta multipliers (explicitly rejected numerous TBs for low-liq/crypto/BTC) by implementing distinct thresholds (8x/2x baseline) per market class (crypto/props/long-dated events); (5) Rejected minimum notional trade size (TB-199 etc.) and volume-to-price-move ratio (TB-200 etc.) by adding executed trade confirmation, minimum trade count, and 10% price move requirements; (6) No spike_min_price_move increases (numerous rejected TBs) contradicted by requiring 10% price move for some segments.
- [ ] **TB-441** `rejected` — For golf props and long-dated events (low liquidity): Require volume delta multiplier ≥2.0x baseline AND minimum of 5 recent trades AND price move ≥2–10% (market-dependent) to distinguish genuine flow from passive liquidity provision.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) TB-001 applied (whale-cluster min_volume_delta ≥1000 for 15m BTC) by introducing market-class segmentation with lower multipliers like 2x baseline for illiquid props, relaxing the strict minimum to avoid noise reintroduction; (2) TB-002 applied (spike_score_threshold ≥8.5) by suggesting market-specific adjustments that could reduce thresholds below 8.5 to align sensitivity per segment; (3) TB-003 applied (whale-cluster whale count ≥50 in 120s AND λ=0.01 for 15m BTC) through segmentation that permits looser criteria like 2x baseline + minimum trade count instead of strict whale counts; (4) No market-type-specific volume delta multipliers (explicitly rejected numerous TBs for low-liq/crypto/BTC) by implementing distinct thresholds (8x/2x baseline) per market class (crypto/props/long-dated events); (5) Rejected minimum notional trade size (TB-199 etc.) and volume-to-price-move ratio (TB-200 etc.) by adding executed trade confirmation, minimum trade count, and 10% price move requirements; (6) No spike_min_price_move increases (numerous rejected TBs) contradicted by requiring 10% price move for some segments.
- [ ] **TB-442** `rejected` — For high-conviction signals (analyst=signal/yes/high): Retain or lower thresholds selectively, as KXTRUMPSAY-26APR13-STUP demonstrates that real signals may have low current price reflection due to public-event lags; tune score_threshold downward for high-confidence analyst labels rather than uniformly raising volume/price thresholds.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) TB-001 applied (whale-cluster min_volume_delta ≥1000 for 15m BTC) by introducing market-class segmentation with lower multipliers like 2x baseline for illiquid props, relaxing the strict minimum to avoid noise reintroduction; (2) TB-002 applied (spike_score_threshold ≥8.5) by suggesting market-specific adjustments that could reduce thresholds below 8.5 to align sensitivity per segment; (3) TB-003 applied (whale-cluster whale count ≥50 in 120s AND λ=0.01 for 15m BTC) through segmentation that permits looser criteria like 2x baseline + minimum trade count instead of strict whale counts; (4) No market-type-specific volume delta multipliers (explicitly rejected numerous TBs for low-liq/crypto/BTC) by implementing distinct thresholds (8x/2x baseline) per market class (crypto/props/long-dated events); (5) Rejected minimum notional trade size (TB-199 etc.) and volume-to-price-move ratio (TB-200 etc.) by adding executed trade confirmation, minimum trade count, and 10% price move requirements; (6) No spike_min_price_move increases (numerous rejected TBs) contradicted by requiring 10% price move for some segments.

---

## 2026-04-12 — Advisor snapshot 145

### Summary
False positives dominate in low-liquidity markets (golf props, Trump speeches, short-term BTC) from quote-driven volume without follow-on trades or significant price moves, while genuine signals show high volume with price impact in event-driven contexts.

### Next step
Add market-type rules: require 2x volume multiplier and >5 trades for low-liquidity props; exclude unmatched quotes from BTC 15m volume delta.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-443** `rejected` — Raise min_price_move to 0.05+ for signals with priceΔ <0.03 to filter noise.
  - **Governor rejection**: The proposed tweak conflicts with multiple historical constraints: (1) Introduces market-type-specific volume multipliers (2x for low-liquidity props), violating 'No market-type-specific volume delta multipliers (e.g., 0.5x/1-10x/1-2x/...)' from TB-XXX rejected tweaks. (2) Adds >5 trades filter, violating 'No minimum notional trade size/USD equivalent filter' (TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378 rejected; blocks low-lot/trade count filters for crypto 15m/low-volume/low-liquidity markets). (3) Sets min_price_move: 0.05, violating 'No spike_min_price_move increases (e.g., ≥0.005/0.01/.../0.05/...)' (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439 rejected; for BTC 15m/high-freq/whale-cluster/low-liq markets). These additions tighten criteria beyond applied whale-cluster rules (TB-001,003) and reintroduce previously rejected filters.
- [ ] **TB-444** `rejected` — Require volume-to-trade ratio > threshold or exclude large unexecuted quotes universally.
  - **Governor rejection**: The proposed tweak conflicts with multiple historical constraints: (1) Introduces market-type-specific volume multipliers (2x for low-liquidity props), violating 'No market-type-specific volume delta multipliers (e.g., 0.5x/1-10x/1-2x/...)' from TB-XXX rejected tweaks. (2) Adds >5 trades filter, violating 'No minimum notional trade size/USD equivalent filter' (TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378 rejected; blocks low-lot/trade count filters for crypto 15m/low-volume/low-liquidity markets). (3) Sets min_price_move: 0.05, violating 'No spike_min_price_move increases (e.g., ≥0.005/0.01/.../0.05/...)' (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439 rejected; for BTC 15m/high-freq/whale-cluster/low-liq markets). These additions tighten criteria beyond applied whale-cluster rules (TB-001,003) and reintroduce previously rejected filters.
- [ ] **TB-445** `rejected` — Set market-specific volume multipliers: 8x baseline for BTC 15m, 2x for golf/Trump props.
  - **Governor rejection**: The proposed tweak conflicts with multiple historical constraints: (1) Introduces market-type-specific volume multipliers (2x for low-liquidity props), violating 'No market-type-specific volume delta multipliers (e.g., 0.5x/1-10x/1-2x/...)' from TB-XXX rejected tweaks. (2) Adds >5 trades filter, violating 'No minimum notional trade size/USD equivalent filter' (TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378 rejected; blocks low-lot/trade count filters for crypto 15m/low-volume/low-liquidity markets). (3) Sets min_price_move: 0.05, violating 'No spike_min_price_move increases (e.g., ≥0.005/0.01/.../0.05/...)' (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439 rejected; for BTC 15m/high-freq/whale-cluster/low-liq markets). These additions tighten criteria beyond applied whale-cluster rules (TB-001,003) and reintroduce previously rejected filters.

---

## 2026-04-12 — Advisor snapshot 146

### Summary
False positives are prevalent in low-liquidity markets like golf props, Trump speech bets, and short-term BTC due to quote-driven volume spikes without sustained trades or significant price moves, while genuine signals show larger price deltas in Trump markets.

### Next step
Introduce market-type rules: raise volume multiplier to 2x baseline and require price move >0.05 or >5 recent trades for low-liquidity props; exclude unmatched quotes from BTC volume delta.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-446** `rejected` — Raise volume delta multiplier to 2x baseline for golf and Trump speech markets
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introduces **market-type-specific volume delta multipliers** (raise volume multiplier to 2x baseline for low-liquidity props), conflicting with TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336,340 which rejected such multipliers. (2) Adds **minimum notional trade size/USD equivalent/trade count filters** (>5 recent trades for low-liquidity props), conflicting with TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378,412,422 which rejected trade count filters like >2/>5 trades. (3) Introduces **spike_min_price_move increases** (min_price_move: 0.05 for low-liquidity markets), conflicting with TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-444 which rejected price move thresholds like ≥0.05 for low-liq/thin markets.
- [ ] **TB-447** `rejected` — Require minimum 5 recent trades or higher volume-to-trade ratio to filter quote noise
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introduces **market-type-specific volume delta multipliers** (raise volume multiplier to 2x baseline for low-liquidity props), conflicting with TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336,340 which rejected such multipliers. (2) Adds **minimum notional trade size/USD equivalent/trade count filters** (>5 recent trades for low-liquidity props), conflicting with TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378,412,422 which rejected trade count filters like >2/>5 trades. (3) Introduces **spike_min_price_move increases** (min_price_move: 0.05 for low-liquidity markets), conflicting with TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-444 which rejected price move thresholds like ≥0.05 for low-liq/thin markets.
- [ ] **TB-448** `rejected` — Increase min_price_move to 0.05 for watch tier signals
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introduces **market-type-specific volume delta multipliers** (raise volume multiplier to 2x baseline for low-liquidity props), conflicting with TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336,340 which rejected such multipliers. (2) Adds **minimum notional trade size/USD equivalent/trade count filters** (>5 recent trades for low-liquidity props), conflicting with TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378,412,422 which rejected trade count filters like >2/>5 trades. (3) Introduces **spike_min_price_move increases** (min_price_move: 0.05 for low-liquidity markets), conflicting with TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-444 which rejected price move thresholds like ≥0.05 for low-liq/thin markets.

---

## 2026-04-12 — Advisor snapshot 147

### Summary
Your detector is generating false positives primarily in low-liquidity markets (golf props, long-dated political markets) and quote-driven artifacts (15-minute BTC) where volume spikes lack genuine trading conviction. The core issue is that volume delta alone, without trade execution validation, triggers false alerts on passive liquidity provision and isolated large quotes.

### Next step
Implement a trade-execution filter: require that volume delta spikes be accompanied by a minimum number of actual matched trades (e.g., ≥5 recent trades) or a minimum trade-to-quote ratio, rather than relying on volume delta as a standalone signal. This directly addresses the pattern where large unexecuted quotes and quote-only noise dominate false positives.

### Suggested thresholds
`min_price_move` → `0.1`

### Recommendations

- [ ] **TB-449** `rejected` — For golf prop and low-liquidity markets, raise spike_min_volume_delta to 1.5x–2.0x baseline and mandate ≥5 recent matched trades within the spike window to filter quote-driven churn.
  - **Governor rejection**: The proposed tweak violates TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378,412,422 by introducing a 'minimum number of actual matched trades (e.g., ≥5 recent trades)' filter, which is explicitly rejected as a minimum notional trade size/USD equivalent/abs volume filter or small-trade filter for crypto 15m/low-volume/low-liquidity/thin markets.
- [ ] **TB-450** `rejected` — For 15-minute BTC and other high-frequency markets, increase the volume-to-matched-trade ratio requirement or exclude passive quotes from volume delta calculations to prevent quote-only artifacts from triggering alerts.
  - **Governor rejection**: The proposed tweak violates TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378,412,422 by introducing a 'minimum number of actual matched trades (e.g., ≥5 recent trades)' filter, which is explicitly rejected as a minimum notional trade size/USD equivalent/abs volume filter or small-trade filter for crypto 15m/low-volume/low-liquidity/thin markets.
- [ ] **TB-451** `rejected` — For long-dated, low-liquidity political markets (Trump speech props), set spike_min_price_move ≥0.10 (10%) or require volume delta multiplier ≥2.0x baseline plus trade execution confirmation to reduce noise from small isolated trades.
  - **Governor rejection**: The proposed tweak violates TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378,412,422 by introducing a 'minimum number of actual matched trades (e.g., ≥5 recent trades)' filter, which is explicitly rejected as a minimum notional trade size/USD equivalent/abs volume filter or small-trade filter for crypto 15m/low-volume/low-liquidity/thin markets.

---

## 2026-04-12 — Advisor snapshot 148

### Summary
False positives are driven by quote-level churning and large unexecuted quotes in low-liquidity golf prop markets and high-volatility short-term BTC markets, despite varying volume deltas and minimal price moves.

### Next step
Introduce market-type rules: raise volume multiplier to 2x+ baseline for golf props and 8x for 15m BTC, while excluding unexecuted quotes from delta calculations.

### Suggested thresholds
`min_volume_delta` → `100000.0`, `min_price_move` → `0.03`, `score_threshold` → `4.0`

### Recommendations

- [ ] **TB-452** `rejected` — Raise spike_min_volume_delta to 100000 for golf scoring markets to filter quote churning.
  - **Governor rejection**: The proposed tweak violates TB-002 (applied: Increase spike_score_threshold to 8.5 to reduce low-confidence triggers) by lowering score_threshold to 4.0, which relaxes a threshold explicitly tightened to reduce noise and false positives.
- [ ] **TB-453** `rejected` — Require min_price_move >0.03 for watch tier signals with zero price delta.
  - **Governor rejection**: The proposed tweak violates TB-002 (applied: Increase spike_score_threshold to 8.5 to reduce low-confidence triggers) by lowering score_threshold to 4.0, which relaxes a threshold explicitly tightened to reduce noise and false positives.
- [ ] **TB-454** `rejected` — Increase spike_score_threshold to 4.0 to suppress low-confidence uncertain/noise signals.
  - **Governor rejection**: The proposed tweak violates TB-002 (applied: Increase spike_score_threshold to 8.5 to reduce low-confidence triggers) by lowering score_threshold to 4.0, which relaxes a threshold explicitly tightened to reduce noise and false positives.

---

## 2026-04-12 — Advisor snapshot 149

### Summary
Your detector is generating false positives in low-liquidity markets (golf props, short-term crypto) where quote-level activity and isolated large orders create inflated volume signals without corresponding sustained trading interest or meaningful price discovery.

### Next step
Implement market-class-specific volume multipliers: require 8x baseline for high-volatility short-term markets (15m crypto), 2.0x for low-liquidity props (golf), and add a follow-on trade confirmation rule to filter quote-driven artifacts.

### Recommendations

- [ ] **TB-455** `rejected` — For golf scoring props: raise spike_min_volume_delta to 2.0x baseline multiplier and require minimum 5 recent trades within the spike window to confirm sustained interest beyond quote churn
  - **Governor rejection**: The proposed tweak violates the historical constraint 'No market-type-specific volume delta multipliers' (TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336,340,343-34X rejected), as it explicitly introduces market-class-specific volume multipliers (e.g., 8x baseline for high-volatility short-term markets like 15m crypto, 2.0x for low-liquidity props like golf).
- [ ] **TB-456** `rejected` — For 15-minute crypto markets: increase volume multiplier from 6x to 8x baseline, or add a secondary filter rejecting isolated quotes unmatched by subsequent trade volume
  - **Governor rejection**: The proposed tweak violates the historical constraint 'No market-type-specific volume delta multipliers' (TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336,340,343-34X rejected), as it explicitly introduces market-class-specific volume multipliers (e.g., 8x baseline for high-volatility short-term markets like 15m crypto, 2.0x for low-liquidity props like golf).
- [ ] **TB-457** `rejected` — For low-price-move signals (≤0.02 fractional): require proportionally higher volume delta or cross-check against order book depth to distinguish genuine pressure from liquidity-driven microstructure noise
  - **Governor rejection**: The proposed tweak violates the historical constraint 'No market-type-specific volume delta multipliers' (TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-336,340,343-34X rejected), as it explicitly introduces market-class-specific volume multipliers (e.g., 8x baseline for high-volatility short-term markets like 15m crypto, 2.0x for low-liquidity props like golf).

---

## 2026-04-12 — Advisor snapshot 150

### Summary
False positives are prominent in low-liquidity markets like golf props and high-volatility BTC 15m markets, where volume spikes are driven by quote churning or isolated large quotes without sustained trading or significant price moves.

### Next step
Introduce market-type rules: raise volume multiplier to 8x+ baseline for BTC 15m and 1.5-2x for golf props; require priceΔ >0.05 and >5 recent trades globally.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-458** `rejected` — Raise spike_min_volume_delta or baseline multiplier to 8x for BTC 15m markets to filter quote-driven artifacts.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introduces **market-type-specific volume delta multipliers** (8x+ for BTC 15m, 1.5-2x for golf props), explicitly rejected (e.g., TB-XXX for low-liq markets); (2) Increases **spike_min_price_move** to >0.05, rejected in numerous TBs (e.g., TB-210,213,216-219, etc., for BTC 15m/high-freq/low-liq); (3) Adds **minimum notional/USD trade size/abs volume/trade count filters** via '>5 recent trades globally', rejected (e.g., TB-199,204, etc.).
- [ ] **TB-459** `rejected` — Set volume threshold to 1.5x+ baseline for golf scoring markets and require >5 recent trades.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introduces **market-type-specific volume delta multipliers** (8x+ for BTC 15m, 1.5-2x for golf props), explicitly rejected (e.g., TB-XXX for low-liq markets); (2) Increases **spike_min_price_move** to >0.05, rejected in numerous TBs (e.g., TB-210,213,216-219, etc., for BTC 15m/high-freq/low-liq); (3) Adds **minimum notional/USD trade size/abs volume/trade count filters** via '>5 recent trades globally', rejected (e.g., TB-199,204, etc.).
- [ ] **TB-460** `rejected` — Increase spike_min_price_move to 0.05 to ensure moves exceed noise levels.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introduces **market-type-specific volume delta multipliers** (8x+ for BTC 15m, 1.5-2x for golf props), explicitly rejected (e.g., TB-XXX for low-liq markets); (2) Increases **spike_min_price_move** to >0.05, rejected in numerous TBs (e.g., TB-210,213,216-219, etc., for BTC 15m/high-freq/low-liq); (3) Adds **minimum notional/USD trade size/abs volume/trade count filters** via '>5 recent trades globally', rejected (e.g., TB-199,204, etc.).

---

## 2026-04-12 — Advisor snapshot 151

### Summary
False positives are prevalent in low-liquidity markets like golf props and high-volatility BTC 15M markets, where volume spikes are driven by quote churning or isolated large quotes rather than sustained trading interest.

### Next step
Introduce market-type specific volume multipliers (e.g., 8x baseline for BTC 15M, 1.5-2x for golf props) to filter artifact-driven spikes.

### Recommendations

- [ ] **TB-461** `rejected` — Raise volume-delta threshold to 1.5x+ baseline for golf scoring markets to filter quote-level churning.
  - **Governor rejection**: The proposed tweak introduces market-type-specific volume multipliers (e.g., 8x baseline for BTC 15M), which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers' (TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-33 rejected).
- [ ] **TB-462** `rejected` — Require BTC 15M volume spikes to exceed 8x baseline or confirm with follow-on trade volume.
  - **Governor rejection**: The proposed tweak introduces market-type-specific volume multipliers (e.g., 8x baseline for BTC 15M), which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers' (TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-33 rejected).
- [ ] **TB-463** `rejected` — Raise volume threshold to 2x baseline for low-liquidity golf prop markets.
  - **Governor rejection**: The proposed tweak introduces market-type-specific volume multipliers (e.g., 8x baseline for BTC 15M), which directly conflicts with the historical constraint 'No market-type-specific volume delta multipliers' (TB-220,221,232-237,244-247,250,278,285,291,295-298,303,305,310,316-319,325-330,334-33 rejected).

---

## 2026-04-12 — Advisor snapshot 152

### Summary
False positives occur in low-liquidity markets like golf props from quote churning and in high-volatility short-term markets like BTC from isolated large quotes, despite moderate volume deltas and small price moves.

### Next step
Introduce market-type rules: raise volume multiplier to 8x+ for BTC 15M and 1.5x+ for golf props; require sustained follow-on volume after spikes.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-464** `planned` — Raise spike_min_volume_delta to 150000+ for golf scoring markets to filter quote-level churning.
- [ ] **TB-465** `planned` — Increase volume spike multiplier to 8x baseline for 15-minute BTC markets and filter isolated unmatched quotes.
- [ ] **TB-466** `planned` — Require priceΔ > 0.03 for watch-tier signals in low-liquidity props to ensure meaningful moves.

---

## 2026-04-12 — Advisor snapshot 153

### Summary
False positives are concentrated in short-duration illiquid markets like 15-minute BTC and golf scoring, where small trades, quote churning, or isolated large quotes trigger detections without sustained interest.

### Next step
Add market-specific volume filters: absolute min volume >100 contracts for 15min markets; raise volΔ multiplier to 8x baseline for BTC 15min; 1.5x+ baseline for golf scoring.

### Recommendations

- [ ] **TB-467** `rejected` — For 15-minute micro-duration markets, require absolute volume >100 contracts to filter single small trades.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introduces 'absolute min volume >100 contracts for 15min markets', conflicting with 'No minimum notional trade size/USD equivalent/abs volume filters (e.g., $500/$10k/>100 contracts; rejected TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378,412,422,449-451)'. (2) Adds 'raise volΔ multiplier to 8x baseline for BTC 15min', conflicting with 'No market-type-specific volume delta multipliers (e.g., 0.5x/1-10x/.../BTC 15min/crypto; ... rejected TB-...)'.
- [ ] **TB-468** `rejected` — For BTC 15min markets, increase volume spike to 8x baseline or filter isolated unmatched quotes.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introduces 'absolute min volume >100 contracts for 15min markets', conflicting with 'No minimum notional trade size/USD equivalent/abs volume filters (e.g., $500/$10k/>100 contracts; rejected TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378,412,422,449-451)'. (2) Adds 'raise volΔ multiplier to 8x baseline for BTC 15min', conflicting with 'No market-type-specific volume delta multipliers (e.g., 0.5x/1-10x/.../BTC 15min/crypto; ... rejected TB-...)'.
- [ ] **TB-469** `rejected` — For golf scoring markets, raise volume-delta threshold to 1.5x+ baseline to ignore quote churning.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) Introduces 'absolute min volume >100 contracts for 15min markets', conflicting with 'No minimum notional trade size/USD equivalent/abs volume filters (e.g., $500/$10k/>100 contracts; rejected TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378,412,422,449-451)'. (2) Adds 'raise volΔ multiplier to 8x baseline for BTC 15min', conflicting with 'No market-type-specific volume delta multipliers (e.g., 0.5x/1-10x/.../BTC 15min/crypto; ... rejected TB-...)'.

---

## 2026-04-12 — Advisor snapshot 154

### Summary
False positives are prominent in short-duration BTC markets and golf scoring markets due to small trades on illiquid books and quote churning mimicking volume spikes, despite varying price moves and scores.

### Next step
Introduce market-type-specific volume filters: absolute min volume >100 for 15m markets, 1.5x+ baseline delta for golf markets.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-470** `rejected` — For 15-minute BTC markets, require volume spikes >8x baseline or add absolute volume threshold >100 contracts.
  - **Governor rejection**: The proposed 'absolute min volume >100 for 15m markets' violates the historical constraint 'No minimum notional/USD trade size/abs volume/trade count filters' (TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378,412,422,449-451,467-469 rejected), which explicitly blocks absolute minimum volume filters for crypto 15m/low-liq/thin markets. Additionally, 'min_price_move: 0.03' conflicts with 'No spike_min_price_move increases' (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445 rejected), as it raises the minimum price move threshold beyond previously rejected increases like ≥0.005/0.01/0.015/0.02/0.03.
- [ ] **TB-471** `rejected` — For golf scoring markets, raise volume-delta threshold to 1.5x+ baseline to filter quote churning.
  - **Governor rejection**: The proposed 'absolute min volume >100 for 15m markets' violates the historical constraint 'No minimum notional/USD trade size/abs volume/trade count filters' (TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378,412,422,449-451,467-469 rejected), which explicitly blocks absolute minimum volume filters for crypto 15m/low-liq/thin markets. Additionally, 'min_price_move: 0.03' conflicts with 'No spike_min_price_move increases' (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445 rejected), as it raises the minimum price move threshold beyond previously rejected increases like ≥0.005/0.01/0.015/0.02/0.03.
- [ ] **TB-472** `rejected` — Require minimum absolute volume threshold across illiquid markets to exclude single small trade spikes.
  - **Governor rejection**: The proposed 'absolute min volume >100 for 15m markets' violates the historical constraint 'No minimum notional/USD trade size/abs volume/trade count filters' (TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378,412,422,449-451,467-469 rejected), which explicitly blocks absolute minimum volume filters for crypto 15m/low-liq/thin markets. Additionally, 'min_price_move: 0.03' conflicts with 'No spike_min_price_move increases' (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445 rejected), as it raises the minimum price move threshold beyond previously rejected increases like ≥0.005/0.01/0.015/0.02/0.03.

---

## 2026-04-12 — Advisor snapshot 155

### Summary
False positives are prominent in short-duration BTC markets and golf scoring markets due to small trades on illiquid books and quote churning, despite high volume deltas and low price moves.

### Next step
Introduce market-type-specific volume filters: absolute volume >100 for 15-min BTC markets and 1.5x baseline delta for golf scoring markets.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-473** `rejected` — Require minimum absolute volume threshold (e.g., >100 contracts) for illiquid short-duration markets to filter single-trade spikes.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume filters** ('absolute volume >100 for 15-min BTC markets and 1.5x baseline delta for golf scoring markets'), which directly violates the active rejected constraint '**No market-type-specific volume delta multipliers** for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m (blocks 0.5x/1-10x/1.5x/2x/2.5x/3x/5-10x/14.9x→15x/25x baseline adjustments)'. The 1.5x baseline delta for golf and absolute volume >100 for BTC 15m are exactly the type of market-specific volume adjustments explicitly blocked.
- [ ] **TB-474** `rejected` — Raise volume delta multiplier to 8x baseline for high-volatility 15-min BTC markets.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume filters** ('absolute volume >100 for 15-min BTC markets and 1.5x baseline delta for golf scoring markets'), which directly violates the active rejected constraint '**No market-type-specific volume delta multipliers** for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m (blocks 0.5x/1-10x/1.5x/2x/2.5x/3x/5-10x/14.9x→15x/25x baseline adjustments)'. The 1.5x baseline delta for golf and absolute volume >100 for BTC 15m are exactly the type of market-specific volume adjustments explicitly blocked.
- [ ] **TB-475** `rejected` — Increase min_price_move to 0.03 for watch/notable tiers to exclude low-impact moves.
  - **Governor rejection**: The proposed tweak introduces **market-type-specific volume filters** ('absolute volume >100 for 15-min BTC markets and 1.5x baseline delta for golf scoring markets'), which directly violates the active rejected constraint '**No market-type-specific volume delta multipliers** for low-liq/pre-game/golf props/NBA/sports winners/crypto/BTC 15m (blocks 0.5x/1-10x/1.5x/2x/2.5x/3x/5-10x/14.9x→15x/25x baseline adjustments)'. The 1.5x baseline delta for golf and absolute volume >100 for BTC 15m are exactly the type of market-specific volume adjustments explicitly blocked.

---

## 2026-04-12 — Advisor snapshot 156

### Summary
The detector is generating false positives on low-liquidity, short-duration markets (15-minute prediction markets and niche contracts) where microstructure noise—single large trades or quote-level activity without sustained momentum—trigger alerts. Price moves are minimal (0.0–0.02) while volume deltas alone drive high scores, misclassifying noise as signal.

### Next step
Implement market-aware thresholds that require concurrent price-volume confirmation: on illiquid markets, require minimum absolute volume (>100 contracts) AND price move >1.5% OR volume delta >1.5x baseline to filter single-trade spikes.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.015`, `score_threshold` → `4.0`

### Recommendations

- [ ] **TB-476** `rejected` — For 15-minute markets and watch-tier tokens, require priceΔ ≥ 0.015 (1.5%) when volΔ < 500, to eliminate volume-only false positives on low-liquidity orderbooks.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) TB-002 applied requires spike_score_threshold ≥8.5 with no reductions, but suggests score_threshold: 4.0 (≤4.0 explicitly rejected); (2) Introduces minimum absolute volume (>100 contracts) filter, rejected by TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378,412,422,449-451,467-469 (blocks min notional/volume/trade count filters); (3) Introduces volume delta >1.5x baseline ratio threshold, rejected by TB-200,202,208,211,214,255-257 (blocks volume-to-price-move ratio thresholds); (4) Sets min_price_move: 0.015, blocked by TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445 (no spike_min_price_move increases ≥0.005/0.01/0.015).
- [ ] **TB-477** `rejected` — Add absolute volume gate: reject signals where volΔ ≥ 500 but absolute trade count < 15 in 120s window (per analyst note on KXBTC15M-26APR121715-15).
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) TB-002 applied requires spike_score_threshold ≥8.5 with no reductions, but suggests score_threshold: 4.0 (≤4.0 explicitly rejected); (2) Introduces minimum absolute volume (>100 contracts) filter, rejected by TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378,412,422,449-451,467-469 (blocks min notional/volume/trade count filters); (3) Introduces volume delta >1.5x baseline ratio threshold, rejected by TB-200,202,208,211,214,255-257 (blocks volume-to-price-move ratio thresholds); (4) Sets min_price_move: 0.015, blocked by TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445 (no spike_min_price_move increases ≥0.005/0.01/0.015).
- [ ] **TB-478** `rejected` — For niche markets (golf scores, event predictions), raise volΔ threshold to 1.5x+ rolling baseline rather than fixed thresholds, as quote-level churn is common.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) TB-002 applied requires spike_score_threshold ≥8.5 with no reductions, but suggests score_threshold: 4.0 (≤4.0 explicitly rejected); (2) Introduces minimum absolute volume (>100 contracts) filter, rejected by TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378,412,422,449-451,467-469 (blocks min notional/volume/trade count filters); (3) Introduces volume delta >1.5x baseline ratio threshold, rejected by TB-200,202,208,211,214,255-257 (blocks volume-to-price-move ratio thresholds); (4) Sets min_price_move: 0.015, blocked by TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445 (no spike_min_price_move increases ≥0.005/0.01/0.015).
- [ ] **TB-479** `rejected` — Lower score_threshold for high-volume, high-price-move signals (e.g., KXPGAROUNDSCORE at volΔ=8076, priceΔ=0.02 was correctly labeled signal/yes with score=2.0), while raising it for price-weak signals.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) TB-002 applied requires spike_score_threshold ≥8.5 with no reductions, but suggests score_threshold: 4.0 (≤4.0 explicitly rejected); (2) Introduces minimum absolute volume (>100 contracts) filter, rejected by TB-199,204,206,265-267,276-283,286,289,294,297,280,358-360,364-366,370-372,378,412,422,449-451,467-469 (blocks min notional/volume/trade count filters); (3) Introduces volume delta >1.5x baseline ratio threshold, rejected by TB-200,202,208,211,214,255-257 (blocks volume-to-price-move ratio thresholds); (4) Sets min_price_move: 0.015, blocked by TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445 (no spike_min_price_move increases ≥0.005/0.01/0.015).

---

## 2026-04-12 — Advisor snapshot 157

### Summary
False positives in whale-cluster signals on high-frequency BTC 15m markets are driven by low volume deltas (sub-0.5x baseline), small price moves (~1%), and insufficient whale counts, allowing microstructure noise and HFT bursts to trigger alerts.

### Next step
Raise whale-cluster detection threshold to require volume delta >0.5x baseline AND 15+ whales in 120s window for 15m markets.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-480** `rejected` — Require volume delta to exceed 0.5x baseline or absolute trade count >15 in 120s for whale-cluster signals
  - **Governor rejection**: The proposed tweak violates TB-001. TB-001 explicitly applied a constraint requiring whale-cluster min_volume_delta ≥1000 for 15m BTC with no relaxations below this threshold. The recommendation to lower min_volume_delta to 500.0 directly contradicts this historical constraint by reducing the threshold by 50%, which constitutes a prohibited relaxation of a previously tightened rule.
- [ ] **TB-481** `rejected` — Raise whale-cluster threshold to 15+ whales in 120s for high-frequency BTC 15m markets
  - **Governor rejection**: The proposed tweak violates TB-001. TB-001 explicitly applied a constraint requiring whale-cluster min_volume_delta ≥1000 for 15m BTC with no relaxations below this threshold. The recommendation to lower min_volume_delta to 500.0 directly contradicts this historical constraint by reducing the threshold by 50%, which constitutes a prohibited relaxation of a previously tightened rule.
- [ ] **TB-482** `rejected` — Implement minimum absolute volume threshold (>100 contracts) for 15-minute micro-duration markets
  - **Governor rejection**: The proposed tweak violates TB-001. TB-001 explicitly applied a constraint requiring whale-cluster min_volume_delta ≥1000 for 15m BTC with no relaxations below this threshold. The recommendation to lower min_volume_delta to 500.0 directly contradicts this historical constraint by reducing the threshold by 50%, which constitutes a prohibited relaxation of a previously tightened rule.

---

## 2026-04-12 — Advisor snapshot 158

### Summary
Your detector is generating false positives in high-frequency, low-liquidity microstructures (15-minute BTC and golf markets) where volume spikes lack corresponding price movement, and in illiquid orderbooks where single trades trigger outsized signals. The pattern suggests your current thresholds conflate microstructure noise with genuine informed flow.

### Next step
Implement a dual-gate filter: require either sustained price impact (priceΔ ≥ 0.02 for BTC 15m) OR absolute volume threshold (>100 contracts) to qualify signals, combined with dynamic volume-delta baselines tied to market liquidity profiles rather than fixed deltas.

### Suggested thresholds
`min_volume_delta` → `0.5`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-483** `rejected` — For whale-cluster tier on BTC 15m: raise spike_min_volume_delta to 0.5x baseline or absolute trade count >15 in 120s window to filter microstructure noise in short-duration markets
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-001 applied** by relaxing volume delta to 'min_volume_delta: 0.5' (far below the required ≥1000 for 15m BTC, explicitly no relaxations like 300k/500/750); (2) **TB-210 etc. (No spike_min_price_move increases)** inversely by introducing a new 'min_price_move: 0.01' requirement (adding price move gate ≥0.01, conflicting with blocks on ≥0.005/0.01 etc. for BTC 15m); (3) **No volume-to-price-move ratio thresholds (TB-200 etc.)** and **No minimum notional/volume filters (TB-199 etc.)** by implementing 'dual-gate filter' requiring priceΔ ≥0.02 OR >100 contracts, and dynamic volume-delta baselines (new ratio/volume/price joint confirmation explicitly rejected); (4) **TB-200,202,208 etc.** directly blocks volΔ/priceΔ joint thresholds like this dual-gate.
- [ ] **TB-484** `rejected` — For micro-cap and illiquid markets: add minimum absolute volume gate (e.g., >100 contracts per signal) to prevent single-trade artifacts from triggering high scores
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-001 applied** by relaxing volume delta to 'min_volume_delta: 0.5' (far below the required ≥1000 for 15m BTC, explicitly no relaxations like 300k/500/750); (2) **TB-210 etc. (No spike_min_price_move increases)** inversely by introducing a new 'min_price_move: 0.01' requirement (adding price move gate ≥0.01, conflicting with blocks on ≥0.005/0.01 etc. for BTC 15m); (3) **No volume-to-price-move ratio thresholds (TB-200 etc.)** and **No minimum notional/volume filters (TB-199 etc.)** by implementing 'dual-gate filter' requiring priceΔ ≥0.02 OR >100 contracts, and dynamic volume-delta baselines (new ratio/volume/price joint confirmation explicitly rejected); (4) **TB-200,202,208 etc.** directly blocks volΔ/priceΔ joint thresholds like this dual-gate.
- [ ] **TB-485** `rejected` — For golf and low-liquidity scoring markets: raise spike_min_volume_delta to 1.5x baseline to distinguish quote-level churning from genuine order flow
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-001 applied** by relaxing volume delta to 'min_volume_delta: 0.5' (far below the required ≥1000 for 15m BTC, explicitly no relaxations like 300k/500/750); (2) **TB-210 etc. (No spike_min_price_move increases)** inversely by introducing a new 'min_price_move: 0.01' requirement (adding price move gate ≥0.01, conflicting with blocks on ≥0.005/0.01 etc. for BTC 15m); (3) **No volume-to-price-move ratio thresholds (TB-200 etc.)** and **No minimum notional/volume filters (TB-199 etc.)** by implementing 'dual-gate filter' requiring priceΔ ≥0.02 OR >100 contracts, and dynamic volume-delta baselines (new ratio/volume/price joint confirmation explicitly rejected); (4) **TB-200,202,208 etc.** directly blocks volΔ/priceΔ joint thresholds like this dual-gate.
- [ ] **TB-486** `rejected` — Require priceΔ ≥ 0.01 (or ≥ 0.02 for BTC 15m) as a secondary confirmation gate—signals with zero price move and moderate volume should downweight or require additional corroboration
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-001 applied** by relaxing volume delta to 'min_volume_delta: 0.5' (far below the required ≥1000 for 15m BTC, explicitly no relaxations like 300k/500/750); (2) **TB-210 etc. (No spike_min_price_move increases)** inversely by introducing a new 'min_price_move: 0.01' requirement (adding price move gate ≥0.01, conflicting with blocks on ≥0.005/0.01 etc. for BTC 15m); (3) **No volume-to-price-move ratio thresholds (TB-200 etc.)** and **No minimum notional/volume filters (TB-199 etc.)** by implementing 'dual-gate filter' requiring priceΔ ≥0.02 OR >100 contracts, and dynamic volume-delta baselines (new ratio/volume/price joint confirmation explicitly rejected); (4) **TB-200,202,208 etc.** directly blocks volΔ/priceΔ joint thresholds like this dual-gate.

---

## 2026-04-12 — Advisor snapshot 159

### Summary
The detector is generating false positives primarily in high-frequency BTC 15-minute markets due to microstructure noise and low-liquidity spikes that lack sustained price impact. Whale-cluster signals with moderate volume deltas (300-500 range) and zero or minimal price moves are frequently mislabeled as informative flow.

### Next step
Implement a minimum absolute volume threshold (>100 contracts) combined with a volume-delta baseline multiplier (0.5x minimum) specifically for whale-cluster tier on 15-minute markets to filter noise-driven spikes while preserving genuine informed flow.

### Suggested thresholds
`min_volume_delta` → `500.0`

### Recommendations

- [ ] **TB-487** `planned` — For whale-cluster tier on KXBTC15M markets: require volΔ ≥ 500 or absolute trade count ≥ 15 in 120s window to reduce false positives from sub-0.2x baseline spikes
- [ ] **TB-488** `planned` — For all high-frequency markets with small contract sizes: add minimum absolute volume filter (e.g., >100 contracts) to reject single-trade spikes on illiquid books
- [ ] **TB-489** `planned` — For low-liquidity prediction markets (golf scoring, niche contracts): raise volume-delta threshold to 1.5x+ baseline to filter quote-level churning unrelated to genuine trading interest

---

## 2026-04-12 — Advisor snapshot 160

### Summary
Whale-cluster signals on KXBTC15M-26APR121715-15 show frequent false positives at low volume deltas (<500) and zero price moves, often labeled as noise/unclear/low, while higher volume deltas (≥500) correlate more with true signals.

### Next step
Raise spike_min_volume_delta to 500 and require at least 0.01 price move for whale-cluster tier in 15m BTC markets to filter microstructure noise and HFT bursts.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-490** `rejected` — Require volume delta ≥0.5x baseline (approx 500) for whale-cluster triggers
  - **Governor rejection**: The proposed tweak violates TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445,476-479 (No spike_min_price_move increases; blocks ≥0.005/0.01/0.015/0.02/0.03/0.05/0.10/priceΔ>0% for BTC 15m/high-freq/whale-cluster) by requiring at least 0.01 price move, which is an explicit increase/restriction on spike_min_price_move that was repeatedly rejected.
- [ ] **TB-491** `rejected` — Add minimum 15 whales in 120s window for high-frequency 15m markets
  - **Governor rejection**: The proposed tweak violates TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445,476-479 (No spike_min_price_move increases; blocks ≥0.005/0.01/0.015/0.02/0.03/0.05/0.10/priceΔ>0% for BTC 15m/high-freq/whale-cluster) by requiring at least 0.01 price move, which is an explicit increase/restriction on spike_min_price_move that was repeatedly rejected.
- [ ] **TB-492** `rejected` — Implement absolute volume threshold >100 contracts for micro-duration markets
  - **Governor rejection**: The proposed tweak violates TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445,476-479 (No spike_min_price_move increases; blocks ≥0.005/0.01/0.015/0.02/0.03/0.05/0.10/priceΔ>0% for BTC 15m/high-freq/whale-cluster) by requiring at least 0.01 price move, which is an explicit increase/restriction on spike_min_price_move that was repeatedly rejected.

---

## 2026-04-12 — Advisor snapshot 161

### Summary
Whale-cluster signals trigger frequent false positives with low volume deltas (<500) and minimal or no price moves, often labeled as noise/unclear/low due to market microstructure noise and HFT bursts in 15m BTC futures, while higher volume deltas (≥500) correlate more with true signals.

### Next step
Raise min_volume_delta to 500 for whale-cluster tier in 15m high-frequency markets to filter sub-0.5x baseline noise.

### Suggested thresholds
`min_volume_delta` → `500.0`

### Recommendations

- [ ] **TB-493** `planned` — Require volume delta ≥500 or 0.5x baseline for whale-cluster triggers
- [ ] **TB-494** `planned` — Increase whale-cluster threshold to 15+ whales in 120s window
- [ ] **TB-495** `planned` — Add absolute trade count >15 in 120s or min volume >100 contracts for micro-duration markets

---

## 2026-04-12 — Advisor snapshot 162

### Summary
The whale-cluster detector on KXBTC15M is generating false positives on volume-only spikes (priceΔ=0.0) without corresponding price movement, while missing some genuine signals. Analyst feedback consistently recommends raising volume delta thresholds to filter microstructure noise in 15-minute prediction markets.

### Next step
Require volume delta ≥500 (0.5x baseline) AND either priceΔ≥0.01 or absolute whale count ≥15 in 120s window to eliminate volume-only false positives while preserving high-conviction informed trades.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-496** `rejected` — Raise spike_min_volume_delta from current baseline to 500+, since signals below this threshold show mixed analyst labels and correlate with noise/unclear ratings
  - **Governor rejection**: The proposed tweak violates TB-001 applied (whale-cluster volume delta threshold ≥1000 for 15m BTC, no relaxations below e.g. 300k/500/750) by setting min_volume_delta: 500.0, which is a 0.5x relaxation below the protected minimum of 1000. It also violates 'No market-type-specific volume delta multipliers (e.g. 0.5x/1-1' by introducing a 0.5x baseline multiplier for KXBTC15M. Additionally, it introduces min_price_move: 0.01, conflicting with 'No spike_min_price_move increases (e.g. ≥0.005/0.01/...)' which rejected ≥0.01 thresholds, and adds absolute whale count ≥15 in 120s, relaxing TB-003 applied (whale-cluster whale count ≥50 in 120s).
- [ ] **TB-497** `rejected` — Add price-movement OR whale-count gating: emit signal only if (priceΔ≥0.01) OR (whale_count_120s≥15), to filter out pure volume events without market impact
  - **Governor rejection**: The proposed tweak violates TB-001 applied (whale-cluster volume delta threshold ≥1000 for 15m BTC, no relaxations below e.g. 300k/500/750) by setting min_volume_delta: 500.0, which is a 0.5x relaxation below the protected minimum of 1000. It also violates 'No market-type-specific volume delta multipliers (e.g. 0.5x/1-1' by introducing a 0.5x baseline multiplier for KXBTC15M. Additionally, it introduces min_price_move: 0.01, conflicting with 'No spike_min_price_move increases (e.g. ≥0.005/0.01/...)' which rejected ≥0.01 thresholds, and adds absolute whale count ≥15 in 120s, relaxing TB-003 applied (whale-cluster whale count ≥50 in 120s).
- [ ] **TB-498** `rejected` — For whale-cluster tier specifically on 15m windows, require score≥9.0 or higher consensus (yes≥0.80) to reduce false positives from high-volume bursts indistinguishable from HFT activity
  - **Governor rejection**: The proposed tweak violates TB-001 applied (whale-cluster volume delta threshold ≥1000 for 15m BTC, no relaxations below e.g. 300k/500/750) by setting min_volume_delta: 500.0, which is a 0.5x relaxation below the protected minimum of 1000. It also violates 'No market-type-specific volume delta multipliers (e.g. 0.5x/1-1' by introducing a 0.5x baseline multiplier for KXBTC15M. Additionally, it introduces min_price_move: 0.01, conflicting with 'No spike_min_price_move increases (e.g. ≥0.005/0.01/...)' which rejected ≥0.01 thresholds, and adds absolute whale count ≥15 in 120s, relaxing TB-003 applied (whale-cluster whale count ≥50 in 120s).

---

## 2026-04-12 — Advisor snapshot 163

### Summary
Whale-cluster signals on KXBTC15M-26APR121715-15 show high false positives with low volume deltas (300-500) and minimal/no price moves, often labeled noise/unclear despite high scores; golf prop market has fleeting spikes mislabeled as notable.

### Next step
Raise whale-cluster volume delta threshold to ≥0.5x baseline and add sustained price hold requirement over 30m for prop/crypto markets.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-499** `planned` — Require volume delta ≥0.5x baseline for whale-cluster in 15m BTC markets to filter microstructure noise.
- [ ] **TB-500** `planned` — Raise whale-cluster threshold to 15+ whales in 120s window for high-frequency markets.
- [ ] **TB-501** `planned` — For golf props, mandate 2x volume multiplier and 30m price hold to catch sustained signals.

---

## 2026-04-12 — Advisor snapshot 164

### Summary
Whale-cluster signals in BTC 15M markets generate frequent false positives due to low volume deltas (often <500) and minimal price moves (<0.03), misidentifying normal noise or HFT bursts as informative spikes, while golf prop markets need higher volume multipliers and sustained price holds.

### Next step
Raise whale-cluster volume delta threshold to 0.5x baseline and require min price move of 0.03 for high-frequency BTC markets.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-502** `rejected` — Require volume delta ≥500 or 0.5x baseline for whale-cluster triggers in BTC 15M to filter microstructure noise.
  - **Governor rejection**: The proposed tweak sets whale-cluster min_volume_delta to 500.0, which violates TB-001 applied (min_volume_delta ≥1000 for 15m BTC, no relaxations e.g. <1000). It also introduces a min_price_move of 0.03 requirement, conflicting with the applied constraint against spike_min_price_move increases (TB-210,213,216-219, etc., rejected such changes).
- [ ] **TB-503** `rejected` — Raise volume multiplier to 2x baseline and add 30m sustained price hold for golf prop markets.
  - **Governor rejection**: The proposed tweak sets whale-cluster min_volume_delta to 500.0, which violates TB-001 applied (min_volume_delta ≥1000 for 15m BTC, no relaxations e.g. <1000). It also introduces a min_price_move of 0.03 requirement, conflicting with the applied constraint against spike_min_price_move increases (TB-210,213,216-219, etc., rejected such changes).
- [ ] **TB-504** `rejected` — Increase whale-cluster threshold to 15+ whales in 120s window for high-frequency BTC markets.
  - **Governor rejection**: The proposed tweak sets whale-cluster min_volume_delta to 500.0, which violates TB-001 applied (min_volume_delta ≥1000 for 15m BTC, no relaxations e.g. <1000). It also introduces a min_price_move of 0.03 requirement, conflicting with the applied constraint against spike_min_price_move increases (TB-210,213,216-219, etc., rejected such changes).

---

## 2026-04-12 — Advisor snapshot 165

### Summary
False positives in whale-cluster signals for KXBTC15M occur primarily with low volume deltas (<500) and minimal/no price moves (priceΔ=0.0-0.01), often labeled as noise/unclear/low due to liquidity artifacts and microstructure noise resembling HFT bursts rather than informed trading.

### Next step
Raise whale-cluster volume delta threshold to 500+ and require priceΔ >=0.02 to filter low-signal spikes in 15m BTC futures.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-505** `rejected` — Require volume delta >=0.5x hourly baseline for whale-cluster alerts to exclude liquidity artifacts.
  - **Governor rejection**: TB-001 applied raises whale-cluster volume delta threshold to 1000 for 15m BTC to catch only stronger signals. The proposed tweak relaxes it to 500.0, conflicting by lowering a previously tightened threshold to reduce noise.
- [ ] **TB-506** `rejected` — Increase whale-cluster to 15+ whales in 120s window for high-frequency BTC markets.
  - **Governor rejection**: TB-001 applied raises whale-cluster volume delta threshold to 1000 for 15m BTC to catch only stronger signals. The proposed tweak relaxes it to 500.0, conflicting by lowering a previously tightened threshold to reduce noise.
- [ ] **TB-507** `rejected` — Raise min_price_move to 0.02 for all tiers to ensure sustained directional pressure.
  - **Governor rejection**: TB-001 applied raises whale-cluster volume delta threshold to 1000 for 15m BTC to catch only stronger signals. The proposed tweak relaxes it to 500.0, conflicting by lowering a previously tightened threshold to reduce noise.

---

## 2026-04-12 — Advisor snapshot 166

### Summary
Whale-cluster signals on BTC 15M markets show high false positives from low volume deltas (often <500) with no/minimal price moves, labeled as noise/unclear due to liquidity artifacts, micro-clusters, or lack of follow-on flow confirmation.

### Next step
Require volume delta >= 0.5x hourly baseline AND >70% follow-on flow agreement in spike direction over next 20 trades for whale-cluster tier.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-508** `rejected` — Raise whale-cluster min volume delta threshold to 500 to filter sub-significant spikes.
  - **Governor rejection**: The proposed tweak violates TB-199, TB-204, TB-206, and related rejected constraints (TB-265-267, TB-276-283, TB-286, TB-289, TB-294, TB-297, TB-358-360, TB-364-366, TB-370-372, TB-378, TB-412, TB-422, TB-449-451, TB-467-469, TB-480-482). These explicitly reject minimum notional trade size, USD equivalent, absolute volume, and trade count filters for crypto 15m/low-volume/low-liquidity markets. The proposed 'min_volume_delta: 500.0' and '>70% follow-on flow agreement in spike direction over next 20 trades' requirements introduce a de facto minimum volume and trade-count filter that was previously rejected. Additionally, 'min_price_move: 0.02' conflicts with TB-210, TB-213, and TB-216-219 (and related spike_min_price_move rejections TB-248-251, TB-265-273, TB-274-295, TB-296, TB-303-305, TB-316-322, TB-337-339, TB-341, TB-343-345, TB-346-348, TB-349-351, TB-352-355, TB-358-360, TB-364-366, TB-370-372, TB-377-379, TB-386-397, TB-401-406, TB-407-412, TB-416-418, TB-419-421, TB-431-439, TB-443-445, TB-476-479, TB-490-492), which collectively reject minimum price move thresholds as noise filters for lower-liquidity and high-frequency crypto markets. This tweak reintroduces previously tightened filters under a different framing (follow-on flow confirmation), reversing the intent of historical constraint rejections.
- [ ] **TB-509** `rejected` — Require minimum price move of 0.02 (2%) for all signals to exclude zero-price-change noise.
  - **Governor rejection**: The proposed tweak violates TB-199, TB-204, TB-206, and related rejected constraints (TB-265-267, TB-276-283, TB-286, TB-289, TB-294, TB-297, TB-358-360, TB-364-366, TB-370-372, TB-378, TB-412, TB-422, TB-449-451, TB-467-469, TB-480-482). These explicitly reject minimum notional trade size, USD equivalent, absolute volume, and trade count filters for crypto 15m/low-volume/low-liquidity markets. The proposed 'min_volume_delta: 500.0' and '>70% follow-on flow agreement in spike direction over next 20 trades' requirements introduce a de facto minimum volume and trade-count filter that was previously rejected. Additionally, 'min_price_move: 0.02' conflicts with TB-210, TB-213, and TB-216-219 (and related spike_min_price_move rejections TB-248-251, TB-265-273, TB-274-295, TB-296, TB-303-305, TB-316-322, TB-337-339, TB-341, TB-343-345, TB-346-348, TB-349-351, TB-352-355, TB-358-360, TB-364-366, TB-370-372, TB-377-379, TB-386-397, TB-401-406, TB-407-412, TB-416-418, TB-419-421, TB-431-439, TB-443-445, TB-476-479, TB-490-492), which collectively reject minimum price move thresholds as noise filters for lower-liquidity and high-frequency crypto markets. This tweak reintroduces previously tightened filters under a different framing (follow-on flow confirmation), reversing the intent of historical constraint rejections.
- [ ] **TB-510** `rejected` — Add flow-divergence filter: confirm spike direction with >70% agreement in subsequent 20 trades.
  - **Governor rejection**: The proposed tweak violates TB-199, TB-204, TB-206, and related rejected constraints (TB-265-267, TB-276-283, TB-286, TB-289, TB-294, TB-297, TB-358-360, TB-364-366, TB-370-372, TB-378, TB-412, TB-422, TB-449-451, TB-467-469, TB-480-482). These explicitly reject minimum notional trade size, USD equivalent, absolute volume, and trade count filters for crypto 15m/low-volume/low-liquidity markets. The proposed 'min_volume_delta: 500.0' and '>70% follow-on flow agreement in spike direction over next 20 trades' requirements introduce a de facto minimum volume and trade-count filter that was previously rejected. Additionally, 'min_price_move: 0.02' conflicts with TB-210, TB-213, and TB-216-219 (and related spike_min_price_move rejections TB-248-251, TB-265-273, TB-274-295, TB-296, TB-303-305, TB-316-322, TB-337-339, TB-341, TB-343-345, TB-346-348, TB-349-351, TB-352-355, TB-358-360, TB-364-366, TB-370-372, TB-377-379, TB-386-397, TB-401-406, TB-407-412, TB-416-418, TB-419-421, TB-431-439, TB-443-445, TB-476-479, TB-490-492), which collectively reject minimum price move thresholds as noise filters for lower-liquidity and high-frequency crypto markets. This tweak reintroduces previously tightened filters under a different framing (follow-on flow confirmation), reversing the intent of historical constraint rejections.

---

## 2026-04-12 — Advisor snapshot 167

### Summary
Whale-cluster signals trigger frequently with low price moves (often 0%) and modest volume deltas (~300-500), leading to high false positives labeled as noise/unclear or signal/no due to lack of sustained directionality or significance relative to baseline.

### Next step
Require volume delta ≥500 and price move ≥0.01 for whale-cluster tier to filter insignificant liquidity artifacts.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.015`

### Recommendations

- [ ] **TB-511** `rejected` — Raise spike_min_volume_delta to 500 to exclude low-volume clusters (<5% baseline equivalent).
  - **Governor rejection**: The proposed tweak violates **TB-001 applied**: whale-cluster **min_volume_delta ≥1000** (no relaxations e.g. to 300k/500/750) by relaxing to 500.0, and **No spike_min_price_move increases** (TB-210/213/etc. rejected; blocks ≥0.005/0.01/0.015/etc.) by introducing a new min_price_move ≥0.015 threshold, which was explicitly rejected to avoid requiring price moves in BTC 15m/whale-cluster scenarios.
- [ ] **TB-512** `rejected` — Increase spike_min_price_move to 0.015 to ensure directional conviction beyond noise.
  - **Governor rejection**: The proposed tweak violates **TB-001 applied**: whale-cluster **min_volume_delta ≥1000** (no relaxations e.g. to 300k/500/750) by relaxing to 500.0, and **No spike_min_price_move increases** (TB-210/213/etc. rejected; blocks ≥0.005/0.01/0.015/etc.) by introducing a new min_price_move ≥0.015 threshold, which was explicitly rejected to avoid requiring price moves in BTC 15m/whale-cluster scenarios.
- [ ] **TB-513** `rejected` — Add follow-on flow filter: require >70% directional agreement in next 20 trades for yes signals.
  - **Governor rejection**: The proposed tweak violates **TB-001 applied**: whale-cluster **min_volume_delta ≥1000** (no relaxations e.g. to 300k/500/750) by relaxing to 500.0, and **No spike_min_price_move increases** (TB-210/213/etc. rejected; blocks ≥0.005/0.01/0.015/etc.) by introducing a new min_price_move ≥0.015 threshold, which was explicitly rejected to avoid requiring price moves in BTC 15m/whale-cluster scenarios.

---

## 2026-04-12 — Advisor snapshot 168

### Summary
Whale-cluster signals on liquid BTC 15M markets generate frequent false positives due to low volume deltas relative to baseline (often <5% hourly), lacking price movement or follow-on flow confirmation, despite high scores.

### Next step
Require volume delta ≥0.5x hourly baseline for whale-cluster tier and add minimum price move threshold to filter liquidity artifacts.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-514** `planned` — Raise spike_min_volume_delta to 500+ to exclude micro-clusters under ~400 volΔ.
- [ ] **TB-515** `planned` — Set spike_min_price_move to 0.02 (2%) as zero/low priceΔ signals are mostly noise/unclear.
- [ ] **TB-516** `planned` — For whale-cluster, add post-spike flow filter: >70% directional agreement in next 20 trades.

---

## 2026-04-12 — Advisor snapshot 169

### Summary
Whale-cluster signals in 15-minute BTC markets frequently trigger false positives due to low-magnitude volume deltas lacking price impact or sustained directional flow, despite high scores around 8.0.

### Next step
Normalize volume delta to baseline and require >5% relative delta for whale-cluster tier to filter insignificant clusters.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-517** `rejected` — Raise spike_min_volume_delta to 500+ or require 2-5% of baseline volume delta.
  - **Governor rejection**: Violates TB-001 applied: whale-cluster min_volume_delta ≥1000 for 15m BTC (no relaxations e.g. to 300k/500/750/0.5x baseline). Proposed sets min_volume_delta: 500.0, which is a relaxation below the required ≥1000. Also violates 'No spike_min_price_move increases (≥0.005/0.02/...)' by introducing min_price_move: 0.02 filter (rejected numerous TBs including those for whale-cluster/low-liq in 15m BTC).
- [ ] **TB-518** `rejected` — Add flow-divergence filter: confirm whale direction with >70% agreement in next 20 trades.
  - **Governor rejection**: Violates TB-001 applied: whale-cluster min_volume_delta ≥1000 for 15m BTC (no relaxations e.g. to 300k/500/750/0.5x baseline). Proposed sets min_volume_delta: 500.0, which is a relaxation below the required ≥1000. Also violates 'No spike_min_price_move increases (≥0.005/0.02/...)' by introducing min_price_move: 0.02 filter (rejected numerous TBs including those for whale-cluster/low-liq in 15m BTC).
- [ ] **TB-519** `rejected` — Require min_price_move >=0.02 or 2x baseline volume for high-liquidity markets.
  - **Governor rejection**: Violates TB-001 applied: whale-cluster min_volume_delta ≥1000 for 15m BTC (no relaxations e.g. to 300k/500/750/0.5x baseline). Proposed sets min_volume_delta: 500.0, which is a relaxation below the required ≥1000. Also violates 'No spike_min_price_move increases (≥0.005/0.02/...)' by introducing min_price_move: 0.02 filter (rejected numerous TBs including those for whale-cluster/low-liq in 15m BTC).

---

## 2026-04-12 — Advisor snapshot 170

### Summary
Whale-cluster signals on KXBTC15M-26APR121715-15 frequently trigger false positives due to low volume deltas (often <500) relative to baseline in thin 15-minute markets, lacking price movement or follow-on confirmation, while genuine signals show higher volumes or price deltas.

### Next step
Raise whale-cluster minimum volume delta threshold to 2-5% of recent baseline or absolute 750+ to filter micro-clusters without muting high-volume true signals.

### Suggested thresholds
`min_volume_delta` → `750.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-520** `rejected` — Require volume delta >= 2x or 5% of hourly baseline before flagging whale-cluster alerts.
  - **Governor rejection**: Violates TB-001 applied: whale-cluster min_volume_delta ≥1000 for 15m BTC (no relaxations e.g. to 300k/500/750/0.5x baseline). The proposal sets min_volume_delta: 750.0, which is a relaxation below the required ≥1000. Additionally violates 'No spike_min_price_move increases' (TB-005 rejected), as it introduces min_price_move: 0.01, previously rejected to avoid tightening price move filters.
- [ ] **TB-521** `rejected` — Add minimum price move of 0.01 (1%) or flow-divergence filter (>70% directional agreement in next 20 trades).
  - **Governor rejection**: Violates TB-001 applied: whale-cluster min_volume_delta ≥1000 for 15m BTC (no relaxations e.g. to 300k/500/750/0.5x baseline). The proposal sets min_volume_delta: 750.0, which is a relaxation below the required ≥1000. Additionally violates 'No spike_min_price_move increases' (TB-005 rejected), as it introduces min_price_move: 0.01, previously rejected to avoid tightening price move filters.
- [ ] **TB-522** `rejected` — For thin markets like 15M crypto futures, enforce cluster volume >10% baseline delta.
  - **Governor rejection**: Violates TB-001 applied: whale-cluster min_volume_delta ≥1000 for 15m BTC (no relaxations e.g. to 300k/500/750/0.5x baseline). The proposal sets min_volume_delta: 750.0, which is a relaxation below the required ≥1000. Additionally violates 'No spike_min_price_move increases' (TB-005 rejected), as it introduces min_price_move: 0.01, previously rejected to avoid tightening price move filters.

---

## 2026-04-12 — Advisor snapshot 171

### Summary
The whale-cluster detector is generating excessive false positives on volume clustering alone, with most signals showing zero price movement (priceΔ=0.0) and modest volume deltas (300–900 range) that lack directional conviction. Analyst feedback consistently flags subsignificant micro-clusters as noise when they don't correlate with follow-on flow or material price impact.

### Next step
Implement a flow-divergence filter requiring follow-on directional consensus (next 20 trades >70% agreement with spike direction) before emitting whale-cluster signals, combined with a minimum volume delta threshold set to 5% of the hourly baseline to filter liquidity artifacts.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-523** `rejected` — Add a flow-divergence validation layer: only flag whale accumulation when follow-on flow (next 20 trades) matches the spike direction with >70% agreement; this eliminates signals that lack conviction.
  - **Governor rejection**: The proposed tweak violates TB-001 applied (whale-cluster min_volume_delta ≥1000 for 15m BTC, no relaxations) by setting min_volume_delta: None, which relaxes the existing minimum threshold. It also conflicts with multiple rejections of minimum notional trade size/volume filters (TB-199,204,206, etc.) and >70% follow-on flow filters (TB-276-283, etc.) by introducing a new follow-on directional consensus filter (>70% agreement) and a volume delta as 5% of hourly baseline (implicitly a new minimum filter), both explicitly rejected to avoid such filters in crypto 15m/low-volume markets.
- [ ] **TB-524** `rejected` — Raise spike_min_volume_delta to require at least 5% of the hourly baseline delta before triggering whale-cluster alerts, filtering subsignificant micro-clusters in 15-minute markets.
  - **Governor rejection**: The proposed tweak violates TB-001 applied (whale-cluster min_volume_delta ≥1000 for 15m BTC, no relaxations) by setting min_volume_delta: None, which relaxes the existing minimum threshold. It also conflicts with multiple rejections of minimum notional trade size/volume filters (TB-199,204,206, etc.) and >70% follow-on flow filters (TB-276-283, etc.) by introducing a new follow-on directional consensus filter (>70% agreement) and a volume delta as 5% of hourly baseline (implicitly a new minimum filter), both explicitly rejected to avoid such filters in crypto 15m/low-volume markets.
- [ ] **TB-525** `rejected` — Introduce a price-impact confirmation rule: require priceΔ ≥ 0.01 (1%) or order-book directional consensus (e.g., bid/ask imbalance >60/40) when volume delta is between 5–10% of baseline, to distinguish informed flow from liquidity churn.
  - **Governor rejection**: The proposed tweak violates TB-001 applied (whale-cluster min_volume_delta ≥1000 for 15m BTC, no relaxations) by setting min_volume_delta: None, which relaxes the existing minimum threshold. It also conflicts with multiple rejections of minimum notional trade size/volume filters (TB-199,204,206, etc.) and >70% follow-on flow filters (TB-276-283, etc.) by introducing a new follow-on directional consensus filter (>70% agreement) and a volume delta as 5% of hourly baseline (implicitly a new minimum filter), both explicitly rejected to avoid such filters in crypto 15m/low-volume markets.
- [ ] **TB-526** `rejected` — Reduce spike_score_threshold from 8.0 to a lower value only after implementing flow divergence and baseline-percentage filters, as the current score alone is insufficient to separate signal from noise.
  - **Governor rejection**: The proposed tweak violates TB-001 applied (whale-cluster min_volume_delta ≥1000 for 15m BTC, no relaxations) by setting min_volume_delta: None, which relaxes the existing minimum threshold. It also conflicts with multiple rejections of minimum notional trade size/volume filters (TB-199,204,206, etc.) and >70% follow-on flow filters (TB-276-283, etc.) by introducing a new follow-on directional consensus filter (>70% agreement) and a volume delta as 5% of hourly baseline (implicitly a new minimum filter), both explicitly rejected to avoid such filters in crypto 15m/low-volume markets.

---

## 2026-04-12 — Advisor snapshot 172

### Summary
Whale-cluster signals on 15-minute BTC markets trigger frequent false positives due to low volume deltas (often <600) and absent price moves, even with high scores (8.0) and yes probabilities >0.5; true signals correlate with higher volumes (>500-900) or minimal price changes (>=0.01).

### Next step
Raise whale-cluster minimum volume delta threshold and add price move requirement for 15-minute BTC markets.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-527** `rejected` — Require volΔ >=500 for whale-cluster tier in 15m BTC to filter sub-baseline bursts.
  - **Governor rejection**: The proposed tweak violates TB-001. TB-001 explicitly applied a minimum_volume_delta ≥1000 for 15m BTC whale-cluster detection and explicitly rejected all relaxations (including to 300, 500, 750, and 0.5x baseline). The proposed tweak recommends lowering min_volume_delta to 500.0, which directly contradicts the hardened constraint and represents a regression to a previously rejected threshold.
- [ ] **TB-528** `rejected` — Add min_price_move >=0.01 to suppress zero-price-change alerts.
  - **Governor rejection**: The proposed tweak violates TB-001. TB-001 explicitly applied a minimum_volume_delta ≥1000 for 15m BTC whale-cluster detection and explicitly rejected all relaxations (including to 300, 500, 750, and 0.5x baseline). The proposed tweak recommends lowering min_volume_delta to 500.0, which directly contradicts the hardened constraint and represents a regression to a previously rejected threshold.
- [ ] **TB-529** `rejected` — Raise whale-cluster threshold to 30 whales in 120s or 10% of baseline delta.
  - **Governor rejection**: The proposed tweak violates TB-001. TB-001 explicitly applied a minimum_volume_delta ≥1000 for 15m BTC whale-cluster detection and explicitly rejected all relaxations (including to 300, 500, 750, and 0.5x baseline). The proposed tweak recommends lowering min_volume_delta to 500.0, which directly contradicts the hardened constraint and represents a regression to a previously rejected threshold.

---

## 2026-04-12 — Advisor snapshot 173

### Summary
All recent whale-cluster signals have zero or near-zero price moves despite high scores and varying volume deltas, leading to a high rate of false positives labeled as noise or non-signals, particularly at low absolute volumes.

### Next step
Raise spike_min_volume_delta to filter sub-baseline volume spikes and require priceΔ > 0 for whale-cluster emissions.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-530** `rejected` — Increase whale-cluster minimum cluster volume to 10% of recent baseline delta
  - **Governor rejection**: The proposed tweak conflicts with two historical constraints: (1) **TB-001 applied**: whale-cluster min_volume_delta ≥1000 for 15m BTC (no relaxations), but the proposal raises it to only 500.0, which is a relaxation below the required minimum of 1000. (2) **No spike_min_price_move increases** (TB-210/213/etc. rejected; blocks ≥0.005/0.01/etc. for BTC 15m), but the proposal introduces min_price_move: 0.01, directly violating the rejection of such price move requirements.
- [ ] **TB-531** `rejected` — Tighten volume-delta multiplier threshold from ~5x to 4x baseline
  - **Governor rejection**: The proposed tweak conflicts with two historical constraints: (1) **TB-001 applied**: whale-cluster min_volume_delta ≥1000 for 15m BTC (no relaxations), but the proposal raises it to only 500.0, which is a relaxation below the required minimum of 1000. (2) **No spike_min_price_move increases** (TB-210/213/etc. rejected; blocks ≥0.005/0.01/etc. for BTC 15m), but the proposal introduces min_price_move: 0.01, directly violating the rejection of such price move requirements.
- [ ] **TB-532** `rejected` — Require minimum price move of 0.01 and absolute volΔ >= 500
  - **Governor rejection**: The proposed tweak conflicts with two historical constraints: (1) **TB-001 applied**: whale-cluster min_volume_delta ≥1000 for 15m BTC (no relaxations), but the proposal raises it to only 500.0, which is a relaxation below the required minimum of 1000. (2) **No spike_min_price_move increases** (TB-210/213/etc. rejected; blocks ≥0.005/0.01/etc. for BTC 15m), but the proposal introduces min_price_move: 0.01, directly violating the rejection of such price move requirements.

---

## 2026-04-12 — Advisor snapshot 174

### Summary
The whale-cluster detector is generating excessive false positives on low-volume, price-neutral spikes (volΔ=300–900, priceΔ=0.0) that lack directional conviction. Analysts consistently flag signals with zero price movement and sub-baseline volume as noise, despite high statistical scores.

### Next step
Implement a mandatory price-move floor (minimum 1–2% for actionable whale signals) and add a baseline-relative volume gate (require volΔ ≥ 10% of recent 120-second baseline) to filter micro-events that cluster statistically but lack market impact.

### Suggested thresholds
`min_volume_delta` → `50.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-533** `rejected` — Raise spike_min_price_move from 0.0 to 0.01 (1%) for whale-cluster tier; price-neutral volume spikes alone do not confirm conviction and drive false positives.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-001 applied** requires whale-cluster min_volume_delta ≥1000 (no relaxations, e.g., to 300k/500/750/0.5x baseline), but the tweak sets min_volume_delta: 50.0, which is a severe relaxation; (2) Introduces **min_price_move: 0.01** (1%), directly conflicting with **No spike_min_price_move increases** (≥0.005/0.01/etc., rejected TB-210,213, etc.); (3) Adds a baseline-relative volume gate (volΔ ≥10% of 120s baseline), conflicting with **No volume-to-price-move ratio thresholds** and **No minimum notional trade size/abs volume filters** (rejected TB-199,200, etc.). These changes relax existing floors and add forbidden filters explicitly rejected to avoid over-filtering.
- [ ] **TB-534** `rejected` — Introduce a baseline-relative volume filter: reject signals where volΔ < 10% of the rolling 120-second baseline delta, as analysts note sub-baseline events generate noise despite high clustering.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-001 applied** requires whale-cluster min_volume_delta ≥1000 (no relaxations, e.g., to 300k/500/750/0.5x baseline), but the tweak sets min_volume_delta: 50.0, which is a severe relaxation; (2) Introduces **min_price_move: 0.01** (1%), directly conflicting with **No spike_min_price_move increases** (≥0.005/0.01/etc., rejected TB-210,213, etc.); (3) Adds a baseline-relative volume gate (volΔ ≥10% of 120s baseline), conflicting with **No volume-to-price-move ratio thresholds** and **No minimum notional trade size/abs volume filters** (rejected TB-199,200, etc.). These changes relax existing floors and add forbidden filters explicitly rejected to avoid over-filtering.
- [ ] **TB-535** `rejected` — Tighten the whale-cluster sensitivity threshold from p=0.0000 to p≤0.001 to exclude marginally significant volume anomalies; combine with a minimum cluster size (e.g., ≥30 whales in 120s for 15-minute BTC) to eliminate short-lived, low-participation bursts.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-001 applied** requires whale-cluster min_volume_delta ≥1000 (no relaxations, e.g., to 300k/500/750/0.5x baseline), but the tweak sets min_volume_delta: 50.0, which is a severe relaxation; (2) Introduces **min_price_move: 0.01** (1%), directly conflicting with **No spike_min_price_move increases** (≥0.005/0.01/etc., rejected TB-210,213, etc.); (3) Adds a baseline-relative volume gate (volΔ ≥10% of 120s baseline), conflicting with **No volume-to-price-move ratio thresholds** and **No minimum notional trade size/abs volume filters** (rejected TB-199,200, etc.). These changes relax existing floors and add forbidden filters explicitly rejected to avoid over-filtering.
- [ ] **TB-536** `rejected` — Add a directional-dominance filter: flag only when one side (bid or ask) shows ≥80% volume concentration; this filters balanced consolidations masquerading as actionable whale moves.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-001 applied** requires whale-cluster min_volume_delta ≥1000 (no relaxations, e.g., to 300k/500/750/0.5x baseline), but the tweak sets min_volume_delta: 50.0, which is a severe relaxation; (2) Introduces **min_price_move: 0.01** (1%), directly conflicting with **No spike_min_price_move increases** (≥0.005/0.01/etc., rejected TB-210,213, etc.); (3) Adds a baseline-relative volume gate (volΔ ≥10% of 120s baseline), conflicting with **No volume-to-price-move ratio thresholds** and **No minimum notional trade size/abs volume filters** (rejected TB-199,200, etc.). These changes relax existing floors and add forbidden filters explicitly rejected to avoid over-filtering.

---

## 2026-04-12 — Advisor snapshot 175

### Summary
Whale-cluster signals on low volume deltas (300-900) and minimal price moves (0-0.01) frequently trigger false positives, even with high scores and statistical significance, due to common liquidity noise in 15-minute BTC markets.

### Next step
Raise whale-cluster minimum volume delta threshold to filter sub-baseline, low-absolute-volume spikes.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-537** `planned` — Increase min_volume_delta from current levels to 1000+ to exclude low-absolute-volume events
- [ ] **TB-538** `planned` — Tighten whale-cluster to require 30+ whales in 120s window
- [ ] **TB-539** `planned` — Require minimum 1% price move (0.01) or directional dominance filter (80%+ one-sided)

---

## 2026-04-12 — Advisor snapshot 176

### Summary
False positives dominate in low-volume whale-cluster detections (volΔ <900) with minimal or no price moves (priceΔ ≤0.01), even at high statistical significance, while medium-high volume spikes with price moves are more reliably labeled as true signals.

### Next step
Raise min_volume_delta to filter low-absolute-volume events and add a minimum cluster volume as % of baseline.

### Suggested thresholds
`min_volume_delta` → `900.0`, `min_price_move` → `0.015`

### Recommendations

- [ ] **TB-540** `rejected` — Increase whale-cluster volume threshold to 900+ or 10% of recent baseline delta
  - **Governor rejection**: The proposed tweak sets min_volume_delta to 900.0, which relaxes the applied TB-001 constraint of whale-cluster min_volume_delta ≥1000 for 15m BTC (no relaxations e.g. to 300k/500/750/0.5x baseline). Additionally, it introduces min_price_move: 0.015, violating the historical constraint 'No spike_min_price_move increases (≥0.005/0.01/0.015/...; rejected TB-210,213,...535-536)'.
- [ ] **TB-541** `rejected` — Tighten min_price_move to 0.015+ for whale-cluster tier to require directional confirmation
  - **Governor rejection**: The proposed tweak sets min_volume_delta to 900.0, which relaxes the applied TB-001 constraint of whale-cluster min_volume_delta ≥1000 for 15m BTC (no relaxations e.g. to 300k/500/750/0.5x baseline). Additionally, it introduces min_price_move: 0.015, violating the historical constraint 'No spike_min_price_move increases (≥0.005/0.01/0.015/...; rejected TB-210,213,...535-536)'.
- [ ] **TB-542** `rejected` — Raise whale-cluster to 30+ whales in 120s for 15m BTC to filter short-lived HFT noise
  - **Governor rejection**: The proposed tweak sets min_volume_delta to 900.0, which relaxes the applied TB-001 constraint of whale-cluster min_volume_delta ≥1000 for 15m BTC (no relaxations e.g. to 300k/500/750/0.5x baseline). Additionally, it introduces min_price_move: 0.015, violating the historical constraint 'No spike_min_price_move increases (≥0.005/0.01/0.015/...; rejected TB-210,213,...535-536)'.

---

## 2026-04-12 — Advisor snapshot 177

### Summary
Whale-cluster signals in low-liquidity 15-minute BTC markets trigger frequent false positives with low volΔ (400-900), no price impact (0.0-0.01), and mixed analyst labels, despite high scores; the single watch-tier signal performs well with moderate priceΔ.

### Next step
Require minimum price move ≥0.01 for whale-cluster tier or raise min_volume_delta to 1000.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-543** `rejected` — Raise min_volume_delta from current to 1000 for whale-cluster in 15m markets
  - **Governor rejection**: The proposed tweak requires 'minimum price move ≥0.01 for whale-cluster tier', which directly conflicts with the historical constraint '**No spike_min_price_move increases** (e.g. ≥0.01/...; rejected TB-210,213,...511-536,540-542)'. This introduces a price move threshold that was explicitly rejected multiple times to avoid filtering out valid spikes.
- [ ] **TB-544** `rejected` — Set min_price_move to 0.01 to filter zero/low impact spikes
  - **Governor rejection**: The proposed tweak requires 'minimum price move ≥0.01 for whale-cluster tier', which directly conflicts with the historical constraint '**No spike_min_price_move increases** (e.g. ≥0.01/...; rejected TB-210,213,...511-536,540-542)'. This introduces a price move threshold that was explicitly rejected multiple times to avoid filtering out valid spikes.
- [ ] **TB-545** `rejected` — Tier-specific: whale-cluster requires volΔ ≥1000 or priceΔ ≥0.015
  - **Governor rejection**: The proposed tweak requires 'minimum price move ≥0.01 for whale-cluster tier', which directly conflicts with the historical constraint '**No spike_min_price_move increases** (e.g. ≥0.01/...; rejected TB-210,213,...511-536,540-542)'. This introduces a price move threshold that was explicitly rejected multiple times to avoid filtering out valid spikes.

---

## 2026-04-12 — Advisor snapshot 178

### Summary
Whale-cluster signals in low-liquidity 15-minute BTC markets trigger frequently on sub-1000 volume deltas with minimal or no price impact, leading to high false positives labeled as noise/unclear or signal/no, while true signals often show higher volumes or slight price moves.

### Next step
Raise min_volume_delta for whale-cluster tier in 15m markets and require priceΔ ≥0.01 alongside volume spike.

### Suggested thresholds
`min_volume_delta` → `900.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-546** `rejected` — Increase spike_min_volume_delta to 900.0 to filter low-volume clusters
  - **Governor rejection**: The proposed tweak violates **TB-001** (Whale-cluster volume delta threshold ≥1000 for 15m BTC) by lowering min_volume_delta to 900.0 (<1000). It also violates the **Blanket Rejections** by adding a min_price_move ≥0.01 requirement, which is a form of 'No spike_min_price_move increases (e.g., ≥0.005/0.01/...)' for BTC 15m/whale-cluster markets, and resembles prohibited 'combined priceΔ/volΔ filters' requiring synchronized volume + price movement.
- [ ] **TB-547** `rejected` — Set spike_min_price_move to 0.01 for whale-cluster signals
  - **Governor rejection**: The proposed tweak violates **TB-001** (Whale-cluster volume delta threshold ≥1000 for 15m BTC) by lowering min_volume_delta to 900.0 (<1000). It also violates the **Blanket Rejections** by adding a min_price_move ≥0.01 requirement, which is a form of 'No spike_min_price_move increases (e.g., ≥0.005/0.01/...)' for BTC 15m/whale-cluster markets, and resembles prohibited 'combined priceΔ/volΔ filters' requiring synchronized volume + price movement.
- [ ] **TB-548** `rejected` — Tiered thresholds: min_volume_delta=1000 for 15m BTC markets
  - **Governor rejection**: The proposed tweak violates **TB-001** (Whale-cluster volume delta threshold ≥1000 for 15m BTC) by lowering min_volume_delta to 900.0 (<1000). It also violates the **Blanket Rejections** by adding a min_price_move ≥0.01 requirement, which is a form of 'No spike_min_price_move increases (e.g., ≥0.005/0.01/...)' for BTC 15m/whale-cluster markets, and resembles prohibited 'combined priceΔ/volΔ filters' requiring synchronized volume + price movement.

---

## 2026-04-12 — Advisor snapshot 179

### Summary
The detector is generating high-volume false positives in 15-minute BTC markets by triggering on statistically significant whale clusters that lack meaningful price impact (priceΔ=0.0 in majority of signals). Volume deltas alone are insufficient discriminators when baseline ratios are near zero.

### Next step
Require minimum price move of ≥1% alongside whale-cluster detection, or raise the volume-delta baseline calculation to account for 15-minute market microstructure idiosyncracies where liquidity clustering is common noise.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-549** `rejected` — Require priceΔ ≥ 0.01 (1%) as a mandatory gate for whale-cluster tier signals to filter out volume spikes disconnected from actual market movement.
  - **Governor rejection**: The proposed tweak requires a **minimum price move of ≥0.01 (1%)**, which directly violates the historical constraint '**No spike_min_price_move increases** (≥0.005/0.01/0.015/0.02/0.03/0.05/0.10/priceΔ>0%; rejected TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445,476-479,490-492,511-536,540-548)'. This was explicitly rejected multiple times to prevent tightening price move requirements.
- [ ] **TB-550** `rejected` — Recalibrate the volume-delta baseline for 15-minute intervals: current 0.0x ratio indicates the detector is hypersensitive to frequency clustering independent of absolute volume; raise baseline to reflect typical whale activity in these shorter windows.
  - **Governor rejection**: The proposed tweak requires a **minimum price move of ≥0.01 (1%)**, which directly violates the historical constraint '**No spike_min_price_move increases** (≥0.005/0.01/0.015/0.02/0.03/0.05/0.10/priceΔ>0%; rejected TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445,476-479,490-492,511-536,540-548)'. This was explicitly rejected multiple times to prevent tightening price move requirements.
- [ ] **TB-551** `rejected` — Increase whale-cluster sensitivity threshold from p=0.0000 to p≤0.001 to exclude sub-baseline, statistically significant but operationally negligible volume bursts.
  - **Governor rejection**: The proposed tweak requires a **minimum price move of ≥0.01 (1%)**, which directly violates the historical constraint '**No spike_min_price_move increases** (≥0.005/0.01/0.015/0.02/0.03/0.05/0.10/priceΔ>0%; rejected TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445,476-479,490-492,511-536,540-548)'. This was explicitly rejected multiple times to prevent tightening price move requirements.
- [ ] **TB-552** `rejected` — For whale-cluster alerts in KXBTC15M, require minimum of 30+ whales in 120s window to filter short-lived, low-conviction bursts common in high-frequency noise.
  - **Governor rejection**: The proposed tweak requires a **minimum price move of ≥0.01 (1%)**, which directly violates the historical constraint '**No spike_min_price_move increases** (≥0.005/0.01/0.015/0.02/0.03/0.05/0.10/priceΔ>0%; rejected TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445,476-479,490-492,511-536,540-548)'. This was explicitly rejected multiple times to prevent tightening price move requirements.

---

## 2026-04-12 — Advisor snapshot 180

### Summary
High false positives in low-liquidity 15-minute BTC whale-cluster signals with no price impact (priceΔ=0.0) and low absolute volume deltas (~500-900), despite high scores; true signals often show priceΔ≥0.02-0.04 or higher volume.

### Next step
Require minimum price move of 0.01 for whale-cluster tier signals in 15-minute markets to filter noise without muting genuine impact.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-553** `rejected` — Raise min_volume_delta to 1000 for 15-minute markets to exclude sub-baseline spikes.
  - **Governor rejection**: The proposed tweak introduces a **min_price_move ≥0.01** requirement, which directly conflicts with the historical constraint '**No spike_min_price_move increases** (e.g. ≥0.005/0.01/0.015/0.02/0.03/0.05/0.10/priceΔ>0%; rejected TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445,476-479,490-492,511-536,540-548,549-552)'. This is an explicit rejection of adding any minimum price move threshold, including exactly 0.01.
- [ ] **TB-554** `rejected` — Increase min_price_move to 0.01 globally, or 0.02 for whale-cluster tier.
  - **Governor rejection**: The proposed tweak introduces a **min_price_move ≥0.01** requirement, which directly conflicts with the historical constraint '**No spike_min_price_move increases** (e.g. ≥0.005/0.01/0.015/0.02/0.03/0.05/0.10/priceΔ>0%; rejected TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445,476-479,490-492,511-536,540-548,549-552)'. This is an explicit rejection of adding any minimum price move threshold, including exactly 0.01.
- [ ] **TB-555** `rejected` — Adjust whale-cluster to require ≥30 whales in 120s and p≤0.001 with priceΔ≥0.01.
  - **Governor rejection**: The proposed tweak introduces a **min_price_move ≥0.01** requirement, which directly conflicts with the historical constraint '**No spike_min_price_move increases** (e.g. ≥0.005/0.01/0.015/0.02/0.03/0.05/0.10/priceΔ>0%; rejected TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445,476-479,490-492,511-536,540-548,549-552)'. This is an explicit rejection of adding any minimum price move threshold, including exactly 0.01.

---

## 2026-04-12 — Advisor snapshot 181

### Summary
High false positives in BTC 15M whale-cluster detections with low/no price moves (priceΔ=0.0-0.01) and modest volΔ despite high scores, often labeled noise/unclear or signal/no; golf markets show mixed results needing volume tuning for intra-round noise.

### Next step
Require minimum price impact ≥0.01 alongside volume delta for all tiers to filter microstructure noise without muting high-conviction signals.

### Suggested thresholds
`min_volume_delta` → `700.0`, `min_price_move` → `0.015`

### Recommendations

- [ ] **TB-556** `rejected` — Raise min_volume_delta for 15M markets to 700+ to reduce sensitivity in low-baseline scenarios.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-001 applied** requires whale-cluster min_volume_delta ≥1000 for 15m BTC with no relaxations (e.g., <1000), but the proposal sets min_volume_delta: 700.0, which relaxes it below 1000. (2) **No spike_min_price_move increases** (TB-210/213/etc. rejected), which blocks ≥0.005/0.01/0.015/etc. min price move requirements for BTC 15m/high-freq/whale-cluster/low-liq markets, but the proposal introduces min_price_move: 0.015, directly conflicting with prior rejections of such filters.
- [ ] **TB-557** `rejected` — Increase min_price_move to 0.015 globally, especially for whale-cluster tier.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-001 applied** requires whale-cluster min_volume_delta ≥1000 for 15m BTC with no relaxations (e.g., <1000), but the proposal sets min_volume_delta: 700.0, which relaxes it below 1000. (2) **No spike_min_price_move increases** (TB-210/213/etc. rejected), which blocks ≥0.005/0.01/0.015/etc. min price move requirements for BTC 15m/high-freq/whale-cluster/low-liq markets, but the proposal introduces min_price_move: 0.015, directly conflicting with prior rejections of such filters.
- [ ] **TB-558** `rejected` — Market-type rules: lower volume multiplier to 1.3x only for golf round-score markets.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) **TB-001 applied** requires whale-cluster min_volume_delta ≥1000 for 15m BTC with no relaxations (e.g., <1000), but the proposal sets min_volume_delta: 700.0, which relaxes it below 1000. (2) **No spike_min_price_move increases** (TB-210/213/etc. rejected), which blocks ≥0.005/0.01/0.015/etc. min price move requirements for BTC 15m/high-freq/whale-cluster/low-liq markets, but the proposal introduces min_price_move: 0.015, directly conflicting with prior rejections of such filters.

---

## 2026-04-12 — Advisor snapshot 182

### Summary
High false positives in low-volume whale-cluster detections on BTC15M markets with 0.0 priceΔ and low absolute volΔ, despite high scores; golf/politics watch signals mixed but some valid with price moves.

### Next step
Require minimum price impact ≥0.01 alongside volume delta for all tiers to filter microstructure noise.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-559** `rejected` — Raise min_volume_delta to 1000 for 15-min markets to cut low-absolute-volume false positives.
  - **Governor rejection**: The proposed tweak violates TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445,476-479,490-492,511-536,540-548,549-552 (rejected proposals to increase spike_min_price_move to ≥0.005/0.01/etc.). It introduces a new **min_price_move ≥0.01** requirement alongside volume delta, effectively blocking detections with insufficient price move (e.g., 0.0 priceΔ), which matches the rejected constraints against adding minimum price move filters.
- [ ] **TB-560** `rejected` — Lower volume delta multiplier to 1.3x specifically for golf round-score markets.
  - **Governor rejection**: The proposed tweak violates TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445,476-479,490-492,511-536,540-548,549-552 (rejected proposals to increase spike_min_price_move to ≥0.005/0.01/etc.). It introduces a new **min_price_move ≥0.01** requirement alongside volume delta, effectively blocking detections with insufficient price move (e.g., 0.0 priceΔ), which matches the rejected constraints against adding minimum price move filters.
- [ ] **TB-561** `rejected` — Increase whale-cluster p-value threshold to ≤0.001 to reduce sensitivity in low-baseline scenarios.
  - **Governor rejection**: The proposed tweak violates TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445,476-479,490-492,511-536,540-548,549-552 (rejected proposals to increase spike_min_price_move to ≥0.005/0.01/etc.). It introduces a new **min_price_move ≥0.01** requirement alongside volume delta, effectively blocking detections with insufficient price move (e.g., 0.0 priceΔ), which matches the rejected constraints against adding minimum price move filters.

---

## 2026-04-12 — Advisor snapshot 183

### Summary
False positives dominate in low-liquidity 15-minute BTC markets due to single-trade or sub-baseline volume spikes with minimal or no price impact, despite high statistical scores; golf markets show noise from quote repositioning, while TRUMPSAY signals are generally valid.

### Next step
Require priceΔ ≥ 0.01 alongside volume delta for all watch and whale-cluster tiers in 15-minute markets to filter microstructure noise.

### Suggested thresholds
`min_price_move` → `0.01`

### Recommendations

- [ ] **TB-562** `rejected` — Raise spike_min_volume_delta to 10x baseline specifically for 15-minute BTC markets.
  - **Governor rejection**: The proposed tweak violates the historical constraint 'No spike_min_price_move increases' (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445,476-479,490-492,511-536,540-548,549-552,553-555 rejected; for BTC 15m/high-freq/whale-cluster/low-liq markets). It introduces a new min_price_move ≥ 0.01 requirement alongside volume delta specifically for 15-minute BTC markets (including low-liquidity ones), which directly conflicts with the explicit rejection of any such price move thresholds.
- [ ] **TB-563** `rejected` — Increase volume delta multiplier threshold to 1.3x for golf round-score markets.
  - **Governor rejection**: The proposed tweak violates the historical constraint 'No spike_min_price_move increases' (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445,476-479,490-492,511-536,540-548,549-552,553-555 rejected; for BTC 15m/high-freq/whale-cluster/low-liq markets). It introduces a new min_price_move ≥ 0.01 requirement alongside volume delta specifically for 15-minute BTC markets (including low-liquidity ones), which directly conflicts with the explicit rejection of any such price move thresholds.
- [ ] **TB-564** `rejected` — Require minimum price impact of 1% for whale-cluster alerts with 0.0 priceΔ.
  - **Governor rejection**: The proposed tweak violates the historical constraint 'No spike_min_price_move increases' (TB-210,213,216-219,248-251,265-273,274-295,296,303-305,316-322,337-339,341,343-345,346-348,349-351,352-355,358-360,364-366,370-372,377-379,386-397,401-406,407-412,416-418,419-421,431-439,443-445,476-479,490-492,511-536,540-548,549-552,553-555 rejected; for BTC 15m/high-freq/whale-cluster/low-liq markets). It introduces a new min_price_move ≥ 0.01 requirement alongside volume delta specifically for 15-minute BTC markets (including low-liquidity ones), which directly conflicts with the explicit rejection of any such price move thresholds.

---
