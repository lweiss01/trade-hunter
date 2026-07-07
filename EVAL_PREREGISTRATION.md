# Trade Hunter Agent Evaluation: Pre-Registration

**Status:** committed BEFORE any scoring of live signals.
**Date registered:** 2026-07-04
**Methodology version:** v1.0
**Scorer pinned at commit:** d756a43d8b71ab9270754053f8849f0abd361f7d
**Signal log schema_version:** 1

This file exists to stop me moving the goalposts after seeing results. Once
committed it is not edited. If the methodology has to change, a new dated file
supersedes it (v1.1, v2.0, ...) and the change is explained. The old file stays
in git history.

---

## 1. Hypothesis under test

The Trade Hunter agent's probability estimate for a flagged market beats the
market's own implied probability at signal time, by enough to survive spread
and fees. Raw accuracy is not the claim. The claim is edge versus the price
that was already there.

## 2. Unit of analysis

One resolved signal event: an agent recommendation frozen at time T, joined to
the market's later settlement. The market's YES bid/ask at T is captured in the
same snapshot the agent saw. No price is backfilled after T.

## 3. Scope and honest limits

- The claim is "on the markets the agent chooses to flag," not "on all markets."
  The agent is a filter and the evaluation set is filtered. This is stated, not
  hidden.
- Evaluation is walk-forward only. Any period the agent tuned on is excluded
  from scoring. The agent is never scored on markets it saw resolve during
  tuning.
- Voided or cancelled markets are dropped, not counted as pushes.
- Benchmark applies to probability markets (Kalshi-style, price = implied prob).
  Non-probability tickers are scored separately and are out of scope for the
  headline claim in v1.0.

## 4. Metrics and pass bars

| Metric | Role | Pass bar |
|---|---|---|
| Brier Skill Score vs market | Headline | > 0 AND bootstrap 95% CI excludes 0 |
| Beat-market rate | Headline | > 0.55 AND CI lower bound > 0.50 |
| Net P&L per market (flat, after fees) | Economic headline | ROI > 0 AND CI excludes 0 |
| Log loss vs market | Support | lower than market's |
| Directional hit rate vs market | Support | above market's |
| Calibration (ECE) | Diagnostic | < 0.05 |
| AUC | Diagnostic | > 0.60 |
| Fractional-Kelly log-growth / max DD | Economic support | positive growth, drawdown tolerable |

An edge is claimed only if all three headline bars pass together. Any single
headline CI that straddles its line means "not yet," regardless of the point
estimate.

## 5. Sample-size gates

- Below 30 resolved pairs: preliminary only, no headline is read.
- 100 resolved pairs: minimum before any public claim.
- Category-level claims (politics, econ, sports, ...) require 30+ resolved
  pairs within that category before that category's number is reported.

## 6. Baselines the agent must beat

Market price at T (the one that matters), always-favorite, coin-flip,
buy-and-hold the flagged market. If the agent cannot beat the market-price
baseline, there is no edge no matter how good raw accuracy looks.

## 7. Multiple testing

Testing across many tickers guarantees some look great by luck. The headline is
the aggregate across flagged markets, not a cherry-picked ticker or category.
If per-ticker claims are made, they are corrected for the number of tickers
tested.

## 8. Cost assumptions

Trades are simulated at the ask, not the mid. Kalshi taker fee formula
ceil(0.07 x P x (1-P) x 100) / 100 per contract, settlement free. Sports and
index markets use different multipliers and are scored with the correct one.
Fee schedule verified against the live Kalshi schedule at time of scoring.

## 9. Validity guard

Scoring refuses to run on a log whose hash chain fails verification. A tampered
or truncated log is not scored. The scorer version is pinned above, so the
exact scoring code committed before results cannot be silently changed to
produce a better number.

---

_Registered before viewing any live scoring output. Do not edit; supersede._
