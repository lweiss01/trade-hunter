
## 2026-05-08 — Advisor snapshot A

### Summary
False positives dominate in low-liquidity NBA series winner markets and 15m crypto markets, driven by high volume deltas with minimal price moves (<0.03) from mechanical quoting, rebalancing, or liquidity noise.

### Next step
Raise min_price_move to 0.05 for all watch-tier signals in low-liquidity series (NBA playoffs/crypto) to filter low-conviction spikes.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [x] **TB-001** `applied` — Require min_price_move >=0.05 for NBA series winner markets to ignore stable-pricing liquidity dumps
- [x] **TB-002** `applied` — Set min_volume_delta multiplier to 50x baseline for 15m crypto unless priceΔ >=0.005 or >80% one-sided order flow
- [x] **TB-003** `applied` — Add tier-specific rule: watch tier requires >10 recent trades for low-liquidity markets to exclude mechanical noise

---

## 2026-05-08 — Advisor snapshot B

### Summary
False positives dominate in low-liquidity NBA series winner markets and short-term crypto markets, driven by mechanical fills, passive liquidity noise, and rebalancing without meaningful price movement.

### Next step
Require price move ≥0.05 (5%) for all watch-tier signals in low-liquidity markets to filter mechanical volume spikes.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [x] **TB-004** `applied` — Raise min_price_move to 0.05 for NBA series winner markets (e.g., KXNBASERIES-*).
- [x] **TB-005** `applied` — Increase min_volume_delta multiplier to 50x baseline for 15m crypto markets (e.g., KXBTC15M-*).
- [x] **TB-006** `applied` — Add rule: require >10 recent trades AND asymmetric order flow (>80% one-sided) for tier:watch in low-activity markets.

---

## 2026-05-08 — Advisor snapshot C

### Summary
False positives are driven by mechanical fills, passive liquidity noise, and rebalancing in low-activity NBA series markets and short-term crypto markets, often with high volume deltas but minimal or no price movement.

### Next step
Require price move ≥0.03 (3%) AND volume delta ≥50x baseline for all markets to filter mechanical noise.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [x] **TB-007** `applied` — Raise min_price_move to 0.05 for NBA playoff series markets with low trade activity.
- [x] **TB-008** `applied` — Set min_volume_delta to 50x baseline for 15m crypto markets unless priceΔ≥0.005.
- [x] **TB-009** `applied` — Add market-type rules: 2x volume multiplier + >10 recent trades for low-liquidity series winner markets.

---

## 2026-05-08 — Advisor snapshot D

### Summary
False positives are driven by mechanical fills, passive liquidity noise, and rebalancing in low-activity NBA series markets and short-term crypto, where high volume deltas occur without meaningful price moves or genuine order flow.

### Next step
Require price move ≥0.03 (3%) AND volume delta ≥2x baseline for all watch-tier signals to filter mechanical noise.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [x] **TB-010** `applied` — Raise min_price_move to 0.05 for NBA playoff series winner markets to ignore stable pricing between games.
- [x] **TB-011** `applied` — Increase min_volume_delta multiplier to 2.0x+ baseline and require >10 recent trades for low-liquidity series markets.
- [x] **TB-012** `applied` — For 15m crypto markets, require priceΔ ≥0.005 or >80% asymmetric order flow alongside volume spikes.

---

## 2026-05-08 — Advisor snapshot E

### Summary
False positives cluster in low-liquidity markets (crypto 15m, NBA series) where volume spikes decouple from price movement, and in high-odds markets where mechanical fills trigger high scores despite minimal directional conviction.

### Next step
Implement market-segment-specific thresholds: require price_move ≥ 0.5% for crypto 15m alerts, ≥ 5% for series/playoff markets, and enforce volume_delta multiplier ≥ 15x baseline only when accompanied by measurable price impact; add asymmetric order flow filter (≥80% one-sided) for volume-only signals.

### Suggested thresholds
`min_volume_delta` → `15.0`, `min_price_move` → `0.05`

### Recommendations

- [x] **TB-013** `applied` — For 15-minute crypto markets: raise volume_delta threshold to 15x baseline and require price_move ≥ 0.5% OR asymmetric order flow ≥80% one-sided to suppress mechanical rebalancing noise
- [x] **TB-014** `applied` — For low-liquidity series/playoff markets (NBA): raise volume_delta multiplier to 2.0x baseline AND price_move to ≥5% to filter stable inter-game pricing
- [x] **TB-015** `applied` — For high-odds notable-tier markets: raise min_price_move to 5% floor and add minimum trade count (≥10 recent trades) to distinguish mechanical dumps from genuine directional flow

---

## 2026-05-08 — Advisor snapshot F

### Summary
False positives are driven by mechanical noise, quoting artifacts, and single large trades in low-liquidity markets like NBA series and 15-min BTC, where high volume deltas occur without sustained price movement.

### Next step
Require price move ≥0.03 AND volume delta ≥2x baseline, with market-type specific overrides for low-liquidity assets.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [x] **TB-016** `applied` — For NBA series markets, set volume delta threshold to 2x baseline and require >10 recent trades.
- [x] **TB-017** `applied` — For 15-min BTC/crypto markets, raise volume delta to 15x baseline unless price move ≥0.005.
- [x] **TB-018** `applied` — For low-liquidity high-odds markets (tier=notable), increase min_price_move to 0.05.

---

## 2026-05-08 — Advisor snapshot G

### Summary
False positives cluster around low-liquidity markets (NBA series, 15m crypto) where mechanical volume activity (quoting noise, rebalancing, passive fills) triggers alerts despite minimal or zero price movement. Score and volume thresholds alone cannot distinguish signal from mechanical noise.

### Next step
Implement a composite filter requiring either (a) price move ≥0.5% with volume spike, or (b) asymmetric order flow >80% one-sided. Decouple thresholds by market tier and liquidity profile rather than applying uniform rules.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [x] **TB-019** `applied` — For watch-tier low-liquidity markets (NBA series, thin crypto): require min_price_move ≥0.05 (5%) OR volume delta ≥2.0x baseline AND >10 recent trades to confirm intent vs. mechanical fills
- [x] **TB-020** `applied` — For 15m crypto (BTC, volatile pairs): raise volume delta multiplier to 15x baseline unless accompanied by price_move ≥0.005 (0.5%) or order-flow asymmetry >80% to suppress rebalancing false positives
- [x] **TB-021** `applied` — For notable-tier high-odds markets with thin liquidity: enforce min_price_move ≥0.05 (5%) to filter mechanical volume dumps that lack conviction
- [x] **TB-022** `applied` — Add order-flow directionality check: require >80% one-sided volume on notable/watch alerts in low-liquidity venues to distinguish passive fills from adversarial flow

---

## 2026-05-08 — Advisor snapshot H

### Summary
False positives dominate in low-liquidity prediction markets (e.g., reality TV, NBA series) and short-term crypto due to single large trades, mechanical fills, quoting noise, and volume spikes without sustained price movement.

### Next step
Require minimum price move of 0.03 (3%) AND volume delta ≥10x baseline for all tiers to filter mechanical noise.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [x] **TB-023** `applied` — Raise min_price_move to 0.05 for notable tier in low-liquidity/high-odds markets
- [x] **TB-024** `applied` — Raise min_volume_delta to 15x baseline for 15m BTC/crypto markets unless priceΔ≥0.005
- [x] **TB-025** `applied` — Add market-type rules: NBA series require volΔ≥2x baseline + >10 recent trades

---

## 2026-05-08 — Advisor snapshot I

### Summary
False positives cluster in low-liquidity markets (reality TV, NBA series) and short-timeframe crypto (15M BTC), where single large orders or mechanical fills trigger high scores despite absent or minimal sustained price impact. Volume delta alone is insufficient; price coherence and order flow persistence are critical missing signals.

### Next step
Implement a flow-coherence filter requiring that volume spikes sustain directional pressure across at least 60% of the next N trades (N=5–10 depending on timeframe/liquidity tier), and apply market-segment-specific volume multipliers: crypto 15M=15x baseline, low-liquidity prediction markets=2000x baseline, NBA series=2x baseline.

### Suggested thresholds
`min_price_move` → `0.01`, `score_threshold` → `8.0`

### Recommendations

- [x] **TB-026** `applied` — For 15-minute crypto (KXBTC15M): raise spike_min_volume_delta to 15x baseline; require priceΔ ≥ 0.5% sustained over next 3 candles to confirm.
- [x] **TB-027** `applied` — For low-liquidity long-tail markets (KXTOPCHEF, etc.): raise spike_min_volume_delta multiplier to 2000x baseline; add check that yes-probability shift > 5% to filter mechanical fills.
- [x] **TB-028** `applied` — For NBA series and mid-liquidity markets: raise spike_min_volume_delta to 2x baseline and enforce that >60% of subsequent trades (5–10 trades) flow in the same direction; filter out tick-level quoting noise by requiring priceΔ ≥ 1–2%.
- [x] **TB-029** `applied` — Add tier-aware score recalibration: watch-tier signals require score ≥ 8 + flow-coherence check; notable-tier signals require score ≥ 500 + price-move ≥ 3–5% depending on liquidity regime.

---

## 2026-05-08 — Advisor snapshot J

### Summary
False positives are triggered by low-price-move signals (2%) with high volume but no actual order flow, likely mechanical quote updates; genuine signals show similar price moves but higher analyst confidence.

### Next step
Add volume quality filter: require non-zero trade volume and baseline volume delta variance >10%.

### Suggested thresholds
`min_volume_delta` → `100000.0`, `min_price_move` → `0.025`, `score_threshold` → `2.2`

### Recommendations

- [x] **TB-030** `applied` — Raise min_price_move to 0.025 to filter 2% moves lacking momentum.
- [x] **TB-031** `applied` — Require volume delta >100k for watch-tier signals.
- [x] **TB-032** `applied` — Increase score_threshold to 2.2 to prioritize higher-confidence signals.

---

## 2026-05-08 — Advisor snapshot K

### Summary
Detector is emitting low-confidence signals (score=2.0) on mechanical quote noise and spread adjustments with minimal price moves (0.02 = 2%), particularly in NBA series markets where automated quote updates dominate genuine order flow.

### Next step
Raise spike_score_threshold from 2.0 to at least 3.5 and require non-zero actual trade count validation to distinguish mechanical liquidity provision from genuine directional flow.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `3.5`

### Recommendations

- [x] **TB-033** `applied` — Increase spike_min_price_move from 0.02 to 0.03 (3% minimum) to filter sub-3% quote noise while retaining signal at TRUMPSAYNICKNAME which moved 2% but showed higher yes-probability (0.34) and lower volume delta variance
- [x] **TB-034** `applied` — Implement asset-class filtering: require spike_min_volume_delta multiplier of 2.0x baseline for prediction markets (especially NBA/sports contracts) where quote automation is endemic, vs 1.5x for equities/crypto
- [x] **TB-035** `applied` — Add trade-count gate: require minimum non-zero trade executions in window (e.g., >5 trades) to validate that volume delta reflects actual order flow, not bid-ask spread widening or market-maker inventory adjustments

---

## 2026-05-08 — Advisor snapshot L

### Summary
Recent whale-cluster signals are correctly labeled as valid (yes/medium) despite zero price movement, indicating pure volume spikes are genuinely informative flow rather than false positives.

### Next step
Retain current thresholds as-is; volume-only spikes from whale-clusters are legitimate signals.

### Recommendations

- [ ] **TB-036** `rejected` — No change needed: zero priceΔ signals are validated by analysts.
  - **Governor rejection**: The proposed tweak sets min_price_move: None and min_volume_delta: None, which directly conflicts with multiple historical constraints that explicitly require minimum thresholds to exclude noise:
- NBA series winner markets: requires min_price_move >=0.05
- 15m crypto markets: requires min_volume_delta multiplier (50x/15x baseline) unless priceΔ >=0.005, and price_move >=0.5% as alternative
- Low-liquidity markets: requires >10 recent trades + >80% one-sided flow (implying volume/price checks to filter mechanical noise)
Relaxing these to None would reintroduce the false positives these constraints were tightened to prevent, even if whale-clusters are sometimes legitimate.
- [ ] **TB-037** `rejected` — Monitor for future signals with low score (<8.0) or non-whale tiers to identify true false positives.
  - **Governor rejection**: The proposed tweak sets min_price_move: None and min_volume_delta: None, which directly conflicts with multiple historical constraints that explicitly require minimum thresholds to exclude noise:
- NBA series winner markets: requires min_price_move >=0.05
- 15m crypto markets: requires min_volume_delta multiplier (50x/15x baseline) unless priceΔ >=0.005, and price_move >=0.5% as alternative
- Low-liquidity markets: requires >10 recent trades + >80% one-sided flow (implying volume/price checks to filter mechanical noise)
Relaxing these to None would reintroduce the false positives these constraints were tightened to prevent, even if whale-clusters are sometimes legitimate.
- [ ] **TB-038** `rejected` — Consider tier-specific tuning if non-whale volume spikes show poor labels.
  - **Governor rejection**: The proposed tweak sets min_price_move: None and min_volume_delta: None, which directly conflicts with multiple historical constraints that explicitly require minimum thresholds to exclude noise:
- NBA series winner markets: requires min_price_move >=0.05
- 15m crypto markets: requires min_volume_delta multiplier (50x/15x baseline) unless priceΔ >=0.005, and price_move >=0.5% as alternative
- Low-liquidity markets: requires >10 recent trades + >80% one-sided flow (implying volume/price checks to filter mechanical noise)
Relaxing these to None would reintroduce the false positives these constraints were tightened to prevent, even if whale-clusters are sometimes legitimate.

---

## 2026-05-08 — Advisor snapshot M

### Summary
All recent whale-cluster signals on KXNBASERIES-26CLEDETR2-DET have zero price movement despite high volume deltas and scores, yet analysts labeled them as valid (yes/high or medium), indicating these may represent genuine whale activity without immediate price impact.

### Next step
No threshold changes needed; zero price delta whale-clusters are legitimately informative.

### Recommendations

- [ ] **TB-039** `rejected` — Maintain current thresholds as analyst labels confirm signal quality
  - **Governor rejection**: The proposed tweak directly violates the active constraint 'Price-move floor: spike_min_price_move ≥ 0.03 (3%) to filter quote noise'. By recommending 'min_price_move: None', the tweak removes a floor that was explicitly established to distinguish genuine price-moving signals from passive quoting noise. The fact that recent whale-cluster signals show zero price movement despite high volume deltas is precisely the scenario this constraint was designed to filter. Removing this threshold would reintroduce the noise-generation problem the constraint was created to prevent, regardless of analyst labeling of individual historical cases.
- [ ] **TB-040** `rejected` — Monitor for future signals with priceΔ > 0 to validate volume-only triggers
  - **Governor rejection**: The proposed tweak directly violates the active constraint 'Price-move floor: spike_min_price_move ≥ 0.03 (3%) to filter quote noise'. By recommending 'min_price_move: None', the tweak removes a floor that was explicitly established to distinguish genuine price-moving signals from passive quoting noise. The fact that recent whale-cluster signals show zero price movement despite high volume deltas is precisely the scenario this constraint was designed to filter. Removing this threshold would reintroduce the noise-generation problem the constraint was created to prevent, regardless of analyst labeling of individual historical cases.
- [ ] **TB-041** `rejected` — Consider tier-specific rules if non-whale signals show false positives
  - **Governor rejection**: The proposed tweak directly violates the active constraint 'Price-move floor: spike_min_price_move ≥ 0.03 (3%) to filter quote noise'. By recommending 'min_price_move: None', the tweak removes a floor that was explicitly established to distinguish genuine price-moving signals from passive quoting noise. The fact that recent whale-cluster signals show zero price movement despite high volume deltas is precisely the scenario this constraint was designed to filter. Removing this threshold would reintroduce the noise-generation problem the constraint was created to prevent, regardless of analyst labeling of individual historical cases.

---

## 2026-05-08 — Advisor snapshot N

### Summary
NBA series markets are generating false positives from routine liquidity spikes with high volume deltas but minimal price movement (0% observed), while genuine whale-cluster signals show strong conviction despite lower or zero price moves.

### Next step
Implement market-segment-specific thresholds: require 2x volume delta baseline and >5% price move for NBA series markets; for whale-cluster tier markets, deprioritize price_move in favor of volume_delta + score combination since informed flow may precede detectable price impact.

### Suggested thresholds
`score_threshold` → `3.0`

### Recommendations

- [ ] **TB-042** `rejected` — Segment thresholds by market tier: apply stricter volume_delta multipliers (2x baseline) and price_move floors (5%+) to watch-tier NBA series to filter routine liquidity
  - **Governor rejection**: The proposed tweak conflicts with the historical NBA series/playoff winner markets constraint, which explicitly requires min_price_move ≥0.05 (5%) for low-liquidity, high-odds markets. The tweak sets min_price_move: None, relaxing this tightened threshold that was applied to prevent false positives from routine liquidity spikes without sufficient price conviction.
- [ ] **TB-043** `rejected` — For whale-cluster signals, reduce weight of price_move requirement since coherent volume flow (5k-2k deltas) at score=8.0 indicates informed positioning before market repricing
  - **Governor rejection**: The proposed tweak conflicts with the historical NBA series/playoff winner markets constraint, which explicitly requires min_price_move ≥0.05 (5%) for low-liquidity, high-odds markets. The tweak sets min_price_move: None, relaxing this tightened threshold that was applied to prevent false positives from routine liquidity spikes without sufficient price conviction.
- [ ] **TB-044** `rejected` — Raise global spike_score_threshold from current floor to 3.0+ for watch-tier markets to suppress low-signal alerts (score=2.823 was mislabeled)
  - **Governor rejection**: The proposed tweak conflicts with the historical NBA series/playoff winner markets constraint, which explicitly requires min_price_move ≥0.05 (5%) for low-liquidity, high-odds markets. The tweak sets min_price_move: None, relaxing this tightened threshold that was applied to prevent false positives from routine liquidity spikes without sufficient price conviction.
- [ ] **TB-045** `rejected` — Monitor whether zero price_move whale-cluster alerts correlate with subsequent price movement in trailing 5-15m window; if so, score=8.0 with volume coherence is predictive independent of immediate price_move
  - **Governor rejection**: The proposed tweak conflicts with the historical NBA series/playoff winner markets constraint, which explicitly requires min_price_move ≥0.05 (5%) for low-liquidity, high-odds markets. The tweak sets min_price_move: None, relaxing this tightened threshold that was applied to prevent false positives from routine liquidity spikes without sufficient price conviction.

---

## 2026-05-08 — Advisor snapshot O

### Summary
High-confidence whale-cluster signals with zero price movement are correctly labeled as genuine, but lower-confidence watch-tier signals with moderate volume spikes and small price moves are false positives due to routine liquidity in NBA series markets.

### Next step
Require minimum price move >0.03 for all tiers, with market-specific volume multipliers for NBA series

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `3.0`

### Recommendations

- [ ] **TB-046** `rejected` — Set min_price_move to 0.03 to filter zero/low price delta triggers
  - **Governor rejection**: Proposed tweak sets min_volume_delta: None, violating 'Prohibited relaxations: No min_volume_delta = None' and multiple historical constraints requiring specific volume deltas (e.g., NBA series: spike_min_volume_delta ≥2x baseline; 15m crypto: ≥15x-50x baseline; low-liquidity long-tail: ≥2000x baseline; global floors: spike_min_volume_delta >100k for watch-tier). This relaxes volume checks previously tightened to filter noise.
- [ ] **TB-047** `rejected` — Raise min_volume_delta multiplier to 2x baseline for NBA series markets
  - **Governor rejection**: Proposed tweak sets min_volume_delta: None, violating 'Prohibited relaxations: No min_volume_delta = None' and multiple historical constraints requiring specific volume deltas (e.g., NBA series: spike_min_volume_delta ≥2x baseline; 15m crypto: ≥15x-50x baseline; low-liquidity long-tail: ≥2000x baseline; global floors: spike_min_volume_delta >100k for watch-tier). This relaxes volume checks previously tightened to filter noise.
- [ ] **TB-048** `rejected` — Lower score_threshold to 3.0 to capture more true whale-clusters without increasing noise
  - **Governor rejection**: Proposed tweak sets min_volume_delta: None, violating 'Prohibited relaxations: No min_volume_delta = None' and multiple historical constraints requiring specific volume deltas (e.g., NBA series: spike_min_volume_delta ≥2x baseline; 15m crypto: ≥15x-50x baseline; low-liquidity long-tail: ≥2000x baseline; global floors: spike_min_volume_delta >100k for watch-tier). This relaxes volume checks previously tightened to filter noise.

---

## 2026-05-08 — Advisor snapshot P

### Summary
High volume delta whale-cluster signals in stable NBA series markets trigger frequently despite zero or minimal price impact, leading to false positives labeled as noise/unclear.

### Next step
Require minimum price move >0.5% for all whale-cluster tier signals to filter out high-volume events without directional impact.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-049** `rejected` — Raise min_volume_delta to 2x baseline volume for NBA series and whale-cluster tiers in high-liquidity markets.
  - **Governor rejection**: Violates 'Prohibited relaxations': Proposed tweak sets min_volume_delta: None, which is explicitly prohibited ('No min_volume_delta=None'). Additionally, it sets a blanket min_price_move: 0.005 (0.5%) that relaxes NBA series/playoff winner markets constraint requiring min_price_move ≥0.05 (5%), and global floors requiring spike_min_price_move ≥0.03 (3%). This removes asset-class/tier-specific multipliers and thresholds previously tightened to filter noise.
- [ ] **TB-050** `rejected` — Enforce min_price_move >=0.005 (0.5%) globally, or 0.05 (5%) specifically for NBA series watch tier.
  - **Governor rejection**: Violates 'Prohibited relaxations': Proposed tweak sets min_volume_delta: None, which is explicitly prohibited ('No min_volume_delta=None'). Additionally, it sets a blanket min_price_move: 0.005 (0.5%) that relaxes NBA series/playoff winner markets constraint requiring min_price_move ≥0.05 (5%), and global floors requiring spike_min_price_move ≥0.03 (3%). This removes asset-class/tier-specific multipliers and thresholds previously tightened to filter noise.
- [ ] **TB-051** `rejected` — Add tier-specific rule: whale-cluster requires priceΔ >0.005 OR sustained momentum across 3+ candles.
  - **Governor rejection**: Violates 'Prohibited relaxations': Proposed tweak sets min_volume_delta: None, which is explicitly prohibited ('No min_volume_delta=None'). Additionally, it sets a blanket min_price_move: 0.005 (0.5%) that relaxes NBA series/playoff winner markets constraint requiring min_price_move ≥0.05 (5%), and global floors requiring spike_min_price_move ≥0.03 (3%). This removes asset-class/tier-specific multipliers and thresholds previously tightened to filter noise.

---

## 2026-05-08 — Advisor snapshot Q

### Summary
False positives are prevalent in high-liquidity NBA series winner markets, where routine volume spikes (e.g., 800k+ volΔ) with minimal price moves (3%) are labeled as noise, while whale-cluster signals trigger on low price impact despite high scores.

### Next step
Require priceΔ >0.05 for all signals in high-baseline-volume markets like NBA series to filter routine liquidity without muting true whale activity.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [x] **TB-052** `applied` — Raise min_price_move to 0.05 globally to eliminate 3% noise triggers
- [x] **TB-053** `applied` — For NBA series markets, enforce 2x baseline volume multiplier and priceΔ >0.05
- [x] **TB-054** `applied` — For whale-cluster tier, require priceΔ >0.005 or sustained momentum across 3 candles

---

## 2026-05-08 — Advisor snapshot R

### Summary
False positives in NBA series winner markets from routine liquidity spikes with high absolute volume deltas but minimal price impact; whale-cluster signals trigger without price movement in high-liquidity environments.

### Next step
Require minimum price move >0.02 for all signals and raise volume multiplier to 2x baseline for NBA markets.

### Suggested thresholds
`min_price_move` → `0.025`

### Recommendations

- [ ] **TB-055** `rejected` — Raise min_price_move to 0.025 globally to filter zero/low-impact volume spikes.
  - **Governor rejection**: Violates 'Prohibited relaxations: No min_volume_delta=None' by explicitly setting min_volume_delta: None, which relaxes the previously tightened NBA-specific threshold of spike_min_volume_delta ≥2x baseline. Also conflicts with NBA historical constraint requiring ≥2x baseline by proposing a raise to 2x (redundant but paired with prohibited None) while weakening price move from ≥0.05 (5%) to 0.025 (2.5%).
- [ ] **TB-056** `rejected` — For NBA series markets, enforce volume delta >2x baseline and priceΔ >0.05.
  - **Governor rejection**: Violates 'Prohibited relaxations: No min_volume_delta=None' by explicitly setting min_volume_delta: None, which relaxes the previously tightened NBA-specific threshold of spike_min_volume_delta ≥2x baseline. Also conflicts with NBA historical constraint requiring ≥2x baseline by proposing a raise to 2x (redundant but paired with prohibited None) while weakening price move from ≥0.05 (5%) to 0.025 (2.5%).
- [ ] **TB-057** `rejected` — For whale-cluster tier in high-liquidity markets, require priceΔ >0.005 or sustained momentum across 3 candles.
  - **Governor rejection**: Violates 'Prohibited relaxations: No min_volume_delta=None' by explicitly setting min_volume_delta: None, which relaxes the previously tightened NBA-specific threshold of spike_min_volume_delta ≥2x baseline. Also conflicts with NBA historical constraint requiring ≥2x baseline by proposing a raise to 2x (redundant but paired with prohibited None) while weakening price move from ≥0.05 (5%) to 0.025 (2.5%).

---

## 2026-05-08 — Advisor snapshot S

### Summary
False positives dominate in high-volume NBA series winner markets from insignificant volume deltas and whale-clusters lacking price impact, while genuine signals show sustained volume with price movement.

### Next step
Require minimum price move >0.02 for all NBA series winner markets and raise volume delta threshold to 2x baseline for high-liquidity markets.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.025`

### Recommendations

- [ ] **TB-058** `rejected` — Market-specific rule: For NBA series winners, enforce min_price_move >= 0.025 to filter noise.
  - **Governor rejection**: Violates 'Prohibited relaxations': No min_price_move=None; proposed min_price_move: 0.025 < historical min_price_move ≥0.05 (5%) for NBA series/playoff winner markets (low-liquidity, high-odds). Also violates 'score_threshold ≥2.2' global floor by setting score_threshold: None.
- [ ] **TB-059** `rejected` — Raise spike_min_volume_delta to 0.5x baseline for high-volume markets like NBA playoffs.
  - **Governor rejection**: Violates 'Prohibited relaxations': No min_price_move=None; proposed min_price_move: 0.025 < historical min_price_move ≥0.05 (5%) for NBA series/playoff winner markets (low-liquidity, high-odds). Also violates 'score_threshold ≥2.2' global floor by setting score_threshold: None.
- [ ] **TB-060** `rejected` — For whale-cluster tier, require priceΔ >0.015 or volΔ >10x baseline to confirm impact.
  - **Governor rejection**: Violates 'Prohibited relaxations': No min_price_move=None; proposed min_price_move: 0.025 < historical min_price_move ≥0.05 (5%) for NBA series/playoff winner markets (low-liquidity, high-odds). Also violates 'score_threshold ≥2.2' global floor by setting score_threshold: None.

---

## 2026-05-08 — Advisor snapshot T

### Summary
False positives in high-volume NBA series winner markets from routine liquidity spikes misclassified as signals, despite moderate price moves.

### Next step
Introduce market-type specific volume multipliers, requiring at least 2x baseline volume delta for high-volume markets like NBA series.

### Recommendations

- [ ] **TB-061** `rejected` — Raise min_volume_delta threshold to 0.5x baseline for high-volume NBA markets
  - **Governor rejection**: Proposed tweak sets min_volume_delta: None, min_price_move: None, and score_threshold: None, directly violating 'Prohibited relaxations': No min_price_move=None; no min_volume_delta=None; no score_threshold=None. Additionally conflicts with NBA series/playoff winner markets constraint requiring min_price_move ≥0.05 (5%) and sports asset-class rules maintaining spike_min_volume_delta ≥2x baseline.
- [ ] **TB-062** `rejected` — Increase volume multiplier to 2x baseline specifically for NBA series winner markets
  - **Governor rejection**: Proposed tweak sets min_volume_delta: None, min_price_move: None, and score_threshold: None, directly violating 'Prohibited relaxations': No min_price_move=None; no min_volume_delta=None; no score_threshold=None. Additionally conflicts with NBA series/playoff winner markets constraint requiring min_price_move ≥0.05 (5%) and sports asset-class rules maintaining spike_min_volume_delta ≥2x baseline.
- [ ] **TB-063** `rejected` — Combine volume delta with price move confirmation to filter insignificant trades
  - **Governor rejection**: Proposed tweak sets min_volume_delta: None, min_price_move: None, and score_threshold: None, directly violating 'Prohibited relaxations': No min_price_move=None; no min_volume_delta=None; no score_threshold=None. Additionally conflicts with NBA series/playoff winner markets constraint requiring min_price_move ≥0.05 (5%) and sports asset-class rules maintaining spike_min_volume_delta ≥2x baseline.

---

## 2026-05-08 — Advisor snapshot U

### Summary
False positives in high-volume NBA series winner markets from routine liquidity spikes and insignificant trades, despite decent scores and minor price moves.

### Next step
Introduce market-type specific volume multipliers (e.g., 2x baseline for high-volume NBA series) to filter routine spikes.

### Recommendations

- [ ] **TB-064** `rejected` — Raise volume delta threshold to 0.5x baseline for high-volume NBA series winner markets
  - **Governor rejection**: The proposed tweak sets min_volume_delta: None and min_price_move: None, which directly violates the 'Prohibited relaxations' historical constraint: 'No min_volume_delta=None; no min_price_move=None'. This relaxes global floors and asset-class specific thresholds (e.g., NBA series: min_price_move ≥0.05; low-liquidity: min_price_move ≥0.05) that were explicitly tightened to prevent noise and regressions.
- [ ] **TB-065** `rejected` — Increase min volume multiplier to 2x baseline for NBA playoff series markets
  - **Governor rejection**: The proposed tweak sets min_volume_delta: None and min_price_move: None, which directly violates the 'Prohibited relaxations' historical constraint: 'No min_volume_delta=None; no min_price_move=None'. This relaxes global floors and asset-class specific thresholds (e.g., NBA series: min_price_move ≥0.05; low-liquidity: min_price_move ≥0.05) that were explicitly tightened to prevent noise and regressions.
- [ ] **TB-066** `rejected` — Add market category rules to dynamically adjust volume thresholds based on baseline liquidity
  - **Governor rejection**: The proposed tweak sets min_volume_delta: None and min_price_move: None, which directly violates the 'Prohibited relaxations' historical constraint: 'No min_volume_delta=None; no min_price_move=None'. This relaxes global floors and asset-class specific thresholds (e.g., NBA series: min_price_move ≥0.05; low-liquidity: min_price_move ≥0.05) that were explicitly tightened to prevent noise and regressions.

---

## 2026-05-08 — Advisor snapshot V

### Summary
Detector is generating false positives on volume-only movements lacking price confirmation, particularly in NBA series markets where large volume deltas occur with zero or minimal price movement (priceΔ=0.0).

### Next step
Implement a price-move floor of 0.02-0.03 minimum fractional change required even when volume delta is high; volume alone without directional price confirmation is insufficient signal.

### Suggested thresholds
`min_volume_delta` → `0.5`, `min_price_move` → `0.02`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-067** `rejected` — Require priceΔ ≥ 0.02 (2%) alongside elevated volume to emit signal; current signals show many spike_score=8.0 with priceΔ=0.0 labeled as false positives
  - **Governor rejection**: Violates **NBA series/playoff winner markets (low-liq, high-odds)** constraint: min_price_move ≥0.05 (5%). Proposed min_price_move: 0.02 is a relaxation below the explicit 0.05 floor required for these markets to prevent noise in low-liq, high-odds scenarios. Also risks violating **Prohibited relaxations**: no weakening NBA price_move <0.05.
- [ ] **TB-068** `rejected` — Increase spike_min_volume_delta to 0.5x market baseline for whale-cluster tier in prediction markets; current signals with volΔ=2000-9991 are noise despite high score
  - **Governor rejection**: Violates **NBA series/playoff winner markets (low-liq, high-odds)** constraint: min_price_move ≥0.05 (5%). Proposed min_price_move: 0.02 is a relaxation below the explicit 0.05 floor required for these markets to prevent noise in low-liq, high-odds scenarios. Also risks violating **Prohibited relaxations**: no weakening NBA price_move <0.05.
- [ ] **TB-069** `rejected` — Lower spike_score_threshold from 8.0 to 6.5 or add volume-to-price correlation gate; high score + zero price movement indicates detection model is weighting volume too heavily
  - **Governor rejection**: Violates **NBA series/playoff winner markets (low-liq, high-odds)** constraint: min_price_move ≥0.05 (5%). Proposed min_price_move: 0.02 is a relaxation below the explicit 0.05 floor required for these markets to prevent noise in low-liq, high-odds scenarios. Also risks violating **Prohibited relaxations**: no weakening NBA price_move <0.05.

---

## 2026-05-08 — Advisor snapshot W

### Summary
Whale-cluster tier signals are firing with high scores (8.0) but zero price impact, generating noise. Watch-tier signals are also triggering on minimal volume deltas relative to baseline, particularly in high-liquidity NBA series markets.

### Next step
Implement a composite gating rule: for whale-cluster events, require either price_move > 0.5% OR volume_delta > 10% of baseline; for watch tier, enforce volume_delta multiplier threshold of 2.0x baseline to filter routine liquidity noise.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-070** `rejected` — Whale-cluster signals: require price_move >= 0.005 (0.5%) as hard floor when priceΔ=0.0, or escalate volume_delta requirement to 10000+ with baseline context
  - **Governor rejection**: Violates multiple historical constraints: (1) 'Prohibited relaxations: no None thresholds' - proposes min_volume_delta: None and score_threshold: None; (2) 'Global floors: no min_price_move=None; no min_volume_delta=None; no score_threshold=None' - directly sets these to None; (3) 'Global floors: spike_min_price_move ≥0.03 (3%)' - proposes min_price_move: 0.005 (0.5%) which relaxes below 3%; (4) For NBA series markets (high-liq), weakens volume gating by setting min_volume_delta: None instead of maintaining ≥2x baseline or >10 recent trades.
- [ ] **TB-071** `rejected` — Watch-tier signals: raise spike_min_volume_delta to 2.0x rolling baseline for high-volume markets (NBA series) to suppress routine trading activity
  - **Governor rejection**: Violates multiple historical constraints: (1) 'Prohibited relaxations: no None thresholds' - proposes min_volume_delta: None and score_threshold: None; (2) 'Global floors: no min_price_move=None; no min_volume_delta=None; no score_threshold=None' - directly sets these to None; (3) 'Global floors: spike_min_price_move ≥0.03 (3%)' - proposes min_price_move: 0.005 (0.5%) which relaxes below 3%; (4) For NBA series markets (high-liq), weakens volume gating by setting min_volume_delta: None instead of maintaining ≥2x baseline or >10 recent trades.
- [ ] **TB-072** `rejected` — Add market-specific multipliers: apply stricter thresholds to liquid playoff markets where large volume deltas occur frequently without directional intent
  - **Governor rejection**: Violates multiple historical constraints: (1) 'Prohibited relaxations: no None thresholds' - proposes min_volume_delta: None and score_threshold: None; (2) 'Global floors: no min_price_move=None; no min_volume_delta=None; no score_threshold=None' - directly sets these to None; (3) 'Global floors: spike_min_price_move ≥0.03 (3%)' - proposes min_price_move: 0.005 (0.5%) which relaxes below 3%; (4) For NBA series markets (high-liq), weakens volume gating by setting min_volume_delta: None instead of maintaining ≥2x baseline or >10 recent trades.

---

## 2026-05-08 — Advisor snapshot X

### Summary
Whale-cluster tier signals are generating false positives with high volume deltas but zero price impact, while watch-tier signals flag insignificant trades. The detector is too permissive on volume-only activity without requiring price confirmation.

### Next step
Implement a dual-gate requirement: for whale-cluster events, require EITHER price_move >= 0.5% OR volume_delta >= 10% of baseline (not volume delta alone). For watch-tier, raise volume delta floor to 0.5x baseline.

### Suggested thresholds
`min_volume_delta` → `10000.0`, `min_price_move` → `0.005`, `score_threshold` → `7.0`

### Recommendations

- [ ] **TB-073** `rejected` — Add compound rule: whale-cluster signals must show price_move > 0.005 (0.5%) OR volΔ > 10% of market baseline, rejecting volume-only spikes
  - **Governor rejection**: Violates multiple historical constraints: 1) Prohibited relaxations - proposes min_price_move=0.005 (0.5%) which is sub-3% global price_move floor (global floors: spike_min_price_move ≥0.03). 2) Low-liquidity/high-odds (tier=watch/notable): requires min_price_move ≥0.05 (5%), but proposal sets 0.005. 3) NBA series/playoff winner markets: min_price_move ≥0.05, violated by 0.005. 4) Watch-tier signals: proposes lowering volume delta floor to 0.5x baseline, weakening the required ≥2x baseline. 5) Global floors: min_volume_delta >100k (watch-tier), but fixed 10000.0 is a relaxation without asset-specific context.
- [ ] **TB-074** `rejected` — Raise spike_min_volume_delta threshold by tier: whale-cluster minimum 10000 units or 10% baseline; watch-tier minimum 700 units or 0.5x baseline
  - **Governor rejection**: Violates multiple historical constraints: 1) Prohibited relaxations - proposes min_price_move=0.005 (0.5%) which is sub-3% global price_move floor (global floors: spike_min_price_move ≥0.03). 2) Low-liquidity/high-odds (tier=watch/notable): requires min_price_move ≥0.05 (5%), but proposal sets 0.005. 3) NBA series/playoff winner markets: min_price_move ≥0.05, violated by 0.005. 4) Watch-tier signals: proposes lowering volume delta floor to 0.5x baseline, weakening the required ≥2x baseline. 5) Global floors: min_volume_delta >100k (watch-tier), but fixed 10000.0 is a relaxation without asset-specific context.
- [ ] **TB-075** `rejected` — Lower spike_score_threshold to 7.0 for whale-cluster to increase selectivity and rely more on structural gating rules than score alone
  - **Governor rejection**: Violates multiple historical constraints: 1) Prohibited relaxations - proposes min_price_move=0.005 (0.5%) which is sub-3% global price_move floor (global floors: spike_min_price_move ≥0.03). 2) Low-liquidity/high-odds (tier=watch/notable): requires min_price_move ≥0.05 (5%), but proposal sets 0.005. 3) NBA series/playoff winner markets: min_price_move ≥0.05, violated by 0.005. 4) Watch-tier signals: proposes lowering volume delta floor to 0.5x baseline, weakening the required ≥2x baseline. 5) Global floors: min_volume_delta >100k (watch-tier), but fixed 10000.0 is a relaxation without asset-specific context.

---

## 2026-05-08 — Advisor snapshot Y

### Summary
All recent whale-cluster signals show zero price movement despite high volume deltas and scores, labeled mostly as noise/unclear or signal/no, indicating false positives from volume-only triggers without price confirmation.

### Next step
Require minimum price move >0.5% for all whale-cluster detections to filter out volume spikes lacking directional impact.

### Suggested thresholds
`min_volume_delta` → `10000.0`, `min_price_move` → `0.005`

### Recommendations

- [ ] **TB-076** `rejected` — Set spike_min_price_move to 0.005 to eliminate zero-price signals.
  - **Governor rejection**: VIOLATION OF GLOBAL FLOOR CONSTRAINT: Proposed score_threshold: None violates explicit global floor rule 'no score_threshold=None'. Historical constraints mandate score_threshold ≥2.2 as a required threshold with no exceptions. Additionally, min_price_move=0.005 (0.5%) violates GLOBAL FLOOR spike_min_price_move ≥0.03 (3%) for general spike detection. While the 0.5% threshold is permitted as a conditional escape clause in specific crypto 15m markets (priceΔ ≥0.005 OR volume multiplier ≥15x-50x), applying it as a blanket requirement for 'all whale-cluster detections' removes mandatory price-move floors across other asset classes and market tiers. This introduces regression risk by weakening protections on NBA/playoff markets (which require min_price_move ≥0.05) and notable-tier markets (min_price_move ≥0.05). The removal of score_threshold entirely also violates the prohibition on None thresholds.
- [ ] **TB-077** `rejected` — For whale-cluster tier, raise spike_min_volume_delta to 10000 to reduce medium-volume false positives.
  - **Governor rejection**: VIOLATION OF GLOBAL FLOOR CONSTRAINT: Proposed score_threshold: None violates explicit global floor rule 'no score_threshold=None'. Historical constraints mandate score_threshold ≥2.2 as a required threshold with no exceptions. Additionally, min_price_move=0.005 (0.5%) violates GLOBAL FLOOR spike_min_price_move ≥0.03 (3%) for general spike detection. While the 0.5% threshold is permitted as a conditional escape clause in specific crypto 15m markets (priceΔ ≥0.005 OR volume multiplier ≥15x-50x), applying it as a blanket requirement for 'all whale-cluster detections' removes mandatory price-move floors across other asset classes and market tiers. This introduces regression risk by weakening protections on NBA/playoff markets (which require min_price_move ≥0.05) and notable-tier markets (min_price_move ≥0.05). The removal of score_threshold entirely also violates the prohibition on None thresholds.
- [ ] **TB-078** `rejected` — Increase spike_score_threshold to 8.5 if price move condition is met, to further cull borderline cases.
  - **Governor rejection**: VIOLATION OF GLOBAL FLOOR CONSTRAINT: Proposed score_threshold: None violates explicit global floor rule 'no score_threshold=None'. Historical constraints mandate score_threshold ≥2.2 as a required threshold with no exceptions. Additionally, min_price_move=0.005 (0.5%) violates GLOBAL FLOOR spike_min_price_move ≥0.03 (3%) for general spike detection. While the 0.5% threshold is permitted as a conditional escape clause in specific crypto 15m markets (priceΔ ≥0.005 OR volume multiplier ≥15x-50x), applying it as a blanket requirement for 'all whale-cluster detections' removes mandatory price-move floors across other asset classes and market tiers. This introduces regression risk by weakening protections on NBA/playoff markets (which require min_price_move ≥0.05) and notable-tier markets (min_price_move ≥0.05). The removal of score_threshold entirely also violates the prohibition on None thresholds.

---

## 2026-05-08 — Advisor snapshot Z

### Summary
Whale-cluster signals are generating frequent false positives in low-price-impact markets like NBA series bets, where high volume deltas occur without any price movement, leading to noise alerts labeled as unclear or low/medium signal.

### Next step
Require minimum price move >0.005 (0.5%) OR volume delta >10% of baseline volume for all tiers to filter noise.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `4.5`

### Recommendations

- [ ] **TB-079** `rejected` — Raise spike_min_price_move to 0.005 to eliminate zero-price-move false positives
  - **Governor rejection**: Proposed min_volume_delta: None violates global floors constraint 'no None thresholds (min_price_move, min_volume_delta, score_threshold)' and prohibited relaxations 'no min_price_move/volume_delta/score_threshold=None'. Also conflicts with NBA series markets requiring spike_min_volume_delta ≥2x baseline and low-liq requiring >10 recent trades; min_price_move=0.005 (0.5%) violates global floors spike_min_price_move ≥0.03 (3%) and NBA/low-liq min_price_move ≥0.05 (5%). score_threshold=4.5 likely weakens tier-aware requirements (watch ≥8, notable ≥500).
- [ ] **TB-080** `rejected` — For whale-cluster tier, add market-specific baseline volume check (e.g., volΔ >10% of avg hourly volume)
  - **Governor rejection**: Proposed min_volume_delta: None violates global floors constraint 'no None thresholds (min_price_move, min_volume_delta, score_threshold)' and prohibited relaxations 'no min_price_move/volume_delta/score_threshold=None'. Also conflicts with NBA series markets requiring spike_min_volume_delta ≥2x baseline and low-liq requiring >10 recent trades; min_price_move=0.005 (0.5%) violates global floors spike_min_price_move ≥0.03 (3%) and NBA/low-liq min_price_move ≥0.05 (5%). score_threshold=4.5 likely weakens tier-aware requirements (watch ≥8, notable ≥500).
- [ ] **TB-081** `rejected` — Increase spike_score_threshold to 4.5 to reduce medium-score watchlist noise
  - **Governor rejection**: Proposed min_volume_delta: None violates global floors constraint 'no None thresholds (min_price_move, min_volume_delta, score_threshold)' and prohibited relaxations 'no min_price_move/volume_delta/score_threshold=None'. Also conflicts with NBA series markets requiring spike_min_volume_delta ≥2x baseline and low-liq requiring >10 recent trades; min_price_move=0.005 (0.5%) violates global floors spike_min_price_move ≥0.03 (3%) and NBA/low-liq min_price_move ≥0.05 (5%). score_threshold=4.5 likely weakens tier-aware requirements (watch ≥8, notable ≥500).

---

## 2026-05-08 — Advisor snapshot 27

### Summary
Multiple whale-cluster signals in KXNBASERIES-26CLEDETR2-DET market are labeled as noise/false positives despite high scores and volume deltas, due to zero price movement; false positives can be reduced by requiring price impact.

### Next step
Require minimum price move >0.005 (0.5%) for all signals, especially whale-clusters.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `4.0`

### Recommendations

- [ ] **TB-082** `rejected` — Set min_price_move to 0.005 to filter zero-price-move events.
  - **Governor rejection**: Proposed min_volume_delta: None violates 'Global Floors: spike_min_volume_delta >100k (watch-tier)' and 'Prohibited Relaxations: no min_price_move/volume_delta/score_threshold=None'. Also conflicts with market-specific rules like 'NBA Series/Playoff Winner Markets: spike_min_volume_delta ≥2x baseline' and 'Low-Liquidity/High-Odds Markets: spike_min_volume_delta implied via >10 recent trades'. Setting volume_delta to None relaxes historical constraints requiring minimum volume deltas, which were tightened to filter noise.
- [ ] **TB-083** `rejected` — For whale-cluster tier, require volΔ >10000 AND priceΔ >0.005.
  - **Governor rejection**: Proposed min_volume_delta: None violates 'Global Floors: spike_min_volume_delta >100k (watch-tier)' and 'Prohibited Relaxations: no min_price_move/volume_delta/score_threshold=None'. Also conflicts with market-specific rules like 'NBA Series/Playoff Winner Markets: spike_min_volume_delta ≥2x baseline' and 'Low-Liquidity/High-Odds Markets: spike_min_volume_delta implied via >10 recent trades'. Setting volume_delta to None relaxes historical constraints requiring minimum volume deltas, which were tightened to filter noise.
- [ ] **TB-084** `rejected` — Raise score_threshold to 4.0 to reduce low-confidence emissions like KXTRUMPSAYNICKNAME.
  - **Governor rejection**: Proposed min_volume_delta: None violates 'Global Floors: spike_min_volume_delta >100k (watch-tier)' and 'Prohibited Relaxations: no min_price_move/volume_delta/score_threshold=None'. Also conflicts with market-specific rules like 'NBA Series/Playoff Winner Markets: spike_min_volume_delta ≥2x baseline' and 'Low-Liquidity/High-Odds Markets: spike_min_volume_delta implied via >10 recent trades'. Setting volume_delta to None relaxes historical constraints requiring minimum volume deltas, which were tightened to filter noise.

---

## 2026-05-08 — Advisor snapshot 28

### Summary
Whale-cluster signals are generating false positives in low-price-impact scenarios, as seen in KXNBASERIES where zero price move (priceΔ=0.0) despite high score (8.0) and volume delta was labeled noise/unclear/low.

### Next step
Require minimum price move >0.005 (0.5%) for all whale-cluster tier signals to filter out volume-only anomalies.

### Suggested thresholds
`min_price_move` → `0.005`, `score_threshold` → `4.5`

### Recommendations

- [ ] **TB-085** `rejected` — Raise spike_min_price_move to 0.005 to eliminate zero/low impact spikes.
  - **Governor rejection**: Conflicts with **NBA Series/Playoff Winner Markets (low-liq, high-odds)** constraint requiring min_price_move ≥0.05 (5%), and **Low-Liquidity/High-Odds Markets (tier=watch/notable)** and **Notable-Tier Markets** also requiring min_price_move ≥0.05 (5%). Proposed min_price_move=0.005 (0.5%) weakens these floors. Additionally violates **Global Floors** no None thresholds rule by setting min_volume_delta: None, and **Prohibited Relaxations** by weakening below specified floors for NBA/low-liq markets.
- [ ] **TB-086** `rejected` — For tier=whale-cluster, enforce volΔ >10% of 1h baseline volume.
  - **Governor rejection**: Conflicts with **NBA Series/Playoff Winner Markets (low-liq, high-odds)** constraint requiring min_price_move ≥0.05 (5%), and **Low-Liquidity/High-Odds Markets (tier=watch/notable)** and **Notable-Tier Markets** also requiring min_price_move ≥0.05 (5%). Proposed min_price_move=0.005 (0.5%) weakens these floors. Additionally violates **Global Floors** no None thresholds rule by setting min_volume_delta: None, and **Prohibited Relaxations** by weakening below specified floors for NBA/low-liq markets.
- [ ] **TB-087** `rejected` — Increase spike_score_threshold to 4.5 to reduce medium/low confidence emissions like KXTRUMPSAYNICKNAME.
  - **Governor rejection**: Conflicts with **NBA Series/Playoff Winner Markets (low-liq, high-odds)** constraint requiring min_price_move ≥0.05 (5%), and **Low-Liquidity/High-Odds Markets (tier=watch/notable)** and **Notable-Tier Markets** also requiring min_price_move ≥0.05 (5%). Proposed min_price_move=0.005 (0.5%) weakens these floors. Additionally violates **Global Floors** no None thresholds rule by setting min_volume_delta: None, and **Prohibited Relaxations** by weakening below specified floors for NBA/low-liq markets.

---

## 2026-05-09 — Advisor snapshot 29

### Summary
Two signals on the same market with identical low priceΔ=0.02 but high volΔ show inconsistency in analyst labeling (one noise/unclear, one signal), indicating false positives from thin volatility despite volume spikes.

### Next step
Raise min_price_move threshold to filter out low-magnitude moves (<3%) that trigger on volume alone.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `2.2`

### Recommendations

- [ ] **TB-088** `rejected` — Increase min_price_move from 0.02 to 0.03 to require stronger price confirmation
  - **Governor rejection**: Violates Global Floors constraint: proposed min_price_move=0.03 is below the required floor of ≥0.05 (5%). Also violates Prohibited Relaxations: no sub-3% global price_move allowed (0.03=3%). Additionally conflicts with NBA Series/Playoff Winner Markets, Low-Liquidity/High-Odds Markets, and Notable-Tier Markets which explicitly require min_price_move ≥0.05. Setting min_volume_delta: None violates 'no None thresholds (min_price_move, min_volume_delta, score_threshold)'.
- [ ] **TB-089** `rejected` — Add dynamic volume delta multiplier (1.5x baseline) for high-conviction markets (>75% implied prob)
  - **Governor rejection**: Violates Global Floors constraint: proposed min_price_move=0.03 is below the required floor of ≥0.05 (5%). Also violates Prohibited Relaxations: no sub-3% global price_move allowed (0.03=3%). Additionally conflicts with NBA Series/Playoff Winner Markets, Low-Liquidity/High-Odds Markets, and Notable-Tier Markets which explicitly require min_price_move ≥0.05. Setting min_volume_delta: None violates 'no None thresholds (min_price_move, min_volume_delta, score_threshold)'.
- [ ] **TB-090** `rejected` — Raise score_threshold to 2.2 to suppress borderline watch-tier signals with unclear labels
  - **Governor rejection**: Violates Global Floors constraint: proposed min_price_move=0.03 is below the required floor of ≥0.05 (5%). Also violates Prohibited Relaxations: no sub-3% global price_move allowed (0.03=3%). Additionally conflicts with NBA Series/Playoff Winner Markets, Low-Liquidity/High-Odds Markets, and Notable-Tier Markets which explicitly require min_price_move ≥0.05. Setting min_volume_delta: None violates 'no None thresholds (min_price_move, min_volume_delta, score_threshold)'.

---

## 2026-05-09 — Advisor snapshot 30

### Summary
False positives cluster in low-liquidity markets where tiny absolute trades trigger disproportionate volume-delta ratios, and in high-conviction markets where thin intraday noise gets amplified by sensitive scoring.

### Next step
Implement dual-threshold logic: enforce minimum absolute volume floor ($1,000+) for low-tier markets independent of volume delta multiplier, and raise volume-delta multiplier for high-probability contracts (>75% implied) to filter thin volatility.

### Suggested thresholds
`min_volume_delta` → `1.5`

### Recommendations

- [ ] **TB-091** `rejected` — Add market-tier-aware volume floor: require spike_min_absolute_volume >= $1,000 for watch-tier or low-liquidity markets, overriding volume-delta ratio logic
  - **Governor rejection**: Proposed tweak violates multiple historical constraints: (1) Sets min_price_move to None, directly contradicting 'Global Floors' requirement that min_price_move ≥0.05 with explicit prohibition on None thresholds; (2) Sets score_threshold to None, violating 'Global Floors' requirement that score_threshold ≥2.2 with explicit prohibition on None thresholds; (3) Reduces min_volume_delta to 1.5x baseline for low-tier markets, conflicting with established floors for Watch-Tier (≥2x baseline), NBA/low-liq markets (≥2x baseline), and Long-Tail markets (≥2000x baseline). The 'Prohibited Relaxations' clause explicitly forbids weakening below specified floors and disallows None settings. This tweak attempts to implement a dual-threshold workaround that bypasses rather than respects the established constraint hierarchy.
- [ ] **TB-092** `rejected` — Raise spike_min_volume_delta multiplier from 1.0x to 1.5x–2.0x baseline for high-conviction markets (yes_prob > 0.75) to dampen intraday noise
  - **Governor rejection**: Proposed tweak violates multiple historical constraints: (1) Sets min_price_move to None, directly contradicting 'Global Floors' requirement that min_price_move ≥0.05 with explicit prohibition on None thresholds; (2) Sets score_threshold to None, violating 'Global Floors' requirement that score_threshold ≥2.2 with explicit prohibition on None thresholds; (3) Reduces min_volume_delta to 1.5x baseline for low-tier markets, conflicting with established floors for Watch-Tier (≥2x baseline), NBA/low-liq markets (≥2x baseline), and Long-Tail markets (≥2000x baseline). The 'Prohibited Relaxations' clause explicitly forbids weakening below specified floors and disallows None settings. This tweak attempts to implement a dual-threshold workaround that bypasses rather than respects the established constraint hierarchy.
- [ ] **TB-093** `rejected` — Lower spike_min_price_move threshold slightly (0.025–0.03) but only when volume_delta exceeds 3.0x baseline, to avoid compensatory over-tuning
  - **Governor rejection**: Proposed tweak violates multiple historical constraints: (1) Sets min_price_move to None, directly contradicting 'Global Floors' requirement that min_price_move ≥0.05 with explicit prohibition on None thresholds; (2) Sets score_threshold to None, violating 'Global Floors' requirement that score_threshold ≥2.2 with explicit prohibition on None thresholds; (3) Reduces min_volume_delta to 1.5x baseline for low-tier markets, conflicting with established floors for Watch-Tier (≥2x baseline), NBA/low-liq markets (≥2x baseline), and Long-Tail markets (≥2000x baseline). The 'Prohibited Relaxations' clause explicitly forbids weakening below specified floors and disallows None settings. This tweak attempts to implement a dual-threshold workaround that bypasses rather than respects the established constraint hierarchy.

---

## 2026-05-09 — Advisor snapshot 31

### Summary
NBA series markets are generating false positives labeled as noise due to liquidity-driven volume spikes with modest price moves (2-3%) that lack genuine trading activity.

### Next step
Introduce market-type rules for NBA series: require 2x volume delta, 1%+ price move, and non-zero recent trades to filter mechanical liquidity noise.

### Suggested thresholds
`min_volume_delta` → `2.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-094** `rejected` — Raise min_volume_delta multiplier to 2x baseline for NBA series markets
  - **Governor rejection**: Conflicts with NBA Series/Playoff Winner Markets constraint: 'min_price_move ≥0.05 (5%)'. Proposed min_price_move: 0.01 (1%) relaxes the explicitly tightened 5% floor designed to filter noise in these markets. Also conflicts with Global Price-Move Floor: 'spike_min_price_move ≥0.03 (3%)' by proposing 1%.
- [ ] **TB-095** `rejected` — Set min_price_move to 0.01 (1%) minimum for watch-tier NBA signals
  - **Governor rejection**: Conflicts with NBA Series/Playoff Winner Markets constraint: 'min_price_move ≥0.05 (5%)'. Proposed min_price_move: 0.01 (1%) relaxes the explicitly tightened 5% floor designed to filter noise in these markets. Also conflicts with Global Price-Move Floor: 'spike_min_price_move ≥0.03 (3%)' by proposing 1%.
- [ ] **TB-096** `rejected` — Add rule requiring non-zero recent trade volume for NBA markets
  - **Governor rejection**: Conflicts with NBA Series/Playoff Winner Markets constraint: 'min_price_move ≥0.05 (5%)'. Proposed min_price_move: 0.01 (1%) relaxes the explicitly tightened 5% floor designed to filter noise in these markets. Also conflicts with Global Price-Move Floor: 'spike_min_price_move ≥0.03 (3%)' by proposing 1%.

---

## 2026-05-09 — Advisor snapshot 32

### Summary
Low price moves (2%) with high volume deltas are generating false positives in NBA series markets, labeled as noise despite some signal potential; liquidity-driven spikes are overwhelming genuine signals.

### Next step
Require minimum 1% price move AND 1.5x volume delta multiplier for sports markets like NBA series to filter liquidity noise.

### Suggested thresholds
`min_price_move` → `0.01`, `score_threshold` → `1.5`

### Recommendations

- [ ] **TB-097** `rejected` — Raise min_price_move to 0.01 globally to eliminate sub-1% spikes.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) min_price_move of 0.01 (1%) falls below the Global Floor of ≥0.05 (5%) and the NBA Series/Playoff Winner Markets explicit requirement of ≥0.05 (5%); (2) min_volume_delta set to None violates the Global Floor prohibition against None thresholds and the NBA Series explicit requirement of ≥2x baseline; (3) score_threshold of 1.5 falls below the Global Floor of ≥2.2. These are explicitly tightened constraints that were applied to prevent false positives in low-liquidity, high-odds markets like NBA series. Relaxing them to 1%, None, and 1.5 respectively directly contradicts the 'Prohibited Relaxations' rule against weakening specified floors.
- [ ] **TB-098** `rejected` — Introduce market-type rules: NBA series require vol delta 1.5x baseline + 1% price move.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) min_price_move of 0.01 (1%) falls below the Global Floor of ≥0.05 (5%) and the NBA Series/Playoff Winner Markets explicit requirement of ≥0.05 (5%); (2) min_volume_delta set to None violates the Global Floor prohibition against None thresholds and the NBA Series explicit requirement of ≥2x baseline; (3) score_threshold of 1.5 falls below the Global Floor of ≥2.2. These are explicitly tightened constraints that were applied to prevent false positives in low-liquidity, high-odds markets like NBA series. Relaxing them to 1%, None, and 1.5 respectively directly contradicts the 'Prohibited Relaxations' rule against weakening specified floors.
- [ ] **TB-099** `rejected` — Increase score_threshold to 1.5 to reduce low-confidence watch-tier signals.
  - **Governor rejection**: The proposed tweak violates multiple historical constraints: (1) min_price_move of 0.01 (1%) falls below the Global Floor of ≥0.05 (5%) and the NBA Series/Playoff Winner Markets explicit requirement of ≥0.05 (5%); (2) min_volume_delta set to None violates the Global Floor prohibition against None thresholds and the NBA Series explicit requirement of ≥2x baseline; (3) score_threshold of 1.5 falls below the Global Floor of ≥2.2. These are explicitly tightened constraints that were applied to prevent false positives in low-liquidity, high-odds markets like NBA series. Relaxing them to 1%, None, and 1.5 respectively directly contradicts the 'Prohibited Relaxations' rule against weakening specified floors.

---

## 2026-05-09 — Advisor snapshot 33

### Summary
False positives in NBA series markets from one-sided reinforcement trades with moderate volume spikes and minimal price moves, while borderline signals with low scores can still be informative.

### Next step
Introduce category-specific thresholds for sports markets like NBA series, requiring higher volume multipliers and price moves to filter skewed outcome noise.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `1.5`

### Recommendations

- [ ] **TB-100** `rejected` — Raise min_price_move to 0.05 for NBA series markets to filter <5% moves
  - **Governor rejection**: The proposed tweak violates **Global Floors** (score_threshold ≥2.2) and **Prohibited Relaxations** (no score_threshold <2.2). The suggested score_threshold: 1.5 weakens the global floor below the explicitly required minimum of 2.2, which was tightened to prevent regressions from low-score noise. It also sets min_volume_delta: None, violating the global prohibition on None thresholds for min_volume_delta.
- [ ] **TB-101** `rejected` — Require volume delta >1.5x baseline average for heavily skewed markets (yes<0.3)
  - **Governor rejection**: The proposed tweak violates **Global Floors** (score_threshold ≥2.2) and **Prohibited Relaxations** (no score_threshold <2.2). The suggested score_threshold: 1.5 weakens the global floor below the explicitly required minimum of 2.2, which was tightened to prevent regressions from low-score noise. It also sets min_volume_delta: None, violating the global prohibition on None thresholds for min_volume_delta.
- [ ] **TB-102** `rejected` — Increase score_threshold to 1.5 globally to reduce watch-tier noise
  - **Governor rejection**: The proposed tweak violates **Global Floors** (score_threshold ≥2.2) and **Prohibited Relaxations** (no score_threshold <2.2). The suggested score_threshold: 1.5 weakens the global floor below the explicitly required minimum of 2.2, which was tightened to prevent regressions from low-score noise. It also sets min_volume_delta: None, violating the global prohibition on None thresholds for min_volume_delta.

---

## 2026-05-09 — Advisor snapshot 34

### Summary
Recent signals show false positives in high-liquidity markets like playoff series due to volume deltas from quotes rather than genuine trade flow, despite low price moves (2%) and moderate scores.

### Next step
Require net directional flow (yes/no imbalance > threshold) alongside volume delta to confirm real trading activity.

### Suggested thresholds
`min_price_move` → `0.025`

### Recommendations

- [ ] **TB-103** `rejected` — Raise volume delta multiplier to 1.5x baseline globally, 2x for high-liquidity markets like playoffs
  - **Governor rejection**: Proposed tweak violates multiple Global Floors: (1) min_volume_delta=None is prohibited (no None thresholds allowed, Volume-Delta Floor requires >100k for watch-tier); (2) min_price_move=0.025 < 0.03 (Price-Move Floor) and <0.05 for low-liquidity/high-odds like NBA playoff series (Asset-Class Rules); (3) score_threshold=None prohibited (Score Threshold Floor ≥2.2, no None values). Also conflicts with NBA Series rules requiring min_price_move ≥0.05 and spike_min_volume_delta ≥2x baseline.
- [ ] **TB-104** `rejected` — Increase min_price_move to 0.025 (2.5%) to filter sub-3% moves
  - **Governor rejection**: Proposed tweak violates multiple Global Floors: (1) min_volume_delta=None is prohibited (no None thresholds allowed, Volume-Delta Floor requires >100k for watch-tier); (2) min_price_move=0.025 < 0.03 (Price-Move Floor) and <0.05 for low-liquidity/high-odds like NBA playoff series (Asset-Class Rules); (3) score_threshold=None prohibited (Score Threshold Floor ≥2.2, no None values). Also conflicts with NBA Series rules requiring min_price_move ≥0.05 and spike_min_volume_delta ≥2x baseline.
- [ ] **TB-105** `rejected` — Add directional imbalance check: |yes% - no%| > 0.3 before signaling
  - **Governor rejection**: Proposed tweak violates multiple Global Floors: (1) min_volume_delta=None is prohibited (no None thresholds allowed, Volume-Delta Floor requires >100k for watch-tier); (2) min_price_move=0.025 < 0.03 (Price-Move Floor) and <0.05 for low-liquidity/high-odds like NBA playoff series (Asset-Class Rules); (3) score_threshold=None prohibited (Score Threshold Floor ≥2.2, no None values). Also conflicts with NBA Series rules requiring min_price_move ≥0.05 and spike_min_volume_delta ≥2x baseline.

---

## 2026-05-09 — Advisor snapshot 35

### Summary
False positives are occurring on low price moves (2%) with high volume deltas in high-liquidity markets like playoff series, lacking directional trade flow confirmation.

### Next step
Require volume delta ≥1.5x baseline AND net directional imbalance (yes/no side) before signaling.

### Suggested thresholds
`min_price_move` → `0.025`, `score_threshold` → `2.1`

### Recommendations

- [ ] **TB-106** `rejected` — Raise min_price_move to 0.025 to filter 2% moves
  - **Governor rejection**: Proposed tweak violates multiple historical constraints:
- Global Floors: `min_price_move = 0.025` (2.5%) weakens below tightened floor `≥ 0.05` (5%); `score_threshold = 2.1` weakens below `≥ 2.2`.
- Prohibited Relaxations: Explicitly bans `min_volume_delta = None`; prohibits weakening below global floors (e.g., price_move <0.05, score <2.2).
- NBA Series/Playoff Winner Markets: `min_price_move = 0.025` < required `≥ 0.05`; `min_volume_delta = None` ignores `≥ 2x baseline` and `>10 recent trades`.
- [ ] **TB-107** `rejected` — Increase min_volume_delta multiplier to 1.5x-2x baseline for high-liquidity markets
  - **Governor rejection**: Proposed tweak violates multiple historical constraints:
- Global Floors: `min_price_move = 0.025` (2.5%) weakens below tightened floor `≥ 0.05` (5%); `score_threshold = 2.1` weakens below `≥ 2.2`.
- Prohibited Relaxations: Explicitly bans `min_volume_delta = None`; prohibits weakening below global floors (e.g., price_move <0.05, score <2.2).
- NBA Series/Playoff Winner Markets: `min_price_move = 0.025` < required `≥ 0.05`; `min_volume_delta = None` ignores `≥ 2x baseline` and `>10 recent trades`.
- [ ] **TB-108** `rejected` — Add directional flow check: |yes - no| > 0.3 before flagging
  - **Governor rejection**: Proposed tweak violates multiple historical constraints:
- Global Floors: `min_price_move = 0.025` (2.5%) weakens below tightened floor `≥ 0.05` (5%); `score_threshold = 2.1` weakens below `≥ 2.2`.
- Prohibited Relaxations: Explicitly bans `min_volume_delta = None`; prohibits weakening below global floors (e.g., price_move <0.05, score <2.2).
- NBA Series/Playoff Winner Markets: `min_price_move = 0.025` < required `≥ 0.05`; `min_volume_delta = None` ignores `≥ 2x baseline` and `>10 recent trades`.

---

## 2026-05-09 — Advisor snapshot 36

### Summary
False positives are triggered by high volume deltas in playoff series winner markets despite minimal 2% price moves, lacking directional trade flow confirmation.

### Next step
Require net directional flow (yes/no imbalance > threshold) before flagging, especially for high-liquidity markets.

### Suggested thresholds
`min_price_move` → `0.025`

### Recommendations

- [ ] **TB-109** `rejected` — Raise volume delta multiplier to 1.5x baseline globally; 2x for playoff series.
  - **Governor rejection**: Violates multiple historical constraints: (1) Global Floors explicitly require spike_min_price_move ≥0.05 (5%) and no None thresholds for min_price_move or min_volume_delta; proposed 0.025 <0.05 and min_volume_delta=None weakens these. (2) NBA Series/Playoff Winner Markets (low-liq, high-odds) require min_price_move ≥0.05; proposed 0.025 weakens this floor. (3) Prohibited Relaxations ban weakening below specified floors (e.g., no price_move <0.05 for NBA/low-liq) and no None settings.
- [ ] **TB-110** `rejected` — Increase min_price_move to 0.025 (2.5%) to filter sub-3% moves.
  - **Governor rejection**: Violates multiple historical constraints: (1) Global Floors explicitly require spike_min_price_move ≥0.05 (5%) and no None thresholds for min_price_move or min_volume_delta; proposed 0.025 <0.05 and min_volume_delta=None weakens these. (2) NBA Series/Playoff Winner Markets (low-liq, high-odds) require min_price_move ≥0.05; proposed 0.025 weakens this floor. (3) Prohibited Relaxations ban weakening below specified floors (e.g., no price_move <0.05 for NBA/low-liq) and no None settings.
- [ ] **TB-111** `rejected` — Add directional imbalance check: |yes - no| / total > 0.2 for signal emission.
  - **Governor rejection**: Violates multiple historical constraints: (1) Global Floors explicitly require spike_min_price_move ≥0.05 (5%) and no None thresholds for min_price_move or min_volume_delta; proposed 0.025 <0.05 and min_volume_delta=None weakens these. (2) NBA Series/Playoff Winner Markets (low-liq, high-odds) require min_price_move ≥0.05; proposed 0.025 weakens this floor. (3) Prohibited Relaxations ban weakening below specified floors (e.g., no price_move <0.05 for NBA/low-liq) and no None settings.

---

## 2026-05-09 — Advisor snapshot 37

### Summary
Recent signals show false positives on low price moves (2%) with high volume deltas but unclear/low confidence, especially on flat volume days lacking directional flow.

### Next step
Require minimum price move of 0.025 (2.5%) to filter out borderline spikes.

### Suggested thresholds
`min_price_move` → `0.025`, `score_threshold` → `2.1`

### Recommendations

- [ ] **TB-112** `rejected` — Raise min_price_move from 0.02 to 0.025 or 0.03 to reduce noise on small moves.
  - **Governor rejection**: VIOLATION OF GLOBAL FLOOR: Proposed `min_price_move: 0.025` (2.5%) violates the explicit global floor `spike_min_price_move ≥ 0.05` (5%). This floor was tightened from prior 0.03/3%, indicating a deliberate hardening to reduce false positives—the exact problem the proposal claims to solve. Lowering to 0.025 reverses this tightening and contradicts the documented constraint. Additionally, `min_volume_delta: None` violates the prohibition on `None` thresholds; global floor requires all volume deltas to have explicit values. `score_threshold: 2.1` also violates the global floor `score_threshold ≥ 2.2`.
- [ ] **TB-113** `rejected` — Increase spike_score_threshold to 2.1 to suppress low-confidence signals like yes=0.26-0.27.
  - **Governor rejection**: VIOLATION OF GLOBAL FLOOR: Proposed `min_price_move: 0.025` (2.5%) violates the explicit global floor `spike_min_price_move ≥ 0.05` (5%). This floor was tightened from prior 0.03/3%, indicating a deliberate hardening to reduce false positives—the exact problem the proposal claims to solve. Lowering to 0.025 reverses this tightening and contradicts the documented constraint. Additionally, `min_volume_delta: None` violates the prohibition on `None` thresholds; global floor requires all volume deltas to have explicit values. `score_threshold: 2.1` also violates the global floor `score_threshold ≥ 2.2`.
- [ ] **TB-114** `rejected` — Add rule requiring net directional flow (yes-side volume > no-side by 1.5x) or volume delta >1.5x baseline.
  - **Governor rejection**: VIOLATION OF GLOBAL FLOOR: Proposed `min_price_move: 0.025` (2.5%) violates the explicit global floor `spike_min_price_move ≥ 0.05` (5%). This floor was tightened from prior 0.03/3%, indicating a deliberate hardening to reduce false positives—the exact problem the proposal claims to solve. Lowering to 0.025 reverses this tightening and contradicts the documented constraint. Additionally, `min_volume_delta: None` violates the prohibition on `None` thresholds; global floor requires all volume deltas to have explicit values. `score_threshold: 2.1` also violates the global floor `score_threshold ≥ 2.2`.

---

## 2026-05-09 — Advisor snapshot 38

### Summary
Recent signals show low price moves (2%) triggering detections with mixed analyst labels (one false positive, one true positive), indicating price threshold is too permissive for watch-tier assets despite high volume deltas.

### Next step
Raise spike_min_price_move to filter out sub-3% moves that generate unreliable signals.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `2.1`

### Recommendations

- [ ] **TB-115** `rejected` — Increase spike_min_price_move from 0.02 to 0.03 to reduce noise from minor fluctuations.
  - **Governor rejection**: Violates multiple historical constraints: (1) Global Floors require `spike_min_price_move ≥ 0.05` (tightened from 0.03), but proposed `min_price_move: 0.03` relaxes below this floor; (2) Global Floors require `score_threshold ≥ 2.2`, but proposed `score_threshold: 2.1` weakens below this; (3) Global Floors prohibit `None` thresholds for core params like `min_volume_delta`, but proposed `min_volume_delta: None` directly violates this.
- [ ] **TB-116** `rejected` — Raise spike_score_threshold to 2.1 to suppress borderline scores like 2.0 that are often false positives.
  - **Governor rejection**: Violates multiple historical constraints: (1) Global Floors require `spike_min_price_move ≥ 0.05` (tightened from 0.03), but proposed `min_price_move: 0.03` relaxes below this floor; (2) Global Floors require `score_threshold ≥ 2.2`, but proposed `score_threshold: 2.1` weakens below this; (3) Global Floors prohibit `None` thresholds for core params like `min_volume_delta`, but proposed `min_volume_delta: None` directly violates this.
- [ ] **TB-117** `rejected` — Add tier-specific price threshold (e.g. 0.025 for watch tier) if global change impacts higher tiers.
  - **Governor rejection**: Violates multiple historical constraints: (1) Global Floors require `spike_min_price_move ≥ 0.05` (tightened from 0.03), but proposed `min_price_move: 0.03` relaxes below this floor; (2) Global Floors require `score_threshold ≥ 2.2`, but proposed `score_threshold: 2.1` weakens below this; (3) Global Floors prohibit `None` thresholds for core params like `min_volume_delta`, but proposed `min_volume_delta: None` directly violates this.

---

## 2026-05-09 — Advisor snapshot 39

### Summary
False positives are triggered by high volume deltas in low-liquidity series markets with small price moves (~2%), likely quote-only fluctuations without sufficient trade activity.

### Next step
Require minimum trade count >10 AND increase volume delta multiplier to 1.5x baseline to filter low-liquidity noise.

### Suggested thresholds
`min_volume_delta` → `1500000.0`, `min_price_move` → `0.025`

### Recommendations

- [ ] **TB-118** `rejected` — Add new rule: minimum trade count >10 to exclude quote-only spikes
  - **Governor rejection**: VIOLATION OF MULTIPLE HISTORICAL CONSTRAINTS: (1) min_price_move: 0.025 (2.5%) violates Global Floors constraint of spike_min_price_move ≥0.05 (5%); (2) score_threshold: None violates Prohibited Relaxations rule explicitly stating 'no None settings'; (3) The proposal to relax price_move below 0.05 for low-liquidity series markets directly contradicts Watch-Tier and NBA Series/Playoff Winner Markets constraints which mandate min_price_move ≥0.05 as an explicit floor. These thresholds were tightened historically to prevent false positives in exactly these market conditions, so further relaxation reintroduces the noise problem rather than solving it.
- [ ] **TB-119** `rejected` — Raise min_volume_delta threshold to filter out sub-1.5M deltas in low-liquidity assets
  - **Governor rejection**: VIOLATION OF MULTIPLE HISTORICAL CONSTRAINTS: (1) min_price_move: 0.025 (2.5%) violates Global Floors constraint of spike_min_price_move ≥0.05 (5%); (2) score_threshold: None violates Prohibited Relaxations rule explicitly stating 'no None settings'; (3) The proposal to relax price_move below 0.05 for low-liquidity series markets directly contradicts Watch-Tier and NBA Series/Playoff Winner Markets constraints which mandate min_price_move ≥0.05 as an explicit floor. These thresholds were tightened historically to prevent false positives in exactly these market conditions, so further relaxation reintroduces the noise problem rather than solving it.
- [ ] **TB-120** `rejected` — Require priceΔ >= 0.025 (2.5%) for watch-tier signals
  - **Governor rejection**: VIOLATION OF MULTIPLE HISTORICAL CONSTRAINTS: (1) min_price_move: 0.025 (2.5%) violates Global Floors constraint of spike_min_price_move ≥0.05 (5%); (2) score_threshold: None violates Prohibited Relaxations rule explicitly stating 'no None settings'; (3) The proposal to relax price_move below 0.05 for low-liquidity series markets directly contradicts Watch-Tier and NBA Series/Playoff Winner Markets constraints which mandate min_price_move ≥0.05 as an explicit floor. These thresholds were tightened historically to prevent false positives in exactly these market conditions, so further relaxation reintroduces the noise problem rather than solving it.

---

## 2026-05-09 — Advisor snapshot 40

### Summary
False positives in NBA playoff series markets are triggered by mechanical liquidity spikes and quote-only fluctuations, labeled as noise despite meeting current volume and price thresholds.

### Next step
Introduce market-specific volume delta multipliers (1.5x-2.0x baseline) for low-liquidity series markets and add minimum trade count requirement (>5-10 recent trades).

### Suggested thresholds
`min_volume_delta` → `1500000.0`, `min_price_move` → `0.025`

### Recommendations

- [ ] **TB-121** `rejected` — Raise min_volume_delta multiplier to 1.5x baseline for tier:watch signals in series markets
  - **Governor rejection**: Proposed tweak violates multiple historical constraints: (1) Global Floors prohibit min_price_move <0.05 (proposed 0.025 weakens to 2.5%) and no None settings for score_threshold (proposed None); (2) NBA Series/Playoff Winner Markets explicitly require min_price_move ≥0.05 (proposed 0.025 relaxes below floor to fix noise); (3) Prohibited Relaxations ban weakening below specified floors like price_move <0.05 for NBA/low-liq markets.
- [ ] **TB-122** `rejected` — Require minimum 10 recent trades to filter quote-only fluctuations
  - **Governor rejection**: Proposed tweak violates multiple historical constraints: (1) Global Floors prohibit min_price_move <0.05 (proposed 0.025 weakens to 2.5%) and no None settings for score_threshold (proposed None); (2) NBA Series/Playoff Winner Markets explicitly require min_price_move ≥0.05 (proposed 0.025 relaxes below floor to fix noise); (3) Prohibited Relaxations ban weakening below specified floors like price_move <0.05 for NBA/low-liq markets.
- [ ] **TB-123** `rejected` — Increase min_price_move to 0.025 for playoff series to reduce medium-confidence noise
  - **Governor rejection**: Proposed tweak violates multiple historical constraints: (1) Global Floors prohibit min_price_move <0.05 (proposed 0.025 weakens to 2.5%) and no None settings for score_threshold (proposed None); (2) NBA Series/Playoff Winner Markets explicitly require min_price_move ≥0.05 (proposed 0.025 relaxes below floor to fix noise); (3) Prohibited Relaxations ban weakening below specified floors like price_move <0.05 for NBA/low-liq markets.

---

## 2026-05-09 — Advisor snapshot 41

### Summary
False positives in NBA playoff series markets are driven by mechanical liquidity spikes and quote-only fluctuations, labeled as noise despite meeting current thresholds, particularly in low-liquidity contexts.

### Next step
Introduce volume delta multiplier (relative to baseline) and minimum trade count requirements, especially for tier:watch in series markets.

### Suggested thresholds
`score_threshold` → `2.5`

### Recommendations

- [ ] **TB-124** `rejected` — Raise min_volume_delta_multiplier to 1.5x-2.0x baseline for playoff series markets
  - **Governor rejection**: The proposed tweak sets `min_volume_delta: None` and `min_price_move: None`, which directly violates the Global Floors 'Prohibited Relaxations' rule: 'No `min_price_move=None`, `min_volume_delta=None`, or `score_threshold=None` settings'. These are explicitly prohibited. Additionally, for NBA Series & Playoff Winner Markets (Low-Liquidity, High-Odds), it violates `min_price_move ≥ 0.05` floor and `spike_min_volume_delta ≥ 2x` baseline. For Watch-Tier markets, it violates `min_price_move ≥ 0.05`.
- [ ] **TB-125** `rejected` — Require minimum 5-10 recent trades for tier:watch signals
  - **Governor rejection**: The proposed tweak sets `min_volume_delta: None` and `min_price_move: None`, which directly violates the Global Floors 'Prohibited Relaxations' rule: 'No `min_price_move=None`, `min_volume_delta=None`, or `score_threshold=None` settings'. These are explicitly prohibited. Additionally, for NBA Series & Playoff Winner Markets (Low-Liquidity, High-Odds), it violates `min_price_move ≥ 0.05` floor and `spike_min_volume_delta ≥ 2x` baseline. For Watch-Tier markets, it violates `min_price_move ≥ 0.05`.
- [ ] **TB-126** `rejected` — Increase spike_score_threshold to 2.5 for low-liquidity series markets
  - **Governor rejection**: The proposed tweak sets `min_volume_delta: None` and `min_price_move: None`, which directly violates the Global Floors 'Prohibited Relaxations' rule: 'No `min_price_move=None`, `min_volume_delta=None`, or `score_threshold=None` settings'. These are explicitly prohibited. Additionally, for NBA Series & Playoff Winner Markets (Low-Liquidity, High-Odds), it violates `min_price_move ≥ 0.05` floor and `spike_min_volume_delta ≥ 2x` baseline. For Watch-Tier markets, it violates `min_price_move ≥ 0.05`.

---

## 2026-05-09 — Advisor snapshot 42

### Summary
Recent signals in low-liquidity NBA playoff series markets (especially DET) are triggering false positives due to mechanical liquidity spikes and quote-only fluctuations despite low price moves (~2%) and moderate scores.

### Next step
Raise volume delta multiplier to 1.5x baseline and add minimum trade count requirement (>10 for tier:watch) to filter mechanical spikes.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `2.5`

### Recommendations

- [x] **TB-127** `applied` — Require minimum 5 recent trades for tier:watch in playoff series markets.
- [x] **TB-128** `applied` — Increase min_volume_delta multiplier from 1.0x to 2.0x for low-liquidity markets.
- [x] **TB-129** `applied` — Raise spike_score_threshold to 2.5 for tier:watch signals with priceΔ < 0.03.

---

## 2026-05-09 — Advisor snapshot 43

### Summary
In playoff series markets, mechanical liquidity spikes trigger false positives with moderate volume deltas and price moves despite low yes probabilities, as labeled noise/medium.

### Next step
Raise volume delta multiplier to 2.0x baseline and require ≥5 recent trades for tier:watch in playoff series markets.

### Suggested thresholds
`min_volume_delta` → `1500000.0`, `score_threshold` → `2.5`

### Recommendations

- [ ] **TB-130** `rejected` — Implement market-type filter for playoff series: min_volume_delta multiplier=2.0x and min_recent_trades=5
  - **Governor rejection**: Violates Global Floors 'Prohibited Relaxations': No `min_price_move=None` settings allowed. The proposed tweak explicitly sets `min_price_move: None`, which is prohibited to ensure conviction via price-move floor ≥0.05.
- [ ] **TB-131** `rejected` — Increase spike_min_volume_delta globally to filter sub-2x baseline spikes
  - **Governor rejection**: Violates Global Floors 'Prohibited Relaxations': No `min_price_move=None` settings allowed. The proposed tweak explicitly sets `min_price_move: None`, which is prohibited to ensure conviction via price-move floor ≥0.05.
- [ ] **TB-132** `rejected` — Raise spike_score_threshold to 2.5 to exclude low-confidence signals like yes=0.21
  - **Governor rejection**: Violates Global Floors 'Prohibited Relaxations': No `min_price_move=None` settings allowed. The proposed tweak explicitly sets `min_price_move: None`, which is prohibited to ensure conviction via price-move floor ≥0.05.

---

## 2026-05-09 — Advisor snapshot 44

### Summary
Recent signals show false positives from mechanical liquidity spikes in playoff series markets, with low price moves (2-3%) and high volume deltas triggering despite analyst 'noise' labels, while true signals have borderline price deltas.

### Next step
Require minimum 5 recent trades for tier:watch in playoff series markets and raise volume delta multiplier to 2.0x baseline to filter mechanical spikes.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-133** `rejected` — Raise min_price_move to 0.03 to filter 2% moves
  - **Governor rejection**: Proposed tweak violates multiple historical constraints for NBA Series/Playoff Winner Markets (low-liq, high-odds): (1) sets `min_price_move: 0.03` below required floor `≥ 0.05`; (2) sets `min_volume_delta: None` prohibited by 'No None thresholds for min_price_move, min_volume_delta, score_threshold' and NBA-specific `spike_min_volume_delta ≥ 2x baseline`; (3) sets `score_threshold: None` prohibited by global floor `score_threshold ≥ 2.2` and 'No None thresholds'. Also conflicts with Low-Liquidity/High-Odds Markets requiring `min_price_move ≥ 0.05` and `>10 recent trades` (though 5 trades is a relaxation), and Global Floors `spike_min_price_move ≥ 0.05` and `spike_min_volume_delta > 100k`.
- [ ] **TB-134** `rejected` — Increase spike_min_volume_delta to require 2.0x baseline multiplier for sports markets
  - **Governor rejection**: Proposed tweak violates multiple historical constraints for NBA Series/Playoff Winner Markets (low-liq, high-odds): (1) sets `min_price_move: 0.03` below required floor `≥ 0.05`; (2) sets `min_volume_delta: None` prohibited by 'No None thresholds for min_price_move, min_volume_delta, score_threshold' and NBA-specific `spike_min_volume_delta ≥ 2x baseline`; (3) sets `score_threshold: None` prohibited by global floor `score_threshold ≥ 2.2` and 'No None thresholds'. Also conflicts with Low-Liquidity/High-Odds Markets requiring `min_price_move ≥ 0.05` and `>10 recent trades` (though 5 trades is a relaxation), and Global Floors `spike_min_price_move ≥ 0.05` and `spike_min_volume_delta > 100k`.
- [ ] **TB-135** `rejected` — Add rule: minimum 5 trades in last 60s for tier=watch signals
  - **Governor rejection**: Proposed tweak violates multiple historical constraints for NBA Series/Playoff Winner Markets (low-liq, high-odds): (1) sets `min_price_move: 0.03` below required floor `≥ 0.05`; (2) sets `min_volume_delta: None` prohibited by 'No None thresholds for min_price_move, min_volume_delta, score_threshold' and NBA-specific `spike_min_volume_delta ≥ 2x baseline`; (3) sets `score_threshold: None` prohibited by global floor `score_threshold ≥ 2.2` and 'No None thresholds'. Also conflicts with Low-Liquidity/High-Odds Markets requiring `min_price_move ≥ 0.05` and `>10 recent trades` (though 5 trades is a relaxation), and Global Floors `spike_min_price_move ≥ 0.05` and `spike_min_volume_delta > 100k`.

---

## 2026-05-09 — Advisor snapshot 45

### Summary
False positives in CLE market signals due to mechanical quote spikes with high volume delta but no sustained trades or real price movement, while DET signals are genuine.

### Next step
Require minimum volume delta to be 2.0x baseline AND at least 5 recent trades for tier:watch signals in playoff series markets.

### Suggested thresholds
`min_price_move` → `0.025`, `score_threshold` → `2.5`

### Recommendations

- [ ] **TB-136** `rejected` — Increase min_volume_delta multiplier to 2.0x baseline volume to filter mechanical liquidity spikes.
  - **Governor rejection**: Violates multiple historical constraints: 1) 'No None thresholds allowed for core parameters: min_volume_delta' - proposed min_volume_delta: None. 2) 'Global spike_min_price_move ≥ 0.05 (5%) with no None settings allowed' - proposed min_price_move: 0.025 < 0.05. 3) 'NBA series / playoff winner markets (low-liq, high-odds): min_price_move ≥ 0.05' - proposed 0.025 < 0.05. 4) 'No weakening of NBA/low-liq price_move below 0.05 or global price_move below 0.05' - weakens to 0.025. 5) 'Low-liquidity / high-odds markets (tier=watch/notable): ... >10 recent trades required' - proposed only 5 trades < 10. 6) 'Trade-count gates: minimum non-zero trades (>10 for low-liquidity series)' - proposed 5 < 10.
- [ ] **TB-137** `rejected` — Add rule requiring sustained price movement over 2-3 minute window post-spike.
  - **Governor rejection**: Violates multiple historical constraints: 1) 'No None thresholds allowed for core parameters: min_volume_delta' - proposed min_volume_delta: None. 2) 'Global spike_min_price_move ≥ 0.05 (5%) with no None settings allowed' - proposed min_price_move: 0.025 < 0.05. 3) 'NBA series / playoff winner markets (low-liq, high-odds): min_price_move ≥ 0.05' - proposed 0.025 < 0.05. 4) 'No weakening of NBA/low-liq price_move below 0.05 or global price_move below 0.05' - weakens to 0.025. 5) 'Low-liquidity / high-odds markets (tier=watch/notable): ... >10 recent trades required' - proposed only 5 trades < 10. 6) 'Trade-count gates: minimum non-zero trades (>10 for low-liquidity series)' - proposed 5 < 10.
- [ ] **TB-138** `rejected` — Raise spike_score_threshold to 2.5 for tier:watch to suppress borderline noise.
  - **Governor rejection**: Violates multiple historical constraints: 1) 'No None thresholds allowed for core parameters: min_volume_delta' - proposed min_volume_delta: None. 2) 'Global spike_min_price_move ≥ 0.05 (5%) with no None settings allowed' - proposed min_price_move: 0.025 < 0.05. 3) 'NBA series / playoff winner markets (low-liq, high-odds): min_price_move ≥ 0.05' - proposed 0.025 < 0.05. 4) 'No weakening of NBA/low-liq price_move below 0.05 or global price_move below 0.05' - weakens to 0.025. 5) 'Low-liquidity / high-odds markets (tier=watch/notable): ... >10 recent trades required' - proposed only 5 trades < 10. 6) 'Trade-count gates: minimum non-zero trades (>10 for low-liquidity series)' - proposed 5 < 10.

---

## 2026-05-09 — Advisor snapshot 46

### Summary
The detector is generating noise signals with low price moves (2-3%) despite moderate volume deltas, indicating that volume alone is insufficient to confirm real market movement. The first signal (CLE) explicitly flagged mechanical quote spikes without corresponding trades.

### Next step
Introduce a volume-to-price ratio validation: require that signals with price moves below 3% demonstrate either higher volume deltas or sustained multi-candle confirmation to filter out quote-only noise.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `2.2`

### Recommendations

- [ ] **TB-139** `rejected` — Raise spike_min_price_move from 3% to 4% for low-volatility periods, or implement a dynamic threshold that scales with recent ATR to adapt to market regime
  - **Governor rejection**: Proposed `min_price_move: 0.04` violates the Global Floor constraint `spike_min_price_move ≥ 0.05` (5%; tightened from 0.03). This floor was explicitly tightened to 0.05 to reduce noise from low-magnitude price moves. The proposal to relax it back to 0.04 directly contradicts this prior hardening decision. Additionally, setting `min_volume_delta: None` violates the explicit constraint 'No `None` thresholds for `min_price_move`, `min_volume_delta`, `score_threshold`'. If noise filtering is needed, the solution must maintain `min_price_move ≥ 0.05` and implement volume-to-price ratio validation as an *additional* gate (not a replacement that weakens the price floor).
- [ ] **TB-140** `rejected` — Add a volume-price ratio check: reject signals where (volΔ / baseline_volume) < threshold unless priceΔ > 4%, reducing mechanical quote spike false positives
  - **Governor rejection**: Proposed `min_price_move: 0.04` violates the Global Floor constraint `spike_min_price_move ≥ 0.05` (5%; tightened from 0.03). This floor was explicitly tightened to 0.05 to reduce noise from low-magnitude price moves. The proposal to relax it back to 0.04 directly contradicts this prior hardening decision. Additionally, setting `min_volume_delta: None` violates the explicit constraint 'No `None` thresholds for `min_price_move`, `min_volume_delta`, `score_threshold`'. If noise filtering is needed, the solution must maintain `min_price_move ≥ 0.05` and implement volume-to-price ratio validation as an *additional* gate (not a replacement that weakens the price floor).
- [ ] **TB-141** `rejected` — Require confirmation over multiple consecutive candles (e.g., 2+ candles with sustained price movement) before emitting a signal, especially for tier=watch signals with score < 2.5
  - **Governor rejection**: Proposed `min_price_move: 0.04` violates the Global Floor constraint `spike_min_price_move ≥ 0.05` (5%; tightened from 0.03). This floor was explicitly tightened to 0.05 to reduce noise from low-magnitude price moves. The proposal to relax it back to 0.04 directly contradicts this prior hardening decision. Additionally, setting `min_volume_delta: None` violates the explicit constraint 'No `None` thresholds for `min_price_move`, `min_volume_delta`, `score_threshold`'. If noise filtering is needed, the solution must maintain `min_price_move ≥ 0.05` and implement volume-to-price ratio validation as an *additional* gate (not a replacement that weakens the price floor).

---

## 2026-05-09 — Advisor snapshot 47

### Summary
The CLE signal shows a false positive with high volume delta but only 3% price move and low yes price (0.17), labeled as noise/unclear/low due to mechanical quote spikes without trades, while DET with lower volume but higher yes price (0.81) is a true signal.

### Next step
Require minimum yes price or odds ratio alongside volume/price deltas to filter mechanical spikes in low-liquidity markets.

### Suggested thresholds
`min_price_move` → `0.04`

### Recommendations

- [ ] **TB-142** `rejected` — Increase min_price_move to 0.04 to filter borderline price changes
  - **Governor rejection**: Violates multiple Global Floors and specific market constraints: (1) sets min_volume_delta: None (prohibited 'no None thresholds for min_volume_delta'); (2) sets min_price_move: 0.04 < 0.05 floor (prohibited 'spike_min_price_move ≥0.05 (5%)' and 'no weakening below specified floors e.g., price_move <0.05 for NBA/low-liq'); (3) sets score_threshold: None (prohibited 'no None thresholds for score_threshold' and implies <2.2 floor). Also weakens Low-Liquidity/High-Odds Markets and Notable-Tier requirements for min_price_move ≥0.05.
- [ ] **TB-143** `rejected` — Add min_yes_price threshold of 0.20 to avoid low-odds mechanical spikes
  - **Governor rejection**: Violates multiple Global Floors and specific market constraints: (1) sets min_volume_delta: None (prohibited 'no None thresholds for min_volume_delta'); (2) sets min_price_move: 0.04 < 0.05 floor (prohibited 'spike_min_price_move ≥0.05 (5%)' and 'no weakening below specified floors e.g., price_move <0.05 for NBA/low-liq'); (3) sets score_threshold: None (prohibited 'no None thresholds for score_threshold' and implies <2.2 floor). Also weakens Low-Liquidity/High-Odds Markets and Notable-Tier requirements for min_price_move ≥0.05.
- [ ] **TB-144** `rejected` — Require sustained price movement over 5-10 minute window instead of instant delta
  - **Governor rejection**: Violates multiple Global Floors and specific market constraints: (1) sets min_volume_delta: None (prohibited 'no None thresholds for min_volume_delta'); (2) sets min_price_move: 0.04 < 0.05 floor (prohibited 'spike_min_price_move ≥0.05 (5%)' and 'no weakening below specified floors e.g., price_move <0.05 for NBA/low-liq'); (3) sets score_threshold: None (prohibited 'no None thresholds for score_threshold' and implies <2.2 floor). Also weakens Low-Liquidity/High-Odds Markets and Notable-Tier requirements for min_price_move ≥0.05.

---

## 2026-05-09 — Advisor snapshot 48

### Summary
False positives in NBA series markets from mechanical liquidity events mimicking informed flow, despite meeting volume and price thresholds, while one similar signal was genuinely informative.

### Next step
Introduce market-type specific volume delta multipliers (e.g., 2.0x baseline for NBA series) to filter mechanical spikes.

### Suggested thresholds
`score_threshold` → `2.5`

### Recommendations

- [ ] **TB-145** `rejected` — Raise min_volume_delta multiplier to 2.0x baseline for NBA series markets.
  - **Governor rejection**: Proposed tweak sets `min_volume_delta: None` and `min_price_move: None`, directly violating Global Floors 'Prohibited Relaxations': No `min_volume_delta=None` or `min_price_move=None` settings allowed. These are non-negotiable floors explicitly prohibiting `None` values.
- [ ] **TB-146** `rejected` — Require sustained price movement over 2-3 bars post-spike for confirmation.
  - **Governor rejection**: Proposed tweak sets `min_volume_delta: None` and `min_price_move: None`, directly violating Global Floors 'Prohibited Relaxations': No `min_volume_delta=None` or `min_price_move=None` settings allowed. These are non-negotiable floors explicitly prohibiting `None` values.
- [ ] **TB-147** `rejected` — Increase score_threshold to 2.5 to filter low-confidence signals.
  - **Governor rejection**: Proposed tweak sets `min_volume_delta: None` and `min_price_move: None`, directly violating Global Floors 'Prohibited Relaxations': No `min_volume_delta=None` or `min_price_move=None` settings allowed. These are non-negotiable floors explicitly prohibiting `None` values.

---

## 2026-06-04 — Advisor snapshot 49

### Summary
The false-positive pattern is a large volume delta with only a small price move, especially when the flow appears quote-only rather than trade-confirmed. The analyst-labeled noise case suggests the detector is too sensitive on volume alone, while the labeled signal case shows very large volume can still be valid when it is clearly informative flow.

### Next step
Tighten the gate by requiring a larger price move or a stronger volume imbalance before emitting on high-volume, low-move events.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.04`, `score_threshold` → `3.0`

### Recommendations

- [x] **TB-148** `applied` — Raise spike_min_price_move from 0.03 to 0.04 to suppress low-move volume surges.
- [x] **TB-149** `applied` — Increase spike_min_volume_delta modestly only if the event also has a confirmed trade imbalance; otherwise keep the volume gate higher for quote-only changes.
- [x] **TB-150** `applied` — Lift spike_score_threshold so low-price-move events need more corroboration before signaling.

---

## 2026-06-04 — Advisor snapshot 50

### Summary
The false positives are concentrated in high-volume, low-price-move bursts where the analyst label says the flow is noise or quote-only rather than a true directional signal. The pattern suggests the detector is over-triggering on volume spikes without enough price confirmation or repeated same-side trade evidence.

### Next step
Tighten the rule to require both a larger price move and sustained trade imbalance for low-priced or zero-priced markets, instead of relying on volume alone.

### Suggested thresholds
`min_volume_delta` → `100000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-151** `rejected` — Raise spike_min_price_move from 0.02 to 0.03 for watch-tier emissions.
  - **Governor rejection**: Yes. The proposed `score_threshold: None` conflicts with the historical global floor requiring `score_threshold ≥ 2.2`; setting it to None removes the explicit threshold entirely, which is a relaxation below the hardened minimum. It also conflicts with the historical requirement that `min_price_move ≥ 0.05`; the proposed `min_price_move: 0.03` is below that floor. These violate the hardened global constraints and the price-move floor for spikes.
- [ ] **TB-152** `rejected` — Increase spike_min_volume_delta to at least 100000 for zero-priced or near-zero-priced markets.
  - **Governor rejection**: Yes. The proposed `score_threshold: None` conflicts with the historical global floor requiring `score_threshold ≥ 2.2`; setting it to None removes the explicit threshold entirely, which is a relaxation below the hardened minimum. It also conflicts with the historical requirement that `min_price_move ≥ 0.05`; the proposed `min_price_move: 0.03` is below that floor. These violate the hardened global constraints and the price-move floor for spikes.
- [ ] **TB-153** `rejected` — Add a gate that requires repeated same-side trades or trade-volume imbalance before emitting when price move is under 0.03.
  - **Governor rejection**: Yes. The proposed `score_threshold: None` conflicts with the historical global floor requiring `score_threshold ≥ 2.2`; setting it to None removes the explicit threshold entirely, which is a relaxation below the hardened minimum. It also conflicts with the historical requirement that `min_price_move ≥ 0.05`; the proposed `min_price_move: 0.03` is below that floor. These violate the hardened global constraints and the price-move floor for spikes.

---

## 2026-06-05 — Advisor snapshot 51

### Summary
Recent false positives are dominated by isolated volume bursts with little or no price movement, especially in low-liquidity or zero-priced markets. Analyst notes consistently favor requiring price confirmation or stronger trade imbalance before emitting a spike.

### Next step
Add a minimum price-move confirmation rule for all spike alerts, and raise the volume threshold specifically for low-liquidity and zero-priced markets.

### Suggested thresholds
`min_volume_delta` → `100000.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-154** `rejected` — Set a floor of min_price_move = 0.02 so flat-price volume bursts do not trigger alerts.
  - **Governor rejection**: The proposed tweak violates the historical hard floor TB-001 / global minimums by setting `min_price_move` to 0.02, which is below the required `min_price_move ≥ 0.05`. It also violates TB-001 by setting `score_threshold` to `None`, conflicting with the explicit hard floor `score_threshold ≥ 2.2` and the rule to keep score as a non-`None` gate. The proposal’s higher `min_volume_delta` does not resolve these conflicts.
- [ ] **TB-155** `rejected` — Increase min_volume_delta to about 100000 for zero-priced or quote-burst-prone markets.
  - **Governor rejection**: The proposed tweak violates the historical hard floor TB-001 / global minimums by setting `min_price_move` to 0.02, which is below the required `min_price_move ≥ 0.05`. It also violates TB-001 by setting `score_threshold` to `None`, conflicting with the explicit hard floor `score_threshold ≥ 2.2` and the rule to keep score as a non-`None` gate. The proposal’s higher `min_volume_delta` does not resolve these conflicts.
- [ ] **TB-156** `rejected` — Require either priceΔ >= 0.02 or a clear same-side volume imbalance before emitting a signal.
  - **Governor rejection**: The proposed tweak violates the historical hard floor TB-001 / global minimums by setting `min_price_move` to 0.02, which is below the required `min_price_move ≥ 0.05`. It also violates TB-001 by setting `score_threshold` to `None`, conflicting with the explicit hard floor `score_threshold ≥ 2.2` and the rule to keep score as a non-`None` gate. The proposal’s higher `min_volume_delta` does not resolve these conflicts.

---

## 2026-06-05 — Advisor snapshot 52

### Summary
The false positives are driven by isolated volume bursts with little or no price confirmation, especially in low-liquidity or quote-heavy markets. Analyst labels consistently favor requiring both a stronger price move and evidence of sustained trade imbalance before emitting a spike.

### Next step
Add a price-confirmation gate: require a minimum fractional price move before a spike can emit, and keep the volume trigger only as a secondary condition.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.03`, `score_threshold` → `3.0`

### Recommendations

- [ ] **TB-157** `rejected` — Raise spike_min_price_move from 0.02 to 0.03.
  - **Governor rejection**: TB-Price-move floor is violated because the proposed `min_price_move: 0.03` relaxes the explicitly tightened hard default of `spike_min_price_move ≥ 0.05` to fix noise. It also conflicts with the low-liquidity / series constraints that require `min_price_move ≥ 0.05` for NBA series/playoff winner, low-liquidity, watch-tier, and notable-tier signals.
- [ ] **TB-158** `rejected` — Raise spike_min_volume_delta from 36.0 to 100.0 for low-liquidity / nomination-style markets.
  - **Governor rejection**: TB-Price-move floor is violated because the proposed `min_price_move: 0.03` relaxes the explicitly tightened hard default of `spike_min_price_move ≥ 0.05` to fix noise. It also conflicts with the low-liquidity / series constraints that require `min_price_move ≥ 0.05` for NBA series/playoff winner, low-liquidity, watch-tier, and notable-tier signals.
- [ ] **TB-159** `rejected` — Increase spike_score_threshold from 2.0 to 3.0 to suppress quote-burst signals with weak follow-through.
  - **Governor rejection**: TB-Price-move floor is violated because the proposed `min_price_move: 0.03` relaxes the explicitly tightened hard default of `spike_min_price_move ≥ 0.05` to fix noise. It also conflicts with the low-liquidity / series constraints that require `min_price_move ≥ 0.05` for NBA series/playoff winner, low-liquidity, watch-tier, and notable-tier signals.

---

## 2026-06-05 — Advisor snapshot 53

### Summary
The false positives are driven by isolated volume bursts with little or no price confirmation, especially in low-liquidity or zero-priced markets. The analyst labels consistently point to requiring both stronger volume and a meaningful price move, or an additional persistence rule, before emitting a spike.

### Next step
Add a minimum price-move gate to volume-based detection and raise the volume threshold for low-liquidity or zero-priced markets so single-burst quote noise does not trigger signals.

### Suggested thresholds
`min_volume_delta` → `100.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-160** `rejected` — Set spike_min_price_move to 0.02 so flat or near-flat bursts do not emit signals.
  - **Governor rejection**: Yes. The proposed tweak violates the historical **global score_threshold floor** because it sets `score_threshold` to `None`, while the constraint explicitly requires `score_threshold >= 2.2` and never `None`. It also conflicts with the low-liquidity / high-odds and watch-tier constraints by lowering `min_price_move` to `0.02`, below the required `0.05` floor for those contexts, even though the stated problem is exactly isolated volume bursts in low-liquidity or zero-priced markets.
- [ ] **TB-161** `rejected` — Raise spike_min_volume_delta to 100 for low-liquidity or zero-priced markets.
  - **Governor rejection**: Yes. The proposed tweak violates the historical **global score_threshold floor** because it sets `score_threshold` to `None`, while the constraint explicitly requires `score_threshold >= 2.2` and never `None`. It also conflicts with the low-liquidity / high-odds and watch-tier constraints by lowering `min_price_move` to `0.02`, below the required `0.05` floor for those contexts, even though the stated problem is exactly isolated volume bursts in low-liquidity or zero-priced markets.
- [ ] **TB-162** `rejected` — Require either two same-side bursts or price confirmation before emitting when priceΔ is below threshold.
  - **Governor rejection**: Yes. The proposed tweak violates the historical **global score_threshold floor** because it sets `score_threshold` to `None`, while the constraint explicitly requires `score_threshold >= 2.2` and never `None`. It also conflicts with the low-liquidity / high-odds and watch-tier constraints by lowering `min_price_move` to `0.02`, below the required `0.05` floor for those contexts, even though the stated problem is exactly isolated volume bursts in low-liquidity or zero-priced markets.

---

## 2026-06-05 — Advisor snapshot 54

### Summary
The false positives are concentrated in low-liquidity or low-priced markets where volume can jump without any meaningful price confirmation. The analyst notes point to the same pattern: isolated volume surges are being over-triggered, especially when price move is flat or minimal.

### Next step
Raise the volume threshold and require a small price-confirmation floor, so a single trade or flat-price churn cannot emit a spike unless it has both stronger flow and at least modest directional movement.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.025`

### Recommendations

- [ ] **TB-163** `rejected` — Increase the minimum volume delta for low-liquidity markets to filter isolated trade bursts.
  - **Governor rejection**: TB-PriceFloor violation: the proposed `min_price_move: 0.025` relaxes the historically enforced global floor of `spike_min_price_move ≥ 0.05`, which was explicitly retained for low-liquidity/high-odds and NBA series/playoff winner markets. TB-ScoreNull violation: the proposal sets `score_threshold: None`, but history explicitly rejects null score thresholds and requires `score_threshold ≥ 2.2` as the global minimum. The higher `min_volume_delta: 500.0` does not resolve these conflicts.
- [ ] **TB-164** `rejected` — Set a price-move floor of about 2-3% before emitting a spike when volume is the main trigger.
  - **Governor rejection**: TB-PriceFloor violation: the proposed `min_price_move: 0.025` relaxes the historically enforced global floor of `spike_min_price_move ≥ 0.05`, which was explicitly retained for low-liquidity/high-odds and NBA series/playoff winner markets. TB-ScoreNull violation: the proposal sets `score_threshold: None`, but history explicitly rejects null score thresholds and requires `score_threshold ≥ 2.2` as the global minimum. The higher `min_volume_delta: 500.0` does not resolve these conflicts.
- [ ] **TB-165** `rejected` — Optionally add a sustained-flow condition so one-off prints do not pass even if the score is high.
  - **Governor rejection**: TB-PriceFloor violation: the proposed `min_price_move: 0.025` relaxes the historically enforced global floor of `spike_min_price_move ≥ 0.05`, which was explicitly retained for low-liquidity/high-odds and NBA series/playoff winner markets. TB-ScoreNull violation: the proposal sets `score_threshold: None`, but history explicitly rejects null score thresholds and requires `score_threshold ≥ 2.2` as the global minimum. The higher `min_volume_delta: 500.0` does not resolve these conflicts.

---

## 2026-06-05 — Advisor snapshot 55

### Summary
The false positives are concentrated in very high-volume, small-price-move situations: one labeled noise case had extreme volume delta but only a 2% move, while the labeled signal had both strong volume and a larger 6% move. This suggests the detector is overweighting volume when price confirmation is weak.

### Next step
Add a price-confirmation rule for high-volume alerts: require either a larger minimum price move or a sustained multi-minute move before emitting a signal.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-166** `rejected` — Raise spike_min_price_move from 0.02 to 0.03 for baseline filtering.
  - **Governor rejection**: The proposed tweak violates the historical global floors: `min_price_move` is set to 0.03, but the hardened policy requires `min_price_move`/`spike_min_price_move` to be explicit and at least 0.05, and older rules still require at least 0.03 only as an absolute noise floor. This also conflicts with the low-liquidity/watch-notable constraints that explicitly tightened `min_price_move` to ≥ 0.05 to suppress false positives in stable or mechanical pricing. In addition, `min_volume_delta` is set to None, which conflicts with the mandatory requirement that `min_volume_delta`/`spike_min_volume_delta` be explicit and never None.
- [ ] **TB-167** `rejected` — For markets with yes > 0.9, require priceΔ >= 0.03 or a multi-minute continuation before flagging.
  - **Governor rejection**: The proposed tweak violates the historical global floors: `min_price_move` is set to 0.03, but the hardened policy requires `min_price_move`/`spike_min_price_move` to be explicit and at least 0.05, and older rules still require at least 0.03 only as an absolute noise floor. This also conflicts with the low-liquidity/watch-notable constraints that explicitly tightened `min_price_move` to ≥ 0.05 to suppress false positives in stable or mechanical pricing. In addition, `min_volume_delta` is set to None, which conflicts with the mandatory requirement that `min_volume_delta`/`spike_min_volume_delta` be explicit and never None.
- [ ] **TB-168** `rejected` — Keep spike_min_volume_delta unchanged for now; tune price confirmation before tightening volume sensitivity.
  - **Governor rejection**: The proposed tweak violates the historical global floors: `min_price_move` is set to 0.03, but the hardened policy requires `min_price_move`/`spike_min_price_move` to be explicit and at least 0.05, and older rules still require at least 0.03 only as an absolute noise floor. This also conflicts with the low-liquidity/watch-notable constraints that explicitly tightened `min_price_move` to ≥ 0.05 to suppress false positives in stable or mechanical pricing. In addition, `min_volume_delta` is set to None, which conflicts with the mandatory requirement that `min_volume_delta`/`spike_min_volume_delta` be explicit and never None.

---

## 2026-06-05 — Advisor snapshot 56

### Summary
The false positives are coming from low-quality spike evidence: quote/price churn or single-step moves that lack enough confirmed execution, especially in low-trade-count and already-high-price markets. The one clearly valid signal is much stronger on both volume and price, so the detector should require more confirmation before emitting at the lower end.

### Next step
Raise the combined emission bar modestly and add a volume-or-price confirmation rule so a signal needs either materially larger volume delta or a larger price move, rather than accepting thin movement alone.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `3.25`

### Recommendations

- [ ] **TB-169** `rejected` — Increase the price-move floor to 0.04 to filter out 2%-3% chop while preserving the 6% high-confidence case.
  - **Governor rejection**: TB-001 is violated because the proposal relaxes the active hard floor for price move: historical constraints require spike_min_price_move ≥ 0.05 globally, including low-liquidity/watch/notable/high-odds markets, but the tweak sets min_price_move to 0.04. TB-003 is also violated because min_volume_delta / spike_min_volume_delta must be explicit and never None, but the proposed tweak sets min_volume_delta to None.
- [ ] **TB-170** `rejected` — Increase the score threshold to 3.25 so borderline watch-tier events with weak confirmation are suppressed.
  - **Governor rejection**: TB-001 is violated because the proposal relaxes the active hard floor for price move: historical constraints require spike_min_price_move ≥ 0.05 globally, including low-liquidity/watch/notable/high-odds markets, but the tweak sets min_price_move to 0.04. TB-003 is also violated because min_volume_delta / spike_min_volume_delta must be explicit and never None, but the proposed tweak sets min_volume_delta to None.
- [ ] **TB-171** `rejected` — Add a gating rule for low-trade-count or already-high-price markets: require either volΔ >= 100000 or priceΔ >= 0.04 before scoring can emit.
  - **Governor rejection**: TB-001 is violated because the proposal relaxes the active hard floor for price move: historical constraints require spike_min_price_move ≥ 0.05 globally, including low-liquidity/watch/notable/high-odds markets, but the tweak sets min_price_move to 0.04. TB-003 is also violated because min_volume_delta / spike_min_volume_delta must be explicit and never None, but the proposed tweak sets min_volume_delta to None.

---

## 2026-06-05 — Advisor snapshot 57

### Summary
The false positives cluster around **watch-tier alerts** where volume lifts are modest relative to baseline and the price move is only 2%–3%, especially in low-to-mid liquidity or low-trade-count markets. The stronger-notable example suggests the detector should require more confirmation before emitting on small moves, rather than broadly suppressing high-volume/high-move cases.

### Next step
Raise the watch-stage bar by requiring either a larger price move or a higher effective volume delta before emission, while keeping the notable tier unchanged so genuinely informative flow still passes.

### Suggested thresholds
`min_volume_delta` → `5500000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-172** `rejected` — Increase **min_price_move** from 0.03 to **0.04** for watch alerts to reduce 2%–3% noise.
  - **Governor rejection**: TB-052/TB-058/TB-100 require score_threshold to never be set to None, but the proposed tweak sets score_threshold: None. It also violates the global floor in TB-052/TB-058/TB-100 by lowering min_price_move to 0.04, below the hardened minimum of 0.05.
- [ ] **TB-173** `rejected` — Increase **min_volume_delta** from the current setting to a higher watch-only cutoff, roughly **1.5x–2x** above the present low-liquidity trigger equivalent.
  - **Governor rejection**: TB-052/TB-058/TB-100 require score_threshold to never be set to None, but the proposed tweak sets score_threshold: None. It also violates the global floor in TB-052/TB-058/TB-100 by lowering min_price_move to 0.04, below the hardened minimum of 0.05.
- [ ] **TB-174** `rejected` — Keep **score_threshold** unchanged for now; the false positives are better explained by weak confirmation than by overall score calibration.
  - **Governor rejection**: TB-052/TB-058/TB-100 require score_threshold to never be set to None, but the proposed tweak sets score_threshold: None. It also violates the global floor in TB-052/TB-058/TB-100 by lowering min_price_move to 0.04, below the hardened minimum of 0.05.

---

## 2026-06-05 — Advisor snapshot 58

### Summary
The false positives cluster around low-information moves: small price changes, quote-like churn, and high-base-price markets where modest volume deltas are getting flagged. The analyst labels consistently suggest tightening confirmation rather than broadly suppressing all spikes.

### Next step
Increase the price-move requirement modestly and add a higher bar for low-liquidity / already-high-price markets, while keeping the score gate unchanged unless you can retrain the combined score. Volume confirmation remains important, but price should do more of the filtering for noisy flow.

### Suggested thresholds
`min_price_move` → `0.04`

### Recommendations

- [ ] **TB-175** `rejected` — Raise the minimum price move from 0.03 to 0.04 to filter repeated quote changes and 2% moves that are being labeled noise.
  - **Governor rejection**: The proposal violates the active hard floors and no-null relaxations: it sets `min_volume_delta` to `None` and `score_threshold` to `None`, which conflicts with the historical constraints requiring `min_volume_delta` to be explicit (never `None`) and `score_threshold ≥ 2.2`. It also weakens `min_price_move` from the hardened floor of `0.05` to `0.04`, which conflicts with the global noise-suppression floor and the active hard floor `min_price_move ≥ 0.05`.
- [ ] **TB-176** `rejected` — Add a liquidity-aware rule: for low-to-mid liquidity political or rate markets, require either at least 2.5x baseline volume or a price move of 0.04+ before emitting a watch signal.
  - **Governor rejection**: The proposal violates the active hard floors and no-null relaxations: it sets `min_volume_delta` to `None` and `score_threshold` to `None`, which conflicts with the historical constraints requiring `min_volume_delta` to be explicit (never `None`) and `score_threshold ≥ 2.2`. It also weakens `min_price_move` from the hardened floor of `0.05` to `0.04`, which conflicts with the global noise-suppression floor and the active hard floor `min_price_move ≥ 0.05`.
- [ ] **TB-177** `rejected` — For markets already near the top of the range, require sustained multi-minute confirmation or a larger move threshold of 0.05+ before flagging.
  - **Governor rejection**: The proposal violates the active hard floors and no-null relaxations: it sets `min_volume_delta` to `None` and `score_threshold` to `None`, which conflicts with the historical constraints requiring `min_volume_delta` to be explicit (never `None`) and `score_threshold ≥ 2.2`. It also weakens `min_price_move` from the hardened floor of `0.05` to `0.04`, which conflicts with the global noise-suppression floor and the active hard floor `min_price_move ≥ 0.05`.

---

## 2026-06-05 — Advisor snapshot 59

### Summary
The false positives cluster around **low-to-mid liquidity** markets where small price moves or repeated quote changes are being overtreated as spikes. The pattern suggests the detector needs stricter confirmation from either *larger executed volume* or a *bigger price move* before emitting a watch alert.

### Next step
Raise the emission bar by requiring a stronger price move for low-liquidity/watch-tier events, while also tightening the volume floor so quote churn alone cannot trigger signals.

### Suggested thresholds
`min_volume_delta` → `5000000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-178** `rejected` — Increase the **minimum price move** from 0.03 to **0.04** for watch-tier alerts in low-liquidity markets.
  - **Governor rejection**: The tweak violates the global hard-floor rule that `score_threshold >= 2.2` because it sets `score_threshold` to `None`, which is explicitly disallowed (no relaxed `None` fallbacks). It also conflicts with the historical constraint that `min_price_move` must be at least `0.05`; the proposed `min_price_move: 0.04` is below that floor. This is a regression relative to the active floor set, even if the intent is to tighten watch-tier confirmation.
- [ ] **TB-179** `rejected` — Increase the **minimum volume delta** to a higher floor to avoid quote-change-driven triggers; a concrete starting point is **5,000,000** for the affected political nomination market class.
  - **Governor rejection**: The tweak violates the global hard-floor rule that `score_threshold >= 2.2` because it sets `score_threshold` to `None`, which is explicitly disallowed (no relaxed `None` fallbacks). It also conflicts with the historical constraint that `min_price_move` must be at least `0.05`; the proposed `min_price_move: 0.04` is below that floor. This is a regression relative to the active floor set, even if the intent is to tighten watch-tier confirmation.
- [ ] **TB-180** `rejected` — Add a rule that emits only when **either** volume delta is clearly above baseline **or** price move exceeds the higher threshold, instead of allowing marginal signals to pass on score alone.
  - **Governor rejection**: The tweak violates the global hard-floor rule that `score_threshold >= 2.2` because it sets `score_threshold` to `None`, which is explicitly disallowed (no relaxed `None` fallbacks). It also conflicts with the historical constraint that `min_price_move` must be at least `0.05`; the proposed `min_price_move: 0.04` is below that floor. This is a regression relative to the active floor set, even if the intent is to tighten watch-tier confirmation.

---

## 2026-06-05 — Advisor snapshot 60

### Summary
The false-positive pattern is a watch-tier alert firing on a large volume delta with only a small price move, especially in low-to-mid liquidity nomination markets. The analyst note explicitly indicates that a 1.7x volume multiple with about a 2% move is often noise, so the detector is currently too sensitive on volume-relative triggers.

### Next step
Raise the minimum price move for watch alerts and add a liquidity-aware volume-multiple gate so that volume surges without a stronger price response do not emit signals.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `3.7`

### Recommendations

- [ ] **TB-181** `rejected` — Increase spike_min_price_move from 0.03 to 0.04 for watch-tier alerts.
  - **Governor rejection**: The proposed tweak violates the historical hard-floor rule because it sets `min_price_move` to 0.04, which is below the explicitly required ≥ 0.05 floor, conflicting with the prior tightening for noise suppression and low-liquidity/watch-tier gating. It also violates the no-relaxation rule by setting `min_volume_delta` to None, which directly contradicts the requirement that `min_volume_delta` remain explicit and not None.
- [ ] **TB-182** `rejected` — Add a liquidity-aware rule: require a higher volume multiple in low-to-mid liquidity political nomination markets before emitting a watch signal.
  - **Governor rejection**: The proposed tweak violates the historical hard-floor rule because it sets `min_price_move` to 0.04, which is below the explicitly required ≥ 0.05 floor, conflicting with the prior tightening for noise suppression and low-liquidity/watch-tier gating. It also violates the no-relaxation rule by setting `min_volume_delta` to None, which directly contradicts the requirement that `min_volume_delta` remain explicit and not None.
- [ ] **TB-183** `rejected` — Slightly raise spike_score_threshold to reduce borderline emits that are driven by volume alone.
  - **Governor rejection**: The proposed tweak violates the historical hard-floor rule because it sets `min_price_move` to 0.04, which is below the explicitly required ≥ 0.05 floor, conflicting with the prior tightening for noise suppression and low-liquidity/watch-tier gating. It also violates the no-relaxation rule by setting `min_volume_delta` to None, which directly contradicts the requirement that `min_volume_delta` remain explicit and not None.

---

## 2026-06-05 — Advisor snapshot 61

### Summary
The false positives are concentrated in low-to-mid liquidity political nomination markets where a large volume jump with only a small price move still scores as notable. The analyst note indicates the current watch threshold is too permissive on volume-multiple alone, so the detector needs more price confirmation before emitting.

### Next step
Raise the price-move gate for watch-tier alerts and require a larger relative volume jump in low-liquidity markets, so volume spikes without meaningful follow-through do not trigger signals.

### Suggested thresholds
`min_price_move` → `0.04`

### Recommendations

- [ ] **TB-184** `rejected` — Increase spike_min_price_move from 0.03 to 0.04 for watch alerts in low-to-mid liquidity markets.
  - **Governor rejection**: The tweak conflicts with the historical constraints because it violates the active price-move floor and the active volume floor. Setting min_price_move to 0.04 relaxes the previously enforced global minimum of min_price_move ≥ 0.05, which is explicitly prohibited. Setting min_volume_delta to None violates the requirement that min_volume_delta / spike_min_volume_delta must be explicit and never None. If score_threshold is intended to replace the global anti-noise gate, leaving it as None also conflicts with the rule that score_threshold must remain ≥ 2.2 and not be unset.
- [ ] **TB-185** `rejected` — Add a liquidity-aware rule that lifts the effective volume threshold for watch-tier political nomination markets by about 25-35%.
  - **Governor rejection**: The tweak conflicts with the historical constraints because it violates the active price-move floor and the active volume floor. Setting min_price_move to 0.04 relaxes the previously enforced global minimum of min_price_move ≥ 0.05, which is explicitly prohibited. Setting min_volume_delta to None violates the requirement that min_volume_delta / spike_min_volume_delta must be explicit and never None. If score_threshold is intended to replace the global anti-noise gate, leaving it as None also conflicts with the rule that score_threshold must remain ≥ 2.2 and not be unset.
- [ ] **TB-186** `rejected` — Keep spike_score_threshold unchanged for now; the issue is better addressed by tightening the price/volume confirmation inputs rather than suppressing all scores.
  - **Governor rejection**: The tweak conflicts with the historical constraints because it violates the active price-move floor and the active volume floor. Setting min_price_move to 0.04 relaxes the previously enforced global minimum of min_price_move ≥ 0.05, which is explicitly prohibited. Setting min_volume_delta to None violates the requirement that min_volume_delta / spike_min_volume_delta must be explicit and never None. If score_threshold is intended to replace the global anti-noise gate, leaving it as None also conflicts with the rule that score_threshold must remain ≥ 2.2 and not be unset.

---

## 2026-06-05 — Advisor snapshot 62

### Summary
The current false positives are concentrated in low-to-mid liquidity political nomination markets where a very large volume delta with only ~2% price movement is still getting through as a watch-level signal. The analyst note indicates the main issue is insufficient volume-multiple gating on weak price confirmation, not the score formula alone.

### Next step
Raise the minimum price-move requirement for watch-tier alerts and add a volume-multiple floor for low-to-mid liquidity nomination markets so large but noisy flow with only shallow price response is filtered earlier.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-187** `rejected` — Increase spike_min_price_move from 0.02 to 0.03 for watch-tier emissions.
  - **Governor rejection**: TB-PRICE-001 is violated because the proposed tweak lowers `min_price_move` to 0.03, but the historical constraint requires `min_price_move ≥ 0.05` globally and explicitly rejects 0.03–0.04 relaxations. TB-NULL-001 is also violated because it sets `min_volume_delta` and `score_threshold` to `None`, which is explicitly disallowed by the no-null relaxations constraint.
- [ ] **TB-188** `rejected` — Add a market-segment rule that requires a higher volume-multiple threshold on low-to-mid liquidity political nomination markets before emitting watch alerts.
  - **Governor rejection**: TB-PRICE-001 is violated because the proposed tweak lowers `min_price_move` to 0.03, but the historical constraint requires `min_price_move ≥ 0.05` globally and explicitly rejects 0.03–0.04 relaxations. TB-NULL-001 is also violated because it sets `min_volume_delta` and `score_threshold` to `None`, which is explicitly disallowed by the no-null relaxations constraint.
- [ ] **TB-189** `rejected` — Keep spike_score_threshold unchanged for now; the recent false positives are better explained by weak price confirmation than by insufficient composite score.
  - **Governor rejection**: TB-PRICE-001 is violated because the proposed tweak lowers `min_price_move` to 0.03, but the historical constraint requires `min_price_move ≥ 0.05` globally and explicitly rejects 0.03–0.04 relaxations. TB-NULL-001 is also violated because it sets `min_volume_delta` and `score_threshold` to `None`, which is explicitly disallowed by the no-null relaxations constraint.

---

## 2026-06-05 — Advisor snapshot 63

### Summary
The recent false-positive pattern is that **watch-tier signals with very small price moves** are still firing, while the analyst-approved signals are already clearly informative on either volume or score. The detector should be made less sensitive to marginal price changes, especially when score is low.

### Next step
Raise the **minimum price move** slightly and require a stronger combined score before emission, while leaving volume sensitivity mostly intact.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `4.0`

### Recommendations

- [ ] **TB-190** `rejected` — Increase spike_min_price_move from 0.03 to 0.04 to suppress marginal 2%–3% moves like the 0.02 and 0.029 cases.
  - **Governor rejection**: TB-001 / Active price floor is violated: the proposed min_price_move of 0.04 relaxes the previously hardened global 0.05 floor, including for watch-tier markets. TB-008 / Active no-null policy is also violated because min_volume_delta is set to None. TB-007 is potentially weakened as well because raising score_threshold to 4.0 changes tuning, but the direct conflict is the price-floor relaxation and null volume gate.
- [ ] **TB-191** `rejected` — Raise spike_score_threshold to 4.0 so low-score watch signals are filtered unless they have exceptional volume confirmation.
  - **Governor rejection**: TB-001 / Active price floor is violated: the proposed min_price_move of 0.04 relaxes the previously hardened global 0.05 floor, including for watch-tier markets. TB-008 / Active no-null policy is also violated because min_volume_delta is set to None. TB-007 is potentially weakened as well because raising score_threshold to 4.0 changes tuning, but the direct conflict is the price-floor relaxation and null volume gate.
- [ ] **TB-192** `rejected` — Keep spike_min_volume_delta unchanged for now, since the strongest false-positive pattern is weak price movement rather than weak volume.
  - **Governor rejection**: TB-001 / Active price floor is violated: the proposed min_price_move of 0.04 relaxes the previously hardened global 0.05 floor, including for watch-tier markets. TB-008 / Active no-null policy is also violated because min_volume_delta is set to None. TB-007 is potentially weakened as well because raising score_threshold to 4.0 changes tuning, but the direct conflict is the price-floor relaxation and null volume gate.

---

## 2026-06-05 — Advisor snapshot 64

### Summary
The false-positive pattern is mostly low price movement: two analyst-confirmed signals had priceΔ at 1% and 2.9% while still scoring and emitting, which suggests the detector is over-sensitive on volume/score alone. One watch-tier case also shows huge volume delta with only 2% price move, so the current gate is likely letting through noisy flow that lacks sufficient price confirmation.

### Next step
Raise the minimum price-move gate first, and keep volume as a secondary confirmer rather than the primary trigger.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `4.0`

### Recommendations

- [ ] **TB-193** `rejected` — Increase spike_min_price_move to exclude 1%–2% moves that still look like noise.
  - **Governor rejection**: TB-Global price floor is violated because the proposed `min_price_move: 0.03` relaxes the explicitly required global floor of `spike_min_price_move ≥ 0.05`. TB-Global active floors is also violated because `min_volume_delta: None` removes an explicit gate that must remain non-null. TB-Global score floor is violated because `score_threshold: 4.0` does not conflict with the minimum, but the proposal’s rationale indicates replacing stricter volume/price confirmation with weaker gating; the explicit conflict is the null volume gate and sub-0.05 price floor.
- [ ] **TB-194** `rejected` — Slightly raise spike_score_threshold so weak low-price-move cases need stronger combined evidence to emit.
  - **Governor rejection**: TB-Global price floor is violated because the proposed `min_price_move: 0.03` relaxes the explicitly required global floor of `spike_min_price_move ≥ 0.05`. TB-Global active floors is also violated because `min_volume_delta: None` removes an explicit gate that must remain non-null. TB-Global score floor is violated because `score_threshold: 4.0` does not conflict with the minimum, but the proposal’s rationale indicates replacing stricter volume/price confirmation with weaker gating; the explicit conflict is the null volume gate and sub-0.05 price floor.
- [ ] **TB-195** `rejected` — Do not raise spike_min_volume_delta aggressively; the large-volume watch case suggests volume can still be informative when price response is modest.
  - **Governor rejection**: TB-Global price floor is violated because the proposed `min_price_move: 0.03` relaxes the explicitly required global floor of `spike_min_price_move ≥ 0.05`. TB-Global active floors is also violated because `min_volume_delta: None` removes an explicit gate that must remain non-null. TB-Global score floor is violated because `score_threshold: 4.0` does not conflict with the minimum, but the proposal’s rationale indicates replacing stricter volume/price confirmation with weaker gating; the explicit conflict is the null volume gate and sub-0.05 price floor.

---

## 2026-06-05 — Advisor snapshot 65

### Summary
The current false-positive pattern is that a signal can fire on weak price movement when volume is present but price confirmation is minimal. The analyst-labeled positives suggest the detector is probably too permissive on price-move confirmation relative to volume.

### Next step
Raise the price-move gate first, because the clearest noisy case has strong volume but only a 1% move while confirmed signals cluster closer to ~2.9%-3.0% move.

### Suggested thresholds
`min_price_move` → `0.028`

### Recommendations

- [ ] **TB-196** `rejected` — Increase spike_min_price_move from 0.03 to 0.025 if you want to preserve more informative flow, or to 0.028 if you want a tighter false-positive filter.
  - **Governor rejection**: TB-global hard floors is violated because `min_price_move` is explicit but set to 0.028, which is below the required ≥ 0.05 floor. This also conflicts with the stricter 0.05 price-move noise filter for low-liquidity, high-odds, watch-tier, notable-tier, and NBA series/playoff winner markets, which explicitly requires maintaining ≥ 0.05 rather than relaxing it.
- [ ] **TB-197** `rejected` — Leave spike_min_volume_delta unchanged for now; the labeled positives include both modest and very large volume deltas, so volume alone is not the main separator.
  - **Governor rejection**: TB-global hard floors is violated because `min_price_move` is explicit but set to 0.028, which is below the required ≥ 0.05 floor. This also conflicts with the stricter 0.05 price-move noise filter for low-liquidity, high-odds, watch-tier, notable-tier, and NBA series/playoff winner markets, which explicitly requires maintaining ≥ 0.05 rather than relaxing it.
- [ ] **TB-198** `rejected` — Keep spike_score_threshold unchanged unless you want a second-pass filter; the score spread is too dominated by event size to justify a precise global cut from only these three cases.
  - **Governor rejection**: TB-global hard floors is violated because `min_price_move` is explicit but set to 0.028, which is below the required ≥ 0.05 floor. This also conflicts with the stricter 0.05 price-move noise filter for low-liquidity, high-odds, watch-tier, notable-tier, and NBA series/playoff winner markets, which explicitly requires maintaining ≥ 0.05 rather than relaxing it.

---

## 2026-06-05 — Advisor snapshot 66

### Summary
The current false-positive pattern is that weak price moves are still passing because very large volume deltas and/or a high combined score are dominating the trigger. The analyst-labeled signals suggest volume alone is not sufficient confirmation, especially when price move is only 1–2%.

### Next step
Raise the price-move floor and require a small joint confirmation rule so large-volume noise cannot trigger on its own.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-199** `rejected` — Increase spike_min_price_move to at least 0.03 so 1–2% moves do not emit signals by themselves.
  - **Governor rejection**: The proposed tweak violates the active floor on `min_price_move ≥ 0.05` by lowering it to `0.03`. That conflicts with the historical constraint that global spike detection, including watch/notable and NBA series/playoff winner markets, must not be relaxed to 0.04/0.03/0.02. It also sets `min_volume_delta` and `score_threshold` to `None`, which conflicts with the active requirements that both must remain explicit and that `score_threshold ≥ 2.2` must never be `None`.
- [ ] **TB-200** `rejected` — Keep spike_min_volume_delta near current levels unless you can pair it with price confirmation; do not use volume as the primary gate.
  - **Governor rejection**: The proposed tweak violates the active floor on `min_price_move ≥ 0.05` by lowering it to `0.03`. That conflicts with the historical constraint that global spike detection, including watch/notable and NBA series/playoff winner markets, must not be relaxed to 0.04/0.03/0.02. It also sets `min_volume_delta` and `score_threshold` to `None`, which conflicts with the active requirements that both must remain explicit and that `score_threshold ≥ 2.2` must never be `None`.
- [ ] **TB-201** `rejected` — Slightly raise spike_score_threshold to suppress borderline watch-tier cases, but only after the price floor is increased.
  - **Governor rejection**: The proposed tweak violates the active floor on `min_price_move ≥ 0.05` by lowering it to `0.03`. That conflicts with the historical constraint that global spike detection, including watch/notable and NBA series/playoff winner markets, must not be relaxed to 0.04/0.03/0.02. It also sets `min_volume_delta` and `score_threshold` to `None`, which conflicts with the active requirements that both must remain explicit and that `score_threshold ≥ 2.2` must never be `None`.

---

## 2026-06-05 — Advisor snapshot 67

### Summary
The false positives cluster around signals with strong quote or volume activity but only small price moves, especially when volume appears repeated or liquidity-driven rather than executed. The more reliable signal in the examples is a larger confirmed price move with meaningful volume confirmation.

### Next step
Tighten the detector to require either a larger price move or stronger trade-confirmation before emitting, because under-3% moves with heavy quote-driven volume are the main false-positive pattern.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `2.9`

### Recommendations

- [ ] **TB-202** `rejected` — Raise the minimum price move for low-conviction flow from 0.03 to 0.04.
  - **Governor rejection**: The proposed tweak violates the historical constraints by relaxing the explicit active price floor from min_price_move / spike_min_price_move ≥ 0.05 to 0.04. This conflicts with the tightened floor established to prevent noise (TB-PRICE-FLOOR). It also violates the active volume floor constraint by setting min_volume_delta / spike_min_volume_delta to None, which is disallowed because the volume gate must remain explicit and non-null (TB-VOLUME-FLOOR). The score_threshold of 2.9 is not a conflict because it remains above the required ≥ 2.2 floor (TB-SCORE-FLOOR).
- [ ] **TB-203** `rejected` — Add a trade-confirmation filter so volume delta only counts if it is executed volume, not repeated quote updates.
  - **Governor rejection**: The proposed tweak violates the historical constraints by relaxing the explicit active price floor from min_price_move / spike_min_price_move ≥ 0.05 to 0.04. This conflicts with the tightened floor established to prevent noise (TB-PRICE-FLOOR). It also violates the active volume floor constraint by setting min_volume_delta / spike_min_volume_delta to None, which is disallowed because the volume gate must remain explicit and non-null (TB-VOLUME-FLOOR). The score_threshold of 2.9 is not a conflict because it remains above the required ≥ 2.2 floor (TB-SCORE-FLOOR).
- [ ] **TB-204** `rejected` — Increase the score threshold modestly to suppress borderline watch-tier alerts.
  - **Governor rejection**: The proposed tweak violates the historical constraints by relaxing the explicit active price floor from min_price_move / spike_min_price_move ≥ 0.05 to 0.04. This conflicts with the tightened floor established to prevent noise (TB-PRICE-FLOOR). It also violates the active volume floor constraint by setting min_volume_delta / spike_min_volume_delta to None, which is disallowed because the volume gate must remain explicit and non-null (TB-VOLUME-FLOOR). The score_threshold of 2.9 is not a conflict because it remains above the required ≥ 2.2 floor (TB-SCORE-FLOOR).

---

## 2026-06-05 — Advisor snapshot 68

### Summary
The recent false positives share a pattern of quote-driven or low-confirmation spikes: strong volume or activity appears, but the price move is too small or not sustained enough to indicate fresh information. The analyst notes consistently recommend requiring more trade-confirmed flow and a larger post-spike price change before emitting a signal.

### Next step
Add a confirmation rule that requires both executed-volume expansion and a stronger price move, rather than triggering on quote-heavy activity alone.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-205** `rejected` — Raise the price-move floor for low-liquidity / quote-driven markets, especially when priceΔ is below 3%.
  - **Governor rejection**: The proposed tweak violates the historical no-relaxation constraints TB-001 and TB-009 by setting `min_price_move` to 0.03, which is explicitly below the required global floor of 0.05. It also violates TB-010/TB-011 because `min_volume_delta` and `score_threshold` are set to `None`, despite the no-null policy and the requirement to keep score_threshold ≥ 2.2. This is a regression toward weaker confirmation and quote-noise-sensitive triggering.
- [ ] **TB-206** `rejected` — Increase the volume-confirmation requirement so volume spikes must be trade-confirmed, not just repeated quote updates.
  - **Governor rejection**: The proposed tweak violates the historical no-relaxation constraints TB-001 and TB-009 by setting `min_price_move` to 0.03, which is explicitly below the required global floor of 0.05. It also violates TB-010/TB-011 because `min_volume_delta` and `score_threshold` are set to `None`, despite the no-null policy and the requirement to keep score_threshold ≥ 2.2. This is a regression toward weaker confirmation and quote-noise-sensitive triggering.
- [ ] **TB-207** `rejected` — If you keep the current price floor, lift the score threshold to suppress marginal signals with unclear analyst labels.
  - **Governor rejection**: The proposed tweak violates the historical no-relaxation constraints TB-001 and TB-009 by setting `min_price_move` to 0.03, which is explicitly below the required global floor of 0.05. It also violates TB-010/TB-011 because `min_volume_delta` and `score_threshold` are set to `None`, despite the no-null policy and the requirement to keep score_threshold ≥ 2.2. This is a regression toward weaker confirmation and quote-noise-sensitive triggering.

---

## 2026-06-05 — Advisor snapshot 69

### Summary
The false positives are concentrated in low-liquidity Fed policy markets where quote-driven movement is being mistaken for real flow. Analyst labels indicate that the detector should demand stronger trade confirmation and sustained price follow-through before emitting.

### Next step
Tighten the trigger to require both a larger executed-volume surge and a more sustained price move, rather than allowing quote-only spikes to pass on score alone.

### Suggested thresholds
`min_volume_delta` → `10000.0`, `min_price_move` → `0.09`, `score_threshold` → `6.5`

### Recommendations

- [x] **TB-208** `applied` — Raise the minimum trade-confirmation bar for macro/Fed markets so repeated quotes do not qualify without executed volume.
- [x] **TB-209** `applied` — Increase the required post-spike price move for low-liquidity contracts, especially when the move is not backed by traded volume.
- [x] **TB-210** `applied` — Add a persistence rule so priceΔ must hold for a short follow-through window before signal emission.

---

## 2026-06-05 — Advisor snapshot 70

### Summary
The false positives are concentrated in low-executed-volume, quote-driven moves where price appears to spike without enough real participation. The analyst note for the SCOTUS market supports tightening volume confirmation rather than broadly raising price sensitivity.

### Next step
Raise the volume confirmation bar for watch-tier signals and require a stronger executed-volume delta before emitting on quote-driven markets.

### Suggested thresholds
`min_volume_delta` → `100000.0`

### Recommendations

- [ ] **TB-211** `rejected` — Increase the minimum volume delta for watch signals, especially in quote-driven markets, to suppress 2.0x baseline moves with little executed volume.
  - **Governor rejection**: TB-001 / TB-002 / TB-009 violated: the proposed tweak sets min_price_move to None and score_threshold to None, which removes the hard price-move floor (min_price_move ≥ 0.05) and the global score gate (score_threshold ≥ 2.2), both of which were explicitly required and must not be relaxed.
- [ ] **TB-212** `rejected` — Keep the current price-move threshold roughly unchanged; the noisy case already met a 3% move, so price alone is not the main discriminator.
  - **Governor rejection**: TB-001 / TB-002 / TB-009 violated: the proposed tweak sets min_price_move to None and score_threshold to None, which removes the hard price-move floor (min_price_move ≥ 0.05) and the global score gate (score_threshold ≥ 2.2), both of which were explicitly required and must not be relaxed.
- [ ] **TB-213** `rejected` — Add a market-structure rule: if executed volume is thin relative to baseline, suppress or downgrade the signal even when price move and score clear threshold.
  - **Governor rejection**: TB-001 / TB-002 / TB-009 violated: the proposed tweak sets min_price_move to None and score_threshold to None, which removes the hard price-move floor (min_price_move ≥ 0.05) and the global score gate (score_threshold ≥ 2.2), both of which were explicitly required and must not be relaxed.

---

## 2026-06-05 — Advisor snapshot 71

### Summary
The main false-positive pattern is low-priced, thinly informative markets where small absolute volume and small quote changes can still trip the detector. The true positive example shows that genuinely informative flow can arrive with very large volume even when price move is modest.

### Next step
Raise the minimum relative-volume requirement for low-priced markets, and only tighten price-move filtering modestly so you reduce noise without suppressing high-volume informational flow.

### Suggested thresholds
`min_volume_delta` → `500.0`, `min_price_move` → `0.015`, `score_threshold` → `3.8`

### Recommendations

- [ ] **TB-214** `rejected` — Add a low-priced-market rule that requires a higher volume delta before emitting a spike.
  - **Governor rejection**: TB-XXX: Violates the hard floor that `min_price_move` must be ≥ 0.05. The proposed `min_price_move: 0.015` relaxes a previously tightened threshold and would re-admit low-price noise that the historical constraints explicitly suppress for low-liquidity/watch/notable markets. TB-XXX: Also conflicts with the low-liquidity / high-odds / watch / notable market rule requiring `min_price_move ≥ 0.05`.
- [ ] **TB-215** `rejected` — Increase the score threshold slightly so small noisy moves with weak volume do not pass.
  - **Governor rejection**: TB-XXX: Violates the hard floor that `min_price_move` must be ≥ 0.05. The proposed `min_price_move: 0.015` relaxes a previously tightened threshold and would re-admit low-price noise that the historical constraints explicitly suppress for low-liquidity/watch/notable markets. TB-XXX: Also conflicts with the low-liquidity / high-odds / watch / notable market rule requiring `min_price_move ≥ 0.05`.
- [ ] **TB-216** `rejected` — Keep the price-move floor close to current levels, since the confirmed signal had only a 1% move but very large volume.
  - **Governor rejection**: TB-XXX: Violates the hard floor that `min_price_move` must be ≥ 0.05. The proposed `min_price_move: 0.015` relaxes a previously tightened threshold and would re-admit low-price noise that the historical constraints explicitly suppress for low-liquidity/watch/notable markets. TB-XXX: Also conflicts with the low-liquidity / high-odds / watch / notable market rule requiring `min_price_move ≥ 0.05`.

---

## 2026-06-05 — Advisor snapshot 72

### Summary
The false-positive pattern is a high-volume, low-price-move burst: one recent watch alert with 0.02 price change was labeled noise, while a similarly sized 0.02 move with very large volume was still a true signal. The main issue is that volume alone is not sufficient; flat-price quote-driven bursts need a stronger price-move or persistence filter.

### Next step
Raise the minimum price-move requirement for watch alerts and keep volume as a necessary but insufficient condition; if you want a single rule change, add a persistence/imbalance check for flat-price bursts.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-217** `rejected` — Increase spike_min_price_move from 0.02 to 0.03 to screen out flat-price noise.
  - **Governor rejection**: The proposed tweak violates the historical constraint that **min_price_move must be ≥ 0.05 globally**. Setting **min_price_move: 0.03** is a relaxation below the explicitly tightened floor, including for watch-tier markets. It also violates the constraint that **min_volume_delta must remain explicit and never be None**, because the proposal sets **min_volume_delta: None**. The proposal also violates the constraint that **score_threshold must remain explicit and never be None**, because it sets **score_threshold: None**. 
- [ ] **TB-218** `rejected` — Raise spike_min_volume_delta modestly only if the current alert stream is still too noisy, but do not rely on volume alone.
  - **Governor rejection**: The proposed tweak violates the historical constraint that **min_price_move must be ≥ 0.05 globally**. Setting **min_price_move: 0.03** is a relaxation below the explicitly tightened floor, including for watch-tier markets. It also violates the constraint that **min_volume_delta must remain explicit and never be None**, because the proposal sets **min_volume_delta: None**. The proposal also violates the constraint that **score_threshold must remain explicit and never be None**, because it sets **score_threshold: None**. 
- [ ] **TB-219** `rejected` — Keep spike_score_threshold unchanged for now; the evidence points more to improving the price-move gate than to a global score cut.
  - **Governor rejection**: The proposed tweak violates the historical constraint that **min_price_move must be ≥ 0.05 globally**. Setting **min_price_move: 0.03** is a relaxation below the explicitly tightened floor, including for watch-tier markets. It also violates the constraint that **min_volume_delta must remain explicit and never be None**, because the proposal sets **min_volume_delta: None**. The proposal also violates the constraint that **score_threshold must remain explicit and never be None**, because it sets **score_threshold: None**. 
- [ ] **TB-220** `rejected` — Add a sustained trade-imbalance or multi-bar confirmation rule for cases where price move is below 3% but volume is extreme.
  - **Governor rejection**: The proposed tweak violates the historical constraint that **min_price_move must be ≥ 0.05 globally**. Setting **min_price_move: 0.03** is a relaxation below the explicitly tightened floor, including for watch-tier markets. It also violates the constraint that **min_volume_delta must remain explicit and never be None**, because the proposal sets **min_volume_delta: None**. The proposal also violates the constraint that **score_threshold must remain explicit and never be None**, because it sets **score_threshold: None**. 

---

## 2026-06-05 — Advisor snapshot 73

### Summary
The false positives cluster around **quote-heavy or already-active markets** where the detector is reacting to modest price changes and volume that is not clearly executed-trade driven. Analyst labels consistently call for stronger confirmation from both **actual traded volume** and a **clearer directional move**.

### Next step
Tighten the detector to require a larger executed-volume delta plus a bigger price move before emitting watch signals, especially for political and rate markets where quote noise is common.

### Suggested thresholds
`min_volume_delta` → `500000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-221** `rejected` — Raise the **minimum volume delta** for watch signals to filter out quote-driven noise.
  - **Governor rejection**: TB-GLOBAL-01 is violated because the proposed tweak sets score_threshold to None, which explicitly conflicts with the hard floor requiring score_threshold ≥ 2.2 and never None. TB-GLOBAL-02 is also violated because the proposal lowers min_price_move to 0.03, below the required global minimum of 0.05. If this is intended for watch-tier or thin markets, it further conflicts with the historical requirement to harden price floors rather than relax them.
- [ ] **TB-222** `rejected` — Increase the **minimum price move** so a spike requires a clearer directional break, not just a small drift.
  - **Governor rejection**: TB-GLOBAL-01 is violated because the proposed tweak sets score_threshold to None, which explicitly conflicts with the hard floor requiring score_threshold ≥ 2.2 and never None. TB-GLOBAL-02 is also violated because the proposal lowers min_price_move to 0.03, below the required global minimum of 0.05. If this is intended for watch-tier or thin markets, it further conflicts with the historical requirement to harden price floors rather than relax them.
- [ ] **TB-223** `rejected` — Require **executed trades** to confirm the spike before emission, rather than allowing quote changes alone to trigger it.
  - **Governor rejection**: TB-GLOBAL-01 is violated because the proposed tweak sets score_threshold to None, which explicitly conflicts with the hard floor requiring score_threshold ≥ 2.2 and never None. TB-GLOBAL-02 is also violated because the proposal lowers min_price_move to 0.03, below the required global minimum of 0.05. If this is intended for watch-tier or thin markets, it further conflicts with the historical requirement to harden price floors rather than relax them.

---

## 2026-06-05 — Advisor snapshot 74

### Summary
The false positives cluster around thin or quote-heavy markets where a single volume print or small price move is being over-read as a spike. Analyst notes consistently ask for stronger confirmation from executed trades plus a larger directional move before emission.

### Next step
Tighten the rule to require both a higher traded-volume delta and a larger price move, with the clearest single change being a higher price-move floor for watch-tier signals.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-224** `rejected` — Raise minimum executed volume delta to filter out single-print noise in thin markets.
  - **Governor rejection**: TB-Global hard floors is violated because the proposed `min_price_move: 0.03` relaxes the historically hardened floor of `min_price_move >= 0.05` back into the explicitly discouraged 0.03–0.04 range. It also violates the score-handling constraint by setting `score_threshold: None`, conflicting with the rule to keep `score_threshold` active. The higher `min_volume_delta` does not offset these regressions because the historical constraints require both stronger volume confirmation and the active price/score gates to remain in place.
- [ ] **TB-225** `rejected` — Increase the minimum price move so small directional blips do not qualify as spikes.
  - **Governor rejection**: TB-Global hard floors is violated because the proposed `min_price_move: 0.03` relaxes the historically hardened floor of `min_price_move >= 0.05` back into the explicitly discouraged 0.03–0.04 range. It also violates the score-handling constraint by setting `score_threshold: None`, conflicting with the rule to keep `score_threshold` active. The higher `min_volume_delta` does not offset these regressions because the historical constraints require both stronger volume confirmation and the active price/score gates to remain in place.
- [ ] **TB-226** `rejected` — Keep the score threshold slightly higher only if the combined-score model still emits too many quote-driven signals.
  - **Governor rejection**: TB-Global hard floors is violated because the proposed `min_price_move: 0.03` relaxes the historically hardened floor of `min_price_move >= 0.05` back into the explicitly discouraged 0.03–0.04 range. It also violates the score-handling constraint by setting `score_threshold: None`, conflicting with the rule to keep `score_threshold` active. The higher `min_volume_delta` does not offset these regressions because the historical constraints require both stronger volume confirmation and the active price/score gates to remain in place.

---

## 2026-06-05 — Advisor snapshot 75

### Summary
The false positives are concentrated in markets where quote or baseline volume changes are being mistaken for real spikes, especially when price moves are only about 2%. Analyst labels repeatedly ask for stronger confirmation from executed trades and clearer directional continuation.

### Next step
Raise the detector’s evidence bar by requiring both a larger price move and a stronger executed-volume spike before emission, rather than relying on a single volume print or quote-heavy activity.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-227** `rejected` — Increase the minimum price move to at least 0.03 so 2% wiggles do not trigger watch signals.
  - **Governor rejection**: TB-001 is violated because the proposed min_price_move of 0.03 relaxes the globally required hard floor of min_price_move ≥ 0.05. TB-002 is also violated because min_volume_delta is set to None, removing the explicitly required volume gate. TB-003 is violated because score_threshold is set to None, below the globally required floor of score_threshold ≥ 2.2. The tweak therefore conflicts with multiple historical hard constraints.
- [ ] **TB-228** `rejected` — Increase the minimum volume delta modestly and tie it to executed trades, not quote updates, to cut thin-market noise.
  - **Governor rejection**: TB-001 is violated because the proposed min_price_move of 0.03 relaxes the globally required hard floor of min_price_move ≥ 0.05. TB-002 is also violated because min_volume_delta is set to None, removing the explicitly required volume gate. TB-003 is violated because score_threshold is set to None, below the globally required floor of score_threshold ≥ 2.2. The tweak therefore conflicts with multiple historical hard constraints.
- [ ] **TB-229** `rejected` — Keep the score threshold roughly where it is unless you still see quote-heavy false positives after tightening the two hard gates.
  - **Governor rejection**: TB-001 is violated because the proposed min_price_move of 0.03 relaxes the globally required hard floor of min_price_move ≥ 0.05. TB-002 is also violated because min_volume_delta is set to None, removing the explicitly required volume gate. TB-003 is violated because score_threshold is set to None, below the globally required floor of score_threshold ≥ 2.2. The tweak therefore conflicts with multiple historical hard constraints.

---

## 2026-06-05 — Advisor snapshot 76

### Summary
The false positives cluster around watch-tier signals that have only modest price movement but large or noisy volume deltas, especially in thin, quote-heavy, or already-active markets. Analyst labels consistently ask for more confirmation from actual traded volume, larger directional price moves, and sometimes sustained continuation rather than a single print.

### Next step
Tighten the detector by requiring both a larger price move and a higher confirmed traded-volume delta before emitting watch-tier spikes, and keep the score threshold as a secondary filter rather than the primary control.

### Suggested thresholds
`min_volume_delta` → `250000.0`, `min_price_move` → `0.04`, `score_threshold` → `3.25`

### Recommendations

- [ ] **TB-230** `rejected` — Raise the minimum price move from 3% to 4% so small 2% moves no longer qualify as spikes on their own.
  - **Governor rejection**: TB-global-floors is violated because the proposed `min_price_move: 0.04` weakens the explicit historical floor of `min_price_move ≥ 0.05` to 0.04. The rest of the tweak is not the conflict; the price threshold reduction directly relaxes a previously tightened constraint.
- [ ] **TB-231** `rejected` — Increase the minimum volume delta to around 250000 so low-quality volume bursts and quote-heavy noise are filtered out.
  - **Governor rejection**: TB-global-floors is violated because the proposed `min_price_move: 0.04` weakens the explicit historical floor of `min_price_move ≥ 0.05` to 0.04. The rest of the tweak is not the conflict; the price threshold reduction directly relaxes a previously tightened constraint.
- [ ] **TB-232** `rejected` — If you need an additional safeguard, raise the score threshold modestly to 3.25 rather than relying on score alone.
  - **Governor rejection**: TB-global-floors is violated because the proposed `min_price_move: 0.04` weakens the explicit historical floor of `min_price_move ≥ 0.05` to 0.04. The rest of the tweak is not the conflict; the price threshold reduction directly relaxes a previously tightened constraint.

---

## 2026-06-05 — Advisor snapshot 77

### Summary
The false positives are concentrated in cases where there is strong volume but the price move is too small or too ambiguous to be informative, especially in late-stage or low-liquidity markets. The pattern suggests the detector needs stricter confirmation from both relative price movement and sustained momentum rather than volume alone.

### Next step
Raise the price-move requirement and add a persistence check so high-volume but sub-meaningful moves do not emit signals.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-233** `rejected` — Increase the minimum fractional price move from 0.03 to 0.05 for late-stage, high-priced markets where sub-2% moves are commonly noise.
  - **Governor rejection**: The proposed tweak violates the historical no-null-gates constraint: TB-No-null-gates requires min_volume_delta and score_threshold to remain explicit, but the proposal sets both to None. It also conflicts with TB-Score-floor, which requires score_threshold ≥ 2.2 and forbids lowering it to a null/unspecified gate.
- [ ] **TB-234** `rejected` — Require a larger multi-tick or sustained move before emitting in low-liquidity rate-path markets, even when volume delta is large.
  - **Governor rejection**: The proposed tweak violates the historical no-null-gates constraint: TB-No-null-gates requires min_volume_delta and score_threshold to remain explicit, but the proposal sets both to None. It also conflicts with TB-Score-floor, which requires score_threshold ≥ 2.2 and forbids lowering it to a null/unspecified gate.
- [ ] **TB-235** `rejected` — Keep volume sensitivity high for genuinely informative flow, but only emit when volume and price move both clear thresholds rather than either one alone.
  - **Governor rejection**: The proposed tweak violates the historical no-null-gates constraint: TB-No-null-gates requires min_volume_delta and score_threshold to remain explicit, but the proposal sets both to None. It also conflicts with TB-Score-floor, which requires score_threshold ≥ 2.2 and forbids lowering it to a null/unspecified gate.

---

## 2026-06-05 — Advisor snapshot 78

### Summary
The false positives cluster around low-liquidity markets where large volume deltas produce signals despite only modest or ceiling-adjacent price moves. A second pattern is that spikes are being flagged before there is sustained confirmation in trade flow or quote behavior.

### Next step
Raise the minimum price-move requirement and add a confirmation rule requiring either a nonzero trade count or a sustained multi-tick quote change before emitting a spike.

### Suggested thresholds
`min_volume_delta` → `6500.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-236** `rejected` — Increase spike_min_price_move to filter sub-3% moves in high-priced or ceiling-adjacent markets.
  - **Governor rejection**: TB-001 / Global floors: the proposed tweak sets `score_threshold` to `None`, which violates the historical requirement that `score_threshold ≥ 2.2` must be explicit and non-`None`. It also conflicts with TB-001 / Global floors and the "Do not permit null relaxations" rule because `min_price_move` is reduced from the historically required floor of `≥ 0.05` to `0.03`, which relaxes a threshold previously tightened to suppress low-liquidity noise. The added confirmation rule is directionally consistent, but the threshold changes themselves are not compatible with the historical constraints.
- [ ] **TB-237** `rejected` — Require sustained quote movement or nonzero trade count confirmation for low-liquidity Fed/rate-path markets.
  - **Governor rejection**: TB-001 / Global floors: the proposed tweak sets `score_threshold` to `None`, which violates the historical requirement that `score_threshold ≥ 2.2` must be explicit and non-`None`. It also conflicts with TB-001 / Global floors and the "Do not permit null relaxations" rule because `min_price_move` is reduced from the historically required floor of `≥ 0.05` to `0.03`, which relaxes a threshold previously tightened to suppress low-liquidity noise. The added confirmation rule is directionally consistent, but the threshold changes themselves are not compatible with the historical constraints.
- [ ] **TB-238** `rejected` — Keep volume sensitivity, but lift spike_min_volume_delta modestly only for markets where price is already near the ceiling and trade counts are large but movement is muted.
  - **Governor rejection**: TB-001 / Global floors: the proposed tweak sets `score_threshold` to `None`, which violates the historical requirement that `score_threshold ≥ 2.2` must be explicit and non-`None`. It also conflicts with TB-001 / Global floors and the "Do not permit null relaxations" rule because `min_price_move` is reduced from the historically required floor of `≥ 0.05` to `0.03`, which relaxes a threshold previously tightened to suppress low-liquidity noise. The added confirmation rule is directionally consistent, but the threshold changes themselves are not compatible with the historical constraints.

---

## 2026-06-05 — Advisor snapshot 79

### Summary
The false positives are concentrated in low-liquidity or late-stage markets where large trade volume alone is triggering spikes despite only modest or sub-2% price movement. Analyst notes consistently ask for stronger confirmation from sustained price action or trade-side imbalance before emitting a signal.

### Next step
Tighten the detector so a spike requires both a higher minimum price move and evidence of sustained trade confirmation, rather than relying on volume alone.

### Suggested thresholds
`min_volume_delta` → `12000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-239** `rejected` — Raise min_price_move to filter out sub-3% quote-driven moves in low-liquidity markets.
  - **Governor rejection**: TB-001 is violated because the proposed `score_threshold: None` removes an explicit hard floor, but historical constraints require `score_threshold` to remain explicit and be ≥ 2.2. TB-002 is also violated because `min_price_move: 0.03` relaxes the previously enforced hard floor of ≥ 0.05 for low-liquidity/high-odds/notable-tier markets and NBA/playoff-related markets. The proposal is therefore a regression on both price-move and score gating.
- [ ] **TB-240** `rejected` — Increase min_volume_delta modestly so only materially larger trade bursts can pass the first gate.
  - **Governor rejection**: TB-001 is violated because the proposed `score_threshold: None` removes an explicit hard floor, but historical constraints require `score_threshold` to remain explicit and be ≥ 2.2. TB-002 is also violated because `min_price_move: 0.03` relaxes the previously enforced hard floor of ≥ 0.05 for low-liquidity/high-odds/notable-tier markets and NBA/playoff-related markets. The proposal is therefore a regression on both price-move and score gating.
- [ ] **TB-241** `rejected` — Add a confirmation rule requiring either nonzero trade count imbalance or a multi-tick sustained move before emitting a spike.
  - **Governor rejection**: TB-001 is violated because the proposed `score_threshold: None` removes an explicit hard floor, but historical constraints require `score_threshold` to remain explicit and be ≥ 2.2. TB-002 is also violated because `min_price_move: 0.03` relaxes the previously enforced hard floor of ≥ 0.05 for low-liquidity/high-odds/notable-tier markets and NBA/playoff-related markets. The proposal is therefore a regression on both price-move and score gating.

---

## 2026-06-05 — Advisor snapshot 80

### Summary
The dominant false-positive pattern is low-liquidity or high-baseline-volume markets where large volume deltas and quote-like price moves still produce analyst-labeled noise. The signals point to a need for stricter confirmation: larger trade-based volume changes, a higher minimum price move, and multi-trade/two-sided validation before emission.

### Next step
Add a confirmation rule requiring at least two executed trades on both sides or a verified trade-side imbalance before a spike can emit, and raise the minimum price-move floor modestly for low-liquidity markets.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-242** `rejected` — Increase spike_min_price_move from 0.03 to 0.05 for low-liquidity markets.
  - **Governor rejection**: TB-NULL-GATES violated: the proposed tweak sets `score_threshold` to `None`, but historical constraints require `score_threshold` to remain explicit and never null. It also omits an explicit `min_volume_delta` in favor of a large value without addressing the globally required explicit volume gate format, but the direct conflict is the null score threshold.
- [ ] **TB-243** `rejected` — Require spike_min_volume_delta to be at least 15000 for low-baseline markets before counting a spike.
  - **Governor rejection**: TB-NULL-GATES violated: the proposed tweak sets `score_threshold` to `None`, but historical constraints require `score_threshold` to remain explicit and never null. It also omits an explicit `min_volume_delta` in favor of a large value without addressing the globally required explicit volume gate format, but the direct conflict is the null score threshold.
- [ ] **TB-244** `rejected` — Keep score gating in place, but only allow scores to pass when the move is trade-confirmed rather than quote-confirmed.
  - **Governor rejection**: TB-NULL-GATES violated: the proposed tweak sets `score_threshold` to `None`, but historical constraints require `score_threshold` to remain explicit and never null. It also omits an explicit `min_volume_delta` in favor of a large value without addressing the globally required explicit volume gate format, but the direct conflict is the null score threshold.

---

## 2026-06-05 — Advisor snapshot 81

### Summary
The false positives cluster in thin, low-baseline markets where large volume deltas and quote-driven price jumps can trigger signals without enough trade confirmation. Analyst labels repeatedly recommend stricter trade-based confirmation and higher minimum movement thresholds for these markets.

### Next step
Tighten the detector for low-liquidity markets by requiring both a higher executed-volume delta and a larger trade-based price move, plus a nonzero multi-trade confirmation rule before emitting a spike.

### Suggested thresholds
`min_volume_delta` → `12000.0`, `min_price_move` → `0.3`

### Recommendations

- [ ] **TB-245** `rejected` — Raise the minimum volume delta to at least 12,000 in low-baseline markets.
  - **Governor rejection**: The proposal conflicts with the historical hard floor on `score_threshold`: TB-global hard floors requires `score_threshold` to be explicit and ≥ 2.2, but the proposed tweak sets `score_threshold: None`, which is a forbidden null relaxation. The other thresholds (`min_volume_delta: 12000.0`, `min_price_move: 0.3`) do not conflict with the stated floors.
- [ ] **TB-246** `rejected` — Raise the minimum price move to at least 0.30 (30%) for low-liquidity Fed meeting markets.
  - **Governor rejection**: The proposal conflicts with the historical hard floor on `score_threshold`: TB-global hard floors requires `score_threshold` to be explicit and ≥ 2.2, but the proposed tweak sets `score_threshold: None`, which is a forbidden null relaxation. The other thresholds (`min_volume_delta: 12000.0`, `min_price_move: 0.3`) do not conflict with the stated floors.
- [ ] **TB-247** `rejected` — Require at least 2 confirmed trades on both sides or a short-window trade print confirmation before flagging a spike.
  - **Governor rejection**: The proposal conflicts with the historical hard floor on `score_threshold`: TB-global hard floors requires `score_threshold` to be explicit and ≥ 2.2, but the proposed tweak sets `score_threshold: None`, which is a forbidden null relaxation. The other thresholds (`min_volume_delta: 12000.0`, `min_price_move: 0.3`) do not conflict with the stated floors.

---

## 2026-06-05 — Advisor snapshot 82

### Summary
The false positives are concentrated in thin or low-baseline markets where large volume deltas can come from single prints or quote-driven moves rather than sustained trade flow. The one clearly validated signal also had a much larger price move, suggesting the detector is over-sensitive to volume-only spikes at low price movement.

### Next step
Tighten detection by requiring both a higher executed-volume floor and a larger short-window price move before scoring can emit, with a multi-trade confirmation rule for low-baseline markets.

### Suggested thresholds
`min_volume_delta` → `12000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-248** `rejected` — Raise the minimum executed volume delta to filter out single-print bursts in thin markets.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets `score_threshold` to `None`, but the historical constraints explicitly require `score_threshold` to remain explicit and >= 2.2, with no null relaxations. TB-001 is also violated because `min_price_move: 0.03` lowers the explicit hard floor below the required >= 0.05.
- [ ] **TB-249** `rejected` — Increase the minimum price move so volume-only events with only ~2% movement do not trigger.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets `score_threshold` to `None`, but the historical constraints explicitly require `score_threshold` to remain explicit and >= 2.2, with no null relaxations. TB-001 is also violated because `min_price_move: 0.03` lowers the explicit hard floor below the required >= 0.05.
- [ ] **TB-250** `rejected` — Add a short-window multi-trade, two-sided confirmation requirement before emitting on very low baselines.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets `score_threshold` to `None`, but the historical constraints explicitly require `score_threshold` to remain explicit and >= 2.2, with no null relaxations. TB-001 is also violated because `min_price_move: 0.03` lowers the explicit hard floor below the required >= 0.05.

---

## 2026-06-05 — Advisor snapshot 83

### Summary
The false positives are concentrated in long-dated, high-volume-but-low-price-move signals where the move is likely quote churn rather than informative trading flow. The clearest corrective pattern is to require stronger price confirmation and/or an execution-based filter before emitting in that regime.

### Next step
Add a regime-specific filter for long-dated Fed markets: require both a higher minimum price move and a higher executed-trades-to-quote-updates ratio before allowing a spike signal.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-251** `rejected` — Increase min_price_move from 0.03 to 0.05 for long-dated Fed markets to suppress quote-churn spikes.
  - **Governor rejection**: TB-001 / active hard floor is violated because the proposed tweak sets `min_price_move` to 0.05 only for a long-dated Fed regime while leaving the global `min_price_move` floor unspecified at the regime level; the historical constraint requires `min_price_move ≥ 0.05` globally and explicitly forbids relaxing it to 0.03–0.04 or allowing `None`. TB-002 / global volume gate is also violated because `min_volume_delta` is set to `None`, but the constraint requires the volume gate to be explicit and not `None`. TB-003 / global score gate is violated because `score_threshold` is set to `None`, but the historical constraint requires `score_threshold ≥ 2.2` and explicitly forbids `None`.
- [ ] **TB-252** `rejected` — Keep high-volume cases from triggering alone by adding an execution-quality gate: require executed trades to materially exceed quote updates.
  - **Governor rejection**: TB-001 / active hard floor is violated because the proposed tweak sets `min_price_move` to 0.05 only for a long-dated Fed regime while leaving the global `min_price_move` floor unspecified at the regime level; the historical constraint requires `min_price_move ≥ 0.05` globally and explicitly forbids relaxing it to 0.03–0.04 or allowing `None`. TB-002 / global volume gate is also violated because `min_volume_delta` is set to `None`, but the constraint requires the volume gate to be explicit and not `None`. TB-003 / global score gate is violated because `score_threshold` is set to `None`, but the historical constraint requires `score_threshold ≥ 2.2` and explicitly forbids `None`.
- [ ] **TB-253** `rejected` — Do not lower the score threshold globally; the clean signal with volΔ=804182.64 and priceΔ=0.02 suggests volume alone can still be meaningful when analyst-confirmed, so use a regime filter instead of blunt global tightening.
  - **Governor rejection**: TB-001 / active hard floor is violated because the proposed tweak sets `min_price_move` to 0.05 only for a long-dated Fed regime while leaving the global `min_price_move` floor unspecified at the regime level; the historical constraint requires `min_price_move ≥ 0.05` globally and explicitly forbids relaxing it to 0.03–0.04 or allowing `None`. TB-002 / global volume gate is also violated because `min_volume_delta` is set to `None`, but the constraint requires the volume gate to be explicit and not `None`. TB-003 / global score gate is violated because `score_threshold` is set to `None`, but the historical constraint requires `score_threshold ≥ 2.2` and explicitly forbids `None`.

---

## 2026-06-05 — Advisor snapshot 84

### Summary
The false positives are concentrated in thin, low-liquidity markets where quote updates or small trade activity produce modest price moves that still trip the detector. Analyst labels consistently ask for stronger executed-volume confirmation and a higher bar for small, quote-only spikes.

### Next step
Raise the detector’s minimum executed-volume requirement and add a trade-led confirmation rule before increasing the score threshold further.

### Suggested thresholds
`min_volume_delta` → `3000.0`

### Recommendations

- [ ] **TB-254** `rejected` — Increase the volume gate for thin markets so quote-only moves with zero or near-zero executed volume do not trigger.
  - **Governor rejection**: TB-001 (Price floor) is violated because the proposed tweak sets `min_price_move` to `None`, which conflicts with the requirement that `min_price_move` / `spike_min_price_move` must be explicit and never `None`, with a hardened floor of ≥ 0.05. TB-003 (Score floor) is also violated because `score_threshold` is set to `None`, but it must be explicit and never `None`, with a global minimum of ≥ 2.2. The proposed increase to `min_volume_delta` does not itself conflict, but leaving the price and score thresholds unset would weaken previously hardened anti-noise constraints.
- [ ] **TB-255** `rejected` — Require a sustained trade-led move in addition to the raw price delta, especially for long-dated Fed and GDP contracts.
  - **Governor rejection**: TB-001 (Price floor) is violated because the proposed tweak sets `min_price_move` to `None`, which conflicts with the requirement that `min_price_move` / `spike_min_price_move` must be explicit and never `None`, with a hardened floor of ≥ 0.05. TB-003 (Score floor) is also violated because `score_threshold` is set to `None`, but it must be explicit and never `None`, with a global minimum of ≥ 2.2. The proposed increase to `min_volume_delta` does not itself conflict, but leaving the price and score thresholds unset would weaken previously hardened anti-noise constraints.
- [ ] **TB-256** `rejected` — Keep price sensitivity unchanged for now; the evidence points more strongly to liquidity/confirmation problems than to an overly low price-move threshold.
  - **Governor rejection**: TB-001 (Price floor) is violated because the proposed tweak sets `min_price_move` to `None`, which conflicts with the requirement that `min_price_move` / `spike_min_price_move` must be explicit and never `None`, with a hardened floor of ≥ 0.05. TB-003 (Score floor) is also violated because `score_threshold` is set to `None`, but it must be explicit and never `None`, with a global minimum of ≥ 2.2. The proposed increase to `min_volume_delta` does not itself conflict, but leaving the price and score thresholds unset would weaken previously hardened anti-noise constraints.

---

## 2026-06-05 — Advisor snapshot 85

### Summary
The false positives are coming from large or thin markets where small or quote-driven price moves are being flagged without enough executed volume confirmation. Analyst labels consistently point to the same fix: require a stronger volume burst and a more meaningful price move before emitting a watch signal.

### Next step
Raise the detector’s minimum executed-volume requirement and pair it with a stricter price-move floor so watch alerts only fire on trade-led spikes, not quote noise.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-257** `rejected` — Increase spike_min_volume_delta to filter out quote-only and low-conviction moves in thin markets.
  - **Governor rejection**: The proposal conflicts with the historical constraint that `score_threshold` must be explicit/non-`None` and at least 2.2. Setting `score_threshold: None` violates that active global floor. The `min_price_move: 0.05` value is consistent with the floor, and raising `min_volume_delta` is not itself a conflict, but the proposal cannot be accepted as written because it removes a required threshold.
- [ ] **TB-258** `rejected` — Increase spike_min_price_move modestly so sub-5% moves in long-dated or illiquid contracts do not trigger watch alerts.
  - **Governor rejection**: The proposal conflicts with the historical constraint that `score_threshold` must be explicit/non-`None` and at least 2.2. Setting `score_threshold: None` violates that active global floor. The `min_price_move: 0.05` value is consistent with the floor, and raising `min_volume_delta` is not itself a conflict, but the proposal cannot be accepted as written because it removes a required threshold.
- [ ] **TB-259** `rejected` — If you want a single additional guardrail, lift spike_score_threshold only slightly; the main fix should be the volume+price gate, not score suppression.
  - **Governor rejection**: The proposal conflicts with the historical constraint that `score_threshold` must be explicit/non-`None` and at least 2.2. Setting `score_threshold: None` violates that active global floor. The `min_price_move: 0.05` value is consistent with the floor, and raising `min_volume_delta` is not itself a conflict, but the proposal cannot be accepted as written because it removes a required threshold.

---

## 2026-06-05 — Advisor snapshot 86

### Summary
The false positives are coming from **quote-only or low-quality price moves** in thin markets, and from **very large but already-liquid markets** where volume surges without enough confirming price continuation. The analyst labels consistently favor stricter confirmation on both volume and sustained move before emitting watch alerts.

### Next step
Raise the detector’s confirmation bar for watch-tier signals by requiring a larger executed volume burst plus a stronger price move, rather than relying on either alone.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`, `score_threshold` → `4.0`

### Recommendations

- [x] **TB-260** `applied` — Increase the minimum price move to filter quote-only drift in thin markets.
- [x] **TB-261** `applied` — Increase the minimum volume delta so large-liquidity markets need a clearer burst before triggering.
- [x] **TB-262** `applied` — Raise the overall score threshold modestly to suppress marginal watch alerts that lack continuation.

---

## 2026-06-05 — Advisor snapshot 87

### Summary
The false positives are concentrated in already-high-probability political markets where modest price steps and large raw volume can still be quote updates or low-information churn. The analyst labels specifically call for stricter confirmation via higher volume relative to baseline and/or a larger or sustained price move.

### Next step
Raise the price-move floor and add a stricter execution-confirmation rule for political markets, rather than relying on raw volume alone.

### Suggested thresholds
`min_volume_delta` → `1500000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-263** `rejected` — Increase the minimum fractional price move to 0.04 so single-step moves around 2% stop triggering.
  - **Governor rejection**: TB-001 / Global hard floors is violated because the proposed `min_price_move: 0.04` is below the historical hard floor of `min_price_move ≥ 0.05`. TB-003 / Score gating is also violated because `score_threshold: None` removes the score gate, which the historical constraints explicitly prohibit.
- [ ] **TB-264** `rejected` — Require at least 2 executed trades for single-step price moves in high-probability political markets.
  - **Governor rejection**: TB-001 / Global hard floors is violated because the proposed `min_price_move: 0.04` is below the historical hard floor of `min_price_move ≥ 0.05`. TB-003 / Score gating is also violated because `score_threshold: None` removes the score gate, which the historical constraints explicitly prohibit.
- [ ] **TB-265** `rejected` — Raise the volume-delta floor to 1500000 for political-market signals unless the move is sustained across multiple updates.
  - **Governor rejection**: TB-001 / Global hard floors is violated because the proposed `min_price_move: 0.04` is below the historical hard floor of `min_price_move ≥ 0.05`. TB-003 / Score gating is also violated because `score_threshold: None` removes the score gate, which the historical constraints explicitly prohibit.

---

## 2026-06-05 — Advisor snapshot 88

### Summary
The false positives are concentrated in thinly traded or quote-driven markets where modest price moves and one-off orders can still trip the detector. The recent analyst labels favor adding stricter confirmation on both volume and trade count rather than lowering sensitivity across the board.

### Next step
Raise the volume requirement and add a minimum executed-trade-count confirmation for single-step price moves; this targets noisy quote updates without suppressing genuinely informative high-volume spikes.

### Suggested thresholds
`min_volume_delta` → `90000.0`, `min_price_move` → `0.055`, `score_threshold` → `4.5`

### Recommendations

- [x] **TB-266** `applied` — Increase spike_min_volume_delta to about 90000 for thinly traded phrase markets.
- [x] **TB-267** `applied` — Increase spike_min_price_move to about 0.055 so small move-and-volatility blips do not emit signals.
- [x] **TB-268** `applied` — Keep spike_score_threshold near current unless false positives persist after the volume/trade-count rule is added; then raise it modestly to 4.5.

---

## 2026-06-05 — Advisor snapshot 89

### Summary
The current false-positive pattern is concentrated in thinly traded phrase markets where sizable-looking moves can still be one-off order noise, even when score and price move are elevated. The analyst note explicitly recommends tightening both volume and price filters to reduce these noisy alerts.

### Next step
Raise both the minimum volume delta and minimum price move for thinly traded phrase markets, and keep the score threshold as a secondary gate rather than the primary filter.

### Suggested thresholds
`min_volume_delta` → `80000.0`, `min_price_move` → `0.06`

### Recommendations

- [ ] **TB-269** `rejected` — Increase the volume floor so isolated prints on thin markets do not trigger.
  - **Governor rejection**: The proposed tweak violates the global hard-floor constraint by setting `score_threshold` to `None`, which is explicitly disallowed; `score_threshold` must remain defined and at least 2.2. It also conflicts with the trade-confirmation gate and execution-quality preference because the proposal does not add any requirement for a minimum non-zero executed trade count or trade-backed confirmation, despite the historical rules requiring executed-trade confirmation with `>5` as a floor and `>10` preferred for low-liquidity series markets.
- [ ] **TB-270** `rejected` — Require a larger fractional price move before emitting a spike.
  - **Governor rejection**: The proposed tweak violates the global hard-floor constraint by setting `score_threshold` to `None`, which is explicitly disallowed; `score_threshold` must remain defined and at least 2.2. It also conflicts with the trade-confirmation gate and execution-quality preference because the proposal does not add any requirement for a minimum non-zero executed trade count or trade-backed confirmation, despite the historical rules requiring executed-trade confirmation with `>5` as a floor and `>10` preferred for low-liquidity series markets.
- [ ] **TB-271** `rejected` — Do not lower the score threshold yet; use stricter input thresholds first to preserve informative flow.
  - **Governor rejection**: The proposed tweak violates the global hard-floor constraint by setting `score_threshold` to `None`, which is explicitly disallowed; `score_threshold` must remain defined and at least 2.2. It also conflicts with the trade-confirmation gate and execution-quality preference because the proposal does not add any requirement for a minimum non-zero executed trade count or trade-backed confirmation, despite the historical rules requiring executed-trade confirmation with `>5` as a floor and `>10` preferred for low-liquidity series markets.

---

## 2026-06-05 — Advisor snapshot 90

### Summary
The false positives cluster around **headline-driven, low-priced political markets** where large volume bursts occur with only small price moves. Analyst labels consistently suggest that volume alone is too permissive and that confirmation should require stronger price follow-through or broader trade participation.

### Next step
Raise the **minimum price move** requirement slightly and add a stricter volume filter for low-liquidity political markets so that volume spikes must be paired with more sustained directional movement before emitting a signal.

### Suggested thresholds
`min_volume_delta` → `180000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-272** `rejected` — Increase **spike_min_price_move** from 0.02 to **0.03** for political succession/appointment markets.
  - **Governor rejection**: The proposal violates the historical hard floor on price confirmation: TB-PRICE-CONFIRMATION requires min_price_move ≥ 0.05, but the tweak sets min_price_move to 0.03, which is an explicit relaxation to a rejected weaker floor. It also conflicts with the no-relaxation rule for low-liquidity/high-odds/notable-tier markets, which rejects 0.03–0.04 thresholds and None-based substitutes. In addition, setting score_threshold to None violates TB-GLOBAL-HARD-FLOORS / TB-NO-RELAXATION-VIA-NULLS, which require score_threshold to be explicit and ≥ 2.2.
- [ ] **TB-273** `rejected` — Raise **spike_min_volume_delta** for low-liquidity political markets by about **20–30%** to suppress headline-only bursts.
  - **Governor rejection**: The proposal violates the historical hard floor on price confirmation: TB-PRICE-CONFIRMATION requires min_price_move ≥ 0.05, but the tweak sets min_price_move to 0.03, which is an explicit relaxation to a rejected weaker floor. It also conflicts with the no-relaxation rule for low-liquidity/high-odds/notable-tier markets, which rejects 0.03–0.04 thresholds and None-based substitutes. In addition, setting score_threshold to None violates TB-GLOBAL-HARD-FLOORS / TB-NO-RELAXATION-VIA-NULLS, which require score_threshold to be explicit and ≥ 2.2.
- [ ] **TB-274** `rejected` — Keep the score gate in place, but require either **priceΔ >= 0.03** or **multi-trade follow-through** before emitting when yes-probability is very low or very high.
  - **Governor rejection**: The proposal violates the historical hard floor on price confirmation: TB-PRICE-CONFIRMATION requires min_price_move ≥ 0.05, but the tweak sets min_price_move to 0.03, which is an explicit relaxation to a rejected weaker floor. It also conflicts with the no-relaxation rule for low-liquidity/high-odds/notable-tier markets, which rejects 0.03–0.04 thresholds and None-based substitutes. In addition, setting score_threshold to None violates TB-GLOBAL-HARD-FLOORS / TB-NO-RELAXATION-VIA-NULLS, which require score_threshold to be explicit and ≥ 2.2.

---

## 2026-06-05 — Advisor snapshot 91

### Summary
The recent false positives share a common pattern: large volume deltas paired with only ~2% price moves in political markets, which analysts labeled uncertain and recommended gating with stronger confirmation. The detector is likely over-sensitive to volume bursts in low-liquidity settings and needs a stricter price-move and follow-through requirement.

### Next step
Raise the price-move floor and make volume bursts in political markets require confirmation from sustained follow-through or multi-trade participation before emitting a signal.

### Suggested thresholds
`min_volume_delta` → `250000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-275** `rejected` — Increase the minimum price move to filter out 2% wiggles that are not yet informative.
  - **Governor rejection**: The proposed tweak conflicts with the historical hard floor on **score_threshold** because it sets score_threshold to **None**, which violates the global constraint that score_threshold must be **≥ 2.2** and must not be relaxed to null. It also conflicts with the low-liquidity / watch-tier history to the extent that it lowers **min_price_move** to **0.03**, below the required **min_price_move ≥ 0.05** floor for those markets.
- [ ] **TB-276** `rejected` — Raise the minimum volume delta for low-liquidity political succession/impeachment markets.
  - **Governor rejection**: The proposed tweak conflicts with the historical hard floor on **score_threshold** because it sets score_threshold to **None**, which violates the global constraint that score_threshold must be **≥ 2.2** and must not be relaxed to null. It also conflicts with the low-liquidity / watch-tier history to the extent that it lowers **min_price_move** to **0.03**, below the required **min_price_move ≥ 0.05** floor for those markets.
- [ ] **TB-277** `rejected` — Add a confirmation rule: require either a second trade-side confirmation or sustained follow-through over the next interval before firing.
  - **Governor rejection**: The proposed tweak conflicts with the historical hard floor on **score_threshold** because it sets score_threshold to **None**, which violates the global constraint that score_threshold must be **≥ 2.2** and must not be relaxed to null. It also conflicts with the low-liquidity / watch-tier history to the extent that it lowers **min_price_move** to **0.03**, below the required **min_price_move ≥ 0.05** floor for those markets.

---

## 2026-06-06 — Advisor snapshot 92

### Summary
The false positives cluster around **thin political markets** where modest volume bursts trigger alerts without meaningful price follow-through. The analyst labels suggest the detector is over-sensitive to volume alone and needs stronger confirmation from price move or directional imbalance.

### Next step
Raise the volume threshold and add a tighter price-move confirmation rule for low-priced political markets, so volume spikes only emit when paired with a clearly larger directional move.

### Suggested thresholds
`min_volume_delta` → `1200.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-278** `rejected` — Increase **spike_min_volume_delta** from the current setting to a higher floor for watch-tier alerts on thin markets.
  - **Governor rejection**: The proposed tweak violates the global floor on `score_threshold`, because it sets `score_threshold` to `None` even though the historical constraint requires `score_threshold ≥ 2.2` and non-`None`. It also conflicts with the historical price-move rule by setting `min_price_move` to `0.01`, which relaxes the active `0.05` minimum and is explicitly disallowed for low-liquidity/high-odds/watch-tier-style noise suppression.
- [ ] **TB-279** `rejected` — Increase **spike_min_price_move** so small moves like 0.1% to 1% do not qualify as spikes unless volume is extreme.
  - **Governor rejection**: The proposed tweak violates the global floor on `score_threshold`, because it sets `score_threshold` to `None` even though the historical constraint requires `score_threshold ≥ 2.2` and non-`None`. It also conflicts with the historical price-move rule by setting `min_price_move` to `0.01`, which relaxes the active `0.05` minimum and is explicitly disallowed for low-liquidity/high-odds/watch-tier-style noise suppression.
- [ ] **TB-280** `rejected` — Require a one-sided trade imbalance or sustained follow-through before emitting signals in political markets with low yes prices.
  - **Governor rejection**: The proposed tweak violates the global floor on `score_threshold`, because it sets `score_threshold` to `None` even though the historical constraint requires `score_threshold ≥ 2.2` and non-`None`. It also conflicts with the historical price-move rule by setting `min_price_move` to `0.01`, which relaxes the active `0.05` minimum and is explicitly disallowed for low-liquidity/high-odds/watch-tier-style noise suppression.

---

## 2026-06-06 — Advisor snapshot 93

### Summary
The false positives are concentrated in thin, low-priced political markets where large volume bursts occur with almost no price movement, so the detector is over-triggering on volume alone. The analyst labels point to needing stronger confirmation from price displacement or directional imbalance before emitting a watch signal.

### Next step
Raise the volume requirement for watch alerts and add a stricter price-move confirmation rule for low-priced political markets.

### Suggested thresholds
`min_volume_delta` → `150.0`, `min_price_move` → `0.01`

### Recommendations

- [ ] **TB-281** `rejected` — Increase spike_min_volume_delta to reduce alerts from modest bursts in thin books.
  - **Governor rejection**: The proposed tweak violates the historical floor in TB-001/TB-002 style constraints: global hard floors require min_price_move ≥ 0.05, but the tweak sets min_price_move to 0.01. It also conflicts with the price-move noise filter that explicitly maintains a 5% floor to suppress quote-only drift and sub-5% chop. In addition, setting score_threshold to None violates the global hard-floor constraint that score_threshold must be ≥ 2.2 with no None relaxations.
- [ ] **TB-282** `rejected` — Increase spike_min_price_move so volume spikes must coincide with a larger directional move.
  - **Governor rejection**: The proposed tweak violates the historical floor in TB-001/TB-002 style constraints: global hard floors require min_price_move ≥ 0.05, but the tweak sets min_price_move to 0.01. It also conflicts with the price-move noise filter that explicitly maintains a 5% floor to suppress quote-only drift and sub-5% chop. In addition, setting score_threshold to None violates the global hard-floor constraint that score_threshold must be ≥ 2.2 with no None relaxations.
- [ ] **TB-283** `rejected` — If possible, require a one-sided trade imbalance or equivalent directional confirmation before emitting watch-tier signals.
  - **Governor rejection**: The proposed tweak violates the historical floor in TB-001/TB-002 style constraints: global hard floors require min_price_move ≥ 0.05, but the tweak sets min_price_move to 0.01. It also conflicts with the price-move noise filter that explicitly maintains a 5% floor to suppress quote-only drift and sub-5% chop. In addition, setting score_threshold to None violates the global hard-floor constraint that score_threshold must be ≥ 2.2 with no None relaxations.

---

## 2026-06-06 — Advisor snapshot 94

### Summary
The false positives are coming from short-lived, quote-driven moves in low-liquidity markets where price change is only marginally above threshold, even when volume looks large. The labels point to a need for stricter price confirmation and a higher volume-multiple requirement before emitting a spike.

### Next step
Raise the price-move floor above 2% and add a liquidity-aware volume-multiple gate so single-interval quote spikes with little or no executed trade activity do not trigger.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `4.5`

### Recommendations

- [ ] **TB-284** `rejected` — Increase spike_min_price_move to 0.03 to suppress 2% noise in thin political markets.
  - **Governor rejection**: The proposal violates the historical hard floor on `min_price_move`: it lowers the threshold to `0.03`, but the constraint requires `min_price_move ≥ 0.05` to remain explicit. It also conflicts with the no-null rule by setting `min_volume_delta` to `None`, which is explicitly forbidden because volume confirmation must remain enabled and non-null.
- [ ] **TB-285** `rejected` — Require a higher volume multiple over baseline for low-liquidity markets, especially when trade count is near zero.
  - **Governor rejection**: The proposal violates the historical hard floor on `min_price_move`: it lowers the threshold to `0.03`, but the constraint requires `min_price_move ≥ 0.05` to remain explicit. It also conflicts with the no-null rule by setting `min_volume_delta` to `None`, which is explicitly forbidden because volume confirmation must remain enabled and non-null.
- [ ] **TB-286** `rejected` — De-emphasize quote-only bursts by lifting spike_score_threshold modestly so weakly confirmed spikes do not emit.
  - **Governor rejection**: The proposal violates the historical hard floor on `min_price_move`: it lowers the threshold to `0.03`, but the constraint requires `min_price_move ≥ 0.05` to remain explicit. It also conflicts with the no-null rule by setting `min_volume_delta` to `None`, which is explicitly forbidden because volume confirmation must remain enabled and non-null.

---

## 2026-06-06 — Advisor snapshot 95

### Summary
The false positives cluster around spikes that are either quote-driven or occur in thin, high-priced, or low-liquidity markets, where modest price moves and raw volume deltas are not reliable on their own. The strongest pattern is that volume confirmation and a higher price-move bar are needed to distinguish meaningful flow from noise.

### Next step
Raise the price-move floor and add a stronger volume-confirmation requirement, with extra filtering for quote-driven or ultra-high-priced markets.

### Suggested thresholds
`min_volume_delta` → `100000.0`, `min_price_move` → `0.04`, `score_threshold` → `3.0`

### Recommendations

- [ ] **TB-287** `rejected` — Increase spike_min_price_move from 0.02-0.03 to 0.04 for low-liquidity and high-price contracts.
  - **Governor rejection**: The proposed tweak conflicts with the historical hard floor for price move: **TB-001 / Global hard floors** requires `min_price_move` (or `spike_min_price_move`) to be explicit and **>= 0.05**, but the proposal sets `min_price_move: 0.04`, which is a relaxation below the previously enforced floor. The other suggested values do not obviously conflict with the stated constraints, but this price threshold does.
- [ ] **TB-288** `rejected` — Increase spike_min_volume_delta by roughly 20-30% and require executed trades, not just quote movement, for emission.
  - **Governor rejection**: The proposed tweak conflicts with the historical hard floor for price move: **TB-001 / Global hard floors** requires `min_price_move` (or `spike_min_price_move`) to be explicit and **>= 0.05**, but the proposal sets `min_price_move: 0.04`, which is a relaxation below the previously enforced floor. The other suggested values do not obviously conflict with the stated constraints, but this price threshold does.
- [ ] **TB-289** `rejected` — Raise spike_score_threshold modestly, but keep it below the point where genuine high-volume spikes are suppressed.
  - **Governor rejection**: The proposed tweak conflicts with the historical hard floor for price move: **TB-001 / Global hard floors** requires `min_price_move` (or `spike_min_price_move`) to be explicit and **>= 0.05**, but the proposal sets `min_price_move: 0.04`, which is a relaxation below the previously enforced floor. The other suggested values do not obviously conflict with the stated constraints, but this price threshold does.

---

## 2026-06-06 — Advisor snapshot 96

### Summary
The false positives are concentrated in **high-priced, thinly traded markets** where a price-only move or quote-driven blip is being treated as a real spike. The analyst notes point to needing stronger confirmation from executed volume and not just a short-lived price jump.

### Next step
Make spike emission require both a larger volume-delta floor and confirmed executed-trade activity, and slightly raise the score threshold so quote-driven or near-zero-trade moves do not pass.

### Suggested thresholds
`min_volume_delta` → `4000.0`, `score_threshold` → `4.5`

### Recommendations

- [ ] **TB-290** `rejected` — Raise **spike_min_volume_delta** to filter out small bursty moves in ultra-high-priced contracts.
  - **Governor rejection**: TB-Global-Price-Floor is violated because the proposal sets min_price_move to None, but the historical constraint requires an explicit min_price_move/spike_min_price_move of at least 0.05 and forbids None. This also conflicts with TB-Low-Liquidity-Default-Noise-Filter, which keeps min_price_move >= 0.05 as the default noise filter for thinly traded/high-odds markets.
- [ ] **TB-291** `rejected` — Add a rule that price spikes in markets with **yes >= 0.95** must be confirmed by executed trades, not just quotes.
  - **Governor rejection**: TB-Global-Price-Floor is violated because the proposal sets min_price_move to None, but the historical constraint requires an explicit min_price_move/spike_min_price_move of at least 0.05 and forbids None. This also conflicts with TB-Low-Liquidity-Default-Noise-Filter, which keeps min_price_move >= 0.05 as the default noise filter for thinly traded/high-odds markets.
- [ ] **TB-292** `rejected` — Increase **spike_score_threshold** modestly so single-interval, quote-driven jumps no longer emit signals.
  - **Governor rejection**: TB-Global-Price-Floor is violated because the proposal sets min_price_move to None, but the historical constraint requires an explicit min_price_move/spike_min_price_move of at least 0.05 and forbids None. This also conflicts with TB-Low-Liquidity-Default-Noise-Filter, which keeps min_price_move >= 0.05 as the default noise filter for thinly traded/high-odds markets.

---

## 2026-06-06 — Advisor snapshot 97

### Summary
The false positives cluster around spikes that are either quote-driven or concentrated in low-confirmation conditions: low trade count, near-zero executed-trade support, or price moves that are too small relative to the market’s regime. The analyst notes also suggest the detector is over-sensitive to price-only changes and needs stronger confirmation from volume and distinct prints, consistent with spike-detection guidance that emphasizes volume confirmation and normalization by volatility.

### Next step
Raise the score threshold modestly and add a confirmation rule requiring both a larger price move and multiple distinct executed yes-side prints before emission, especially in low-liquidity or near-peg markets.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `2.9`

### Recommendations

- [ ] **TB-293** `rejected` — Increase spike_min_price_move for low-liquidity or near-peg markets to suppress small quote-driven moves that are not backed by execution.
  - **Governor rejection**: TB-001 / Global floors is violated because the proposed tweak sets `min_price_move` to 0.04, which relaxes the historically hardened floor of `min_price_move ≥ 0.05`. It also violates TB-001 because `min_volume_delta` is `None`, while the historical constraint requires `min_volume_delta` to be explicit/non-None. The proposed change is therefore in conflict with previously applied noise-hardening rules.
- [ ] **TB-294** `rejected` — Require at least 2-3 distinct yes-side prints when trade count is low, so a single short-interval quote change cannot trigger a signal.
  - **Governor rejection**: TB-001 / Global floors is violated because the proposed tweak sets `min_price_move` to 0.04, which relaxes the historically hardened floor of `min_price_move ≥ 0.05`. It also violates TB-001 because `min_volume_delta` is `None`, while the historical constraint requires `min_volume_delta` to be explicit/non-None. The proposed change is therefore in conflict with previously applied noise-hardening rules.
- [ ] **TB-295** `rejected` — Keep spike_min_volume_delta as a confirmation gate, but make it harder to satisfy when absolute price is very low or very high, where tiny moves are often noise.
  - **Governor rejection**: TB-001 / Global floors is violated because the proposed tweak sets `min_price_move` to 0.04, which relaxes the historically hardened floor of `min_price_move ≥ 0.05`. It also violates TB-001 because `min_volume_delta` is `None`, while the historical constraint requires `min_volume_delta` to be explicit/non-None. The proposed change is therefore in conflict with previously applied noise-hardening rules.

---

## 2026-06-06 — Advisor snapshot 98

### Summary
The current false positives cluster around cases where a large volume delta or a small price move is enough to trigger, even when the market is low-liquidity or the contract is already near an extreme price. The labels suggest the detector needs stronger confirmation from price displacement and trade-print quality, not just raw volume or a single move.

### Next step
Tighten the trigger by requiring both a larger price move and a higher-quality volume confirmation, with an extra guardrail for ultra-high-priced contracts and low-trade-count markets.

### Suggested thresholds
`min_volume_delta` → `10000.0`, `min_price_move` → `0.04`, `score_threshold` → `2.8`

### Recommendations

- [ ] **TB-296** `rejected` — Increase the minimum price move to filter out 2%–3% wiggles that are often noise in extreme-priced contracts.
  - **Governor rejection**: TB-001 / Global hard floors are violated because the proposed `min_price_move` is 0.04, which is below the historical hard floor of `min_price_move >= 0.05`. The tweak is also a relaxation relative to the tightened global floor, even though `min_volume_delta` and `score_threshold` remain compliant.
- [ ] **TB-297** `rejected` — Raise the minimum volume delta so isolated bursts do not emit unless they are large enough to be structurally meaningful.
  - **Governor rejection**: TB-001 / Global hard floors are violated because the proposed `min_price_move` is 0.04, which is below the historical hard floor of `min_price_move >= 0.05`. The tweak is also a relaxation relative to the tightened global floor, even though `min_volume_delta` and `score_threshold` remain compliant.
- [ ] **TB-298** `rejected` — Add a confirmation rule: require multiple distinct yes-side prints or executed-trade confirmation before emitting on low-liquidity or near-100% markets.
  - **Governor rejection**: TB-001 / Global hard floors are violated because the proposed `min_price_move` is 0.04, which is below the historical hard floor of `min_price_move >= 0.05`. The tweak is also a relaxation relative to the tightened global floor, even though `min_volume_delta` and `score_threshold` remain compliant.

---

## 2026-06-06 — Advisor snapshot 99

### Summary
The false positives cluster around **high-volume but low-price-move** events, especially in low-liquidity or mechanically driven markets. Analyst notes also point to **quote-only moves** and the need for **confirmation beyond raw volume**.

### Next step
Tighten the detector to require a larger price move and stronger confirmation for low-liquidity bursts, so large notional volume alone does not emit a spike signal.

### Suggested thresholds
`min_volume_delta` → `150000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-299** `rejected` — Raise the minimum price move from 0.03 to **0.04** to suppress 1-3% mechanical noise while keeping materially larger moves.
  - **Governor rejection**: TB-global-hard-floors: proposed min_price_move of 0.04 violates the historical hard floor min_price_move ≥ 0.05, including the explicit market-specific rule for NBA series / playoff winner / low-liquidity high-odds / watch / notable markets to not relax into 0.03–0.04. TB-score-policy: score_threshold set to None violates the requirement to keep score_threshold active and the global floor score_threshold ≥ 2.2. TB-global-hard-floors: min_volume_delta is not a conflict if explicit at 150000.0, but the proposal still conflicts because it relaxes price and disables score gating.
- [ ] **TB-300** `rejected` — Increase the minimum volume delta to **150000** for low-liquidity or nomination-style markets where burst volume can be non-informational.
  - **Governor rejection**: TB-global-hard-floors: proposed min_price_move of 0.04 violates the historical hard floor min_price_move ≥ 0.05, including the explicit market-specific rule for NBA series / playoff winner / low-liquidity high-odds / watch / notable markets to not relax into 0.03–0.04. TB-score-policy: score_threshold set to None violates the requirement to keep score_threshold active and the global floor score_threshold ≥ 2.2. TB-global-hard-floors: min_volume_delta is not a conflict if explicit at 150000.0, but the proposal still conflicts because it relaxes price and disables score gating.
- [ ] **TB-301** `rejected` — Add a confirmation rule: require either **actual traded volume** or **multi-trade confirmation** before flagging quote-only moves.
  - **Governor rejection**: TB-global-hard-floors: proposed min_price_move of 0.04 violates the historical hard floor min_price_move ≥ 0.05, including the explicit market-specific rule for NBA series / playoff winner / low-liquidity high-odds / watch / notable markets to not relax into 0.03–0.04. TB-score-policy: score_threshold set to None violates the requirement to keep score_threshold active and the global floor score_threshold ≥ 2.2. TB-global-hard-floors: min_volume_delta is not a conflict if explicit at 150000.0, but the proposal still conflicts because it relaxes price and disables score gating.

---

## 2026-06-06 — Advisor snapshot 100

### Summary
The false positives are concentrated in thin or low-liquidity markets where very large volume bursts come with only tiny price changes, making the flow look dramatic but not informative. The analyst labels also suggest quote-only or mechanical activity is being overcounted without enough confirmation from actual traded movement.

### Next step
Raise the minimum price-move filter and add a higher volume floor for thin markets, while requiring repeated same-side trades before emitting a signal.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-302** `rejected` — Increase spike_min_price_move to 0.03 if it is below that, and consider 0.04 for long-dated or thin contract types.
  - **Governor rejection**: The proposed tweak violates the historical hard floors: `min_price_move` is lowered to 0.03, but the global hard floor requires `min_price_move` / `spike_min_price_move` to be explicit and ≥ 0.05, never `None`. It also conflicts with the low-liquidity / watch-tier rule that enforces `min_price_move ≥ 0.05` to suppress quote-only and stable-pricing noise. In addition, `min_volume_delta: None` and `score_threshold: None` violate the global requirements that `min_volume_delta` / `spike_min_volume_delta` must be explicit and that `score_threshold` must be explicit and ≥ 2.2, never `None`.
- [ ] **TB-303** `rejected` — Raise spike_min_volume_delta modestly for low-liquidity macro and political nomination markets to suppress huge-but-meaningless bursts.
  - **Governor rejection**: The proposed tweak violates the historical hard floors: `min_price_move` is lowered to 0.03, but the global hard floor requires `min_price_move` / `spike_min_price_move` to be explicit and ≥ 0.05, never `None`. It also conflicts with the low-liquidity / watch-tier rule that enforces `min_price_move ≥ 0.05` to suppress quote-only and stable-pricing noise. In addition, `min_volume_delta: None` and `score_threshold: None` violate the global requirements that `min_volume_delta` / `spike_min_volume_delta` must be explicit and that `score_threshold` must be explicit and ≥ 2.2, never `None`.
- [ ] **TB-304** `rejected` — Add a confirmation rule: require either multiple same-side trades or sustained price movement before triggering a signal.
  - **Governor rejection**: The proposed tweak violates the historical hard floors: `min_price_move` is lowered to 0.03, but the global hard floor requires `min_price_move` / `spike_min_price_move` to be explicit and ≥ 0.05, never `None`. It also conflicts with the low-liquidity / watch-tier rule that enforces `min_price_move ≥ 0.05` to suppress quote-only and stable-pricing noise. In addition, `min_volume_delta: None` and `score_threshold: None` violate the global requirements that `min_volume_delta` / `spike_min_volume_delta` must be explicit and that `score_threshold` must be explicit and ≥ 2.2, never `None`.

---

## 2026-06-06 — Advisor snapshot 101

### Summary
The false positives cluster around low-liquidity or thin markets where large volume deltas are paired with very small price moves, especially quote-only or mechanical bursts. Analyst labels repeatedly suggest these should require stronger price confirmation and/or executed-trade confirmation before emitting a signal.

### Next step
Tighten the detector with a higher minimum price-move requirement plus an execution-confirmation rule for low-liquidity markets, rather than relying on volume alone.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-305** `rejected` — Raise the minimum price move to filter 1% to 3% quote flickers in thin markets.
  - **Governor rejection**: The proposed tweak violates the historical global floors and no-null-gates constraints: `min_price_move` is reduced to 0.03, but the floor is `min_price_move ≥ 0.05`; `min_volume_delta` is set to `None`, but it must be explicit/non-`None`; and `score_threshold` is set to `None`, but it must remain ≥ 2.2 with no null relaxations. This is a direct regression against the previously applied tightening rules.
- [ ] **TB-306** `rejected` — Require confirmed executed volume or repeated same-side trades before flagging a spike in low-liquidity macro and nomination markets.
  - **Governor rejection**: The proposed tweak violates the historical global floors and no-null-gates constraints: `min_price_move` is reduced to 0.03, but the floor is `min_price_move ≥ 0.05`; `min_volume_delta` is set to `None`, but it must be explicit/non-`None`; and `score_threshold` is set to `None`, but it must remain ≥ 2.2 with no null relaxations. This is a direct regression against the previously applied tightening rules.
- [ ] **TB-307** `rejected` — Increase the score threshold modestly for markets where volume is high but price move is below the new minimum, so mechanical bursts do not emit signals.
  - **Governor rejection**: The proposed tweak violates the historical global floors and no-null-gates constraints: `min_price_move` is reduced to 0.03, but the floor is `min_price_move ≥ 0.05`; `min_volume_delta` is set to `None`, but it must be explicit/non-`None`; and `score_threshold` is set to `None`, but it must remain ≥ 2.2 with no null relaxations. This is a direct regression against the previously applied tightening rules.

---

## 2026-06-06 — Advisor snapshot 102

### Summary
Recent false positives cluster around **thin or low-liquidity markets** where large quoted or notional volume changes produce only **tiny price moves**, especially when there are sparse prints or no confirmed trades. Analyst notes repeatedly ask for **trade confirmation**, **multiple executed trades**, and a **larger price-move requirement** before emitting a spike.

### Next step
Raise the detection floor by requiring both a **larger minimum price move** and **confirmed executed volume** in addition to the score threshold; the strongest single change is to add a trade-confirmation rule for low-liquidity markets so quote refreshes and mechanical bursts do not trigger signals.

### Suggested thresholds
`min_volume_delta` → `100000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-308** `rejected` — Increase **spike_min_price_move** to at least **0.03** so 1%-2% quote moves in sparse markets stop firing.
  - **Governor rejection**: TB-global hard floors is violated because the proposed tweak sets `min_price_move: 0.03`, which relaxes the explicitly tightened floor and conflicts with the historical hard minimum `min_price_move ≥ 0.05` (and it is not one of the rejected relaxations only because it is still below the floor). It also violates the same TB-global hard floors by setting `score_threshold: None`, which is explicitly disallowed. In addition, for low-liquidity markets the historical TB-watch-tier / TB-notable-tier constraints require `min_price_move ≥ 0.05` plus trade-confirmation/volume gates, so the proposed `0.03` price floor undercuts those noise-fix constraints.
- [ ] **TB-309** `rejected` — Set **spike_min_volume_delta** higher for thin markets, around **100000** as a starting point, and require it to be backed by executed trades.
  - **Governor rejection**: TB-global hard floors is violated because the proposed tweak sets `min_price_move: 0.03`, which relaxes the explicitly tightened floor and conflicts with the historical hard minimum `min_price_move ≥ 0.05` (and it is not one of the rejected relaxations only because it is still below the floor). It also violates the same TB-global hard floors by setting `score_threshold: None`, which is explicitly disallowed. In addition, for low-liquidity markets the historical TB-watch-tier / TB-notable-tier constraints require `min_price_move ≥ 0.05` plus trade-confirmation/volume gates, so the proposed `0.03` price floor undercuts those noise-fix constraints.
- [ ] **TB-310** `rejected` — Keep **spike_score_threshold** unchanged for now; the main issue is not aggregate score but low-quality volume/price combinations that should be filtered earlier.
  - **Governor rejection**: TB-global hard floors is violated because the proposed tweak sets `min_price_move: 0.03`, which relaxes the explicitly tightened floor and conflicts with the historical hard minimum `min_price_move ≥ 0.05` (and it is not one of the rejected relaxations only because it is still below the floor). It also violates the same TB-global hard floors by setting `score_threshold: None`, which is explicitly disallowed. In addition, for low-liquidity markets the historical TB-watch-tier / TB-notable-tier constraints require `min_price_move ≥ 0.05` plus trade-confirmation/volume gates, so the proposed `0.03` price floor undercuts those noise-fix constraints.

---

## 2026-06-06 — Advisor snapshot 103

### Summary
The false positives are concentrated in low-liquidity, quote-driven markets where small price moves and sparse execution volume are being mistaken for informative spikes. Several analyst labels specifically call out quote refreshes and mechanical bursts as the cause, especially when price moves are only 1%–3%.

### Next step
Require both a larger minimum price move and executed-trade confirmation before emitting spikes in thin markets; this is the single best way to cut quote-only false positives without suppressing genuinely strong flow.

### Suggested thresholds
`min_volume_delta` → `30000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-311** `rejected` — Raise spike_min_price_move from 0.03 to 0.05 for low-liquidity macro/political markets.
  - **Governor rejection**: The proposed tweak conflicts with the historical score-floor constraint: score_threshold is set to None, but the global floor explicitly requires score_threshold ≥ 2.2 and not None. It also conflicts with the trade-confirmation gate only insofar as the proposal mentions executed-trade confirmation in prose but does not encode any explicit non-None trade/flow gate in the suggested thresholds; however, the direct rule violation is the removal of the score threshold.
- [ ] **TB-312** `rejected` — Increase the executed volume confirmation bar by requiring at least one real trade print or a higher min_volume_delta, especially when priceΔ is below 0.05.
  - **Governor rejection**: The proposed tweak conflicts with the historical score-floor constraint: score_threshold is set to None, but the global floor explicitly requires score_threshold ≥ 2.2 and not None. It also conflicts with the trade-confirmation gate only insofar as the proposal mentions executed-trade confirmation in prose but does not encode any explicit non-None trade/flow gate in the suggested thresholds; however, the direct rule violation is the removal of the score threshold.
- [ ] **TB-313** `rejected` — For thin, long-dated contracts, add a repeated-same-side-trades rule or raise spike_score_threshold modestly only for no-trade quote moves.
  - **Governor rejection**: The proposed tweak conflicts with the historical score-floor constraint: score_threshold is set to None, but the global floor explicitly requires score_threshold ≥ 2.2 and not None. It also conflicts with the trade-confirmation gate only insofar as the proposal mentions executed-trade confirmation in prose but does not encode any explicit non-None trade/flow gate in the suggested thresholds; however, the direct rule violation is the removal of the score threshold.

---

## 2026-06-06 — Advisor snapshot 104

### Summary
The false positives are coming from very large volume spikes paired with minimal price movement, especially in low-liquidity political markets. Analyst notes also suggest quote churn is being mistaken for actionable flow, so the detector needs stronger price-confirmation or follow-through gating.

### Next step
Keep the volume trigger high, but require a larger price move or a short sustained follow-through before emitting a signal.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-314** `rejected` — Raise spike_min_price_move from 0.03 to 0.05 to filter volume-only bursts with weak immediate price response.
  - **Governor rejection**: TB-001 / Global hard floors: `min_volume_delta` is set to `None`, which violates the explicit non-`None` requirement. TB-002 / No-null relaxations: `min_volume_delta` and `score_threshold` must never be `None`. TB-003 / Global hard floors: `score_threshold` is also set to `None`, violating the explicit ≥2.2 requirement. The proposed tweak therefore conflicts with historical constraints even though `min_price_move: 0.05` satisfies the floor.
- [ ] **TB-315** `rejected` — Add a follow-through rule: only emit if price holds the move for 2-3 minutes or makes a second higher high/higher low after the spike.
  - **Governor rejection**: TB-001 / Global hard floors: `min_volume_delta` is set to `None`, which violates the explicit non-`None` requirement. TB-002 / No-null relaxations: `min_volume_delta` and `score_threshold` must never be `None`. TB-003 / Global hard floors: `score_threshold` is also set to `None`, violating the explicit ≥2.2 requirement. The proposed tweak therefore conflicts with historical constraints even though `min_price_move: 0.05` satisfies the floor.
- [ ] **TB-316** `rejected` — For low-liquidity political markets, require either executed volume above the current floor or a stronger combined score before alerting on quote-only activity.
  - **Governor rejection**: TB-001 / Global hard floors: `min_volume_delta` is set to `None`, which violates the explicit non-`None` requirement. TB-002 / No-null relaxations: `min_volume_delta` and `score_threshold` must never be `None`. TB-003 / Global hard floors: `score_threshold` is also set to `None`, violating the explicit ≥2.2 requirement. The proposed tweak therefore conflicts with historical constraints even though `min_price_move: 0.05` satisfies the floor.

---

## 2026-06-06 — Advisor snapshot 105

### Summary
The false positives are concentrated in low-liquidity or quote-churn-heavy markets where very large volume deltas pair with only tiny price moves, producing noisy triggers that analysts labeled as noise/unclear. The one clean signal shows that genuine events can still be preserved when price move and execution are both meaningful.

### Next step
Raise the minimum price-move requirement and add a stricter low-liquidity execution filter so volume alone cannot trigger spikes in thin markets.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-317** `rejected` — Increase spike_min_price_move from 0.03 to 0.05.
  - **Governor rejection**: The proposed tweak violates the historical hard-floor policy by setting `min_volume_delta` to `None` and `score_threshold` to `None`, which conflicts with the explicit global constraints requiring `min_volume_delta` to be explicit/non-`None` and `score_threshold ≥ 2.2`. This also conflicts with the low-liquidity/thin-market guidance that volume alone must not trigger spikes and that stronger execution gating should be added rather than removed.
- [ ] **TB-318** `rejected` — Add a low-liquidity guardrail that requires either meaningful executed volume or multiple independent trades before emitting.
  - **Governor rejection**: The proposed tweak violates the historical hard-floor policy by setting `min_volume_delta` to `None` and `score_threshold` to `None`, which conflicts with the explicit global constraints requiring `min_volume_delta` to be explicit/non-`None` and `score_threshold ≥ 2.2`. This also conflicts with the low-liquidity/thin-market guidance that volume alone must not trigger spikes and that stronger execution gating should be added rather than removed.
- [ ] **TB-319** `rejected` — For quote-only spike patterns, raise spike_min_volume_delta selectively rather than globally so genuinely informative high-volume moves are not muted.
  - **Governor rejection**: The proposed tweak violates the historical hard-floor policy by setting `min_volume_delta` to `None` and `score_threshold` to `None`, which conflicts with the explicit global constraints requiring `min_volume_delta` to be explicit/non-`None` and `score_threshold ≥ 2.2`. This also conflicts with the low-liquidity/thin-market guidance that volume alone must not trigger spikes and that stronger execution gating should be added rather than removed.

---

## 2026-06-06 — Advisor snapshot 106

### Summary
The false positives are concentrated in low-liquidity, quote-driven spikes where price moves are small and analyst labels are noise or unclear. The only clearly informative signal is the CPI 0.2 contract, which pairs meaningful volume with a much larger price move.

### Next step
Raise the minimum price-move gate for low-liquidity quote-only events and require either executed trade flow or multi-minute follow-through before emitting a signal.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-320** `rejected` — Increase the quote-only price-move floor to 0.05 for low-liquidity markets.
  - **Governor rejection**: Conflict with the historical **global floors** and **score gating** constraints. The proposed tweak sets `min_volume_delta: None`, which violates the explicit non-`None` requirement for `min_volume_delta`, and sets `score_threshold: None`, which violates the requirement that `score_threshold ≥ 2.2` with no `None` relaxations. The proposal also weakens the historical gatekeeping by relying on follow-through instead of preserving an explicit minimum volume gate, which conflicts with the prior **volume-confirmation rule** that volume spikes must be trade-backed with explicit minimum volume gates.
- [ ] **TB-321** `rejected` — Add a trade-flow requirement: do not emit if volume delta is large but there is no evidence of real executed trades or follow-through.
  - **Governor rejection**: Conflict with the historical **global floors** and **score gating** constraints. The proposed tweak sets `min_volume_delta: None`, which violates the explicit non-`None` requirement for `min_volume_delta`, and sets `score_threshold: None`, which violates the requirement that `score_threshold ≥ 2.2` with no `None` relaxations. The proposal also weakens the historical gatekeeping by relying on follow-through instead of preserving an explicit minimum volume gate, which conflicts with the prior **volume-confirmation rule** that volume spikes must be trade-backed with explicit minimum volume gates.
- [ ] **TB-322** `rejected` — Keep the score threshold unchanged for now; the main issue is event quality, not aggregate scoring.
  - **Governor rejection**: Conflict with the historical **global floors** and **score gating** constraints. The proposed tweak sets `min_volume_delta: None`, which violates the explicit non-`None` requirement for `min_volume_delta`, and sets `score_threshold: None`, which violates the requirement that `score_threshold ≥ 2.2` with no `None` relaxations. The proposal also weakens the historical gatekeeping by relying on follow-through instead of preserving an explicit minimum volume gate, which conflicts with the prior **volume-confirmation rule** that volume spikes must be trade-backed with explicit minimum volume gates.

---

## 2026-06-06 — Advisor snapshot 107

### Summary
The false positives are concentrated in low-liquidity and quote-only markets where large apparent spikes are driven by brief price changes without enough executed trade confirmation. The analyst labels consistently ask for more sustained follow-through, stronger volume confirmation, or multiple prints before emitting a signal.

### Next step
Tighten the detector by requiring both a higher minimum volume delta and a stronger sustained price move before signaling, with an added rule that quote-only markets need multiple traded prints or multi-minute follow-through.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-323** `rejected` — Raise the minimum confirmation requirement for quote-only alerts: do not emit on a single price jump unless it persists across multiple timestamps or trades.
  - **Governor rejection**: TB-001 / TB-003 conflict: the proposed tweak sets `score_threshold` to `None`, but the historical constraints require `score_threshold` to be explicit, non-None, and >= 2.2. This removes the score floor entirely, which is a direct regression.
- [ ] **TB-324** `rejected` — Increase the volume filter for thin markets so brief liquidity sweeps do not qualify as spikes, especially when the price move is large but not sustained.
  - **Governor rejection**: TB-001 / TB-003 conflict: the proposed tweak sets `score_threshold` to `None`, but the historical constraints require `score_threshold` to be explicit, non-None, and >= 2.2. This removes the score floor entirely, which is a direct regression.
- [ ] **TB-325** `rejected` — Keep genuine signals like KXCPI-26JUL-T0.2 unmuted by favoring a combined rule: require either real executed volume or a materially larger price move than the current 3% floor.
  - **Governor rejection**: TB-001 / TB-003 conflict: the proposed tweak sets `score_threshold` to `None`, but the historical constraints require `score_threshold` to be explicit, non-None, and >= 2.2. This removes the score floor entirely, which is a direct regression.

---

## 2026-06-06 — Advisor snapshot 108

### Summary
The main false-positive pattern is quote-churn or low-liquidity movement being labeled as a spike, especially in CPI, Fed, and thin political markets. Analysts repeatedly ask for stronger execution confirmation, sustained follow-through, and higher minimum volume before emitting signals.

### Next step
Tighten the detector to require confirmed executed volume plus multi-timestamp follow-through for low-liquidity/quote-only markets, rather than relying on a single large quote move.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`

### Recommendations

- [x] **TB-326** `applied` — Raise the minimum volume gate for low-liquidity markets to about 20,000 traded volume delta, since the 10k-20k range still produced noisy CPI and thin-market alerts while 4k+ and 11k+ were often false positives.
- [x] **TB-327** `applied` — Increase the minimum price move floor to about 0.05 for quote-only alerts, because 0.02 moves were repeatedly labeled noise while 0.05+ began separating more informative CPI flow.
- [x] **TB-328** `applied` — Add a persistence rule: require the move to hold across multiple timestamps or several independent trades before triggering, especially for zero-liquidity and quote-driven markets.

---

## 2026-06-06 — Advisor snapshot 109

### Summary
The false positives are concentrated in low-liquidity or quote-only CPI/political markets where large volume deltas or brief quote moves occur without meaningful positive price follow-through. Analyst labels repeatedly call for requiring real executed flow, sustained multi-timestamp confirmation, or a larger price move before emitting signals.

### Next step
Tighten the detector to require both a positive price move and execution-confirmed follow-through for low-liquidity markets, rather than relying on volume delta alone.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-329** `rejected` — Raise the minimum price-move gate to filter flat or quote-churn events.
  - **Governor rejection**: TB-NULL-001 / Global hard floors and No null relaxations are violated because `score_threshold` is set to `None`, but the historical constraints require `score_threshold ≥ 2.2` and explicitly forbid `None`. The proposed tweak also relies on volume and price floors only, which is not itself a conflict, but the null score threshold directly conflicts with the locked tuning constraints.
- [ ] **TB-330** `rejected` — Add a confirmation rule requiring executed trades or multiple prints before signaling in quote-only markets.
  - **Governor rejection**: TB-NULL-001 / Global hard floors and No null relaxations are violated because `score_threshold` is set to `None`, but the historical constraints require `score_threshold ≥ 2.2` and explicitly forbid `None`. The proposed tweak also relies on volume and price floors only, which is not itself a conflict, but the null score threshold directly conflicts with the locked tuning constraints.
- [ ] **TB-331** `rejected` — Increase the volume threshold specifically for thin CPI/political contracts to suppress low-quality spikes.
  - **Governor rejection**: TB-NULL-001 / Global hard floors and No null relaxations are violated because `score_threshold` is set to `None`, but the historical constraints require `score_threshold ≥ 2.2` and explicitly forbid `None`. The proposed tweak also relies on volume and price floors only, which is not itself a conflict, but the null score threshold directly conflicts with the locked tuning constraints.

---

## 2026-06-06 — Advisor snapshot 110

### Summary
The false positives cluster around low-liquidity or quote-only moves with large volume deltas but little or no real price confirmation, especially in thin political/CPI-style markets. Analyst notes repeatedly call for requiring sustained traded flow, positive price movement, or multi-print follow-through before emitting a spike.

### Next step
Tighten the detector to require both a minimum positive price move and stronger trade confirmation for low-liquidity markets, rather than relying on volume delta alone.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-332** `rejected` — Raise the minimum price move to filter flat-action volume spikes, especially where priceΔ is near zero.
  - **Governor rejection**: TB-Global-ScoreGate is violated because the proposed tweak sets score_threshold to None, which removes an explicitly required score gate. Historical constraints require score_threshold ≥ 2.2 and explicitly forbid null/removed score gating.
- [ ] **TB-333** `rejected` — Increase the minimum volume delta for low-liquidity contracts so quote-only or thin-print events do not pass.
  - **Governor rejection**: TB-Global-ScoreGate is violated because the proposed tweak sets score_threshold to None, which removes an explicitly required score gate. Historical constraints require score_threshold ≥ 2.2 and explicitly forbid null/removed score gating.
- [ ] **TB-334** `rejected` — Add a confirmation rule requiring sustained multi-timestamp follow-through or multiple executed trades before signaling.
  - **Governor rejection**: TB-Global-ScoreGate is violated because the proposed tweak sets score_threshold to None, which removes an explicitly required score gate. Historical constraints require score_threshold ≥ 2.2 and explicitly forbid null/removed score gating.

---

## 2026-06-06 — Advisor snapshot 111

### Summary
False positives are concentrated in low-liquidity or quote-only markets, where isolated volume bursts or flat-price quote moves trigger signals without sustained follow-through. The analyst labels consistently favor requiring both stronger trade volume and a meaningful price move, especially in thin political and CPI markets.

### Next step
Raise the detector’s price-move floor and add a follow-through confirmation rule so volume spikes alone do not emit signals in thin markets.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-335** `rejected` — Increase min_price_move to 0.03 for low-liquidity and quote-only markets.
  - **Governor rejection**: Yes. The proposal violates the historical floor constraints by setting `min_price_move` to 0.03, which relaxes the explicitly protected global floor of `min_price_move/spike_min_price_move ≥ 0.05` and falls into the rejected 0.03–0.04 territory. It also conflicts with the requirement that `min_volume_delta/spike_min_volume_delta` must be explicit and never `None`, and with the requirement that `score_threshold ≥ 2.2` and never `None`. This is a regression against the tightened noise-filters for thin markets.
- [ ] **TB-336** `rejected` — Require either sustained multi-timestamp price movement or multiple independent prints before emitting a spike.
  - **Governor rejection**: Yes. The proposal violates the historical floor constraints by setting `min_price_move` to 0.03, which relaxes the explicitly protected global floor of `min_price_move/spike_min_price_move ≥ 0.05` and falls into the rejected 0.03–0.04 territory. It also conflicts with the requirement that `min_volume_delta/spike_min_volume_delta` must be explicit and never `None`, and with the requirement that `score_threshold ≥ 2.2` and never `None`. This is a regression against the tightened noise-filters for thin markets.
- [ ] **TB-337** `rejected` — Raise min_volume_delta for political and CPI contracts to suppress isolated block-trade noise.
  - **Governor rejection**: Yes. The proposal violates the historical floor constraints by setting `min_price_move` to 0.03, which relaxes the explicitly protected global floor of `min_price_move/spike_min_price_move ≥ 0.05` and falls into the rejected 0.03–0.04 territory. It also conflicts with the requirement that `min_volume_delta/spike_min_volume_delta` must be explicit and never `None`, and with the requirement that `score_threshold ≥ 2.2` and never `None`. This is a regression against the tightened noise-filters for thin markets.

---

## 2026-06-06 — Advisor snapshot 112

### Summary
The false positives are concentrated in thin or quote-driven markets where price can jump without durable executed flow, especially in low-liquidity or long-dated contracts. Analyst labels repeatedly ask for more confirmation from traded volume, trade count, and sustained multi-minute movement rather than isolated prints or single-quote swings.

### Next step
Raise the executed-volume floor and require a larger concurrent price move, while also adding a persistence rule so spikes must hold across multiple timestamps before emission.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-338** `rejected` — Increase the detector’s minimum executed-volume threshold for thin markets, especially CPI and zero-liquidity political contracts.
  - **Governor rejection**: TB-001 is violated because the proposed `min_price_move: 0.03` relaxes the active hard floor of `min_price_move ≥ 0.05` globally; the historical constraints explicitly reject 0.03–0.04. TB-003 is also violated because `score_threshold: None` conflicts with the active hard floor requiring `score_threshold ≥ 2.2` and explicitly forbidding `None`.
- [ ] **TB-339** `rejected` — Raise the minimum price-move requirement for a spike so quote-only blips do not trigger on flat or near-flat markets.
  - **Governor rejection**: TB-001 is violated because the proposed `min_price_move: 0.03` relaxes the active hard floor of `min_price_move ≥ 0.05` globally; the historical constraints explicitly reject 0.03–0.04. TB-003 is also violated because `score_threshold: None` conflicts with the active hard floor requiring `score_threshold ≥ 2.2` and explicitly forbidding `None`.
- [ ] **TB-340** `rejected` — Add a persistence filter: require multiple independent trades or sustained price change over several minutes before emitting a signal.
  - **Governor rejection**: TB-001 is violated because the proposed `min_price_move: 0.03` relaxes the active hard floor of `min_price_move ≥ 0.05` globally; the historical constraints explicitly reject 0.03–0.04. TB-003 is also violated because `score_threshold: None` conflicts with the active hard floor requiring `score_threshold ≥ 2.2` and explicitly forbidding `None`.

---

## 2026-06-06 — Advisor snapshot 113

### Summary
The false positives are concentrated in thin or quote-driven markets where large volume deltas do not coincide with meaningful executed price movement, especially in CPI and long-dated political contracts. Analyst labels consistently ask for more confirmation from sustained moves, executed prints, or trade imbalance before emitting a spike signal.

### Next step
Raise the minimum price-move requirement and add a persistence/confirmation rule so the detector only fires when volume is accompanied by sustained executed price movement, not a brief quote swing.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`, `score_threshold` → `20.0`

### Recommendations

- [x] **TB-341** `applied` — Increase spike_min_price_move from 0.03 to 0.05 to suppress flat or quote-only moves while preserving genuinely large spikes.
- [x] **TB-342** `applied` — Increase spike_min_volume_delta to 15000 to filter thin-market noise and isolated block prints.
- [x] **TB-343** `applied` — Require the signal to persist across multiple timestamps or traded prints before emission; if you need a numeric score gate, raise spike_score_threshold modestly to 20.0.

---

## 2026-06-06 — Advisor snapshot 114

### Summary
The false positives cluster in thin or quote-driven markets where large volume deltas are not paired with meaningful, sustained price movement. Analyst notes repeatedly ask for stricter confirmation via executed volume, multi-print persistence, and larger concurrent price change.

### Next step
Tighten the detector to require both higher executed volume and a sustained price move over multiple timestamps before emitting, especially for thin or low-priced markets.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-344** `rejected` — Raise spike_min_volume_delta to reduce isolated block-trade hits in long-dated and thin markets.
  - **Governor rejection**: Violates the historical **score gate** constraint: previously applied TB rule requires **score_threshold ≥ 2.2** and explicitly forbids `None`, but the proposed tweak sets `score_threshold: None`. The proposed `min_volume_delta: 20000.0` and `min_price_move: 0.05` do not conflict with the stated floors.
- [ ] **TB-345** `rejected` — Increase spike_min_price_move so flat-price, quote-only, or single-swing events do not trigger.
  - **Governor rejection**: Violates the historical **score gate** constraint: previously applied TB rule requires **score_threshold ≥ 2.2** and explicitly forbids `None`, but the proposed tweak sets `score_threshold: None`. The proposed `min_volume_delta: 20000.0` and `min_price_move: 0.05` do not conflict with the stated floors.
- [ ] **TB-346** `rejected` — Add a persistence rule: require the move to hold across multiple prints or minutes before the signal is emitted.
  - **Governor rejection**: Violates the historical **score gate** constraint: previously applied TB rule requires **score_threshold ≥ 2.2** and explicitly forbids `None`, but the proposed tweak sets `score_threshold: None`. The proposed `min_volume_delta: 20000.0` and `min_price_move: 0.05` do not conflict with the stated floors.

---

## 2026-06-06 — Advisor snapshot 115

### Summary
The false positives are concentrated in thin or category-specific markets where isolated volume bursts or quote-driven moves are being promoted without enough confirmed execution or sustained price follow-through. The analyst labels consistently ask for stricter volume confirmation and a larger, more durable price move before emitting a spike.

### Next step
Raise the minimum volume delta and minimum price move together, and add a persistence rule so spikes require sustained price movement over multiple minutes instead of a single bar or quote swing.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-347** `rejected` — Increase the volume gate for thin macro and low-priced markets to suppress one-off prints and quote noise.
  - **Governor rejection**: The proposed tweak conflicts with the historical global floor rules: it lowers `min_price_move` to 0.03, violating the explicitly enforced `min_price_move >= 0.05` price-confirmation gate for general spike detection and low-liquidity/category-specific markets. It also sets `score_threshold` to `None`, which violates the active score gate requiring `score_threshold >= 2.2` with no `None` relaxation. The added persistence rule is compatible, but the threshold relaxations are not.
- [ ] **TB-348** `rejected` — Require a non-trivial concurrent price move before signal emission, especially for long-dated political markets.
  - **Governor rejection**: The proposed tweak conflicts with the historical global floor rules: it lowers `min_price_move` to 0.03, violating the explicitly enforced `min_price_move >= 0.05` price-confirmation gate for general spike detection and low-liquidity/category-specific markets. It also sets `score_threshold` to `None`, which violates the active score gate requiring `score_threshold >= 2.2` with no `None` relaxation. The added persistence rule is compatible, but the threshold relaxations are not.
- [ ] **TB-349** `rejected` — If persistence is available, require multi-minute follow-through or positive trade imbalance before flagging a spike.
  - **Governor rejection**: The proposed tweak conflicts with the historical global floor rules: it lowers `min_price_move` to 0.03, violating the explicitly enforced `min_price_move >= 0.05` price-confirmation gate for general spike detection and low-liquidity/category-specific markets. It also sets `score_threshold` to `None`, which violates the active score gate requiring `score_threshold >= 2.2` with no `None` relaxation. The added persistence rule is compatible, but the threshold relaxations are not.

---

## 2026-06-06 — Advisor snapshot 116

### Summary
The false positives are coming from low-liquidity or thin markets where quote churn, isolated blocks, or flat-price volume bursts trigger signals without sustained directional confirmation. Analyst labels consistently favor stronger confirmation from executed volume, trade count, and a real price move rather than single-print or alternating-quote activity.

### Next step
Raise the minimum executed-volume requirement and add a stronger price-move confirmation rule, so spikes only emit when volume is accompanied by sustained directional movement rather than churn.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.03`, `score_threshold` → `20.0`

### Recommendations

- [ ] **TB-350** `rejected` — Increase the volume gate for thin markets and low-priced contracts to suppress flat-price volume bursts.
  - **Governor rejection**: The proposed tweak violates the historical hard floor for price confirmation: TB-PRICE-HARD-FLOOR / price confirmation hierarchy requires min_price_move ≥ 0.05 and explicitly rejects sub-5% relaxations, including 0.03–0.04, even when paired with stronger volume or score filters. Setting min_price_move to 0.03 conflicts with that prior tightening. The proposed score_threshold of 20.0 and higher min_volume_delta do not create the conflict; the price floor does.
- [ ] **TB-351** `rejected` — Require a larger minimum price move, especially for long-dated or macro-style markets where isolated prints are misleading.
  - **Governor rejection**: The proposed tweak violates the historical hard floor for price confirmation: TB-PRICE-HARD-FLOOR / price confirmation hierarchy requires min_price_move ≥ 0.05 and explicitly rejects sub-5% relaxations, including 0.03–0.04, even when paired with stronger volume or score filters. Setting min_price_move to 0.03 conflicts with that prior tightening. The proposed score_threshold of 20.0 and higher min_volume_delta do not create the conflict; the price floor does.
- [ ] **TB-352** `rejected` — Add a persistence rule: confirm only if the move holds across multiple minutes or is backed by executed trades, not just quote alternation.
  - **Governor rejection**: The proposed tweak violates the historical hard floor for price confirmation: TB-PRICE-HARD-FLOOR / price confirmation hierarchy requires min_price_move ≥ 0.05 and explicitly rejects sub-5% relaxations, including 0.03–0.04, even when paired with stronger volume or score filters. Setting min_price_move to 0.03 conflicts with that prior tightening. The proposed score_threshold of 20.0 and higher min_volume_delta do not create the conflict; the price floor does.

---

## 2026-06-06 — Advisor snapshot 117

### Summary
The false positives are coming from thin or illiquid markets where quote churn or isolated block trades create large apparent spikes without sustained execution or directional follow-through. The analyst labels consistently favor adding stronger confirmation from executed volume, trade count, and persistence of price move rather than relying on one-shot jumps.

### Next step
Raise the confirmation bar so a spike only emits when executed volume and price movement both clear higher thresholds, and require persistence over multiple minutes for thin markets.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-353** `rejected` — Increase the minimum executed-volume threshold for thin markets to filter out quote-only churn and isolated prints.
  - **Governor rejection**: The proposed tweak violates the historical hard floor by setting `min_price_move: 0.03`, which conflicts with the explicitly hardened global minimum `min_price_move ≥ 0.05` and the stricter 5% floor for low-liquidity / watch / notable / high-odds markets. It also sets `score_threshold: None`, which conflicts with the requirement that score remain an active filter with `score_threshold ≥ 2.2` and no `None` relaxations for this gate.
- [ ] **TB-354** `rejected` — Require a larger concurrent price move before emitting, especially for long-dated or macro-style contracts.
  - **Governor rejection**: The proposed tweak violates the historical hard floor by setting `min_price_move: 0.03`, which conflicts with the explicitly hardened global minimum `min_price_move ≥ 0.05` and the stricter 5% floor for low-liquidity / watch / notable / high-odds markets. It also sets `score_threshold: None`, which conflicts with the requirement that score remain an active filter with `score_threshold ≥ 2.2` and no `None` relaxations for this gate.
- [ ] **TB-355** `rejected` — Add a persistence rule: price must stay directionally moved for multiple minutes rather than triggering on a single swing.
  - **Governor rejection**: The proposed tweak violates the historical hard floor by setting `min_price_move: 0.03`, which conflicts with the explicitly hardened global minimum `min_price_move ≥ 0.05` and the stricter 5% floor for low-liquidity / watch / notable / high-odds markets. It also sets `score_threshold: None`, which conflicts with the requirement that score remain an active filter with `score_threshold ≥ 2.2` and no `None` relaxations for this gate.

---

## 2026-06-06 — Advisor snapshot 118

### Summary
The false positives are concentrated in thin or low-priced markets where quote churn, isolated block trades, or tiny price moves can trigger spikes without sustained execution flow. The analyst notes consistently call for stricter confirmation from executed volume and larger, sustained price movement.

### Next step
Raise the detection bar for low-liquidity markets by requiring both higher executed volume and a larger price move before emitting a spike, with additional confirmation from trade count or multi-minute persistence.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-356** `rejected` — Increase the volume-delta floor for thin macro and long-dated political markets to suppress block-trade and quote-burst noise.
  - **Governor rejection**: The proposed tweak violates the historical global hard floor TB-001 because it sets min_price_move to 0.03, which explicitly relaxes the previously enforced minimum of min_price_move ≥ 0.05. It also conflicts with TB-002/TB-004/TB-007 style low-liquidity guardrails, which require a stronger price move floor (≥ 0.05) and/or explicit directional, trade-count, and persistence confirmation rather than lowering the price threshold. Setting score_threshold to None also conflicts with the score hardening rule because score must remain an active non-None gate with score_threshold ≥ 2.2.
- [ ] **TB-357** `rejected` — Require a larger minimum price move, especially in low-priced markets, so micro-moves do not pass as spikes.
  - **Governor rejection**: The proposed tweak violates the historical global hard floor TB-001 because it sets min_price_move to 0.03, which explicitly relaxes the previously enforced minimum of min_price_move ≥ 0.05. It also conflicts with TB-002/TB-004/TB-007 style low-liquidity guardrails, which require a stronger price move floor (≥ 0.05) and/or explicit directional, trade-count, and persistence confirmation rather than lowering the price threshold. Setting score_threshold to None also conflicts with the score hardening rule because score must remain an active non-None gate with score_threshold ≥ 2.2.
- [ ] **TB-358** `rejected` — Add a persistence rule: confirm the signal only if the move is sustained across multiple minutes and supported by executed trades rather than quotes alone.
  - **Governor rejection**: The proposed tweak violates the historical global hard floor TB-001 because it sets min_price_move to 0.03, which explicitly relaxes the previously enforced minimum of min_price_move ≥ 0.05. It also conflicts with TB-002/TB-004/TB-007 style low-liquidity guardrails, which require a stronger price move floor (≥ 0.05) and/or explicit directional, trade-count, and persistence confirmation rather than lowering the price threshold. Setting score_threshold to None also conflicts with the score hardening rule because score must remain an active non-None gate with score_threshold ≥ 2.2.

---

## 2026-06-06 — Advisor snapshot 119

### Summary
Recent false positives cluster in thin, low-priced or quote-driven markets where large volume or quote churn produces only small or fleeting price moves. Analyst notes consistently ask for more execution-based confirmation and persistence, rather than simply lowering sensitivity to price or volume.

### Next step
Raise the detector’s confirmation bar for thin markets by requiring both higher executed volume and a sustained price move over multiple minutes before emitting a spike.

### Suggested thresholds
`min_volume_delta` → `12000.0`, `min_price_move` → `0.12`

### Recommendations

- [ ] **TB-359** `rejected` — Increase the minimum executed-volume trigger for thin macro/political markets to cut isolated block-trade noise.
  - **Governor rejection**: TB-001 violated: `score_threshold` is set to `None`, but the historical constraint requires an explicit, non-None `score_threshold` of at least 2.2. The proposed `min_volume_delta: 12000.0` and `min_price_move: 0.12` do not conflict with the stated floors.
- [ ] **TB-360** `rejected` — Raise the minimum price-move requirement slightly and add a persistence check so brief quote bursts do not fire signals.
  - **Governor rejection**: TB-001 violated: `score_threshold` is set to `None`, but the historical constraint requires an explicit, non-None `score_threshold` of at least 2.2. The proposed `min_volume_delta: 12000.0` and `min_price_move: 0.12` do not conflict with the stated floors.
- [ ] **TB-361** `rejected` — Require trade-count or executed-volume confirmation instead of quote churn alone for markets with sparse prints.
  - **Governor rejection**: TB-001 violated: `score_threshold` is set to `None`, but the historical constraint requires an explicit, non-None `score_threshold` of at least 2.2. The proposed `min_volume_delta: 12000.0` and `min_price_move: 0.12` do not conflict with the stated floors.

---

## 2026-06-06 — Advisor snapshot 120

### Summary
The false positives are concentrated in thin, low-priced macro markets where quote bursts or one-minute micro-moves are being mistaken for real flow. The analyst labels consistently call for stronger confirmation from executed volume and sustained price movement rather than single-spike activity.

### Next step
Tighten the detector with a higher executed-volume/confirmation requirement for thin markets, and require the price move to persist for multiple minutes before emitting a signal.

### Suggested thresholds
`min_volume_delta` → `11000.0`, `min_price_move` → `0.12`

### Recommendations

- [ ] **TB-362** `rejected` — Raise spike_min_volume_delta to filter thin-book quote bursts in low-priced macro markets.
  - **Governor rejection**: The proposal conflicts with the historical global floor rule by setting `score_threshold` to `None`, which violates the explicit constraint that `score_threshold ≥ 2.2` and must never be `None`. It also appears to relax the price floor relative to prior tightening: `min_price_move: 0.12` does not violate the floor itself, but the change to `score_threshold` removes an active filter that was explicitly retained for borderline watch-tier / thin-liquidity cases.
- [ ] **TB-363** `rejected` — Increase spike_min_price_move modestly so only more material moves trigger, but avoid over-tightening because the labeled signals still show meaningful price deltas.
  - **Governor rejection**: The proposal conflicts with the historical global floor rule by setting `score_threshold` to `None`, which violates the explicit constraint that `score_threshold ≥ 2.2` and must never be `None`. It also appears to relax the price floor relative to prior tightening: `min_price_move: 0.12` does not violate the floor itself, but the change to `score_threshold` removes an active filter that was explicitly retained for borderline watch-tier / thin-liquidity cases.
- [ ] **TB-364** `rejected` — Add a persistence rule: require the move to remain directional for more than one minute, or confirm with executed trades versus quotes before signaling.
  - **Governor rejection**: The proposal conflicts with the historical global floor rule by setting `score_threshold` to `None`, which violates the explicit constraint that `score_threshold ≥ 2.2` and must never be `None`. It also appears to relax the price floor relative to prior tightening: `min_price_move: 0.12` does not violate the floor itself, but the change to `score_threshold` removes an active filter that was explicitly retained for borderline watch-tier / thin-liquidity cases.

---

## 2026-06-06 — Advisor snapshot 121

### Summary
The false positives are concentrated in low-priced, thin macro markets where quote churn or small price blips are being promoted as spikes despite weak executed flow. The clearest pattern is that analysts want stronger confirmation from volume and persistence, not just a one-bar move.

### Next step
Tighten the detector by requiring both a larger price move and stronger executed-volume confirmation before emitting in low-priced illiquid markets; if only one rule changes, raise the price-move floor and add a persistence check.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.06`

### Recommendations

- [ ] **TB-365** `rejected` — Raise spike_min_price_move from 0.03 to 0.06 for low-priced macro markets to suppress small quote-driven fluctuations.
  - **Governor rejection**: TB-GLOBAL-HARD-FLOORS is violated because the proposed tweak sets `score_threshold` to `None`, but the historical constraints require an explicit non-`None` `score_threshold` and keep it at least 2.2. The proposed `min_price_move: 0.06` does not conflict with the price-floor constraints, but removing the score gate does.
- [ ] **TB-366** `rejected` — Increase spike_min_volume_delta from 10000 to 15000 to require a clearer executed-volume burst over baseline.
  - **Governor rejection**: TB-GLOBAL-HARD-FLOORS is violated because the proposed tweak sets `score_threshold` to `None`, but the historical constraints require an explicit non-`None` `score_threshold` and keep it at least 2.2. The proposed `min_price_move: 0.06` does not conflict with the price-floor constraints, but removing the score gate does.
- [ ] **TB-367** `rejected` — Add a persistence rule: require the price move to remain directionally intact for at least 1 minute before signaling.
  - **Governor rejection**: TB-GLOBAL-HARD-FLOORS is violated because the proposed tweak sets `score_threshold` to `None`, but the historical constraints require an explicit non-`None` `score_threshold` and keep it at least 2.2. The proposed `min_price_move: 0.06` does not conflict with the price-floor constraints, but removing the score gate does.

---

## 2026-06-06 — Advisor snapshot 122

### Summary
The false positives are dominated by quote-driven or thin-book micro-spikes in low-priced macro markets, where large quote churn or brief price jumps are being flagged without sustained executed volume. Analyst labels consistently ask for stronger confirmation from traded volume and persistence over multiple minutes before emission.

### Next step
Raise the confirmation bar: require both a larger price move and sustained executed volume over more than one minute before emitting a spike, especially for low-priced or no-trade macro markets.

### Suggested thresholds
`min_volume_delta` → `18000.0`, `min_price_move` → `0.08`

### Recommendations

- [ ] **TB-368** `rejected` — Increase spike_min_price_move to 0.08 to 0.10 for low-priced macro markets.
  - **Governor rejection**: TB-NULL-01 is violated because the proposed tweak sets `score_threshold` to `None`, and the historical constraints explicitly reject any rule that sets `score_threshold` to `None`. The proposed `min_price_move: 0.08` and `min_volume_delta: 18000.0` do not conflict with the stated hard floors, but the null relaxation alone is a rejection.
- [ ] **TB-369** `rejected` — Increase spike_min_volume_delta to around 15000 to 20000 to suppress quote bursts in thin books.
  - **Governor rejection**: TB-NULL-01 is violated because the proposed tweak sets `score_threshold` to `None`, and the historical constraints explicitly reject any rule that sets `score_threshold` to `None`. The proposed `min_price_move: 0.08` and `min_volume_delta: 18000.0` do not conflict with the stated hard floors, but the null relaxation alone is a rejection.
- [ ] **TB-370** `rejected` — Keep spike_score_threshold roughly unchanged unless you need an additional global brake; use market-specific persistence rules first.
  - **Governor rejection**: TB-NULL-01 is violated because the proposed tweak sets `score_threshold` to `None`, and the historical constraints explicitly reject any rule that sets `score_threshold` to `None`. The proposed `min_price_move: 0.08` and `min_volume_delta: 18000.0` do not conflict with the stated hard floors, but the null relaxation alone is a rejection.

---

## 2026-06-06 — Advisor snapshot 123

### Summary
The false positives are concentrated in thin macro markets where quote churn and small micro-moves are being mistaken for real spikes, especially when executed volume is weak or absent. The analyst labels consistently call for stronger confirmation from executed trades and/or sustained movement rather than purely quote-driven activity.

### Next step
Require both a larger price move and executed-volume confirmation before emitting in thin macro markets; the single best change is to raise the price-move floor and pair it with a higher trade-confirmation bar to suppress quote-driven noise.

### Suggested thresholds
`min_price_move` → `0.1`

### Recommendations

- [ ] **TB-371** `rejected` — Increase spike_min_price_move from 0.03 to 0.10 for low-priced macro markets.
  - **Governor rejection**: Yes. The proposed tweak violates the historical hard-floor policy by setting `min_volume_delta: None`, which conflicts with the global hard floor requiring `min_volume_delta` to be explicit/non-`None` and rejecting `None` relaxations. It also conflicts with the combined-gate and trade-confirmation rules because the change weakens the executed-volume confirmation exactly in the thin/quote-churn regime where stronger trade confirmation was previously required.
- [ ] **TB-372** `rejected` — Raise spike_min_volume_delta from the current level to a stricter baseline, and require executed trades rather than quote changes as the confirming volume source.
  - **Governor rejection**: Yes. The proposed tweak violates the historical hard-floor policy by setting `min_volume_delta: None`, which conflicts with the global hard floor requiring `min_volume_delta` to be explicit/non-`None` and rejecting `None` relaxations. It also conflicts with the combined-gate and trade-confirmation rules because the change weakens the executed-volume confirmation exactly in the thin/quote-churn regime where stronger trade confirmation was previously required.
- [ ] **TB-373** `rejected` — Lift spike_score_threshold modestly to reduce borderline emits that are still mostly quote-driven.
  - **Governor rejection**: Yes. The proposed tweak violates the historical hard-floor policy by setting `min_volume_delta: None`, which conflicts with the global hard floor requiring `min_volume_delta` to be explicit/non-`None` and rejecting `None` relaxations. It also conflicts with the combined-gate and trade-confirmation rules because the change weakens the executed-volume confirmation exactly in the thin/quote-churn regime where stronger trade confirmation was previously required.

---

## 2026-06-06 — Advisor snapshot 124

### Summary
The false positives are concentrated in thin, low-priced macro markets where quote-heavy bursts or alternating quotes are being mistaken for meaningful spikes. Analyst labels consistently ask for stronger confirmation from executed trades and/or a sustained multi-minute price move.

### Next step
Raise the detector’s confirmation bar by requiring both a larger price move and executed-volume confirmation for low-priced markets, with a persistence check over more than one minute before emitting a signal.

### Suggested thresholds
`min_volume_delta` → `10000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-374** `rejected` — Increase the minimum price move for low-priced macro markets to filter out micro-moves driven by quote churn.
  - **Governor rejection**: The proposed tweak conflicts with the historical hard floor on price movement: it sets `min_price_move: 0.03`, which violates the active global noise-suppression constraint requiring `min_price_move ≥ 0.05` and explicitly rejecting 0.03–0.04 near-noise thresholds. It also weakens the execution-backed gating by leaving `score_threshold` as `None`, which conflicts with the active hard floor requiring `score_threshold ≥ 2.2` with no null relaxations.
- [ ] **TB-375** `rejected` — Require executed trades, not just quotes, to meet the spike condition when volume delta is high but trade confirmation is weak.
  - **Governor rejection**: The proposed tweak conflicts with the historical hard floor on price movement: it sets `min_price_move: 0.03`, which violates the active global noise-suppression constraint requiring `min_price_move ≥ 0.05` and explicitly rejecting 0.03–0.04 near-noise thresholds. It also weakens the execution-backed gating by leaving `score_threshold` as `None`, which conflicts with the active hard floor requiring `score_threshold ≥ 2.2` with no null relaxations.
- [ ] **TB-376** `rejected` — Add a persistence rule: the price move must hold for at least 2 minutes before the signal is emitted.
  - **Governor rejection**: The proposed tweak conflicts with the historical hard floor on price movement: it sets `min_price_move: 0.03`, which violates the active global noise-suppression constraint requiring `min_price_move ≥ 0.05` and explicitly rejecting 0.03–0.04 near-noise thresholds. It also weakens the execution-backed gating by leaving `score_threshold` as `None`, which conflicts with the active hard floor requiring `score_threshold ≥ 2.2` with no null relaxations.

---

## 2026-06-06 — Advisor snapshot 125

### Summary
The recent false positives are concentrated in thin, low-priced macro markets where quote-driven bursts and small short-lived price moves are being overclassified as spikes. Analyst labels consistently ask for stronger execution confirmation, larger sustained price moves, and longer persistence before emission.

### Next step
Raise the detector’s price-move requirement and add an execution-confirmation rule so quote bursts do not pass without meaningful traded-volume support.

### Suggested thresholds
`min_volume_delta` → `12000.0`, `min_price_move` → `0.12`

### Recommendations

- [ ] **TB-377** `rejected` — Increase the minimum fractional price move to 0.12 to suppress small quote-driven micro-moves in low-priced macro markets.
  - **Governor rejection**: TB-Score-Floor: the proposed tweak sets `score_threshold` to None, which conflicts with the historical constraint that `score_threshold` must be explicit and >= 2.2; rejecting None was explicitly required.
- [ ] **TB-378** `rejected` — Raise the minimum volume delta to 12000 to require more executed flow before flagging a spike.
  - **Governor rejection**: TB-Score-Floor: the proposed tweak sets `score_threshold` to None, which conflicts with the historical constraint that `score_threshold` must be explicit and >= 2.2; rejecting None was explicitly required.
- [ ] **TB-379** `rejected` — Require the price move to persist for at least 2 minutes or be confirmed by a higher share of executed trades versus quotes.
  - **Governor rejection**: TB-Score-Floor: the proposed tweak sets `score_threshold` to None, which conflicts with the historical constraint that `score_threshold` must be explicit and >= 2.2; rejecting None was explicitly required.

---

## 2026-06-06 — Advisor snapshot 126

### Summary
The false positives are concentrated in thin, low-priced macro markets where quote-heavy bursts produce large apparent price moves without enough executed volume confirmation. Analyst labels consistently call for stronger volume confirmation and multi-minute persistence before emitting a spike.

### Next step
Tighten the detector to require both a larger executed-volume delta and a sustained price move over multiple minutes before flagging low-priced macro-market spikes.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-380** `rejected` — Raise the minimum executed-volume delta for low-priced markets to around 20,000 so quote bursts like the 7k–11k cases do not trigger signals.
  - **Governor rejection**: TB-Global-hard-floors is violated because the proposed tweak sets `score_threshold` to `None`, which is an explicit null relaxation of a core gate. The historical constraints require `score_threshold ≥ 2.2` with no `None` relaxations, and also state `No null gating` for core thresholds. The other proposed thresholds (`min_price_move: 0.05`, `min_volume_delta: 20000.0`) do not conflict with the stated floors.
- [ ] **TB-381** `rejected` — Raise the minimum price move to about 0.05 (5%) for thin macro markets, or require that smaller moves persist for more than one minute.
  - **Governor rejection**: TB-Global-hard-floors is violated because the proposed tweak sets `score_threshold` to `None`, which is an explicit null relaxation of a core gate. The historical constraints require `score_threshold ≥ 2.2` with no `None` relaxations, and also state `No null gating` for core thresholds. The other proposed thresholds (`min_price_move: 0.05`, `min_volume_delta: 20000.0`) do not conflict with the stated floors.
- [ ] **TB-382** `rejected` — Increase the combined score threshold modestly, but use it as a secondary filter after volume and persistence gating rather than the primary fix.
  - **Governor rejection**: TB-Global-hard-floors is violated because the proposed tweak sets `score_threshold` to `None`, which is an explicit null relaxation of a core gate. The historical constraints require `score_threshold ≥ 2.2` with no `None` relaxations, and also state `No null gating` for core thresholds. The other proposed thresholds (`min_price_move: 0.05`, `min_volume_delta: 20000.0`) do not conflict with the stated floors.

---

## 2026-06-06 — Advisor snapshot 127

### Summary
The false positives are concentrated in thin, low-priced macro markets where quote-driven bursts produce large apparent price moves without enough executed-volume confirmation. Analyst labels repeatedly ask for stronger volume and sustained multi-minute confirmation rather than single-burst triggers.

### Next step
Tighten the detector around executed flow: require a higher minimum volume delta and a larger sustained price move before score-based emission, especially in low-priced macro markets.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.08`, `score_threshold` → `10.0`

### Recommendations

- [x] **TB-383** `applied` — Raise min_volume_delta to about 20000 to suppress quote-only bursts below meaningful executed flow.
- [x] **TB-384** `applied` — Raise min_price_move to about 0.08 so small one-minute oscillations do not trigger spikes.
- [x] **TB-385** `applied` — Increase score_threshold modestly to about 10.0 to filter marginal events while keeping clearly informative flow.

---

## 2026-06-06 — Advisor snapshot 128

### Summary
The false positives are concentrated in thin macro markets where quote-driven price bursts and low executed trade activity are being mistaken for real spikes. The analyst notes consistently recommend adding confirmation from executed volume, trade count, or sustained multi-minute movement before emitting a signal.

### Next step
Add an executed-activity confirmation rule: require both a higher minimum volume delta and a larger price move for low-liquidity macro markets, rather than relying on either alone.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.12`, `score_threshold` → `25.0`

### Recommendations

- [x] **TB-386** `applied` — Raise min_volume_delta to 20000 for thin macro markets to filter quote-only bursts.
- [x] **TB-387** `applied` — Raise min_price_move to 0.12 for low-price macro contracts so brief 3%-4% wiggles do not trigger signals.
- [x] **TB-388** `applied` — Increase score_threshold modestly to suppress marginal alerts, while keeping high-conviction spikes detectable.

---

## 2026-06-06 — Advisor snapshot 129

### Summary
Recent false positives are concentrated in thin, low-priced macro markets where quote-driven or low-trade bursts produce large apparent price moves without enough executed volume. Analyst labels consistently ask for stronger confirmation from real trades, not just price or quote oscillations.

### Next step
Raise the detector’s executed-volume confirmation requirement first: require a higher minimum volume delta and/or a minimum executed-trade share before emitting spikes in low-liquidity macro markets.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.12`

### Recommendations

- [ ] **TB-389** `rejected` — Increase min_volume_delta for thin macro markets to filter quote-only bursts that are currently triggering on small trade counts.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets `score_threshold` to `None`, which conflicts with the explicit historical constraint that `score_threshold` must be non-`None` and ≥ 2.2. TB-002 is also violated because `min_price_move` is tightened to 0.12, which is not itself a conflict, but the proposal does not address the required explicit/non-`None` `min_volume_delta` in a way that violates the rule; the only clear conflict is the null score gate relaxation.
- [ ] **TB-390** `rejected` — Add a rule that price moves must be confirmed by executed trading activity over multiple minutes, not a single burst.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets `score_threshold` to `None`, which conflicts with the explicit historical constraint that `score_threshold` must be non-`None` and ≥ 2.2. TB-002 is also violated because `min_price_move` is tightened to 0.12, which is not itself a conflict, but the proposal does not address the required explicit/non-`None` `min_volume_delta` in a way that violates the rule; the only clear conflict is the null score gate relaxation.
- [ ] **TB-391** `rejected` — If you want a single global knob, modestly lift the score threshold only after tightening the volume/trade-confirmation rule, so genuinely informative high-volume spikes still pass.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets `score_threshold` to `None`, which conflicts with the explicit historical constraint that `score_threshold` must be non-`None` and ≥ 2.2. TB-002 is also violated because `min_price_move` is tightened to 0.12, which is not itself a conflict, but the proposal does not address the required explicit/non-`None` `min_volume_delta` in a way that violates the rule; the only clear conflict is the null score gate relaxation.

---

## 2026-06-06 — Advisor snapshot 130

### Summary
The false positives are concentrated in low-liquidity, low-price macro markets where quote bursts and a few trades create large apparent price moves. Analyst notes repeatedly ask for more execution-based confirmation and a larger sustained move before emitting a spike.

### Next step
Increase the detector’s execution-quality gate: require both a higher minimum executed volume delta and a larger sustained price move before scoring can trigger a signal, especially for thin macro markets.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.12`

### Recommendations

- [ ] **TB-392** `rejected` — Raise the minimum executed volume delta to filter quote-only bursts in thin markets.
  - **Governor rejection**: TB-001 and TB-003 are violated: `score_threshold` is proposed as None, but the historical global floor requires an explicit `score_threshold`/`spike_score_threshold` of at least 2.2; additionally, the tweak does not preserve the required explicit non-None scoring gate. The proposed `min_price_move` of 0.12 and `min_volume_delta` of 15000 do not conflict with the stated floors themselves.
- [ ] **TB-393** `rejected` — Increase the minimum price move for low-price macro markets so small quote oscillations do not count as spikes.
  - **Governor rejection**: TB-001 and TB-003 are violated: `score_threshold` is proposed as None, but the historical global floor requires an explicit `score_threshold`/`spike_score_threshold` of at least 2.2; additionally, the tweak does not preserve the required explicit non-None scoring gate. The proposed `min_price_move` of 0.12 and `min_volume_delta` of 15000 do not conflict with the stated floors themselves.
- [ ] **TB-394** `rejected` — Add a rule requiring the move to persist across multiple minutes or be backed by a higher share of executed trades before emission.
  - **Governor rejection**: TB-001 and TB-003 are violated: `score_threshold` is proposed as None, but the historical global floor requires an explicit `score_threshold`/`spike_score_threshold` of at least 2.2; additionally, the tweak does not preserve the required explicit non-None scoring gate. The proposed `min_price_move` of 0.12 and `min_volume_delta` of 15000 do not conflict with the stated floors themselves.

---

## 2026-06-06 — Advisor snapshot 131

### Summary
The false positives are concentrated in low-priced, thin macro markets where quote-heavy bursts create large apparent price moves without enough executed flow. Analyst notes consistently ask for stronger trade-count/executed-volume confirmation and, in some cases, a larger sustained move before emitting a spike.

### Next step
Raise the price-move requirement for low-priced macro markets and pair it with a higher executed-volume floor, so quote-only bursts no longer clear the detector.

### Suggested thresholds
`min_volume_delta` → `10000.0`, `min_price_move` → `0.1`

### Recommendations

- [ ] **TB-395** `rejected` — Increase spike_min_price_move to 0.10 for low-priced macro contracts.
  - **Governor rejection**: TB-GLOBAL-001 is violated because the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical constraint that `score_threshold ≥ 2.2` with no `None` relaxations. The other changes (`min_price_move: 0.1`, `min_volume_delta: 10000.0`) are tightening moves, not conflicts.
- [ ] **TB-396** `rejected` — Increase spike_min_volume_delta to 10000 to filter thin-market quote bursts.
  - **Governor rejection**: TB-GLOBAL-001 is violated because the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical constraint that `score_threshold ≥ 2.2` with no `None` relaxations. The other changes (`min_price_move: 0.1`, `min_volume_delta: 10000.0`) are tightening moves, not conflicts.
- [ ] **TB-397** `rejected` — If market price is below 0.25, require both the higher volume delta and a sustained multi-minute move before signaling.
  - **Governor rejection**: TB-GLOBAL-001 is violated because the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical constraint that `score_threshold ≥ 2.2` with no `None` relaxations. The other changes (`min_price_move: 0.1`, `min_volume_delta: 10000.0`) are tightening moves, not conflicts.

---

## 2026-06-06 — Advisor snapshot 132

### Summary
The false positives cluster around **thin macro markets** where **large quote-driven or low-trade bursts** create big apparent volume deltas and price moves without analyst-confirmed signal. The strongest pattern is that current thresholds are too permissive on *price move confirmation* relative to the noisy volume/quote activity.

### Next step
Tighten the detector by requiring a larger minimum price move and a minimum executed-volume filter for thin macro markets before emitting a signal.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-398** `rejected` — Raise the price-move floor for watch/notable spikes to suppress quote-only bursts on macro markets.
  - **Governor rejection**: The proposal violates the historical constraint that `min_volume_delta` must be explicit and never `None` (global floors). It also conflicts with the thin macro / political / Fed / nomination-market guidance that requires executed-trade confirmation and a raised volume floor to suppress quote-driven bursts; setting `min_volume_delta: None` removes that protection. In addition, `score_threshold: None` conflicts with the global floor `score_threshold >= 2.2` and the rule against null relaxations for core gates.
- [ ] **TB-399** `rejected` — Add an executed-volume or trade-count gate so volume deltas from quote changes do not trigger alerts.
  - **Governor rejection**: The proposal violates the historical constraint that `min_volume_delta` must be explicit and never `None` (global floors). It also conflicts with the thin macro / political / Fed / nomination-market guidance that requires executed-trade confirmation and a raised volume floor to suppress quote-driven bursts; setting `min_volume_delta: None` removes that protection. In addition, `score_threshold: None` conflicts with the global floor `score_threshold >= 2.2` and the rule against null relaxations for core gates.
- [ ] **TB-400** `rejected` — Keep the score threshold unchanged for now; the analyst labels point more to bad trigger conditions than to combined-score calibration.
  - **Governor rejection**: The proposal violates the historical constraint that `min_volume_delta` must be explicit and never `None` (global floors). It also conflicts with the thin macro / political / Fed / nomination-market guidance that requires executed-trade confirmation and a raised volume floor to suppress quote-driven bursts; setting `min_volume_delta: None` removes that protection. In addition, `score_threshold: None` conflicts with the global floor `score_threshold >= 2.2` and the rule against null relaxations for core gates.

---

## 2026-06-06 — Advisor snapshot 133

### Summary
The false positives are concentrated in thinly traded macro markets where large volume deltas can still come from quote churn or a few trades, and some alerts are firing on modest 2% price moves. The analyst labels consistently recommend requiring stronger real execution evidence, especially a larger price move and/or higher trade-count or notional-change confirmation.

### Next step
Keep the volume gate strict for low-liquidity markets, but raise the price-move requirement to filter out quote-driven noise and only emit when volume is paired with a more meaningful move.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-401** `rejected` — Increase spike_min_price_move from 0.03 to 0.05 for macro markets with thin liquidity.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it sets `min_volume_delta: None`, which violates the global hard floor requiring `min_volume_delta` to be explicit/non-`None`, and it also sets `score_threshold: None`, which violates the global hard floor requiring `score_threshold ≥ 2.2` with no `None` relaxations. This is a regression relative to the hardened constraints, even though `min_price_move: 0.05` is consistent with the price-move floor.
- [ ] **TB-402** `rejected` — Add a secondary rule requiring either higher executed trade count or higher notional change when volume delta is large but price move is below threshold.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it sets `min_volume_delta: None`, which violates the global hard floor requiring `min_volume_delta` to be explicit/non-`None`, and it also sets `score_threshold: None`, which violates the global hard floor requiring `score_threshold ≥ 2.2` with no `None` relaxations. This is a regression relative to the hardened constraints, even though `min_price_move: 0.05` is consistent with the price-move floor.
- [ ] **TB-403** `rejected` — Leave spike_score_threshold unchanged for now; the strongest false-positive pattern is weak price confirmation, not low combined score.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it sets `min_volume_delta: None`, which violates the global hard floor requiring `min_volume_delta` to be explicit/non-`None`, and it also sets `score_threshold: None`, which violates the global hard floor requiring `score_threshold ≥ 2.2` with no `None` relaxations. This is a regression relative to the hardened constraints, even though `min_price_move: 0.05` is consistent with the price-move floor.

---

## 2026-06-06 — Advisor snapshot 134

### Summary
The false positives are concentrated in thinly traded macro markets where volume spikes and even large price moves are being triggered by quote churn or very few trades. Analyst labels repeatedly recommend requiring more real executed volume and/or a larger price move before emitting a signal.

### Next step
Tighten the detector for low-liquidity macro markets by raising the minimum price-move requirement and adding a stronger volume/notional floor so quote-driven churn cannot clear the spike rule.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-404** `rejected` — Raise spike_min_price_move from 0.03 to 0.05 for macro/low-liquidity names.
  - **Governor rejection**: TB-XXX violation: the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical no-null relaxation rule and the global hard floor that `score_threshold/spike_score_threshold` must remain explicit and ≥ 2.2. Even though `min_price_move: 0.05` aligns with the price floor, removing `score_threshold` weakens an explicitly required active gate.
- [ ] **TB-405** `rejected` — Increase spike_min_volume_delta to at least 15000 for this market family, with a separate higher floor for very thin books.
  - **Governor rejection**: TB-XXX violation: the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical no-null relaxation rule and the global hard floor that `score_threshold/spike_score_threshold` must remain explicit and ≥ 2.2. Even though `min_price_move: 0.05` aligns with the price floor, removing `score_threshold` weakens an explicitly required active gate.
- [ ] **TB-406** `rejected` — Keep spike_score_threshold unchanged for now; the errors are driven more by liquidity filters than by combined-score calibration.
  - **Governor rejection**: TB-XXX violation: the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical no-null relaxation rule and the global hard floor that `score_threshold/spike_score_threshold` must remain explicit and ≥ 2.2. Even though `min_price_move: 0.05` aligns with the price floor, removing `score_threshold` weakens an explicitly required active gate.

---

## 2026-06-06 — Advisor snapshot 135

### Summary
The false positives are concentrated in thin-liquidity macro markets where quote churn or a few trades produce large-looking moves without sustained follow-through. Analyst notes repeatedly recommend requiring more real executed volume, more trades, or a larger price move before emitting a spike signal.

### Next step
Raise the detection bar for low-liquidity macro markets by combining a higher minimum price move with a higher minimum trade/volume confirmation requirement, rather than relying on score alone.

### Suggested thresholds
`min_volume_delta` → `10000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-407** `rejected` — Increase min_price_move from 0.03 to 0.05 for thinly traded macro markets.
  - **Governor rejection**: TB-Global floors is violated because the proposed tweak sets score_threshold to None, but the historical constraint requires score_threshold ≥ 2.2 and non-None with no null relaxations. The proposed min_price_move = 0.05 is consistent, but the null score gate conflicts with the explicit floor.
- [ ] **TB-408** `rejected` — Increase min_volume_delta from the current setting to at least 10000 for low-liquidity events where quote-driven churn is common.
  - **Governor rejection**: TB-Global floors is violated because the proposed tweak sets score_threshold to None, but the historical constraint requires score_threshold ≥ 2.2 and non-None with no null relaxations. The proposed min_price_move = 0.05 is consistent, but the null score gate conflicts with the explicit floor.
- [ ] **TB-409** `rejected` — Add a confirmation rule: require sustained movement or multiple confirming trades before signaling, especially when score is only moderately above threshold.
  - **Governor rejection**: TB-Global floors is violated because the proposed tweak sets score_threshold to None, but the historical constraint requires score_threshold ≥ 2.2 and non-None with no null relaxations. The proposed min_price_move = 0.05 is consistent, but the null score gate conflicts with the explicit floor.

---

## 2026-06-06 — Advisor snapshot 136

### Summary
The false positives are concentrated in low-liquidity macro markets where quote-driven or thinly executed moves trigger signals despite weak follow-through. The analyst labels repeatedly ask for more confirmation from real trades or sustained price movement before firing.

### Next step
Raise the price-move and execution-quality bar for macro spikes, especially by requiring both a larger fractional move and stronger executed volume confirmation before emitting a signal.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-410** `rejected` — Increase the minimum price move from 0.03 to 0.05 for macro markets that are thin or quote-heavy.
  - **Governor rejection**: The proposal violates the historical hard-floor rules by setting `min_volume_delta` to `None` and `score_threshold` to `None`. This conflicts with the explicit constraints that `min_volume_delta` / `spike_min_volume_delta` must be non-`None` and meaningful, and that `score_threshold` / `spike_score_threshold` must be explicit and ≥ 2.2. The proposed `min_price_move: 0.05` is consistent with the floor, but the missing execution-quality and score gates would relax previously tightened anti-noise controls.
- [ ] **TB-411** `rejected` — Add an execution-confirmation rule: require either a minimum trade-count floor or a minimum share of executed volume, not just raw volume delta.
  - **Governor rejection**: The proposal violates the historical hard-floor rules by setting `min_volume_delta` to `None` and `score_threshold` to `None`. This conflicts with the explicit constraints that `min_volume_delta` / `spike_min_volume_delta` must be non-`None` and meaningful, and that `score_threshold` / `spike_score_threshold` must be explicit and ≥ 2.2. The proposed `min_price_move: 0.05` is consistent with the floor, but the missing execution-quality and score gates would relax previously tightened anti-noise controls.
- [ ] **TB-412** `rejected` — For low-priced contracts, require sustained movement for at least 1 minute or multiple confirming trades before triggering a signal.
  - **Governor rejection**: The proposal violates the historical hard-floor rules by setting `min_volume_delta` to `None` and `score_threshold` to `None`. This conflicts with the explicit constraints that `min_volume_delta` / `spike_min_volume_delta` must be non-`None` and meaningful, and that `score_threshold` / `spike_score_threshold` must be explicit and ≥ 2.2. The proposed `min_price_move: 0.05` is consistent with the floor, but the missing execution-quality and score gates would relax previously tightened anti-noise controls.

---

## 2026-06-06 — Advisor snapshot 137

### Summary
The false positives cluster around thin or quote-driven macro-market moves: several low-tier alerts have large volume deltas but only ~2% price movement and analyst notes explicitly call out quote churn or thin follow-through. One high-score macro signal still appears informative, so the best fix is to require more executed-trade confirmation rather than broadly tightening score alone.

### Next step
Raise the bar on low-price/illiquid spikes by requiring either a larger executed-volume share or a sustained price move before emission, while keeping the existing score path open for genuinely strong trade-backed moves.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-413** `rejected` — Increase the minimum price move to 0.03 for macro/low-priced markets, since multiple false positives sit at 0.02 while still preserving the 0.09-0.11 signals.
  - **Governor rejection**: The proposal violates the historical hard floor on price movement: TB-001 requires `min_price_move` / `spike_min_price_move` to remain explicit and ≥ 0.05, but the tweak lowers `min_price_move` to 0.03. It also conflicts with the low-liquidity / quote-churn guardrail that says to keep `min_price_move ≥ 0.05` for thin or noisy markets. The change does not relax `min_volume_delta` or `score_threshold`, but the lowered price threshold is a direct regression against the previously tightened floor.
- [ ] **TB-414** `rejected` — Add an execution-quality gate: only emit when a majority of the volume delta comes from executed trades rather than quotes.
  - **Governor rejection**: The proposal violates the historical hard floor on price movement: TB-001 requires `min_price_move` / `spike_min_price_move` to remain explicit and ≥ 0.05, but the tweak lowers `min_price_move` to 0.03. It also conflicts with the low-liquidity / quote-churn guardrail that says to keep `min_price_move ≥ 0.05` for thin or noisy markets. The change does not relax `min_volume_delta` or `score_threshold`, but the lowered price threshold is a direct regression against the previously tightened floor.
- [ ] **TB-415** `rejected` — Keep score threshold unchanged for now; the evidence points more to quote-heavy noise than to an overly permissive combined score.
  - **Governor rejection**: The proposal violates the historical hard floor on price movement: TB-001 requires `min_price_move` / `spike_min_price_move` to remain explicit and ≥ 0.05, but the tweak lowers `min_price_move` to 0.03. It also conflicts with the low-liquidity / quote-churn guardrail that says to keep `min_price_move ≥ 0.05` for thin or noisy markets. The change does not relax `min_volume_delta` or `score_threshold`, but the lowered price threshold is a direct regression against the previously tightened floor.

---

## 2026-06-06 — Advisor snapshot 138

### Summary
The false positives are concentrated in quote-driven or thin-liquidity macro markets where large volume deltas do not reliably translate into sustained price movement. Analyst labels repeatedly flag noise when price change is small or follow-through is weak, while one high-score case with a clearer price move is labeled as a true signal.

### Next step
Tighten the detector to require both a larger executed-volume component and a sustained price move before emitting, rather than relying on raw volume delta alone.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `10.0`

### Recommendations

- [ ] **TB-416** `rejected` — Raise the price move floor to filter quote churn: set spike_min_price_move to 0.05.
  - **Governor rejection**: Yes. The proposal violates the historical hard-floor constraints and anti-relaxation rule: TB-XXX requires `min_volume_delta` to be explicit and non-None, but the new tweak sets `min_volume_delta: None`. It also weakens the volume gate that was explicitly required to suppress quote-driven noise, which conflicts with the rule against substituting `None` for core thresholds.
- [ ] **TB-417** `rejected` — Add a volume-quality rule for illiquid markets: require a higher share of executed trades within the delta, or suppress spikes dominated by quote updates.
  - **Governor rejection**: Yes. The proposal violates the historical hard-floor constraints and anti-relaxation rule: TB-XXX requires `min_volume_delta` to be explicit and non-None, but the new tweak sets `min_volume_delta: None`. It also weakens the volume gate that was explicitly required to suppress quote-driven noise, which conflicts with the rule against substituting `None` for core thresholds.
- [ ] **TB-418** `rejected` — Increase the score cutoff modestly so borderline quote-driven events do not emit unless price confirmation is present.
  - **Governor rejection**: Yes. The proposal violates the historical hard-floor constraints and anti-relaxation rule: TB-XXX requires `min_volume_delta` to be explicit and non-None, but the new tweak sets `min_volume_delta: None`. It also weakens the volume gate that was explicitly required to suppress quote-driven noise, which conflicts with the rule against substituting `None` for core thresholds.

---

## 2026-06-06 — Advisor snapshot 139

### Summary
Recent false positives are dominated by quote-heavy or thin-liquidity bursts with large reported volume deltas but weak confirmation from sustained traded flow or price follow-through. The analyst labels consistently ask for more executed volume and a longer-lived price move before emitting signals.

### Next step
Tighten the detector by requiring both a higher volume floor and a sustained price move confirmation, with the most immediate change being a modest increase to the minimum price-move threshold plus a rule that a larger share of the spike must come from executed trades rather than quotes.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-419** `rejected` — Raise the minimum executed-volume requirement for macro contracts with quote-heavy bursts, especially low-priced markets.
  - **Governor rejection**: TB-global hard floors: the proposed `min_price_move: 0.03` violates the explicit floor requiring `min_price_move >= 0.05` and specifically rejects 0.03–0.04. It also violates the explicit requirement that `min_volume_delta` must be explicit and never `None`, and `score_threshold` must be explicit and `>= 2.2`; setting either to `None` conflicts with those rules.
- [ ] **TB-420** `rejected` — Require price movement to persist for multiple minutes before flagging, instead of accepting a single jump.
  - **Governor rejection**: TB-global hard floors: the proposed `min_price_move: 0.03` violates the explicit floor requiring `min_price_move >= 0.05` and specifically rejects 0.03–0.04. It also violates the explicit requirement that `min_volume_delta` must be explicit and never `None`, and `score_threshold` must be explicit and `>= 2.2`; setting either to `None` conflicts with those rules.
- [ ] **TB-421** `rejected` — Increase the combined score threshold only slightly, since the main failure mode is poor confirmation rather than weak raw scores.
  - **Governor rejection**: TB-global hard floors: the proposed `min_price_move: 0.03` violates the explicit floor requiring `min_price_move >= 0.05` and specifically rejects 0.03–0.04. It also violates the explicit requirement that `min_volume_delta` must be explicit and never `None`, and `score_threshold` must be explicit and `>= 2.2`; setting either to `None` conflicts with those rules.

---

## 2026-06-06 — Advisor snapshot 140

### Summary
The false positives are concentrated in quote-heavy, low-priced macro contracts where large volume deltas are not matched by sustained executed trading or durable price follow-through. Several analyst labels specifically call for stricter confirmation via multi-minute movement or trade imbalance rather than single burst events.

### Next step
Require both a larger executed-volume component and sustained price movement over at least 1 minute before emitting a spike signal.

### Suggested thresholds
`min_volume_delta` → `12000.0`, `min_price_move` → `0.12`

### Recommendations

- [ ] **TB-422** `rejected` — Increase the volume gate for thin macro contracts: raise spike_min_volume_delta to 12000.0.
  - **Governor rejection**: The tweak conflicts with the historical floor on score handling: **score_threshold ≥ 2.2** must remain explicit and cannot be removed or set to null, but the proposal sets `score_threshold: None`. It does not appear to violate the `min_price_move ≥ 0.05` floor because `0.12` is stricter, and `min_volume_delta` remains explicit.
- [ ] **TB-423** `rejected` — Add a price-confirmation floor: raise spike_min_price_move to 0.12 so single-jump quote bursts are less likely to pass.
  - **Governor rejection**: The tweak conflicts with the historical floor on score handling: **score_threshold ≥ 2.2** must remain explicit and cannot be removed or set to null, but the proposal sets `score_threshold: None`. It does not appear to violate the `min_price_move ≥ 0.05` floor because `0.12` is stricter, and `min_volume_delta` remains explicit.
- [ ] **TB-424** `rejected` — If you prefer a softer change, leave thresholds close to current values and raise spike_score_threshold modestly to reduce marginal quote-driven signals.
  - **Governor rejection**: The tweak conflicts with the historical floor on score handling: **score_threshold ≥ 2.2** must remain explicit and cannot be removed or set to null, but the proposal sets `score_threshold: None`. It does not appear to violate the `min_price_move ≥ 0.05` floor because `0.12` is stricter, and `min_volume_delta` remains explicit.

---

## 2026-06-06 — Advisor snapshot 141

### Summary
The false positives cluster around thin, quote-heavy macro contracts where large volume deltas are not accompanied by durable price follow-through. Analyst notes repeatedly point to noisy single-jump behavior, especially in low-priced or illiquid markets.

### Next step
Raise the price-move requirement and add a persistence rule so a spike only emits when the move is sustained for multiple minutes, not just when volume surges once.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-425** `rejected` — Increase spike_min_price_move to 0.05 to filter out 10%–3% one-off jumps that lack follow-through.
  - **Governor rejection**: The proposal violates the historical constraint that min_volume_delta / spike_min_volume_delta must be explicit and must not be set to None. It also violates the global hard floor that score_threshold / spike_score_threshold must be explicit and not set to None. Keeping min_price_move at 0.05 is consistent with the floor, but omitting the other two thresholds conflicts with the tightened historical rules.
- [ ] **TB-426** `rejected` — Require a sustained move over at least 2-3 minutes, or an equivalent multi-bar confirmation, before emitting a spike.
  - **Governor rejection**: The proposal violates the historical constraint that min_volume_delta / spike_min_volume_delta must be explicit and must not be set to None. It also violates the global hard floor that score_threshold / spike_score_threshold must be explicit and not set to None. Keeping min_price_move at 0.05 is consistent with the floor, but omitting the other two thresholds conflicts with the tightened historical rules.
- [ ] **TB-427** `rejected` — For thin markets, require executed-volume confirmation above quote-driven flow, such as at least 60% of the delta coming from trades rather than quotes.
  - **Governor rejection**: The proposal violates the historical constraint that min_volume_delta / spike_min_volume_delta must be explicit and must not be set to None. It also violates the global hard floor that score_threshold / spike_score_threshold must be explicit and not set to None. Keeping min_price_move at 0.05 is consistent with the floor, but omitting the other two thresholds conflicts with the tightened historical rules.

---

## 2026-06-06 — Advisor snapshot 142

### Summary
The false positives are concentrated in thin, quote-driven markets where large apparent volume spikes coincide with weak or brief price movement. Analyst labels repeatedly point to the same fix: require stronger confirmation from sustained traded volume and a larger price move before emitting a signal.

### Next step
Tighten the detector by raising the price-move floor and adding a persistence/quality filter on volume so short quote bursts do not pass as spikes.

### Suggested thresholds
`min_volume_delta` → `12000.0`, `min_price_move` → `0.15`

### Recommendations

- [ ] **TB-428** `rejected` — Raise spike_min_price_move to 0.15 to suppress low-follow-through bursts in thin macro contracts.
  - **Governor rejection**: The proposal violates the historical global score gate by setting `score_threshold: None`, which conflicts with the mandatory requirement that `score_threshold ≥ 2.2` with no null relaxations. It also appears to relax the low-liquidity/wach-tier confirmation framework by relying on a price-move floor of `0.15` and a volume threshold without preserving the explicitly required non-`None` score brake.
- [ ] **TB-429** `rejected` — Increase spike_min_volume_delta to 12000 so only larger expansions clear the trigger in noisy markets.
  - **Governor rejection**: The proposal violates the historical global score gate by setting `score_threshold: None`, which conflicts with the mandatory requirement that `score_threshold ≥ 2.2` with no null relaxations. It also appears to relax the low-liquidity/wach-tier confirmation framework by relying on a price-move floor of `0.15` and a volume threshold without preserving the explicitly required non-`None` score brake.
- [ ] **TB-430** `rejected` — Add a rule that at least 1.5x baseline volume must persist for multiple minutes, or require executed-trade volume to dominate quote-driven delta.
  - **Governor rejection**: The proposal violates the historical global score gate by setting `score_threshold: None`, which conflicts with the mandatory requirement that `score_threshold ≥ 2.2` with no null relaxations. It also appears to relax the low-liquidity/wach-tier confirmation framework by relying on a price-move floor of `0.15` and a volume threshold without preserving the explicitly required non-`None` score brake.

---

## 2026-06-06 — Advisor snapshot 143

### Summary
Recent false positives are concentrated in thin, quote-driven macro markets where small price drift or single-burst volume changes are being misclassified as spikes. Analyst notes consistently call for stronger confirmation from executed trades, sustained multi-minute movement, and higher relative volume before emission.

### Next step
Tighten the detector with a modest price-move floor plus a higher volume requirement, and add a confirmation rule requiring sustained traded activity on the same side before a spike can emit.

### Suggested thresholds
`min_volume_delta` → `30000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-431** `rejected` — Raise spike_min_price_move to 0.05 for low-liquidity macro contracts so small 2%-3% drifts do not trigger.
  - **Governor rejection**: TB-global-score-gate is violated: the proposed tweak sets `score_threshold` / `spike_score_threshold` to `None`, but the historical constraint explicitly requires this gate to remain explicit and >= 2.2, and forbids `None`.
- [ ] **TB-432** `rejected` — Raise spike_min_volume_delta to 1.5x current baseline-equivalent behavior by requiring a clearly larger executed-volume burst rather than quote-heavy flow.
  - **Governor rejection**: TB-global-score-gate is violated: the proposed tweak sets `score_threshold` / `spike_score_threshold` to `None`, but the historical constraint explicitly requires this gate to remain explicit and >= 2.2, and forbids `None`.
- [ ] **TB-433** `rejected` — Require at least one confirmed same-side trade burst over multiple minutes before emitting, and increase spike_score_threshold slightly only if you need an additional global brake.
  - **Governor rejection**: TB-global-score-gate is violated: the proposed tweak sets `score_threshold` / `spike_score_threshold` to `None`, but the historical constraint explicitly requires this gate to remain explicit and >= 2.2, and forbids `None`.

---

## 2026-06-06 — Advisor snapshot 144

### Summary
The false positives are coming from thin macro markets where quote/volume bursts trigger signals without enough sustained price follow-through or executed trade imbalance. Analyst labels consistently ask for stronger confirmation from multi-minute price movement and traded volume rather than one-off spikes.

### Next step
Tighten the detector by requiring both a larger sustained price move and stronger executed-volume confirmation before emitting, especially for low-priced macro contracts.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-434** `rejected` — Raise the minimum price move to 0.05 to filter out shallow drift in thin markets.
  - **Governor rejection**: TB-Global-Score: the proposed tweak sets score_threshold to None, which violates the historical hard floor that score_threshold must be explicit and >= 2.2. The other proposed thresholds (min_price_move 0.05 and min_volume_delta 15000.0) do not conflict with the listed floor/gating constraints.
- [ ] **TB-435** `rejected` — Raise the minimum volume delta to 15000 to avoid quote-heavy bursts with weak follow-through.
  - **Governor rejection**: TB-Global-Score: the proposed tweak sets score_threshold to None, which violates the historical hard floor that score_threshold must be explicit and >= 2.2. The other proposed thresholds (min_price_move 0.05 and min_volume_delta 15000.0) do not conflict with the listed floor/gating constraints.
- [ ] **TB-436** `rejected` — Add or effectively enforce a higher score gate so signals need both volume and price confirmation, not either one alone.
  - **Governor rejection**: TB-Global-Score: the proposed tweak sets score_threshold to None, which violates the historical hard floor that score_threshold must be explicit and >= 2.2. The other proposed thresholds (min_price_move 0.05 and min_volume_delta 15000.0) do not conflict with the listed floor/gating constraints.

---

## 2026-06-06 — Advisor snapshot 145

### Summary
The false positives cluster in thin, low-liquidity macro contracts where quote-heavy or one-off bursts produce only small follow-through, so the detector is firing on activity without enough confirmed directional movement. Analyst labels consistently recommend requiring sustained trade imbalance, confirmed executed volume, and a larger price move before emitting alerts.

### Next step
Raise the price-move floor and require either a stronger executed-volume burst or a sustained multi-minute directional move before signaling, rather than treating quote-heavy bursts as spikes.

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-437** `rejected` — Increase spike_min_price_move from 0.03 to 0.05 to suppress flat or near-flat quote drift.
  - **Governor rejection**: TB-XXX: The proposed tweak explicitly sets score_threshold to None, which violates the historical score gate requirement to keep score_threshold/spike_score_threshold explicit and ≥ 2.2, and the no-null-relaxations rule. The new min_price_move = 0.05 is consistent, but the None score threshold is a direct regression.
- [ ] **TB-438** `rejected` — Increase spike_min_volume_delta from about 10k-20k to at least 25k for low-liquidity macro markets, or gate on executed volume rather than quote updates.
  - **Governor rejection**: TB-XXX: The proposed tweak explicitly sets score_threshold to None, which violates the historical score gate requirement to keep score_threshold/spike_score_threshold explicit and ≥ 2.2, and the no-null-relaxations rule. The new min_price_move = 0.05 is consistent, but the None score threshold is a direct regression.
- [ ] **TB-439** `rejected` — Add a persistence rule: require the move to hold for multiple minutes or be supported by same-side trade imbalance before emitting, instead of a single burst.
  - **Governor rejection**: TB-XXX: The proposed tweak explicitly sets score_threshold to None, which violates the historical score gate requirement to keep score_threshold/spike_score_threshold explicit and ≥ 2.2, and the no-null-relaxations rule. The new min_price_move = 0.05 is consistent, but the None score threshold is a direct regression.

---

## 2026-06-06 — Advisor snapshot 146

### Summary
The false positives cluster around low-liquidity macro contracts with quote-heavy or brief volume bursts, where price moves are small or not sustained enough to be informative. Analysts repeatedly ask for stronger confirmation from executed volume, same-side trade follow-through, and multi-minute price persistence before firing.

### Next step
Raise the detector to require both a larger volume delta and a sustained price move, with an execution-confirmation rule for thin markets; the cleanest single change is to increase spike_min_price_move and add a trade-follow-through gate.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`

### Recommendations

- [x] **TB-440** `applied` — Increase spike_min_price_move to 0.05 to filter out 2–3% drift and quote noise in thin macro markets.
- [x] **TB-441** `applied` — Increase spike_min_volume_delta to 15000 so low-priced contracts need a clearer burst above baseline before alerting.
- [x] **TB-442** `applied` — Require at least 2 same-side executed trades above the spread within the detection window for watch/notable emits in low-liquidity markets.

---

## 2026-06-06 — Advisor snapshot 147

### Summary
The false positives cluster in thin, low-liquidity macro markets where quote-heavy bursts and small price drifts are being treated as spikes. The analyst labels repeatedly ask for more emphasis on executed trades, sustained multi-minute movement, and larger relative volume jumps.

### Next step
Add a sustain-and-execution gate: require either confirmed executed volume above baseline or a multi-minute directional price move before emitting, rather than reacting to one-off quote/price bursts.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-443** `rejected` — Raise spike_min_price_move to 0.05 to suppress 2%–3% drift noise in low-priced macro contracts.
  - **Governor rejection**: TB-001 / Global hard floors is violated because `score_threshold` is set to `None`, which removes the explicitly required score gate. TB-003 / Score gate is also violated for the same reason: the historical constraint requires an explicit score threshold and forbids null relaxations. The other suggested thresholds (`min_price_move: 0.05`, explicit `min_volume_delta: 15000.0`) do not conflict with the stated floors.
- [ ] **TB-444** `rejected` — Raise spike_min_volume_delta to 15000 to filter quote-heavy bursts that do not produce follow-through.
  - **Governor rejection**: TB-001 / Global hard floors is violated because `score_threshold` is set to `None`, which removes the explicitly required score gate. TB-003 / Score gate is also violated for the same reason: the historical constraint requires an explicit score threshold and forbids null relaxations. The other suggested thresholds (`min_price_move: 0.05`, explicit `min_volume_delta: 15000.0`) do not conflict with the stated floors.
- [ ] **TB-445** `rejected` — Keep spike_score_threshold unchanged for now; the better fix is a stricter pre-emission rule requiring sustained price movement or confirmed same-side trades.
  - **Governor rejection**: TB-001 / Global hard floors is violated because `score_threshold` is set to `None`, which removes the explicitly required score gate. TB-003 / Score gate is also violated for the same reason: the historical constraint requires an explicit score threshold and forbids null relaxations. The other suggested thresholds (`min_price_move: 0.05`, explicit `min_volume_delta: 15000.0`) do not conflict with the stated floors.

---

## 2026-06-06 — Advisor snapshot 148

### Summary
The false positives are concentrated in thin macro markets where quote-only or low-liquidity activity produces small price drifts and repeat alerts without executed-trade confirmation. The analyst labels consistently ask for stronger sustained movement or a real trade imbalance before signaling.

### Next step
Raise the price-move floor and require executed-trade confirmation for low-liquidity macro markets, rather than relying on quote-driven volume bursts alone.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`

### Recommendations

- [x] **TB-446** `applied` — Increase spike_min_price_move to 0.05 to suppress 3% quote-driven moves that were repeatedly labeled noise.
- [x] **TB-447** `applied` — Increase spike_min_volume_delta to 20000.0 so one-off quote bursts around ~10k-19k do not trigger alerts by themselves.
- [x] **TB-448** `applied` — Add a rule that a signal only emits when there is at least one confirmed executed trade or sustained multi-minute price movement; keep the score threshold unchanged for now.

---

## 2026-06-06 — Advisor snapshot 149

### Summary
The false positives are concentrated in low-liquidity macro markets where quote-only or lightly traded activity produces small 2–3% price moves with large volume deltas but no confirmed trade imbalance. Analyst labels consistently ask for stronger sustained price movement or executed-trade confirmation before emitting a signal.

### Next step
Raise the price-move requirement and pair it with a stronger executed-trade filter for low-liquidity markets, rather than relying on volume bursts alone.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-449** `rejected` — Increase the minimum price move to 0.05 for watch-tier macro spikes.
  - **Governor rejection**: The proposed tweak violates the historical hard floor that `min_volume_delta` must be explicit/non-`None`; setting `min_volume_delta: None` conflicts with the global hard floor. It also conflicts with the watch-tier/low-liquidity constraints that require an active `score_threshold` and no `None` relaxations, so `score_threshold: None` is disallowed. The `min_price_move: 0.05` value is consistent, but the proposal still relaxes two explicitly hardened TB rules.
- [ ] **TB-450** `rejected` — Require at least one confirmed executed trade on the same side before emitting a signal.
  - **Governor rejection**: The proposed tweak violates the historical hard floor that `min_volume_delta` must be explicit/non-`None`; setting `min_volume_delta: None` conflicts with the global hard floor. It also conflicts with the watch-tier/low-liquidity constraints that require an active `score_threshold` and no `None` relaxations, so `score_threshold: None` is disallowed. The `min_price_move: 0.05` value is consistent, but the proposal still relaxes two explicitly hardened TB rules.
- [ ] **TB-451** `rejected` — For low-priced or thin markets, require a sustained multi-minute move or repeated same-side prints instead of a one-off quote jump.
  - **Governor rejection**: The proposed tweak violates the historical hard floor that `min_volume_delta` must be explicit/non-`None`; setting `min_volume_delta: None` conflicts with the global hard floor. It also conflicts with the watch-tier/low-liquidity constraints that require an active `score_threshold` and no `None` relaxations, so `score_threshold: None` is disallowed. The `min_price_move: 0.05` value is consistent, but the proposal still relaxes two explicitly hardened TB rules.

---

## 2026-06-06 — Advisor snapshot 150

### Summary
The false positives are concentrated in low-liquidity macro markets where small price moves and quote-driven activity are being scored as spikes despite limited executed-trade confirmation. Analyst notes consistently ask for stronger volume confirmation and sustained multi-interval price movement before triggering.

### Next step
Tighten the detector to require both a larger traded-volume burst and a confirmed price move, with special emphasis on executed-trade confirmation rather than quote-only drift.

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.05`, `score_threshold` → `5.0`

### Recommendations

- [x] **TB-452** `applied` — Raise the minimum traded-volume requirement to filter out quote-only spikes in thin macro markets.
- [x] **TB-453** `applied` — Increase the minimum price-move threshold slightly so 2% to 3% drift does not trigger unless backed by real volume.
- [x] **TB-454** `applied` — Add a persistence rule: require sustained movement or repeated same-side prints across multiple intervals before emitting a signal.

---

## 2026-06-06 — Advisor snapshot 151

### Summary
The false positives are concentrated in thin, low-liquidity macro markets where quote-driven moves and repeated updates are being mistaken for real spikes. Analyst notes consistently ask for stronger confirmation from executed volume and sustained multi-interval price movement rather than single-interval quote bursts.

### Next step
Raise the minimum volume-delta requirement and add a confirmation rule that requires either executed trades or sustained price movement across multiple intervals before emitting a spike.

### Suggested thresholds
`min_volume_delta` → `30000.0`, `min_price_move` → `0.05`, `score_threshold` → `8.0`

### Recommendations

- [x] **TB-455** `applied` — Increase spike_min_volume_delta to 30000 to filter out quote-only bursts in CPI/GDP-like markets.
- [x] **TB-456** `applied` — Increase spike_min_price_move to 0.05 so sub-5% moves are not flagged unless volume confirmation is strong.
- [x] **TB-457** `applied` — Raise spike_score_threshold modestly to 8.0 to suppress low-confidence watch-tier signals without blocking the stronger notable cases.

---

## 2026-06-06 — Advisor snapshot 152

### Summary
The false positives are concentrated in low-liquidity, quote-driven, or single-print bursts where volume jumps or small price moves do not reflect sustained traded participation. Analyst labels repeatedly ask for stronger confirmation from executed volume, multi-interval persistence, or larger price movement before emission.

### Next step
Raise the spike detector’s confirmation bar: require both a larger traded-volume delta and a slightly larger price move before emitting, with an explicit guard against quote-only or single-print activity.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-458** `rejected` — Increase the minimum traded-volume delta materially for macro/event markets where alerts are currently firing on quote updates or low trade count.
  - **Governor rejection**: TB-XXX violation: the proposed tweak sets score_threshold to None, which conflicts with the historical constraint that score_threshold / spike_score_threshold must be explicit and >= 2.2, never None. The new min_price_move = 0.05 does not conflict, and min_volume_delta = 50000.0 is explicit, but the null score gate is a regression toward a blanket relaxation.
- [ ] **TB-459** `rejected` — Raise the minimum price move so sub-5% moves do not trigger unless there is clear executed-volume confirmation.
  - **Governor rejection**: TB-XXX violation: the proposed tweak sets score_threshold to None, which conflicts with the historical constraint that score_threshold / spike_score_threshold must be explicit and >= 2.2, never None. The new min_price_move = 0.05 does not conflict, and min_volume_delta = 50000.0 is explicit, but the null score gate is a regression toward a blanket relaxation.
- [ ] **TB-460** `rejected` — Add a persistence rule requiring the move to hold across multiple intervals or repeated same-side prints above the spread before the signal can emit.
  - **Governor rejection**: TB-XXX violation: the proposed tweak sets score_threshold to None, which conflicts with the historical constraint that score_threshold / spike_score_threshold must be explicit and >= 2.2, never None. The new min_price_move = 0.05 does not conflict, and min_volume_delta = 50000.0 is explicit, but the null score gate is a regression toward a blanket relaxation.

---

## 2026-06-06 — Advisor snapshot 153

### Summary
The false positives are concentrated in low-liquidity or quote-driven spikes where volume changes and small price moves are enough to trigger alerts, especially in political and CPI/Fed markets. The analyst labels consistently favor requiring stronger confirmation from executed trades, sustained movement, or broader participation before emitting a signal.

### Next step
Raise the volume gate and add a stronger price-confirmation rule for low-liquidity markets, with sustained multi-interval or executed-trade confirmation before emitting a spike.

### Suggested thresholds
`min_volume_delta` → `300.0`, `min_price_move` → `0.05`, `score_threshold` → `45.0`

### Recommendations

- [x] **TB-461** `applied` — Increase spike_min_volume_delta to at least 300 for low-liquidity event markets to suppress single-print bursts.
- [x] **TB-462** `applied` — Increase spike_min_price_move to 0.05 so sub-5% quote-only moves do not trigger alerts on their own.
- [x] **TB-463** `applied` — Raise spike_score_threshold modestly to 45 to force stronger combined confirmation before emission.

---

## 2026-06-06 — Advisor snapshot 154

### Summary
The false positives cluster around quote-driven or low-liquidity spikes where volume jumps but the price move is still small or unconfirmed. The pattern suggests the detector is too sensitive to volume-only bursts and needs stronger confirmation from price and executed trades.

### Next step
Raise the price-move floor and require confirmation from executed trading activity, not quote changes alone; the cleanest single adjustment is to tighten both volume and price gates before score aggregation.

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-464** `rejected` — Increase spike_min_price_move to 0.05 to suppress sub-5% quote-only moves that repeatedly labeled as noise.
  - **Governor rejection**: TB-003 is violated because the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical hard score gate requiring `score_threshold ≥ 2.2` and explicitly non-null. The other thresholds (`min_price_move: 0.05`, explicit `min_volume_delta`) are consistent with the historical constraints.
- [ ] **TB-465** `rejected` — Raise spike_min_volume_delta to 25000 to avoid triggering on single-print or low-liquidity bursts that still produce large relative deltas.
  - **Governor rejection**: TB-003 is violated because the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical hard score gate requiring `score_threshold ≥ 2.2` and explicitly non-null. The other thresholds (`min_price_move: 0.05`, explicit `min_volume_delta`) are consistent with the historical constraints.
- [ ] **TB-466** `rejected` — Add a rule that volume spikes must be confirmed by executed trades or persistence across multiple intervals before emitting a signal.
  - **Governor rejection**: TB-003 is violated because the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical hard score gate requiring `score_threshold ≥ 2.2` and explicitly non-null. The other thresholds (`min_price_move: 0.05`, explicit `min_volume_delta`) are consistent with the historical constraints.

---

## 2026-06-06 — Advisor snapshot 155

### Summary
The false positives are concentrated in quote-driven or low-liquidity bursts where volume spikes are large but price move is small or unconfirmed, especially in political event and CPI markets. The analyst labels consistently ask for a higher volume confirmation and a larger sustained price move before emitting a signal.

### Next step
Increase the volume threshold first, and pair it with a modestly higher price-move floor so single-print or quote-only bursts do not pass unless they show confirmed traded movement.

### Suggested thresholds
`min_volume_delta` → `30000.0`, `min_price_move` → `0.05`

### Recommendations

- [x] **TB-467** `applied` — Raise spike_min_volume_delta to about 30000 for low-liquidity/event-style markets.
- [x] **TB-468** `applied` — Raise spike_min_price_move to 0.05 to require at least a 5% move before flagging borderline bursts.
- [x] **TB-469** `applied` — Keep spike_score_threshold unchanged unless you still see quote-only alerts after the first two changes; if so, lift it slightly to suppress low-confidence emissions.

---

## 2026-06-06 — Advisor snapshot 156

### Summary
The false positives are driven by quote-led or single-print price flickers that look large on price but lack convincing traded-volume confirmation. Low-liquidity markets also need a stricter filter because small bursts can trigger high scores without sustained participation.

### Next step
Raise the detector’s traded-volume requirement and make price movement pass only when it is both larger and sustained, so quote-only flickers and one-off prints do not emit signals.

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-470** `rejected` — Increase spike_min_volume_delta to require clearer traded-volume confirmation before emitting.
  - **Governor rejection**: TB-001 / Global hard floors and TB-010 / No null relaxations are violated because `score_threshold` is explicitly set to `None`, but historical constraints require `score_threshold/spike_score_threshold ≥ 2.2` and non-`None`, and never allow `score_threshold` to be `None`.
- [ ] **TB-471** `rejected` — Increase spike_min_price_move modestly for low-liquidity event markets so small quote-driven moves do not qualify.
  - **Governor rejection**: TB-001 / Global hard floors and TB-010 / No null relaxations are violated because `score_threshold` is explicitly set to `None`, but historical constraints require `score_threshold/spike_score_threshold ≥ 2.2` and non-`None`, and never allow `score_threshold` to be `None`.
- [ ] **TB-472** `rejected` — Add a persistence rule: require the move to hold across multiple intervals or include two-sided participation before scoring above threshold.
  - **Governor rejection**: TB-001 / Global hard floors and TB-010 / No null relaxations are violated because `score_threshold` is explicitly set to `None`, but historical constraints require `score_threshold/spike_score_threshold ≥ 2.2` and non-`None`, and never allow `score_threshold` to be `None`.

---

## 2026-06-06 — Advisor snapshot 157

### Summary
The false positives are dominated by quote-driven or low-liquidity flickers that show modest price movement without enough confirmed traded volume or sustained follow-through. Analyst labels consistently ask for stronger volume confirmation and a larger or multi-interval price move before emitting a spike signal.

### Next step
Raise the detector’s minimum volume delta and require either a larger price move or persistence across multiple intervals so quote-only changes do not trigger spikes.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-473** `rejected` — Increase spike_min_volume_delta to filter out low-liquidity single-print bursts.
  - **Governor rejection**: The proposed tweak violates the historical hard-floor constraint that `score_threshold ≥ 2.2` with no `None` relaxations. Setting `score_threshold` to `None` is an explicit relaxation that conflicts with the previously enforced anti-noise rule and the global hard floors.
- [ ] **TB-474** `rejected` — Raise spike_min_price_move slightly so a spike needs a more meaningful sustained move, not a brief quote flicker.
  - **Governor rejection**: The proposed tweak violates the historical hard-floor constraint that `score_threshold ≥ 2.2` with no `None` relaxations. Setting `score_threshold` to `None` is an explicit relaxation that conflicts with the previously enforced anti-noise rule and the global hard floors.
- [ ] **TB-475** `rejected` — Add a persistence rule: require the price move to hold across multiple intervals before emitting a signal.
  - **Governor rejection**: The proposed tweak violates the historical hard-floor constraint that `score_threshold ≥ 2.2` with no `None` relaxations. Setting `score_threshold` to `None` is an explicit relaxation that conflicts with the previously enforced anti-noise rule and the global hard floors.

---

## 2026-06-06 — Advisor snapshot 158

### Summary
The false positives cluster around low-liquidity, quote-driven spikes where price moves are small or unstable and analyst notes repeatedly ask for confirmation from real traded volume. Several signals were flagged despite only modest price movement, so the detector is too sensitive to noise in thin markets.

### Next step
Raise the minimum volume delta and add a slightly higher minimum price move so only traded, sustained moves emit signals; keep the score threshold unchanged for now.

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-476** `rejected` — Increase spike_min_volume_delta to about 25,000 to filter out low-liquidity bursts and quote-only flickers.
  - **Governor rejection**: Yes. The proposed `min_price_move: 0.04` conflicts with the historical floor `min_price_move ≥ 0.05` and specifically violates the low-liquidity / high-odds / watch / notable / thin-market hardening rule that says not to relax into `0.03–0.04`. The `score_threshold: None` also conflicts with the global score-gating constraint that it must remain explicit and non-`None` with `score_threshold ≥ 2.2`. Raising `min_volume_delta` is not the conflict; the conflict is the relaxed price floor and removal of score gating.
- [ ] **TB-477** `rejected` — Increase spike_min_price_move to about 0.04 so sub-4% moves do not trigger without stronger confirmation.
  - **Governor rejection**: Yes. The proposed `min_price_move: 0.04` conflicts with the historical floor `min_price_move ≥ 0.05` and specifically violates the low-liquidity / high-odds / watch / notable / thin-market hardening rule that says not to relax into `0.03–0.04`. The `score_threshold: None` also conflicts with the global score-gating constraint that it must remain explicit and non-`None` with `score_threshold ≥ 2.2`. Raising `min_volume_delta` is not the conflict; the conflict is the relaxed price floor and removal of score gating.
- [ ] **TB-478** `rejected` — Require either confirmed traded volume or persistence across multiple intervals before emitting, especially in macro and political event markets.
  - **Governor rejection**: Yes. The proposed `min_price_move: 0.04` conflicts with the historical floor `min_price_move ≥ 0.05` and specifically violates the low-liquidity / high-odds / watch / notable / thin-market hardening rule that says not to relax into `0.03–0.04`. The `score_threshold: None` also conflicts with the global score-gating constraint that it must remain explicit and non-`None` with `score_threshold ≥ 2.2`. Raising `min_volume_delta` is not the conflict; the conflict is the relaxed price floor and removal of score gating.

---

## 2026-06-06 — Advisor snapshot 159

### Summary
The false positives cluster around quote-driven or single-print price jumps in low-liquidity markets, where price moves are too small or too fleeting to confirm with real executed flow. Analyst notes repeatedly ask for stronger volume confirmation and a sustained move before emitting a signal.

### Next step
Raise the volume requirement first, and pair it with a slightly higher minimum price move so low-liquidity quote flickers do not pass even if they briefly score well.

### Suggested thresholds
`min_price_move` → `0.04`

### Recommendations

- [ ] **TB-479** `rejected` — Increase the minimum sustained-volume requirement for CPI and political event markets to filter out quote-only bursts.
  - **Governor rejection**: The tweak violates the historical global floor that `min_price_move ≥ 0.05` and appears to relax it to `0.04`. It also violates the no-null rules by setting `min_volume_delta: None` and `score_threshold: None`, despite the historical constraints requiring `min_volume_delta` to be explicit/non-None and `score_threshold ≥ 2.2` with no null relaxations. This conflicts with the stricter low-liquidity/watch/series rules that require stronger volume confirmation and trade-backed persistence rather than quote-only flickers.
- [ ] **TB-480** `rejected` — Require a larger price move before flagging low-liquidity markets as actionable, especially when executed flow is thin.
  - **Governor rejection**: The tweak violates the historical global floor that `min_price_move ≥ 0.05` and appears to relax it to `0.04`. It also violates the no-null rules by setting `min_volume_delta: None` and `score_threshold: None`, despite the historical constraints requiring `min_volume_delta` to be explicit/non-None and `score_threshold ≥ 2.2` with no null relaxations. This conflicts with the stricter low-liquidity/watch/series rules that require stronger volume confirmation and trade-backed persistence rather than quote-only flickers.
- [ ] **TB-481** `rejected` — Add a confirmation rule that the move must be sustained by actual trade prints or two-sided participation, not just a transient quote spike.
  - **Governor rejection**: The tweak violates the historical global floor that `min_price_move ≥ 0.05` and appears to relax it to `0.04`. It also violates the no-null rules by setting `min_volume_delta: None` and `score_threshold: None`, despite the historical constraints requiring `min_volume_delta` to be explicit/non-None and `score_threshold ≥ 2.2` with no null relaxations. This conflicts with the stricter low-liquidity/watch/series rules that require stronger volume confirmation and trade-backed persistence rather than quote-only flickers.

---

## 2026-06-06 — Advisor snapshot 160

### Summary
The false positives cluster around quote-only or low-confirmation moves in low-liquidity CPI markets: several alerts had small price changes and analysts explicitly asked for more sustained traded volume or a larger move. The detector is currently too sensitive to brief price flickers unless they are backed by real execution flow.

### Next step
Raise the volume gate first and add a stronger price-confirmation rule for low-liquidity macro markets, so only moves with both executed flow and meaningful displacement emit signals.

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.05`, `score_threshold` → `4.0`

### Recommendations

- [x] **TB-482** `applied` — Increase spike_min_volume_delta to filter out quote-driven jumps with little executed flow.
- [x] **TB-483** `applied` — Increase spike_min_price_move so small 2% moves do not trigger unless volume is exceptionally strong.
- [x] **TB-484** `applied` — Increase spike_score_threshold modestly to suppress borderline alerts that lack sustained confirmation.

---

## 2026-06-06 — Advisor snapshot 161

### Summary
The false positives are concentrated in low-liquidity CPI markets where quote-driven price flickers and weak or non-executed volume are being promoted as spikes. Analyst notes repeatedly ask for both a larger price move and real traded volume before emitting a signal.

### Next step
Tighten the detector with a joint gate: require both higher executed volume and a larger sustained price move before the score can trigger, rather than relying on score alone.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-485** `rejected` — Raise the minimum executed volume requirement for CPI-style markets to around 20,000.
  - **Governor rejection**: Yes — the proposal violates the historical hard floor that `score_threshold` must be explicit/non-`None` and at least 2.2. Setting `score_threshold: None` conflicts with the active hard floors and the no-null-relaxations rule. The tightened `min_price_move: 0.05` is consistent, but the null score threshold is not.
- [ ] **TB-486** `rejected` — Raise the minimum price-move threshold to around 0.05 so 2%–4% quote flickers do not trigger.
  - **Governor rejection**: Yes — the proposal violates the historical hard floor that `score_threshold` must be explicit/non-`None` and at least 2.2. Setting `score_threshold: None` conflicts with the active hard floors and the no-null-relaxations rule. The tightened `min_price_move: 0.05` is consistent, but the null score threshold is not.
- [ ] **TB-487** `rejected` — Keep the score threshold as a secondary filter, but do not let it override missing trade prints or low sustained volume.
  - **Governor rejection**: Yes — the proposal violates the historical hard floor that `score_threshold` must be explicit/non-`None` and at least 2.2. Setting `score_threshold: None` conflicts with the active hard floors and the no-null-relaxations rule. The tightened `min_price_move: 0.05` is consistent, but the null score threshold is not.

---

## 2026-06-06 — Advisor snapshot 162

### Summary
The false positives are concentrated in low-liquidity CPI markets where quote-driven price jumps and shallow volume deltas are being mistaken for actionable spikes. Analyst notes repeatedly ask for stronger trade confirmation, especially non-zero executed volume and a larger sustained price move.

### Next step
Tighten the detector by requiring both a higher minimum executed volume delta and a larger minimum price move before a signal can pass the score gate.

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.05`

### Recommendations

- [x] **TB-488** `applied` — Increase the volume floor for CPI-style markets so quote-only jumps do not trigger on their own.
- [x] **TB-489** `applied` — Raise the minimum price-move requirement for watch-tier spikes from ~2% to a clearly sustained move.
- [x] **TB-490** `applied` — Keep the score threshold as a secondary filter, but make trade-prints/ executed volume mandatory for emission.

---

## 2026-06-06 — Advisor snapshot 163

### Summary
The false positives are driven by quote-led price jumps that lack enough executed volume, especially in CPI-linked markets. The analyst labels consistently favor requiring stronger confirmation from both price move and volume before emitting a spike.

### Next step
Tighten the trigger so a spike requires a larger price move and non-zero executed volume, with CPI-specific minimum sustained-volume filtering if possible.

### Recommendations

- [x] **TB-491** `applied` — Raise the minimum executed volume delta above the current floor so quote-only jumps do not trigger.
- [x] **TB-492** `applied` — Increase the minimum price move threshold for CPI-style markets to filter small impulse moves.
- [x] **TB-493** `applied` — Add a rule that suppresses signals unless both volume delta and price move clear their respective minimums.

---

## 2026-06-06 — Advisor snapshot 164

### Summary
The false positives are dominated by thin-market, quote-only price jumps that produce meaningful-looking price deltas without executed volume. Both analyst labels point to the same issue: require stronger confirmation from real traded volume and/or a larger move before emitting.

### Next step
Raise the trigger bar for thin CPI-style markets by requiring both non-zero executed volume and a higher minimum price move before scoring can pass threshold.

### Suggested thresholds
`min_volume_delta` → `1.0`, `min_price_move` → `0.08`, `score_threshold` → `5.5`

### Recommendations

- [x] **TB-494** `applied` — Increase the price-move floor for this market type to cut quote-only jumps.
- [x] **TB-495** `applied` — Add a hard non-zero executed-volume requirement so price-only moves do not trigger.
- [x] **TB-496** `applied` — If you keep the current score model, raise the score threshold modestly to suppress marginal alerts.

---

## 2026-06-06 — Advisor snapshot 165

### Summary
The false positives are concentrated in thin, low-liquidity CPI-style markets where quote-driven price moves are being flagged without enough traded-volume confirmation. The analyst notes consistently recommend requiring either real executed volume or a larger sustained price move before emitting a spike.

### Next step
Tighten the detector by requiring both a higher minimum price move and a stronger trade-confirmation gate for low-liquidity markets; the clearest concrete change is to raise the price-move floor and add a volume/exec-trade confirmation requirement rather than relying on score alone.

### Suggested thresholds
`min_price_move` → `0.07`

### Recommendations

- [x] **TB-497** `applied` — Raise spike_min_price_move from 0.03 to 0.07 for thin macro/CPI markets to suppress quote-only blips.
- [x] **TB-498** `applied` — Add a hard trade-confirmation gate: do not emit unless executed-trade volume or order-book depth confirms the move.
- [x] **TB-499** `applied` — Keep spike_score_threshold unchanged for now; the labels point more strongly to a missing confirmation filter than to a broadly too-low composite score.

---

## 2026-06-06 — Advisor snapshot 166

### Summary
The false positives cluster in thin, quote-driven CPI markets where modest price moves are being emitted without strong trade confirmation. Analyst labels repeatedly point to noise/unclear cases when volume or trade evidence is weak, even when the score is moderate to high.

### Next step
Tighten the detector for this market family by requiring stronger execution confirmation before emitting a spike, rather than relying on quote-only price moves.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.07`

### Recommendations

- [ ] **TB-500** `rejected` — Raise the minimum price move from 0.03 to 0.07 for CPI watch-tier alerts so small quote-driven moves do not trigger signals.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets `score_threshold: None`, but the historical global hard floors require `score_threshold ≥ 2.2` and explicit/non-`None` at all times. No other listed threshold is relaxed, but leaving `score_threshold` unset conflicts directly with the hard floor.
- [ ] **TB-501** `rejected` — Raise the minimum volume delta from 10000 to 20000 to better distinguish real traded spikes from thin-liquidity noise.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets `score_threshold: None`, but the historical global hard floors require `score_threshold ≥ 2.2` and explicit/non-`None` at all times. No other listed threshold is relaxed, but leaving `score_threshold` unset conflicts directly with the hard floor.
- [ ] **TB-502** `rejected` — Keep the score threshold unchanged for now and gate on trade-confirmation depth instead, since the current errors look more like missing execution confirmation than weak scoring.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets `score_threshold: None`, but the historical global hard floors require `score_threshold ≥ 2.2` and explicit/non-`None` at all times. No other listed threshold is relaxed, but leaving `score_threshold` unset conflicts directly with the hard floor.

---

## 2026-06-06 — Advisor snapshot 167

### Summary
The false positives are concentrated in thin, quote-driven macro markets where small or modest price moves are being flagged without enough trade confirmation. The analyst notes consistently call for stronger volume/trade confirmation and a larger sustained move before emitting a signal.

### Next step
Tighten the detector to require both a larger price move and stronger execution confirmation in low-liquidity markets, rather than relying on volume delta alone.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-503** `rejected` — Raise the minimum price move from 0.03 to 0.05 to filter out marginal quote-driven spikes.
  - **Governor rejection**: TB-003 is violated because `score_threshold` is set to `None`, which explicitly relaxes the historical requirement that `score_threshold` / `spike_score_threshold` remain explicit and ≥ 2.2. This conflicts with the prior rejection of any `None` relaxation for the score gate.
- [ ] **TB-504** `rejected` — Increase the minimum volume delta from 10,000 to 20,000 so only materially larger flow triggers alerts.
  - **Governor rejection**: TB-003 is violated because `score_threshold` is set to `None`, which explicitly relaxes the historical requirement that `score_threshold` / `spike_score_threshold` remain explicit and ≥ 2.2. This conflicts with the prior rejection of any `None` relaxation for the score gate.
- [ ] **TB-505** `rejected` — Add a trade-confirmation rule for watch-tier alerts: require executed-trade evidence or sustained volume acceleration before emitting a signal.
  - **Governor rejection**: TB-003 is violated because `score_threshold` is set to `None`, which explicitly relaxes the historical requirement that `score_threshold` / `spike_score_threshold` remain explicit and ≥ 2.2. This conflicts with the prior rejection of any `None` relaxation for the score gate.

---

## 2026-06-06 — Advisor snapshot 168

### Summary
The false positives are concentrated in thin, quote-driven macro markets where small price moves and large-looking volume deltas are still being labeled as noise or unclear. The common failure mode is reacting to brief, unconfirmed moves without enough sustained trade confirmation.

### Next step
Tighten the detector to require both a larger sustained price move and a higher volume-change floor before emitting watch-tier signals, with an explicit confirmation rule favoring executed trades over quote-only movement.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-506** `rejected` — Raise the watch-tier minimum price move from 0.03 to 0.05 to filter out brief 3% blips that are still being labeled noise.
  - **Governor rejection**: Yes. The proposed tweak violates the historical global floor that `score_threshold` / `spike_score_threshold` must remain explicit and ≥ 2.2, because it sets `score_threshold` to `None`. This matches the previously rejected relaxation rule (TB-XXX: score threshold cannot be removed/disabled). The other proposed values (`min_price_move: 0.05`, `min_volume_delta: 20000.0`) do not conflict with the listed floors.
- [ ] **TB-507** `rejected` — Raise the minimum volume delta to about 20000 to reduce thin-market quote noise while still allowing genuinely informative flow through.
  - **Governor rejection**: Yes. The proposed tweak violates the historical global floor that `score_threshold` / `spike_score_threshold` must remain explicit and ≥ 2.2, because it sets `score_threshold` to `None`. This matches the previously rejected relaxation rule (TB-XXX: score threshold cannot be removed/disabled). The other proposed values (`min_price_move: 0.05`, `min_volume_delta: 20000.0`) do not conflict with the listed floors.
- [ ] **TB-508** `rejected` — Add a confirmation rule: require multi-minute directional persistence or a rise in executed trade count before a signal can clear watch tier.
  - **Governor rejection**: Yes. The proposed tweak violates the historical global floor that `score_threshold` / `spike_score_threshold` must remain explicit and ≥ 2.2, because it sets `score_threshold` to `None`. This matches the previously rejected relaxation rule (TB-XXX: score threshold cannot be removed/disabled). The other proposed values (`min_price_move: 0.05`, `min_volume_delta: 20000.0`) do not conflict with the listed floors.

---

## 2026-06-06 — Advisor snapshot 169

### Summary
The false positives are concentrated in thin, low-liquidity macro markets where quote-driven or single-print moves are being flagged without enough executed-trade confirmation. Several recent watch/notable signals were labeled noise or uncertain even when price moved 2-3%, which suggests the detector is too sensitive to isolated volume/price bursts.

### Next step
Require both a higher price move and explicit trade confirmation before emitting spikes in thin macro markets; the cleanest single change is to raise the minimum price move and gate on nonzero executed volume or trade-count acceleration rather than quote-only movement.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-509** `rejected` — Raise spike_min_price_move from 0.03 to 0.05 for this market class.
  - **Governor rejection**: The proposal violates the historical no-null-relaxation / score-gating constraint: `score_threshold` must remain explicit and non-None, but the tweak sets `score_threshold: None` (TB-Score / global score-floor rule). It also conflicts with the global floor that `min_volume_delta` must be explicit/non-None, because the text says to gate on nonzero executed volume or trade-count acceleration rather than a fixed explicit minimum volume threshold, which removes the required explicit volume gate.
- [ ] **TB-510** `rejected` — Add a hard executed-trade confirmation rule: do not flag if volume delta is driven by quotes only or if executed volume is zero.
  - **Governor rejection**: The proposal violates the historical no-null-relaxation / score-gating constraint: `score_threshold` must remain explicit and non-None, but the tweak sets `score_threshold: None` (TB-Score / global score-floor rule). It also conflicts with the global floor that `min_volume_delta` must be explicit/non-None, because the text says to gate on nonzero executed volume or trade-count acceleration rather than a fixed explicit minimum volume threshold, which removes the required explicit volume gate.
- [ ] **TB-511** `rejected` — Increase spike_min_volume_delta to 20000.0 for watch-tier alerts, and require sustained movement over multiple minutes before emitting.
  - **Governor rejection**: The proposal violates the historical no-null-relaxation / score-gating constraint: `score_threshold` must remain explicit and non-None, but the tweak sets `score_threshold: None` (TB-Score / global score-floor rule). It also conflicts with the global floor that `min_volume_delta` must be explicit/non-None, because the text says to gate on nonzero executed volume or trade-count acceleration rather than a fixed explicit minimum volume threshold, which removes the required explicit volume gate.

---

## 2026-06-06 — Advisor snapshot 170

### Summary
Recent analyst labels show a repeated false-positive pattern in thin, quote-driven macro markets where small price moves and large-looking volume deltas are not backed by executed-trade confirmation. The issue is especially acute on watch-tier alerts, where noise is being triggered by price/volume changes that are directionally real but not yet informative.

### Next step
Add an executed-trade confirmation rule and raise the watch-tier volume bar; require nonzero executed trades plus a larger sustained price move before emitting a spike signal.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-512** `rejected` — Raise the minimum volume delta for watch-tier alerts to cut thin-market noise.
  - **Governor rejection**: The proposed tweak violates the active global floor constraint by setting `min_price_move` to 0.04, which is below the required `min_price_move >= 0.05` floor. It also conflicts with the tier-hardening approach because it sets `score_threshold` to `None`, while the historical constraints explicitly require `score_threshold >= 2.2` and never `None`.
- [ ] **TB-513** `rejected` — Increase the minimum price move slightly so quote-only swings do not trigger.
  - **Governor rejection**: The proposed tweak violates the active global floor constraint by setting `min_price_move` to 0.04, which is below the required `min_price_move >= 0.05` floor. It also conflicts with the tier-hardening approach because it sets `score_threshold` to `None`, while the historical constraints explicitly require `score_threshold >= 2.2` and never `None`.
- [ ] **TB-514** `rejected` — Require multi-minute directional persistence with executed trades before flagging as signal.
  - **Governor rejection**: The proposed tweak violates the active global floor constraint by setting `min_price_move` to 0.04, which is below the required `min_price_move >= 0.05` floor. It also conflicts with the tier-hardening approach because it sets `score_threshold` to `None`, while the historical constraints explicitly require `score_threshold >= 2.2` and never `None`.

---

## 2026-06-06 — Advisor snapshot 171

### Summary
The false positives are concentrated in thin or quote-driven macro markets where price moves are small, volume is uneven, and analyst labels call for executed-trade confirmation rather than quote-only swings.

### Next step
Require a larger price move plus nonzero executed volume before emitting a spike on thin macro markets; this is the clearest single change to cut noise without suppressing meaningful flow.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-515** `rejected` — Raise the minimum price move from 0.03 to 0.05 for watch-level spike emissions.
  - **Governor rejection**: TB-Global-score gating is violated because the proposed tweak sets score_threshold to None, but the historical constraints explicitly require score_threshold ≥ 2.2 with no None relaxations. The other proposed thresholds do not conflict: min_price_move = 0.05 satisfies the global floor and the thin-market tightening, and min_volume_delta is explicit/non-None.
- [ ] **TB-516** `rejected` — Increase the minimum volume delta from 10986.02 to 15000.0 for thin macro contracts.
  - **Governor rejection**: TB-Global-score gating is violated because the proposed tweak sets score_threshold to None, but the historical constraints explicitly require score_threshold ≥ 2.2 with no None relaxations. The other proposed thresholds do not conflict: min_price_move = 0.05 satisfies the global floor and the thin-market tightening, and min_volume_delta is explicit/non-None.
- [ ] **TB-517** `rejected` — Add a gating rule that suppresses signals unless there is at least one executed trade and a multi-minute directional move.
  - **Governor rejection**: TB-Global-score gating is violated because the proposed tweak sets score_threshold to None, but the historical constraints explicitly require score_threshold ≥ 2.2 with no None relaxations. The other proposed thresholds do not conflict: min_price_move = 0.05 satisfies the global floor and the thin-market tightening, and min_volume_delta is explicit/non-None.

---

## 2026-06-06 — Advisor snapshot 172

### Summary
The false positives are concentrated in thin, quote-driven macro markets where modest price moves and large quoted volume deltas are being flagged despite analyst labels calling them noise or unclear. The pattern suggests the detector is too sensitive to volume alone and needs stronger confirmation from executed trading and sustained price movement.

### Next step
Raise the price-move and volume-confirmation bars for thin markets, and require executed-trade evidence or a multi-minute sustained move before emitting a spike.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-518** `rejected` — Increase spike_min_price_move from 0.03 to 0.04 for thin macro markets.
  - **Governor rejection**: TB-001 / Generic price-confirmation floor is violated because the proposed min_price_move of 0.04 relaxes the historical global floor of min_price_move >= 0.05; this is explicitly rejected as a noise-relaxation. TB-002 / Score hardening is also violated because score_threshold is set to None, conflicting with the requirement that score_threshold be explicit/non-None and >= 2.2. TB-003 / No relaxations is violated for the same reason, since None/unset score gates are disallowed.
- [ ] **TB-519** `rejected` — Increase spike_min_volume_delta from 10000 to 15000 to suppress quote-driven bursts.
  - **Governor rejection**: TB-001 / Generic price-confirmation floor is violated because the proposed min_price_move of 0.04 relaxes the historical global floor of min_price_move >= 0.05; this is explicitly rejected as a noise-relaxation. TB-002 / Score hardening is also violated because score_threshold is set to None, conflicting with the requirement that score_threshold be explicit/non-None and >= 2.2. TB-003 / No relaxations is violated for the same reason, since None/unset score gates are disallowed.
- [ ] **TB-520** `rejected` — Add a rule that price moves must persist for multiple minutes with nonzero executed trades before the spike can pass the score gate.
  - **Governor rejection**: TB-001 / Generic price-confirmation floor is violated because the proposed min_price_move of 0.04 relaxes the historical global floor of min_price_move >= 0.05; this is explicitly rejected as a noise-relaxation. TB-002 / Score hardening is also violated because score_threshold is set to None, conflicting with the requirement that score_threshold be explicit/non-None and >= 2.2. TB-003 / No relaxations is violated for the same reason, since None/unset score gates are disallowed.

---

## 2026-06-06 — Advisor snapshot 173

### Summary
The false positives are concentrated in thin, quote-driven CPI markets where volume spikes and small price moves are being flagged without enough executed-trade confirmation. The analyst labels consistently suggest the detector is too sensitive to low-quality flow, especially when price move is only 2–3%.

### Next step
Tighten the rule for thin/quote-driven markets by requiring a larger price move and at least some executed-trade confirmation before emitting, rather than relying on volume delta alone.

### Suggested thresholds
`min_volume_delta` → `12000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-521** `rejected` — Raise `spike_min_price_move` from 0.03 to 0.04 for thin macro/quote-driven markets.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets min_price_move to 0.04, which conflicts with the historical hard floor of min_price_move ≥ 0.05 and the explicit rule not to relax into 0.03–0.04 price floors. TB-002 is also violated because score_threshold is set to None, but the historical constraints require score_threshold ≥ 2.2 and never None. The proposal is otherwise consistent with tightening thin/quote-driven markets, but these two settings regress past hard constraints.
- [ ] **TB-522** `rejected` — Increase `spike_min_volume_delta` modestly to filter low-quality bursts, but keep it below a level that would suppress legitimate trade-led spikes.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets min_price_move to 0.04, which conflicts with the historical hard floor of min_price_move ≥ 0.05 and the explicit rule not to relax into 0.03–0.04 price floors. TB-002 is also violated because score_threshold is set to None, but the historical constraints require score_threshold ≥ 2.2 and never None. The proposal is otherwise consistent with tightening thin/quote-driven markets, but these two settings regress past hard constraints.
- [ ] **TB-523** `rejected` — Add a trade-confirmation gate for watch-tier macro markets: if executed volume is zero or absent, require the higher price-move threshold before signaling.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets min_price_move to 0.04, which conflicts with the historical hard floor of min_price_move ≥ 0.05 and the explicit rule not to relax into 0.03–0.04 price floors. TB-002 is also violated because score_threshold is set to None, but the historical constraints require score_threshold ≥ 2.2 and never None. The proposal is otherwise consistent with tightening thin/quote-driven markets, but these two settings regress past hard constraints.

---

## 2026-06-06 — Advisor snapshot 174

### Summary
The false positives cluster around thin, quote-driven CPI markets where moderate price moves occur without strong executed volume, so the detector is over-triggering on sparse liquidity rather than meaningful flow. The analyst notes consistently ask for stricter confirmation from real trades and/or a larger sustained move, which points to tightening both volume and price gates.

### Next step
Raise the trigger to require both higher executed volume and a slightly larger sustained price move before emitting on low-liquidity macro contracts; if only one condition is met, suppress the signal unless the combined score is clearly exceptional.

### Suggested thresholds
`min_volume_delta` → `12000.0`, `min_price_move` → `0.04`, `score_threshold` → `3.25`

### Recommendations

- [ ] **TB-524** `rejected` — Increase the minimum volume delta to filter quote-only swings in thin CPI markets.
  - **Governor rejection**: TB-001 violated: the proposed `min_price_move: 0.04` relaxes the historical price floor, which explicitly requires `min_price_move ≥ 0.05` globally and rejects `0.03–0.04`. TB-003 is also violated indirectly if `score_threshold: 3.25` is interpreted as tightening only, but the proposal is still conflicting because it lowers the price gate below the previously enforced minimum. The volume threshold does not conflict with the historical floor because it remains explicit and non-`None`.
- [ ] **TB-525** `rejected` — Raise the minimum price move modestly so 2%-3% quote drift no longer triggers by itself.
  - **Governor rejection**: TB-001 violated: the proposed `min_price_move: 0.04` relaxes the historical price floor, which explicitly requires `min_price_move ≥ 0.05` globally and rejects `0.03–0.04`. TB-003 is also violated indirectly if `score_threshold: 3.25` is interpreted as tightening only, but the proposal is still conflicting because it lowers the price gate below the previously enforced minimum. The volume threshold does not conflict with the historical floor because it remains explicit and non-`None`.
- [ ] **TB-526** `rejected` — Increase the score threshold slightly to require stronger joint evidence when liquidity is poor.
  - **Governor rejection**: TB-001 violated: the proposed `min_price_move: 0.04` relaxes the historical price floor, which explicitly requires `min_price_move ≥ 0.05` globally and rejects `0.03–0.04`. TB-003 is also violated indirectly if `score_threshold: 3.25` is interpreted as tightening only, but the proposal is still conflicting because it lowers the price gate below the previously enforced minimum. The volume threshold does not conflict with the historical floor because it remains explicit and non-`None`.

---

## 2026-06-06 — Advisor snapshot 175

### Summary
The false positives are concentrated in thin, quote-driven CPI contracts where modest price moves and large-looking volume deltas are still being labeled as low-confidence noise. The consistent pattern is that executed-trade confirmation and stronger sustained price movement are needed before emitting a spike.

### Next step
Tighten the detector for thin CPI markets by requiring both higher volume evidence and a larger sustained price move before a signal can pass the combined score gate.

### Suggested thresholds
`min_volume_delta` → `12000.0`, `min_price_move` → `0.04`, `score_threshold` → `4.0`

### Recommendations

- [x] **TB-527** `applied` — Raise the minimum volume delta to filter out quote-only bursts in thin markets.
- [x] **TB-528** `applied` — Increase the minimum price move so a short-lived 2%–5% quote swing does not trigger a spike.
- [x] **TB-529** `applied` — Keep the score threshold modestly higher only after adding the volume/price floor, so genuinely informative flow is not muted.

---

## 2026-06-06 — Advisor snapshot 176

### Summary
Recent false positives cluster in thin, quote-driven CPI markets where modest price moves are triggered by sparse or non-executed flow. Analyst notes repeatedly recommend requiring sustained movement and/or real executed volume before emitting a spike.

### Next step
Raise the bar for quote-only signals by requiring either higher executed volume or a larger sustained price move before a spike can fire, with the strongest evidence for increasing the price-move floor.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-530** `rejected` — Increase the minimum price move from 3% to 5% to suppress sparse-quote noise while preserving larger genuine moves.
  - **Governor rejection**: TB-global-floor violation: the proposed tweak sets `min_volume_delta` to `None`, which conflicts with the historical constraint that `min_volume_delta` must be explicit/non-`None` and must never be relaxed to `None`. The proposed `min_price_move: 0.05` is consistent with the floor, but the `min_volume_delta` relaxation is not.
- [ ] **TB-531** `rejected` — Require executed volume, not just quote changes, for thin macro contracts when the move is under 5%.
  - **Governor rejection**: TB-global-floor violation: the proposed tweak sets `min_volume_delta` to `None`, which conflicts with the historical constraint that `min_volume_delta` must be explicit/non-`None` and must never be relaxed to `None`. The proposed `min_price_move: 0.05` is consistent with the floor, but the `min_volume_delta` relaxation is not.
- [ ] **TB-532** `rejected` — Leave the score threshold unchanged for now; the main failure mode is low-quality price action rather than weak combined scoring.
  - **Governor rejection**: TB-global-floor violation: the proposed tweak sets `min_volume_delta` to `None`, which conflicts with the historical constraint that `min_volume_delta` must be explicit/non-`None` and must never be relaxed to `None`. The proposed `min_price_move: 0.05` is consistent with the floor, but the `min_volume_delta` relaxation is not.

---

## 2026-06-06 — Advisor snapshot 177

### Summary
The recent false positives are concentrated in thin, low-liquidity CPI markets where quote-driven moves and sparse trades create apparent spikes without durable follow-through. Analyst notes consistently ask for more persistence and executed volume before triggering.

### Next step
Raise the minimum volume delta and require sustained multi-trade price movement for thin macro markets before emitting a spike.

### Suggested thresholds
`min_volume_delta` → `12000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-533** `rejected` — Increase the volume gate to filter quote-only bursts that do not convert into real traded flow.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical global floor requiring `score_threshold ≥ 2.2` and explicitly forbidding null relaxations for `score_threshold`.
- [ ] **TB-534** `rejected` — Require at least two-sided or multi-trade persistence before flagging a spike on low-liquidity contracts.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical global floor requiring `score_threshold ≥ 2.2` and explicitly forbidding null relaxations for `score_threshold`.
- [ ] **TB-535** `rejected` — Add a modestly higher price-move floor so isolated 3%-5% quote jumps do not trigger signals without confirming volume.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical global floor requiring `score_threshold ≥ 2.2` and explicitly forbidding null relaxations for `score_threshold`.

---

## 2026-06-06 — Advisor snapshot 178

### Summary
The false positives are concentrated in thin, low-liquidity macro markets where quote-driven or low-persistence price moves are being promoted to signals despite weak executed flow. Analyst notes repeatedly ask for more sustained movement and/or real traded volume before firing.

### Next step
Add a persistence/confirmation rule first, and raise the price-move floor modestly; the strongest single change is to require executed volume across multiple trades before emitting a signal.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-536** `rejected` — Increase the minimum price move to 0.05 to filter out 2%–3% quote flickers that are repeatedly labeled noise.
  - **Governor rejection**: The proposed tweak violates the historical volume gate and trade-confirmation constraints by setting min_volume_delta to None, which conflicts with the explicit requirement to keep min_volume_delta non-None and to require a real executed-volume threshold. It also weakens the historical persistence/execution-quality requirements for thin markets by omitting the multi-trade confirmation that was explicitly tightened to prevent quote-driven false positives.
- [ ] **TB-537** `rejected` — Require sustained price movement over multiple trades or bars, not a one-tick spike, before detection.
  - **Governor rejection**: The proposed tweak violates the historical volume gate and trade-confirmation constraints by setting min_volume_delta to None, which conflicts with the explicit requirement to keep min_volume_delta non-None and to require a real executed-volume threshold. It also weakens the historical persistence/execution-quality requirements for thin markets by omitting the multi-trade confirmation that was explicitly tightened to prevent quote-driven false positives.
- [ ] **TB-538** `rejected` — Raise the volume gate materially for thin markets so quote-only moves with large nominal volΔ but little execution quality do not pass.
  - **Governor rejection**: The proposed tweak violates the historical volume gate and trade-confirmation constraints by setting min_volume_delta to None, which conflicts with the explicit requirement to keep min_volume_delta non-None and to require a real executed-volume threshold. It also weakens the historical persistence/execution-quality requirements for thin markets by omitting the multi-trade confirmation that was explicitly tightened to prevent quote-driven false positives.

---

## 2026-06-06 — Advisor snapshot 179

### Summary
The false positives are concentrated in thin macro markets where quote-driven or low-persistence moves produce small price changes despite large volume deltas. Analyst labels consistently ask for stronger confirmation via sustained multi-trade drift or executed volume before emitting a signal.

### Next step
Tighten the detector to require both a larger price move and higher persistence for thin macro markets, while also raising the volume gate modestly to suppress quote-only spikes.

### Suggested thresholds
`min_volume_delta` → `12000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-539** `rejected` — Raise spike_min_price_move from 0.03 to 0.05 to filter out low-confidence 2%–3% flickers that are being labeled noise.
  - **Governor rejection**: TB-003 / global floors is violated because `score_threshold` is set to `None`, but the historical constraints require `score_threshold ≥ 2.2` and non-`None`. The proposed tweak also does not address the required explicit non-`None` score gate.
- [ ] **TB-540** `rejected` — Raise spike_min_volume_delta from the current setting to about 12000.0 so thin markets need more decisive flow before triggering.
  - **Governor rejection**: TB-003 / global floors is violated because `score_threshold` is set to `None`, but the historical constraints require `score_threshold ≥ 2.2` and non-`None`. The proposed tweak also does not address the required explicit non-`None` score gate.
- [ ] **TB-541** `rejected` — Add a persistence rule: require at least 2 executed trades or sustained price movement across multiple prints before emitting a signal.
  - **Governor rejection**: TB-003 / global floors is violated because `score_threshold` is set to `None`, but the historical constraints require `score_threshold ≥ 2.2` and non-`None`. The proposed tweak also does not address the required explicit non-`None` score gate.

---

## 2026-06-06 — Advisor snapshot 180

### Summary
The false positives are concentrated in thin macro markets where quote-only or low-persistence moves trigger spikes despite weak executed participation. The analyst labels consistently suggest these should require more confirmation from traded volume, sustained drift, or repeated two-sided flow.

### Next step
Tighten the detector by requiring both a larger price move and confirmed executed volume persistence before emitting a spike on low-liquidity macro markets.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.08`

### Recommendations

- [ ] **TB-542** `rejected` — Raise the minimum price move to filter out 2%-to-6% quote-only wiggles on thin markets.
  - **Governor rejection**: Conflict with the historical global floor on score threshold: `score_threshold` / `spike_score_threshold` must be explicit and ≥ 2.2, but the proposed tweak sets `score_threshold: None`, which violates that requirement. The proposed `min_price_move: 0.08` and `min_volume_delta: 15000.0` do not conflict with the stated floors.
- [ ] **TB-543** `rejected` — Increase the volume-delta floor modestly so low-quality signals need more actual participation before triggering.
  - **Governor rejection**: Conflict with the historical global floor on score threshold: `score_threshold` / `spike_score_threshold` must be explicit and ≥ 2.2, but the proposed tweak sets `score_threshold: None`, which violates that requirement. The proposed `min_price_move: 0.08` and `min_volume_delta: 15000.0` do not conflict with the stated floors.
- [ ] **TB-544** `rejected` — Add a persistence rule: require the move to hold across multiple trades or minutes, or require repeated two-sided flow for acceptance.
  - **Governor rejection**: Conflict with the historical global floor on score threshold: `score_threshold` / `spike_score_threshold` must be explicit and ≥ 2.2, but the proposed tweak sets `score_threshold: None`, which violates that requirement. The proposed `min_price_move: 0.08` and `min_volume_delta: 15000.0` do not conflict with the stated floors.

---

## 2026-06-06 — Advisor snapshot 181

### Summary
The false positives are concentrated in thin, low-priced macro markets where quote-driven or low-persistence moves trigger signals without enough executed trade confirmation. Analyst labels repeatedly mark these as noise unless the move is sustained, multi-trade, or backed by real volume.

### Next step
Raise the minimum persistence and executed-volume requirement for low-liquidity spikes; keep price sensitivity, but require either a larger move or multiple confirmed trades before emitting.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-545** `rejected` — Increase spike_min_volume_delta to filter quote-only jumps that are not supported by executed flow.
  - **Governor rejection**: TB-Score-HardFloor is violated because the proposed tweak sets score_threshold to None, but the historical constraints require score_threshold / spike_score_threshold to remain explicit and >= 2.2 with no None relaxations. The proposed min_price_move = 0.05 is compliant, and min_volume_delta = 15000.0 is explicit/non-None, but the score_threshold relaxation conflicts with the hard floor.
- [ ] **TB-546** `rejected` — Increase spike_min_price_move modestly so small 2% moves in thin markets do not fire signals on their own.
  - **Governor rejection**: TB-Score-HardFloor is violated because the proposed tweak sets score_threshold to None, but the historical constraints require score_threshold / spike_score_threshold to remain explicit and >= 2.2 with no None relaxations. The proposed min_price_move = 0.05 is compliant, and min_volume_delta = 15000.0 is explicit/non-None, but the score_threshold relaxation conflicts with the hard floor.
- [ ] **TB-547** `rejected` — Add or strengthen a persistence rule: require the move to hold across multiple trades or minutes before emission.
  - **Governor rejection**: TB-Score-HardFloor is violated because the proposed tweak sets score_threshold to None, but the historical constraints require score_threshold / spike_score_threshold to remain explicit and >= 2.2 with no None relaxations. The proposed min_price_move = 0.05 is compliant, and min_volume_delta = 15000.0 is explicit/non-None, but the score_threshold relaxation conflicts with the hard floor.

---

## 2026-06-06 — Advisor snapshot 182

### Summary
Recent analyst labels show a consistent false-positive pattern in thin, quote-driven macro markets: large volume deltas alone are triggering signals even when the price move is small or the move is not trade-confirmed. The clearest fix is to require stronger price confirmation and/or executed-volume confirmation before emitting a spike.

### Next step
Raise the bar on quote-only detections by requiring either a larger fractional price move or confirmed executed volume before a signal can pass the combined score threshold.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-548** `rejected` — Increase the minimum price move to 0.05 so thin markets need a clearer move before flagging.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets min_volume_delta to None, which removes the required explicit volume gate. TB-003 is also violated because score_threshold is set to None, but the historical constraint requires an explicit score_threshold >= 2.2. The min_price_move value of 0.05 is consistent with the floor, but the proposal still conflicts with the historical constraints due to the removed gates.
- [ ] **TB-549** `rejected` — Add a rule that volume delta must be trade-confirmed, not quote-only, for low-liquidity markets.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets min_volume_delta to None, which removes the required explicit volume gate. TB-003 is also violated because score_threshold is set to None, but the historical constraint requires an explicit score_threshold >= 2.2. The min_price_move value of 0.05 is consistent with the floor, but the proposal still conflicts with the historical constraints due to the removed gates.
- [ ] **TB-550** `rejected` — Keep the score threshold unchanged for now and suppress signals that do not meet both liquidity and price-confirmation requirements.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets min_volume_delta to None, which removes the required explicit volume gate. TB-003 is also violated because score_threshold is set to None, but the historical constraint requires an explicit score_threshold >= 2.2. The min_price_move value of 0.05 is consistent with the floor, but the proposal still conflicts with the historical constraints due to the removed gates.

---

## 2026-06-06 — Advisor snapshot 183

### Summary
The false positives are concentrated in thin, low-liquidity markets where quote-only or low-quality price bursts trigger signals despite little evidence of real traded demand. The analyst labels consistently suggest tightening the detector around confirmed execution and sustained price movement rather than raw volume spikes alone.

### Next step
Require both a higher minimum executed volume and a larger price move for thin/low-priced markets; if only one can change globally, raise the price-move threshold first to suppress quote-driven bursts.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-551** `rejected` — Increase the minimum price move to filter out 2% moves in thin markets, since the noisy examples cluster at priceΔ=0.02 while informative cases are at 0.07-0.09.
  - **Governor rejection**: Yes. The proposed tweak sets `min_volume_delta: None` and `score_threshold: None`, which violates the historical hard constraints that `min_volume_delta` must be explicit and never `None` and that `score_threshold` must be explicit and ≥ 2.2, never `None`. This also conflicts with the explicit 'No null relaxations' rule, which rejects nulling any core gate.
- [ ] **TB-552** `rejected` — Add an execution-quality gate: only trigger when volume delta reflects confirmed traded volume, not quote updates alone.
  - **Governor rejection**: Yes. The proposed tweak sets `min_volume_delta: None` and `score_threshold: None`, which violates the historical hard constraints that `min_volume_delta` must be explicit and never `None` and that `score_threshold` must be explicit and ≥ 2.2, never `None`. This also conflicts with the explicit 'No null relaxations' rule, which rejects nulling any core gate.
- [ ] **TB-553** `rejected` — For low-liquidity macro markets, require either sustained multi-minute imbalance or a higher combined score before emitting a signal.
  - **Governor rejection**: Yes. The proposed tweak sets `min_volume_delta: None` and `score_threshold: None`, which violates the historical hard constraints that `min_volume_delta` must be explicit and never `None` and that `score_threshold` must be explicit and ≥ 2.2, never `None`. This also conflicts with the explicit 'No null relaxations' rule, which rejects nulling any core gate.

---

## 2026-06-06 — Advisor snapshot 184

### Summary
The recent false positives are concentrated in thin, quote-driven markets where large volume deltas do not correspond to meaningful executed trading, and modest price moves are still getting flagged. The analyst notes consistently recommend demanding either real traded volume, a larger price move, or persistence before emitting a spike.

### Next step
Tighten the detector primarily by requiring a larger price move on low-liquidity/quote-heavy markets, and backstop it with a higher minimum volume delta so quote-only bursts do not pass.

### Suggested thresholds
`min_volume_delta` → `12000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-554** `rejected` — Raise the minimum price move to 0.05 for thin or quote-driven markets.
  - **Governor rejection**: Yes. The tweak violates the historical global floor TB-001 because it sets `score_threshold` to `None`, while the constraint explicitly says `score_threshold >= 2.2` and never `None`. It also conflicts with TB-005 because score is required to remain a live gate, not null, and should be used as a secondary filter after price, volume, trade-count, and persistence checks.
- [ ] **TB-555** `rejected` — Increase the minimum volume delta to 12000 to reduce quote-only bursts.
  - **Governor rejection**: Yes. The tweak violates the historical global floor TB-001 because it sets `score_threshold` to `None`, while the constraint explicitly says `score_threshold >= 2.2` and never `None`. It also conflicts with TB-005 because score is required to remain a live gate, not null, and should be used as a secondary filter after price, volume, trade-count, and persistence checks.
- [ ] **TB-556** `rejected` — If both volume and price move are weak, require multi-minute persistence before emitting a signal.
  - **Governor rejection**: Yes. The tweak violates the historical global floor TB-001 because it sets `score_threshold` to `None`, while the constraint explicitly says `score_threshold >= 2.2` and never `None`. It also conflicts with TB-005 because score is required to remain a live gate, not null, and should be used as a secondary filter after price, volume, trade-count, and persistence checks.

---

## 2026-06-06 — Advisor snapshot 185

### Summary
The false positives are concentrated in thin, quote-driven macro markets where large score/volume changes are not backed by executed trades or sustained mid-price movement. Analyst labels consistently recommend tightening the trigger so quote-only bursts do not emit signals.

### Next step
Add a trade-confirmation gate for thin markets: require either meaningful executed volume or a larger sustained price move before a spike can trigger.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-557** `rejected` — Raise the minimum price move from 0.03 to 0.05 to suppress small quote-only shifts.
  - **Governor rejection**: Conflict with the historical hard floors: the proposal sets `score_threshold` to `None`, but the active global constraint requires `score_threshold` to remain explicit and ≥ 2.2, never `None`. This violates the hardened tuning floor and would reintroduce a previously rejected relaxation.
- [ ] **TB-558** `rejected` — Increase the minimum volume delta from 10,986 to 20,000 so only stronger flow clears the detector.
  - **Governor rejection**: Conflict with the historical hard floors: the proposal sets `score_threshold` to `None`, but the active global constraint requires `score_threshold` to remain explicit and ≥ 2.2, never `None`. This violates the hardened tuning floor and would reintroduce a previously rejected relaxation.
- [ ] **TB-559** `rejected` — Keep the score threshold unchanged for now; the main issue is trigger quality, not combined-score ranking.
  - **Governor rejection**: Conflict with the historical hard floors: the proposal sets `score_threshold` to `None`, but the active global constraint requires `score_threshold` to remain explicit and ≥ 2.2, never `None`. This violates the hardened tuning floor and would reintroduce a previously rejected relaxation.

---

## 2026-06-06 — Advisor snapshot 186

### Summary
Recent analyst labels show a consistent false-positive pattern driven by quote-only or thin-market moves: large volume deltas are appearing without enough confirmed price follow-through, especially in Kalshi macro markets. The detector is firing on moves that analysts classify as noise/unclear unless there is sustained mid-price movement or executed trade confirmation.

### Next step
Require more trade-confirmed movement before emission by raising the price-move floor and, if possible, gating on executed volume rather than quote-only shifts.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-560** `rejected` — Raise spike_min_price_move from 0.03 to 0.05 to suppress small quote-driven moves while preserving larger genuine spikes.
  - **Governor rejection**: The proposed tweak violates the historical **global score gate** constraint: **TB-002** requires `score_threshold` to remain explicit and **≥ 2.2**, and the proposal sets `score_threshold: None`. The `min_price_move: 0.05` value is consistent with the historical floor, and `min_volume_delta: 15000.0` does not directly conflict with any stated minimum.
- [ ] **TB-561** `rejected` — Increase spike_min_volume_delta from 0 to a positive executed-volume floor so thin-market quote bursts do not trigger signals without real trading.
  - **Governor rejection**: The proposed tweak violates the historical **global score gate** constraint: **TB-002** requires `score_threshold` to remain explicit and **≥ 2.2**, and the proposal sets `score_threshold: None`. The `min_price_move: 0.05` value is consistent with the historical floor, and `min_volume_delta: 15000.0` does not directly conflict with any stated minimum.
- [ ] **TB-562** `rejected` — Keep spike_score_threshold modestly higher if needed, but prioritize the volume/price gate first because the false positives are concentrated in low-confirmation moves.
  - **Governor rejection**: The proposed tweak violates the historical **global score gate** constraint: **TB-002** requires `score_threshold` to remain explicit and **≥ 2.2**, and the proposal sets `score_threshold: None`. The `min_price_move: 0.05` value is consistent with the historical floor, and `min_volume_delta: 15000.0` does not directly conflict with any stated minimum.

---

## 2026-06-06 — Advisor snapshot 187

### Summary
The false positives are concentrated in **low-liquidity macro contracts** where **quote-only price moves** and repeated quote updates trigger spikes without executed-trade confirmation. Analyst labels repeatedly recommend stronger trade confirmation and/or sustained-volume requirements rather than simply lowering sensitivity across the board.

### Next step
Add a **trade-confirmation gate** for low-liquidity macro markets: require at least **1 executed trade** plus a sustained move before emitting, and raise the volume-move bar for quote-driven spikes.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.08`

### Recommendations

- [ ] **TB-563** `rejected` — Raise **min_price_move** to **0.08** for low-priced macro contracts to filter mechanical repricing and quote flicker.
  - **Governor rejection**: Conflicts with the active hard floor constraint: the proposal sets `score_threshold` to `None`, but historical constraints require `score_threshold ≥ 2.2` and explicit/non-`None`. This violates the no-relaxation rule for TB-active hard floors. It also appears to weaken the volume floor relative to prior low-liquidity/quote-heavy protections unless `min_volume_delta` is being interpreted as an explicit floor; however the direct violation is the `score_threshold: None` setting.
- [ ] **TB-564** `rejected` — Raise **min_volume_delta** to **15000** for low-trade-count Fed/CPI markets so repeated quote updates do not fire alerts.
  - **Governor rejection**: Conflicts with the active hard floor constraint: the proposal sets `score_threshold` to `None`, but historical constraints require `score_threshold ≥ 2.2` and explicit/non-`None`. This violates the no-relaxation rule for TB-active hard floors. It also appears to weaken the volume floor relative to prior low-liquidity/quote-heavy protections unless `min_volume_delta` is being interpreted as an explicit floor; however the direct violation is the `score_threshold: None` setting.
- [ ] **TB-565** `rejected` — Require both **price move persistence across multiple trades** and **at least one executed trade** before signaling; use this rule before tightening the global score threshold.
  - **Governor rejection**: Conflicts with the active hard floor constraint: the proposal sets `score_threshold` to `None`, but historical constraints require `score_threshold ≥ 2.2` and explicit/non-`None`. This violates the no-relaxation rule for TB-active hard floors. It also appears to weaken the volume floor relative to prior low-liquidity/quote-heavy protections unless `min_volume_delta` is being interpreted as an explicit floor; however the direct violation is the `score_threshold: None` setting.

---

## 2026-06-06 — Advisor snapshot 188

### Summary
The false positives are concentrated in low-liquidity macro contracts where quote-only repricing and repeated quote updates create apparent spikes without trade confirmation. The pattern suggests the detector is too sensitive to price moves unless they are backed by executed volume or persistence across trades.

### Next step
Add a trade-confirmation gate for low-liquidity contracts: require either executed-volume persistence or multiple-trade confirmation before emitting on quote-driven price moves.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`, `score_threshold` → `6.0`

### Recommendations

- [x] **TB-566** `applied` — Raise the minimum price move for low-priced macro contracts from 0.03 to 0.05 when trade count is low or confirmation is absent.
- [x] **TB-567** `applied` — Increase the minimum volume delta for quote-driven Fed-style markets from 12700 to about 15000 before allowing a spike to fire.
- [x] **TB-568** `applied` — Raise the score threshold modestly to filter mechanical repricings, but keep it below the level that would suppress confirmed high-volume moves.

---

## 2026-06-06 — Advisor snapshot 189

### Summary
Recent false positives are being driven by low-liquidity, quote-driven price moves that look like spikes despite weak trade confirmation or flat/sustained volume. The analyst labels consistently ask for stronger confirmation, especially multi-tick follow-through and repeated same-side trades, rather than just a larger raw move.

### Next step
Raise the trade-confirmation requirement for low-liquidity macro contracts and make quote-only price moves insufficient unless they persist across multiple trades.

### Suggested thresholds
`min_price_move` → `0.08`, `score_threshold` → `6.0`

### Recommendations

- [ ] **TB-569** `rejected` — Increase spike_min_price_move modestly to filter small mechanical repricings, especially in low-priced macro markets.
  - **Governor rejection**: The proposed tweak violates the historical hard floor that `min_volume_delta` must remain explicit/non-`None` and not be relaxed. This is a direct conflict with the global constraint that `min_volume_delta` cannot be set to `None` (TB-Global-Hard-Floors / TB-Volume-Confirmation). It also weakens the historical low-liquidity trade-confirmation requirement by removing an explicit executed-volume gate, which conflicts with the trade-confirmation and quote-noise-suppression rules that require non-quote, trade-backed confirmation (TB-Trade-Confirmation-Gate / TB-Quote-Noise-Suppression).
- [ ] **TB-570** `rejected` — Add a trade-confirmation rule: require either multiple trades on the same side or sustained multi-tick follow-through before emitting a spike.
  - **Governor rejection**: The proposed tweak violates the historical hard floor that `min_volume_delta` must remain explicit/non-`None` and not be relaxed. This is a direct conflict with the global constraint that `min_volume_delta` cannot be set to `None` (TB-Global-Hard-Floors / TB-Volume-Confirmation). It also weakens the historical low-liquidity trade-confirmation requirement by removing an explicit executed-volume gate, which conflicts with the trade-confirmation and quote-noise-suppression rules that require non-quote, trade-backed confirmation (TB-Trade-Confirmation-Gate / TB-Quote-Noise-Suppression).
- [ ] **TB-571** `rejected` — If you want a single scalar tightening first, raise spike_score_threshold slightly rather than sharply increasing volume alone, so genuinely strong flow still passes.
  - **Governor rejection**: The proposed tweak violates the historical hard floor that `min_volume_delta` must remain explicit/non-`None` and not be relaxed. This is a direct conflict with the global constraint that `min_volume_delta` cannot be set to `None` (TB-Global-Hard-Floors / TB-Volume-Confirmation). It also weakens the historical low-liquidity trade-confirmation requirement by removing an explicit executed-volume gate, which conflicts with the trade-confirmation and quote-noise-suppression rules that require non-quote, trade-backed confirmation (TB-Trade-Confirmation-Gate / TB-Quote-Noise-Suppression).

---

## 2026-06-06 — Advisor snapshot 190

### Summary
The false positives are concentrated in quote-driven, low-liquidity macro contracts where price moves occur without executed-trade confirmation or sustained follow-through. The detector is also too sensitive to repeated flickers and low-conviction repricing rather than genuine momentum.

### Next step
Tighten the detector around trade-confirmed movement by requiring either sustained multi-tick follow-through or multiple same-side trades before emitting a spike, and raise the price-move floor for low-liquidity markets.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-572** `rejected` — Increase spike_min_price_move from 0.03 to 0.05 for low-liquidity or low-trade-count markets.
  - **Governor rejection**: TB-001 / No relaxation into nulls is violated because the proposed tweak sets min_volume_delta to None, while the historical constraints require min_volume_delta to be explicit and non-None. This also conflicts with the trade-confirmation and volume-gating rules for low-liquidity/quote-driven markets, which require executed-trade confirmation rather than removing the volume threshold entirely.
- [ ] **TB-573** `rejected` — Add a trade-confirmation rule: do not emit on quote-only moves unless the move persists across at least 2-3 ticks or is backed by multiple executed trades on the same side.
  - **Governor rejection**: TB-001 / No relaxation into nulls is violated because the proposed tweak sets min_volume_delta to None, while the historical constraints require min_volume_delta to be explicit and non-None. This also conflicts with the trade-confirmation and volume-gating rules for low-liquidity/quote-driven markets, which require executed-trade confirmation rather than removing the volume threshold entirely.
- [ ] **TB-574** `rejected` — Raise spike_score_threshold modestly to suppress marginal flicker-driven signals, especially when volume delta is high but trade confirmation is absent.
  - **Governor rejection**: TB-001 / No relaxation into nulls is violated because the proposed tweak sets min_volume_delta to None, while the historical constraints require min_volume_delta to be explicit and non-None. This also conflicts with the trade-confirmation and volume-gating rules for low-liquidity/quote-driven markets, which require executed-trade confirmation rather than removing the volume threshold entirely.

---

## 2026-06-06 — Advisor snapshot 191

### Summary
The false positives are concentrated in **quote-driven, low-liquidity macro markets** where price moves are small or mechanically repriced and not backed by executed trades or sustained follow-through. Analyst notes repeatedly recommend adding trade-confirmation and higher movement/volume gates to suppress flicker-like signals while preserving genuine spikes.

### Next step
Require **trade confirmation or sustained follow-through** before emitting watch/notable spikes in low-liquidity macro markets; as the best numeric backstop, raise the price-move floor modestly and keep volume gating secondary to avoid quote-only noise.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [x] **TB-575** `applied` — Increase **min_price_move** from 0.03 to **0.05** for CPI/Fed-style contracts to filter small quote flickers.
- [x] **TB-576** `applied` — Increase **min_volume_delta** from the current level to at least **1.5x baseline volume** (or an equivalent absolute floor) before watch-level emission.
- [x] **TB-577** `applied` — Add a rule that quote-only moves must persist across **multiple trades / multi-tick follow-through**; otherwise suppress the spike even if score clears threshold.

---

## 2026-06-06 — Advisor snapshot 192

### Summary
The false positives are clustered in low-liquidity or quote-driven macro contracts where small price moves and flat or noisy volume are being overcalled as spikes. Analyst labels repeatedly ask for stronger volume confirmation, larger price displacement, or trade confirmation before emitting signals.

### Next step
Raise the detector’s evidence bar for watch/notable emissions by requiring both a larger price move and a real volume multiple above baseline, with an explicit confirmation rule for executed trades to suppress quote flicker.

### Suggested thresholds
`min_price_move` → `0.04`

### Recommendations

- [ ] **TB-578** `rejected` — Increase the minimum price move to filter out small repricings that lack follow-through.
  - **Governor rejection**: TB-Global-01 is violated because the proposed tweak sets `min_price_move` to 0.04, which relaxes the explicitly enforced global hard floor of `min_price_move ≥ 0.05`. TB-Global-02 and TB-Global-03 are also violated because `min_volume_delta` and `score_threshold` are set to `None`, but historical constraints require both to remain explicit/non-None. In addition, TB-LowLiq-01 rejects lowering the price floor into the 0.03–0.04 range for low-liquidity/watch/notable markets; the fix should add trade-count and persistence confirmation instead, not reduce the floor.
- [ ] **TB-579** `rejected` — Require at least a 1.5x baseline volume multiple before watch-level alerts in CPI-style macro markets.
  - **Governor rejection**: TB-Global-01 is violated because the proposed tweak sets `min_price_move` to 0.04, which relaxes the explicitly enforced global hard floor of `min_price_move ≥ 0.05`. TB-Global-02 and TB-Global-03 are also violated because `min_volume_delta` and `score_threshold` are set to `None`, but historical constraints require both to remain explicit/non-None. In addition, TB-LowLiq-01 rejects lowering the price floor into the 0.03–0.04 range for low-liquidity/watch/notable markets; the fix should add trade-count and persistence confirmation instead, not reduce the floor.
- [ ] **TB-580** `rejected` — Add a trade-confirmation gate: do not emit on quote-only moves without sustained follow-through or multiple same-side trades.
  - **Governor rejection**: TB-Global-01 is violated because the proposed tweak sets `min_price_move` to 0.04, which relaxes the explicitly enforced global hard floor of `min_price_move ≥ 0.05`. TB-Global-02 and TB-Global-03 are also violated because `min_volume_delta` and `score_threshold` are set to `None`, but historical constraints require both to remain explicit/non-None. In addition, TB-LowLiq-01 rejects lowering the price floor into the 0.03–0.04 range for low-liquidity/watch/notable markets; the fix should add trade-count and persistence confirmation instead, not reduce the floor.

---

## 2026-06-06 — Advisor snapshot 193

### Summary
The false positives are mostly quote-driven or low-execution moves in macro CPI/FED contracts, where small price changes and shallow volume deltas are being misread as spikes. Analyst notes consistently ask for stronger executed-volume confirmation, larger price displacement, or sustained multi-tick follow-through before emitting signals.

### Next step
Raise the minimum price-move requirement modestly and add a volume-confirmation rule for low-liquidity markets, so quote-only flickers no longer pass while genuine high-volume spikes still do.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-581** `rejected` — Increase spike_min_price_move from 0.03 to 0.05 for CPI-style and other low-liquidity macro contracts.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it sets `min_volume_delta` to `None`, which violates the explicit non-`None` Volume gate requirement. It also omits the stronger low-liquidity / thin-market confirmation rules that require executed-trade confirmation and, in some cases, elevated volume thresholds rather than removing the gate.
- [ ] **TB-582** `rejected` — Require at least 1.5x baseline executed volume, or a comparable minimum volume delta, before watch/notable spikes can emit on low-trade markets.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it sets `min_volume_delta` to `None`, which violates the explicit non-`None` Volume gate requirement. It also omits the stronger low-liquidity / thin-market confirmation rules that require executed-trade confirmation and, in some cases, elevated volume thresholds rather than removing the gate.
- [ ] **TB-583** `rejected` — Add a follow-through filter: require multiple trades on the same side or sustained multi-tick continuation before promoting a signal to notable.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it sets `min_volume_delta` to `None`, which violates the explicit non-`None` Volume gate requirement. It also omits the stronger low-liquidity / thin-market confirmation rules that require executed-trade confirmation and, in some cases, elevated volume thresholds rather than removing the gate.

---

## 2026-06-06 — Advisor snapshot 194

### Summary
The false positives cluster around quote-driven, low-conviction moves where price changes are small-to-moderate but executed volume is not strong enough to confirm a real information event. Analyst notes consistently ask for more sustained volume and/or a larger price displacement before emitting a signal.

### Next step
Tighten the detector with a higher minimum executed-volume requirement plus a modestly higher price-move floor, rather than relying on score alone.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-584** `rejected` — Raise the price-move floor to at least 0.04 so 2%-3% quote churn is less likely to trigger watch-level spikes.
  - **Governor rejection**: Violates the historical floor on score gating: the proposed `score_threshold: None` conflicts with the explicit no-relaxations rule requiring a non-`None` score gate and the global floor `score_threshold ≥ 2.2`. It also conflicts with the price floor because `min_price_move: 0.04` weakens the explicitly tightened minimum `min_price_move ≥ 0.05` into the disallowed 0.03–0.04 range.
- [ ] **TB-585** `rejected` — Increase the volume gate to require a clearer multiple above baseline, with 1.5x baseline as the minimum starting point for CPI-style macro markets.
  - **Governor rejection**: Violates the historical floor on score gating: the proposed `score_threshold: None` conflicts with the explicit no-relaxations rule requiring a non-`None` score gate and the global floor `score_threshold ≥ 2.2`. It also conflicts with the price floor because `min_price_move: 0.04` weakens the explicitly tightened minimum `min_price_move ≥ 0.05` into the disallowed 0.03–0.04 range.
- [ ] **TB-586** `rejected` — Keep the score threshold as a secondary filter, but do not use it alone to suppress low-volume flickers; prioritize volume confirmation first.
  - **Governor rejection**: Violates the historical floor on score gating: the proposed `score_threshold: None` conflicts with the explicit no-relaxations rule requiring a non-`None` score gate and the global floor `score_threshold ≥ 2.2`. It also conflicts with the price floor because `min_price_move: 0.04` weakens the explicitly tightened minimum `min_price_move ≥ 0.05` into the disallowed 0.03–0.04 range.

---

## 2026-06-06 — Advisor snapshot 195

### Summary
The false positives cluster around quote-driven or low-execution moves that barely clear the current volume filter, especially in high-liquidity macro contracts where a small price change is not enough evidence of new information. The analyst labels consistently point to insufficient executed volume confirmation and overly sensitive spike detection on low-liquidity or quote-only adjustments.

### Next step
Raise the detector’s effective confirmation bar by requiring both a larger executed-volume multiple and a larger price move before emitting a spike, with the biggest tightening applied to low-liquidity and quote-only markets.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.04`, `score_threshold` → `16.0`

### Recommendations

- [ ] **TB-587** `rejected` — Increase the minimum price move for spike emission to filter out 2% to 3% quote churn in macro contracts.
  - **Governor rejection**: TB-001 / TB-004 conflict: the proposed `min_price_move: 0.04` relaxes the historical hard floor of `min_price_move ≥ 0.05`, which was explicitly retained for NBA series/playoff winner/low-liquidity high-odds/watch/notable markets. It also conflicts with the higher-confidence floor in TB-001 because the new tweak lowers price confirmation rather than tightening it, and the suggested `score_threshold: 16.0` does not compensate for a price gate that is explicitly disallowed from dropping below 0.05.
- [ ] **TB-588** `rejected` — Require a clearer executed-volume expansion above baseline before flagging low-liquidity CPI spikes.
  - **Governor rejection**: TB-001 / TB-004 conflict: the proposed `min_price_move: 0.04` relaxes the historical hard floor of `min_price_move ≥ 0.05`, which was explicitly retained for NBA series/playoff winner/low-liquidity high-odds/watch/notable markets. It also conflicts with the higher-confidence floor in TB-001 because the new tweak lowers price confirmation rather than tightening it, and the suggested `score_threshold: 16.0` does not compensate for a price gate that is explicitly disallowed from dropping below 0.05.
- [ ] **TB-589** `rejected` — Lift the combined score threshold modestly so borderline quote-only moves no longer emit signals.
  - **Governor rejection**: TB-001 / TB-004 conflict: the proposed `min_price_move: 0.04` relaxes the historical hard floor of `min_price_move ≥ 0.05`, which was explicitly retained for NBA series/playoff winner/low-liquidity high-odds/watch/notable markets. It also conflicts with the higher-confidence floor in TB-001 because the new tweak lowers price confirmation rather than tightening it, and the suggested `score_threshold: 16.0` does not compensate for a price gate that is explicitly disallowed from dropping below 0.05.

---

## 2026-06-06 — Advisor snapshot 196

### Summary
The false positives cluster around thin or quote-driven moves in low-liquidity macro markets, where small price changes or baseline-level volume are being over-flagged. Analyst labels repeatedly suggest requiring stronger executed volume confirmation and/or a larger price move before emitting a spike.

### Next step
Tighten the detector by raising the minimum executed-volume requirement and modestly increasing the minimum price-move floor for watch-tier signals, while keeping the combined score threshold secondary.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-590** `rejected` — Increase the volume gate for low-liquidity / quote-driven markets so quote-only churn does not trigger a spike.
  - **Governor rejection**: TB-GLOBAL is violated because the proposed `score_threshold: None` disables the score gate, but historical constraints require `score_threshold/spike_score_threshold ≥ 2.2` and non-None. It also conflicts with the low-liquidity/watch-tier rule set, which says not to relax into 0.03–0.04 price floors; `min_price_move: 0.04` is below the required 0.05 floor.
- [ ] **TB-591** `rejected` — Raise the price-move floor slightly for watch-level alerts, because 2%–3% moves are repeatedly labeled as noise when volume is weak.
  - **Governor rejection**: TB-GLOBAL is violated because the proposed `score_threshold: None` disables the score gate, but historical constraints require `score_threshold/spike_score_threshold ≥ 2.2` and non-None. It also conflicts with the low-liquidity/watch-tier rule set, which says not to relax into 0.03–0.04 price floors; `min_price_move: 0.04` is below the required 0.05 floor.
- [ ] **TB-592** `rejected` — Add a market-type-specific rule: require either a stronger volume multiple or multiple confirming trades before flagging macro contracts.
  - **Governor rejection**: TB-GLOBAL is violated because the proposed `score_threshold: None` disables the score gate, but historical constraints require `score_threshold/spike_score_threshold ≥ 2.2` and non-None. It also conflicts with the low-liquidity/watch-tier rule set, which says not to relax into 0.03–0.04 price floors; `min_price_move: 0.04` is below the required 0.05 floor.

---

## 2026-06-06 — Advisor snapshot 197

### Summary
The false positives cluster around quote-driven or low-confirmation moves: small 2–3% price changes with weak or merely baseline volume are repeatedly labeled noise, especially in thinly traded CPI and rate markets. The detector is too sensitive to short-lived updates unless it requires stronger executed volume or a larger price move.

### Next step
Tighten the detector by requiring both a higher minimum volume delta and a higher minimum price move for watch-tier signals in thin/quote-driven macro markets, rather than relying on score alone.

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-593** `rejected` — Raise the minimum price move from 0.03 to 0.05 for watch-tier macro spikes to filter out 3% quote churn.
  - **Governor rejection**: TB-001 / Global hard floors is violated because `score_threshold` is set to `None`, and historical constraints require `score_threshold ≥ 2.2` and non-`None`. The proposal also drops score as a gate despite the explicit rule that score must remain a live secondary suppressor, not be removed.
- [ ] **TB-594** `rejected` — Increase the minimum volume delta to about 25000 to require clearer executed flow before flagging.
  - **Governor rejection**: TB-001 / Global hard floors is violated because `score_threshold` is set to `None`, and historical constraints require `score_threshold ≥ 2.2` and non-`None`. The proposal also drops score as a gate despite the explicit rule that score must remain a live secondary suppressor, not be removed.
- [ ] **TB-595** `rejected` — Keep score_threshold unchanged for now; the main failure mode is low-confirmation price/volume triggers, not combined score calibration.
  - **Governor rejection**: TB-001 / Global hard floors is violated because `score_threshold` is set to `None`, and historical constraints require `score_threshold ≥ 2.2` and non-`None`. The proposal also drops score as a gate despite the explicit rule that score must remain a live secondary suppressor, not be removed.

---

## 2026-06-06 — Advisor snapshot 198

### Summary
The false positives cluster around small price moves with insufficient confirmation, especially in thinly traded or quote-driven macro markets. Analyst labels consistently suggest the detector is reacting to churn unless there is stronger executed volume or a larger move.

### Next step
Tighten the detector by requiring more executed volume before allowing a 3% move to trigger, and raise the score threshold modestly so quote-only updates in low-liquidity markets stop surfacing as spikes.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-596** `rejected` — Increase min_price_move from 0.03 to 0.05 for watch-tier signals in thinly traded rate/macro markets.
  - **Governor rejection**: Yes. The proposed tweak violates the historical constraint that `score_threshold` must remain explicit and non-`None` (the score gate remains active). Setting `score_threshold: None` directly conflicts with the global hard floor / live secondary brake rule, which requires `score_threshold ≥ 2.2` and non-`None`. It also does not conflict with `min_price_move: 0.05`, but the `score_threshold` setting is a regression.
- [ ] **TB-597** `rejected` — Raise min_volume_delta above 20,000 for quote-heavy CPI/Fed markets unless price move is at least 0.10.
  - **Governor rejection**: Yes. The proposed tweak violates the historical constraint that `score_threshold` must remain explicit and non-`None` (the score gate remains active). Setting `score_threshold: None` directly conflicts with the global hard floor / live secondary brake rule, which requires `score_threshold ≥ 2.2` and non-`None`. It also does not conflict with `min_price_move: 0.05`, but the `score_threshold` setting is a regression.
- [ ] **TB-598** `rejected` — Increase spike_score_threshold slightly to suppress borderline detections that only clear the current floor by a small margin.
  - **Governor rejection**: Yes. The proposed tweak violates the historical constraint that `score_threshold` must remain explicit and non-`None` (the score gate remains active). Setting `score_threshold: None` directly conflicts with the global hard floor / live secondary brake rule, which requires `score_threshold ≥ 2.2` and non-`None`. It also does not conflict with `min_price_move: 0.05`, but the `score_threshold` setting is a regression.

---

## 2026-06-06 — Advisor snapshot 199

### Summary
The false positives are concentrated in thinly traded or quote-driven macro contracts where small price moves and modest volume deltas are being flagged as spikes. Analyst notes consistently recommend requiring more executed volume and/or a larger price move to distinguish real information flow from quote churn.

### Next step
Tighten the detector to require both a larger price move and a higher executed-volume floor for low-liquidity macro contracts, rather than relying on either signal alone.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`, `score_threshold` → `3.0`

### Recommendations

- [x] **TB-599** `applied` — Raise the minimum price move from 0.03 to 0.05 for watch-tier spike emissions in thin CPI/rate markets.
- [x] **TB-600** `applied` — Increase the minimum volume delta to roughly 20000 for low-liquidity macro contracts to filter quote-only updates.
- [x] **TB-601** `applied` — Raise the combined score threshold modestly to 3.0 so borderline watch signals do not emit unless both price and volume are clearly supportive.

---

## 2026-06-06 — Advisor snapshot 200

### Summary
The false positives are concentrated in thinly traded or quote-driven CPI/FED contracts where small price moves and large raw volume deltas are being flagged without convincing executed-trade confirmation. Analyst labels consistently point to needing stronger price confirmation and/or real trade volume before emitting a spike.

### Next step
Tighten the detector by requiring both a larger minimum price move and confirmed executed trade volume for low-liquidity markets, rather than relying on raw volume delta alone.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-602** `rejected` — Raise the price-move floor to at least 0.03 for these markets.
  - **Governor rejection**: Violates the historical hard-floor rule: min_price_move was previously constrained to ≥ 0.05, but the proposed tweak sets it to 0.03, which is a forbidden relaxation into the 0.03–0.04 range. It also conflicts with the global gate rule that min_volume_delta must be explicit/non-None and score_threshold must remain active at ≥ 2.2; the proposal sets both to None, which is a null relaxation explicitly disallowed.
- [ ] **TB-603** `rejected` — Add a trade-confirmation gate: do not trigger on quote-only updates unless there is actual executed volume above baseline.
  - **Governor rejection**: Violates the historical hard-floor rule: min_price_move was previously constrained to ≥ 0.05, but the proposed tweak sets it to 0.03, which is a forbidden relaxation into the 0.03–0.04 range. It also conflicts with the global gate rule that min_volume_delta must be explicit/non-None and score_threshold must remain active at ≥ 2.2; the proposal sets both to None, which is a null relaxation explicitly disallowed.
- [ ] **TB-604** `rejected` — Keep the score threshold unchanged for now; the main issue is input-quality filtering, not ranking sensitivity.
  - **Governor rejection**: Violates the historical hard-floor rule: min_price_move was previously constrained to ≥ 0.05, but the proposed tweak sets it to 0.03, which is a forbidden relaxation into the 0.03–0.04 range. It also conflicts with the global gate rule that min_volume_delta must be explicit/non-None and score_threshold must remain active at ≥ 2.2; the proposal sets both to None, which is a null relaxation explicitly disallowed.

---

## 2026-06-06 — Advisor snapshot 201

### Summary
The false positives are concentrated in thin-liquidity or single-trade CPI markets where small price changes and isolated volume bursts are being over-signaled. The analyst notes consistently ask for stronger confirmation: larger price moves, higher absolute volume, and repeated same-side trades or sustained momentum.

### Next step
Tighten the detector with a higher minimum price move and a higher minimum volume delta, and add a confirmation rule requiring multiple same-side trades before emitting.

### Suggested thresholds
`min_volume_delta` → `10000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-605** `rejected` — Raise spike_min_price_move to filter out 1%–2% noise in thin CPI markets.
  - **Governor rejection**: TB-global hard floors and the later anti-noise tightening are violated because the proposed `min_price_move: 0.03` relaxes the historically enforced floor of `min_price_move ≥ 0.05`, which was repeatedly tightened specifically to prevent noise and rejected when moved back into the `0.03–0.04` range. The proposal also sets `score_threshold: None`, conflicting with the global score policy requiring score_threshold to remain explicit and never `None`. 
- [ ] **TB-606** `rejected` — Increase spike_min_volume_delta so isolated prints do not trigger on their own.
  - **Governor rejection**: TB-global hard floors and the later anti-noise tightening are violated because the proposed `min_price_move: 0.03` relaxes the historically enforced floor of `min_price_move ≥ 0.05`, which was repeatedly tightened specifically to prevent noise and rejected when moved back into the `0.03–0.04` range. The proposal also sets `score_threshold: None`, conflicting with the global score policy requiring score_threshold to remain explicit and never `None`. 
- [ ] **TB-607** `rejected` — Require either 2+ same-side trades or a sustained move over the threshold before emitting.
  - **Governor rejection**: TB-global hard floors and the later anti-noise tightening are violated because the proposed `min_price_move: 0.03` relaxes the historically enforced floor of `min_price_move ≥ 0.05`, which was repeatedly tightened specifically to prevent noise and rejected when moved back into the `0.03–0.04` range. The proposal also sets `score_threshold: None`, conflicting with the global score policy requiring score_threshold to remain explicit and never `None`. 

---

## 2026-06-06 — Advisor snapshot 202

### Summary
The false positives are concentrated in thin-liquidity CPI markets where very small absolute volume and modest one-shot price moves are being labeled as spikes. The analyst notes consistently ask for stronger volume confirmation and/or sustained multi-minute continuation before emission.

### Next step
Raise the minimum absolute volume requirement first, and add a rule that CPI spikes must show either a larger price move or repeated same-side trades over multiple minutes before triggering.

### Suggested thresholds
`min_volume_delta` → `50.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-608** `rejected` — Increase spike_min_volume_delta to filter thin-liquidity CPI noise, especially cases like volΔ=7 with a 1% move.
  - **Governor rejection**: TB-001 is violated because the proposed `min_price_move: 0.03` relaxes the historical hardened price-confirmation floor of `min_price_move ≥ 0.05`, which was explicitly set to prevent noisy false positives in thin markets. TB-002 is also violated because `score_threshold: None` removes the required active score brake; historical constraints require `score_threshold ≥ 2.2` and never `None`.
- [ ] **TB-609** `rejected` — Raise spike_min_price_move modestly so single-trade, high-price markets do not emit on tiny 1-2% moves.
  - **Governor rejection**: TB-001 is violated because the proposed `min_price_move: 0.03` relaxes the historical hardened price-confirmation floor of `min_price_move ≥ 0.05`, which was explicitly set to prevent noisy false positives in thin markets. TB-002 is also violated because `score_threshold: None` removes the required active score brake; historical constraints require `score_threshold ≥ 2.2` and never `None`.
- [ ] **TB-610** `rejected` — Keep score_threshold as a secondary backstop, but make volume/continuation the primary gate for CPI markets.
  - **Governor rejection**: TB-001 is violated because the proposed `min_price_move: 0.03` relaxes the historical hardened price-confirmation floor of `min_price_move ≥ 0.05`, which was explicitly set to prevent noisy false positives in thin markets. TB-002 is also violated because `score_threshold: None` removes the required active score brake; historical constraints require `score_threshold ≥ 2.2` and never `None`.

---

## 2026-06-06 — Advisor snapshot 203

### Summary
The false positives are coming from late-stage or flat markets where volume bursts and small price drift trigger signals despite weak follow-through. The analyst notes point to needing both stronger volume confirmation and a more sustained directional move before emitting a spike signal.

### Next step
Raise the volume gate and require a larger price move, rather than loosening the score threshold; the best next step is to make signals harder to trigger on isolated bursts and marginal drift.

### Suggested thresholds
`min_volume_delta` → `120000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-611** `rejected` — Increase spike_min_volume_delta to filter out single-burst late-stage prints, especially in extreme-price markets where volume alone is not informative.
  - **Governor rejection**: TB-Price-Move-Floor is violated because the proposed min_price_move of 0.04 relaxes the hardened global floor of min_price_move ≥ 0.05 / spike_min_price_move ≥ 0.05, which is explicitly prohibited for the low-liquidity/watch-tier/NBA-series regimes. TB-Score-Gate-Minimum is also violated because score_threshold is set to None, but the historical constraints require an explicit non-None score gate with a live minimum of ≥ 2.2.
- [ ] **TB-612** `rejected` — Increase spike_min_price_move so small 2%-3% drift does not qualify unless it is part of a stronger move.
  - **Governor rejection**: TB-Price-Move-Floor is violated because the proposed min_price_move of 0.04 relaxes the hardened global floor of min_price_move ≥ 0.05 / spike_min_price_move ≥ 0.05, which is explicitly prohibited for the low-liquidity/watch-tier/NBA-series regimes. TB-Score-Gate-Minimum is also violated because score_threshold is set to None, but the historical constraints require an explicit non-None score gate with a live minimum of ≥ 2.2.
- [ ] **TB-613** `rejected` — Keep spike_score_threshold unchanged for now; the pattern suggests a thresholding problem at the input gates, not just the final score.
  - **Governor rejection**: TB-Price-Move-Floor is violated because the proposed min_price_move of 0.04 relaxes the hardened global floor of min_price_move ≥ 0.05 / spike_min_price_move ≥ 0.05, which is explicitly prohibited for the low-liquidity/watch-tier/NBA-series regimes. TB-Score-Gate-Minimum is also violated because score_threshold is set to None, but the historical constraints require an explicit non-None score gate with a live minimum of ≥ 2.2.

---

## 2026-06-06 — Advisor snapshot 204

### Summary
Recent false positives are driven by quote-only or single-burst activity that produces modest price movement without durable traded confirmation, especially in late-stage CPI markets. The common pattern is high apparent volume with small-to-moderate price drift, which analysts repeatedly labeled noise or low-confidence signals.

### Next step
Raise the minimum price-move requirement and add a confirmation rule for actual traded volume/aggressive fills before emission; this targets the observed quote-spike false positives without suppressing genuinely informative flow.

### Suggested thresholds
`min_volume_delta` → `30000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-614** `rejected` — Increase spike_min_price_move to 0.04 to require a more meaningful directional move before triggering.
  - **Governor rejection**: TB-001 / TB-002 / TB-004 conflict: the proposed `min_price_move: 0.04` relaxes the historically enforced hard floor of `min_price_move >= 0.05`, which was explicitly tightened to reject sub-5% confirmation in spike detection. Because this is a late-stage CPI / low-liquidity quote-noise context, the historical constraints also require stronger confirmation against quote-only bursts, so lowering the price floor to 0.04 conflicts with the prior regression-prevention rules. In addition, `score_threshold: None` violates the global hard floor requiring `score_threshold >= 2.2` with no `None` relaxations.
- [ ] **TB-615** `rejected` — Raise spike_min_volume_delta to 30000.0 to filter out smaller bursty events that are not sustained.
  - **Governor rejection**: TB-001 / TB-002 / TB-004 conflict: the proposed `min_price_move: 0.04` relaxes the historically enforced hard floor of `min_price_move >= 0.05`, which was explicitly tightened to reject sub-5% confirmation in spike detection. Because this is a late-stage CPI / low-liquidity quote-noise context, the historical constraints also require stronger confirmation against quote-only bursts, so lowering the price floor to 0.04 conflicts with the prior regression-prevention rules. In addition, `score_threshold: None` violates the global hard floor requiring `score_threshold >= 2.2` with no `None` relaxations.
- [ ] **TB-616** `rejected` — Require either multiple aggressive trades or confirmed order-fill volume in addition to the numeric thresholds for CPI markets.
  - **Governor rejection**: TB-001 / TB-002 / TB-004 conflict: the proposed `min_price_move: 0.04` relaxes the historically enforced hard floor of `min_price_move >= 0.05`, which was explicitly tightened to reject sub-5% confirmation in spike detection. Because this is a late-stage CPI / low-liquidity quote-noise context, the historical constraints also require stronger confirmation against quote-only bursts, so lowering the price floor to 0.04 conflicts with the prior regression-prevention rules. In addition, `score_threshold: None` violates the global hard floor requiring `score_threshold >= 2.2` with no `None` relaxations.

---

## 2026-06-06 — Advisor snapshot 205

### Summary
The false-positive pattern is dominated by low-volume, low-price-move signals that still pass the score filter. One recent analyst-confirmed signal had a strong volume jump and 5.3% move, while another analyst-confirmed signal with only 1% price move and trivial volume delta suggests the current gates are too permissive on price/volume alone.

### Next step
Raise the minimum price-move gate first, and use a modest volume floor to keep the detector focused on materially informative flow.

### Suggested thresholds
`min_volume_delta` → `1000.0`, `min_price_move` → `0.02`, `score_threshold` → `5.0`

### Recommendations

- [ ] **TB-617** `rejected` — Increase spike_min_price_move to 0.02 so 1% blips do not emit signals.
  - **Governor rejection**: The proposed tweak violates the historical price-floor constraint: TB-001 requires min_price_move ≥ 0.05, but the proposal lowers it to 0.02. It also conflicts with TB-001/TB-004 style anti-noise policy by relaxing the price confirmation that was explicitly tightened to suppress low-volume, low-move false positives. The proposed min_volume_delta and score_threshold do not offset that regression because the floor on price move is explicitly non-relaxable.
- [ ] **TB-618** `rejected` — Add or raise a volume floor near the upper end of recent low-signal noise, but keep it well below the large confirmed flow example.
  - **Governor rejection**: The proposed tweak violates the historical price-floor constraint: TB-001 requires min_price_move ≥ 0.05, but the proposal lowers it to 0.02. It also conflicts with TB-001/TB-004 style anti-noise policy by relaxing the price confirmation that was explicitly tightened to suppress low-volume, low-move false positives. The proposed min_volume_delta and score_threshold do not offset that regression because the floor on price move is explicitly non-relaxable.
- [ ] **TB-619** `rejected` — Slightly raise spike_score_threshold only after tightening the price gate, to avoid suppressing high-volume informative spikes.
  - **Governor rejection**: The proposed tweak violates the historical price-floor constraint: TB-001 requires min_price_move ≥ 0.05, but the proposal lowers it to 0.02. It also conflicts with TB-001/TB-004 style anti-noise policy by relaxing the price confirmation that was explicitly tightened to suppress low-volume, low-move false positives. The proposed min_volume_delta and score_threshold do not offset that regression because the floor on price move is explicitly non-relaxable.

---

## 2026-06-06 — Advisor snapshot 206

### Summary
The false positives are coming from signals that pair a modest price move with heavy volume churn, especially when analyst labels call for confirmation from more than one executed trade. A stricter volume-and-price gate should reduce noise without suppressing the clearly informative move in the strongest signal.

### Next step
Raise the minimum volume and price requirements together, and add a trade-count confirmation rule so quote churn alone cannot trigger a spike.

### Suggested thresholds
`min_volume_delta` → `120000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-620** `rejected` — Increase min_volume_delta to 120000.0 to filter the borderline churn-heavy alerts.
  - **Governor rejection**: The proposal violates the historical global floor on `score_threshold`: it sets `score_threshold` to `None`, but the constraint requires it to remain explicit and be ≥ 2.2. The proposed `min_price_move: 0.05` is compliant, and `min_volume_delta: 120000.0` does not by itself conflict with the stated floors.
- [ ] **TB-621** `rejected` — Increase min_price_move to 0.05 so small relative moves do not emit on volume alone.
  - **Governor rejection**: The proposal violates the historical global floor on `score_threshold`: it sets `score_threshold` to `None`, but the constraint requires it to remain explicit and be ≥ 2.2. The proposed `min_price_move: 0.05` is compliant, and `min_volume_delta: 120000.0` does not by itself conflict with the stated floors.
- [ ] **TB-622** `rejected` — Require at least 2 executed trades before emitting when score is near threshold.
  - **Governor rejection**: The proposal violates the historical global floor on `score_threshold`: it sets `score_threshold` to `None`, but the constraint requires it to remain explicit and be ≥ 2.2. The proposed `min_price_move: 0.05` is compliant, and `min_volume_delta: 120000.0` does not by itself conflict with the stated floors.

---

## 2026-06-06 — Advisor snapshot 207

### Summary
The false-positive pattern is a small price move with very large volume delta, which can still be labeled only uncertain/low-confidence unless there is broader trade confirmation. The current detector likely overweights quote/volume churn and underweights the need for executed-trade follow-through and stronger price displacement.

### Next step
Tighten the trigger so volume alone cannot emit a spike: require both a higher volume delta floor and a stronger price move, or gate emission on a minimum executed-trade count before the score threshold can fire.

### Suggested thresholds
`min_volume_delta` → `125000.0`, `min_price_move` → `0.05`, `score_threshold` → `4.5`

### Recommendations

- [x] **TB-623** `applied` — Raise the volume floor moderately to suppress churn-driven alerts.
- [x] **TB-624** `applied` — Increase the minimum price move so 4-5% moves are the new baseline for emission.
- [x] **TB-625** `applied` — Add a separate executed-trade confirmation rule; if that is unavailable, raise the score threshold slightly.

---

## 2026-06-06 — Advisor snapshot 208

### Summary
The false positives are coming from **large volume bursts without enough sustained price movement**, especially in politically illiquid markets where quote-driven activity can look like a spike. The one true signal shows that strong spikes are best confirmed by both meaningful volume and a larger price move, not volume alone.

### Next step
Tighten the detector to require a materially larger price move before emitting, and add a market-liquidity rule that raises the volume bar for politically illiquid markets.

### Suggested thresholds
`min_volume_delta` → `300000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-626** `rejected` — Raise **min_price_move** from 0.02 to **0.04** for watch-level alerts.
  - **Governor rejection**: The proposal violates the historical hard floor on price movement: `min_price_move: 0.04` relaxes the explicitly required `min_price_move` / `spike_min_price_move` floor of ≥ 0.05. It also violates the layered gating constraint by setting `score_threshold: None`, which conflicts with the requirement that `score_threshold` / `spike_score_threshold` be explicit and ≥ 2.2. The `min_volume_delta` value is explicit, so that part is not the conflict.
- [ ] **TB-627** `rejected` — Increase **min_volume_delta** modestly to **300000** for politically illiquid markets only.
  - **Governor rejection**: The proposal violates the historical hard floor on price movement: `min_price_move: 0.04` relaxes the explicitly required `min_price_move` / `spike_min_price_move` floor of ≥ 0.05. It also violates the layered gating constraint by setting `score_threshold: None`, which conflicts with the requirement that `score_threshold` / `spike_score_threshold` be explicit and ≥ 2.2. The `min_volume_delta` value is explicit, so that part is not the conflict.
- [ ] **TB-628** `rejected` — Keep **score_threshold** unchanged for now; the main failure mode is weak price confirmation, not low combined score.
  - **Governor rejection**: The proposal violates the historical hard floor on price movement: `min_price_move: 0.04` relaxes the explicitly required `min_price_move` / `spike_min_price_move` floor of ≥ 0.05. It also violates the layered gating constraint by setting `score_threshold: None`, which conflicts with the requirement that `score_threshold` / `spike_score_threshold` be explicit and ≥ 2.2. The `min_volume_delta` value is explicit, so that part is not the conflict.

---

## 2026-06-06 — Advisor snapshot 209

### Summary
The false positives are concentrated in politically illiquid markets where large volume bursts occur with little or no price follow-through. The clearest pattern is quote-driven or low-probability flow that should not trigger on volume alone.

### Next step
Raise the price-move requirement for alerts and pair it with a slightly higher volume floor, so volume spikes without meaningful price confirmation are suppressed.

### Suggested thresholds
`min_volume_delta` → `300000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-629** `rejected` — Increase spike_min_price_move to 0.03 to 0.04 so low-probability markets need a clearer move before emitting.
  - **Governor rejection**: TB-001 is violated because `min_price_move` is relaxed to 0.03, but the historical constraint requires `min_price_move ≥ 0.05` globally and explicitly forbids 0.03–0.04. TB-003 is also violated because `score_threshold` is set to `None`, but the historical constraint requires an explicit `score_threshold / spike_score_threshold ≥ 2.2` and forbids `None`.
- [ ] **TB-630** `rejected` — Increase spike_min_volume_delta modestly for watch-tier political markets to reduce quote-driven burst noise.
  - **Governor rejection**: TB-001 is violated because `min_price_move` is relaxed to 0.03, but the historical constraint requires `min_price_move ≥ 0.05` globally and explicitly forbids 0.03–0.04. TB-003 is also violated because `score_threshold` is set to `None`, but the historical constraint requires an explicit `score_threshold / spike_score_threshold ≥ 2.2` and forbids `None`.
- [ ] **TB-631** `rejected` — Keep spike_score_threshold unchanged unless you can separately confirm that score is not already dominated by volume in these cases.
  - **Governor rejection**: TB-001 is violated because `min_price_move` is relaxed to 0.03, but the historical constraint requires `min_price_move ≥ 0.05` globally and explicitly forbids 0.03–0.04. TB-003 is also violated because `score_threshold` is set to `None`, but the historical constraint requires an explicit `score_threshold / spike_score_threshold ≥ 2.2` and forbids `None`.

---

## 2026-06-06 — Advisor snapshot 210

### Summary
The false positives are dominated by quote- or liquidity-driven volume surges with little or no price movement, especially in very low-probability markets. The clean signal shows that meaningful spikes still have both strong volume and a sizable price move.

### Next step
Add a price-move floor specifically to guard against volume-only spikes; require both volume and price confirmation before emitting a signal.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-632** `rejected` — Raise the minimum price move from 0.00 to at least 0.03 to suppress volume-only noise.
  - **Governor rejection**: TB-global hard floors / TB-price confirmation are violated: the proposal sets `min_price_move: 0.03`, but the historical constraints require `min_price_move ≥ 0.05` and explicitly reject `0.03–0.04` price floors for spike emission. It also conflicts with the hard requirement that `min_volume_delta` remain explicit and non-`None`, and with the score gate rule that `score_threshold` must stay explicit and non-`None` (≥ 2.2), since the proposal sets both to `None`.
- [ ] **TB-633** `rejected` — Keep the volume threshold high for now; the bad case has extremely large volume but no price follow-through.
  - **Governor rejection**: TB-global hard floors / TB-price confirmation are violated: the proposal sets `min_price_move: 0.03`, but the historical constraints require `min_price_move ≥ 0.05` and explicitly reject `0.03–0.04` price floors for spike emission. It also conflicts with the hard requirement that `min_volume_delta` remain explicit and non-`None`, and with the score gate rule that `score_threshold` must stay explicit and non-`None` (≥ 2.2), since the proposal sets both to `None`.
- [ ] **TB-634** `rejected` — If you prefer a single combined-rule change, require sustained trade imbalance or multi-bar confirmation when price move is below the floor.
  - **Governor rejection**: TB-global hard floors / TB-price confirmation are violated: the proposal sets `min_price_move: 0.03`, but the historical constraints require `min_price_move ≥ 0.05` and explicitly reject `0.03–0.04` price floors for spike emission. It also conflicts with the hard requirement that `min_volume_delta` remain explicit and non-`None`, and with the score gate rule that `score_threshold` must stay explicit and non-`None` (≥ 2.2), since the proposal sets both to `None`.

---

## 2026-06-06 — Advisor snapshot 211

### Summary
The false positives are dominated by **volume-led spikes without enough confirming price movement**, especially in thin or very low-probability markets. Analyst notes repeatedly ask for stronger confirmation beyond quoted volume, pointing to a need for tighter price-move gating and/or trade-quality confirmation.

### Next step
Add a **price-confirmation floor** so volume spikes only emit when paired with a materially larger price move, and use a trade-imbalance or executed-trade confirmation rule for low-probability markets.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-635** `rejected` — Raise **spike_min_price_move** from 0.03 to **0.05** to suppress quote-driven noise with little directional follow-through.
  - **Governor rejection**: The proposed tweak violates the historical no-relaxation rule by setting `min_volume_delta` to `None` and `score_threshold` to `None`. This conflicts with the global hard floors that require `min_volume_delta` to be explicit/non-`None` and `score_threshold ≥ 2.2` and non-`None`, and with the prior rejection of any unset `min_volume_delta` or `score_threshold`.
- [ ] **TB-636** `rejected` — Increase **spike_min_volume_delta** modestly from the current level only if the spike also lacks executed-trade confirmation; otherwise keep volume permissive to avoid muting informative flow.
  - **Governor rejection**: The proposed tweak violates the historical no-relaxation rule by setting `min_volume_delta` to `None` and `score_threshold` to `None`. This conflicts with the global hard floors that require `min_volume_delta` to be explicit/non-`None` and `score_threshold ≥ 2.2` and non-`None`, and with the prior rejection of any unset `min_volume_delta` or `score_threshold`.
- [ ] **TB-637** `rejected` — Require **both** a price move and a meaningful executed-trade imbalance for markets with yes-probability below about 0.10.
  - **Governor rejection**: The proposed tweak violates the historical no-relaxation rule by setting `min_volume_delta` to `None` and `score_threshold` to `None`. This conflicts with the global hard floors that require `min_volume_delta` to be explicit/non-`None` and `score_threshold ≥ 2.2` and non-`None`, and with the prior rejection of any unset `min_volume_delta` or `score_threshold`.

---

## 2026-06-06 — Advisor snapshot 212

### Summary
False positives cluster in thin or low-dispersion markets where large volume bursts or quote moves are not matched by meaningful executed trading or sustained price movement. The analyst notes repeatedly call for higher price-move and volume requirements, especially for ultra-low-priced or CPI-style contracts.

### Next step
Tighten the detector by requiring both a larger fractional price move and evidence of executed trades, with the biggest immediate gain coming from raising the price-move floor for thin/low-priced markets.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-638** `rejected` — Raise spike_min_price_move to 0.05 for low-dispersion or ultra-low-priced markets, while keeping a separate lower tier for truly high-conviction flow.
  - **Governor rejection**: TB-003 / TB-006 violation: the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical hard floor requiring `score_threshold ≥ 2.2` and explicit/non-`None`. The other suggested values (`min_price_move: 0.05`, `min_volume_delta: 5000.0`) do not conflict with the stated floors.
- [ ] **TB-639** `rejected` — Increase spike_min_volume_delta to 5000 as a first-pass filter for thin markets to suppress quote-only bursts.
  - **Governor rejection**: TB-003 / TB-006 violation: the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical hard floor requiring `score_threshold ≥ 2.2` and explicit/non-`None`. The other suggested values (`min_price_move: 0.05`, `min_volume_delta: 5000.0`) do not conflict with the stated floors.
- [ ] **TB-640** `rejected` — Add a rule that at least 2 executed trades must occur within the detection window before emitting a spike signal.
  - **Governor rejection**: TB-003 / TB-006 violation: the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical hard floor requiring `score_threshold ≥ 2.2` and explicit/non-`None`. The other suggested values (`min_price_move: 0.05`, `min_volume_delta: 5000.0`) do not conflict with the stated floors.

---

## 2026-06-06 — Advisor snapshot 213

### Summary
The false positives cluster around thin or quote-driven CPI-style moves where price changes are modest or extreme-price markets get flagged without enough executed-trade confirmation. The pattern suggests the detector is too sensitive to volume bursts alone and should demand both stronger price movement and trade confirmation.

### Next step
Raise the minimum price-move threshold and add an executed-trade confirmation rule before emitting a signal.

### Suggested thresholds
`min_volume_delta` → `100000.0`, `min_price_move` → `0.05`, `score_threshold` → `4.0`

### Recommendations

- [x] **TB-641** `applied` — Increase spike_min_price_move from 0.03 to 0.05 to suppress low-quality CPI noise while keeping larger dislocations.
- [x] **TB-642** `applied` — Raise spike_min_volume_delta to about 100000 for CPI-style markets, or require a meaningful executed-trade count alongside volume delta.
- [x] **TB-643** `applied` — Lift spike_score_threshold modestly to 4.0 so borderline volume-only bursts do not trigger alerts.

---

## 2026-06-06 — Advisor snapshot 214

### Summary
The false positives cluster in thin, far-dated or low-dispersion markets where large volume deltas and modest price moves can still be quote-driven or otherwise non-executed flow. Analyst notes repeatedly ask for confirmation from executed trades, sustained/multi-trade flow, and higher price-move requirements before emission.

### Next step
Add a trade-confirmation gate and raise the price-move floor for thin markets; if only one numeric change is made, increase spike_min_price_move first and require executed-trade confirmation as a separate rule.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-644** `rejected` — Raise minimum traded volume for long-dated Fed/CPI-style contracts, especially where analyst labels show uncertainty or noise.
  - **Governor rejection**: TB-XXX hard floor violation: the proposed tweak sets score_threshold to None, but historical constraints explicitly require score_threshold to be explicit/non-None and >= 2.2, and also prohibit null relaxations for score_threshold. The min_price_move value of 0.05 is compliant, and min_volume_delta=20000.0 is explicit, but the None score_threshold conflicts with the prior tightened floor.
- [ ] **TB-645** `rejected` — Require at least 2 executed trades or sustained flow before a spike can emit, instead of reacting to quote-driven bursts alone.
  - **Governor rejection**: TB-XXX hard floor violation: the proposed tweak sets score_threshold to None, but historical constraints explicitly require score_threshold to be explicit/non-None and >= 2.2, and also prohibit null relaxations for score_threshold. The min_price_move value of 0.05 is compliant, and min_volume_delta=20000.0 is explicit, but the None score_threshold conflicts with the prior tightened floor.
- [ ] **TB-646** `rejected` — Increase the price-move threshold modestly to filter low-dispersion markets with already-extreme prices; keep the score threshold as a secondary backstop rather than the primary filter.
  - **Governor rejection**: TB-XXX hard floor violation: the proposed tweak sets score_threshold to None, but historical constraints explicitly require score_threshold to be explicit/non-None and >= 2.2, and also prohibit null relaxations for score_threshold. The min_price_move value of 0.05 is compliant, and min_volume_delta=20000.0 is explicit, but the None score_threshold conflicts with the prior tightened floor.

---

## 2026-06-06 — Advisor snapshot 215

### Summary
The false positives cluster in thin or far-dated contracts where large quoted moves and volume bursts are not necessarily trade-confirmed. Analyst notes repeatedly point to requiring executed-trade confirmation, higher volume floors, and stronger price-move filters to avoid quote-driven spikes.

### Next step
Add a trade-confirmation rule for spikes: only emit when the move is supported by multiple executed trades or sustained flow, and raise both the volume and price-move floors for thin/far-dated markets.

### Suggested thresholds
`min_volume_delta` → `10000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-647** `rejected` — Raise spike_min_volume_delta to 10000.0 for far-dated Fed-style contracts and thin CPI-style markets.
  - **Governor rejection**: TB-001 / Global floors and no-null relaxations are violated because the proposal sets score_threshold to None, but historical constraints require score_threshold to be explicit/non-None and ≥ 2.2. The proposed min_price_move = 0.05 and min_volume_delta = 10000.0 do not conflict with the stated floors.
- [ ] **TB-648** `rejected` — Raise spike_min_price_move to 0.05 to suppress small quote-driven moves while preserving the larger analyst-confirmed signals.
  - **Governor rejection**: TB-001 / Global floors and no-null relaxations are violated because the proposal sets score_threshold to None, but historical constraints require score_threshold to be explicit/non-None and ≥ 2.2. The proposed min_price_move = 0.05 and min_volume_delta = 10000.0 do not conflict with the stated floors.
- [ ] **TB-649** `rejected` — Require at least 2 executed trades, or an equivalent sustained-flow condition, before emitting a spike signal.
  - **Governor rejection**: TB-001 / Global floors and no-null relaxations are violated because the proposal sets score_threshold to None, but historical constraints require score_threshold to be explicit/non-None and ≥ 2.2. The proposed min_price_move = 0.05 and min_volume_delta = 10000.0 do not conflict with the stated floors.

---

## 2026-06-06 — Advisor snapshot 216

### Summary
The false positives are concentrated in thin, far-dated Fed markets where large quote-driven moves can trigger signals even when analyst labels say the flow is unclear or noisy. The recent labels consistently suggest tightening both volume and price confirmation, with a preference for trade-confirmed sustained flow over one-shot spikes.

### Next step
Raise the detector’s volume floor and require sustained, trade-confirmed participation before emitting a spike, especially for long-dated Fed contracts.

### Suggested thresholds
`min_volume_delta` → `12000.0`, `min_price_move` → `0.4`

### Recommendations

- [ ] **TB-650** `rejected` — Increase spike_min_volume_delta to filter thin-market noise.
  - **Governor rejection**: TB-Global score floor is violated because the proposed tweak sets `score_threshold` to `None`, but the historical constraints require `score_threshold` to remain explicit/non-`None` and at least 2.2. The proposed `min_volume_delta: 12000.0` and `min_price_move: 0.4` do not conflict with the stated floors.
- [ ] **TB-651** `rejected` — Increase spike_min_price_move so only more material moves qualify.
  - **Governor rejection**: TB-Global score floor is violated because the proposed tweak sets `score_threshold` to `None`, but the historical constraints require `score_threshold` to remain explicit/non-`None` and at least 2.2. The proposed `min_volume_delta: 12000.0` and `min_price_move: 0.4` do not conflict with the stated floors.
- [ ] **TB-652** `rejected` — Add a trade-confirmation rule: require multiple trades or sustained flow, not quote-only movement.
  - **Governor rejection**: TB-Global score floor is violated because the proposed tweak sets `score_threshold` to `None`, but the historical constraints require `score_threshold` to remain explicit/non-`None` and at least 2.2. The proposed `min_volume_delta: 12000.0` and `min_price_move: 0.4` do not conflict with the stated floors.

---

## 2026-06-06 — Advisor snapshot 217

### Summary
Recent false positives cluster in low-liquidity, quote-driven macro markets where modest price flickers or passive re-quoting are being classified as spikes. The strongest pattern is that analysts want more evidence of executed trade flow and sustained movement before emitting signals.

### Next step
Tighten the detector with a trade-confirmation rule for quote-only markets: require executed trades or sustained price movement before a spike can fire, rather than relying on price/quote changes alone.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-653** `rejected` — Raise the minimum traded-volume change for low-liquidity CPI/Fed markets to suppress quote-only flickers.
  - **Governor rejection**: TB-HF-001 is violated because the proposed tweak sets `score_threshold` to `None`, which is a prohibited null relaxation under the historical global hard floors requiring `score_threshold ≥ 2.2` with no null relaxations. The proposal is otherwise aligned with trade-confirmation tightening, but the null score threshold directly conflicts with the historical constraint.
- [ ] **TB-654** `rejected` — Require multiple executed trades or sustained flow over a short window before flagging far-dated macro markets.
  - **Governor rejection**: TB-HF-001 is violated because the proposed tweak sets `score_threshold` to `None`, which is a prohibited null relaxation under the historical global hard floors requiring `score_threshold ≥ 2.2` with no null relaxations. The proposal is otherwise aligned with trade-confirmation tightening, but the null score threshold directly conflicts with the historical constraint.
- [ ] **TB-655** `rejected` — Increase the price-move bar slightly for quote-driven alerts so a brief 3% move does not trigger a signal by itself.
  - **Governor rejection**: TB-HF-001 is violated because the proposed tweak sets `score_threshold` to `None`, which is a prohibited null relaxation under the historical global hard floors requiring `score_threshold ≥ 2.2` with no null relaxations. The proposal is otherwise aligned with trade-confirmation tightening, but the null score threshold directly conflicts with the historical constraint.

---

## 2026-06-06 — Advisor snapshot 218

### Summary
The false positives are concentrated in low-liquidity, quote-driven CPI moves where modest price flickers and large volume deltas were labeled as noise/unclear. The FED examples indicate that genuinely informative flow can still appear at substantial volume and large price moves, so the fix should target quote-only micro-spikes rather than broadly raising sensitivity.

### Next step
Add a rule requiring executed-trade confirmation for quote-only markets, and only emit without that confirmation if price move is materially larger.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-656** `rejected` — Increase the minimum traded-volume delta for quote-only macro markets to suppress passive re-quoting.
  - **Governor rejection**: TB-001 / Global hard floors and TB-003 / score_threshold conflict: the proposal sets score_threshold to None, but historical constraints require spike_score_threshold to be explicit and >= 2.2 and never None. The proposal also introduces an executed-trade confirmation rule only for quote-only markets, which is compatible, but the missing score threshold violates the explicit hard-floor requirement.
- [ ] **TB-657** `rejected` — Raise the minimum price move for quote-only triggers from 3% to about 5%.
  - **Governor rejection**: TB-001 / Global hard floors and TB-003 / score_threshold conflict: the proposal sets score_threshold to None, but historical constraints require spike_score_threshold to be explicit and >= 2.2 and never None. The proposal also introduces an executed-trade confirmation rule only for quote-only markets, which is compatible, but the missing score threshold violates the explicit hard-floor requirement.
- [ ] **TB-658** `rejected` — Keep the score threshold unchanged for now; the cleaner lever is a quote-only execution filter.
  - **Governor rejection**: TB-001 / Global hard floors and TB-003 / score_threshold conflict: the proposal sets score_threshold to None, but historical constraints require spike_score_threshold to be explicit and >= 2.2 and never None. The proposal also introduces an executed-trade confirmation rule only for quote-only markets, which is compatible, but the missing score threshold violates the explicit hard-floor requirement.

---

## 2026-06-06 — Advisor snapshot 219

### Summary
The false positives cluster around **quote-only or passive re-quoting moves** in low-liquidity CPI markets: the detector is firing on meaningful-looking price/volume deltas that analysts judged as noise or uncertain when there was no clear executed-trade confirmation. The pattern suggests the current trigger is too sensitive to transient price flickers and quote updates.

### Next step
Require **executed-trade confirmation** for quote-driven spikes in low-liquidity macro markets; if that is not available, raise the trigger bar materially by increasing both minimum volume delta and minimum sustained price move.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-659** `rejected` — Increase **spike_min_volume_delta** to about **15000** so smaller quote-driven bursts like the 11072.56 watch-case do not trigger as readily.
  - **Governor rejection**: TB-XXX violated: the proposed tweak sets `score_threshold` to `None`, which relaxes an explicitly tightened floor (`score_threshold ≥ 2.2`) under the historical active floors and watch/low-liquidity hardening rules. The other proposed values (`min_price_move = 0.05`, `min_volume_delta = 15000.0`) do not conflict on their face, but removing the score threshold conflicts with the requirement not to relax it to `None` or below the floor.
- [ ] **TB-660** `rejected` — Increase **spike_min_price_move** to about **0.05** to filter out 3% flickers that analysts labeled as likely false positives.
  - **Governor rejection**: TB-XXX violated: the proposed tweak sets `score_threshold` to `None`, which relaxes an explicitly tightened floor (`score_threshold ≥ 2.2`) under the historical active floors and watch/low-liquidity hardening rules. The other proposed values (`min_price_move = 0.05`, `min_volume_delta = 15000.0`) do not conflict on their face, but removing the score threshold conflicts with the requirement not to relax it to `None` or below the floor.
- [ ] **TB-661** `rejected` — Keep **spike_score_threshold** unchanged unless you cannot add trade-confirmation logic; if you must tune it, raise it modestly by about **15-20%** rather than making a large jump.
  - **Governor rejection**: TB-XXX violated: the proposed tweak sets `score_threshold` to `None`, which relaxes an explicitly tightened floor (`score_threshold ≥ 2.2`) under the historical active floors and watch/low-liquidity hardening rules. The other proposed values (`min_price_move = 0.05`, `min_volume_delta = 15000.0`) do not conflict on their face, but removing the score threshold conflicts with the requirement not to relax it to `None` or below the floor.

---

## 2026-06-06 — Advisor snapshot 220

### Summary
The false positives cluster around quote-driven, low-liquidity rate markets where large apparent price moves are not backed by enough executed volume or sustained follow-through. Analyst notes consistently point to tightening the volume and persistence requirements rather than raising the score gate alone.

### Next step
Increase the minimum executed-volume requirement and add a trade-count or sustained-follow-through rule for low-liquidity/quote-driven markets before triggering on a spike.

### Suggested thresholds
`min_volume_delta` → `10000.0`, `min_price_move` → `0.03`

### Recommendations

- [x] **TB-662** `applied` — Raise the minimum traded-volume floor for this market family to filter one-tick quote jumps that reverse immediately.
- [x] **TB-663** `applied` — Require sustained price impact across multiple trades, not just a single large move, before emitting a signal.
- [x] **TB-664** `applied` — Prefer a volume-to-quote-change imbalance check and discount spikes dominated by quote updates over executed prints.

---

## 2026-06-06 — Advisor snapshot 221

### Summary
The false positives are concentrated in thin, quote-driven macro markets where large-looking price moves are not backed by enough executed trade volume or trade count. Several labeled signals indicate that the detector is firing on transient spikes with immediate mean reversion rather than sustained informational flow.

### Next step
Raise the minimum executed-volume requirement and add a trade-count/sustained-move gate for low-liquidity markets, rather than relying on price move alone.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-665** `rejected` — Increase spike_min_volume_delta to filter out quote-driven moves with weak execution backing.
  - **Governor rejection**: TB-001 is violated because the proposed `min_price_move: 0.04` relaxes the explicitly enforced global hard floor of `min_price_move ≥ 0.05`, and the historical constraints explicitly forbid 0.03–0.04 price thresholds in thin/quote-driven/high-odds markets. TB-001 is also violated because `score_threshold: None` conflicts with the requirement that `score_threshold ≥ 2.2` be explicit/non-`None` with no null relaxations.
- [ ] **TB-666** `rejected` — Increase spike_min_price_move modestly so single-tick or one-leg jumps do not trigger alerts.
  - **Governor rejection**: TB-001 is violated because the proposed `min_price_move: 0.04` relaxes the explicitly enforced global hard floor of `min_price_move ≥ 0.05`, and the historical constraints explicitly forbid 0.03–0.04 price thresholds in thin/quote-driven/high-odds markets. TB-001 is also violated because `score_threshold: None` conflicts with the requirement that `score_threshold ≥ 2.2` be explicit/non-`None` with no null relaxations.
- [ ] **TB-667** `rejected` — Add a persistence rule: require the price move to hold across multiple trades before emitting a signal.
  - **Governor rejection**: TB-001 is violated because the proposed `min_price_move: 0.04` relaxes the explicitly enforced global hard floor of `min_price_move ≥ 0.05`, and the historical constraints explicitly forbid 0.03–0.04 price thresholds in thin/quote-driven/high-odds markets. TB-001 is also violated because `score_threshold: None` conflicts with the requirement that `score_threshold ≥ 2.2` be explicit/non-`None` with no null relaxations.

---

## 2026-06-06 — Advisor snapshot 222

### Summary
The false positives are concentrated in low-liquidity, quote-driven macro markets where small price moves and large quoted volume deltas are being mistaken for actionable spikes. Analyst labels consistently call for requiring executed trades and sustained price impact, not just quote updates or one-tick moves.

### Next step
Add a trade-confirmation rule and raise the price-move floor for thin macro markets; this is the single best way to suppress quote-only noise without broadly muting informative flow.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-668** `rejected` — Require at least one recent executed trade before emitting a spike signal.
  - **Governor rejection**: TB-NULL-01 is violated because the proposed tweak sets min_score_threshold to None, which conflicts with the historical constraint that score_threshold must remain explicit/non-None and never be relaxed to None.
- [ ] **TB-669** `rejected` — Increase the minimum fractional price move to 0.05 for low-liquidity macro markets.
  - **Governor rejection**: TB-NULL-01 is violated because the proposed tweak sets min_score_threshold to None, which conflicts with the historical constraint that score_threshold must remain explicit/non-None and never be relaxed to None.
- [ ] **TB-670** `rejected` — Raise the volume-delta gate modestly so quote-only bursts must clear a higher bar before scoring.
  - **Governor rejection**: TB-NULL-01 is violated because the proposed tweak sets min_score_threshold to None, which conflicts with the historical constraint that score_threshold must remain explicit/non-None and never be relaxed to None.

---

## 2026-06-06 — Advisor snapshot 223

### Summary
Recent analyst labels show a consistent false-positive pattern in low-liquidity, quote-driven macro/rate markets: spikes are being triggered by modest price moves and large quote churn rather than durable executed trading. Several cases also revert quickly, suggesting the detector is too sensitive to short-lived price changes without enough trade confirmation.

### Next step
Require stronger execution confirmation before emitting a spike: raise the minimum price-move threshold slightly and add a trade-volume/trade-count gate so quote-only movement cannot pass alone.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-671** `rejected` — Increase spike_min_price_move from 0.03 to 0.05 for low-liquidity macro/rate markets.
  - **Governor rejection**: TB-Global hard floors is violated because the proposed tweak sets `min_volume_delta: None` and `score_threshold: None`, but the historical constraints require `min_volume_delta` to be explicit/non-`None` and `score_threshold ≥ 2.2` with no `None` relaxations. The proposed change also conflicts with the low-liquidity execution-quality and trade-count gates because it adds stronger execution confirmation conceptually, but does not actually specify a trade-volume/trade-count floor, leaving quote-only movement able to pass alone.
- [ ] **TB-672** `rejected` — Add a rule that at least one recent executed trade must be present before a spike can emit.
  - **Governor rejection**: TB-Global hard floors is violated because the proposed tweak sets `min_volume_delta: None` and `score_threshold: None`, but the historical constraints require `min_volume_delta` to be explicit/non-`None` and `score_threshold ≥ 2.2` with no `None` relaxations. The proposed change also conflicts with the low-liquidity execution-quality and trade-count gates because it adds stronger execution confirmation conceptually, but does not actually specify a trade-volume/trade-count floor, leaving quote-only movement able to pass alone.
- [ ] **TB-673** `rejected` — Raise the effective volume filter for these markets by requiring a larger traded-volume multiple relative to quote updates; if you need a numeric starting point, try doubling the current minimum volume delta.
  - **Governor rejection**: TB-Global hard floors is violated because the proposed tweak sets `min_volume_delta: None` and `score_threshold: None`, but the historical constraints require `min_volume_delta` to be explicit/non-`None` and `score_threshold ≥ 2.2` with no `None` relaxations. The proposed change also conflicts with the low-liquidity execution-quality and trade-count gates because it adds stronger execution confirmation conceptually, but does not actually specify a trade-volume/trade-count floor, leaving quote-only movement able to pass alone.

---

## 2026-06-06 — Advisor snapshot 224

### Summary
The false positives are concentrated in thin, low-liquidity macro markets where quote churn or one-tick moves trigger alerts without enough executed trading or sustained price follow-through. Analyst labels consistently ask for stronger confirmation from traded volume, multi-trade persistence, and a larger minimum price move before emitting signals.

### Next step
Increase the price-move floor and require stronger executed-volume confirmation before emission, with the biggest gain coming from filtering quote-driven spikes rather than lowering sensitivity uniformly.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-674** `rejected` — Raise spike_min_price_move to 0.05 for thin CPI/FED-style markets so 1–3% quote noise does not trigger alerts.
  - **Governor rejection**: The proposal violates the historical constraint that **min_volume_delta must remain explicit and non-None**. Setting `min_volume_delta: None` conflicts with the active volume gate and would relax a previously tightened confirmation requirement. It also violates the score gate because `score_threshold` must remain explicit and non-None, with a global floor of at least 2.2.
- [ ] **TB-675** `rejected` — Add a trade-confirmation rule: require at least 2 executed trades or a minimum executed-volume multiple before alerting on watch/notable tiers.
  - **Governor rejection**: The proposal violates the historical constraint that **min_volume_delta must remain explicit and non-None**. Setting `min_volume_delta: None` conflicts with the active volume gate and would relax a previously tightened confirmation requirement. It also violates the score gate because `score_threshold` must remain explicit and non-None, with a global floor of at least 2.2.
- [ ] **TB-676** `rejected` — Keep score_threshold unchanged for now and tighten the structural filters first, since the errors are driven more by weak confirmation than by low combined scores.
  - **Governor rejection**: The proposal violates the historical constraint that **min_volume_delta must remain explicit and non-None**. Setting `min_volume_delta: None` conflicts with the active volume gate and would relax a previously tightened confirmation requirement. It also violates the score gate because `score_threshold` must remain explicit and non-None, with a global floor of at least 2.2.

---

## 2026-06-06 — Advisor snapshot 225

### Summary
The false positives are concentrated in thin, quote-driven macro markets where volume spikes and small price moves trigger alerts but analysts label them noise. Several signals show immediate mean reversion or quote-only churn, suggesting the detector is too sensitive to volume without enough confirmed price continuation or executed trading.

### Next step
Tighten the detector by requiring both a larger minimum price move and stronger executed-volume confirmation before emitting, with the biggest gain likely from raising the price-move floor and the volume floor together.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.05`, `score_threshold` → `28.0`

### Recommendations

- [x] **TB-677** `applied` — Raise min_price_move to 0.05 to suppress quote-only and one-tick spikes in low-liquidity markets.
- [x] **TB-678** `applied` — Raise min_volume_delta to 5000.0 so alerts require more substantial activity than the current thin-market bursts.
- [x] **TB-679** `applied` — Increase score_threshold modestly to 28.0 to filter marginal cases while preserving the clearly informative high-score moves.

---

## 2026-06-06 — Advisor snapshot 226

### Summary
The false positives are concentrated in thin, low-liquidity CPI markets where quote-driven or small price moves are being promoted despite weak execution confirmation. The analyst notes consistently ask for a larger volume multiple plus a minimum price move and/or at least one real trade before signaling.

### Next step
Tighten the detector to require both a larger executed-volume move and a non-trivial price move before emitting on thin macro markets, rather than relying on quote churn or volume alone.

### Suggested thresholds
`min_volume_delta` → `4000.0`, `min_price_move` → `0.05`

### Recommendations

- [x] **TB-680** `applied` — Raise min_price_move to 0.05 for CPI watch/notable alerts on low-liquidity names.
- [x] **TB-681** `applied` — Raise min_volume_delta to 4000 for low-liquidity macro-market spikes.
- [x] **TB-682** `applied` — Add a rule that quote-only movement cannot emit unless there is at least one executed trade and score exceeds the current threshold.

---

## 2026-06-06 — Advisor snapshot 227

### Summary
The false positives are concentrated in thin/low-liquidity macro markets where volume spikes and quote churn are being promoted without enough real price movement or executed-trade confirmation. Analyst labels consistently point to requiring stronger volume confirmation and a non-trivial price move before emitting signals.

### Next step
Tighten the rule so a spike must clear both a higher volume bar and a minimum price move, with an executed-trade confirmation for watch-tier alerts in low-liquidity macro markets.

### Suggested thresholds
`min_volume_delta` → `3500.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-683** `rejected` — Raise the minimum price-move gate to filter out quote churn that lacks directional follow-through.
  - **Governor rejection**: TB-GLOBAL-03 / TB-GLOBAL-04: the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical hard floor that `score_threshold` must be explicit and >= 2.2. The price and volume floors themselves are not conflicting, but nulling the score gate is a prohibited relaxation. Also, for the stated low-liquidity/watch-tier context, historical constraints require executed-trade confirmation and stronger trade-count/persistence gates; the proposed tweak mentions executed-trade confirmation only in the recommendation text, but does not encode those required gates in the thresholds, so it does not fully satisfy the combined-gate constraints.
- [ ] **TB-684** `rejected` — Increase the volume threshold for watch-tier alerts by requiring a larger relative volume multiple, not just absolute delta.
  - **Governor rejection**: TB-GLOBAL-03 / TB-GLOBAL-04: the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical hard floor that `score_threshold` must be explicit and >= 2.2. The price and volume floors themselves are not conflicting, but nulling the score gate is a prohibited relaxation. Also, for the stated low-liquidity/watch-tier context, historical constraints require executed-trade confirmation and stronger trade-count/persistence gates; the proposed tweak mentions executed-trade confirmation only in the recommendation text, but does not encode those required gates in the thresholds, so it does not fully satisfy the combined-gate constraints.
- [ ] **TB-685** `rejected` — Add a trade-execution requirement for low-liquidity macro markets so quote-only moves do not emit signals.
  - **Governor rejection**: TB-GLOBAL-03 / TB-GLOBAL-04: the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical hard floor that `score_threshold` must be explicit and >= 2.2. The price and volume floors themselves are not conflicting, but nulling the score gate is a prohibited relaxation. Also, for the stated low-liquidity/watch-tier context, historical constraints require executed-trade confirmation and stronger trade-count/persistence gates; the proposed tweak mentions executed-trade confirmation only in the recommendation text, but does not encode those required gates in the thresholds, so it does not fully satisfy the combined-gate constraints.

---

## 2026-06-06 — Advisor snapshot 228

### Summary
The false positives are concentrated in thin macro markets where a large volume delta alone can trigger alerts even when price is flat or the move is mostly quote churn. The analyst labels suggest the detector needs stricter confirmation from price movement and/or repeated trade evidence before emitting a signal.

### Next step
Add a minimum price-move confirmation on top of volume, and raise the volume requirement slightly so thin-market churn no longer triggers watch-tier signals by itself.

### Suggested thresholds
`min_volume_delta` → `4000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-686** `rejected` — Raise spike_min_price_move from 0.00 to 0.03 so flat-price volume bursts do not fire.
  - **Governor rejection**: TB-001 / global hard floors is violated because the proposed `min_price_move: 0.03` relaxes the explicitly required floor `min_price_move ≥ 0.05`. The proposal also conflicts with the repeated rejection of 0.03–0.04 price floors, which were not allowed as a noise fix.
- [ ] **TB-687** `rejected` — Increase spike_min_volume_delta from 1994.0 to 4000.0 to require more substantial participation before a signal.
  - **Governor rejection**: TB-001 / global hard floors is violated because the proposed `min_price_move: 0.03` relaxes the explicitly required floor `min_price_move ≥ 0.05`. The proposal also conflicts with the repeated rejection of 0.03–0.04 price floors, which were not allowed as a noise fix.
- [ ] **TB-688** `rejected` — Keep spike_score_threshold unchanged for now; the main issue is missing confirmation, not overall score calibration.
  - **Governor rejection**: TB-001 / global hard floors is violated because the proposed `min_price_move: 0.03` relaxes the explicitly required floor `min_price_move ≥ 0.05`. The proposal also conflicts with the repeated rejection of 0.03–0.04 price floors, which were not allowed as a noise fix.

---

## 2026-06-06 — Advisor snapshot 229

### Summary
The false positive pattern is a low-volume, quote-only move that can still clear the current score and price thresholds. The informative signal has much higher volume at a similar price move, so volume or execution quality should be weighted more heavily than price alone.

### Next step
Raise the volume floor and add an execution-quality gate for low-volume markets, rather than broadly increasing the price-move threshold.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-689** `rejected` — Increase spike_min_volume_delta to exclude small quote-driven moves like the false positive while preserving the high-volume signal.
  - **Governor rejection**: TB-001 and TB-002 are violated because the proposed tweak sets `score_threshold` to `None`, which conflicts with the explicit hard floor requiring `score_threshold ≥ 2.2` and forbids nulls. In addition, TB-001 requires `min_volume_delta` to remain explicit/non-`None`; while `5000.0` is explicit, the proposal is still conflicting because it removes the score gate entirely rather than keeping it active as a secondary brake.
- [ ] **TB-690** `rejected` — Keep spike_min_price_move near the current level so genuine medium-sized moves are not muted.
  - **Governor rejection**: TB-001 and TB-002 are violated because the proposed tweak sets `score_threshold` to `None`, which conflicts with the explicit hard floor requiring `score_threshold ≥ 2.2` and forbids nulls. In addition, TB-001 requires `min_volume_delta` to remain explicit/non-`None`; while `5000.0` is explicit, the proposal is still conflicting because it removes the score gate entirely rather than keeping it active as a secondary brake.
- [ ] **TB-691** `rejected` — Require a nonzero executed-trade imbalance or equivalent trade-confirmation rule when volume is below the new floor.
  - **Governor rejection**: TB-001 and TB-002 are violated because the proposed tweak sets `score_threshold` to `None`, which conflicts with the explicit hard floor requiring `score_threshold ≥ 2.2` and forbids nulls. In addition, TB-001 requires `min_volume_delta` to remain explicit/non-`None`; while `5000.0` is explicit, the proposal is still conflicting because it removes the score gate entirely rather than keeping it active as a secondary brake.

---

## 2026-06-06 — Advisor snapshot 230

### Summary
The false positives cluster around **small or low-quality price moves** that are paired with enough volume to trip the detector, especially in low-volume Kalshi-style markets. Analyst labels suggest the current trigger is too sensitive when there is only a modest price change or a quote-only move, while a larger move with substantial volume can still be a real signal.

### Next step
Raise the **price-move floor** and add a **liquidity/imbalance confirmation rule** before changing the volume threshold globally.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-692** `rejected` — Increase spike_min_price_move to **0.03** so 2% moves no longer trigger on volume alone.
  - **Governor rejection**: TB-001 / Global floors is violated because the proposed `min_price_move: 0.03` relaxes the historically tightened floor below the required `min_price_move ≥ 0.05`, which was explicitly hardened to treat sub-5% moves as noise. TB-002 / Global floors is also violated because `min_volume_delta` is set to `None`, but the historical constraints require `min_volume_delta` to be explicit and non-`None`. TB-003 / Global floors is violated because `score_threshold` is set to `None`, but the historical constraints require `score_threshold ≥ 2.2` and non-`None`.
- [ ] **TB-693** `rejected` — Require a **nonzero executed-trade imbalance** or equivalent trade-confirmation check for low-volume markets with quote-only movement.
  - **Governor rejection**: TB-001 / Global floors is violated because the proposed `min_price_move: 0.03` relaxes the historically tightened floor below the required `min_price_move ≥ 0.05`, which was explicitly hardened to treat sub-5% moves as noise. TB-002 / Global floors is also violated because `min_volume_delta` is set to `None`, but the historical constraints require `min_volume_delta` to be explicit and non-`None`. TB-003 / Global floors is violated because `score_threshold` is set to `None`, but the historical constraints require `score_threshold ≥ 2.2` and non-`None`.
- [ ] **TB-694** `rejected` — Keep spike_min_volume_delta unchanged for now; the cleanest filter is to block weak price confirmation first rather than suppressing informative volume surges.
  - **Governor rejection**: TB-001 / Global floors is violated because the proposed `min_price_move: 0.03` relaxes the historically tightened floor below the required `min_price_move ≥ 0.05`, which was explicitly hardened to treat sub-5% moves as noise. TB-002 / Global floors is also violated because `min_volume_delta` is set to `None`, but the historical constraints require `min_volume_delta` to be explicit and non-`None`. TB-003 / Global floors is violated because `score_threshold` is set to `None`, but the historical constraints require `score_threshold ≥ 2.2` and non-`None`.

---

## 2026-06-06 — Advisor snapshot 231

### Summary
The false positives cluster in low-price-move, quote-only or low-volume Kalshi-like markets where volume increase alone is not informative enough. The analyst labels favor tightening the price-move gate and adding an execution-quality filter rather than broadly raising all thresholds.

### Next step
Raise the minimum price move for low-volume/quote-only markets and require a nonzero executed-trade imbalance before emitting a spike signal.

### Suggested thresholds
`min_price_move` → `0.04`

### Recommendations

- [ ] **TB-695** `rejected` — Increase spike_min_price_move from 0.03 to 0.04 to suppress 2%–3% move false positives.
  - **Governor rejection**: Violates the historical global floor TB-001/TB-002: it sets `min_price_move` to 0.04, which is below the explicitly required `min_price_move ≥ 0.05`. It also violates TB-001/TB-002 by leaving `min_volume_delta` and `score_threshold` as `None`, despite the explicit non-`None` requirement for both. The added execution-imbalance idea does not fix these relaxations.
- [ ] **TB-696** `rejected` — Add a rule that low-volume Kalshi markets must have nonzero executed-trade imbalance to qualify.
  - **Governor rejection**: Violates the historical global floor TB-001/TB-002: it sets `min_price_move` to 0.04, which is below the explicitly required `min_price_move ≥ 0.05`. It also violates TB-001/TB-002 by leaving `min_volume_delta` and `score_threshold` as `None`, despite the explicit non-`None` requirement for both. The added execution-imbalance idea does not fix these relaxations.
- [ ] **TB-697** `rejected` — Keep spike_min_volume_delta unchanged globally; use market-type-specific gating instead of a blanket volume hike.
  - **Governor rejection**: Violates the historical global floor TB-001/TB-002: it sets `min_price_move` to 0.04, which is below the explicitly required `min_price_move ≥ 0.05`. It also violates TB-001/TB-002 by leaving `min_volume_delta` and `score_threshold` as `None`, despite the explicit non-`None` requirement for both. The added execution-imbalance idea does not fix these relaxations.

---

## 2026-06-06 — Advisor snapshot 232

### Summary
The false positives are concentrated in **low-price-move or quote-only alerts**, especially when volume is only modestly above baseline. The analyst notes point to the same pattern: raise the volume bar for these markets and require more convincing price action or executed-trade imbalance before emitting.

### Next step
Tighten the detector with a **market-type-specific rule** for low-volume Kalshi markets: require a larger price move and/or nonzero executed-trade imbalance before triggering, rather than only increasing the global score threshold.

### Suggested thresholds
`min_volume_delta` → `130000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-698** `rejected` — Raise **min_price_move** to 0.03 to suppress 2% quote-only moves that are being labeled noise.
  - **Governor rejection**: The proposed tweak violates the historical hard floor for low-liquidity / low-price-move markets by setting `min_price_move: 0.03`, which conflicts with the explicit constraint to keep `min_price_move ≥ 0.05` and the repeated rule that `0.03–0.04` is disallowed for these contexts. It also leaves `score_threshold` as `None`, conflicting with the global hard floor that `score_threshold ≥ 2.2` must remain explicit/non-`None`.
- [ ] **TB-699** `rejected` — Raise **min_volume_delta** to 130000 for low-volume watch-tier markets to filter ~1.0x baseline volume bumps that are not informative.
  - **Governor rejection**: The proposed tweak violates the historical hard floor for low-liquidity / low-price-move markets by setting `min_price_move: 0.03`, which conflicts with the explicit constraint to keep `min_price_move ≥ 0.05` and the repeated rule that `0.03–0.04` is disallowed for these contexts. It also leaves `score_threshold` as `None`, conflicting with the global hard floor that `score_threshold ≥ 2.2` must remain explicit/non-`None`.
- [ ] **TB-700** `rejected` — Keep **score_threshold** unchanged globally for now; use a conditional rule for low-volume markets instead of muting higher-quality flow.
  - **Governor rejection**: The proposed tweak violates the historical hard floor for low-liquidity / low-price-move markets by setting `min_price_move: 0.03`, which conflicts with the explicit constraint to keep `min_price_move ≥ 0.05` and the repeated rule that `0.03–0.04` is disallowed for these contexts. It also leaves `score_threshold` as `None`, conflicting with the global hard floor that `score_threshold ≥ 2.2` must remain explicit/non-`None`.

---

## 2026-06-06 — Advisor snapshot 233

### Summary
The false positives cluster around cases with only ~2% price movement, where volume alone is enough to trigger a signal. The analyst feedback suggests the detector is too sensitive on low-move, baseline-like volume changes in this market type.

### Next step
Raise the minimum price-move gate slightly and add a market-type-specific volume floor for low-move events so volume spikes cannot fire unless price confirms more strongly.

### Suggested thresholds
`min_volume_delta` → `125000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-701** `rejected` — Increase spike_min_price_move from 0.03 to 0.04 to suppress 2% move noise.
  - **Governor rejection**: Violates the historical price-floor hardening rule: TB-price-floor-hardened requires rejecting 0.02–0.04 relaxations and using 0.05 as the minimum default confirmation bar. The proposed min_price_move of 0.04 is below the enforced floor. It also violates the score-floor hardening rule because score_threshold is set to None, but the primary conflict is the explicit price-floor regression.
- [ ] **TB-702** `rejected` — Raise spike_min_volume_delta modestly, especially for this market type, so ~1.0x baseline volume increases do not qualify.
  - **Governor rejection**: Violates the historical price-floor hardening rule: TB-price-floor-hardened requires rejecting 0.02–0.04 relaxations and using 0.05 as the minimum default confirmation bar. The proposed min_price_move of 0.04 is below the enforced floor. It also violates the score-floor hardening rule because score_threshold is set to None, but the primary conflict is the explicit price-floor regression.
- [ ] **TB-703** `rejected` — Keep the score threshold near current levels unless follow-up labels show score is still admitting low-conviction signals after the gate changes.
  - **Governor rejection**: Violates the historical price-floor hardening rule: TB-price-floor-hardened requires rejecting 0.02–0.04 relaxations and using 0.05 as the minimum default confirmation bar. The proposed min_price_move of 0.04 is below the enforced floor. It also violates the score-floor hardening rule because score_threshold is set to None, but the primary conflict is the explicit price-floor regression.

---

## 2026-06-06 — Advisor snapshot 234

### Summary
The current false positives are coming from low-priced, quote-like moves that clear the price and volume screens but still lack convincing participation. The labeled signal shows that genuinely informative flow has much larger volume delta and price displacement, so the filters should be tightened mainly at the low end rather than broadly.

### Next step
Raise the minimum price-move floor for low-priced markets and add a modest minimum volume-delta floor so small quote-only spikes do not emit.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.06`

### Recommendations

- [ ] **TB-704** `rejected` — Increase spike_min_price_move from 0.03 to 0.06 for low-priced markets.
  - **Governor rejection**: TB-XXX: The proposed tweak violates the historical hard-floor constraint by setting `score_threshold` to `None` instead of keeping it explicit, non-null, and ≥ 2.2. It also conflicts with the explicit floor policy if the target market family is low-priced/low-liquidity or similar, because the history requires `min_price_move/spike_min_price_move` to stay ≥ 0.05 and `min_volume_delta/spike_min_volume_delta` to remain explicit and non-None. While `min_price_move: 0.06` is acceptable, `score_threshold: None` is not.
- [ ] **TB-705** `rejected` — Add or raise spike_min_volume_delta to at least 5000.0 before a spike can trigger.
  - **Governor rejection**: TB-XXX: The proposed tweak violates the historical hard-floor constraint by setting `score_threshold` to `None` instead of keeping it explicit, non-null, and ≥ 2.2. It also conflicts with the explicit floor policy if the target market family is low-priced/low-liquidity or similar, because the history requires `min_price_move/spike_min_price_move` to stay ≥ 0.05 and `min_volume_delta/spike_min_volume_delta` to remain explicit and non-None. While `min_price_move: 0.06` is acceptable, `score_threshold: None` is not.
- [ ] **TB-706** `rejected` — Keep spike_score_threshold unchanged for now; the main issue appears to be weak input filtering rather than overall score calibration.
  - **Governor rejection**: TB-XXX: The proposed tweak violates the historical hard-floor constraint by setting `score_threshold` to `None` instead of keeping it explicit, non-null, and ≥ 2.2. It also conflicts with the explicit floor policy if the target market family is low-priced/low-liquidity or similar, because the history requires `min_price_move/spike_min_price_move` to stay ≥ 0.05 and `min_volume_delta/spike_min_volume_delta` to remain explicit and non-None. While `min_price_move: 0.06` is acceptable, `score_threshold: None` is not.

---

## 2026-06-06 — Advisor snapshot 235

### Summary
The false positives are concentrated in low-price, quote-like moves: a 1% move on a low-priced market was labeled noise, while a much larger 2% move on a high-volume market still looks informative. The pattern suggests the detector is too sensitive to small absolute price changes unless volume is clearly above baseline.

### Next step
Raise the minimum price-move filter for low-priced markets and require a stronger volume floor before emitting signals; keep the score threshold secondary so genuinely large, high-volume moves still pass.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-707** `rejected` — Set a higher low-price price-move floor, using 0.03 as the default minimum and 0.05 for sub-$0.20-like markets.
  - **Governor rejection**: Violates the global hard floor on score threshold because `score_threshold` is set to `None`, but historical constraints require `score_threshold ≥ 2.2` and explicitly prohibit `None`. It also conflicts with the historical rule that the score gate remains active as a secondary brake, so removing it entirely is not allowed.
- [ ] **TB-708** `rejected` — Add a nonzero-above-baseline volume requirement, e.g. demand volΔ > 5000 before quote-only spikes can trigger.
  - **Governor rejection**: Violates the global hard floor on score threshold because `score_threshold` is set to `None`, but historical constraints require `score_threshold ≥ 2.2` and explicitly prohibit `None`. It also conflicts with the historical rule that the score gate remains active as a secondary brake, so removing it entirely is not allowed.
- [ ] **TB-709** `rejected` — Increase spike_score_threshold modestly only after the price/volume filters are in place; use it as a backstop, not the primary gate.
  - **Governor rejection**: Violates the global hard floor on score threshold because `score_threshold` is set to `None`, but historical constraints require `score_threshold ≥ 2.2` and explicitly prohibit `None`. It also conflicts with the historical rule that the score gate remains active as a secondary brake, so removing it entirely is not allowed.

---

## 2026-06-06 — Advisor snapshot 236

### Summary
The false positives cluster around low-price or low-volatility markets where small or zero price moves are being promoted by volume-only or quote-only activity. The analyst labels consistently ask for stronger confirmation: real traded volume, a larger minimum move, or persistence across intervals.

### Next step
Raise the price-move gate and require persistence/real volume before emission, rather than relying on score alone.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-710** `rejected` — Increase the minimum price move for low-priced markets so 1%-2% wiggles do not trigger watch alerts.
  - **Governor rejection**: Violates the global floor that `score_threshold` must be explicit and never `None` (historical constraint: score_threshold ≥ 2.2 and never None). The proposed tweak sets `score_threshold: None`, which is a direct regression. It also proposes `min_price_move: 0.03`, which conflicts with the hardening rule rejecting sub-5% move thresholds in low-liquidity / quote-driven / watch / notable-type markets.
- [ ] **TB-711** `rejected` — Require non-zero traded volume above baseline for any alert, especially when priceΔ is near zero.
  - **Governor rejection**: Violates the global floor that `score_threshold` must be explicit and never `None` (historical constraint: score_threshold ≥ 2.2 and never None). The proposed tweak sets `score_threshold: None`, which is a direct regression. It also proposes `min_price_move: 0.03`, which conflicts with the hardening rule rejecting sub-5% move thresholds in low-liquidity / quote-driven / watch / notable-type markets.
- [ ] **TB-712** `rejected` — Add a multi-interval persistence filter for watch-tier signals to suppress one-bar quote spikes without muting larger confirmed moves.
  - **Governor rejection**: Violates the global floor that `score_threshold` must be explicit and never `None` (historical constraint: score_threshold ≥ 2.2 and never None). The proposed tweak sets `score_threshold: None`, which is a direct regression. It also proposes `min_price_move: 0.03`, which conflicts with the hardening rule rejecting sub-5% move thresholds in low-liquidity / quote-driven / watch / notable-type markets.

---

## 2026-06-06 — Advisor snapshot 237

### Summary
False positives cluster around low-price or quote-only moves with weak execution confirmation, especially where volume is modest or the price change is near the existing floor. The clearest pattern is that analyst-approved signals tend to have either materially larger price moves or much stronger volume, while noisy alerts often have tiny or zero price movement.

### Next step
Tighten the detector to require both a larger price move and meaningful traded volume before emitting watch-tier signals, instead of relying on either condition alone.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.03`, `score_threshold` → `4.0`

### Recommendations

- [ ] **TB-713** `rejected` — Raise **min_price_move** to **0.03** to suppress 1-2% quote-only alerts while preserving the 3%+ moves that are more often informative.
  - **Governor rejection**: TB-Price-move floor is violated: the proposed min_price_move of 0.03 relaxes the explicitly enforced global hard floor of min_price_move / spike_min_price_move ≥ 0.05 into the disallowed 0.03–0.04 range. TB-Volume and TB-Score are not violated because min_volume_delta remains explicit and min_score_threshold=4.0 is above the ≥2.2 floor.
- [ ] **TB-714** `rejected` — Raise **min_volume_delta** to **20000** for watch-tier emissions to filter low-liquidity noise and zero-move volume blips.
  - **Governor rejection**: TB-Price-move floor is violated: the proposed min_price_move of 0.03 relaxes the explicitly enforced global hard floor of min_price_move / spike_min_price_move ≥ 0.05 into the disallowed 0.03–0.04 range. TB-Volume and TB-Score are not violated because min_volume_delta remains explicit and min_score_threshold=4.0 is above the ≥2.2 floor.
- [ ] **TB-715** `rejected` — Increase **score_threshold** to **4.0** so marginal composite signals do not trigger unless they are strong on at least one axis.
  - **Governor rejection**: TB-Price-move floor is violated: the proposed min_price_move of 0.03 relaxes the explicitly enforced global hard floor of min_price_move / spike_min_price_move ≥ 0.05 into the disallowed 0.03–0.04 range. TB-Volume and TB-Score are not violated because min_volume_delta remains explicit and min_score_threshold=4.0 is above the ≥2.2 floor.

---

## 2026-06-06 — Advisor snapshot 238

### Summary
The false positives cluster around quote-only or low-confirmation spikes: small or zero price moves, weak executed volume, and low-liquidity markets. The detector is still catching one genuine CPI move, so the fix should be stricter confirmation rather than a broad suppression.

### Next step
Require both a meaningful price move and non-trivial executed volume before emitting a spike, especially for low-liquidity or event-driven markets.

### Suggested thresholds
`min_volume_delta` → `10000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-716** `rejected` — Raise the minimum price-move filter from 0.03 to 0.04 for low-priced or quote-sensitive markets.
  - **Governor rejection**: TB-global-floor violation: the proposed tweak sets min_price_move to 0.04, which conflicts with the historical floor min_price_move ≥ 0.05 and explicitly re-enters the rejected 0.03–0.04 range. It also violates the explicit non-null requirement for score_threshold by setting it to None. The proposed min_volume_delta = 10000.0 is not, by itself, a conflict from the constraints provided.
- [ ] **TB-717** `rejected` — Raise the minimum volume delta from 5,000 to 10,000 to block quote-only spikes with weak trade confirmation.
  - **Governor rejection**: TB-global-floor violation: the proposed tweak sets min_price_move to 0.04, which conflicts with the historical floor min_price_move ≥ 0.05 and explicitly re-enters the rejected 0.03–0.04 range. It also violates the explicit non-null requirement for score_threshold by setting it to None. The proposed min_volume_delta = 10000.0 is not, by itself, a conflict from the constraints provided.
- [ ] **TB-718** `rejected` — Add a persistence rule: require the spike condition to hold for at least 2 intervals before signaling.
  - **Governor rejection**: TB-global-floor violation: the proposed tweak sets min_price_move to 0.04, which conflicts with the historical floor min_price_move ≥ 0.05 and explicitly re-enters the rejected 0.03–0.04 range. It also violates the explicit non-null requirement for score_threshold by setting it to None. The proposed min_volume_delta = 10000.0 is not, by itself, a conflict from the constraints provided.

---

## 2026-06-06 — Advisor snapshot 239

### Summary
The false positives cluster around alerts with weak or absent traded-volume confirmation, especially quote-only or low-liquidity moves with small price changes. One high-scoring political-market alert also fired on negligible price movement, suggesting the detector needs stronger gating on real movement and persistence.

### Next step
Raise the minimum traded-volume gate and require a larger price move before emitting watch-level spikes, especially for low-liquidity or event-driven markets.

### Suggested thresholds
`min_volume_delta` → `10000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-719** `rejected` — Increase min_volume_delta to reduce quote-only and low-activity triggers; the cleanest false positives had volΔ in the tens to low thousands, while a true CPI signal had volΔ above 157k.
  - **Governor rejection**: Yes. The proposed `min_price_move: 0.03` conflicts with the historical 0.05 price floor for NBA series / playoff winner / low-liquidity high-odds / watch / notable markets. That floor was explicitly tightened to avoid sub-5% noise, so relaxing it to 0.03 violates the preserved constraint. In addition, `score_threshold: None` conflicts with the global constraint that score_threshold must remain explicit/non-None (and ≥2.2).
- [ ] **TB-720** `rejected` — Raise min_price_move to at least 0.03 so 1-2% moves do not trigger watch alerts in thin markets; the false-positive CPI alert at 0.02 was explicitly labeled noise.
  - **Governor rejection**: Yes. The proposed `min_price_move: 0.03` conflicts with the historical 0.05 price floor for NBA series / playoff winner / low-liquidity high-odds / watch / notable markets. That floor was explicitly tightened to avoid sub-5% noise, so relaxing it to 0.03 violates the preserved constraint. In addition, `score_threshold: None` conflicts with the global constraint that score_threshold must remain explicit/non-None (and ≥2.2).
- [ ] **TB-721** `rejected` — Add a persistence rule or equivalent score penalty for zero/near-zero price moves, since the political-market false positive had priceΔ=0.0 despite a high score.
  - **Governor rejection**: Yes. The proposed `min_price_move: 0.03` conflicts with the historical 0.05 price floor for NBA series / playoff winner / low-liquidity high-odds / watch / notable markets. That floor was explicitly tightened to avoid sub-5% noise, so relaxing it to 0.03 violates the preserved constraint. In addition, `score_threshold: None` conflicts with the global constraint that score_threshold must remain explicit/non-None (and ≥2.2).

---

## 2026-06-07 — Advisor snapshot 240

### Summary
Recent false positives are concentrated in low-priced, low-liquidity or quote-driven political/CPI markets where small price moves and/or quote activity are being overcounted as spikes. The analyst labels consistently recommend stricter gating on executed volume, larger sustained price moves, and persistence to avoid noise.

### Next step
Raise the detector’s minimum volume gate and require both a non-zero price move and executed-trade persistence before emitting a spike, especially for quote-heavy low-liquidity markets.

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-722** `rejected` — Increase the volume threshold for quote-driven alerts in low-priced political markets; quote-only or quote-dominant activity is repeatedly labeled noise.
  - **Governor rejection**: Yes. The proposed tweak violates the historical floor on price confirmation: `min_price_move: 0.03` conflicts with the explicitly tightened anti-noise rule requiring `min_price_move`/`spike_min_price_move` to stay set at **≥ 0.05** and specifically rejecting **0.02–0.04** floors. It also conflicts with the non-null score constraint because `score_threshold: None` is disallowed; `score_threshold`/`spike_score_threshold` must stay set, non-null, and **≥ 2.2**.
- [ ] **TB-723** `rejected` — Require a larger minimum price move for low-liquidity CPI-style markets, since 1–2% moves are producing false positives while genuine signals still appear at roughly 3% in the labeled set.
  - **Governor rejection**: Yes. The proposed tweak violates the historical floor on price confirmation: `min_price_move: 0.03` conflicts with the explicitly tightened anti-noise rule requiring `min_price_move`/`spike_min_price_move` to stay set at **≥ 0.05** and specifically rejecting **0.02–0.04** floors. It also conflicts with the non-null score constraint because `score_threshold: None` is disallowed; `score_threshold`/`spike_score_threshold` must stay set, non-null, and **≥ 2.2**.
- [ ] **TB-724** `rejected` — Add a persistence rule so a spike must hold across multiple intervals, or require executed volume to exceed quote activity by a clear margin before triggering.
  - **Governor rejection**: Yes. The proposed tweak violates the historical floor on price confirmation: `min_price_move: 0.03` conflicts with the explicitly tightened anti-noise rule requiring `min_price_move`/`spike_min_price_move` to stay set at **≥ 0.05** and specifically rejecting **0.02–0.04** floors. It also conflicts with the non-null score constraint because `score_threshold: None` is disallowed; `score_threshold`/`spike_score_threshold` must stay set, non-null, and **≥ 2.2**.

---

## 2026-06-07 — Advisor snapshot 241

### Summary
The false positives cluster around low-price, low-liquidity, quote-driven moves with little or no executed trade confirmation, often showing only ~2% price movement. The detector should become stricter on quote-only activity and require more persistent or larger moves before emitting a spike.

### Next step
Tighten the detector to require either executed trade volume or a larger confirmed price move; quote-only spikes should no longer pass on volume delta alone.

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-725** `rejected` — Raise the minimum price move to at least 0.03 to filter out 2% quote wiggles that are being labeled noise.
  - **Governor rejection**: TB-001 is violated because the proposed `min_price_move: 0.03` relaxes the previously enforced global active price floor of `min_price_move >= 0.05`, which was explicitly tightened to prevent low-price, low-liquidity false positives. TB-003 is also violated because `score_threshold: None` removes an explicit non-`None` score floor, contrary to the historical requirement that the score threshold remain explicit and >= 2.2.
- [ ] **TB-726** `rejected` — Increase the minimum volume delta to about 25,000 to suppress low-liquidity quote-driven alerts while preserving larger genuine bursts.
  - **Governor rejection**: TB-001 is violated because the proposed `min_price_move: 0.03` relaxes the previously enforced global active price floor of `min_price_move >= 0.05`, which was explicitly tightened to prevent low-price, low-liquidity false positives. TB-003 is also violated because `score_threshold: None` removes an explicit non-`None` score floor, contrary to the historical requirement that the score threshold remain explicit and >= 2.2.
- [ ] **TB-727** `rejected` — Add a rule that quote-only signals must show persistence across multiple intervals or executed trades before triggering.
  - **Governor rejection**: TB-001 is violated because the proposed `min_price_move: 0.03` relaxes the previously enforced global active price floor of `min_price_move >= 0.05`, which was explicitly tightened to prevent low-price, low-liquidity false positives. TB-003 is also violated because `score_threshold: None` removes an explicit non-`None` score floor, contrary to the historical requirement that the score threshold remain explicit and >= 2.2.

---

## 2026-06-07 — Advisor snapshot 242

### Summary
The false positives are concentrated in low-liquidity, quote-driven prediction markets where modest price moves and large nominal volume deltas can still be noise. Analyst notes repeatedly ask for stronger confirmation from executed trades or sustained follow-through rather than initial quote movement.

### Next step
Raise the detector’s emphasis on confirmed execution by increasing the volume bar for low-liquidity/quote-driven markets and requiring a slightly larger price move before emitting a spike.

### Suggested thresholds
`min_volume_delta` → `12000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-728** `rejected` — Increase spike_min_volume_delta modestly for CPI and political markets that are mostly quote-driven.
  - **Governor rejection**: Violates the active price-floor constraint: `min_price_move` must be explicit and >= 0.05, but the प्रस्तावed tweak lowers it to 0.03. It also violates the active score-floor constraint because `score_threshold` must be explicit and >= 2.2, but the proposal sets it to None. The higher `min_volume_delta` does not offset these regressions.
- [ ] **TB-729** `rejected` — Raise spike_min_price_move to filter out 2% follow-throughless quote pops while preserving clear 10% signal cases.
  - **Governor rejection**: Violates the active price-floor constraint: `min_price_move` must be explicit and >= 0.05, but the प्रस्तावed tweak lowers it to 0.03. It also violates the active score-floor constraint because `score_threshold` must be explicit and >= 2.2, but the proposal sets it to None. The higher `min_volume_delta` does not offset these regressions.
- [ ] **TB-730** `rejected` — Keep spike_score_threshold unchanged for now unless you want a broader de-noising pass; the main issue is threshold shape, not overall score calibration.
  - **Governor rejection**: Violates the active price-floor constraint: `min_price_move` must be explicit and >= 0.05, but the प्रस्तावed tweak lowers it to 0.03. It also violates the active score-floor constraint because `score_threshold` must be explicit and >= 2.2, but the proposal sets it to None. The higher `min_volume_delta` does not offset these regressions.

---

## 2026-06-07 — Advisor snapshot 243

### Summary
The false positives cluster in low-liquidity or quote-driven markets where a modest price move and large raw volume delta still do not correspond to analyst-confirmed signal quality. The strongest pattern is that quote-only or weak-follow-through spikes should require more confirmation before emission.

### Next step
Keep the score threshold flexible, but add a stricter gating rule for low-liquidity/quote-driven markets: require executed trade confirmation or a sustained follow-through price move before emitting a spike.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-731** `rejected` — Raise spike_min_price_move from 0.03 to 0.05 for low-liquidity macro and long-dated political markets.
  - **Governor rejection**: The proposed tweak violates the historical score-gate constraint: TB-score requires score_threshold to remain explicit and non-None, with a global minimum of >= 2.2. Setting score_threshold: None relaxes that tightened gate and conflicts with the prior constraint. It also risks weakening the combined-gate policy by allowing a lower-confidence emission path, even though the new executed-trade/follow-through condition is additive rather than a replacement.
- [ ] **TB-732** `rejected` — Add a follow-through condition: require the initial move to persist for a second observation window or print executed trades after the quote move.
  - **Governor rejection**: The proposed tweak violates the historical score-gate constraint: TB-score requires score_threshold to remain explicit and non-None, with a global minimum of >= 2.2. Setting score_threshold: None relaxes that tightened gate and conflicts with the prior constraint. It also risks weakening the combined-gate policy by allowing a lower-confidence emission path, even though the new executed-trade/follow-through condition is additive rather than a replacement.
- [ ] **TB-733** `rejected` — Increase spike_min_volume_delta modestly for quote-driven classes, but only as a secondary filter; volume alone is not enough.
  - **Governor rejection**: The proposed tweak violates the historical score-gate constraint: TB-score requires score_threshold to remain explicit and non-None, with a global minimum of >= 2.2. Setting score_threshold: None relaxes that tightened gate and conflicts with the prior constraint. It also risks weakening the combined-gate policy by allowing a lower-confidence emission path, even though the new executed-trade/follow-through condition is additive rather than a replacement.

---

## 2026-06-07 — Advisor snapshot 244

### Summary
The false positive appears to be a low-liquidity macro-market spike where price and volume moved enough to trigger, but analyst review judged the move unconfirmed or noise. The detector is already catching a genuine signal in the same class, so the fix should be a confirmation rule or class-specific tightening rather than a broad blunt increase.

### Next step
Add a confirmation requirement for low-liquidity macro markets: keep volume/price triggers, but only emit when the move is followed by sustained trade follow-through or a larger relative volume multiple within the next short window.

### Recommendations

- [ ] **TB-734** `rejected` — Raise the effective trigger for low-liquidity macro markets by requiring higher sustained volume rather than a one-bar volume delta alone.
  - **Governor rejection**: TB-01 / active floors are violated: the proposed tweak sets `min_volume_delta`, `min_price_move`, and `score_threshold` to `None`, which conflicts with the historical constraints requiring an explicit `spike_min_volume_delta`/`min_volume_delta` (non-None), explicit `spike_min_price_move`/`min_price_move` ≥ 0.05, and explicit `spike_score_threshold`/`score_threshold` ≥ 2.2. TB-04 / trade-confirmation gate is also not satisfied by removing these thresholds, since the historical rules require confirmation via executed trades, same-side prints, or persistence rather than quote-only or unbounded emission.
- [ ] **TB-735** `rejected` — Require post-spike confirmation, such as a follow-through trade or persistent price hold after the initial quote move, before emitting.
  - **Governor rejection**: TB-01 / active floors are violated: the proposed tweak sets `min_volume_delta`, `min_price_move`, and `score_threshold` to `None`, which conflicts with the historical constraints requiring an explicit `spike_min_volume_delta`/`min_volume_delta` (non-None), explicit `spike_min_price_move`/`min_price_move` ≥ 0.05, and explicit `spike_score_threshold`/`score_threshold` ≥ 2.2. TB-04 / trade-confirmation gate is also not satisfied by removing these thresholds, since the historical rules require confirmation via executed trades, same-side prints, or persistence rather than quote-only or unbounded emission.
- [ ] **TB-736** `rejected` — Avoid a global increase in score threshold; preserve sensitivity for high-confidence cases like KXCPI-26NOV-T0.0 and apply tightening only to the noisy class.
  - **Governor rejection**: TB-01 / active floors are violated: the proposed tweak sets `min_volume_delta`, `min_price_move`, and `score_threshold` to `None`, which conflicts with the historical constraints requiring an explicit `spike_min_volume_delta`/`min_volume_delta` (non-None), explicit `spike_min_price_move`/`min_price_move` ≥ 0.05, and explicit `spike_score_threshold`/`score_threshold` ≥ 2.2. TB-04 / trade-confirmation gate is also not satisfied by removing these thresholds, since the historical rules require confirmation via executed trades, same-side prints, or persistence rather than quote-only or unbounded emission.

---

## 2026-06-07 — Advisor snapshot 245

### Summary
The false positives are clustered in sticky, high-probability macro markets where price moves are modest but raw volume is large, suggesting the detector is over-weighting volume without enough confirmation of trade-driven imbalance or sustained follow-through.

### Next step
Keep the current price-move gate, but raise the volume requirement and add a confirmation rule that requires executed-trade dominance or a sustained relative-volume multiple before emitting a signal.

### Suggested thresholds
`min_volume_delta` → `500000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-737** `rejected` — Increase spike_min_volume_delta to 500000.0 to suppress large-but-uninformative macro-contract chatter while preserving the clearly strong 2.8M-volume case as an outlier that should still be evaluated by score.
  - **Governor rejection**: TB-Core floors is violated because the proposed tweak sets `score_threshold` to `None`, which explicitly nulls the score floor instead of keeping score as a non-`None` secondary brake. This also conflicts with the historical constraint that `score_threshold` must not be nulled out or relaxed below 2.2.
- [ ] **TB-738** `rejected` — Add a relative-volume confirmation rule: require at least 2.0x baseline volume before a spike can fire, especially for high-probability CPI/Fed-style contracts.
  - **Governor rejection**: TB-Core floors is violated because the proposed tweak sets `score_threshold` to `None`, which explicitly nulls the score floor instead of keeping score as a non-`None` secondary brake. This also conflicts with the historical constraint that `score_threshold` must not be nulled out or relaxed below 2.2.
- [ ] **TB-739** `rejected` — Require follow-through confirmation for low-liquidity macro markets: do not emit unless priceΔ stays at or above 0.05 for a second check or the move is supported by executed-trade volume rather than quote updates.
  - **Governor rejection**: TB-Core floors is violated because the proposed tweak sets `score_threshold` to `None`, which explicitly nulls the score floor instead of keeping score as a non-`None` secondary brake. This also conflicts with the historical constraint that `score_threshold` must not be nulled out or relaxed below 2.2.

---

## 2026-06-07 — Advisor snapshot 246

### Summary
Both recent alerts look like **sticky macro-market volume surges** rather than clean, trade-driven spikes: one had meaningful price movement but was labeled noise/unclear, and the other had very large volume delta with only a small price move and was also labeled noise/unclear. The pattern suggests the detector is over-weighting raw volume in low-probability contexts and needs a stronger confirmation rule.

### Next step
Raise the **effective spike bar** by requiring either a larger relative volume surge or a stronger price confirmation before emitting, rather than relying on absolute volume delta alone.

### Suggested thresholds
`min_volume_delta` → `200000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-740** `rejected` — Increase **min_price_move** to **0.05** so low-conviction 2% moves like KXFED no longer trigger.
  - **Governor rejection**: The proposed tweak conflicts with the historical score-gate constraint: **TB-ScoreFloor** requires `score_threshold` / `spike_score_threshold ≥ 2.2` and explicit/non-`None`, but the proposal sets `score_threshold: None`, which nulls the score gate. It also conflicts with the broader trade-confirmation / persistence / order-flow rules because it relies on raw volume surges rather than preserving an explicit confirmation filter, but the direct rule violation is TB-ScoreFloor.
- [ ] **TB-741** `rejected` — Increase **min_volume_delta** to **200000** to reduce alerts from ordinary macro-market churn like KXCPI.
  - **Governor rejection**: The proposed tweak conflicts with the historical score-gate constraint: **TB-ScoreFloor** requires `score_threshold` / `spike_score_threshold ≥ 2.2` and explicit/non-`None`, but the proposal sets `score_threshold: None`, which nulls the score gate. It also conflicts with the broader trade-confirmation / persistence / order-flow rules because it relies on raw volume surges rather than preserving an explicit confirmation filter, but the direct rule violation is TB-ScoreFloor.
- [ ] **TB-742** `rejected` — Add a rule that volume must be at least **2x baseline** or paired with clear executed-trade imbalance before signaling.
  - **Governor rejection**: The proposed tweak conflicts with the historical score-gate constraint: **TB-ScoreFloor** requires `score_threshold` / `spike_score_threshold ≥ 2.2` and explicit/non-`None`, but the proposal sets `score_threshold: None`, which nulls the score gate. It also conflicts with the broader trade-confirmation / persistence / order-flow rules because it relies on raw volume surges rather than preserving an explicit confirmation filter, but the direct rule violation is TB-ScoreFloor.

---

## 2026-06-07 — Advisor snapshot 247

### Summary
The false positives are concentrated in price-only or price-light moves that occur without enough relative volume confirmation, especially in sticky macro markets. The analyst labels consistently favor tightening the volume gate rather than relying on price move alone.

### Next step
Raise the volume-based trigger and make volume confirmation mandatory for emission, since the current failures are mostly high-score but low-conviction moves without sufficient trade participation.

### Suggested thresholds
`min_volume_delta` → `2.0`, `score_threshold` → `4.5`

### Recommendations

- [ ] **TB-743** `rejected` — Increase spike_min_volume_delta to a higher relative-volume requirement, not just an absolute delta, so near-baseline activity does not pass on price alone.
  - **Governor rejection**: TB-002 / Active price floor is violated because the proposed tweak sets min_price_move to None, which relaxes an explicitly tightened hard floor of min_price_move ≥ 0.05. It also conflicts with the combined-gate policy and active price-floor requirements for low-liquidity/watch/notable/high-odds markets, which require the price floor to remain explicit and non-None rather than removing it.
- [ ] **TB-744** `rejected` — Keep spike_min_price_move roughly where it is, because the main issue is not tiny price movement but insufficient volume confirmation.
  - **Governor rejection**: TB-002 / Active price floor is violated because the proposed tweak sets min_price_move to None, which relaxes an explicitly tightened hard floor of min_price_move ≥ 0.05. It also conflicts with the combined-gate policy and active price-floor requirements for low-liquidity/watch/notable/high-odds markets, which require the price floor to remain explicit and non-None rather than removing it.
- [ ] **TB-745** `rejected` — Raise spike_score_threshold modestly only after tightening volume, so weakly supported signals are filtered without suppressing genuinely strong, high-volume spikes.
  - **Governor rejection**: TB-002 / Active price floor is violated because the proposed tweak sets min_price_move to None, which relaxes an explicitly tightened hard floor of min_price_move ≥ 0.05. It also conflicts with the combined-gate policy and active price-floor requirements for low-liquidity/watch/notable/high-odds markets, which require the price floor to remain explicit and non-None rather than removing it.

---

## 2026-06-07 — Advisor snapshot 248

### Summary
The false positives cluster around spikes that are either illiquid macro moves without confirming trades or price-only jumps on weak/baseline volume. The pattern suggests the detector is over-sensitive to single-leg price movement and needs stronger confirmation from volume and trade-side activity.

### Next step
Tighten the gate on confirmation: require both a higher volume delta and a side-confirming trade before emitting, especially in illiquid macro markets.

### Suggested thresholds
`min_volume_delta` → `30000.0`, `score_threshold` → `12.0`

### Recommendations

- [ ] **TB-746** `rejected` — Raise the minimum volume delta to filter out price-only jumps on near-baseline flow.
  - **Governor rejection**: TB-001 and TB-002 are violated because the proposal sets min_price_move to None, which relaxes the explicitly required active floor of >= 0.05 and removes the price-move floor-first constraint. TB-003 is not violated because score_threshold is raised to 12.0, but the price-floor regression alone conflicts with the historical constraints.
- [ ] **TB-747** `rejected` — Add a confirmation rule that at least one trade print supports the direction of the move before flagging.
  - **Governor rejection**: TB-001 and TB-002 are violated because the proposal sets min_price_move to None, which relaxes the explicitly required active floor of >= 0.05 and removes the price-move floor-first constraint. TB-003 is not violated because score_threshold is raised to 12.0, but the price-floor regression alone conflicts with the historical constraints.
- [ ] **TB-748** `rejected` — Increase the combined score threshold modestly so borderline single-signal events do not emit.
  - **Governor rejection**: TB-001 and TB-002 are violated because the proposal sets min_price_move to None, which relaxes the explicitly required active floor of >= 0.05 and removes the price-move floor-first constraint. TB-003 is not violated because score_threshold is raised to 12.0, but the price-floor regression alone conflicts with the historical constraints.

---

## 2026-06-07 — Advisor snapshot 249

### Summary
The false positives are coming from signals with large raw volume but weak price confirmation and no trade-side concentration, especially in flatter or illiquid markets. The current detector is over-triggering on isolated volume bursts that analyst review classifies as noise/unclear or noise/no.

### Next step
Keep the score logic, but add a stricter gate for low-conviction spikes: require both a larger relative volume multiple and a minimum price move before emitting, with an extra side-confirmation filter for illiquid markets.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-749** `rejected` — Raise the volume gate to a relative-volume rule: require at least 1.5x baseline volume before watch-level alerts.
  - **Governor rejection**: The proposed tweak violates the historical constraints by relaxing explicitly fixed floors to `None`: `min_volume_delta: None` conflicts with the requirement that `min_volume_delta` must remain a concrete threshold and not `None`, and `score_threshold: None` conflicts with the rule that `score_threshold` must remain set with a global floor of at least 2.2. It also lowers `min_price_move` to 0.03, which conflicts with the global price floor of at least 0.05 for spike detection and the low-liquidity/high-noise rules requiring a stricter price floor rather than a looser one.
- [ ] **TB-750** `rejected` — Increase the price-move floor so flat-volume bursts do not pass; require at least a 0.03 fractional move for emission.
  - **Governor rejection**: The proposed tweak violates the historical constraints by relaxing explicitly fixed floors to `None`: `min_volume_delta: None` conflicts with the requirement that `min_volume_delta` must remain a concrete threshold and not `None`, and `score_threshold: None` conflicts with the rule that `score_threshold` must remain set with a global floor of at least 2.2. It also lowers `min_price_move` to 0.03, which conflicts with the global price floor of at least 0.05 for spike detection and the low-liquidity/high-noise rules requiring a stricter price floor rather than a looser one.
- [ ] **TB-751** `rejected` — For illiquid macro markets, suppress signals unless there is at least one side-confirming trade or concentrated trade-side flow.
  - **Governor rejection**: The proposed tweak violates the historical constraints by relaxing explicitly fixed floors to `None`: `min_volume_delta: None` conflicts with the requirement that `min_volume_delta` must remain a concrete threshold and not `None`, and `score_threshold: None` conflicts with the rule that `score_threshold` must remain set with a global floor of at least 2.2. It also lowers `min_price_move` to 0.03, which conflicts with the global price floor of at least 0.05 for spike detection and the low-liquidity/high-noise rules requiring a stricter price floor rather than a looser one.

---

## 2026-06-07 — Advisor snapshot 250

### Summary
The false positives are concentrated in low-conviction, quote-driven moves where price changes are small, volume looks flat or unbalanced, and analysts labeled the signals as noise or unclear. The common pattern is that the detector is firing on size-of-flow alone without enough confirmed price displacement or trade-side concentration.

### Next step
Tighten the detector to require a larger price move plus a volume-imbalance confirmation before emitting watch/notable spikes, rather than relying on raw volume delta alone.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.03`, `score_threshold` → `3.0`

### Recommendations

- [ ] **TB-752** `rejected` — Raise the minimum price move to 0.03 so 2% quote drift no longer triggers a spike.
  - **Governor rejection**: The proposal violates the historical price-floor constraint: TB-001/TB-004 require explicit min_price_move / spike_min_price_move ≥ 0.05, but the tweak sets min_price_move to 0.03. It also weakens the volume floor relative to the stated historical standard: TB-002/TB-005 require min_volume_delta / spike_min_volume_delta to be explicit and non-None, with raised floors in thin markets rather than reducing confirmation, but the tweak lowers min_volume_delta to 1.5 without indicating it is a raised floor.
- [ ] **TB-753** `rejected` — Add a volume imbalance gate: require at least 1.5x baseline volume before a watch-level alert can emit.
  - **Governor rejection**: The proposal violates the historical price-floor constraint: TB-001/TB-004 require explicit min_price_move / spike_min_price_move ≥ 0.05, but the tweak sets min_price_move to 0.03. It also weakens the volume floor relative to the stated historical standard: TB-002/TB-005 require min_volume_delta / spike_min_volume_delta to be explicit and non-None, with raised floors in thin markets rather than reducing confirmation, but the tweak lowers min_volume_delta to 1.5 without indicating it is a raised floor.
- [ ] **TB-754** `rejected` — Increase the score threshold modestly to suppress borderline signals that still pass the raw volume filter.
  - **Governor rejection**: The proposal violates the historical price-floor constraint: TB-001/TB-004 require explicit min_price_move / spike_min_price_move ≥ 0.05, but the tweak sets min_price_move to 0.03. It also weakens the volume floor relative to the stated historical standard: TB-002/TB-005 require min_volume_delta / spike_min_volume_delta to be explicit and non-None, with raised floors in thin markets rather than reducing confirmation, but the tweak lowers min_volume_delta to 1.5 without indicating it is a raised floor.

---

## 2026-06-07 — Advisor snapshot 251

### Summary
The false positives are driven by quote-like or low-immediacy moves: both recent watch signals had only ~2% price moves despite large reported volume deltas, and analysts labeled them noise/unclear. The pattern suggests the detector is too sensitive to volume without enough confirmation from actual price displacement or trade-side imbalance.

### Next step
Tighten the gate by requiring a larger price move and a stronger volume-imbalance condition before emitting watch-level spikes, rather than relying on combined score alone.

### Suggested thresholds
`min_price_move` → `0.03`, `score_threshold` → `2.2`

### Recommendations

- [ ] **TB-755** `rejected` — Raise min_price_move from 0.02 to 0.03.
  - **Governor rejection**: TB-global and TB-noise rules are violated: the proposed `min_price_move: 0.03` relaxes the hardened floor `min_price_move ≥ 0.05` that was explicitly required for low-liquidity/watch/notable/high-odds markets and rejected as a 0.03–0.04 relaxation. It also conflicts with the trade-confirmation / volume-price-coupling constraints by setting `min_volume_delta: None`, which removes the explicit non-`None` volume confirmation requirement and allows volume-driven emissions without a stronger executed-trade/imbalance gate.
- [ ] **TB-756** `rejected` — Increase the volume requirement to at least 1.5x baseline or an equivalent trade-side imbalance filter before counting volume delta as a spike.
  - **Governor rejection**: TB-global and TB-noise rules are violated: the proposed `min_price_move: 0.03` relaxes the hardened floor `min_price_move ≥ 0.05` that was explicitly required for low-liquidity/watch/notable/high-odds markets and rejected as a 0.03–0.04 relaxation. It also conflicts with the trade-confirmation / volume-price-coupling constraints by setting `min_volume_delta: None`, which removes the explicit non-`None` volume confirmation requirement and allows volume-driven emissions without a stronger executed-trade/imbalance gate.
- [ ] **TB-757** `rejected` — Lift score_threshold modestly so borderline watch cases with flat price action do not emit.
  - **Governor rejection**: TB-global and TB-noise rules are violated: the proposed `min_price_move: 0.03` relaxes the hardened floor `min_price_move ≥ 0.05` that was explicitly required for low-liquidity/watch/notable/high-odds markets and rejected as a 0.03–0.04 relaxation. It also conflicts with the trade-confirmation / volume-price-coupling constraints by setting `min_volume_delta: None`, which removes the explicit non-`None` volume confirmation requirement and allows volume-driven emissions without a stronger executed-trade/imbalance gate.

---

## 2026-06-07 — Advisor snapshot 252

### Summary
The false positives are concentrated in low-priced or flat-baseline markets where quote-only or small fractional moves are being promoted by large raw volume deltas. The analyst labels consistently ask for more evidence of *sustained* price movement and *trade-side imbalance* before emitting a spike.

### Next step
Increase the volume gate and require a larger price move before signaling, with an additional rule that flat-baseline markets must show traded-volume imbalance rather than just raw volume expansion.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-758** `rejected` — Raise the minimum volume delta for watch-level spikes, especially in low-priced political markets, to suppress headline-driven noise.
  - **Governor rejection**: The proposed tweak violates the historical floor rules by setting min_price_move to 0.03, which conflicts with the active/global spike price floor that requires min_price_move ≥ 0.05 and explicitly rejects 0.03–0.04 relaxations. It also conflicts with the active score floor because score_threshold is set to None, while the historical constraint requires score_threshold ≥ 2.2 and explicit/non-None. In addition, setting min_volume_delta to None violates the active volume floor requiring an explicit/non-None volume gate.
- [ ] **TB-759** `rejected` — Increase the minimum price move from 0.02 to 0.03 so quote-only or borderline moves do not pass as spikes.
  - **Governor rejection**: The proposed tweak violates the historical floor rules by setting min_price_move to 0.03, which conflicts with the active/global spike price floor that requires min_price_move ≥ 0.05 and explicitly rejects 0.03–0.04 relaxations. It also conflicts with the active score floor because score_threshold is set to None, while the historical constraint requires score_threshold ≥ 2.2 and explicit/non-None. In addition, setting min_volume_delta to None violates the active volume floor requiring an explicit/non-None volume gate.
- [ ] **TB-760** `rejected` — Add a secondary imbalance filter: only emit when volume delta is accompanied by clear trade-side concentration or baseline-relative expansion (for example, at least 1.5x baseline volume).
  - **Governor rejection**: The proposed tweak violates the historical floor rules by setting min_price_move to 0.03, which conflicts with the active/global spike price floor that requires min_price_move ≥ 0.05 and explicitly rejects 0.03–0.04 relaxations. It also conflicts with the active score floor because score_threshold is set to None, while the historical constraint requires score_threshold ≥ 2.2 and explicit/non-None. In addition, setting min_volume_delta to None violates the active volume floor requiring an explicit/non-None volume gate.

---

## 2026-06-07 — Advisor snapshot 253

### Summary
The false positives are coming from low-confidence, quote-driven or headline-sensitive moves where volume is elevated but the price move is still small or not well sustained. The labels suggest you need stronger confirmation from both price movement and traded imbalance before emitting a spike.

### Next step
Tighten the detector with a higher minimum price move and require a clearer volume anomaly before scoring a signal, especially for low-priced or politically sensitive markets.

### Suggested thresholds
`min_volume_delta` → `10000.0`, `min_price_move` → `0.04`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-761** `rejected` — Raise the minimum price move to filter out flat-baseline noise and quote-only blips.
  - **Governor rejection**: TB-002 is violated because `min_price_move: 0.04` is below the explicitly required hard floor of `≥ 0.05`, and 0.03–0.04 relaxations are disallowed. This is a relaxation of a previously tightened noise-control threshold, especially problematic for low-liquidity / watch / notable / politically sensitive markets where the stricter 0.05 floor is required. The other proposed thresholds do not conflict on their face, since `min_volume_delta` is explicit and non-null and `score_threshold` is explicit and above 2.2.
- [ ] **TB-762** `rejected` — Increase the volume delta floor for low-priced/headline-sensitive markets to avoid classifying routine churn as spikes.
  - **Governor rejection**: TB-002 is violated because `min_price_move: 0.04` is below the explicitly required hard floor of `≥ 0.05`, and 0.03–0.04 relaxations are disallowed. This is a relaxation of a previously tightened noise-control threshold, especially problematic for low-liquidity / watch / notable / politically sensitive markets where the stricter 0.05 floor is required. The other proposed thresholds do not conflict on their face, since `min_volume_delta` is explicit and non-null and `score_threshold` is explicit and above 2.2.
- [ ] **TB-763** `rejected` — Add a directional traded-imbalance or sustained-move requirement so volume alone cannot trigger a signal.
  - **Governor rejection**: TB-002 is violated because `min_price_move: 0.04` is below the explicitly required hard floor of `≥ 0.05`, and 0.03–0.04 relaxations are disallowed. This is a relaxation of a previously tightened noise-control threshold, especially problematic for low-liquidity / watch / notable / politically sensitive markets where the stricter 0.05 floor is required. The other proposed thresholds do not conflict on their face, since `min_volume_delta` is explicit and non-null and `score_threshold` is explicit and above 2.2.

---

## 2026-06-07 — Advisor snapshot 254

### Summary
The false positives are coming from thin or near-zero-price markets where large percentage moves or raw volume jumps still reflect weak conviction. The analyst notes point to adding more confirmation, especially a higher volume bar and a sustained price move requirement.

### Next step
Raise the minimum volume delta and require a larger minimum price move, with an added rule for thin markets that both conditions must be met before emitting a spike.

### Suggested thresholds
`min_volume_delta` → `3000.0`, `min_price_move` → `0.05`

### Recommendations

- [x] **TB-764** `applied` — Increase spike_min_volume_delta to filter out low-conviction bursts in thin markets.
- [x] **TB-765** `applied` — Increase spike_min_price_move so near-zero starting prices do not trigger on tiny absolute moves.
- [x] **TB-766** `applied` — Add a conjunction rule for thin markets: require both a higher volume delta and multiple executed trades before emitting.

---

## 2026-06-07 — Advisor snapshot 255

### Summary
The false positives are concentrated in thin, low-priced markets where tiny absolute price moves or quote bursts pass the current spike gate despite weak conviction. The pattern suggests the detector needs more sustained movement, especially when starting prices are near zero.

### Next step
Add a low-price/near-zero guardrail that requires both a larger price move and evidence of sustained multi-trade confirmation before emitting a spike.

### Suggested thresholds
`min_volume_delta` → `11000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-767** `rejected` — Raise the price-move floor for thin or near-zero markets to avoid treating small absolute moves as spikes.
  - **Governor rejection**: TB-NULL-001 is violated because `score_threshold` is set to `None`, but the historical constraints require `score_threshold` / `spike_score_threshold` to remain explicit and ≥ 2.2, with the score gate never removed. The proposed tweak also preserves `min_price_move: 0.05`, which does not conflict, but the null score gate is a direct regression.
- [ ] **TB-768** `rejected` — Require confirmation across multiple independent trades over several minutes, not a single burst, when initial yes/price levels are very low.
  - **Governor rejection**: TB-NULL-001 is violated because `score_threshold` is set to `None`, but the historical constraints require `score_threshold` / `spike_score_threshold` to remain explicit and ≥ 2.2, with the score gate never removed. The proposed tweak also preserves `min_price_move: 0.05`, which does not conflict, but the null score gate is a direct regression.
- [ ] **TB-769** `rejected` — Increase the volume gate modestly for low-priced markets so score gains from noisy microstructure do not trigger signals by themselves.
  - **Governor rejection**: TB-NULL-001 is violated because `score_threshold` is set to `None`, but the historical constraints require `score_threshold` / `spike_score_threshold` to remain explicit and ≥ 2.2, with the score gate never removed. The proposed tweak also preserves `min_price_move: 0.05`, which does not conflict, but the null score gate is a direct regression.

---

## 2026-06-07 — Advisor snapshot 256

### Summary
The false positives are coming from **quote-heavy, trade-light CPI moves**: large volume deltas can still be noise when price displacement is short-lived or only around the minimum move. The labels suggest the detector is firing too easily on modest price changes and should require stronger confirmation from both volume quality and sustained movement.

### Next step
Raise the **price-move requirement** slightly and add a stronger **trade-confirmation gate** so CPI signals only emit when movement is both larger and more sustained, rather than reacting to brief quote-driven spikes.

### Suggested thresholds
`min_volume_delta` → `8000.0`, `min_price_move` → `0.05`, `score_threshold` → `12.0`

### Recommendations

- [x] **TB-770** `applied` — Increase **spike_min_price_move** from 0.03 to **0.05** for CPI-like markets.
- [x] **TB-771** `applied` — Increase **spike_min_volume_delta** modestly from 4300-ish sensitivity to a higher floor near **8000** to reduce quote-heavy triggers.
- [x] **TB-772** `applied` — Keep the score gate, but require the spike score to clear a slightly higher bar, around **12.0**, only if priceΔ is below 0.05.

---

## 2026-06-07 — Advisor snapshot 257

### Summary
The false positives are coming from price-heavy but trade-light moves: alerts fire on notable fractional price changes even when the volume confirmation is weak or routine. The analyst labels point to needing stronger confirmation from *sustained* volume expansion and directional follow-through, especially in CPI-style markets.

### Next step
Tighten the trigger so price move alone is not enough: require both a larger volume surge and multi-minute sustained movement before emitting, with the largest gain coming from raising the volume-confirmation gate rather than the score cutoff.

### Suggested thresholds
`min_volume_delta` → `1.5`

### Recommendations

- [ ] **TB-773** `rejected` — Increase spike_min_volume_delta to require a clearly larger relative volume surge, roughly 1.5x baseline confirmation.
  - **Governor rejection**: Yes. The proposal explicitly sets `min_price_move: None`, which violates the global hard floor requiring `min_price_move ≥ 0.05` and no null relaxations. It also fails the price-confirmation-first constraint by trying to make price move optional, which is incompatible with the historical rule that volume must be paired with a material directional move.
- [ ] **TB-774** `rejected` — Add a persistence rule: only emit when the price move is sustained for multiple minutes, not just a brief quote-driven jump.
  - **Governor rejection**: Yes. The proposal explicitly sets `min_price_move: None`, which violates the global hard floor requiring `min_price_move ≥ 0.05` and no null relaxations. It also fails the price-confirmation-first constraint by trying to make price move optional, which is incompatible with the historical rule that volume must be paired with a material directional move.
- [ ] **TB-775** `rejected` — Keep spike_min_price_move near current levels for now; focus on filtering with trade-confirmed volume share before lowering sensitivity further.
  - **Governor rejection**: Yes. The proposal explicitly sets `min_price_move: None`, which violates the global hard floor requiring `min_price_move ≥ 0.05` and no null relaxations. It also fails the price-confirmation-first constraint by trying to make price move optional, which is incompatible with the historical rule that volume must be paired with a material directional move.
- [ ] **TB-776** `rejected` — If you need a single numeric score adjustment, raise spike_score_threshold modestly rather than aggressively, so genuine high-conviction flow is preserved.
  - **Governor rejection**: Yes. The proposal explicitly sets `min_price_move: None`, which violates the global hard floor requiring `min_price_move ≥ 0.05` and no null relaxations. It also fails the price-confirmation-first constraint by trying to make price move optional, which is incompatible with the historical rule that volume must be paired with a material directional move.

---

## 2026-06-07 — Advisor snapshot 258

### Summary
The false positives are concentrated in thin or quote-heavy CPI/prediction-market moves where modest price jumps and raw volume deltas are being treated as spikes without enough trade confirmation or follow-through. Analyst notes repeatedly ask for higher price-move and volume confirmation, especially on low-liquidity macro contracts.

### Next step
Raise the price-move and volume-confirmation gates together, and require multi-window follow-through for thin markets before emitting a spike.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.06`, `score_threshold` → `7.5`

### Recommendations

- [x] **TB-777** `applied` — Increase spike_min_price_move from 0.03 to 0.06 for low-liquidity macro contracts.
- [x] **TB-778** `applied` — Increase spike_min_volume_delta from 11000 to 20000, but only if the volume is trade-confirmed rather than quote-driven.
- [x] **TB-779** `applied` — Require either 2 consecutive windows of directional continuation or a higher spike_score_threshold before emitting on CPI-like markets.

---

## 2026-06-07 — Advisor snapshot 259

### Summary
Recent false positives cluster in thin, event-driven macro markets where one-off quote moves and modest volume deltas are enough to trigger alerts. Analysts repeatedly ask for stronger confirmation from either traded volume, sustained multi-tick follow-through, or a larger price move before emission.

### Next step
Raise the price-move bar and require confirmation across time: keep volume-sensitive detection, but only emit when price move is at least 0.06 and is sustained across multiple ticks or backed by clearly above-baseline traded volume.

### Suggested thresholds
`min_price_move` → `0.06`

### Recommendations

- [ ] **TB-780** `rejected` — Increase spike_min_price_move to 0.06 to filter routine 3%-5% repricings that are repeatedly labeled noise/unclear.
  - **Governor rejection**: The proposed tweak conflicts with the historical **Volume floor** constraint: it sets `min_volume_delta` to `None`, but the historical rule requires `min_volume_delta/spike_min_volume_delta` to be explicit, non-`None`, and meaningfully above baseline. It also conflicts with the historical **Score floor** constraint: it sets `score_threshold` to `None`, but the rule requires `score_threshold/spike_score_threshold` to remain explicit, non-`None`, and ≥ 2.2. Raising `min_price_move` to 0.06 does not conflict with the price-floor rule, but removing the volume and score gates does.
- [ ] **TB-781** `rejected` — Add a rule that a signal must show sustained follow-through across at least 2 time windows or multiple ticks, not just a single jump.
  - **Governor rejection**: The proposed tweak conflicts with the historical **Volume floor** constraint: it sets `min_volume_delta` to `None`, but the historical rule requires `min_volume_delta/spike_min_volume_delta` to be explicit, non-`None`, and meaningfully above baseline. It also conflicts with the historical **Score floor** constraint: it sets `score_threshold` to `None`, but the rule requires `score_threshold/spike_score_threshold` to remain explicit, non-`None`, and ≥ 2.2. Raising `min_price_move` to 0.06 does not conflict with the price-floor rule, but removing the volume and score gates does.
- [ ] **TB-782** `rejected` — Require a stronger volume confirmation for thin contracts, using a larger volume delta multiple above baseline before emission.
  - **Governor rejection**: The proposed tweak conflicts with the historical **Volume floor** constraint: it sets `min_volume_delta` to `None`, but the historical rule requires `min_volume_delta/spike_min_volume_delta` to be explicit, non-`None`, and meaningfully above baseline. It also conflicts with the historical **Score floor** constraint: it sets `score_threshold` to `None`, but the rule requires `score_threshold/spike_score_threshold` to remain explicit, non-`None`, and ≥ 2.2. Raising `min_price_move` to 0.06 does not conflict with the price-floor rule, but removing the volume and score gates does.

---

## 2026-06-07 — Advisor snapshot 260

### Summary
The false positives are concentrated in thin, quote-heavy macro markets where price can move on little or no trade-confirmed volume, especially around CPI and Fed contracts. Analyst labels repeatedly suggest that single-interval spikes are not enough and that sustained multi-window follow-through or directional traded volume is needed.

### Next step
Add a persistence gate: require either trade-confirmed volume above threshold or the same directional price move to persist across multiple intervals before emitting a spike.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.08`

### Recommendations

- [ ] **TB-783** `rejected` — Increase the volume filter first, because most noise cases are quote-driven rather than trade-driven; target a higher minimum trade-confirmed volume delta.
  - **Governor rejection**: The proposal violates the historical **score gate** constraint (TB-SCORE-001): `score_threshold` must remain explicit and ≥ 2.2, but the tweak sets `score_threshold: None`, which is a prohibited null relaxation. It also appears to conflict with the historical **volume gate** principle (TB-VOLUME-001 / TB-CONFIRM-001) by allowing emission based on persistence alone, because the historical constraints require an explicit non-`None` volume gate and combined confirmation rather than price-only or persistence-only emission.
- [ ] **TB-784** `rejected` — Raise the price-move threshold modestly for thin macro contracts, since several false positives occur at 3%–7% moves that do not hold.
  - **Governor rejection**: The proposal violates the historical **score gate** constraint (TB-SCORE-001): `score_threshold` must remain explicit and ≥ 2.2, but the tweak sets `score_threshold: None`, which is a prohibited null relaxation. It also appears to conflict with the historical **volume gate** principle (TB-VOLUME-001 / TB-CONFIRM-001) by allowing emission based on persistence alone, because the historical constraints require an explicit non-`None` volume gate and combined confirmation rather than price-only or persistence-only emission.
- [ ] **TB-785** `rejected` — Require sustained follow-through over 2+ consecutive intervals for watch/notable alerts, especially when volume is large but trade confirmation is weak.
  - **Governor rejection**: The proposal violates the historical **score gate** constraint (TB-SCORE-001): `score_threshold` must remain explicit and ≥ 2.2, but the tweak sets `score_threshold: None`, which is a prohibited null relaxation. It also appears to conflict with the historical **volume gate** principle (TB-VOLUME-001 / TB-CONFIRM-001) by allowing emission based on persistence alone, because the historical constraints require an explicit non-`None` volume gate and combined confirmation rather than price-only or persistence-only emission.

---

## 2026-06-07 — Advisor snapshot 261

### Summary
The false positives cluster in thin, event-driven macro markets where quote-driven or one-tick price jumps can satisfy the current trigger even when the move is not well supported by traded volume. Analyst labels repeatedly point to the same fix: require sustained multi-interval confirmation and/or a larger relative volume surge before emitting a signal.

### Next step
Raise the minimum price move modestly and add a persistence rule: only emit when the move is confirmed across multiple intervals or accompanied by directional traded volume.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [x] **TB-786** `applied` — Increase min_price_move from 0.03 to 0.05 for thin macro contracts.
- [x] **TB-787** `applied` — Require volume delta to exceed baseline by at least 1.5x, or set a higher absolute floor for watch/notable alerts on low-liquidity markets.
- [x] **TB-788** `applied` — Add a multi-interval confirmation rule: price or volume must remain elevated for 2 consecutive intervals before signaling.

---

## 2026-06-07 — Advisor snapshot 262

### Summary
The false positives cluster in thin, low-liquidity macro/CPI and Fed markets where quote-driven or one-off price jumps pass the detector despite weak trade confirmation. Analyst labels consistently recommend tightening the volume component and requiring sustained, trade-confirmed movement rather than a single-window spike.

### Next step
Require both a higher minimum volume delta and multi-window trade-confirmed follow-through before emitting a signal, with the biggest gain coming from filtering quote-only spikes in thin markets.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.07`

### Recommendations

- [x] **TB-789** `applied` — Raise spike_min_volume_delta to about 20000.0 for thin macro/CPI contracts.
- [x] **TB-790** `applied` — Raise spike_min_price_move to about 0.07 to 0.09 so small quote-led moves do not trigger.
- [x] **TB-791** `applied` — Add a sustain rule: require the price move to persist across at least 2 intervals, or require executed-trade share to exceed quotes before signaling.

---

## 2026-06-07 — Advisor snapshot 263

### Summary
The false positives are concentrated in thin CPI and other low-liquidity event markets where quote-driven or short-lived jumps produce enough score to alert, but analyst labels repeatedly mark them as noise or unclear. The consistent fix is to require stronger trade-confirmed volume and a sustained price move before emitting a signal.

### Next step
Raise the detector to require both a larger traded-volume surge and a sustained price move across multiple windows for low-liquidity markets, with the most direct single change being a higher minimum price-move floor plus a trade-confirmation requirement.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-792** `rejected` — Increase spike_min_price_move from 0.03 to 0.05 for low-liquidity macro/event markets.
  - **Governor rejection**: The proposed tweak conflicts with TB-001/TB-002 because it sets `min_volume_delta` to `None`, violating the historical rule that `min_volume_delta` must be explicit and non-`None` and that there are no null relaxations for this field. The proposed `min_price_move: 0.05` and `score_threshold: 3.5` do not conflict with the listed floors, but the null volume setting does.
- [ ] **TB-793** `rejected` — Add a trade-confirmation rule: ignore quote-only spikes unless executed volume rises by at least 1.5x baseline.
  - **Governor rejection**: The proposed tweak conflicts with TB-001/TB-002 because it sets `min_volume_delta` to `None`, violating the historical rule that `min_volume_delta` must be explicit and non-`None` and that there are no null relaxations for this field. The proposed `min_price_move: 0.05` and `score_threshold: 3.5` do not conflict with the listed floors, but the null volume setting does.
- [ ] **TB-794** `rejected` — Lift spike_score_threshold modestly to suppress marginal watch-tier alerts that lack sustained follow-through.
  - **Governor rejection**: The proposed tweak conflicts with TB-001/TB-002 because it sets `min_volume_delta` to `None`, violating the historical rule that `min_volume_delta` must be explicit and non-`None` and that there are no null relaxations for this field. The proposed `min_price_move: 0.05` and `score_threshold: 3.5` do not conflict with the listed floors, but the null volume setting does.

---

## 2026-06-07 — Advisor snapshot 264

### Summary
The false positives are concentrated in thin, low-liquidity CPI/Fed markets where quote-driven or one-off volume jumps trigger alerts despite only modest or inconsistent price follow-through. The analyst labels repeatedly ask for stronger trade-confirmed volume, larger sustained price moves, or multi-window confirmation before emitting a signal.

### Next step
Tighten the detector for thin markets by requiring both a higher volume multiple above baseline and a larger sustained price move across more than one interval, rather than relying on a single-window spike.

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.08`, `score_threshold` → `6.5`

### Recommendations

- [x] **TB-795** `applied` — Raise spike_min_volume_delta to reduce quote-only triggers in thin macro contracts; target a materially higher floor than the current level.
- [x] **TB-796** `applied` — Raise spike_min_price_move so a signal requires more than a small 2%-4% move unless volume is clearly trade-confirmed.
- [x] **TB-797** `applied` — Add a persistence rule: require follow-through across 2+ consecutive windows or directional traded volume before emitting a signal.

---

## 2026-06-07 — Advisor snapshot 265

### Summary
The false positives are concentrated in thin, low-liquidity CPI and Fed markets where quote-driven or single-interval volume spikes trigger alerts even when price barely moves. Analyst labels consistently recommend adding confirmation from sustained price action or executed trades rather than relying on volume alone.

### Next step
Require both a larger price move and some sustained follow-through before emitting on thin markets, with the clearest single change being to raise the minimum price-move filter and pair it with a multi-tick confirmation rule.

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.06`

### Recommendations

- [ ] **TB-798** `rejected` — Increase spike_min_price_move to 0.06 to suppress near-zero and quote-only moves that are repeatedly labeled noise.
  - **Governor rejection**: Yes. The proposed tweak sets score_threshold to None, which violates the historical no-null relaxation rule for `score_threshold` and conflicts with the explicit hard floor TB-001 / TB-002 requirement that `score_threshold` remain explicit and ≥ 2.2. The new `min_price_move: 0.06` and `min_volume_delta: 25000.0` do not conflict with the historical floors, but nulling the score gate does.
- [ ] **TB-799** `rejected` — Add a sustained directional confirmation rule: require price to hold the move across at least 2 consecutive windows or multiple ticks before alerting.
  - **Governor rejection**: Yes. The proposed tweak sets score_threshold to None, which violates the historical no-null relaxation rule for `score_threshold` and conflicts with the explicit hard floor TB-001 / TB-002 requirement that `score_threshold` remain explicit and ≥ 2.2. The new `min_price_move: 0.06` and `min_volume_delta: 25000.0` do not conflict with the historical floors, but nulling the score gate does.
- [ ] **TB-800** `rejected` — For low-liquidity markets, require trade-confirmed volume rather than total volume alone, or raise spike_min_volume_delta modestly to avoid single-burst false positives.
  - **Governor rejection**: Yes. The proposed tweak sets score_threshold to None, which violates the historical no-null relaxation rule for `score_threshold` and conflicts with the explicit hard floor TB-001 / TB-002 requirement that `score_threshold` remain explicit and ≥ 2.2. The new `min_price_move: 0.06` and `min_volume_delta: 25000.0` do not conflict with the historical floors, but nulling the score gate does.

---

## 2026-06-07 — Advisor snapshot 266

### Summary
The false positives are concentrated in thin, low-liquidity markets where volume-only or quote-only spikes can fire without a meaningful sustained price move. Analyst labels repeatedly call for more price confirmation and more trade-confirmed volume rather than a simple volume delta trigger.

### Next step
Require both a larger sustained price move and trade-confirmed volume before emitting, rather than relying on volume delta alone; the single best next change is to raise the minimum price-move filter and gate alerts on confirmed traded volume across more than one interval.

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-801** `rejected` — Increase spike_min_price_move from 0.03 to 0.05 for watch-tier thin markets to suppress near-zero baseline liquidity noise.
  - **Governor rejection**: The proposed tweak violates the historical constraint to keep `score_threshold ≥ 2.2` and explicit/non-`None`. Setting `score_threshold: None` removes the score gate, which is explicitly disallowed. The new `min_price_move: 0.05` and explicit `min_volume_delta: 25000.0` do not conflict with the stated floor/explicit-volume requirements.
- [ ] **TB-802** `rejected` — Add a rule that at least one additional tick or time window must confirm the direction before alerting on low-liquidity CPI/Fed markets.
  - **Governor rejection**: The proposed tweak violates the historical constraint to keep `score_threshold ≥ 2.2` and explicit/non-`None`. Setting `score_threshold: None` removes the score gate, which is explicitly disallowed. The new `min_price_move: 0.05` and explicit `min_volume_delta: 25000.0` do not conflict with the stated floor/explicit-volume requirements.
- [ ] **TB-803** `rejected` — Raise spike_min_volume_delta modestly to 25000.0 for watch-tier alerts, but only as a secondary filter behind price confirmation.
  - **Governor rejection**: The proposed tweak violates the historical constraint to keep `score_threshold ≥ 2.2` and explicit/non-`None`. Setting `score_threshold: None` removes the score gate, which is explicitly disallowed. The new `min_price_move: 0.05` and explicit `min_volume_delta: 25000.0` do not conflict with the stated floor/explicit-volume requirements.

---

## 2026-06-07 — Advisor snapshot 267

### Summary
The false positives are concentrated in thin, low-liquidity markets where volume-only or quote-only bursts are triggering signals despite little or no sustained price movement. Analyst labels repeatedly recommend requiring a larger confirmed price move and more traded-volume confirmation before emitting a spike.

### Next step
Add a price-confirmation gate: require a sustained multi-tick directional move and trade-confirmed volume participation before any watch-tier spike can emit.

### Suggested thresholds
`min_volume_delta` → `1.5`, `min_price_move` → `0.05`

### Recommendations

- [x] **TB-804** `applied` — Raise minimum price move from 0.03 to 0.05 for low-liquidity markets.
- [x] **TB-805** `applied` — Require at least 1.5x baseline volume delta before a spike can emit in watch-tier markets.
- [x] **TB-806** `applied` — Block signals unless price moves in the same direction across 2+ consecutive ticks or intervals.

---

## 2026-06-07 — Advisor snapshot 268

### Summary
The false positives cluster in low-liquidity or near-zero-baseline markets where large volume deltas without meaningful price movement are being labeled as signals. Several analyst notes point to quote-only or volume-only spikes as the main failure mode, especially when priceΔ is 0.0–0.04 and the move is not sustained.

### Next step
Require both a larger minimum price move and confirmation from executed-trade volume, so thin-book quote bursts cannot trigger on volume alone.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.05`

### Recommendations

- [x] **TB-807** `applied` — Raise spike_min_price_move from 0.03 to 0.05 for low-liquidity markets.
- [x] **TB-808** `applied` — Add a trade-confirmation rule: emit only if at least 60% of spike volume delta comes from executed trades rather than quotes.
- [x] **TB-809** `applied` — Increase spike_min_volume_delta modestly for low-liquidity CPI/watch markets, but only as a secondary filter behind the price-move requirement.

---

## 2026-06-07 — Advisor snapshot 269

### Summary
The false positives are dominated by thin-liquidity, volume-only bursts with little or no price movement, especially in low-baseline macro markets. Analyst labels point to the need for a stronger price-move gate and a liquidity-adjusted volume requirement rather than a blanket score cut.

### Next step
Make price movement a hard gate: require a meaningful sustained move before emitting any spike in near-zero baseline liquidity markets, and only then apply the score threshold.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-810** `rejected` — Increase min_price_move from 0.03 to 0.05 for low-liquidity markets.
  - **Governor rejection**: The proposed tweak violates the active hard-floor rule for `min_volume_delta`: historical constraints require it to be explicit/non-`None`, but the proposal sets `min_volume_delta` to `None`. It also violates the no-null-relaxation rule, which forbids setting `min_volume_delta` or `score_threshold` to `None`. `min_price_move: 0.05` is consistent with the floor, but the null volume and score settings conflict with the hardened tuning.
- [ ] **TB-811** `rejected` — Add a rule that volume spikes on near-zero baseline liquidity must exceed a larger baseline multiple, not just an absolute delta.
  - **Governor rejection**: The proposed tweak violates the active hard-floor rule for `min_volume_delta`: historical constraints require it to be explicit/non-`None`, but the proposal sets `min_volume_delta` to `None`. It also violates the no-null-relaxation rule, which forbids setting `min_volume_delta` or `score_threshold` to `None`. `min_price_move: 0.05` is consistent with the floor, but the null volume and score settings conflict with the hardened tuning.
- [ ] **TB-812** `rejected` — Keep score_threshold unchanged for now; the evidence points more strongly to a missing price-move filter than to an underpowered score cut.
  - **Governor rejection**: The proposed tweak violates the active hard-floor rule for `min_volume_delta`: historical constraints require it to be explicit/non-`None`, but the proposal sets `min_volume_delta` to `None`. It also violates the no-null-relaxation rule, which forbids setting `min_volume_delta` or `score_threshold` to `None`. `min_price_move: 0.05` is consistent with the floor, but the null volume and score settings conflict with the hardened tuning.

---

## 2026-06-07 — Advisor snapshot 270

### Summary
The false positives are concentrated in low-volatility macro contracts where modest absolute volume bursts and small price moves still pass the current trigger. Analyst labels indicate these are often routine liquidity churn rather than genuinely informative flow.

### Next step
Raise the detector’s gating requirements for macro contracts by requiring both a larger trade-driven volume surge and a larger price move before score evaluation, instead of relying on score alone.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.03`, `score_threshold` → `4.5`

### Recommendations

- [ ] **TB-813** `rejected` — Increase spike_min_volume_delta for long-dated macro names to filter routine liquidity bursts.
  - **Governor rejection**: TB-active floors is violated because the proposal relaxes `min_price_move` to `0.03`, but the historical constraint requires `min_price_move >= 0.05` globally and explicitly forbids relaxing into `0.03–0.04` ranges. The other proposed values (`min_volume_delta: 15000.0`, `score_threshold: 4.5`) are not conflicting on their face.
- [ ] **TB-814** `rejected` — Increase spike_min_price_move for low-volatility macro markets so quote churn and tiny moves do not trigger signals.
  - **Governor rejection**: TB-active floors is violated because the proposal relaxes `min_price_move` to `0.03`, but the historical constraint requires `min_price_move >= 0.05` globally and explicitly forbids relaxing into `0.03–0.04` ranges. The other proposed values (`min_volume_delta: 15000.0`, `score_threshold: 4.5`) are not conflicting on their face.
- [ ] **TB-815** `rejected` — If you want a single universal change, raise spike_score_threshold slightly and keep the stricter volume/price gates as the primary filter.
  - **Governor rejection**: TB-active floors is violated because the proposal relaxes `min_price_move` to `0.03`, but the historical constraint requires `min_price_move >= 0.05` globally and explicitly forbids relaxing into `0.03–0.04` ranges. The other proposed values (`min_volume_delta: 15000.0`, `score_threshold: 4.5`) are not conflicting on their face.

---

## 2026-06-07 — Advisor snapshot 271

### Summary
The false positives are dominated by quote-only or thin-liquidity moves that show a price change without meaningful executed trading, especially in low-trade markets. Analyst labels indicate these should be filtered more aggressively unless both volume and price movement are clearly present.

### Next step
Require nonzero executed volume plus a larger price move before emitting signals in thin markets, and raise the score cutoff modestly to suppress quote-driven noise.

### Suggested thresholds
`min_volume_delta` → `8000.0`, `min_price_move` → `0.03`, `score_threshold` → `17.0`

### Recommendations

- [ ] **TB-816** `rejected` — Increase the minimum trade-volume filter so quote-only moves do not trigger on their own.
  - **Governor rejection**: TB-Global anti-relaxation rule is violated because the proposal lowers `min_price_move` from the historical hard floor of `≥ 0.05` to `0.03`, which is an explicit relaxation into the prohibited `0.03–0.04` range. It also conflicts with the thin-market historical constraints that require `min_price_move ≥ 0.05` plus explicit volume/trade confirmation.
- [ ] **TB-817** `rejected` — Raise the price-move threshold for low-liquidity markets to avoid small, noisy moves being flagged.
  - **Governor rejection**: TB-Global anti-relaxation rule is violated because the proposal lowers `min_price_move` from the historical hard floor of `≥ 0.05` to `0.03`, which is an explicit relaxation into the prohibited `0.03–0.04` range. It also conflicts with the thin-market historical constraints that require `min_price_move ≥ 0.05` plus explicit volume/trade confirmation.
- [ ] **TB-818** `rejected` — Add or strengthen a rule that requires executed trades, not just quote changes, for spike emission.
  - **Governor rejection**: TB-Global anti-relaxation rule is violated because the proposal lowers `min_price_move` from the historical hard floor of `≥ 0.05` to `0.03`, which is an explicit relaxation into the prohibited `0.03–0.04` range. It also conflicts with the thin-market historical constraints that require `min_price_move ≥ 0.05` plus explicit volume/trade confirmation.

---

## 2026-06-07 — Advisor snapshot 272

### Summary
The false positives are concentrated in thin or quote-driven market moves where price changes are small, volume surges are noisy, and analyst labels repeatedly mark the alerts as noise/unclear/low. The pattern suggests the detector is too sensitive to low-quality flow and should require stronger confirmation from both price movement and executed volume.

### Next step
Add a dual-gate rule for low-trade markets: require both a larger price move and nonzero/executed volume before emitting, and raise the overall score threshold slightly to suppress quote-only spikes.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-819** `rejected` — Increase the minimum price move from 0.02 to 0.05 for these markets.
  - **Governor rejection**: TB-Score-Null: the proposed tweak sets `score_threshold` to `None`, which violates the historical constraint that the score gate must stay active and must never be `None`. The other thresholds (`min_price_move: 0.05`, `min_volume_delta: 20000.0`) do not conflict with the stated hard floors, but the null score relaxation does.
- [ ] **TB-820** `rejected` — Raise the minimum volume delta from 7,412 to about 20,000 to favor clear multi-trade surges over baseline noise.
  - **Governor rejection**: TB-Score-Null: the proposed tweak sets `score_threshold` to `None`, which violates the historical constraint that the score gate must stay active and must never be `None`. The other thresholds (`min_price_move: 0.05`, `min_volume_delta: 20000.0`) do not conflict with the stated hard floors, but the null score relaxation does.
- [ ] **TB-821** `rejected` — Require executed-trade volume, not quote-only changes, when the market is thin or the score is below the top tier.
  - **Governor rejection**: TB-Score-Null: the proposed tweak sets `score_threshold` to `None`, which violates the historical constraint that the score gate must stay active and must never be `None`. The other thresholds (`min_price_move: 0.05`, `min_volume_delta: 20000.0`) do not conflict with the stated hard floors, but the null score relaxation does.

---

## 2026-06-07 — Advisor snapshot 273

### Summary
Recent false positives are concentrated in low-trade or quote-driven macro markets where small price moves and modest volume deltas still score as signals. Analyst labels consistently suggest requiring stronger executed-volume confirmation before emitting alerts.

### Next step
Raise the detection floor for thin markets by requiring a larger price move plus a meaningful executed-volume surge, and do not let quote-only movement trigger a signal on its own.

### Suggested thresholds
`min_volume_delta` → `50000.0`, `min_price_move` → `0.05`

### Recommendations

- [x] **TB-822** `applied` — Increase the minimum price move from 0.03 to 0.05 for low-trade/quote-driven markets.
- [x] **TB-823** `applied` — Increase the minimum volume delta from 20,000 to 50,000 when the market is flagged as thin or quote-driven.
- [x] **TB-824** `applied` — Add a rule that quote-only moves require nonzero executed trades and a higher combined score before alerting.

---

## 2026-06-07 — Advisor snapshot 274

### Summary
The false positives are concentrated in low-liquidity CPI contracts where quote-driven or single-print moves are being mistaken for real spikes. The analyst labels consistently ask for stronger confirmation via larger price moves, higher volume multiples, and persistence across multiple trades.

### Next step
Tighten the detector for low-liquidity CPI markets by requiring both a larger price move and confirmed multi-trade volume persistence before emitting, rather than relying on a single threshold bump.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [x] **TB-825** `applied` — Raise spike_min_price_move from 0.03 to 0.05 for the low-liquidity CPI family.
- [x] **TB-826** `applied` — Add a trade-persistence rule: require at least 2-3 executed trades supporting the move before alerting.
- [x] **TB-827** `applied` — Keep spike_min_volume_delta unchanged globally, but apply a higher effective volume multiple in CPI low-liquidity markets.

---

## 2026-06-07 — Advisor snapshot 275

### Summary
False positives cluster in thin, low-liquidity CPI contracts where modest price moves and single-print or quote-driven volume bursts are being treated as spikes. Analyst labels consistently favor adding confirmation from larger price movement, persistence across multiple trades, and stronger executed-volume evidence before emitting a signal.

### Next step
Tighten the detector for this market family by requiring both a larger price move and a stronger multi-trade volume confirmation, with the score threshold raised only modestly if needed after the rule change.

### Suggested thresholds
`min_price_move` → `0.04`

### Recommendations

- [ ] **TB-828** `rejected` — Raise spike_min_price_move to filter out 2%–3% quote noise in thin CPI markets and require at least a 4% move before flagging.
  - **Governor rejection**: TB-001 / Global hard floors: the proposed `min_price_move: 0.04` violates the historical floor `min_price_move ≥ 0.05`. This is also a relaxation into the explicitly rejected 0.03–0.04 range for thin, low-liquidity CPI-style contracts, which must keep stricter price floors and executed-trade confirmation.
- [ ] **TB-829** `rejected` — Increase spike_min_volume_delta so a single burst does not trigger detection; require a clearer above-baseline volume surge sustained across multiple trades.
  - **Governor rejection**: TB-001 / Global hard floors: the proposed `min_price_move: 0.04` violates the historical floor `min_price_move ≥ 0.05`. This is also a relaxation into the explicitly rejected 0.03–0.04 range for thin, low-liquidity CPI-style contracts, which must keep stricter price floors and executed-trade confirmation.
- [ ] **TB-830** `rejected` — Add a persistence rule: only emit when the move is confirmed by multiple executed trades on both sides, not quote updates alone.
  - **Governor rejection**: TB-001 / Global hard floors: the proposed `min_price_move: 0.04` violates the historical floor `min_price_move ≥ 0.05`. This is also a relaxation into the explicitly rejected 0.03–0.04 range for thin, low-liquidity CPI-style contracts, which must keep stricter price floors and executed-trade confirmation.

---

## 2026-06-07 — Advisor snapshot 276

### Summary
False positives are concentrated in low-liquidity CPI contracts where modest price moves and quote-driven or single-print volume spikes are being labeled as signals. The analyst notes consistently point to needing a larger price move plus multi-trade persistence, while one high-volume contract already remains a true signal.

### Next step
Tighten the detector for low-liquidity CPI markets by requiring both a larger minimum price move and evidence of persistence across multiple trades before emitting a signal.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-831** `rejected` — Raise the price-move floor for low-liquidity CPI contracts from 0.03 to 0.05.
  - **Governor rejection**: TB-001 / global hard floors are violated because the proposed tweak sets min_volume_delta to None and score_threshold to None, and the historical constraints require both to remain explicit/non-None. The proposed min_price_move of 0.05 is consistent with the floor, but the null relaxations conflict with the no-null-relaxations rule and the combined confirmation gate.
- [ ] **TB-832** `rejected` — Add a multi-trade persistence rule so a spike only triggers after the move is confirmed across at least 2-3 trades, not a single quote update or print.
  - **Governor rejection**: TB-001 / global hard floors are violated because the proposed tweak sets min_volume_delta to None and score_threshold to None, and the historical constraints require both to remain explicit/non-None. The proposed min_price_move of 0.05 is consistent with the floor, but the null relaxations conflict with the no-null-relaxations rule and the combined confirmation gate.
- [ ] **TB-833** `rejected` — Increase the combined score threshold modestly for watch/notable emissions in this market family, while leaving high-volume/high-confidence markets unmuted.
  - **Governor rejection**: TB-001 / global hard floors are violated because the proposed tweak sets min_volume_delta to None and score_threshold to None, and the historical constraints require both to remain explicit/non-None. The proposed min_price_move of 0.05 is consistent with the floor, but the null relaxations conflict with the no-null-relaxations rule and the combined confirmation gate.

---

## 2026-06-07 — Advisor snapshot 277

### Summary
The false positives are concentrated in low-liquidity CPI contracts where modest price moves and single-leg volume bursts are being flagged as spikes. The analyst notes point to quote updates and small prints, so the detector needs stronger confirmation from both price action and trade persistence.

### Next step
Tighten the spike gate for low-liquidity CPI markets by requiring a larger price move plus persistence across multiple trades before emitting, rather than relying on one volume burst.

### Suggested thresholds
`min_volume_delta` → `3500.0`, `min_price_move` → `0.05`

### Recommendations

- [x] **TB-834** `applied` — Raise spike_min_price_move from 0.03 to 0.05 for CPI contracts.
- [x] **TB-835** `applied` — Increase spike_min_volume_delta from 1728.02-style triggers to a higher floor near the larger false-positive cases, around 3500.
- [x] **TB-836** `applied` — Add a persistence rule: require at least 2-3 trades confirming the move before signaling in low-liquidity monthly/long-dated CPI markets.

---

## 2026-06-07 — Advisor snapshot 278

### Summary
The false positives are concentrated in low-liquidity CPI contracts where relatively small price moves and quote-like volume bursts are being over-interpreted as spikes. The analyst notes point to a need for stronger confirmation from both price persistence and multi-trade participation before emission.

### Next step
Tighten the detector for low-liquidity CPI names by requiring a larger price move plus persistence across multiple trades, and make the score threshold harder to clear for watch/notable-tier events.

### Suggested thresholds
`min_price_move` → `0.07`, `score_threshold` → `8.0`

### Recommendations

- [ ] **TB-837** `rejected` — Raise spike_min_price_move to reduce quote-update noise in long-dated CPI contracts.
  - **Governor rejection**: TB-001 / Global hard floors is violated because min_volume_delta is set to None, but the historical constraints require min_volume_delta to be explicit and non-None with a real volume gate in place. The proposed change also conflicts with the low-liquidity/watch-tier rules that require executed-trade or trade-count confirmation, since removing the volume gate weakens the required multi-trade confirmation.
- [ ] **TB-838** `rejected` — Add a persistence rule: require the price move to hold across multiple trades before signaling.
  - **Governor rejection**: TB-001 / Global hard floors is violated because min_volume_delta is set to None, but the historical constraints require min_volume_delta to be explicit and non-None with a real volume gate in place. The proposed change also conflicts with the low-liquidity/watch-tier rules that require executed-trade or trade-count confirmation, since removing the volume gate weakens the required multi-trade confirmation.
- [ ] **TB-839** `rejected` — Increase spike_score_threshold modestly so borderline low-liquidity bursts do not emit.
  - **Governor rejection**: TB-001 / Global hard floors is violated because min_volume_delta is set to None, but the historical constraints require min_volume_delta to be explicit and non-None with a real volume gate in place. The proposed change also conflicts with the low-liquidity/watch-tier rules that require executed-trade or trade-count confirmation, since removing the volume gate weakens the required multi-trade confirmation.

---

## 2026-06-07 — Advisor snapshot 279

### Summary
The false positives are concentrated in low-liquidity CPI contracts where modest price moves and large-looking volume deltas are likely being driven by quote updates or small prints rather than durable information. Both labeled examples suggest the detector should demand stronger price confirmation and persistence before emitting a spike.

### Next step
Tighten the rule for long-dated, low-liquidity CPI markets by requiring both a larger price move and multi-trade persistence before emission, rather than relying on volume delta alone.

### Suggested thresholds
`min_volume_delta` → `3000.0`, `min_price_move` → `0.08`

### Recommendations

- [x] **TB-840** `applied` — Raise the minimum price move to 0.08 for CPI spikes in this liquidity regime.
- [x] **TB-841** `applied` — Increase the minimum volume delta to 3000 for these contracts, but only if paired with persistence across multiple trades.
- [x] **TB-842** `applied` — Add a persistence filter: require at least 2 consecutive trades confirming the move, including activity from both sides, before signaling.

---

## 2026-06-07 — Advisor snapshot 280

### Summary
The false positives are coming from thin or low-price markets where a single quote burst or tiny executed volume can clear the current filters without a durable move. The analyst labels consistently favor requiring more confirmation from both price movement and executed-trade activity.

### Next step
Raise the detector’s confirmation bar for low-liquidity signals by requiring both a larger sustained price move and multiple directional trades before emission, rather than relying on volume alone.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-843** `rejected` — Increase spike_min_price_move from 0.03 to 0.05 for thin Kalshi-style rate/CPI markets.
  - **Governor rejection**: TB-001 / TB-002 / TB-003 conflict: the proposed tweak sets `score_threshold` to `None`, which violates the active global floor requiring `score_threshold ≥ 2.2` and explicit/non-`None`. It also replaces the prior low-liquidity confirmation regime with a volume-only floor (`min_volume_delta: 15000.0`) without preserving the explicitly required directional/trade-confirmation gates for thin markets, which conflicts with the historical constraints that low-liquidity, thin, and quote-driven markets need executed-trade confirmation, persistence, and/or strong one-sided flow before emission.
- [ ] **TB-844** `rejected` — Add an executed-trade confirmation rule: require at least 2 directional trades, or equivalent non-quote activity, before a spike can emit.
  - **Governor rejection**: TB-001 / TB-002 / TB-003 conflict: the proposed tweak sets `score_threshold` to `None`, which violates the active global floor requiring `score_threshold ≥ 2.2` and explicit/non-`None`. It also replaces the prior low-liquidity confirmation regime with a volume-only floor (`min_volume_delta: 15000.0`) without preserving the explicitly required directional/trade-confirmation gates for thin markets, which conflicts with the historical constraints that low-liquidity, thin, and quote-driven markets need executed-trade confirmation, persistence, and/or strong one-sided flow before emission.
- [ ] **TB-845** `rejected` — Raise spike_min_volume_delta modestly to reduce quote-burst triggers on very low-price markets, while preserving watch-tier sensitivity.
  - **Governor rejection**: TB-001 / TB-002 / TB-003 conflict: the proposed tweak sets `score_threshold` to `None`, which violates the active global floor requiring `score_threshold ≥ 2.2` and explicit/non-`None`. It also replaces the prior low-liquidity confirmation regime with a volume-only floor (`min_volume_delta: 15000.0`) without preserving the explicitly required directional/trade-confirmation gates for thin markets, which conflicts with the historical constraints that low-liquidity, thin, and quote-driven markets need executed-trade confirmation, persistence, and/or strong one-sided flow before emission.

---

## 2026-06-07 — Advisor snapshot 281

### Summary
The false positives are concentrated in thin or low-price markets where bursty volume and quote-only activity produce small or noisy price changes. Analyst labels consistently suggest requiring stronger price confirmation and/or executed-trade confirmation, not just volume spikes.

### Next step
Raise the detector’s price-move requirement and add a trade-quality gate for thin markets so bursty volume alone cannot trigger an alert.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-846** `rejected` — Increase spike_min_price_move to 0.05 to suppress low-information 1%–4% moves that are being labeled noise.
  - **Governor rejection**: TB-XXX violated: the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical constraint that `score_threshold` / `spike_score_threshold` must remain explicit and >= 2.2. Although `min_price_move` is kept at 0.05 and `min_volume_delta` is explicit, removing the score gate is a prohibited null relaxation and weakens the low-confidence brake.
- [ ] **TB-847** `rejected` — Add an executed-trade confirmation rule: require multiple directional trades or nonzero executed volume, not quote-only bursts.
  - **Governor rejection**: TB-XXX violated: the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical constraint that `score_threshold` / `spike_score_threshold` must remain explicit and >= 2.2. Although `min_price_move` is kept at 0.05 and `min_volume_delta` is explicit, removing the score gate is a prohibited null relaxation and weakens the low-confidence brake.
- [ ] **TB-848** `rejected` — Raise spike_min_volume_delta modestly for watch-tier and low-price markets to filter small absolute trades that still look spiky.
  - **Governor rejection**: TB-XXX violated: the proposed tweak sets `score_threshold` to `None`, which conflicts with the historical constraint that `score_threshold` / `spike_score_threshold` must remain explicit and >= 2.2. Although `min_price_move` is kept at 0.05 and `min_volume_delta` is explicit, removing the score gate is a prohibited null relaxation and weakens the low-confidence brake.

---

## 2026-06-07 — Advisor snapshot 282

### Summary
The false positives are concentrated in thin, low-baseline markets where quote-only or bursty activity produces large volume deltas without reliable confirmation from executed trades or sustained price follow-through. The most consistent fix is to require stronger confirmation before emitting a spike.

### Next step
Require at least one executed trade or directional trade imbalance before firing on thin markets, and raise the price-move floor for quote-only alerts.

### Suggested thresholds
`min_volume_delta` → `3000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-849** `rejected` — Increase spike_min_volume_delta to 3000.0 to reduce thin-market bursts that are too easy to trigger.
  - **Governor rejection**: Yes. The proposed tweak violates the historical constraint that the global score gate must remain explicit and non-None: `score_threshold: None` conflicts with the previously enforced `score_threshold ≥ 2.2` and the rule that the score gate must never be removed. It also does not satisfy the trade-confirmation/persistence constraints for thin markets because it only mentions requiring one executed trade or directional imbalance, which is weaker than the historical requirements for sustained follow-through and stronger confirmation in thin or mechanical markets.
- [ ] **TB-850** `rejected` — Increase spike_min_price_move to 0.05 so tiny absolute moves in low-price markets do not emit alerts.
  - **Governor rejection**: Yes. The proposed tweak violates the historical constraint that the global score gate must remain explicit and non-None: `score_threshold: None` conflicts with the previously enforced `score_threshold ≥ 2.2` and the rule that the score gate must never be removed. It also does not satisfy the trade-confirmation/persistence constraints for thin markets because it only mentions requiring one executed trade or directional imbalance, which is weaker than the historical requirements for sustained follow-through and stronger confirmation in thin or mechanical markets.
- [ ] **TB-851** `rejected` — Add a confirmation rule: suppress alerts unless there is at least one executed trade or sustained follow-through, especially when volume is quote-only.
  - **Governor rejection**: Yes. The proposed tweak violates the historical constraint that the global score gate must remain explicit and non-None: `score_threshold: None` conflicts with the previously enforced `score_threshold ≥ 2.2` and the rule that the score gate must never be removed. It also does not satisfy the trade-confirmation/persistence constraints for thin markets because it only mentions requiring one executed trade or directional imbalance, which is weaker than the historical requirements for sustained follow-through and stronger confirmation in thin or mechanical markets.

---

## 2026-06-07 — Advisor snapshot 283

### Summary
The false positives are concentrated in thin or quote-driven markets where volume bursts and small price moves are being treated as spikes without enough execution confirmation. Analysts repeatedly recommend tightening confirmation rules, especially for CPI and Fed markets, to avoid noisy single-burst alerts.

### Next step
Add a confirmation rule requiring at least one executed trade or directional side imbalance before emitting a spike, and raise the price-move floor slightly for thin markets rather than relying on volume alone.

### Suggested thresholds
`min_volume_delta` → `3000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-852** `rejected` — Increase the minimum price move to 0.05 to filter out small quote-only oscillations in thin markets.
  - **Governor rejection**: TB-003 is violated because the proposed tweak sets score_threshold to None, but the historical hard floor requires score_threshold/spike_score_threshold to be explicit and >= 2.2, never None. The proposed min_price_move = 0.05 and explicit min_volume_delta = 3000.0 do not conflict.
- [ ] **TB-853** `rejected` — Require at least one executed trade or a confirmed side imbalance before any spike alert fires.
  - **Governor rejection**: TB-003 is violated because the proposed tweak sets score_threshold to None, but the historical hard floor requires score_threshold/spike_score_threshold to be explicit and >= 2.2, never None. The proposed min_price_move = 0.05 and explicit min_volume_delta = 3000.0 do not conflict.
- [ ] **TB-854** `rejected` — Raise the minimum volume delta modestly to 3000 so bursty low-quality flow does not pass on volume alone.
  - **Governor rejection**: TB-003 is violated because the proposed tweak sets score_threshold to None, but the historical hard floor requires score_threshold/spike_score_threshold to be explicit and >= 2.2, never None. The proposed min_price_move = 0.05 and explicit min_volume_delta = 3000.0 do not conflict.

---

## 2026-06-07 — Advisor snapshot 284

### Summary
The false positives are concentrated in thin, bursty markets where large volume deltas and/or price jumps still do not correspond to confirmed executed-trade follow-through. The strongest pattern is that quote-only or low-quality moves are being promoted too easily, especially when analyst labels call them noise or unclear.

### Next step
Increase the minimum price-move requirement and add an execution-quality gate: require either at least one executed trade or clear side imbalance before emitting a spike signal.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-855** `rejected` — Raise the volume floor for thin markets to suppress burst-driven noise.
  - **Governor rejection**: TB-002 / TB-003 are violated because the proposed tweak sets score_threshold to None, which explicitly removes the live secondary score brake. Historical constraints require score_threshold to remain explicit and non-None, with score_threshold ≥ 2.2 globally, so nulling it conflicts with the no-null-relaxation and score-floor rules.
- [ ] **TB-856** `rejected` — Require a larger fractional price move before triggering on quote-only moves.
  - **Governor rejection**: TB-002 / TB-003 are violated because the proposed tweak sets score_threshold to None, which explicitly removes the live secondary score brake. Historical constraints require score_threshold to remain explicit and non-None, with score_threshold ≥ 2.2 globally, so nulling it conflicts with the no-null-relaxation and score-floor rules.
- [ ] **TB-857** `rejected` — Add a confirmation rule that prefers executed trades or sustained follow-through over raw quote changes.
  - **Governor rejection**: TB-002 / TB-003 are violated because the proposed tweak sets score_threshold to None, which explicitly removes the live secondary score brake. Historical constraints require score_threshold to remain explicit and non-None, with score_threshold ≥ 2.2 globally, so nulling it conflicts with the no-null-relaxation and score-floor rules.

---

## 2026-06-07 — Advisor snapshot 285

### Summary
The false positives cluster around thin markets where large volume bursts or quote-only moves are being flagged despite weak or no executed-trade confirmation. The analyst notes consistently recommend tighter trade-confirmation and/or larger price-move requirements to suppress noisy alerts.

### Next step
Add a trade-confirmation gate for spike emission: require at least one executed trade or confirmed side imbalance before signaling, and raise the minimum price-move threshold for quote-only bursts in thin markets.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-858** `rejected` — Increase spike_min_price_move from 0.03 to 0.05 for thin or quote-driven markets.
  - **Governor rejection**: TB-HIST-03 / TB-HIST-05 are violated because the proposed tweak sets `min_volume_delta` to None and `score_threshold` to None, which conflicts with the historical requirement that both be explicit, non-None, and for `score_threshold` to be >= 2.2. It also weakens the structural filter for thin markets by making trade confirmation conditional only on 'at least one executed trade or confirmed side imbalance,' which is looser than the historical trade-count and persistence gates for low-liquidity/watch-tier markets.
- [ ] **TB-859** `rejected` — Require at least one executed trade, or equivalent trade-confirmation, before emitting a spike.
  - **Governor rejection**: TB-HIST-03 / TB-HIST-05 are violated because the proposed tweak sets `min_volume_delta` to None and `score_threshold` to None, which conflicts with the historical requirement that both be explicit, non-None, and for `score_threshold` to be >= 2.2. It also weakens the structural filter for thin markets by making trade confirmation conditional only on 'at least one executed trade or confirmed side imbalance,' which is looser than the historical trade-count and persistence gates for low-liquidity/watch-tier markets.
- [ ] **TB-860** `rejected` — Raise spike_min_volume_delta modestly only for low-baseline markets, rather than globally.
  - **Governor rejection**: TB-HIST-03 / TB-HIST-05 are violated because the proposed tweak sets `min_volume_delta` to None and `score_threshold` to None, which conflicts with the historical requirement that both be explicit, non-None, and for `score_threshold` to be >= 2.2. It also weakens the structural filter for thin markets by making trade confirmation conditional only on 'at least one executed trade or confirmed side imbalance,' which is looser than the historical trade-count and persistence gates for low-liquidity/watch-tier markets.

---

## 2026-06-07 — Advisor snapshot 286

### Summary
The false positives are concentrated in thin or low-baseline markets where quote-only bursts or one-sided prints can create large volume deltas without reliable execution confirmation. The current pattern suggests the detector is too sensitive to volume alone and needs stronger trade-confirmation or price-move requirements.

### Next step
Raise the minimum trade-confirmation bar for thin markets by requiring either multiple executed trades or a larger price move before emitting a spike.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.05`, `score_threshold` → `25.0`

### Recommendations

- [x] **TB-861** `applied` — Increase spike_min_price_move to 0.05 to suppress low-quality quote-only bursts.
- [x] **TB-862** `applied` — Increase spike_min_volume_delta to 5000.0 for thin CPI/FED-style markets to avoid one-sided microprints.
- [x] **TB-863** `applied` — Increase spike_score_threshold modestly to 25.0 so low-confidence bursts do not emit unless they also clear stronger trade confirmation.

---

## 2026-06-07 — Advisor snapshot 287

### Summary
The false positives are concentrated in thin or quote-only markets where volume/price blips are getting flagged without enough executed-trade confirmation. Analyst notes repeatedly ask for stronger volume and follow-through filters, especially in CPI and Fed markets.

### Next step
Add a trade-confirmation gate for spikes: require at least one executed trade or multi-trade confirmation in addition to the existing volume/price thresholds, and slightly raise the score floor only for low-liquidity markets.

### Suggested thresholds
`min_volume_delta` → `3000.0`, `min_price_move` → `0.05`, `score_threshold` → `6.0`

### Recommendations

- [x] **TB-864** `applied` — Raise spike_min_volume_delta to about 3000 to suppress thin-market one-sided prints while preserving the larger confirmed moves seen in fed-rate signals.
- [x] **TB-865** `applied` — Raise spike_min_price_move to about 0.05 so small quote-only moves do not emit signals unless they are backed by execution volume.
- [x] **TB-866** `applied` — Raise spike_score_threshold modestly to about 6.0, but apply it primarily to low-baseline CPI/Fed markets rather than all instruments.

---

## 2026-06-07 — Advisor snapshot 288

### Summary
The false positives are concentrated in thin or bursty markets where a large score is driven by one-sided volume or quote-only activity rather than a convincing trade-confirmed move. The pattern suggests the detector is over-sensitive to isolated volume spikes, especially when price confirmation is weak or absent.

### Next step
Raise the bar on confirmation before emission: require both a larger price move and multi-trade confirmation for low-baseline markets, rather than relying on volume alone.

### Suggested thresholds
`min_price_move` → `0.05`, `score_threshold` → `22.0`

### Recommendations

- [ ] **TB-867** `rejected` — Increase spike_min_price_move from 0.03 to 0.05 to suppress quote-only or weak-move bursts.
  - **Governor rejection**: TB-001 / TB-002 / TB-003 are violated because the proposal sets min_volume_delta to None, which removes the explicitly required hard volume floor and weakens the executed-volume gate for thin or quote-driven markets. TB-004 / TB-005 are also in tension because the summary says to require multi-trade confirmation for low-baseline markets, but the proposed thresholds do not encode any trade-count or persistence gate. The score_threshold=22.0 is not the conflict; the conflict is the null volume floor and missing explicit confirmation constraints.
- [ ] **TB-868** `rejected` — Add a multi-trade confirmation rule for thin markets: do not emit on a single print even if volume_delta is high.
  - **Governor rejection**: TB-001 / TB-002 / TB-003 are violated because the proposal sets min_volume_delta to None, which removes the explicitly required hard volume floor and weakens the executed-volume gate for thin or quote-driven markets. TB-004 / TB-005 are also in tension because the summary says to require multi-trade confirmation for low-baseline markets, but the proposed thresholds do not encode any trade-count or persistence gate. The score_threshold=22.0 is not the conflict; the conflict is the null volume floor and missing explicit confirmation constraints.
- [ ] **TB-869** `rejected` — If you keep volume sensitivity high, raise spike_score_threshold modestly so low-quality volume bursts no longer clear the combined gate.
  - **Governor rejection**: TB-001 / TB-002 / TB-003 are violated because the proposal sets min_volume_delta to None, which removes the explicitly required hard volume floor and weakens the executed-volume gate for thin or quote-driven markets. TB-004 / TB-005 are also in tension because the summary says to require multi-trade confirmation for low-baseline markets, but the proposed thresholds do not encode any trade-count or persistence gate. The score_threshold=22.0 is not the conflict; the conflict is the null volume floor and missing explicit confirmation constraints.

---

## 2026-06-07 — Advisor snapshot 289

### Summary
The false positives are concentrated in **large-volume, low-information bursts**: near-certain markets with tiny price moves, very thin markets with one-sided prints, and quote-only bursts that lack trade confirmation. The detector is over-sensitive to volume alone and needs stronger confirmation from price movement and executed trades.

### Next step
Raise the **minimum volume delta** and add a stricter **trade-confirmation / price-move gate** so large but informationally weak bursts do not emit signals.

### Suggested thresholds
`min_volume_delta` → `5000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-870** `rejected` — Increase spike_min_volume_delta to filter near-certain markets where ~1% price moves are generating noisy alerts.
  - **Governor rejection**: Violates the historical core active floor for **min_price_move**: the proposal sets **min_price_move = 0.03**, which relaxes the explicitly required **min_price_move ≥ 0.05** and contradicts the low-liquidity / watch / notable / high-odds requirement to enforce at least 0.05. It also conflicts with the core active floor on **score_threshold** by setting it to **None** instead of keeping it explicit and **≥ 2.2**.
- [ ] **TB-871** `rejected` — Require a larger minimum price move before emitting in thin or quote-driven markets, especially when volume delta is small or single-sided.
  - **Governor rejection**: Violates the historical core active floor for **min_price_move**: the proposal sets **min_price_move = 0.03**, which relaxes the explicitly required **min_price_move ≥ 0.05** and contradicts the low-liquidity / watch / notable / high-odds requirement to enforce at least 0.05. It also conflicts with the core active floor on **score_threshold** by setting it to **None** instead of keeping it explicit and **≥ 2.2**.
- [ ] **TB-872** `rejected` — Raise the combined score threshold modestly only after tightening the volume and confirmation gates, so genuinely informative high-volume events still pass.
  - **Governor rejection**: Violates the historical core active floor for **min_price_move**: the proposal sets **min_price_move = 0.03**, which relaxes the explicitly required **min_price_move ≥ 0.05** and contradicts the low-liquidity / watch / notable / high-odds requirement to enforce at least 0.05. It also conflicts with the core active floor on **score_threshold** by setting it to **None** instead of keeping it explicit and **≥ 2.2**.

---

## 2026-06-07 — Advisor snapshot 290

### Summary
The false positives cluster around thin or near-certain markets where quote-driven or one-sided volume bursts create signals despite little meaningful price discovery. The strongest pattern is to require more executed-trade confirmation, especially when price is already extreme or baseline liquidity is low.

### Next step
Add a trade-confirmation gate before emitting any spike signal: require multiple executed trades (or equivalent trade-count confirmation) in addition to volume delta, and apply a higher volume floor for thin or near-certain markets.

### Suggested thresholds
`min_volume_delta` → `15000.0`

### Recommendations

- [ ] **TB-873** `rejected` — Raise the minimum volume delta modestly for thin markets to suppress one-sided prints, especially low-price CPI-style contracts.
  - **Governor rejection**: TB-GLOBAL-03 / TB-GLOBAL-04 are violated because the proposed tweak sets `min_price_move` to `None` and `score_threshold` to `None`, which is an explicit relaxation of required non-`None` floors. TB-GLOBAL-01 is also violated because the historical hard floor requires `min_price_move >= 0.05`, but the proposal removes that floor entirely. The added trade-confirmation gate is compatible with the history, but not when paired with nulling the core thresholds.
- [ ] **TB-874** `rejected` — Add a minimum executed-trade count or multi-trade confirmation rule so single bursts of volume cannot trigger signals on quote-driven moves.
  - **Governor rejection**: TB-GLOBAL-03 / TB-GLOBAL-04 are violated because the proposed tweak sets `min_price_move` to `None` and `score_threshold` to `None`, which is an explicit relaxation of required non-`None` floors. TB-GLOBAL-01 is also violated because the historical hard floor requires `min_price_move >= 0.05`, but the proposal removes that floor entirely. The added trade-confirmation gate is compatible with the history, but not when paired with nulling the core thresholds.
- [ ] **TB-875** `rejected` — Increase the score threshold only slightly, and preferably only for near-certain markets, so genuinely informative high-volume moves are not muted.
  - **Governor rejection**: TB-GLOBAL-03 / TB-GLOBAL-04 are violated because the proposed tweak sets `min_price_move` to `None` and `score_threshold` to `None`, which is an explicit relaxation of required non-`None` floors. TB-GLOBAL-01 is also violated because the historical hard floor requires `min_price_move >= 0.05`, but the proposal removes that floor entirely. The added trade-confirmation gate is compatible with the history, but not when paired with nulling the core thresholds.

---

## 2026-06-07 — Advisor snapshot 291

### Summary
The false positives are concentrated in thin or near-certain markets where quote updates or one-sided prints create large volume deltas without meaningful executed-trade confirmation, especially when price moves are small or mechanically induced. Analyst notes repeatedly call for stricter trade-confirmation and higher absolute-volume gating in sparse-liquidity CPI and rate markets.

### Next step
Add an executed-trade confirmation gate and raise the minimum volume delta so quote-driven bursts in thin markets do not trigger unless there is both meaningful price movement and multiple real trades.

### Suggested thresholds
`min_volume_delta` → `30000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-876** `rejected` — Increase min_volume_delta to 30000.0 to suppress sparse-liquidity noise while preserving the clearly informative high-volume cases.
  - **Governor rejection**: TB-001 / active hard floors are violated because the proposed tweak lowers `min_price_move` to 0.03, but the historical constraints require `min_price_move ≥ 0.05` for low-liquidity/high-odds/watch/notable markets and explicitly say not to relax into 0.03–0.04. TB-005 is also violated because `score_threshold` is set to `None`, which conflicts with the hard floor requiring `score_threshold ≥ 2.2` remain explicit/non-None. The new trade-confirmation and higher volume gate are compatible, but the price-floor relaxation and null score threshold are not.
- [ ] **TB-877** `rejected` — Raise min_price_move to 0.03 so 1% to 2% nudges in near-certain or thin markets do not emit signals without stronger evidence.
  - **Governor rejection**: TB-001 / active hard floors are violated because the proposed tweak lowers `min_price_move` to 0.03, but the historical constraints require `min_price_move ≥ 0.05` for low-liquidity/high-odds/watch/notable markets and explicitly say not to relax into 0.03–0.04. TB-005 is also violated because `score_threshold` is set to `None`, which conflicts with the hard floor requiring `score_threshold ≥ 2.2` remain explicit/non-None. The new trade-confirmation and higher volume gate are compatible, but the price-floor relaxation and null score threshold are not.
- [ ] **TB-878** `rejected` — Require at least 2 executed trades before emitting a spike signal in CPI and rate markets, or equivalently add a trade-count filter alongside the existing score.
  - **Governor rejection**: TB-001 / active hard floors are violated because the proposed tweak lowers `min_price_move` to 0.03, but the historical constraints require `min_price_move ≥ 0.05` for low-liquidity/high-odds/watch/notable markets and explicitly say not to relax into 0.03–0.04. TB-005 is also violated because `score_threshold` is set to `None`, which conflicts with the hard floor requiring `score_threshold ≥ 2.2` remain explicit/non-None. The new trade-confirmation and higher volume gate are compatible, but the price-floor relaxation and null score threshold are not.

---

## 2026-06-07 — Advisor snapshot 292

### Summary
The false positives cluster in thin or near-certain markets where small price moves and quote-driven activity are being scored as spikes, especially when there is little executed-trade confirmation. The analyst notes consistently point to raising the volume bar and adding a trade-count or multi-trade filter rather than relying on price move alone.

### Next step
Raise the minimum volume requirement and require executed-trade confirmation in sparse-liquidity markets; do not lower the price-move threshold further.

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.02`

### Recommendations

- [ ] **TB-879** `rejected` — Increase spike_min_volume_delta to about 25000 to filter one-sided prints and quote noise in thin markets.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it relaxes the explicitly tightened **price floor**: the proposed `min_price_move: 0.02` violates the global rule requiring `min_price_move >= 0.05` for quote-driven, thin, watch, notable, NBA series/playoff winner, CPI/Fed, and similar markets. It also conflicts with the low-liquidity confirmation rules by omitting an explicit non-`None` `score_threshold` despite the live secondary brake requiring `score_threshold >= 2.2`, and by not specifying the required executed-trade/trade-count gate for sparse-liquidity markets.
- [ ] **TB-880** `rejected` — Add a minimum executed-trade or multi-trade confirmation rule for CPI and other sparse-liquidity markets before emitting a spike.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it relaxes the explicitly tightened **price floor**: the proposed `min_price_move: 0.02` violates the global rule requiring `min_price_move >= 0.05` for quote-driven, thin, watch, notable, NBA series/playoff winner, CPI/Fed, and similar markets. It also conflicts with the low-liquidity confirmation rules by omitting an explicit non-`None` `score_threshold` despite the live secondary brake requiring `score_threshold >= 2.2`, and by not specifying the required executed-trade/trade-count gate for sparse-liquidity markets.
- [ ] **TB-881** `rejected` — Keep spike_min_price_move at 0.02 for now, but require the combined score to clear a higher bar only when volume is below the new minimum.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it relaxes the explicitly tightened **price floor**: the proposed `min_price_move: 0.02` violates the global rule requiring `min_price_move >= 0.05` for quote-driven, thin, watch, notable, NBA series/playoff winner, CPI/Fed, and similar markets. It also conflicts with the low-liquidity confirmation rules by omitting an explicit non-`None` `score_threshold` despite the live secondary brake requiring `score_threshold >= 2.2`, and by not specifying the required executed-trade/trade-count gate for sparse-liquidity markets.

---

## 2026-06-07 — Advisor snapshot 293

### Summary
The false positives cluster in thin, low-priced, or near-certain markets where quote-only or one-sided activity can create large apparent spikes without meaningful information change. The common fix is to require more execution confirmation and a larger sustained move before emitting a signal.

### Next step
Add an execution-confirmation rule for thin markets: require at least 2 executed trades from more than one participant or multiple ticks of persistence before signaling, especially when yes price is below 0.25 or above 0.90.

### Recommendations

- [ ] **TB-882** `rejected` — Raise the minimum volume delta modestly for low-liquidity contracts to suppress quote-driven spikes.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it relaxes multiple explicitly tightened active floors: `min_price_move` is set to `None`, violating the global requirement `min_price_move ≥ 0.05` and the low-liquidity/NBA/watch-tier floor of 0.05; `score_threshold` is set to `None`, violating the global requirement `score_threshold ≥ 2.2` and the rule that score gating must remain a live secondary brake; and `min_volume_delta` is set to `None`, violating the requirement that `min_volume_delta` remain explicit/non-None. The added execution-confirmation requirement is compatible, but it does not offset these threshold relaxations.
- [ ] **TB-883** `rejected` — Increase the minimum price-move requirement for very low-priced or near-certain markets so small percentage moves do not trigger on huge volume alone.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it relaxes multiple explicitly tightened active floors: `min_price_move` is set to `None`, violating the global requirement `min_price_move ≥ 0.05` and the low-liquidity/NBA/watch-tier floor of 0.05; `score_threshold` is set to `None`, violating the global requirement `score_threshold ≥ 2.2` and the rule that score gating must remain a live secondary brake; and `min_volume_delta` is set to `None`, violating the requirement that `min_volume_delta` remain explicit/non-None. The added execution-confirmation requirement is compatible, but it does not offset these threshold relaxations.
- [ ] **TB-884** `rejected` — Keep the score threshold mostly unchanged and use a liquidity/exec-trade filter first, since the false positives are concentrated in specific market conditions rather than across all signals.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it relaxes multiple explicitly tightened active floors: `min_price_move` is set to `None`, violating the global requirement `min_price_move ≥ 0.05` and the low-liquidity/NBA/watch-tier floor of 0.05; `score_threshold` is set to `None`, violating the global requirement `score_threshold ≥ 2.2` and the rule that score gating must remain a live secondary brake; and `min_volume_delta` is set to `None`, violating the requirement that `min_volume_delta` remain explicit/non-None. The added execution-confirmation requirement is compatible, but it does not offset these threshold relaxations.

---

## 2026-06-07 — Advisor snapshot 294

### Summary
The false positives are concentrated in low-liquidity, low-priced markets where quote updates or one-off volume bursts trigger spikes without sustained execution or meaningful price follow-through. The strongest pattern is that small price moves can still produce very large volume deltas, especially in thin macro and near-certain contracts.

### Next step
Add a liquidity-aware rule: require either a larger sustained price move or multiple executed trades across distinct participants before emitting on thin markets, rather than relying on volume delta alone.

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-885** `rejected` — Increase spike_min_volume_delta for thin, low-priced contracts so quote-driven bursts do not clear the detector.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it sets `score_threshold: None`, which violates the global hard floor requiring `score_threshold >= 2.2` and never `None`. It also weakens the historical rule for thin / low-liquidity / watch / notable markets by replacing the required stricter confirmation with a rule that can emit on a larger sustained price move or multiple trades, but without preserving the active score gate. This is a blanket relaxation of an active threshold rather than an added gate, which is disallowed.
- [ ] **TB-886** `rejected` — Raise spike_min_price_move modestly for near-certain and sparse-liquidity markets to require clearer follow-through.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it sets `score_threshold: None`, which violates the global hard floor requiring `score_threshold >= 2.2` and never `None`. It also weakens the historical rule for thin / low-liquidity / watch / notable markets by replacing the required stricter confirmation with a rule that can emit on a larger sustained price move or multiple trades, but without preserving the active score gate. This is a blanket relaxation of an active threshold rather than an added gate, which is disallowed.
- [ ] **TB-887** `rejected` — Add an executed-trade confirmation filter: suppress signals unless the move is backed by repeated prints, not just quote changes.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it sets `score_threshold: None`, which violates the global hard floor requiring `score_threshold >= 2.2` and never `None`. It also weakens the historical rule for thin / low-liquidity / watch / notable markets by replacing the required stricter confirmation with a rule that can emit on a larger sustained price move or multiple trades, but without preserving the active score gate. This is a blanket relaxation of an active threshold rather than an added gate, which is disallowed.

---

## 2026-06-07 — Advisor snapshot 295

### Summary
Recent false positives cluster in thin or low-priced markets where quote-only activity or small price changes are being over-interpreted as spikes. The strongest pattern is that volume and price thresholds are too permissive when there is no sustained, executed-trade confirmation.

### Next step
Add an executed-trade confirmation rule for low-liquidity markets and raise the volume threshold there, rather than relying on price move alone.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-888** `rejected` — Increase the minimum volume delta for thin macro and near-certain markets, since several noisy alerts had very large volume but little informational price change.
  - **Governor rejection**: The proposed tweak violates the historical floor constraints by setting `min_volume_delta` to `None` and `score_threshold` to `None`, which conflicts with the active rules requiring both to remain explicit/non-None. This also conflicts with the no-blanket-relaxations policy because it removes core gates instead of tightening them via additional confirmation. The `min_price_move: 0.05` value is consistent with the active floor, but the null relaxations are not.
- [ ] **TB-889** `rejected` — Require a larger sustained price move when yes-price is extreme or when the move is only a single-tick quote update.
  - **Governor rejection**: The proposed tweak violates the historical floor constraints by setting `min_volume_delta` to `None` and `score_threshold` to `None`, which conflicts with the active rules requiring both to remain explicit/non-None. This also conflicts with the no-blanket-relaxations policy because it removes core gates instead of tightening them via additional confirmation. The `min_price_move: 0.05` value is consistent with the active floor, but the null relaxations are not.
- [ ] **TB-890** `rejected` — Add a filter that suppresses signals unless there are repeated executed yes/no trades or multi-tick persistence, especially in CPI and Fed contracts.
  - **Governor rejection**: The proposed tweak violates the historical floor constraints by setting `min_volume_delta` to `None` and `score_threshold` to `None`, which conflicts with the active rules requiring both to remain explicit/non-None. This also conflicts with the no-blanket-relaxations policy because it removes core gates instead of tightening them via additional confirmation. The `min_price_move: 0.05` value is consistent with the active floor, but the null relaxations are not.

---

## 2026-06-07 — Advisor snapshot 296

### Summary
The false positives are concentrated in thin, low-liquidity macro contracts where quote-only or low-execution moves are being mistaken for real spikes. The strongest pattern is that analyst-labeled noise appears when price moves are modest but volume/quote activity is bursty rather than sustained or trade-confirmed.

### Next step
Add a traded-volume confirmation rule for low-liquidity contracts and raise the volume-delta floor modestly before tightening price-move or score thresholds.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-891** `rejected` — Require executed-trade confirmation for spikes in low-liquidity Fed/CPI markets, especially when the move is quote-driven.
  - **Governor rejection**: TB-001 is violated because the proposed `min_price_move: 0.04` relaxes the explicitly enforced global price floor of `min_price_move >= 0.05`. TB-003 is also violated because `score_threshold: None` removes the explicit score floor, but the historical constraint requires `score_threshold >= 2.2` and says it must remain explicit/non-`None` as a secondary brake. The higher `min_volume_delta` does not offset these regressions.
- [ ] **TB-892** `rejected` — Raise the minimum volume delta to filter out thin-market burstiness while preserving genuinely high-participation events.
  - **Governor rejection**: TB-001 is violated because the proposed `min_price_move: 0.04` relaxes the explicitly enforced global price floor of `min_price_move >= 0.05`. TB-003 is also violated because `score_threshold: None` removes the explicit score floor, but the historical constraint requires `score_threshold >= 2.2` and says it must remain explicit/non-`None` as a secondary brake. The higher `min_volume_delta` does not offset these regressions.
- [ ] **TB-893** `rejected` — Increase the minimum price move slightly only for sparse-liquidity contracts, rather than globally, to avoid muting informative flow.
  - **Governor rejection**: TB-001 is violated because the proposed `min_price_move: 0.04` relaxes the explicitly enforced global price floor of `min_price_move >= 0.05`. TB-003 is also violated because `score_threshold: None` removes the explicit score floor, but the historical constraint requires `score_threshold >= 2.2` and says it must remain explicit/non-`None` as a secondary brake. The higher `min_volume_delta` does not offset these regressions.

---

## 2026-06-07 — Advisor snapshot 297

### Summary
The false positives cluster around low-liquidity macro contracts where quote-only or thin activity triggers spikes despite weak confirmation from executed trades or sustained follow-through. The analyst labels consistently favor stricter confirmation from volume and persistence rather than a much higher raw score threshold.

### Next step
Tighten the detector by requiring both a larger price move and confirmed executed volume persistence before emitting, rather than relying on score alone.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-894** `rejected` — Increase spike_min_price_move from 0.03 to 0.05 for low-liquidity macro contracts.
  - **Governor rejection**: TB-001 / TB-002 violated: the proposed tweak sets score_threshold to None, which conflicts with the historical global floor requiring an explicit/non-None score_threshold ≥ 2.2 and the rule rejecting None score/volume gates. It also weakens the score gate by removing it entirely, which is disallowed because the score gate must remain active as a secondary brake.
- [ ] **TB-895** `rejected` — Require executed volume confirmation by raising spike_min_volume_delta to about 15000.
  - **Governor rejection**: TB-001 / TB-002 violated: the proposed tweak sets score_threshold to None, which conflicts with the historical global floor requiring an explicit/non-None score_threshold ≥ 2.2 and the rule rejecting None score/volume gates. It also weakens the score gate by removing it entirely, which is disallowed because the score gate must remain active as a secondary brake.
- [ ] **TB-896** `rejected` — Keep spike_score_threshold unchanged unless you cannot add trade-confirmation logic; the main issue is quote-only false positives, not weak combined score.
  - **Governor rejection**: TB-001 / TB-002 violated: the proposed tweak sets score_threshold to None, which conflicts with the historical global floor requiring an explicit/non-None score_threshold ≥ 2.2 and the rule rejecting None score/volume gates. It also weakens the score gate by removing it entirely, which is disallowed because the score gate must remain active as a secondary brake.

---

## 2026-06-07 — Advisor snapshot 298

### Summary
The false positives cluster around low-liquidity macro markets where quote-only or thin-volume moves are being labeled as spikes despite weak confirmation. The analyst notes consistently ask for stronger confirmation from executed trades, sustained price impact, or multi-tick persistence.

### Next step
Keep the core detector more selective by adding a higher price-move floor for low-liquidity macro contracts, and require either confirmed executed volume or persistence across multiple ticks before emitting.

### Suggested thresholds
`min_price_move` → `0.05`

### Recommendations

- [ ] **TB-897** `rejected` — Raise spike_min_price_move from 0.03 to 0.05 for thin Fed/CPI-style markets.
  - **Governor rejection**: Yes. The proposed tweak violates the active hard-floor rule that `min_volume_delta` must be explicit and never `None`, and it also violates the active hard-floor rule that `score_threshold` must be explicit and never `None` with a live secondary brake of at least 2.2. In addition, the proposal is incomplete relative to the historical requirement for an explicit real volume gate and a non-`None` score brake, even though it keeps `min_price_move` at the required 0.05.
- [ ] **TB-898** `rejected` — Add a rule that quote-only moves must be sustained across multiple ticks or accompanied by executed trades before signaling.
  - **Governor rejection**: Yes. The proposed tweak violates the active hard-floor rule that `min_volume_delta` must be explicit and never `None`, and it also violates the active hard-floor rule that `score_threshold` must be explicit and never `None` with a live secondary brake of at least 2.2. In addition, the proposal is incomplete relative to the historical requirement for an explicit real volume gate and a non-`None` score brake, even though it keeps `min_price_move` at the required 0.05.
- [ ] **TB-899** `rejected` — Increase spike_score_threshold modestly to suppress borderline alerts while preserving larger, trade-backed moves.
  - **Governor rejection**: Yes. The proposed tweak violates the active hard-floor rule that `min_volume_delta` must be explicit and never `None`, and it also violates the active hard-floor rule that `score_threshold` must be explicit and never `None` with a live secondary brake of at least 2.2. In addition, the proposal is incomplete relative to the historical requirement for an explicit real volume gate and a non-`None` score brake, even though it keeps `min_price_move` at the required 0.05.

---

## 2026-06-07 — Advisor snapshot 299

### Summary
The false positives are concentrated in low-liquidity macro contracts where quote-only moves and short-dated rate/CPI chatter are being flagged despite weak execution evidence. Analyst labels consistently recommend tightening the detector around executed volume and sustained price impact rather than raw quote movement.

### Next step
Require both a higher volume delta and a slightly larger price move before emitting spikes in thin macro markets, with executed trade volume treated as mandatory for low-liquidity rate/CPI contracts.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-900** `rejected` — Raise the volume gate so quote-only updates no longer trigger spikes in short-dated Fed/CPI markets.
  - **Governor rejection**: TB-score_threshold floor is violated: the proposed tweak sets score_threshold to None, but the historical constraint explicitly requires a non-None score gate and keeps it ≥ 2.2. This is a regression because it removes a required explicit brake rather than tightening noise suppression.
- [ ] **TB-901** `rejected` — Increase the minimum price-move requirement modestly to filter out small transient quote jumps.
  - **Governor rejection**: TB-score_threshold floor is violated: the proposed tweak sets score_threshold to None, but the historical constraint explicitly requires a non-None score gate and keeps it ≥ 2.2. This is a regression because it removes a required explicit brake rather than tightening noise suppression.
- [ ] **TB-902** `rejected` — Add a rule that at least some executed trade volume must be present for emission in low-liquidity macro contracts.
  - **Governor rejection**: TB-score_threshold floor is violated: the proposed tweak sets score_threshold to None, but the historical constraint explicitly requires a non-None score gate and keeps it ≥ 2.2. This is a regression because it removes a required explicit brake rather than tightening noise suppression.

---

## 2026-06-07 — Advisor snapshot 300

### Summary
The false positives are concentrated in low-liquidity, thinly traded markets where quote-only or price-only moves are triggering spikes without enough executed volume or sustained confirmation. Recent analyst labels repeatedly ask for stronger volume confirmation and, in some cases, a concurrent price move before emission.

### Next step
Require both a larger volume delta and a non-trivial price move before signaling in thin markets; the cleanest single change is to raise the price-move floor while pairing it with a volume-confirmation rule.

### Suggested thresholds
`min_volume_delta` → `30000.0`, `min_price_move` → `0.05`

### Recommendations

- [ ] **TB-903** `rejected` — Increase spike_min_price_move from 0.03 to 0.05 to suppress quote-only jumps in thin macro and Fed contracts.
  - **Governor rejection**: TB-001 / Global floors and TB-009 / Score remains a brake are violated because the proposal sets `score_threshold: None`, which removes the required active score floor. The other suggested values (`min_price_move: 0.05`, `min_volume_delta: 30000.0`) are compatible with the historical constraints, but `score_threshold` cannot be nulled.
- [ ] **TB-904** `rejected` — Raise spike_min_volume_delta from 20000 to 30000 for low-liquidity markets so incidental quote activity does not trigger signals.
  - **Governor rejection**: TB-001 / Global floors and TB-009 / Score remains a brake are violated because the proposal sets `score_threshold: None`, which removes the required active score floor. The other suggested values (`min_price_move: 0.05`, `min_volume_delta: 30000.0`) are compatible with the historical constraints, but `score_threshold` cannot be nulled.
- [ ] **TB-905** `rejected` — Add a hard filter: only emit when executed trade volume is present, or when price move exceeds threshold for at least two consecutive observations.
  - **Governor rejection**: TB-001 / Global floors and TB-009 / Score remains a brake are violated because the proposal sets `score_threshold: None`, which removes the required active score floor. The other suggested values (`min_price_move: 0.05`, `min_volume_delta: 30000.0`) are compatible with the historical constraints, but `score_threshold` cannot be nulled.

---

## 2026-06-07 — Advisor snapshot 301

### Summary
The false positives are dominated by thin, low-priced, or quote-driven markets where large volume changes or isolated price jumps are not confirmed by sustained execution. The repeated analyst guidance is to require both stronger price confirmation and real traded volume before emitting a spike.

### Next step
Add a hard confirmation rule: only emit when volume delta is materially higher and there is at least a modest price move, with a higher bar for thin/short-dated markets.

### Suggested thresholds
`min_volume_delta` → `25000.0`, `min_price_move` → `0.03`, `score_threshold` → `7.5`

### Recommendations

- [ ] **TB-906** `rejected` — Raise the volume gate for low-liquidity names to cut quote-only spikes, especially in thin macro and Fed markets.
  - **Governor rejection**: Violates the historical hard floor constraint by relaxing `min_price_move` from the explicitly required minimum of 0.05 to 0.03. This conflicts with the tightened price-confirmation rule for thin/low-liquidity/watch/notable/macro-style markets, where the floor must not be reduced below 0.05. The proposal also sets `min_volume_delta` explicitly, so the specific conflict is the price floor relaxation.
- [ ] **TB-907** `rejected` — Require a non-zero concurrent price move for any volume-based spike, so pure volume surges without price confirmation do not fire.
  - **Governor rejection**: Violates the historical hard floor constraint by relaxing `min_price_move` from the explicitly required minimum of 0.05 to 0.03. This conflicts with the tightened price-confirmation rule for thin/low-liquidity/watch/notable/macro-style markets, where the floor must not be reduced below 0.05. The proposal also sets `min_volume_delta` explicitly, so the specific conflict is the price floor relaxation.
- [ ] **TB-908** `rejected` — Add a trade-quality filter that checks for executed volume or sustained price impact before signaling.
  - **Governor rejection**: Violates the historical hard floor constraint by relaxing `min_price_move` from the explicitly required minimum of 0.05 to 0.03. This conflicts with the tightened price-confirmation rule for thin/low-liquidity/watch/notable/macro-style markets, where the floor must not be reduced below 0.05. The proposal also sets `min_volume_delta` explicitly, so the specific conflict is the price floor relaxation.

---

## 2026-06-07 — Advisor snapshot 302

### Summary
The false positives cluster in thin, low-priced markets where volume spikes and quote-only moves are being flagged without enough executed-trade confirmation or sustained price impact. The repeated analyst labels indicate the detector is too sensitive to raw volume deltas in low-liquidity macro and event markets.

### Next step
Raise the volume trigger and add a confirmation rule that requires executed trades or sustained price movement before emitting a spike.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-909** `rejected` — Increase minimum volume delta to filter thin-market noise, especially for low-priced CPI/Fed contracts.
  - **Governor rejection**: TB-001 is violated: the proposed `min_price_move: 0.03` relaxes the active price floor, which must remain `>= 0.05` and explicit/non-None. TB-003 is also violated: `score_threshold: None` removes the active score gate, but the score threshold must stay explicit/non-None and `>= 2.2` as a live secondary brake. The added confirmation rule is compatible, but these relaxations conflict with the historical constraints.
- [ ] **TB-910** `rejected` — Require a concurrent price move of at least 3% before flagging quote-driven bursts in thin markets.
  - **Governor rejection**: TB-001 is violated: the proposed `min_price_move: 0.03` relaxes the active price floor, which must remain `>= 0.05` and explicit/non-None. TB-003 is also violated: `score_threshold: None` removes the active score gate, but the score threshold must stay explicit/non-None and `>= 2.2` as a live secondary brake. The added confirmation rule is compatible, but these relaxations conflict with the historical constraints.
- [ ] **TB-911** `rejected` — Add an execution-confirmation rule: only emit if there is traded volume or persistent order-book imbalance, not quote updates alone.
  - **Governor rejection**: TB-001 is violated: the proposed `min_price_move: 0.03` relaxes the active price floor, which must remain `>= 0.05` and explicit/non-None. TB-003 is also violated: `score_threshold: None` removes the active score gate, but the score threshold must stay explicit/non-None and `>= 2.2` as a live secondary brake. The added confirmation rule is compatible, but these relaxations conflict with the historical constraints.

---

## 2026-06-07 — Advisor snapshot 303

### Summary
The false positives are concentrated in thin, low-priced markets where volume jumps are not accompanied by meaningful price movement or confirmed executed-trade imbalance. Several labeled examples explicitly call for stricter confirmation on volume-only or quote-driven spikes.

### Next step
Tighten the detector with a higher volume threshold and a minimum price-move confirmation, while also requiring executed-trade volume or sustained order-book imbalance before emitting a spike.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.03`, `score_threshold` → `6.5`

### Recommendations

- [ ] **TB-912** `rejected` — Raise the volume trigger for thin macro and event markets so raw volume surges alone do not emit signals.
  - **Governor rejection**: The proposed tweak violates the active floor by setting min_price_move to 0.03, which relaxes a globally required min_price_move ≥ 0.05. This conflicts with the historical constraint that explicitly rejects 0.03–0.04 for thin, low-liquidity, watch, notable, NBA series/playoff, CPI/Fed, and quote-driven markets. It also weakens the live secondary brake because score_threshold is being raised to 6.5, but the conflict is specifically the price-floor relaxation.
- [ ] **TB-913** `rejected` — Require a non-trivial price move alongside volume, especially for low-priced contracts where quote updates can mimic spikes.
  - **Governor rejection**: The proposed tweak violates the active floor by setting min_price_move to 0.03, which relaxes a globally required min_price_move ≥ 0.05. This conflicts with the historical constraint that explicitly rejects 0.03–0.04 for thin, low-liquidity, watch, notable, NBA series/playoff, CPI/Fed, and quote-driven markets. It also weakens the live secondary brake because score_threshold is being raised to 6.5, but the conflict is specifically the price-floor relaxation.
- [ ] **TB-914** `rejected` — Add a confirmation gate for executed trades or sustained order-book imbalance before scoring a signal as actionable.
  - **Governor rejection**: The proposed tweak violates the active floor by setting min_price_move to 0.03, which relaxes a globally required min_price_move ≥ 0.05. This conflicts with the historical constraint that explicitly rejects 0.03–0.04 for thin, low-liquidity, watch, notable, NBA series/playoff, CPI/Fed, and quote-driven markets. It also weakens the live secondary brake because score_threshold is being raised to 6.5, but the conflict is specifically the price-floor relaxation.

---

## 2026-06-07 — Advisor snapshot 304

### Summary
The false positives are concentrated in thin, low-priced markets where large volume deltas occur without a meaningful price move. The analyst labels consistently ask for stronger confirmation from executed trades or sustained imbalance before emitting a spike.

### Next step
Raise the volume threshold modestly and require a non-trivial price move for low-priced markets, or equivalently gate signals on confirmed trade imbalance so volume-only bursts do not fire.

### Suggested thresholds
`min_volume_delta` → `10000.0`, `min_price_move` → `0.03`

### Recommendations

- [ ] **TB-915** `rejected` — Increase the minimum volume delta to reduce thin-market chatter.
  - **Governor rejection**: The proposed tweak violates the historical hard floor TB-001/TB-004 style constraint that low-liquidity/watch/low-priced markets must keep min_price_move >= 0.05 as the default hard confirmation bar. Setting min_price_move to 0.03 is a relaxation into the explicitly rejected 0.03–0.04 range. It also conflicts with the active-floor rule requiring score_threshold to remain non-None and >= 2.2, because score_threshold is set to None.
- [ ] **TB-916** `rejected` — Set a minimum price move so volume spikes without price confirmation are suppressed.
  - **Governor rejection**: The proposed tweak violates the historical hard floor TB-001/TB-004 style constraint that low-liquidity/watch/low-priced markets must keep min_price_move >= 0.05 as the default hard confirmation bar. Setting min_price_move to 0.03 is a relaxation into the explicitly rejected 0.03–0.04 range. It also conflicts with the active-floor rule requiring score_threshold to remain non-None and >= 2.2, because score_threshold is set to None.
- [ ] **TB-917** `rejected` — Add a confirmation rule: only emit when volume spike is paired with executed-trade persistence or sustained order-book imbalance.
  - **Governor rejection**: The proposed tweak violates the historical hard floor TB-001/TB-004 style constraint that low-liquidity/watch/low-priced markets must keep min_price_move >= 0.05 as the default hard confirmation bar. Setting min_price_move to 0.03 is a relaxation into the explicitly rejected 0.03–0.04 range. It also conflicts with the active-floor rule requiring score_threshold to remain non-None and >= 2.2, because score_threshold is set to None.

---

## 2026-06-07 — Advisor snapshot 305

### Summary
The false positives are concentrated in thin or low-priced markets where volume churn can look like a spike even when price barely moves. Analyst notes consistently ask for stronger confirmation from executed trades, sustained imbalance, or a larger price move before emitting.

### Next step
Tighten the detector by requiring a higher combined volume-and-price confirmation for thin markets, rather than relying on volume delta alone.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.03`, `score_threshold` → `3.5`

### Recommendations

- [ ] **TB-918** `rejected` — Raise the minimum price move to at least 0.03 so low-information 1-2% oscillations do not emit.
  - **Governor rejection**: TB-001 violated: the proposed `min_price_move: 0.03` relaxes the active hard floor `min_price_move ≥ 0.05` globally, including thin/low-liquidity and quote-driven markets where a stricter floor must be kept. TB-002 is not violated because `min_volume_delta` remains explicit and non-null, and TB-003 is not violated because `score_threshold: 3.5` is above the required global minimum of 2.2.
- [ ] **TB-919** `rejected` — Raise the minimum volume delta to about 20000 for thin markets with weak price follow-through.
  - **Governor rejection**: TB-001 violated: the proposed `min_price_move: 0.03` relaxes the active hard floor `min_price_move ≥ 0.05` globally, including thin/low-liquidity and quote-driven markets where a stricter floor must be kept. TB-002 is not violated because `min_volume_delta` remains explicit and non-null, and TB-003 is not violated because `score_threshold: 3.5` is above the required global minimum of 2.2.
- [ ] **TB-920** `rejected` — Increase the score threshold modestly so only spikes with both meaningful volume and price confirmation pass.
  - **Governor rejection**: TB-001 violated: the proposed `min_price_move: 0.03` relaxes the active hard floor `min_price_move ≥ 0.05` globally, including thin/low-liquidity and quote-driven markets where a stricter floor must be kept. TB-002 is not violated because `min_volume_delta` remains explicit and non-null, and TB-003 is not violated because `score_threshold: 3.5` is above the required global minimum of 2.2.

---

## 2026-06-07 — Advisor snapshot 306

### Summary
The recent false positives cluster in thin or low-priced markets where modest price moves and raw volume deltas still trigger alerts. Analyst notes point to quote churn and low-information oscillation, implying the detector needs stricter confirmation on execution quality or a larger move to qualify as a spike.

### Next step
Raise the minimum price-move and volume requirements together, and add a confirmation rule that prefers executed trades or sustained order-book imbalance over raw volume alone.

### Suggested thresholds
`min_volume_delta` → `15000.0`, `min_price_move` → `0.04`

### Recommendations

- [ ] **TB-921** `rejected` — Increase spike_min_price_move from 0.03 to 0.04 for thin/watch markets.
  - **Governor rejection**: TB-001 / TB-002 violated: the proposed tweak relaxes the explicit core floor for thin/low-liquidity and notable markets by setting min_price_move to 0.04, but the historical constraints require min_price_move ≥ 0.05 for NBA series/playoff winner/low-liquidity high-odds/watch/notable markets and say to enforce stronger confirmation rather than looser 0.03–0.04 thresholds. TB-003 also requires score_threshold to remain explicit and non-None, but the proposal sets score_threshold to None, which conflicts with the no-relaxation-to-None rule for core gates and the global requirement score_threshold ≥ 2.2 explicit/non-None.
- [ ] **TB-922** `rejected` — Increase spike_min_volume_delta from 12702.36 to 15000.0 as a first-pass filter for low-information flow.
  - **Governor rejection**: TB-001 / TB-002 violated: the proposed tweak relaxes the explicit core floor for thin/low-liquidity and notable markets by setting min_price_move to 0.04, but the historical constraints require min_price_move ≥ 0.05 for NBA series/playoff winner/low-liquidity high-odds/watch/notable markets and say to enforce stronger confirmation rather than looser 0.03–0.04 thresholds. TB-003 also requires score_threshold to remain explicit and non-None, but the proposal sets score_threshold to None, which conflicts with the no-relaxation-to-None rule for core gates and the global requirement score_threshold ≥ 2.2 explicit/non-None.
- [ ] **TB-923** `rejected` — Keep spike_score_threshold near 2.625 for now, but only emit when the score is accompanied by confirmed trades or persistence over multiple updates.
  - **Governor rejection**: TB-001 / TB-002 violated: the proposed tweak relaxes the explicit core floor for thin/low-liquidity and notable markets by setting min_price_move to 0.04, but the historical constraints require min_price_move ≥ 0.05 for NBA series/playoff winner/low-liquidity high-odds/watch/notable markets and say to enforce stronger confirmation rather than looser 0.03–0.04 thresholds. TB-003 also requires score_threshold to remain explicit and non-None, but the proposal sets score_threshold to None, which conflicts with the no-relaxation-to-None rule for core gates and the global requirement score_threshold ≥ 2.2 explicit/non-None.

---

## 2026-06-07 — Advisor snapshot 307

### Summary
The false positives are concentrated in low-liquidity, quote-only market spikes where a small price move and large apparent volume delta still produce a signal. Analyst labels indicate these are mostly noise from churn rather than informative flow.

### Next step
Add a market-type guard: require either nonzero trade prints or a stronger continuation condition before emitting a spike in low-liquidity quote-driven markets, and otherwise raise the combined score cutoff slightly.

### Suggested thresholds
`score_threshold` → `3.0`

### Recommendations

- [ ] **TB-924** `rejected` — For low-liquidity quote-only markets, require confirmed trade volume > 0 before the spike can emit.
  - **Governor rejection**: Yes. The proposed tweak violates the historical floor rules by setting `min_volume_delta` to `None` and `min_price_move` to `None`, which conflicts with the explicit TB-Volume Floor and TB-Price Floor constraints requiring both to be explicit; `min_price_move` must be ≥ 0.05 and `min_volume_delta` must be non-`None`. It also conflicts with the TB-Score Floor because `score_threshold` is raised to 3.0, which is not a conflict by itself, but the proposal still removes two previously tightened gates rather than hardening them for low-liquidity/quote-driven spikes.
- [ ] **TB-925** `rejected` — If trade prints are unavailable, require at least 2 consecutive ticks of same-direction price continuation in addition to the current move threshold.
  - **Governor rejection**: Yes. The proposed tweak violates the historical floor rules by setting `min_volume_delta` to `None` and `min_price_move` to `None`, which conflicts with the explicit TB-Volume Floor and TB-Price Floor constraints requiring both to be explicit; `min_price_move` must be ≥ 0.05 and `min_volume_delta` must be non-`None`. It also conflicts with the TB-Score Floor because `score_threshold` is raised to 3.0, which is not a conflict by itself, but the proposal still removes two previously tightened gates rather than hardening them for low-liquidity/quote-driven spikes.
- [ ] **TB-926** `rejected` — Increase spike_score_threshold modestly for this market class to suppress borderline watch-level churn.
  - **Governor rejection**: Yes. The proposed tweak violates the historical floor rules by setting `min_volume_delta` to `None` and `min_price_move` to `None`, which conflicts with the explicit TB-Volume Floor and TB-Price Floor constraints requiring both to be explicit; `min_price_move` must be ≥ 0.05 and `min_volume_delta` must be non-`None`. It also conflicts with the TB-Score Floor because `score_threshold` is raised to 3.0, which is not a conflict by itself, but the proposal still removes two previously tightened gates rather than hardening them for low-liquidity/quote-driven spikes.

---

## 2026-06-07 — Advisor snapshot 308

### Summary
The false positives are mostly low-information quote-driven or low-liquidity spikes where price moves are only around 2–3% but volume is elevated, so the detector is firing before there is enough confirmation. Analyst notes consistently ask for either stronger price continuation, confirmed trades, or a higher volume multiple before emitting a signal.

### Next step
Tighten the detector to require stronger confirmation in quote-driven or low-liquidity markets: raise the price-move floor and add a higher volume-multiple gate before a spike can pass the score threshold.

### Suggested thresholds
`min_price_move` → `0.04`

### Recommendations

- [ ] **TB-927** `rejected` — Increase the minimum price move from 0.03 to 0.04 for actionable alerts in political/quote-driven markets.
  - **Governor rejection**: TB-001 and TB-003 are violated: the proposed `min_price_move` of 0.04 relaxes the explicitly tightened active price floor from ≥ 0.05 into the rejected 0.03–0.04 range, and `min_volume_delta: None` / `score_threshold: None` null core gates that historical constraints require to remain explicit and non-null. The tweak also conflicts with the low-liquidity guidance by weakening confirmation instead of adding executed-trade, trade-count, or persistence corroboration.
- [ ] **TB-928** `rejected` — Require at least ~3x baseline traded volume, or explicit nonzero trade prints, instead of relying on quote-only movement.
  - **Governor rejection**: TB-001 and TB-003 are violated: the proposed `min_price_move` of 0.04 relaxes the explicitly tightened active price floor from ≥ 0.05 into the rejected 0.03–0.04 range, and `min_volume_delta: None` / `score_threshold: None` null core gates that historical constraints require to remain explicit and non-null. The tweak also conflicts with the low-liquidity guidance by weakening confirmation instead of adding executed-trade, trade-count, or persistence corroboration.
- [ ] **TB-929** `rejected` — Keep the score threshold unchanged for now and use the higher price/volume confirmation as the main false-positive filter.
  - **Governor rejection**: TB-001 and TB-003 are violated: the proposed `min_price_move` of 0.04 relaxes the explicitly tightened active price floor from ≥ 0.05 into the rejected 0.03–0.04 range, and `min_volume_delta: None` / `score_threshold: None` null core gates that historical constraints require to remain explicit and non-null. The tweak also conflicts with the low-liquidity guidance by weakening confirmation instead of adding executed-trade, trade-count, or persistence corroboration.

---

## 2026-06-07 — Advisor snapshot 309

### Summary
The false positives are concentrated in quote-driven or low-liquidity spikes where price moves are modest and volume confirmation is weak or absent. The analyst labels suggest these are being over-emitted as actionable signals despite lacking sustained trade participation.

### Next step
Tighten the detector with a stronger volume-confirmation gate and a slightly higher price-move floor, while keeping the overall score threshold secondary.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `3.0`

### Recommendations

- [ ] **TB-930** `rejected` — Require nonzero executed trade volume before emitting a signal in low-liquidity/quote-only markets.
  - **Governor rejection**: TB-001 is violated because `min_price_move` is lowered to 0.04, which conflicts with the historical floor of `min_price_move >= 0.05` and the explicit rejection of 0.03–0.04. TB-002 is also violated because `min_volume_delta` is set to `None`, but the historical constraint requires an explicit/non-`None` volume gate.
- [ ] **TB-931** `rejected` — Raise the price-move floor from 0.03 to 0.04 for actionable spike signals.
  - **Governor rejection**: TB-001 is violated because `min_price_move` is lowered to 0.04, which conflicts with the historical floor of `min_price_move >= 0.05` and the explicit rejection of 0.03–0.04. TB-002 is also violated because `min_volume_delta` is set to `None`, but the historical constraint requires an explicit/non-`None` volume gate.
- [ ] **TB-932** `rejected` — Add a relative volume check for political markets: only flag when traded volume is >3x baseline or the score clears a higher bar.
  - **Governor rejection**: TB-001 is violated because `min_price_move` is lowered to 0.04, which conflicts with the historical floor of `min_price_move >= 0.05` and the explicit rejection of 0.03–0.04. TB-002 is also violated because `min_volume_delta` is set to `None`, but the historical constraint requires an explicit/non-`None` volume gate.

---

## 2026-06-07 — Advisor snapshot 310

### Summary
The false positives are concentrated in low-liquidity, quote-driven spikes where price moves are small and execution quality is weak or absent. The analyst labels consistently ask for stronger confirmation from traded volume and/or a larger price move before emitting a signal.

### Next step
Tighten the detector by requiring both a higher price move floor and confirmed executed volume for low-liquidity markets, rather than relying on score alone.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `3.0`

### Recommendations

- [ ] **TB-933** `rejected` — Raise the minimum price move to 0.04 to suppress quote-only oscillations while preserving larger genuine spikes.
  - **Governor rejection**: Violates the historical hard floor on price move: TB-001/TB-004 require min_price_move ≥ 0.05, but the proposed tweak lowers it to 0.04. It also conflicts with the low-liquidity/watch-tier constraint (TB-002/TB-005/TB-007) that explicitly forbids relaxing into 0.03–0.04 for those markets. Additionally, TB-001/TB-008 require min_volume_delta to remain explicit/non-None, so setting min_volume_delta to None is also a direct conflict.
- [ ] **TB-934** `rejected` — Require nonzero confirmed traded volume before emitting a signal in markets with repeated quote updates and zero prints.
  - **Governor rejection**: Violates the historical hard floor on price move: TB-001/TB-004 require min_price_move ≥ 0.05, but the proposed tweak lowers it to 0.04. It also conflicts with the low-liquidity/watch-tier constraint (TB-002/TB-005/TB-007) that explicitly forbids relaxing into 0.03–0.04 for those markets. Additionally, TB-001/TB-008 require min_volume_delta to remain explicit/non-None, so setting min_volume_delta to None is also a direct conflict.
- [ ] **TB-935** `rejected` — Increase the score threshold modestly to reduce marginal watch-tier emissions that are being labeled uncertain/noise.
  - **Governor rejection**: Violates the historical hard floor on price move: TB-001/TB-004 require min_price_move ≥ 0.05, but the proposed tweak lowers it to 0.04. It also conflicts with the low-liquidity/watch-tier constraint (TB-002/TB-005/TB-007) that explicitly forbids relaxing into 0.03–0.04 for those markets. Additionally, TB-001/TB-008 require min_volume_delta to remain explicit/non-None, so setting min_volume_delta to None is also a direct conflict.

---

## 2026-06-07 — Advisor snapshot 311

### Summary
The false positives are concentrated in quote-driven or low-liquidity events where volume or score can be high without meaningful executed price continuation. Analyst labels repeatedly recommend requiring both confirmed traded volume and a larger price move before treating these as actionable.

### Next step
Tighten the detector with a higher price-move gate and an execution-confirmation requirement for low-liquidity markets: do not emit on quote-only oscillation unless executed volume is present and price has moved at least 4%.

### Suggested thresholds
`min_price_move` → `0.04`

### Recommendations

- [ ] **TB-936** `rejected` — Raise spike_min_price_move to 0.04 to filter quote-driven oscillation that is not translating into sustained price movement.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets `min_price_move` to 0.04, but the historical floor for active tuning is explicit and non-`None` at `min_price_move >= 0.05`. It also conflicts with the low-liquidity/watch constraint, which specifically forbids relaxing into 0.03–0.04 thresholds and requires explicit volume confirmation rather than `min_volume_delta: None`. In addition, TB-001 requires `score_threshold` to remain explicit and non-`None` and `>= 2.2`, so setting `score_threshold: None` is also a violation.
- [ ] **TB-937** `rejected` — Add a hard rule that zero-trade or quote-only events must have nonzero executed volume before signaling.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets `min_price_move` to 0.04, but the historical floor for active tuning is explicit and non-`None` at `min_price_move >= 0.05`. It also conflicts with the low-liquidity/watch constraint, which specifically forbids relaxing into 0.03–0.04 thresholds and requires explicit volume confirmation rather than `min_volume_delta: None`. In addition, TB-001 requires `score_threshold` to remain explicit and non-`None` and `>= 2.2`, so setting `score_threshold: None` is also a violation.
- [ ] **TB-938** `rejected` — For low-liquidity markets, require either sustained multi-tick continuation or a higher score_threshold before emitting.
  - **Governor rejection**: TB-001 is violated because the proposed tweak sets `min_price_move` to 0.04, but the historical floor for active tuning is explicit and non-`None` at `min_price_move >= 0.05`. It also conflicts with the low-liquidity/watch constraint, which specifically forbids relaxing into 0.03–0.04 thresholds and requires explicit volume confirmation rather than `min_volume_delta: None`. In addition, TB-001 requires `score_threshold` to remain explicit and non-`None` and `>= 2.2`, so setting `score_threshold: None` is also a violation.

---

## 2026-06-07 — Advisor snapshot 312

### Summary
Recent false positives are dominated by quote-driven or zero-print spikes with meaningful-looking scores but weak or absent executed-volume confirmation. The analyst labels consistently favor tightening price/volume confirmation rather than raising the score threshold alone.

### Next step
Require nonzero executed volume confirmation and a larger price move for low-liquidity/quote-only markets before emitting a spike signal.

### Suggested thresholds
`min_price_move` → `0.04`

### Recommendations

- [ ] **TB-939** `rejected` — Raise spike_min_price_move to 0.04 to filter small quote-only moves that are being labeled unclear/noise.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it relaxes `min_volume_delta` to `None`, violating the global floor that `min_volume_delta` must be explicit/non-`None` and the no-relaxation rule against setting it to `None`. It also relaxes `score_threshold` to `None`, violating the global floor that `score_threshold ≥ 2.2` and explicit/non-`None`. Finally, setting `min_price_move` to `0.04` conflicts with the global floor `min_price_move ≥ 0.05`.
- [ ] **TB-940** `rejected` — Add a hard executed-volume floor: do not trigger on zero-trade prints, even if score is high.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it relaxes `min_volume_delta` to `None`, violating the global floor that `min_volume_delta` must be explicit/non-`None` and the no-relaxation rule against setting it to `None`. It also relaxes `score_threshold` to `None`, violating the global floor that `score_threshold ≥ 2.2` and explicit/non-`None`. Finally, setting `min_price_move` to `0.04` conflicts with the global floor `min_price_move ≥ 0.05`.
- [ ] **TB-941** `rejected` — Keep score_threshold unchanged for now; the false positives are better explained by poor price/volume confirmation than by low combined score.
  - **Governor rejection**: The proposed tweak conflicts with the historical constraints because it relaxes `min_volume_delta` to `None`, violating the global floor that `min_volume_delta` must be explicit/non-`None` and the no-relaxation rule against setting it to `None`. It also relaxes `score_threshold` to `None`, violating the global floor that `score_threshold ≥ 2.2` and explicit/non-`None`. Finally, setting `min_price_move` to `0.04` conflicts with the global floor `min_price_move ≥ 0.05`.

---

## 2026-06-07 — Advisor snapshot 313

### Summary
The false positives are concentrated in quote-driven or execution-light spikes: two high-scoring alerts had zero price move but large volume deltas, while the analyst-labeled uncertain cases specifically call out quote-only oscillation and political-market quote spikes. The detector is likely over-triggering on volume/score without enough confirmation from actual price movement and executed volume.

### Next step
Require a larger price move plus confirmed executed volume before emitting, rather than relying on volume delta alone.

### Suggested thresholds
`min_price_move` → `0.04`, `score_threshold` → `4.0`

### Recommendations

- [ ] **TB-942** `rejected` — Raise spike_min_price_move to 0.04 to suppress quote-only and low-move noise.
  - **Governor rejection**: TB-GLOBAL-02 and TB-GLOBAL-03 are violated because the proposed tweak sets min_volume_delta to None, which is a forbidden null relaxation, and it also keeps min_price_move below the historical hard floor by lowering it to 0.04 instead of maintaining min_price_move ≥ 0.05. In addition, the tweak weakens confirmation by relying on score_threshold 4.0 while removing the required explicit volume floor, which conflicts with the confirmation hierarchy and the explicit/non-None volume requirement.
- [ ] **TB-943** `rejected` — Add an execution-confirmation rule: do not emit unless traded volume is clearly present, not just quote activity.
  - **Governor rejection**: TB-GLOBAL-02 and TB-GLOBAL-03 are violated because the proposed tweak sets min_volume_delta to None, which is a forbidden null relaxation, and it also keeps min_price_move below the historical hard floor by lowering it to 0.04 instead of maintaining min_price_move ≥ 0.05. In addition, the tweak weakens confirmation by relying on score_threshold 4.0 while removing the required explicit volume floor, which conflicts with the confirmation hierarchy and the explicit/non-None volume requirement.
- [ ] **TB-944** `rejected` — Increase spike_score_threshold modestly so borderline quote-driven events do not pass when priceΔ is small.
  - **Governor rejection**: TB-GLOBAL-02 and TB-GLOBAL-03 are violated because the proposed tweak sets min_volume_delta to None, which is a forbidden null relaxation, and it also keeps min_price_move below the historical hard floor by lowering it to 0.04 instead of maintaining min_price_move ≥ 0.05. In addition, the tweak weakens confirmation by relying on score_threshold 4.0 while removing the required explicit volume floor, which conflicts with the confirmation hierarchy and the explicit/non-None volume requirement.

---

## 2026-06-08 — Advisor snapshot 314

### Summary
Volume spikes alone are triggering false positives, especially in thin/low-conviction markets where quote volume doesn't reflect genuine conviction. Price movement is being decoupled from volume signals.

### Next step
Enforce minimum price-move requirements that scale with market type: require 2-3% price moves to accompany volume spikes in low-conviction/thin markets, and distinguish trade volume from quote volume.

### Suggested thresholds
`min_price_move` → `0.03`

### Recommendations

- [ ] **TB-945** `rejected` — Increase spike_min_price_move to 0.03 (3%) for watch-tier alerts when volume_delta exceeds threshold but market conviction (yes probability) is below 0.65
  - **Governor rejection**: VIOLATION of multiple Active Tuning Constraints: (1) min_price_move=0.03 violates 'Price-move floor' constraint requiring spike_min_price_move ≥ 0.05 (5%) globally with explicit rejection of 0.03–0.04 range. (2) min_volume_delta=None violates 'Volume-delta floor' constraint requiring spike_min_volume_delta be explicit and non-None; 'Prohibited relaxations' explicitly forbids min_volume_delta=None. (3) score_threshold=None violates 'Score threshold floor' constraint requiring spike_score_threshold ≥ 2.2 globally and remain explicit and non-None; 'Prohibited relaxations' explicitly forbids score_threshold=None. The proposed tweak systematically relaxes three critical parameters that were previously tightened to suppress noise and false positives.
- [ ] **TB-946** `rejected` — Add a trade-volume validation gate: require minimum executed trade volume (not just quote volume) to trigger alerts in binary political and low-liquidity markets
  - **Governor rejection**: VIOLATION of multiple Active Tuning Constraints: (1) min_price_move=0.03 violates 'Price-move floor' constraint requiring spike_min_price_move ≥ 0.05 (5%) globally with explicit rejection of 0.03–0.04 range. (2) min_volume_delta=None violates 'Volume-delta floor' constraint requiring spike_min_volume_delta be explicit and non-None; 'Prohibited relaxations' explicitly forbids min_volume_delta=None. (3) score_threshold=None violates 'Score threshold floor' constraint requiring spike_score_threshold ≥ 2.2 globally and remain explicit and non-None; 'Prohibited relaxations' explicitly forbids score_threshold=None. The proposed tweak systematically relaxes three critical parameters that were previously tightened to suppress noise and false positives.
- [ ] **TB-947** `rejected` — For notable-tier signals, require price_move >= 0.02 (2%) when volume_delta exceeds 3M to filter mechanical executions from genuine conviction shifts
  - **Governor rejection**: VIOLATION of multiple Active Tuning Constraints: (1) min_price_move=0.03 violates 'Price-move floor' constraint requiring spike_min_price_move ≥ 0.05 (5%) globally with explicit rejection of 0.03–0.04 range. (2) min_volume_delta=None violates 'Volume-delta floor' constraint requiring spike_min_volume_delta be explicit and non-None; 'Prohibited relaxations' explicitly forbids min_volume_delta=None. (3) score_threshold=None violates 'Score threshold floor' constraint requiring spike_score_threshold ≥ 2.2 globally and remain explicit and non-None; 'Prohibited relaxations' explicitly forbids score_threshold=None. The proposed tweak systematically relaxes three critical parameters that were previously tightened to suppress noise and false positives.

---

## 2026-06-08 — Advisor snapshot 315

### Summary
False positives are driven by mechanical/quote activity masquerading as meaningful flow: zero-price-movement volume spikes in illiquid markets, and extreme quote-to-trade ratios inflating signal scores.

### Next step
Add a volume-quality gate: reject signals where (quote_volume / trade_volume) > 10 or where price_delta == 0 in low-conviction markets.

### Suggested thresholds
`min_price_move` → `0.005`

### Recommendations

- [ ] **TB-948** `rejected` — Introduce max_quote_to_trade_ratio filter set to 10–15x; flag and suppress signals exceeding this (KXCPI case hits 60,000x).
  - **Governor rejection**: CRITICAL VIOLATIONS of three explicit global constraints: (1) min_volume_delta set to None violates 'Global Volume-Delta Floor' constraint which explicitly prohibits None values and requires explicit, non-None market-type-specific floors; (2) min_price_move=0.005 (0.5%) violates 'Global Price-Move Floor' constraint which sets floor at ≥0.05 (5%) and explicitly rejects 0.03–0.04 range—0.005 is 10x below the enforced minimum; (3) score_threshold set to None violates 'Global Score Threshold Floor' constraint which requires ≥2.2 and must remain explicit and non-None, serving as secondary brake. The proposed tweak removes three core gates that were established precisely to prevent false positives in low-liquidity regimes. The quote/trade ratio gate is a valid signal refinement but cannot replace these hard floors.
- [ ] **TB-949** `rejected` — For markets with conviction < 0.70 or long-dated expirations, require price_delta > 0 in absolute terms; zero-price spikes are mechanical order clustering.
  - **Governor rejection**: CRITICAL VIOLATIONS of three explicit global constraints: (1) min_volume_delta set to None violates 'Global Volume-Delta Floor' constraint which explicitly prohibits None values and requires explicit, non-None market-type-specific floors; (2) min_price_move=0.005 (0.5%) violates 'Global Price-Move Floor' constraint which sets floor at ≥0.05 (5%) and explicitly rejects 0.03–0.04 range—0.005 is 10x below the enforced minimum; (3) score_threshold set to None violates 'Global Score Threshold Floor' constraint which requires ≥2.2 and must remain explicit and non-None, serving as secondary brake. The proposed tweak removes three core gates that were established precisely to prevent false positives in low-liquidity regimes. The quote/trade ratio gate is a valid signal refinement but cannot replace these hard floors.
- [ ] **TB-950** `rejected` — Recalibrate spike_score calculation to weight price_delta more heavily relative to volume_delta, or apply multiplicative penalty when price_delta is near-zero.
  - **Governor rejection**: CRITICAL VIOLATIONS of three explicit global constraints: (1) min_volume_delta set to None violates 'Global Volume-Delta Floor' constraint which explicitly prohibits None values and requires explicit, non-None market-type-specific floors; (2) min_price_move=0.005 (0.5%) violates 'Global Price-Move Floor' constraint which sets floor at ≥0.05 (5%) and explicitly rejects 0.03–0.04 range—0.005 is 10x below the enforced minimum; (3) score_threshold set to None violates 'Global Score Threshold Floor' constraint which requires ≥2.2 and must remain explicit and non-None, serving as secondary brake. The proposed tweak removes three core gates that were established precisely to prevent false positives in low-liquidity regimes. The quote/trade ratio gate is a valid signal refinement but cannot replace these hard floors.

---
