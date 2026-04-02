# M003: 

## Vision
Find pricing disagreements across platforms. By the end of this milestone, the app will detect when Kalshi and Polymarket diverge on equivalent contracts and provide liquidity context to assess whether the divergence is actionable.

## Slice Overview
| ID | Slice | Risk | Depends | Done | After this |
|----|-------|------|---------|------|------------|
| S01 | Cross-Platform Market Matching | low | — | ⬜ | Market mapping table defines equivalent Kalshi and Polymarket contracts. Dashboard shows paired markets side by side with shared event page. |
| S02 | Spread and Divergence Monitoring | medium | S01 | ⬜ | Spread monitoring calculates yes-price gap between paired markets. Alerts trigger when spread exceeds threshold and persists for configured duration. |
| S03 | Liquidity-Aware Interpretation | medium | S02 | ⬜ | Signal cards show liquidity context: bid/ask spread (if available), recent trade count (last 30 min), estimated slippage for $100 position. |
