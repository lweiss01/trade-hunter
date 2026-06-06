
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

- [ ] **TB-326** `planned` — Raise the minimum volume gate for low-liquidity markets to about 20,000 traded volume delta, since the 10k-20k range still produced noisy CPI and thin-market alerts while 4k+ and 11k+ were often false positives.
- [ ] **TB-327** `planned` — Increase the minimum price move floor to about 0.05 for quote-only alerts, because 0.02 moves were repeatedly labeled noise while 0.05+ began separating more informative CPI flow.
- [ ] **TB-328** `planned` — Add a persistence rule: require the move to hold across multiple timestamps or several independent trades before triggering, especially for zero-liquidity and quote-driven markets.

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

- [ ] **TB-341** `planned` — Increase spike_min_price_move from 0.03 to 0.05 to suppress flat or quote-only moves while preserving genuinely large spikes.
- [ ] **TB-342** `planned` — Increase spike_min_volume_delta to 15000 to filter thin-market noise and isolated block prints.
- [ ] **TB-343** `planned` — Require the signal to persist across multiple timestamps or traded prints before emission; if you need a numeric score gate, raise spike_score_threshold modestly to 20.0.

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

- [ ] **TB-383** `planned` — Raise min_volume_delta to about 20000 to suppress quote-only bursts below meaningful executed flow.
- [ ] **TB-384** `planned` — Raise min_price_move to about 0.08 so small one-minute oscillations do not trigger spikes.
- [ ] **TB-385** `planned` — Increase score_threshold modestly to about 10.0 to filter marginal events while keeping clearly informative flow.

---

## 2026-06-06 — Advisor snapshot 128

### Summary
The false positives are concentrated in thin macro markets where quote-driven price bursts and low executed trade activity are being mistaken for real spikes. The analyst notes consistently recommend adding confirmation from executed volume, trade count, or sustained multi-minute movement before emitting a signal.

### Next step
Add an executed-activity confirmation rule: require both a higher minimum volume delta and a larger price move for low-liquidity macro markets, rather than relying on either alone.

### Suggested thresholds
`min_volume_delta` → `20000.0`, `min_price_move` → `0.12`, `score_threshold` → `25.0`

### Recommendations

- [ ] **TB-386** `planned` — Raise min_volume_delta to 20000 for thin macro markets to filter quote-only bursts.
- [ ] **TB-387** `planned` — Raise min_price_move to 0.12 for low-price macro contracts so brief 3%-4% wiggles do not trigger signals.
- [ ] **TB-388** `planned` — Increase score_threshold modestly to suppress marginal alerts, while keeping high-conviction spikes detectable.

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

- [ ] **TB-440** `planned` — Increase spike_min_price_move to 0.05 to filter out 2–3% drift and quote noise in thin macro markets.
- [ ] **TB-441** `planned` — Increase spike_min_volume_delta to 15000 so low-priced contracts need a clearer burst above baseline before alerting.
- [ ] **TB-442** `planned` — Require at least 2 same-side executed trades above the spread within the detection window for watch/notable emits in low-liquidity markets.

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

- [ ] **TB-446** `planned` — Increase spike_min_price_move to 0.05 to suppress 3% quote-driven moves that were repeatedly labeled noise.
- [ ] **TB-447** `planned` — Increase spike_min_volume_delta to 20000.0 so one-off quote bursts around ~10k-19k do not trigger alerts by themselves.
- [ ] **TB-448** `planned` — Add a rule that a signal only emits when there is at least one confirmed executed trade or sustained multi-minute price movement; keep the score threshold unchanged for now.

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

- [ ] **TB-452** `planned` — Raise the minimum traded-volume requirement to filter out quote-only spikes in thin macro markets.
- [ ] **TB-453** `planned` — Increase the minimum price-move threshold slightly so 2% to 3% drift does not trigger unless backed by real volume.
- [ ] **TB-454** `planned` — Add a persistence rule: require sustained movement or repeated same-side prints across multiple intervals before emitting a signal.

---

## 2026-06-06 — Advisor snapshot 151

### Summary
The false positives are concentrated in thin, low-liquidity macro markets where quote-driven moves and repeated updates are being mistaken for real spikes. Analyst notes consistently ask for stronger confirmation from executed volume and sustained multi-interval price movement rather than single-interval quote bursts.

### Next step
Raise the minimum volume-delta requirement and add a confirmation rule that requires either executed trades or sustained price movement across multiple intervals before emitting a spike.

### Suggested thresholds
`min_volume_delta` → `30000.0`, `min_price_move` → `0.05`, `score_threshold` → `8.0`

### Recommendations

- [ ] **TB-455** `planned` — Increase spike_min_volume_delta to 30000 to filter out quote-only bursts in CPI/GDP-like markets.
- [ ] **TB-456** `planned` — Increase spike_min_price_move to 0.05 so sub-5% moves are not flagged unless volume confirmation is strong.
- [ ] **TB-457** `planned` — Raise spike_score_threshold modestly to 8.0 to suppress low-confidence watch-tier signals without blocking the stronger notable cases.

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

- [ ] **TB-461** `planned` — Increase spike_min_volume_delta to at least 300 for low-liquidity event markets to suppress single-print bursts.
- [ ] **TB-462** `planned` — Increase spike_min_price_move to 0.05 so sub-5% quote-only moves do not trigger alerts on their own.
- [ ] **TB-463** `planned` — Raise spike_score_threshold modestly to 45 to force stronger combined confirmation before emission.

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

- [ ] **TB-467** `planned` — Raise spike_min_volume_delta to about 30000 for low-liquidity/event-style markets.
- [ ] **TB-468** `planned` — Raise spike_min_price_move to 0.05 to require at least a 5% move before flagging borderline bursts.
- [ ] **TB-469** `planned` — Keep spike_score_threshold unchanged unless you still see quote-only alerts after the first two changes; if so, lift it slightly to suppress low-confidence emissions.

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

- [ ] **TB-482** `planned` — Increase spike_min_volume_delta to filter out quote-driven jumps with little executed flow.
- [ ] **TB-483** `planned` — Increase spike_min_price_move so small 2% moves do not trigger unless volume is exceptionally strong.
- [ ] **TB-484** `planned` — Increase spike_score_threshold modestly to suppress borderline alerts that lack sustained confirmation.

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

- [ ] **TB-488** `planned` — Increase the volume floor for CPI-style markets so quote-only jumps do not trigger on their own.
- [ ] **TB-489** `planned` — Raise the minimum price-move requirement for watch-tier spikes from ~2% to a clearly sustained move.
- [ ] **TB-490** `planned` — Keep the score threshold as a secondary filter, but make trade-prints/ executed volume mandatory for emission.

---

## 2026-06-06 — Advisor snapshot 163

### Summary
The false positives are driven by quote-led price jumps that lack enough executed volume, especially in CPI-linked markets. The analyst labels consistently favor requiring stronger confirmation from both price move and volume before emitting a spike.

### Next step
Tighten the trigger so a spike requires a larger price move and non-zero executed volume, with CPI-specific minimum sustained-volume filtering if possible.

### Recommendations

- [ ] **TB-491** `planned` — Raise the minimum executed volume delta above the current floor so quote-only jumps do not trigger.
- [ ] **TB-492** `planned` — Increase the minimum price move threshold for CPI-style markets to filter small impulse moves.
- [ ] **TB-493** `planned` — Add a rule that suppresses signals unless both volume delta and price move clear their respective minimums.

---

## 2026-06-06 — Advisor snapshot 164

### Summary
The false positives are dominated by thin-market, quote-only price jumps that produce meaningful-looking price deltas without executed volume. Both analyst labels point to the same issue: require stronger confirmation from real traded volume and/or a larger move before emitting.

### Next step
Raise the trigger bar for thin CPI-style markets by requiring both non-zero executed volume and a higher minimum price move before scoring can pass threshold.

### Suggested thresholds
`min_volume_delta` → `1.0`, `min_price_move` → `0.08`, `score_threshold` → `5.5`

### Recommendations

- [ ] **TB-494** `planned` — Increase the price-move floor for this market type to cut quote-only jumps.
- [ ] **TB-495** `planned` — Add a hard non-zero executed-volume requirement so price-only moves do not trigger.
- [ ] **TB-496** `planned` — If you keep the current score model, raise the score threshold modestly to suppress marginal alerts.

---

## 2026-06-06 — Advisor snapshot 165

### Summary
The false positives are concentrated in thin, low-liquidity CPI-style markets where quote-driven price moves are being flagged without enough traded-volume confirmation. The analyst notes consistently recommend requiring either real executed volume or a larger sustained price move before emitting a spike.

### Next step
Tighten the detector by requiring both a higher minimum price move and a stronger trade-confirmation gate for low-liquidity markets; the clearest concrete change is to raise the price-move floor and add a volume/exec-trade confirmation requirement rather than relying on score alone.

### Suggested thresholds
`min_price_move` → `0.07`

### Recommendations

- [ ] **TB-497** `planned` — Raise spike_min_price_move from 0.03 to 0.07 for thin macro/CPI markets to suppress quote-only blips.
- [ ] **TB-498** `planned` — Add a hard trade-confirmation gate: do not emit unless executed-trade volume or order-book depth confirms the move.
- [ ] **TB-499** `planned` — Keep spike_score_threshold unchanged for now; the labels point more strongly to a missing confirmation filter than to a broadly too-low composite score.

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

- [ ] **TB-527** `planned` — Raise the minimum volume delta to filter out quote-only bursts in thin markets.
- [ ] **TB-528** `planned` — Increase the minimum price move so a short-lived 2%–5% quote swing does not trigger a spike.
- [ ] **TB-529** `planned` — Keep the score threshold modestly higher only after adding the volume/price floor, so genuinely informative flow is not muted.

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

- [ ] **TB-566** `planned` — Raise the minimum price move for low-priced macro contracts from 0.03 to 0.05 when trade count is low or confirmation is absent.
- [ ] **TB-567** `planned` — Increase the minimum volume delta for quote-driven Fed-style markets from 12700 to about 15000 before allowing a spike to fire.
- [ ] **TB-568** `planned` — Raise the score threshold modestly to filter mechanical repricings, but keep it below the level that would suppress confirmed high-volume moves.

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

- [ ] **TB-575** `planned` — Increase **min_price_move** from 0.03 to **0.05** for CPI/Fed-style contracts to filter small quote flickers.
- [ ] **TB-576** `planned` — Increase **min_volume_delta** from the current level to at least **1.5x baseline volume** (or an equivalent absolute floor) before watch-level emission.
- [ ] **TB-577** `planned` — Add a rule that quote-only moves must persist across **multiple trades / multi-tick follow-through**; otherwise suppress the spike even if score clears threshold.

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

- [ ] **TB-599** `planned` — Raise the minimum price move from 0.03 to 0.05 for watch-tier spike emissions in thin CPI/rate markets.
- [ ] **TB-600** `planned` — Increase the minimum volume delta to roughly 20000 for low-liquidity macro contracts to filter quote-only updates.
- [ ] **TB-601** `planned` — Raise the combined score threshold modestly to 3.0 so borderline watch signals do not emit unless both price and volume are clearly supportive.

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
