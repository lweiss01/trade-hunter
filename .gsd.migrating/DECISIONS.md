# Decisions Register

Append-only log of architectural and pattern decisions.

---

## D001: In-memory store for MVP, SQLite later
**Scope:** Architecture  
**Decision:** Use in-memory collections for MVP event store; migrate to SQLite in Phase 1.  
**Rationale:** Faster iteration during MVP validation. SQLite adds persistence but requires schema design and migration tooling. Defer until live data proves the detector logic works.  
**Made by:** Agent  
**When:** Initial architecture  
**Revisable:** Yes — migration to SQLite is already planned

## D002: Generic ingest API over vendor-specific endpoints
**Scope:** API design  
**Decision:** Single `POST /api/events` endpoint accepts normalized events from any source. Vendor-specific paths (e.g. `/api/alerts/polyalerthub`) are aliases that transform to canonical format.  
**Rationale:** Keeps core logic decoupled from upstream schema changes. Easy to add new sources (Polymarket Analytics, custom scrapers) without rewriting detection logic.  
**Made by:** Agent  
**When:** Initial API design  
**Revisable:** No — this pattern should hold

## D003: Transparent rule-based detection over ML scoring
**Scope:** Detection strategy  
**Decision:** Use explainable thresholds (volume delta vs baseline, price move, cooldown) instead of opaque ML models.  
**Rationale:** Trust requires interpretability. User needs to understand why an alert fired to decide whether to investigate. Simple rules also make tuning easier.  
**Made by:** Collaborative  
**When:** Detector design  
**Revisable:** No — core design principle

## D004: Discord webhook as primary notification channel
**Scope:** Notification strategy  
**Decision:** Prioritize Discord webhook over browser push, email, or in-app notifications.  
**Rationale:** User already monitors Discord. Webhook is low-friction, supports rich embeds, and doesn't require browser to be open.  
**Made by:** Collaborative  
**When:** Notification design  
**Revisable:** Yes — could add other channels later

## D005: Kalshi-first execution context, Polymarket-aware for comparison
**Scope:** Platform priority  
**Decision:** Optimize for Kalshi execution with Polymarket as a cross-reference context layer.  
**Rationale:** User trades on Kalshi. Polymarket provides comparison context for divergence detection but is not the primary execution venue.  
**Made by:** Collaborative  
**When:** Platform strategy  
**Revisable:** No — reflects actual trading workflow

## D006: No automated execution
**Scope:** Product boundary  
**Decision:** This tool surfaces signals and context; it does not place trades.  
**Rationale:** Solo retail trader needs decision support, not automated execution risk. Keeps regulatory complexity low and forces human review of every signal.  
**Made by:** Collaborative  
**When:** Product scoping  
**Revisable:** No — core product principle
