# Knowledge Register

Append-only log of project-specific rules, patterns, and lessons learned.

Read this at the start of every unit. Append when discovering recurring issues, non-obvious patterns, or rules future agents should follow.

---

## K001: Volume normalization varies by source
**Category:** Data model  
**When:** Initial event schema design  
**What:** `MarketEvent.volume_kind` can be `"cumulative"` (running total) or `"delta"` (incremental change). Detector must compute delta from cumulative when needed.  
**Why it matters:** Kalshi WebSocket sends cumulative volume; PolyAlertHub might send deltas. Detector assumes delta for spike calculation, so normalization must happen in `_volume_delta()`.  
**Pattern:** Always check `volume_kind` before using `volume` in detector logic.

## K002: Spike cooldown prevents alert spam
**Category:** Detection tuning  
**When:** Detector implementation  
**What:** `spike_cooldown_seconds` (default 300s) prevents re-alerting on the same market within the cooldown window.  
**Why it matters:** Without cooldown, a sustained move would trigger dozens of alerts. Cooldown ensures one alert per distinct move.  
**Pattern:** When adjusting detector thresholds, verify cooldown is still appropriate. High-volatility markets may need shorter cooldowns; low-volatility may need longer.

## K003: Tier assignment uses composite scoring
**Category:** Signal interpretation  
**When:** Tier logic implementation  
**What:** Tiers are `watch` (baseline), `notable` (elevated score or moderate move), `high conviction flow` (extreme score + high volume multiple + large price move), and `cross-venue divergence` (special case).  
**Why it matters:** Tier helps prioritize when multiple alerts arrive simultaneously.  
**Pattern:** When adding new tier logic, preserve the composite scoring (volume multiple + price move + score threshold) to avoid oversensitivity.

## K004: Topic inference uses keyword matching
**Category:** Categorization  
**When:** Topic assignment  
**What:** `_topic()` uses simple keyword matching on `title` and `market_id` to assign categories: crypto, elections, macro, sports, geopolitics, general.  
**Why it matters:** Topic assignment is used for filtering and watchlist grouping.  
**Pattern:** When adding new topics, extend the keyword map in `detector.py::_topic()`. Avoid over-tuning — simple heuristics are better than brittle regexes.

## K005: Dashboard uses thread-safe in-memory store
**Category:** Concurrency  
**When:** Store implementation  
**What:** `MarketStore` uses `threading.Lock` to protect shared state. Multiple feeds and API requests can write events concurrently.  
**Why it matters:** Without locking, concurrent writes would corrupt deques and dicts.  
**Pattern:** When migrating to SQLite, preserve transactional safety. SQLite's default `SERIALIZED` mode is sufficient for this workload.

## K006: Feed status tracking separate from event data
**Category:** Observability  
**When:** Feed adapter design  
**What:** Each feed reports health via `store.update_feed_status(name, payload)` with fields like `status`, `last_event_at`, `error_count`, `reconnects`.  
**Why it matters:** Dashboard needs to distinguish "no signals" from "feed is down."  
**Pattern:** Every feed adapter should call `update_feed_status()` on start, stop, error, and reconnect.

## K007: Kalshi WebSocket sends variable message schemas
**Category:** External API quirk  
**When:** Kalshi adapter development  
**What:** Kalshi WebSocket messages vary by subscription type. Ticker updates have different fields than trade updates. Some fields are optional.  
**Why it matters:** Adapter must be defensive when extracting `yes_bid`, `no_ask`, `volume`, etc.  
**Pattern:** Use `.get()` with defaults instead of direct key access. Log unexpected schemas for debugging.

## K008: Simulation feed uses realistic event timing
**Category:** Testing  
**When:** Simulation feed implementation  
**What:** Simulation feed sleeps 1-3 seconds between events and generates realistic volume/price sequences.  
**Why it matters:** Makes local testing meaningful without credentials. Detector behavior should match production.  
**Pattern:** When adding new feed types, create a simulation mode first to verify detector logic before connecting live data.
