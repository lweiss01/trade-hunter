const metricsEl = document.querySelector("#metrics");
const signalsEl = document.querySelector("#signals");
const topicFilterRowEl = document.querySelector("#topic-filter-row");
const whatMattersNowEl = document.querySelector("#what-matters-now");
const selectedSignalWorkbenchEl = document.querySelector("#selected-signal-workbench");
const signalSortEl = document.querySelector("#signal-sort");
const signalLatestToggleEl = document.querySelector("#signal-latest-toggle");
const activityEl = document.querySelector("#activity");
const feedsEl = document.querySelector("#feeds");
const marketsEl = document.querySelector("#markets");
const demoButton = document.querySelector("#demo-spike");
const demoPanel = document.querySelector("#demo-panel");
const modeBadgeEl = document.querySelector("#mode-badge");
const settingsToggleEl = document.querySelector("#settings-toggle");
const navTabEls = Array.from(document.querySelectorAll(".nav-tab"));
const pageViewEls = Array.from(document.querySelectorAll("[data-page-view]"));
const tickerForm = document.querySelector("#ticker-form");
const tickerInput = document.querySelector("#ticker-input");
const tickerListEl = document.querySelector("#ticker-list");
const tickerMessageEl = document.querySelector("#ticker-message");
const tickerAddButton = document.querySelector("#ticker-add");
const categoryForm = document.querySelector("#category-form");
const categoryShortcutsEl = document.querySelector("#category-shortcuts");
const categoryInput = document.querySelector("#category-input");
const categoryResultsEl = document.querySelector("#category-results");
const categoryMessageEl = document.querySelector("#category-message");
const tuningAdvisorEl = document.querySelector("#tuning-advisor");
const settingsLoadStatusEl = document.querySelector("#settings-load-status");
const settingEnableSimulationEl = document.querySelector("#setting-enable-simulation");
const settingQuietModeEl = document.querySelector("#setting-quiet-mode");
const settingEnableKalshiEl = document.querySelector("#setting-enable-kalshi");
const settingKalshiApiKeyIdEl = document.querySelector("#setting-kalshi-api-key-id");
const settingKalshiPrivateKeyPathEl = document.querySelector("#setting-kalshi-private-key-path");
const settingKalshiMarketsEl = document.querySelector("#setting-kalshi-markets");
const settingDiscordAnalystMinConfidenceEl = document.querySelector("#setting-discord-analyst-min-confidence");
const settingDiscordAnalystFollowupEl = document.querySelector("#setting-discord-analyst-followup");
const settingDiscordWebhookUrlEl = document.querySelector("#setting-discord-webhook-url");
const settingDiscordAlertModeEl = document.querySelector("#setting-discord-alert-mode");
const settingDiscordRouteCryptoEl = document.querySelector("#setting-discord-route-crypto");
const settingDiscordRouteMacroEl = document.querySelector("#setting-discord-route-macro");
const settingDiscordRouteElectionsEl = document.querySelector("#setting-discord-route-elections");
const settingIngestApiTokenEl = document.querySelector("#setting-ingest-api-token");
const settingPolyalerthubTokenEl = document.querySelector("#setting-polyalerthub-token");
const settingSpikeMinVolumeDeltaEl = document.querySelector("#setting-spike-min-volume-delta");
const settingSpikeMinPriceMoveEl = document.querySelector("#setting-spike-min-price-move");
const settingSpikeScoreThresholdEl = document.querySelector("#setting-spike-score-threshold");
const settingSpikeBaselinePointsEl = document.querySelector("#setting-spike-baseline-points");
const settingSpikeCooldownSecondsEl = document.querySelector("#setting-spike-cooldown-seconds");
const settingRetentionDaysEl = document.querySelector("#setting-retention-days");
const settingAppHostEl = document.querySelector("#setting-app-host");
const settingAppPortEl = document.querySelector("#setting-app-port");
const settingsStatusCoreEl = document.querySelector("#settings-status-core");
const settingsStatusKalshiEl = document.querySelector("#settings-status-kalshi");
const settingsStatusAnalystEl = document.querySelector("#settings-status-analyst");
const settingsStatusDiscordEl = document.querySelector("#settings-status-discord");
const settingsStatusIngestEl = document.querySelector("#settings-status-ingest");
const settingsStatusDetectorEl = document.querySelector("#settings-status-detector");
const settingsStatusStorageEl = document.querySelector("#settings-status-storage");
const settingsSaveButtonEl = document.querySelector("#settings-save-btn");
const settingsSaveStatusEl = document.querySelector("#settings-save-status");

const editableSettingsControls = [
  settingEnableSimulationEl,
  settingQuietModeEl,
  settingEnableKalshiEl,
  settingDiscordAnalystMinConfidenceEl,
  settingDiscordAnalystFollowupEl,
  settingDiscordAlertModeEl,
  settingSpikeMinVolumeDeltaEl,
  settingSpikeMinPriceMoveEl,
  settingSpikeScoreThresholdEl,
  settingSpikeBaselinePointsEl,
  settingSpikeCooldownSecondsEl,
  settingRetentionDaysEl,
  settingAppHostEl,
  settingAppPortEl,
].filter(Boolean);

const readOnlySettingsControls = [
  settingKalshiApiKeyIdEl,
  settingKalshiPrivateKeyPathEl,
  settingKalshiMarketsEl,
  settingDiscordWebhookUrlEl,
  settingDiscordRouteCryptoEl,
  settingDiscordRouteMacroEl,
  settingDiscordRouteElectionsEl,
  settingIngestApiTokenEl,
  settingPolyalerthubTokenEl,
].filter(Boolean);

let tickerMutationInFlight = false;
let tuningApplyInFlight = false;
let trackedTickers = [];
let signalSortMode = "newest";
let signalLatestOnly = false;
let activeSignalTopic = "all";
let selectedSignalKey = null;
let selectedMarketId = null;
let currentPage = "dashboard";
let lastDashboardState = null;
let lastSettingsState = null;
let settingsSaveInFlight = false;

// Per-market price history for sparklines (last 20 yes_price values)
const priceHistory = new Map();
const SPARK_MAX = 20;
const SIGNAL_TOPICS = [
  ["all", "All"],
  ["macro", "Macro"],
  ["crypto", "Crypto"],
  ["elections", "Elections"],
  ["geopolitics", "Geopolitics"],
  ["sports", "Sports"],
  ["general", "General"],
];

function setActivePage(page) {
  currentPage = page;

  pageViewEls.forEach((view) => {
    const isActive = view.dataset.pageView === page;
    view.hidden = !isActive;
    view.classList.toggle("active", isActive);
  });

  navTabEls.forEach((tab) => {
    const isActive = tab.dataset.page === page;
    tab.classList.toggle("active", isActive);
    tab.setAttribute("aria-selected", isActive ? "true" : "false");
  });

  if (settingsToggleEl) {
    settingsToggleEl.classList.toggle("active", page === "settings");
    settingsToggleEl.setAttribute("aria-pressed", page === "settings" ? "true" : "false");
  }
}

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

async function fetchSettings() {
  const response = await fetch("/api/settings");
  if (!response.ok) {
    throw new Error("Failed to load settings");
  }
  return response.json();
}

async function saveSettings(payload) {
  const response = await fetch("/api/settings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ settings: payload }),
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Failed to save settings");
  }

  return data;
}

function setSettingsControlsEditable(isEditable) {
  editableSettingsControls.forEach((control) => {
    control.disabled = !isEditable || settingsSaveInFlight;
  });

  readOnlySettingsControls.forEach((control) => {
    control.disabled = true;
  });

  if (settingsSaveButtonEl) {
    settingsSaveButtonEl.disabled = !isEditable || settingsSaveInFlight;
  }
}

function setSettingsSaveStatus(message, tone = "") {
  if (!settingsSaveStatusEl) return;
  settingsSaveStatusEl.className = `settings-save-status ${tone}`.trim();
  settingsSaveStatusEl.textContent = message;
}

function collectSettingsPayload() {
  return {
    enable_simulation: Boolean(settingEnableSimulationEl?.checked),
    quiet_mode: Boolean(settingQuietModeEl?.checked),
    enable_kalshi: Boolean(settingEnableKalshiEl?.checked),
    discord_analyst_min_confidence: String(settingDiscordAnalystMinConfidenceEl?.value || "medium"),
    discord_analyst_followup: Boolean(settingDiscordAnalystFollowupEl?.checked),
    discord_alert_mode: String(settingDiscordAlertModeEl?.value || "all"),
    spike_min_volume_delta: Number(settingSpikeMinVolumeDeltaEl?.value || 0),
    spike_min_price_move: Number(settingSpikeMinPriceMoveEl?.value || 0),
    spike_score_threshold: Number(settingSpikeScoreThresholdEl?.value || 0),
    spike_baseline_points: Number(settingSpikeBaselinePointsEl?.value || 0),
    spike_cooldown_seconds: Number(settingSpikeCooldownSecondsEl?.value || 0),
    retention_days: Number(settingRetentionDaysEl?.value || 0),
    host: String(settingAppHostEl?.value || "").trim(),
    port: Number(settingAppPortEl?.value || 0),
  };
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
  const mode = String(config?.active_mode || "none").toLowerCase();
  const isLive = mode === "live";
  const label = isLive ? "LIVE" : mode === "simulation" ? "SIM" : mode.toUpperCase();

  if (modeBadgeEl) {
    modeBadgeEl.className = `mode-badge ${isLive ? "live" : "sim"}`;
    modeBadgeEl.innerHTML = `${isLive ? '<span class="live-dot"></span>' : ""}${escapeHtml(label)}`;
  }

  if (demoPanel) {
    demoPanel.hidden = mode !== "simulation";
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
      .querySelectorAll(".ticker-remove, .prune-dead-btn")
      .forEach((button) => {
        button.disabled = isBusy;
      });
  }
}

function setSettingsStatus(el, tone, label) {
  if (!el) return;
  el.className = `settings-status ${tone}`;
  el.textContent = label;
}

function formatPresenceLabel(isPresent, configuredLabel = "configured") {
  return isPresent ? configuredLabel : "not set";
}

function renderSettings(settingsPayload) {
  const settings = settingsPayload?.settings || {};
  const presence = settings.presence || {};
  lastSettingsState = settingsPayload || null;

  if (settingsLoadStatusEl) {
    settingsLoadStatusEl.textContent = "live editable";
  }

  setSettingsControlsEditable(true);

  if (settingEnableSimulationEl) settingEnableSimulationEl.checked = Boolean(settings.enable_simulation);
  if (settingQuietModeEl) settingQuietModeEl.checked = Boolean(settings.quiet_mode);
  if (settingEnableKalshiEl) settingEnableKalshiEl.checked = Boolean(settings.enable_kalshi);
  if (settingKalshiApiKeyIdEl) settingKalshiApiKeyIdEl.value = formatPresenceLabel(presence.kalshi_api_key_id);
  if (settingKalshiPrivateKeyPathEl) settingKalshiPrivateKeyPathEl.value = formatPresenceLabel(presence.kalshi_private_key_path);
  if (settingKalshiMarketsEl) settingKalshiMarketsEl.value = (settings.kalshi_markets || []).join(", ") || "none tracked";
  if (settingDiscordAnalystMinConfidenceEl) settingDiscordAnalystMinConfidenceEl.value = settings.discord_analyst_min_confidence || "medium";
  if (settingDiscordAnalystFollowupEl) settingDiscordAnalystFollowupEl.checked = Boolean(settings.discord_analyst_followup);
  if (settingDiscordWebhookUrlEl) settingDiscordWebhookUrlEl.value = formatPresenceLabel(presence.discord_webhook_url);
  if (settingDiscordAlertModeEl) settingDiscordAlertModeEl.value = settings.discord_alert_mode || "all";
  if (settingDiscordRouteCryptoEl) settingDiscordRouteCryptoEl.value = presence.discord_webhook_routes?.includes("crypto") ? "configured" : "not set";
  if (settingDiscordRouteMacroEl) settingDiscordRouteMacroEl.value = presence.discord_webhook_routes?.includes("macro") ? "configured" : "not set";
  if (settingDiscordRouteElectionsEl) settingDiscordRouteElectionsEl.value = presence.discord_webhook_routes?.includes("elections") ? "configured" : "not set";
  if (settingIngestApiTokenEl) settingIngestApiTokenEl.value = formatPresenceLabel(presence.ingest_api_token);
  if (settingPolyalerthubTokenEl) settingPolyalerthubTokenEl.value = formatPresenceLabel(presence.polyalerthub_token);
  if (settingSpikeMinVolumeDeltaEl) settingSpikeMinVolumeDeltaEl.value = settings.spike_min_volume_delta ?? "";
  if (settingSpikeMinPriceMoveEl) settingSpikeMinPriceMoveEl.value = settings.spike_min_price_move ?? "";
  if (settingSpikeScoreThresholdEl) settingSpikeScoreThresholdEl.value = settings.spike_score_threshold ?? "";
  if (settingSpikeBaselinePointsEl) settingSpikeBaselinePointsEl.value = settings.spike_baseline_points ?? "";
  if (settingSpikeCooldownSecondsEl) settingSpikeCooldownSecondsEl.value = settings.spike_cooldown_seconds ?? "";
  if (settingRetentionDaysEl) settingRetentionDaysEl.value = settings.retention_days ?? "";
  if (settingAppHostEl) settingAppHostEl.value = settings.host || "";
  if (settingAppPortEl) settingAppPortEl.value = settings.port ?? "";

  setSettingsStatus(settingsStatusCoreEl, "configured", "configured");
  setSettingsStatus(settingsStatusAnalystEl, "configured", "configured");
  setSettingsStatus(settingsStatusDetectorEl, "configured", "configured");
  setSettingsStatus(settingsStatusStorageEl, "configured", "configured");

  if (!settings.enable_kalshi) {
    setSettingsStatus(settingsStatusKalshiEl, "disabled", "disabled");
  } else if (presence.kalshi_api_key_id && presence.kalshi_private_key_path) {
    setSettingsStatus(settingsStatusKalshiEl, "configured", "configured");
  } else {
    setSettingsStatus(settingsStatusKalshiEl, "missing", "missing key");
  }

  if (presence.discord_webhook_url || (presence.discord_webhook_routes || []).length) {
    setSettingsStatus(settingsStatusDiscordEl, "configured", "configured");
  } else {
    setSettingsStatus(settingsStatusDiscordEl, "disabled", "disabled");
  }

  if (presence.ingest_api_token || presence.polyalerthub_token) {
    setSettingsStatus(settingsStatusIngestEl, "configured", "configured");
  } else {
    setSettingsStatus(settingsStatusIngestEl, "missing", "missing key");
  }

  if (!settingsSaveInFlight) {
    setSettingsSaveStatus("Loaded from .env. Save to persist edits. Restart required to apply.");
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
  const routeCount = Object.keys(config.discord_routes || {}).length;
  const liveWindow = telemetry.freshness_window_minutes;
  const windowLabel = liveWindow ? `in ${liveWindow}m window` : "active";

  const stats = [
    { label: "tracked markets",  value: markets.length,              sub: windowLabel },
    { label: "signals",          value: signals.length,              sub: windowLabel },
    { label: "live flow events", value: (state.activity || []).length, sub: windowLabel },
    { label: "trade events",     value: summary.trade_events || 0,   sub: windowLabel },
    { label: "active feeds",     value: Object.keys(feeds).length,   sub: null },
    { label: "discord routes",   value: routeCount,                  sub: routeCount ? null : "default or disabled" },
  ];

  metricsEl.innerHTML = `<div class="metric-strip">${
    stats.map(s => {
      const sub = s.sub ? `<span class="metric-chip-sub">${s.sub}</span>` : "";
      return `<span class="metric-chip"><span class="metric-chip-val">${s.value}</span><span class="metric-chip-label">${s.label}</span>${sub}</span>`;
    }).join("")
  }</div>`;
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

function getSignalKey(signal) {
  return `${signal?.event?.market_id || "unknown-market"}|${signal?.detected_at || "unknown-time"}`;
}

function findBestSignalForMarket(signals, marketId) {
  return (signals || []).find((signal) => signal?.event?.market_id === marketId) || null;
}

function normalizeTopic(value) {
  const topic = String(value || "general").trim().toLowerCase();
  return SIGNAL_TOPICS.some(([key]) => key === topic) ? topic : "general";
}

function getSignalTopicCounts(signals) {
  const counts = Object.fromEntries(SIGNAL_TOPICS.map(([key]) => [key, 0]));
  for (const signal of signals || []) {
    const topic = normalizeTopic(signal?.event?.topic || signal?.topic);
    counts[topic] += 1;
    counts.all += 1;
  }
  return counts;
}

function renderTopicFilterRow(signals) {
  if (!topicFilterRowEl) return;
  const counts = getSignalTopicCounts(signals || []);

  topicFilterRowEl.innerHTML = SIGNAL_TOPICS.map(([key, label]) => {
    const isActive = activeSignalTopic === key;
    return `<button class="topic-chip ${isActive ? "active" : ""}" type="button" data-topic="${key}" aria-pressed="${isActive ? "true" : "false"}">${label} <span class="topic-count">${counts[key] || 0}</span></button>`;
  }).join("");
}

function normalizeSignals(signals) {
  let result = [...signals];

  if (activeSignalTopic !== "all") {
    result = result.filter((signal) => normalizeTopic(signal?.event?.topic || signal?.topic) === activeSignalTopic);
  }

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

function formatThresholdValue(key, value) {
  if (value == null) return "n/a";
  if (key === "min_price_move") return `${(Number(value) * 100).toFixed(1)}%`;
  if (key === "score_threshold") return Number(value).toFixed(2);
  return Number(value).toFixed(0);
}

function renderWhatMattersNow(signal) {
  if (!whatMattersNowEl) return;

  if (!signal) {
    whatMattersNowEl.innerHTML = "";
    whatMattersNowEl.hidden = true;
    return;
  }

  const freshness = signalFreshness(signal.detected_at);
  const title = signal?.event?.title || signal?.event?.market_id || "Signal";
  const tier = String(signal.tier || "watch");
  const topic = normalizeTopic(signal?.event?.topic || signal?.topic);
  const whyThisMatters = summarizeReason(signal.reason);
  const nextChecks = [];

  if (signal?.event?.volume != null) nextChecks.push(`check liquidity (${formatVolume(signal.event.volume)} vol)`);
  if (signal?.event?.yes_price != null) nextChecks.push(`confirm price context (${formatPrice(signal.event.yes_price)})`);
  nextChecks.push(`review ${topic} context`);

  whatMattersNowEl.hidden = false;
  whatMattersNowEl.innerHTML = `
    <article class="priority-strip">
      <div class="priority-strip-head">
        <span class="priority-kicker">What matters now</span>
        <div class="priority-tags">
          <span class="mini-badge">${escapeHtml(tier)}</span>
          <span class="flow-pill info">score ${Number(signal.score || 0).toFixed(2)}</span>
          <span class="flow-pill ${freshness.className}">${escapeHtml(freshness.label)}</span>
        </div>
      </div>
      <strong class="priority-title">${escapeHtml(title)}</strong>
      <div class="priority-meta">${escapeHtml(signal?.event?.platform || "unknown")} · ${escapeHtml(signal?.event?.market_id || "unknown-market")} · ${escapeHtml(topic)} · ${formatTimestamp(signal.detected_at)}</div>
      <div class="priority-summary"><span class="priority-label">Why this matters</span>${escapeHtml(whyThisMatters)}</div>
      <div class="priority-next"><span class="priority-label">Next checks</span>${nextChecks.map((item) => `<span class="priority-check">${escapeHtml(item)}</span>`).join("")}</div>
    </article>
  `;
}

function renderSelectedSignalWorkbench(signals, activity) {
  if (!selectedSignalWorkbenchEl) return;

  const ordered = signals || [];
  const allActivity = activity || [];

  if (!ordered.length && !selectedMarketId) {
    selectedSignalWorkbenchEl.innerHTML = `<div class="empty">Select a signal or flow row to inspect its full context.</div>`;
    return;
  }

  const selected = ordered.find((signal) => getSignalKey(signal) === selectedSignalKey) || null;

  if (selected) {
    selectedSignalKey = getSignalKey(selected);
    selectedMarketId = selected?.event?.market_id || selectedMarketId;
    selectedMarketId = selected?.event?.market_id || selectedMarketId;

    const relatedActivity = allActivity.filter((item) => item.market_id === selected?.event?.market_id).slice(0, 6);
    const analyst = selected.analyst || null;
    const freshness = signalFreshness(selected.detected_at);
    const liquidityBits = [
      selected?.event?.yes_price != null ? `yes ${formatPrice(selected.event.yes_price)}` : null,
      selected?.event?.volume != null ? `vol ${formatVolume(selected.event.volume)}` : null,
      selected?.event?.trade_size != null ? `trade ${formatVolume(selected.event.trade_size)}` : null,
    ].filter(Boolean);
    const checklist = [
      `confirm catalyst for ${normalizeTopic(selected?.event?.topic || selected?.topic)}`,
      `review latest flow for ${selected?.event?.market_id || "market"}`,
      `check liquidity before action`,
    ];

    selectedSignalWorkbenchEl.innerHTML = `
      <div class="panel-head workbench-head">
        <div>
          <h2>Selected Signal Workbench</h2>
          <div class="workbench-subtitle">List = triage. Detail = investigation.</div>
        </div>
        <div class="priority-tags">
          <span class="mini-badge">${escapeHtml(selected.tier || "watch")}</span>
          <span class="flow-pill info">score ${Number(selected.score || 0).toFixed(2)}</span>
          <span class="flow-pill ${freshness.className}">${escapeHtml(freshness.label)}</span>
        </div>
      </div>
      <div class="workbench-grid">
        <section class="workbench-panel">
          <span class="priority-kicker">Event summary</span>
          <strong class="workbench-title">${escapeHtml(selected?.event?.title || selected?.event?.market_id || "Signal")}</strong>
          <div class="workbench-meta">${escapeHtml(selected?.event?.platform || "unknown")} · ${escapeHtml(selected?.event?.market_id || "unknown-market")} · ${escapeHtml(selected?.source_label || selected?.event?.source || "unknown")} · ${formatTimestamp(selected.detected_at)}</div>
          <p class="workbench-copy">${escapeHtml(selected.reason || "No detector rationale available.")}</p>
          ${analyst ? `<div class="workbench-analyst"><span class="priority-label">Analyst view</span><p class="workbench-copy">${escapeHtml(analyst.rationale || "No analyst rationale available.")}</p></div>` : ""}
        </section>
        <section class="workbench-panel">
          <span class="priority-kicker">Liquidity context</span>
          <div class="workbench-pill-row">${liquidityBits.map((item) => `<span class="priority-check">${escapeHtml(item)}</span>`).join("") || '<span class="empty">No liquidity fields on this signal yet.</span>'}</div>
          <span class="priority-kicker">Research checklist</span>
          <ul class="workbench-list">${checklist.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
        </section>
        <section class="workbench-panel workbench-panel-wide">
          <span class="priority-kicker">Recent market-only flow</span>
          ${relatedActivity.length ? `<div class="workbench-flow">${relatedActivity.map((item) => `<div class="workbench-flow-row"><span class="flow-kind ${item.event_kind === "trade" ? "trade" : "quote"}">${item.event_kind === "trade" ? "T" : "Q"}</span><span class="flow-mid">${escapeHtml(item.market_id || "unknown")}</span><span class="flow-val">${item.yes_price != null ? formatPrice(item.yes_price) : "n/a"}</span><span class="flow-muted">vol ${item.volume != null ? formatVolume(item.volume) : "n/a"}</span><span class="flow-age ${flowFreshness(item.timestamp).className}">${escapeHtml(flowFreshness(item.timestamp).label)}</span></div>`).join("")}</div>` : `<div class="empty">No recent activity matched this signal’s market.</div>`}
        </section>
      </div>
    `;
    return;
  }

  const fallbackActivity = allActivity.filter((item) => item.market_id === selectedMarketId).slice(0, 6);
  const fallbackEvent = fallbackActivity[0] || null;

  selectedSignalKey = null;

  if (!fallbackEvent) {
    selectedSignalWorkbenchEl.innerHTML = `<div class="empty">Select a signal or flow row to inspect its full context.</div>`;
    return;
  }

  const fallbackFreshness = flowFreshness(fallbackEvent.timestamp);
  const fallbackChecks = [
    `review latest flow for ${fallbackEvent.market_id || "market"}`,
    `check whether price movement is backed by trades`,
    `inspect liquidity before action`,
  ];
  const fallbackLiquidity = [
    fallbackEvent.yes_price != null ? `yes ${formatPrice(fallbackEvent.yes_price)}` : null,
    fallbackEvent.volume != null ? `vol ${formatVolume(fallbackEvent.volume)}` : null,
    fallbackEvent.trade_side ? `${fallbackEvent.trade_side}` : null,
  ].filter(Boolean);

  selectedSignalWorkbenchEl.innerHTML = `
    <div class="panel-head workbench-head">
      <div>
        <h2>Selected Signal Workbench</h2>
        <div class="workbench-subtitle">List = triage. Detail = investigation.</div>
      </div>
      <div class="priority-tags">
        <span class="mini-badge">flow-only</span>
        <span class="flow-pill ${fallbackFreshness.className}">${escapeHtml(fallbackFreshness.label)}</span>
      </div>
    </div>
    <div class="workbench-grid">
      <section class="workbench-panel">
        <span class="priority-kicker">Event summary</span>
        <strong class="workbench-title">${escapeHtml(fallbackEvent.title || fallbackEvent.market_id || "Market flow")}</strong>
        <div class="workbench-meta">${escapeHtml(fallbackEvent.platform || "unknown")} · ${escapeHtml(fallbackEvent.market_id || "unknown-market")} · ${escapeHtml(fallbackEvent.source || "unknown")} · ${formatTimestamp(fallbackEvent.timestamp)}</div>
        <p class="workbench-copy">No current signal matches this market. Showing the latest flow context directly so the workbench still supports investigation.</p>
      </section>
      <section class="workbench-panel">
        <span class="priority-kicker">Liquidity context</span>
        <div class="workbench-pill-row">${fallbackLiquidity.map((item) => `<span class="priority-check">${escapeHtml(item)}</span>`).join("") || '<span class="empty">No liquidity fields on this market flow yet.</span>'}</div>
        <span class="priority-kicker">Research checklist</span>
        <ul class="workbench-list">${fallbackChecks.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
      </section>
      <section class="workbench-panel workbench-panel-wide">
        <span class="priority-kicker">Recent market-only flow</span>
        <div class="workbench-flow">${fallbackActivity.map((item) => `<div class="workbench-flow-row"><span class="flow-kind ${item.event_kind === "trade" ? "trade" : "quote"}">${item.event_kind === "trade" ? "T" : "Q"}</span><span class="flow-mid">${escapeHtml(item.market_id || "unknown")}</span><span class="flow-val">${item.yes_price != null ? formatPrice(item.yes_price) : "n/a"}</span><span class="flow-muted">vol ${item.volume != null ? formatVolume(item.volume) : "n/a"}</span><span class="flow-age ${flowFreshness(item.timestamp).className}">${escapeHtml(flowFreshness(item.timestamp).label)}</span></div>`).join("")}</div>
      </section>
    </div>
  `;
}

async function applyRecommendedTuning() {
  if (tuningApplyInFlight) return;
  tuningApplyInFlight = true;
  renderTuningAdvisor(lastDashboardState || {});
  try {
    const response = await fetch("/api/config/apply-tuning", { method: "POST" });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error || "Failed to apply tuning suggestion");
    }
    await refresh();
    const appliedKeys = Object.keys(payload.applied || {});
    if (tuningAdvisorEl && appliedKeys.length) {
      const banner = document.createElement("div");
      banner.className = "tuning-global";
      banner.textContent = `Applied: ${appliedKeys.join(", ")}`;
      tuningAdvisorEl.prepend(banner);
    }
  } catch (error) {
    if (tuningAdvisorEl) {
      const banner = document.createElement("div");
      banner.className = "empty";
      banner.textContent = error.message || "Failed to apply tuning suggestion.";
      tuningAdvisorEl.prepend(banner);
    }
  } finally {
    tuningApplyInFlight = false;
    renderTuningAdvisor(lastDashboardState || {});
  }
}

function renderTuningAdvisor(state) {
  if (!tuningAdvisorEl) return;
  const advisor = state.tuning_advisor || null;
  if (!advisor) {
    tuningAdvisorEl.innerHTML = `<div class="empty">Waiting for enough analysed signals to recommend threshold tweaks.</div>`;
    return;
  }
  if (advisor.pending) {
    tuningAdvisorEl.innerHTML = `<div class="empty">Analysing recent false-positive patterns…</div>`;
    return;
  }
  const recs = advisor.recommendations || [];
  const suggested = advisor.suggested_thresholds || {};
  const applied = state.config?.applied_thresholds || {};
  const suggestedEntries = Object.entries(suggested);
  tuningAdvisorEl.innerHTML = `
    <div class="tuning-summary">${escapeHtml(advisor.summary || "")}</div>
    <div class="tuning-global"><strong>Best next tweak:</strong> ${escapeHtml(advisor.global_recommendation || "")}</div>
    ${recs.length ? `<ul class="tuning-list">${recs.map(r => `<li>${escapeHtml(r)}</li>`).join("")}</ul>` : ""}
    ${suggestedEntries.length ? `
      <div class="tuning-global"><strong>Suggested thresholds:</strong> ${suggestedEntries.map(([key, value]) => `${escapeHtml(key)} ${escapeHtml(formatThresholdValue(key, value))} (live ${escapeHtml(formatThresholdValue(key, applied[key]))})`).join(" · ")}</div>
      <div class="tuning-actions"><button id="apply-tuning" class="action" type="button" ${tuningApplyInFlight ? "disabled" : ""}>${tuningApplyInFlight ? "Applying…" : "Apply recommended tweak"}</button></div>
    ` : ""}
  `;
  const applyButton = tuningAdvisorEl.querySelector("#apply-tuning");
  if (applyButton) {
    applyButton.addEventListener("click", applyRecommendedTuning, { once: true });
  }
}

function renderSignals(signals) {
  renderTopicFilterRow(signals || []);
  const ordered = normalizeSignals(signals || []);
  renderWhatMattersNow(ordered[0] || null);
  renderSelectedSignalWorkbench(ordered, lastDashboardState?.activity || []);

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
    const analyst = signal.analyst || null;

    let analystHtml = "";
    if (analyst?.pending) {
      analystHtml = `<div class="analyst-row analyst-pending">⏳ analysing…</div>`;
    } else if (analyst) {
      const conf = analyst.confidence || "low";
      const ns = analyst.noise_or_signal || "uncertain";
      const dir = analyst.direction || "unclear";
      const confClass = conf === "high" ? "analyst-high" : conf === "medium" ? "analyst-med" : "analyst-low";
      const nsIcon = ns === "signal" ? "▲" : ns === "noise" ? "✕" : "~";
      const nsClass = ns === "signal" ? "analyst-signal" : ns === "noise" ? "analyst-noise" : "analyst-uncertain";
      analystHtml = `
        <div class="analyst-row">
          <span class="analyst-badge ${nsClass}">${nsIcon} ${ns}</span>
          <span class="analyst-badge ${confClass}">${dir} · ${conf} confidence</span>
          <span class="analyst-rationale">${escapeHtml(analyst.rationale)}</span>
        </div>
        ${analyst.threshold_note && analyst.threshold_note !== "none"
          ? `<div class="analyst-threshold">⚙ ${escapeHtml(analyst.threshold_note)}</div>`
          : ""}
      `;
    }

    return `
    <article class="signal-card compact ${getSignalKey(signal) === selectedSignalKey ? "selected" : ""}" data-signal-key="${escapeHtml(getSignalKey(signal))}" tabindex="0" role="button" aria-pressed="${getSignalKey(signal) === selectedSignalKey ? "true" : "false"}">
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
      ${analystHtml}
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
    const price = item.yes_price != null ? `<span class="flow-val primary">${formatPrice(item.yes_price)}</span>` : "";
    const vol = item.volume != null ? `<span class="flow-muted">vol ${formatVolume(item.volume)}</span>` : "";
    const side = item.trade_side ? `<span class="flow-muted secondary">${escapeHtml(item.trade_side)}</span>` : "";
    const kind = item.event_kind === "trade" ? `<span class="flow-kind trade">T</span>` : `<span class="flow-kind quote">Q</span>`;
    const dup = count > 1 ? `<span class="flow-dup">×${count}</span>` : "";
    const spark = sparklineSvg(item.market_id);
    const age = `<span class="flow-age ${freshness.className}">${escapeHtml(freshness.label)}</span>`;
    const matchedSignal = findBestSignalForMarket(lastDashboardState?.signals || [], item.market_id);
    const signalKey = matchedSignal ? getSignalKey(matchedSignal) : "";
    const isSelected = signalKey ? signalKey === selectedSignalKey : item.market_id === selectedMarketId;

    return `
      <div class="flow-row ${isSelected ? "selected" : ""}" data-market-id="${escapeHtml(item.market_id || "")}" data-signal-key="${escapeHtml(signalKey)}" tabindex="0" role="button" aria-pressed="${isSelected ? "true" : "false"}">
        <div class="flow-row-mainline">
          <div class="flow-leading">${kind}<span class="flow-mid">${escapeHtml(item.market_id)}</span>${dup}</div>
          <div class="flow-primary-metric">${price}</div>
        </div>
        <div class="flow-row-secondary">${vol}${side}${spark}${age}</div>
      </div>
    `;
  }).join("");
}

function renderFeeds(state) {
  const feeds = state.feeds || {};
  const activity = state.activity || [];
  const telemetry = state.telemetry || {};

  const pills = [];

  const pushPill = (label, tone = "info", withDot = false) => {
    pills.push(
      `<span class="nav-pill ${tone}">${withDot ? '<span class="dot"></span>' : ""}${escapeHtml(label)}</span>`,
    );
  };

  const freshnessWindow = telemetry.freshness_window_minutes;
  if (freshnessWindow) {
    pushPill(`window: ${freshnessWindow}m`, "info");
  }

  const latestEventAge = formatAgeFromNow(telemetry.latest_event_at);
  const latestEventClass = latestEventAge === "unknown" ? "warn" : (latestEventAge.includes("h") ? "danger" : "ok");
  pushPill(`last event: ${latestEventAge}`, latestEventClass, latestEventClass === "ok");

  const kalshiAge = formatAgeFromNow(telemetry.kalshi_last_event_at);
  const kalshiAgeClass = kalshiAge === "unknown" ? "warn" : (kalshiAge.includes("h") ? "danger" : "ok");
  pushPill(`kalshi: ${kalshiAge}`, kalshiAgeClass, kalshiAgeClass === "ok");

  pushPill(`tickers: ${Number(telemetry.subscribed_tickers || 0)}`, "info");

  if (activity.length) {
    const latestTs = activity[0]?.timestamp;
    const ageMinutes = latestTs ? Math.max(0, Math.floor((Date.now() - new Date(latestTs).getTime()) / 60000)) : null;
    const freshnessClass = ageMinutes !== null && ageMinutes <= 5 ? "ok" : ageMinutes !== null && ageMinutes <= 15 ? "warn" : "danger";
    const freshnessLabel = ageMinutes === null ? "freshness: unknown" : `freshness: ${ageMinutes}m`;
    pushPill(freshnessLabel, freshnessClass, freshnessClass === "ok");
  } else {
    pushPill("freshness: no recent events", "warn");
  }

  const discordFeed = feeds.discord || {};
  const discordDetail = String(discordFeed.detail || "").toLowerCase();
  const discordDisabled = !discordFeed.running || discordDetail.includes("disabled");
  const discordDefault = discordDetail.includes("default");
  const discordClass = discordDisabled ? "warn" : (discordDefault ? "info" : "ok");
  const discordLabel = discordDisabled ? "discord: disabled" : (discordDefault ? "discord: default" : "discord: active");
  pushPill(discordLabel, discordClass, discordClass === "ok");

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

function getTrackedTickerRows(tickers, markets, deadTickers = []) {
  const deadSet = new Set((deadTickers || []).map((ticker) => normalizeTicker(ticker)));

  return (tickers || []).map((ticker) => {
    const normalizedTicker = normalizeTicker(ticker);
    const isDeadTicker = deadSet.has(normalizedTicker);
    const exactMatch = (markets || []).find((market) => market?.market_id === ticker) || null;
    const seriesMatches = exactMatch
      ? [exactMatch]
      : (markets || []).filter((market) => String(market?.market_id || "").startsWith(`${ticker}-`));
    const bestMatch = exactMatch || seriesMatches[0] || null;
    const freshness = bestMatch ? flowFreshness(bestMatch.timestamp) : { label: "unresolved", className: "stale" };
    const statusLabel = isDeadTicker
      ? "expired/invalid"
      : bestMatch
        ? (seriesMatches.length > 1 && !exactMatch ? `${freshness.label} • ${seriesMatches.length} markets` : freshness.label)
        : "unresolved";
    const resolvedTitle = isDeadTicker
      ? "Ticker no longer resolves on the Kalshi API"
      : bestMatch
        ? (exactMatch ? bestMatch.title : `${bestMatch.title} (${seriesMatches.length} open markets)`)
        : "No live market snapshot yet";

    return {
      ticker,
      title: resolvedTitle,
      yesPrice: bestMatch?.yes_price,
      statusLabel,
      statusClass: isDeadTicker ? "dead" : freshness.className,
    };
  });
}

function renderTickerList(markets) {
  if (!tickerListEl) return;

  trackedTickers = Array.isArray(markets) ? [...markets] : [];
  const marketSnapshots = lastDashboardState?.markets || [];
  const deadTickers = lastDashboardState?.config?.dead_kalshi_markets || [];

  if (!trackedTickers.length) {
    tickerListEl.innerHTML = `<div class="empty">No Kalshi tickers tracked yet.</div>`;
    return;
  }

  const rows = getTrackedTickerRows(trackedTickers, marketSnapshots, deadTickers);

  const deadInTracked = deadTickers.filter((d) =>
    trackedTickers.some((t) => normalizeTicker(t) === normalizeTicker(d))
  );

  const pruneBar = deadInTracked.length
    ? `<div class="prune-bar">
        <span class="prune-bar-label">
          <span class="prune-bar-count">${deadInTracked.length}</span> expired/invalid ticker${deadInTracked.length === 1 ? "" : "s"} detected by the feed.
        </span>
        <button class="prune-dead-btn" type="button" data-dead="${escapeHtml(deadInTracked.join(","))}">
          Remove expired (${deadInTracked.length})
        </button>
      </div>`
    : "";

  tickerListEl.innerHTML = `
    ${pruneBar}
    <div class="tracked-table">
      <div class="tracked-head">
        <div>Ticker</div>
        <div>Title</div>
        <div>Yes</div>
        <div>Status</div>
        <div>Action</div>
      </div>
      ${rows.map((row) => `
        <div class="tracked-row">
          <div class="tracked-cell tracked-code">${escapeHtml(row.ticker)}</div>
          <div class="tracked-cell tracked-title">${escapeHtml(row.title)}</div>
          <div class="tracked-cell tracked-price">${row.yesPrice != null ? formatPrice(row.yesPrice) : "n/a"}</div>
          <div class="tracked-cell"><span class="tracked-status ${row.statusClass}">${escapeHtml(row.statusLabel)}</span></div>
          <div class="tracked-cell tracked-action"><button class="ticker-remove" type="button" data-ticker="${escapeHtml(row.ticker)}">Remove</button></div>
        </div>
      `).join("")}
    </div>
  `;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

async function runCategorySearch(query) {
  const q = String(query || "").trim();
  if (!q || !categoryMessageEl || !categoryResultsEl) return;

  categoryMessageEl.textContent = "Searching…";
  categoryResultsEl.innerHTML = "";

  try {
    const resp = await fetch(`/api/kalshi/categories?q=${encodeURIComponent(q)}&limit=20`);
    const data = await resp.json();
    const results = data.results || [];
    const trackedSet = new Set(trackedTickers);

    if (!results.length) {
      categoryMessageEl.textContent = `No open markets found for "${q}".`;
      return;
    }

    categoryMessageEl.textContent = `${results.length} event(s) found. Click a series slug to track it.`;
    categoryResultsEl.innerHTML = results.map((r) => {
      const ticker = r.series_ticker || "";
      const alreadyTracked = ticker && trackedSet.has(ticker);
      return `
        <div class="category-result-row ${alreadyTracked ? "tracked" : ""}">
          <div class="category-result-meta">
            <span class="category-result-title">${escapeHtml(r.title)}</span>
            <span class="category-result-cat">${escapeHtml(r.category)}</span>
          </div>
          <div class="category-result-tickers">
            ${ticker ? `<button class="category-add-btn ${alreadyTracked ? "tracked" : ""}" data-ticker="${escapeHtml(ticker)}" data-state="${alreadyTracked ? "tracked" : "add"}" ${alreadyTracked ? "disabled" : ""} title="${alreadyTracked ? `${escapeHtml(ticker)} is already tracked` : `Add ${escapeHtml(ticker)} to watched tickers`}">${alreadyTracked ? `${escapeHtml(ticker)} ✓` : `${escapeHtml(ticker)} +`}</button>` : "<span class=\"category-result-empty\">No series ticker</span>"}
          </div>
        </div>
      `;
    }).join("");

    categoryResultsEl.querySelectorAll(".category-add-btn").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const ticker = btn.dataset.ticker;
        if (!ticker || btn.dataset.state === "tracked") return;
        btn.disabled = true;
        btn.dataset.state = "adding";
        btn.textContent = "Adding…";
        try {
          const resp = await fetch("/api/kalshi/markets", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ticker }),
          });
          const result = await resp.json();
          if (result.ok) {
            btn.dataset.state = "tracked";
            btn.classList.add("tracked");
            btn.textContent = `${ticker} ✓`;
            categoryMessageEl.textContent = `Added ${ticker} to tracked tickers.`;
            await refresh();
            await runCategorySearch(q);
          } else {
            btn.dataset.state = "add";
            btn.textContent = `${ticker} +`;
            btn.disabled = false;
            categoryMessageEl.textContent = result.error || "Failed to add ticker.";
          }
        } catch {
          btn.dataset.state = "add";
          btn.textContent = `${ticker} +`;
          btn.disabled = false;
          categoryMessageEl.textContent = "Network error.";
        }
      });
    });
  } catch {
    categoryMessageEl.textContent = "Search failed — check network.";
  }
}

async function refreshSettings(force = false) {
  if (!force && currentPage !== "settings" && lastSettingsState) {
    return;
  }

  try {
    const settingsPayload = await fetchSettings();
    renderSettings(settingsPayload);
  } catch (error) {
    if (settingsLoadStatusEl) {
      settingsLoadStatusEl.textContent = "load failed";
    }
    setSettingsControlsEditable(false);
    setSettingsSaveStatus("Failed to load settings.", "error");
  }
}

async function refresh() {
  try {
    const state = await fetchState();
    lastDashboardState = state;
    recordPriceHistory(state.activity || []);
    renderMetrics(state);
    renderModeUI(state.config || {});
    renderSignals(state.signals || []);
    renderTuningAdvisor(state);
    renderActivity(state.activity || [], state.telemetry || {}, state.config || {});
    renderFeeds(state);
    renderMarkets(state.markets || [], state.telemetry || {}, state.config || {});
    renderTickerList(state.config?.kalshi_markets || []);
    await refreshSettings();
  } catch (error) {
    signalsEl.innerHTML = `<div class="empty">${escapeHtml(error.message)}</div>`;
  }
}

if (navTabEls.length) {
  navTabEls.forEach((tab) => {
    tab.addEventListener("click", () => {
      const page = tab.dataset.page || "dashboard";
      setActivePage(page);
    });
  });
}

if (topicFilterRowEl) {
  topicFilterRowEl.addEventListener("click", (event) => {
    const button = event.target.closest(".topic-chip");
    if (!button) return;
    activeSignalTopic = button.dataset.topic || "all";
    renderSignals(lastDashboardState?.signals || []);
  });
}

if (signalsEl) {
  const activateSignalFromElement = (target) => {
    const card = target.closest(".signal-card[data-signal-key]");
    if (!card) return;
    selectedSignalKey = card.dataset.signalKey || null;
    selectedMarketId = null;
    renderSignals(lastDashboardState?.signals || []);
    renderActivity(lastDashboardState?.activity || [], lastDashboardState?.telemetry || {}, lastDashboardState?.config || {});
  };

  signalsEl.addEventListener("click", (event) => {
    activateSignalFromElement(event.target);
  });

  signalsEl.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" && event.key !== " ") return;
    const card = event.target.closest(".signal-card[data-signal-key]");
    if (!card) return;
    event.preventDefault();
    activateSignalFromElement(card);
  });
}

if (activityEl) {
  const activateFlowRow = (target) => {
    const row = target.closest(".flow-row[data-market-id]");
    if (!row) return;
    const signalKey = row.dataset.signalKey;
    if (signalKey) {
      selectedSignalKey = signalKey;
      selectedMarketId = null;
    } else {
      const matchedSignal = findBestSignalForMarket(lastDashboardState?.signals || [], row.dataset.marketId || "");
      if (matchedSignal) {
        selectedSignalKey = getSignalKey(matchedSignal);
        selectedMarketId = null;
      } else {
        selectedSignalKey = null;
        selectedMarketId = row.dataset.marketId || null;
      }
    }
    renderSignals(lastDashboardState?.signals || []);
    renderActivity(lastDashboardState?.activity || [], lastDashboardState?.telemetry || {}, lastDashboardState?.config || {});
  };

  activityEl.addEventListener("click", (event) => {
    activateFlowRow(event.target);
  });

  activityEl.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" && event.key !== " ") return;
    const row = event.target.closest(".flow-row[data-market-id]");
    if (!row) return;
    event.preventDefault();
    activateFlowRow(row);
  });
}

if (settingsToggleEl) {
  settingsToggleEl.addEventListener("click", async () => {
    const nextPage = currentPage === "settings" ? "dashboard" : "settings";
    setActivePage(nextPage);
    if (nextPage === "settings") {
      await refreshSettings(true);
    }
  });
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
    if (tickerMutationInFlight) return;

    const pruneButton = event.target.closest(".prune-dead-btn");
    if (pruneButton) {
      const deadTickers = (lastDashboardState?.config?.dead_kalshi_markets || [])
        .map((ticker) => normalizeTicker(ticker))
        .filter(Boolean);
      const trackedSet = new Set((trackedTickers || []).map((ticker) => normalizeTicker(ticker)).filter(Boolean));
      const targets = deadTickers.filter((ticker) => trackedSet.has(ticker));

      if (!targets.length) {
        setTickerMessage("No feed-confirmed expired tickers to remove.");
        return;
      }

      setTickerMutationBusy(true);
      setTickerMessage(`Removing ${targets.length} expired ticker${targets.length === 1 ? "" : "s"}...`);

      try {
        let markets = trackedTickers;
        for (const ticker of targets) {
          markets = await postTicker("/api/kalshi/markets/remove", ticker);
        }
        renderTickerList(markets);
        setTickerMessage(`Removed ${targets.length} expired ticker${targets.length === 1 ? "" : "s"}.`);
        await refresh();
      } catch (error) {
        setTickerMessage(error.message || "Failed to remove expired tickers.", true);
      } finally {
        setTickerMutationBusy(false);
      }
      return;
    }

    const button = event.target.closest(".ticker-remove");
    if (!button) return;

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
    await runCategorySearch(categoryInput?.value || "");
  });
}

if (categoryShortcutsEl) {
  categoryShortcutsEl.addEventListener("click", async (event) => {
    const button = event.target.closest("button[data-category-shortcut]");
    if (!button || !categoryInput) return;
    categoryInput.value = button.dataset.categoryShortcut || "";
    await runCategorySearch(categoryInput.value);
  });
}

editableSettingsControls.forEach((control) => {
  control.addEventListener("input", () => {
    if (settingsSaveInFlight) return;
    setSettingsSaveStatus("Unsaved changes. Save to write .env and restart to apply.", "pending");
  });
  control.addEventListener("change", () => {
    if (settingsSaveInFlight) return;
    setSettingsSaveStatus("Unsaved changes. Save to write .env and restart to apply.", "pending");
  });
});

if (settingsSaveButtonEl) {
  settingsSaveButtonEl.addEventListener("click", async () => {
    if (settingsSaveInFlight) return;

    settingsSaveInFlight = true;
    setSettingsControlsEditable(true);
    setSettingsSaveStatus("Saving to .env...", "pending");

    try {
      const payload = collectSettingsPayload();
      const result = await saveSettings(payload);
      if (settingsLoadStatusEl) {
        settingsLoadStatusEl.textContent = "saved • restart required";
      }
      renderSettings({ settings: result.settings || (lastSettingsState?.settings || {}) });
      setSettingsSaveStatus("Saved to .env. Restart the app to apply server-side changes.", "success");
    } catch (error) {
      setSettingsSaveStatus(error.message || "Failed to save settings.", "error");
    } finally {
      settingsSaveInFlight = false;
      setSettingsControlsEditable(true);
    }
  });
}

setActivePage(currentPage);
refresh();
setInterval(refresh, 3000);
