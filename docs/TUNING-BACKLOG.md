
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
