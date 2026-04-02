const metricsEl = document.querySelector("#metrics");
const signalsEl = document.querySelector("#signals");
const activityEl = document.querySelector("#activity");
const feedsEl = document.querySelector("#feeds");
const marketsEl = document.querySelector("#markets");
const demoButton = document.querySelector("#demo-spike");

async function fetchState() {
  const response = await fetch("/api/state");
  if (!response.ok) {
    throw new Error("Failed to load dashboard state");
  }
  return response.json();
}

function formatPrice(value) {
  if (value === null || value === undefined) return "n/a";
  return `${(value * 100).toFixed(1)}c`;
}

function formatTimestamp(value) {
  const date = new Date(value);
  return date.toLocaleTimeString([], { hour: "numeric", minute: "2-digit", second: "2-digit" });
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
  const routeCount = (config.discord_routes || []).length;

  metricsEl.innerHTML = `
    <article class="metric-card">
      <div class="metric-label">Tracked Markets</div>
      <div class="metric-value">${markets.length}</div>
      <div class="metric-subtle">latest 50 kept in memory</div>
    </article>
    <article class="metric-card">
      <div class="metric-label">Recent Signals</div>
      <div class="metric-value">${signals.length}</div>
      <div class="metric-subtle">top 25 detector hits</div>
    </article>
    <article class="metric-card">
      <div class="metric-label">Live Flow</div>
      <div class="metric-value">${summary.live_events || 0}</div>
      <div class="metric-subtle">recent live events in memory</div>
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

function renderSignals(signals) {
  if (!signals.length) {
    signalsEl.innerHTML = `<div class="empty">No spikes yet. Keep the page open or trigger the demo event.</div>`;
    return;
  }

  signalsEl.innerHTML = signals.map((signal) => `
    <article class="signal-card">
      <div class="signal-top">
        <strong class="signal-title">${escapeHtml(signal.event.title)}</strong>
        <div class="signal-tags">
          <span class="mini-badge">${escapeHtml(signal.tier || "watch")}</span>
          <span class="signal-score">score ${Number(signal.score).toFixed(2)}</span>
        </div>
      </div>
      <div class="signal-meta">
        ${escapeHtml(signal.event.platform)} • ${escapeHtml(signal.event.market_id)} • ${escapeHtml(signal.source_label || signal.event.source)}<br>
        ${escapeHtml(signal.topic || signal.event.topic || "general")} • ${escapeHtml(signal.event.event_kind || "quote")}<br>
        ${escapeHtml(signal.reason)}<br>
        ${formatTimestamp(signal.detected_at)}
      </div>
    </article>
  `).join("");
}

function renderActivity(activity) {
  if (!activity.length) {
    activityEl.innerHTML = `<div class="empty">No live flow yet. Simulation or real feeds will start filling this stream.</div>`;
    return;
  }

  activityEl.innerHTML = activity.map((item) => `
    <article class="flow-card">
      <div class="flow-top">
        <strong class="flow-title">${escapeHtml(item.title)}</strong>
        <span class="mini-badge">${escapeHtml(item.live ? "live" : "demo")}</span>
      </div>
      <div class="flow-meta">
        ${escapeHtml(item.platform)} • ${escapeHtml(item.source)} • ${escapeHtml(item.event_kind || "quote")}<br>
        ${escapeHtml(item.topic || "general")} • yes ${formatPrice(item.yes_price)} • vol ${formatVolume(item.volume)}<br>
        ${item.trade_size === null || item.trade_size === undefined ? "no trade size" : `trade ${formatVolume(item.trade_size)}`} • ${formatTimestamp(item.timestamp)}
      </div>
    </article>
  `).join("");
}

function renderFeeds(feeds) {
  const entries = Object.entries(feeds || {});
  if (!entries.length) {
    feedsEl.innerHTML = `<div class="empty">No feed adapters have reported status yet.</div>`;
    return;
  }

  feedsEl.innerHTML = entries.map(([name, feed]) => `
    <article class="feed-card">
      <div class="feed-top">
        <strong class="feed-title">${escapeHtml(name)}</strong>
        <span class="feed-indicator">
          <span class="dot ${feed.running ? "ok" : ""}"></span>
          <span class="status-text">${feed.running ? "running" : "idle"}</span>
        </span>
      </div>
      <div class="feed-meta">${escapeHtml(feed.detail || "No detail yet")}</div>
    </article>
  `).join("");
}

function renderMarkets(markets) {
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
    marketsEl.innerHTML = `${head}<div class="empty">No market events yet.</div>`;
    return;
  }

  const rows = markets.map((market) => `
    <div class="market-row">
      <div class="market-name">
        <strong class="market-title">${escapeHtml(market.title)}</strong>
        <span class="market-id">${escapeHtml(market.market_id)} • ${escapeHtml(market.topic || "general")}</span>
      </div>
      <div class="market-cell">${escapeHtml(market.platform)}</div>
      <div class="market-cell">${escapeHtml(market.source)}</div>
      <div class="market-cell">${escapeHtml(market.event_kind || "quote")} • ${escapeHtml(market.live ? "live" : "demo")}</div>
      <div class="market-cell">${formatPrice(market.yes_price)}</div>
      <div class="market-cell">${formatVolume(market.volume)}</div>
      <div class="market-cell">${formatTimestamp(market.timestamp)}</div>
    </div>
  `).join("");

  marketsEl.innerHTML = head + rows;
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
    renderMetrics(state);
    renderSignals(state.signals || []);
    renderActivity(state.activity || []);
    renderFeeds(state.feeds || {});
    renderMarkets(state.markets || []);
  } catch (error) {
    signalsEl.innerHTML = `<div class="empty">${escapeHtml(error.message)}</div>`;
  }
}

demoButton.addEventListener("click", async () => {
  await fetch("/api/demo/spike", { method: "POST" });
  await refresh();
});

refresh();
setInterval(refresh, 3000);
