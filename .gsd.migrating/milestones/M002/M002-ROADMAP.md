# M002: 

## Vision
Turn raw alerts into interpretable context. By the end of this milestone, users can quickly understand why a signal fired, how severe it is, and what events led into the spike.

## Slice Overview
| ID | Slice | Risk | Depends | Done | After this |
|----|-------|------|---------|------|------------|
| S01 | Signal Explanation Cards | low | — | ⬜ | Signal detail card shows volume delta vs 1-hour and 24-hour baseline, price move over 1 min/5 min/30 min, whether signal was detector-driven or vendor-driven, and last 5 events leading into spike. |
| S02 | Confidence and Severity Tier Refinement | low | S01 | ⬜ | Signals labeled as watch/notable/high conviction flow based on transparent composite scoring. High conviction requires score ≥ 6.0, price move ≥ 1.75x threshold, volume multiple ≥ 3.0. |
| S03 | Dashboard Information Architecture | low | S01, S02 | ⬜ | Dashboard has dedicated views: live spike board (most recent signals), market detail (full event timeline for a market), alert history (all signals with filters). |
