# Trade Hunter 🎯

**The institutional edge for prediction market flow.**

In prediction markets, alpha isn't just about knowing the news first—it's about seeing the money move before the news breaks. By the time a headline hits social media, the orderbook has already repriced. 

**Trade Hunter** is a real-time, locally-hosted intelligence dashboard built to catch coordinated institutional flow, aggressive hedging, and mathematically improbable volume spikes across prediction markets (like Kalshi) the exact second they happen.

---

## ⚡ Why Trade Hunter?

Standard price charts show you where a market has been. Trade Hunter tells you *who* is moving it right now. 

Instead of staring at a dozen tabs, Trade Hunter silently monitors every active prediction market simultaneously. It strips out retail noise and mathematically models the baseline flow, screaming only when it detects undeniable, high-conviction momentum.

### The Feature Mix
* **🐋 Whale Cluster Detection:** Uses dynamic 99th-percentile trade caching and Poisson probability modeling (p < 0.01) to detect when massive, coordinated orders sweep the book within a 120-second rolling window.
* **🧠 Dual AI Analysts (Claude + Perplexity):** Every major spike is immediately analyzed by an integrated AI agent. It reads the order flow context and labels the move as `signal`, `noise`, or `uncertain`, attaching a plain-English rationale.
* **⚙️ Autonomous Tuning Advisor:** An AI feedback loop that actively reads the historical database of false positives and autonomously suggests threshold corrections, ensuring the detector gets smarter over time.
* **📈 Dynamic Baseline Detector:** Flags `notable` or `high conviction flow` based on dynamic volume delta multiples and price-action thresholds, rather than static numbers.
* **🔔 Smart Discord Integration:** Routes specific market topics (e.g., Crypto, Elections, Geopolitics) to different Discord channels, optionally filtering out alerts until the AI Analyst confirms they are genuine signals.
* **🔌 PolyAlertHub Relay:** Built-in endpoint for ingesting third-party or external scraper alerts directly into your flow.
* **💾 Zero-Friction Local Runtime:** Powered by a lightweight SQLite backbone with self-cleaning retention, running seamlessly on `localhost:8765`.

---

## 🚀 Quick Start

Ensure you have Python 3.11+ installed.

```bash
# On Windows (uses our guarded, self-healing single-instance launcher):
.\trade-hunter.cmd

# On macOS / Linux:
python -m app
```

Open `http://127.0.0.1:8765` in your browser.

> **Note:** By default, Trade Hunter starts in `SIMULATION` mode, injecting synthetic data so you can see the dashboard light up immediately without any API keys.

---

## ⚙️ Configuration & Live Mode

To switch to live Kalshi data and enable the AI Analysts, create a `.env` file in the root directory:

```env
# Core Modes
ENABLE_SIMULATION=false
ENABLE_KALSHI=true

# Kalshi Credentials
KALSHI_API_KEY_ID=your-key-id
KALSHI_PRIVATE_KEY_PATH=/path/to/kalshi.key
KALSHI_MARKETS=KXBTC15M,KXTOPCHEF-26DEC31

# AI Analyst Integrations
ANTHROPIC_API_KEY=sk-ant-api03...  # Primary Analyst
PERPLEXITY_API_KEY=pplx-...        # Fallback Analyst

# Notifications
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

### Market Resolution Magic
You don't need to hunt for exact contract IDs. `KALSHI_MARKETS` accepts:
* **Series Slugs** (e.g., `KXBTC15M`) → Auto-resolves to the currently open 15-minute BTC market.
* **Event Tickers** (e.g., `KXTOPCHEF`) → Auto-subscribes to *all* open sub-markets for that event.
* **Specific Tickers** → For tracking an exact, granular contract.

You can also dynamically add/remove markets directly from the Dashboard UI without ever restarting the server.

---

## 📊 Reading the Dashboard

When an alert fires, it is graded into visual tiers so you know exactly how to react:

| Tier | Meaning | Visual |
|---|---|---|
| `watch` | Noticeable activity, worth monitoring. | Standard |
| `notable` | Significant move, worth investigating. | Yellow Edge |
| `high conviction flow` | Massive volume multiple + price shift. | Red Neon Edge |
| `whale-cluster` | >=3 99th-percentile trades in 120s (p < 0.01). | Purple Neon Edge |

**The 10-Minute Freshness Window:** 
In live mode, the dashboard exclusively displays events from the last 10 minutes. If the panels look empty, check the status pills at the top—if `kalshi seen` is updating, data is flowing, but the markets are just genuinely quiet.

---

## 🛠️ System Architecture

* **Database:** SQLite (`trade_hunter.db`). Survives restarts, auto-cleans events older than `RETENTION_DAYS` (default 7).
* **Single-Instance Guardian:** On Windows, `trade-hunter.cmd` automatically hunts down and cleanly terminates any hanging or zombied instances holding port 8765 before launching, guaranteeing a pristine startup every time.
* **Testing:** Run `py -m app --smoke-test` to safely test the detector pipeline and AI integrations locally without touching live order flow.

---
*Built to separate the signal from the noise.*