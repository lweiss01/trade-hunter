# Requirements Contract

Requirements move between states as slices prove or invalidate them:
- **Active**: currently in scope, being worked on or planned
- **Validated**: proven by completed slices with evidence
- **Deferred**: out of scope for current milestone, revisit later
- **Blocked**: waiting on external dependency or unresolved decision
- **Out of Scope**: explicitly excluded

---

## Active

### R001: Real-time market monitoring
**Description:** Monitor Kalshi and Polymarket markets for unusual activity (volume spikes, price moves) in real time.
**Primary owner:** Data ingestion + detection
**Supporting slices:** Feed adapters, spike detector
**Notes:** Core value proposition — must be reliable and timely.

### R002: Explainable alerts
**Description:** Every alert should explain why it was triggered (volume delta vs baseline, price move, tier assignment) with transparent rules.
**Primary owner:** Detection logic
**Supporting slices:** Spike detector, alert cards
**Notes:** Trust requires interpretability — no black-box scoring.

### R003: Cross-platform divergence detection
**Description:** Detect and surface price disagreements between equivalent Kalshi and Polymarket contracts.
**Primary owner:** Cross-platform analysis
**Supporting slices:** Market matching, spread monitoring
**Notes:** High-value signal — pricing disagreements are actionable.

### R004: Discord notifications
**Description:** Push alerts to Discord webhook with rich embeds, categories, and acknowledgment workflow.
**Primary owner:** Notification system
**Supporting slices:** Discord notifier
**Notes:** Primary awareness channel — should be reliable and configurable.

### R005: Persistent event history
**Description:** Store events, signals, and feed health in SQLite with retention policy.
**Primary owner:** Storage layer
**Supporting slices:** SQLite migration
**Notes:** Enables historical analysis and outcome tracking.

### R006: Liquidity-aware context
**Description:** Include bid/ask spread, recent trade count, estimated slippage in signal explanations.
**Primary owner:** Market context enrichment
**Supporting slices:** Liquidity metrics
**Notes:** Prevents false positives from thin-market noise.

### R007: Watchlists and filters
**Description:** Support user-defined watchlists by platform, category, topic, liquidity, volume threshold.
**Primary owner:** Filtering system
**Supporting slices:** Watchlist UI, filter controls
**Notes:** Makes alert stream relevant — reduces noise.

### R008: Signal outcome tracking
**Description:** Record what happened after each alert (price movement, divergence closure, reversion) and whether user acted.
**Primary owner:** Feedback loop
**Supporting slices:** Outcome logger
**Notes:** Learn which signals are useful over time.

### R009: Catalyst context
**Description:** Attach scheduled events (CPI release, Fed speaker, election debate) to alerts when available.
**Primary owner:** External data enrichment
**Supporting slices:** Catalyst feed
**Notes:** Easier to interpret moves with known catalysts.

### R010: Detector tuning dashboard
**Description:** UI controls for baseline window, volume threshold, price threshold, cooldown, venue-specific sensitivity.
**Primary owner:** Configuration UI
**Supporting slices:** Tuning controls
**Notes:** Adapt detector to different market behaviors.

---

## Validated

_No requirements validated yet._

---

## Deferred

### R011: Browser push notifications
**Description:** Push notifications to browser when dashboard is not focused.
**Primary owner:** Browser API integration
**Notes:** Deferred — Discord webhook is higher priority.

### R012: Mobile-friendly layout
**Description:** Responsive dashboard optimized for mobile review during active market periods.
**Primary owner:** UI/UX
**Notes:** Deferred — desktop-first for now.

### R013: Portfolio awareness
**Description:** Prioritize alerts for contracts user already holds.
**Primary owner:** Position tracking
**Notes:** Deferred — requires position data integration.

### R014: Backtesting harness
**Description:** Test detector settings against historical data to optimize thresholds.
**Primary owner:** Analytics tooling
**Notes:** Deferred — need persistent data first.

---

## Blocked

_No requirements blocked._

---

## Out of Scope

### R015: Automated trade execution
**Description:** Auto-place orders based on signals.
**Primary owner:** N/A
**Notes:** Explicitly out of scope — this is a research tool, not an execution system.

### R016: Real-time charting library
**Description:** Embedded TradingView-style charts for every market.
**Primary owner:** N/A
**Notes:** Out of scope — external charting tools are sufficient.
