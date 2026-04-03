const metricsEl = document.querySelector("#metrics");
const signalsEl = document.querySelector("#signals");
const signalSortEl = document.querySelector("#signal-sort");
const signalLatestToggleEl = document.querySelector("#signal-latest-toggle");
const activityEl = document.querySelector("#activity");
const feedsEl = document.querySelector("#feeds");
const marketsEl = document.querySelector("#markets");
const demoButton = document.querySelector("#demo-spike");
const demoPanel = document.querySelector("#demo-panel");
const tickerForm = document.querySelector("#ticker-form");
const tickerInput = document.querySelector("#ticker-input");
const tickerListEl = document.querySelector("#ticker-list");
const tickerMessageEl = document.querySelector("#ticker-message");
const tickerAddButton = document.querySelector("#ticker-add");
const categoryForm = document.querySelector("#category-form");
const categoryInput = document.querySelector("#category-input");
const categoryResultsEl = document.querySelector("#category-results");
const categoryMessageEl = document.querySelector("#category-message");

let tickerMutationInFlight = false;
let trackedTickers = [];
let signalSortMode = "newest";
let signalLatestOnly = false;
let lastDashboardState = null;

// Per-market price history for sparklines (last 20 yes_price values)
const priceHistory = new Map();
const SPARK_MAX = 20;

function recordPriceHistory(events) {
  for (const e of (events || [])) {
    if (e.yes_price == null) continue;
    const mid = e.market_id || "unknown";
    if (!priceHistory.has(mid)) priceHistory.set(mid, []);
    const hist = priceHistory.get(mid);
    hist.push(e.yes_price);
    if (hist.length > SPARK_MAX) hist.shift();
  }
}

function sparklineSvg(marketId) {
  const hist = priceHistory.get(marketId);
  if (!hist || hist.length < 2) return "";
  const w = 48, h = 14, pad = 1;
  const min = Math.min(...hist);
  const max = Math.max(...hist);
  const range = max - min || 0.001;
  const pts = hist.map((v, i) => {
    const x = pad + (i / (hist.length - 1)) * (w - pad * 2);
    const y = (h - pad) - ((v - min) / range) * (h - pad * 2);
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(" ");
  const trend = hist[hist.length - 1] - hist[hist.length - 2];
  const color = trend > 0.001 ? "var(--success)" : trend < -0.001 ? "var(--danger)" : "var(--muted)";
  return `<svg class="sparkline" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" aria-hidden="true"><polyline points="${pts}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"/></svg>`;
}

async function fetchState() {
  const response = await fetch("/api/state");
  if (!response.ok) {
    throw new Error("Failed to load dashboard state");
  }
  return response.json();
}

async function postTicker(url, ticker) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ticker }),
  });

  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || "Ticker request failed");
  }

  return payload.markets || [];
}

function normalizeTicker(value) {
  return String(value || "").trim().toUpperCase();
}

function isValidTickerFormat(ticker) {
  return /^[A-Z0-9](?:[A-Z0-9-]{1,62}[A-Z0-9])?$/.test(ticker);
}

function setTickerMessage(message, isError = false) {
  if (!tickerMessageEl) return;
  tickerMessageEl.textContent = message;
  tickerMessageEl.classList.toggle("error", isError);
}

function renderModeUI(config) {
  const mode = config?.active_mode || "none";
  if (demoPanel) {
    demoPanel.style.display = mode === "simulation" ? "block" : "none";
  }
}

function setTickerMutationBusy(isBusy) {
  tickerMutationInFlight = isBusy;

  if (tickerForm) {
    tickerForm.setAttribute("aria-busy", isBusy ? "true" : "false");
  }

  if (tickerInput) {
    tickerInput.disabled = isBusy;
  }

  if (tickerAddButton) {
    tickerAddButton.disabled = isBusy;
  }

  if (tickerListEl) {
    tickerListEl
      .querySelectorAll(".ticker-remove")
      .forEach((button) => {
        button.disabled = isBusy;
      });
  }
}

function formatPrice(value) {
  if (value === null || value === undefined) return "n/a";
  return `${(value * 100).toFixed(1)}c`;
}

function formatTimestamp(value) {
  const date = new Date(value);
  return date.toLocaleTimeString([], { hour: "numeric", minute: "2-digit", second: "2-digit" });
}

function formatAgeFromNow(value) {
  if (!value) return "unknown";
  const ts = new Date(value).getTime();
  if (!Number.isFinite(ts)) return "unknown";
  const deltaMs = Date.now() - ts;
  const mins = Math.max(0, Math.floor(deltaMs / 60000));
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  const rem = mins % 60;
  return rem ? `${hours}h ${rem}m ago` : `${hours}h ago`;
}

function flowFreshness(value) {
  const ts = new Date(value).getTime();
  if (!Number.isFinite(ts)) return { label: "unknown", className: "stale" };

  const ageMinutes = Math.max(0, Math.floor((Date.now() - ts) / 60000));
  if (ageMinutes <= 5) return { label: `fresh ${ageMinutes}m`, className: "fresh" };
  if (ageMinutes <= 15) return { label: `warm ${ageMinutes}m`, className: "warm" };
  return { label: `stale ${ageMinutes}m`, className: "stale" };
}

function formatVolume(value) {
  if (value === null || value === undefined) return "n/a";
  return Number(value).toLocaleString(undefined, {
    minimumFractionDigits: value >= 100 ? 0 : 1,
    maximumFractionDigits: value >= 100 ? 0 : 1,
  });
}

function renderMetrics(state) {
  const markets = state.markets || [];
  const signals = state.signals || [];
  const feeds = state.feeds || {};
  const config = state.config || {};
  const summary = state.summary || {};
  const telemetry = state.telemetry || {};
  const liveWindow = telemetry.freshness_window_minutes;
  const routeCount = (config.discord_routes || []).length;

  metricsEl.innerHTML = `
    <article class="metric-card">
      <div class="metric-label">Tracked Markets</div>
      <div class="metric-value">${markets.length}</div>
      <div class="metric-subtle">latest state within ${liveWindow || "active"}m window</div>
    </article>
    <article class="metric-card">
      <div class="metric-label">Recent Signals</div>
      <div class="metric-value">${signals.length}</div>
      <div class="metric-subtle">detector hits within ${liveWindow || "active"}m window</div>
    </article>
    <article class="metric-card">
      <div class="metric-label">Live Flow</div>
      <div class="metric-value">${summary.live_events || 0}</div>
      <div class="metric-subtle">recent live events in window</div>
    </article>
    <article class="metric-card">
      <div class="metric-label">Trade Events</div>
      <div class="metric-value">${summary.trade_events || 0}</div>
      <div class="metric-subtle">recent trade-style updates</div>
    </article>
    <article class="metric-card">
      <div class="metric-label">Feed Health</div>
      <div class="metric-value">${Object.keys(feeds).length}</div>
      <div class="metric-subtle">${config.kalshi ? "Kalshi enabled" : "Kalshi disabled"}</div>
    </article>
    <article class="metric-card">
      <div class="metric-label">Discord Routes</div>
      <div class="metric-value">${routeCount}</div>
      <div class="metric-subtle">${routeCount ? config.discord_routes.join(", ") : "default only or disabled"}</div>
    </article>
  `;
}

function signalFreshness(value) {
  const ts = new Date(value).getTime();
  if (!Number.isFinite(ts)) return { label: "unknown", className: "stale" };

  const ageMinutes = Math.max(0, Math.floor((Date.now() - ts) / 60000));
  if (ageMinutes <= 5) return { label: `fresh ${ageMinutes}m`, className: "fresh" };
  if (ageMinutes <= 15) return { label: `warm ${ageMinutes}m`, className: "warm" };
  return { label: `stale ${ageMinutes}m`, className: "stale" };
}

function summarizeReason(reason) {
  const text = String(reason || "").trim();
  if (!text) return "No detector rationale available.";
  return text.length > 140 ? `${text.slice(0, 137)}…` : text;
}

function normalizeSignals(signals) {
  let result = [...signals];

  if (signalLatestOnly) {
    const seen = new Set();
    result = result.filter((signal) => {
      const marketId = signal?.event?.market_id || "unknown-market";
      if (seen.has(marketId)) return false;
      seen.add(marketId);
      return true;
    });
  }

  if (signalSortMode === "score") {
    result.sort((a, b) => Number(b.score || 0) - Number(a.score || 0));
  } else {
    result.sort((a, b) => new Date(b.detected_at).getTime() - new Date(a.detected_at).getTime());
  }

  return result;
}

function renderSignals(signals) {
  const ordered = normalizeSignals(signals || []);

  if (!ordered.length) {
    const latestSignalAge = formatAgeFromNow(lastDashboardState?.telemetry?.latest_signal_at);
    const windowMinutes = lastDashboardState?.telemetry?.freshness_window_minutes;
    if (windowMinutes) {
      signalsEl.innerHTML = `<div class="empty">No signals in the last ${windowMinutes} minutes. Last stored signal: ${escapeHtml(latestSignalAge)}.</div>`;
    } else {
      signalsEl.innerHTML = `<div class="empty">No spikes yet. Keep the page open or trigger the demo event.</div>`;
    }
    return;
  }

  signalsEl.innerHTML = ordered.map((signal) => {
    const freshness = signalFreshness(signal.detected_at);
    return `
    <article class="signal-card compact">
      <div class="signal-row-main">
        <strong class="signal-title">${escapeHtml(signal.event.title)}</strong>
        <div class="signal-tags">
          <span class="mini-badge">${escapeHtml(signal.tier || "watch")}</span>
          <span class="flow-pill info">score ${Number(signal.score).toFixed(2)}</span>
          <span class="flow-pill ${freshness.className}">${escapeHtml(freshness.label)}</span>
        </div>
      </div>
      <div class="signal-row-subtle">
        ${escapeHtml(signal.event.platform)} · ${escapeHtml(signal.event.market_id)} · ${escapeHtml(signal.source_label || signal.event.source)} · ${formatTimestamp(signal.detected_at)}
      </div>
      <div class="signal-why">${escapeHtml(summarizeReason(signal.reason))}</div>
    </article>
  `;
  }).join("");
}

function collapseEvents(events) {
  const order = [];
  const groups = new Map();

  for (const event of events || []) {
    const key = [
      event.source,
      event.platform,
      event.market_id,
      event.event_kind,
      event.timestamp,
      event.trade_size,
      event.yes_price,
      event.volume,
    ].join("|");

    if (!groups.has(key)) {
      groups.set(key, { event, count: 1 });
      order.push(key);
    } else {
      groups.get(key).count += 1;
    }
  }

  return order.map((key) => groups.get(key));
}

function renderActivity(activity, telemetry = {}, config = {}) {
  if (!activity.length) {
    const mode = config.active_mode || "unknown";
    const windowMinutes = telemetry.freshness_window_minutes;
    const latestAge = formatAgeFromNow(telemetry.latest_event_at);
    const tickerCount = Number(telemetry.subscribed_tickers || 0);

    if (mode === "live" && windowMinutes) {
      activityEl.innerHTML = `<div class="empty">No fresh events in the last ${windowMinutes} minutes. Last stored event: ${escapeHtml(latestAge)}. Subscribed tickers: ${tickerCount}.</div>`;
    } else {
      activityEl.innerHTML = `<div class="empty">No live flow yet. Simulation or real feeds will start filling this stream.</div>`;
    }
    return;
  }

  const collapsed = collapseEvents(activity);

  activityEl.innerHTML = collapsed.map(({ event: item, count }) => {
    const freshness = flowFreshness(item.timestamp);
    const price = item.yes_price != null ? `<span class="flow-val">${formatPrice(item.yes_price)}</span>` : "";
    const vol = item.volume != null ? `<span class="flow-muted">vol ${formatVolume(item.volume)}</span>` : "";
    const side = item.trade_side ? `<span class="flow-muted">${escapeHtml(item.trade_side)}</span>` : "";
    const kind = item.event_kind === "trade" ? `<span class="flow-kind trade">T</span>` : `<span class="flow-kind quote">Q</span>`;
    const dup = count > 1 ? `<span class="flow-dup">×${count}</span>` : "";
    const spark = sparklineSvg(item.market_id);
    const age = `<span class="flow-age ${freshness.className}">${escapeHtml(freshness.label)}</span>`;

    return `<div class="flow-row">${kind}${dup}<span class="flow-mid">${escapeHtml(item.market_id)}</span>${price}${vol}${side}${spark}${age}</div>`;
  }).join("");
}

function renderFeeds(state) {
  const feeds = state.feeds || {};
  const config = state.config || {};
  const summary = state.summary || {};
  const activity = state.activity || [];
  const telemetry = state.telemetry || {};

  const pills = [];

  const mode = config.active_mode || "none";
  const modePillClass = mode === "live" ? "live" : "info";
  pills.push(`<span class="status-pill ${modePillClass}">mode: ${escapeHtml(mode)}</span>`);

  const freshnessWindow = telemetry.freshness_window_minutes;
  if (freshnessWindow) {
    pills.push(`<span class="status-pill info">window: ${freshnessWindow}m</span>`);
  }

  const latestEventAge = formatAgeFromNow(telemetry.latest_event_at);
  const latestEventClass = latestEventAge === "unknown" ? "warn" : (latestEventAge.includes("h") ? "danger" : "ok");
  pills.push(`<span class="status-pill ${latestEventClass}">last event: ${escapeHtml(latestEventAge)}</span>`);

  const kalshiAge = formatAgeFromNow(telemetry.kalshi_last_event_at);
  const kalshiAgeClass = kalshiAge === "unknown" ? "warn" : (kalshiAge.includes("h") ? "danger" : "ok");
  pills.push(`<span class="status-pill ${kalshiAgeClass}">kalshi seen: ${escapeHtml(kalshiAge)}</span>`);

  pills.push(`<span class="status-pill info">tickers: ${Number(telemetry.subscribed_tickers || 0)}</span>`);

  if (activity.length) {
    const latestTs = activity[0]?.timestamp;
    const ageMinutes = latestTs ? Math.max(0, Math.floor((Date.now() - new Date(latestTs).getTime()) / 60000)) : null;
    const freshnessClass = ageMinutes !== null && ageMinutes <= 5 ? "ok" : ageMinutes !== null && ageMinutes <= 15 ? "warn" : "danger";
    const freshnessLabel = ageMinutes === null ? "freshness: unknown" : `freshness: ${ageMinutes}m`;
    pills.push(`<span class="status-pill ${freshnessClass}">${escapeHtml(freshnessLabel)}</span>`);
  } else {
    pills.push('<span class="status-pill warn">freshness: no recent events</span>');
  }

  const sourceEntries = Object.entries(summary.sources || {});
  for (const [source, count] of sourceEntries) {
    pills.push(`<span class="status-pill info">${escapeHtml(source)} ${Number(count)}</span>`);
  }

  for (const [name, feed] of Object.entries(feeds)) {
    // Simulation is always suppressed in live mode — skip pill entirely.
    if (name === "simulation" && mode === "live") continue;

    if (name === "discord") {
      const detail = String(feed.detail || "");
      const isDisabled = !feed.running || detail.toLowerCase().includes("disabled");
      const isDefault = detail.toLowerCase().includes("default");
      const discordClass = isDisabled ? "warn" : (isDefault ? "info" : "ok");
      const discordLabel = isDisabled ? "discord: disabled" : (isDefault ? "discord: default webhook" : "discord: active");
      pills.push(`<span class="status-pill ${discordClass}">${escapeHtml(discordLabel)}</span>`);
      continue;
    }

    const statusClass = feed.running ? "ok" : (String(feed.detail || "").toLowerCase().includes("error") ? "danger" : "warn");
    const dotClass = feed.running ? "dot ok" : "dot";
    const statusText = feed.running ? "running" : "idle";
    pills.push(
      `<span class="status-pill ${statusClass}"><span class="${dotClass}"></span>${escapeHtml(name)}: ${escapeHtml(statusText)}</span>`,
    );
  }

  feedsEl.innerHTML = pills.join("");
}

function renderMarkets(markets, telemetry = {}, config = {}) {
  const head = `
    <div class="market-head">
      <div>Market</div>
      <div>Platform</div>
      <div>Source</div>
      <div>Event</div>
      <div>Yes</div>
      <div>Volume</div>
      <div>Seen</div>
    </div>
  `;

  if (!markets.length) {
    const mode = config.active_mode || "unknown";
    const windowMinutes = telemetry.freshness_window_minutes;
    const latestAge = formatAgeFromNow(telemetry.latest_event_at);
    if (mode === "live" && windowMinutes) {
      marketsEl.innerHTML = `${head}<div class="empty">No market snapshots inside the ${windowMinutes}m live window. Last stored market event: ${escapeHtml(latestAge)}.</div>`;
    } else {
      marketsEl.innerHTML = `${head}<div class="empty">No market events yet.</div>`;
    }
    return;
  }

  const collapsed = collapseEvents(markets);

  const rows = collapsed.map(({ event: market, count }) => `
    <div class="market-row">
      <div class="market-name">
        <strong class="market-title">${escapeHtml(market.title)}</strong>
        <span class="market-id">${escapeHtml(market.market_id)} • ${escapeHtml(market.topic || "general")}</span>
      </div>
      <div class="market-cell">${escapeHtml(market.platform)}</div>
      <div class="market-cell">${escapeHtml(market.source)}</div>
      <div class="market-cell">${escapeHtml(market.event_kind || "quote")} ${count > 1 ? `• x${count}` : ""} • ${escapeHtml(market.live ? "live" : "demo")}</div>
      <div class="market-cell">${formatPrice(market.yes_price)}</div>
      <div class="market-cell">${formatVolume(market.volume)}</div>
      <div class="market-cell">${formatTimestamp(market.timestamp)}</div>
    </div>
  `).join("");

  marketsEl.innerHTML = head + rows;
}

function renderTickerList(markets) {
  if (!tickerListEl) return;

  trackedTickers = Array.isArray(markets) ? [...markets] : [];

  if (!trackedTickers.length) {
    tickerListEl.innerHTML = `<div class="empty">No Kalshi tickers tracked yet.</div>`;
    return;
  }

  tickerListEl.innerHTML = trackedTickers
    .map((ticker) => `
      <div class="ticker-chip">
        <span class="ticker-code">${escapeHtml(ticker)}</span>
        <button class="ticker-remove" type="button" data-ticker="${escapeHtml(ticker)}">Remove</button>
      </div>
    `)
    .join("");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

async function refresh() {
  try {
    const state = await fetchState();
    lastDashboardState = state;
    recordPriceHistory(state.activity || []);
    renderMetrics(state);
    renderModeUI(state.config || {});
    renderSignals(state.signals || []);
    renderActivity(state.activity || [], state.telemetry || {}, state.config || {});
    renderFeeds(state);
    renderMarkets(state.markets || [], state.telemetry || {}, state.config || {});
    renderTickerList(state.config?.kalshi_markets || []);
  } catch (error) {
    signalsEl.innerHTML = `<div class="empty">${escapeHtml(error.message)}</div>`;
  }
}

if (demoButton) {
  demoButton.addEventListener("click", async () => {
    await fetch("/api/demo/spike", { method: "POST" });
    await refresh();
  });
}

if (tickerForm) {
  tickerForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (tickerMutationInFlight) return;

    const ticker = normalizeTicker(tickerInput.value);

    if (!ticker) {
      setTickerMessage("Ticker is required.", true);
      return;
    }

    if (!isValidTickerFormat(ticker)) {
      setTickerMessage("Ticker format is invalid. Use letters, numbers, and hyphens.", true);
      return;
    }

    setTickerMutationBusy(true);
    setTickerMessage(`Adding ${ticker}...`);

    const alreadyTracked = trackedTickers.includes(ticker);

    try {
      const markets = await postTicker("/api/kalshi/markets", ticker);
      renderTickerList(markets);
      tickerInput.value = "";
      setTickerMessage(alreadyTracked ? `Already tracking ${ticker}.` : `Added ${ticker}.`);
      await refresh();
    } catch (error) {
      setTickerMessage(error.message || "Failed to add ticker.", true);
    } finally {
      setTickerMutationBusy(false);
    }
  });
}

if (tickerListEl) {
  tickerListEl.addEventListener("click", async (event) => {
    const button = event.target.closest(".ticker-remove");
    if (!button || tickerMutationInFlight) return;

    const ticker = normalizeTicker(button.dataset.ticker);
    if (!ticker) return;

    setTickerMutationBusy(true);
    setTickerMessage(`Removing ${ticker}...`);

    try {
      const markets = await postTicker("/api/kalshi/markets/remove", ticker);
      renderTickerList(markets);
      setTickerMessage(`Removed ${ticker}.`);
      await refresh();
    } catch (error) {
      setTickerMessage(error.message || "Failed to remove ticker.", true);
    } finally {
      setTickerMutationBusy(false);
    }
  });
}

if (signalSortEl) {
  signalSortEl.addEventListener("change", () => {
    signalSortMode = signalSortEl.value === "score" ? "score" : "newest";
    renderSignals(lastDashboardState?.signals || []);
  });
}

if (signalLatestToggleEl) {
  signalLatestToggleEl.addEventListener("click", () => {
    signalLatestOnly = !signalLatestOnly;
    signalLatestToggleEl.setAttribute("aria-pressed", signalLatestOnly ? "true" : "false");
    signalLatestToggleEl.classList.toggle("active", signalLatestOnly);
    renderSignals(lastDashboardState?.signals || []);
  });
}

if (categoryForm) {
  categoryForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const q = (categoryInput?.value || "").trim();
    if (!q) return;

    categoryMessageEl.textContent = "Searching…";
    categoryResultsEl.innerHTML = "";

    try {
      const resp = await fetch(`/api/kalshi/categories?q=${encodeURIComponent(q)}&limit=20`);
      const data = await resp.json();
      const results = data.results || [];

      if (!results.length) {
        categoryMessageEl.textContent = `No open markets found for "${q}".`;
        return;
      }

      categoryMessageEl.textContent = `${results.length} event(s) found. Click a series slug to track it.`;
      categoryResultsEl.innerHTML = results.map((r) => `
        <div class="category-result-row">
          <div class="category-result-meta">
            <span class="category-result-title">${escapeHtml(r.title)}</span>
            <span class="category-result-cat">${escapeHtml(r.category)}</span>
          </div>
          <div class="category-result-tickers">
            ${r.series_ticker ? `<button class="category-add-btn" data-ticker="${escapeHtml(r.series_ticker)}" title="Add ${escapeHtml(r.series_ticker)} to watched tickers">${escapeHtml(r.series_ticker)} +</button>` : ""}
          </div>
        </div>
      `).join("");

      // Wire up add buttons
      categoryResultsEl.querySelectorAll(".category-add-btn").forEach((btn) => {
        btn.addEventListener("click", async () => {
          const ticker = btn.dataset.ticker;
          btn.disabled = true;
          btn.textContent = "Adding…";
          try {
            const resp = await fetch("/api/kalshi/markets", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ ticker }),
            });
            const result = await resp.json();
            if (result.ok) {
              btn.textContent = `${ticker} ✓`;
              categoryMessageEl.textContent = `Added ${ticker} to tracked tickers.`;
            } else {
              btn.textContent = `${ticker} +`;
              btn.disabled = false;
              categoryMessageEl.textContent = result.error || "Failed to add ticker.";
            }
          } catch {
            btn.textContent = `${ticker} +`;
            btn.disabled = false;
            categoryMessageEl.textContent = "Network error.";
          }
        });
      });
    } catch {
      categoryMessageEl.textContent = "Search failed — check network.";
    }
  });
}

refresh();
setInterval(refresh, 3000);
