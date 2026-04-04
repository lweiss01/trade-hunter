# Trade Hunter UI Revision Checklist

Last updated: 2026-04-03

This checklist captures concrete changes to apply to the Trade Hunter dashboard mockup to improve readability, reduce visual noise, and better align the UI with the product’s decision-support goals.

---

## 1. Typography and Density

- [ ] Increase the root font size from `14px` to **15–16px** for better long-session readability.
- [ ] Raise the minimum size for recurring small text:
  - Pills, tags, table headers.
  - Flow metadata, status text, and settings helper copy.
- [ ] Reserve very small mono text for **secondary metadata only**, not primary decision information.
- [ ] Slightly increase `line-height` for:
  - Analyst rationale.
  - Settings descriptions.
  - Tuning/backlog text.

---

## 2. Tone Down Decorative Effects

- [ ] Reduce or remove the **grid texture** on `body::before` so it is barely perceptible, if kept at all.
- [ ] Reduce or remove the **teal radial glow** on `body::after` to avoid “AI template” vibes.
- [ ] Soften any glowy/outer-shadow treatments on:
  - Mode/health badges.
  - High-priority signal accents.

Goal: keep the terminal feel but rely more on solid surfaces and contrast than on glows.

---

## 3. Signal Cards

- [ ] Remove the thick **left accent stripe** on signal cards:
  - Replace with a subtler indicator: top accent rule, colored border, or small status chip.
- [ ] Make the signal **title** slightly larger or bolder than other card text so it clearly dominates.
- [ ] Reduce the number of visible **tags** by default:
  - Keep only the most important 2–3 tags in the primary row.
- [ ] Collapse low-value metadata into a single, tighter line.
- [ ] Shorten the default analyst rationale:
  - Show a truncated version in the list.
  - Move the full rationale to an expanded state or detail pane.
- [ ] De-emphasize or conditionally show the **score bar**:
  - Stronger visual weight for notable / high-conviction signals.
  - Quieter treatment or hidden for low-tier alerts.

---

## 4. “What Matters Now” Layer

- [ ] Add a **“Top signal right now”** strip above the signal list:
  - One most important alert with a brief “why this matters” summary.
- [ ] Pin 1–2 high-priority signals above the main feed:
  - Make these visually distinct (border, background, icon).
- [ ] For top alerts, include a short “next checks” / mini checklist row:
  - Examples: cross-venue check, liquidity check, catalyst check, etc.
- [ ] Add clear visual distinctions for:
  - New signals.
  - Important / high-conviction signals.
  - Items that need review vs. items already reviewed.

---

## 5. Selected-Signal Workspace

- [ ] Introduce a **selected-signal detail pane** (side panel or bottom panel):
  - Event summary.
  - Recent trade flow (for that market only).
  - Liquidity context.
  - Any cross-venue / divergence info (once implemented).
  - A small research checklist.
  - Note / journal area (future-friendly).
- [ ] Make signal cards clickable:
  - Clicking a card focuses the detail pane on that signal.
- [ ] Ensure the detail pane feels like the “workbench”:
  - List = triage.
  - Detail = investigation.

---

## 6. Top Bar and Header

- [ ] Keep **mode badge** (live vs simulation) and core **feed-health** indicators, but:
  - Limit the number of pills shown by default.
  - Move secondary telemetry into a hover tooltip or “more” expander.
- [ ] Give the **ticker quick-add input**:
  - Slightly more width.
  - Clearer placeholder text explaining what it accepts.
- [ ] Make the **settings button** more visually distinct:
  - Use icon + label, or a more “nav-like” control instead of a tiny subtle icon.
- [ ] Visually group header regions:
  - Brand.
  - Mode & health.
  - Navigation tabs.
  - Quick add & actions.

---

## 7. Live Trade Flow Panel

- [ ] Increase row height and horizontal padding for flow rows slightly to reduce crowding.
- [ ] Choose a single **primary focal metric** per row (e.g., price or market ID) and emphasize only that.
- [ ] Make duplicate count, side, and age visually secondary.
- [ ] Consider subtle zebra striping or stronger hover states for long lists.
- [ ] Make rows clickable:
  - Clicking a flow row selects that market and syncs the selected-signal/detail pane.

---

## 8. Market Table

- [ ] Loosen the truncation on market titles:
  - Allow wider columns or two-line wrap on hover/expanded state.
- [ ] Ensure human-readable titles visually dominate over raw IDs.
- [ ] Optionally add:
  - Per-row status indicator for “active anomaly / quiet / unresolved”.
- [ ] Add clear sort affordances for:
  - Volume.
  - Price move.
  - Freshness / last activity.
  - Score (if relevant).
- [ ] Add a quick filter for:
  - “Only markets with recent spikes.”
  - “Only tracked watchlists/themes.”

---

## 9. Topic Filters and Chips

- [ ] Reduce visual weight of **topic chips**:
  - They should not compete with signals for attention.
- [ ] Make active chips more obvious and inactive ones more neutral.
- [ ] Consider moving counts into small badges rather than inline text.

---

## 10. Category Search and Tracked Tickers

- [ ] After adding a ticker, show clearer **success / already tracked / unresolved** feedback.
- [ ] Add state markers on tracked tickers:
  - Active, quiet, unresolved, or stale feed.
- [ ] Ensure the “remove” action on ticker pills is large and easy to hit.
- [ ] Keep the search UX aligned with the user guide:
  - Category search → list of events → click to add.

---

## 11. Settings Page

### Grouping and Status

- [ ] Group settings into meaningful sections:
  - Core mode (live vs simulation).
  - Kalshi connection.
  - AI analyst.
  - Discord / notifications.
  - Ingest/auth (PolyAlertHub, generic ingest).
  - Detector tuning.
  - Storage / retention.
- [ ] For each section, show a concise status summary:
  - Configured.
  - Missing key.
  - Disabled.
- [ ] Distinguish “recommended” vs. “advanced” settings:
  - Hide advanced settings behind disclosure toggles.

### Form Usability

- [ ] Increase helper text size and line-height.
- [ ] Adjust input widths to match expected content (keys, URLs, lists).
- [ ] Add inline examples for:
  - `KALSHI_MARKETS` formats.
  - Discord webhook URLs.
  - API keys.
- [ ] Add “Test connection” buttons where feasible:
  - Kalshi.
  - AI provider(s).
  - Discord.

### Onboarding

- [ ] Add a first-run onboarding card or guided setup section at the top:
  - Offer presets such as:
    - “Simulation only”.
    - “Live Kalshi basic”.
    - “Full analyst + Discord alerts”.

---

## 12. Tuning Advisor and Backlog

- [ ] Make the **“best next tweak”** visually dominant in the tuning advisor UI.
- [ ] Clearly separate tuning backlog items into:
  - Applied.
  - Planned.
  - Rejected / superseded.
- [ ] For each tuning recommendation, display:
  - Short description.
  - Expected effect (e.g., “fewer thin-market false positives”).
- [ ] Where possible, link tuning suggestions to:
  - The signal patterns that motivated them.

---

## 13. Visual System Cleanup

- [ ] Reassess the use of secondary accent colors (e.g., indigo):
  - Reduce the number of distinct semantic accent colors in frequent UI elements.
- [ ] Reserve the strongest colors for:
  - Teal (healthy/live).
  - Amber (caution).
  - Red (alert/actionable).
- [ ] Make pills, tabs, tags, and buttons more visually distinct:
  - Tabs: stronger borders/underlines.
  - Filters: lighter chips.
  - Alert tags: small colored badges.

---

## 14. Accessibility and Comfort

- [ ] Ensure small/muted text still meets contrast requirements against the background.
- [ ] Add clear keyboard focus styles to:
  - Buttons.
  - Tabs.
  - Links.
  - Interactive chips and pills.
- [ ] Confirm that small icon-only controls:
  - Have accessible labels.
  - Have sufficiently large hit areas.
- [ ] Use more than color alone for important states:
  - Combine color with icons, wording, or position.

---

## 15. Responsive Behavior

- [ ] Define explicit collapse rules for:
  - Main grid (signal + detail vs. flow + markets).
  - Bottom grid / secondary panels.
  - Header layout (e.g., wrapping or collapsing telemetry).
- [ ] On narrower widths:
  - Stack secondary panels below the main signal area.
  - Move non-essential header pills into a drawer or menu.
- [ ] Verify that:
  - Tables remain readable (horizontal scroll or stacked cards).
  - Flow lists maintain reasonable row height and spacing.

---

## Implementation Order (Suggested)

1. Typography & density adjustments.
2. Remove left accent stripe and tone down ambient effects.
3. Simplify signal cards and add a “top signal” strip.
4. Implement a selected-signal detail pane.
5. Reorganize settings into workflow-based groups with status.
6. Tighten trade flow and market table hierarchy.
7. Add first-pass responsive rules for laptop widths.

Use this list as the source of truth for revising the `design-proposal.html` file and keep it updated as you implement changes.
