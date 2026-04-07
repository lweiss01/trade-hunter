# Trade Hunter Roadmap

This roadmap turns the current MVP into a practical decision-support tool for prediction-market research.

The guiding principle is simple: surface unusual market behavior quickly, explain why it matters, and make the next research step obvious.

## Product goal

Help a small retail trader notice market activity that deserves attention without drowning in noise.

Trade Hunter should answer four questions clearly:

1. What is moving right now?
2. Why does this look unusual?
3. Is the move isolated to one venue or echoed elsewhere?
4. What should I inspect before deciding whether there is a tradable edge?

## Current state

Already built in this repo:

- local dashboard with recent signals, feed status, and market tape
- in-memory event store
- spike detector using volume delta, price movement, and rolling baselines
- generic ingest API for outside alerts
- PolyAlertHub-compatible ingest endpoint
- optional `pykalshi` adapter scaffold
- Discord webhook notification path
- simulation feed for local testing

This is a good foundation, but it is still an operator dashboard rather than a full trading-research assistant.

## Guiding principles

- Prefer explainable alerts over black-box scoring
- Keep false positives low enough that alerts remain worth reading
- Show cross-platform context whenever possible
- Separate signal detection from trade decision-making
- Make the dashboard legible for quick scanning during active market periods
- Default to observational tooling, not automated execution

## Phase 1: Connect the real feeds

Goal: replace fake data with useful live inputs.

### 1. PolyAlertHub ingest

Objective:
- accept real PolyAlertHub alerts and normalize them into the internal event schema

Deliverables:
- documented relay format for PolyAlertHub payloads
- signature or token validation for inbound alerts
- source-specific parsing for whale, trader, price, and market alerts
- source labels in the dashboard so you can see whether a spike came from your detector or an outside alert feed

Why it matters:
- gives you immediate value without needing to invent every signal yourself
- lets you compare vendor alerts against your own detector over time

### 2. Kalshi live stream via `pykalshi`

Objective:
- subscribe to selected Kalshi markets and convert ticker and trade updates into detector-ready events

Deliverables:
- env-driven market subscription lists
- reconnect handling and status reporting
- normalized trade-size and price updates
- market metadata enrichment so ticker symbols resolve to readable titles

Why it matters:
- gives you a direct feed for the venue you are actively trading on
- enables custom detection instead of relying only on third-party services

### 3. Better local persistence

Objective:
- move from memory-only state to SQLite

Deliverables:
- event table
- signal table
- feed-health table
- simple retention policy and archival rules

Why it matters:
- lets you answer whether a signal type is actually useful over days and weeks
- prevents data loss on restart or external-drive disconnects

## Phase 2: Make signals understandable

Goal: turn raw alerts into interpretable context.

### 4. Signal explanation cards

Add per-signal breakdowns such as:
- volume delta versus 1-hour and 24-hour baseline
- yes-price move over 1 minute, 5 minutes, and 30 minutes
- whether the signal was detector-driven, vendor-driven, or both
- last few events leading into the spike

Why it matters:
- lets you decide quickly whether the move is just noise, a liquidity sweep, or a real repricing event

### 5. Confidence and severity tiers

Add labels like:
- watch
- notable
- high conviction flow
- cross-venue divergence

This should be based on transparent rules, not vague AI scoring.

Why it matters:
- helps you rank alerts when several markets move at once

### 6. Cleaner dashboard information architecture

Add dedicated views for:
- live spike board
- watchlists by theme
- market detail page
- venue comparison page
- alert history

Why it matters:
- makes the app easier to scan and less like a raw event console

## Phase 3: Cross-platform edge detection

Goal: find discrepancies, not just movement.

### 7. Cross-platform market matching

Objective:
- map equivalent or near-equivalent markets between Kalshi and Polymarket

Deliverables:
- manual mapping table first
- later, fuzzy title matching with review controls
- shared event pages showing both venues side by side

Why it matters:
- the most actionable signals often come from disagreement, lag, or overreaction across platforms

### 8. Spread and divergence monitoring

Track:
- yes-price gap between equivalent contracts
- divergence persistence over time
- sudden narrowing or widening of spread
- divergence adjusted for fees and liquidity

Why it matters:
- this is where “interesting spike” starts becoming “possible edge to investigate”

### 9. Liquidity-aware interpretation

Add context like:
- bid/ask spread
- recent trade count
- estimated slippage for small position sizes
- order-book imbalance where available

Why it matters:
- a move in a thin market can look dramatic but be hard to monetize responsibly

## Phase 4: Actionability and workflow

Goal: make the app useful during real decision-making.

### 10. Research checklist on each alert

Every signal should prompt a short workflow such as:
- what changed?
- is the move cross-platform?
- was there news?
- is liquidity sufficient?
- is the market nearing resolution or a key catalyst?
- what invalidates the trade idea?

Why it matters:
- helps reduce impulsive decisions driven by adrenaline or FOMO

### 11. Discord improvements

Upgrade from basic webhook alerts to:
- richer embeds
- alert categories and colors
- watchlist-specific channels
- acknowledge or snooze links
- daily digest of strongest signals

Why it matters:
- reduces dashboard dependence and improves follow-through

### 12. Personal watchlists and filters

Support filters by:
- platform
- category
- market status
- event date window
- minimum liquidity
- minimum volume surge
- custom keyword lists

Why it matters:
- makes the app fit your interests instead of forcing one global signal stream

## Phase 5: Evidence and feedback loops

Goal: learn which alerts are actually useful.

### 13. Signal outcome tracking

For each alert, record:
- what the price did afterward
- whether the divergence closed
- whether the move reverted quickly
- whether you acted on it
- whether it would have been useful in hindsight

Why it matters:
- turns intuition into measurable feedback

### 14. Journal and tagging system

Allow notes such as:
- real edge
- false alarm
- news-driven
- low-liquidity fake-out
- good setup but too late

Why it matters:
- helps improve both detector tuning and your own process

### 15. Detector tuning dashboard

Add controls for:
- baseline window length
- volume spike multiple
- price move threshold
- cooldown window
- venue-specific sensitivity

Why it matters:
- lets you adapt the detector to different categories of market behavior

## Phase 6: Higher-leverage enhancements

Goal: make the tool smarter without making it opaque.

### 16. News and catalyst context

Attach recent headlines or scheduled catalysts to a spike when possible.

Examples:
- CPI release upcoming
- Fed speaker in 20 minutes
- court ruling expected today
- election debate tonight

Why it matters:
- a move is easier to interpret when tied to a likely catalyst

### 17. Topic-level heatmaps

Show where activity is clustering across themes like:
- macro
- elections
- crypto
- sports
- geopolitics

Why it matters:
- helps identify sector-wide flow instead of isolated noise

### 18. Multi-signal confirmation

Boost importance when several conditions line up:
- spike in volume
- price repricing
- whale alert
- cross-platform divergence
- catalyst proximity

Why it matters:
- one weak clue is noise; multiple aligned clues are more interesting

### 19. Explainable ranking model

Eventually replace simple thresholds with a weighted ranking model, but keep it human-readable.

For example:
- 35% volume abnormality
- 25% price abnormality
- 20% cross-platform divergence
- 10% liquidity quality
- 10% catalyst relevance

Why it matters:
- improves prioritization while keeping trust high

## Nice-to-have ideas

These are useful, but not first-wave priorities:

- mobile-friendly layout refinement
- browser push notifications
- exportable CSV or notebook-style review packets
- dark/light theme toggle
- reusable templates for elections, macro, and crypto watchlists
- side-by-side charting for matched markets
- portfolio-awareness so alerts can prioritize contracts you already hold
- simple backtesting harness for detector settings

## Recommended build order

Best next sequence:

1. PolyAlertHub ingest hardening
2. Kalshi `pykalshi` live connection
3. SQLite persistence
4. alert detail pages and explanation cards
5. cross-platform market matching
6. spread/divergence views
7. outcome tracking and tuning tools

This order matters because it prioritizes real data quality before advanced UI and analytics.

## What will make this app genuinely better

The highest-value improvements are probably not more charts.

The most useful upgrades are:
- better signal explanations
- cross-platform divergence detection
- liquidity-aware context
- historical outcome tracking
- filters that keep your alert stream relevant

Those features are what turn a noisy monitor into something that can actually sharpen judgment.

## Suggested interpretation for your use case

Since you have started small on Kalshi and want an edge without overcomplicating things, the best version of this tool is probably:
- Kalshi-first for execution context
- Polymarket-aware for comparison context
- Discord-enabled for timely awareness
- opinionated about filtering out low-quality, low-liquidity noise

That gives you a workflow that is realistic for a solo trader with a small account: fewer alerts, clearer explanations, faster review.

- ⬜ **M010:** Cross-Platform Whale Flow (Polymarket)
- ⬜ **M011:** AI Whale Tuning & Analysis
- ⬜ **M012:** Tuning Conflict Resolution Layer
