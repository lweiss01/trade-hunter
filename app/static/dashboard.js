const metricsEl = document.querySelector("#metrics");
const signalsEl = document.querySelector("#signals");
const topicFilterRowEl = document.querySelector("#topic-filter-row");
const signalSortEl = document.querySelector("#signal-sort");
const signalLatestToggleEl = document.querySelector("#signal-latest-toggle");
const activityEl = document.querySelector("#activity");
const feedsEl = document.querySelector("#feeds");
const marketsEl = document.querySelector("#markets");
const dashboardMarketsEl = document.querySelector("#dashboard-markets");
const demoButton = document.querySelector("#demo-spike");
const demoPanel = document.querySelector("#demo-panel");
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
const settingsStatusCoreEl = null; // removed — merged into Feeds panel
const settingsStatusKalshiEl = document.querySelector("#settings-status-kalshi"); // now the Feeds panel badge
const settingsStatusAnalystEl = null; // removed — merged into Discord panel
const settingsStatusDiscordEl = document.querySelector("#settings-status-discord");
const settingsStatusIngestEl = null; // removed — merged into Feeds panel
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

let trackedTickers = [];
let signalSortMode = "newest";
let signalLatestOnly = false;
let activeSignalTopic = "all";
let currentPage = "dashboard";
let lastDashboardState = null;
let lastSettingsState = null;
let settingsSaveInFlight = false;
let tickerMutationInFlight = false;

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

  setSettingsStatus(settingsStatusDetectorEl, "configured", "configured");
  setSettingsStatus(settingsStatusStorageEl, "configured", "configured");

  // Feeds panel: show worst-case status across Kalshi + ingest
  const kalshiOk = settings.enable_kalshi && presence.kalshi_api_key_id && presence.kalshi_private_key_path;
  const ingestOk = presence.ingest_api_token || presence.polyalerthub_token;
  if (kalshiOk || ingestOk) {
    setSettingsStatus(settingsStatusKalshiEl, "configured", "data sources");
  } else if (!settings.enable_kalshi) {
    setSettingsStatus(settingsStatusKalshiEl, "disabled", "simulation only");
  } else {
    setSettingsStatus(settingsStatusKalshiEl, "missing", "missing key");
  }

  if (presence.discord_webhook_url || (presence.discord_webhook_routes || []).length) {
    setSettingsStatus(settingsStatusDiscordEl, "configured", "configured");
  } else {
    setSettingsStatus(settingsStatusDiscordEl, "disabled", "disabled");
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
  const windowLabel = liveWindow ? `${liveWindow}m` : null;
  const mode = String(config.active_mode || "none").toLowerCase();
  const modeValue = mode === "live" ? "Live" : mode === "simulation" ? "Simulation" : "Offline";

  const stats = [
    { label: "tracked markets",  value: markets.length,                sub: windowLabel },
    { label: "signals",          value: signals.length,                sub: windowLabel },
    { label: "flow events",      value: (state.activity || []).length, sub: windowLabel },
    { label: "trades",           value: summary.trade_events || 0,     sub: windowLabel },
    { label: "active feeds",     value: Object.keys(feeds).length,     sub: null },
    { label: "discord routes",   value: routeCount,                    sub: routeCount ? null : "default or disabled" },
    { label: "application mode", value: modeValue,                     sub: null, tone: mode === "live" ? "mode-live" : mode === "simulation" ? "mode-sim" : "mode-off" },
  ];

  metricsEl.innerHTML = `<div class="metric-strip">${
    stats.map((s, i) => {
      const sub = s.sub ? `<span class="metric-chip-sub">${s.sub}</span>` : "";
      const tone = s.tone ? ` ${s.tone}` : "";
      const cls = i === 0 ? `metric-chip highlight${tone}` : `metric-chip${tone}`;
      if (s.label === "application mode") {
        return `<span class="${cls}"><span class="metric-chip-label metric-chip-label-mode">Application mode:</span><span class="metric-chip-val metric-chip-val-mode">${s.value}</span>${sub}</span>`;
      }
      return `<span class="${cls}"><span class="metric-chip-val">${s.value}</span><span class="metric-chip-label">${s.label}</span>${sub}</span>`;
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
  const nextSteps = [];

  if (signal?.event?.volume != null) nextSteps.push(`Check liquidity (${formatVolume(signal.event.volume)} vol)`);
  if (signal?.event?.yes_price != null) nextSteps.push(`Confirm price context (${formatPrice(signal.event.yes_price)})`);
  nextSteps.push(`Review ${topic} context`);

  whatMattersNowEl.hidden = false;
  whatMattersNowEl.innerHTML = `
    <div class="wmn-strip">
      <div class="wmn-head">
        <div class="wmn-eyebrow">
          <span class="wmn-label">Top signal right now</span>
          <div class="wmn-tags">
            <span class="sig-tag tier-${escapeHtml(tier)}">${escapeHtml(tier)}</span>
            <span class="sig-tag score">score ${Number(signal.score || 0).toFixed(2)}</span>
            <span class="sig-tag ${freshness.className}">${escapeHtml(freshness.label)}</span>
          </div>
        </div>
        <strong class="wmn-title">${escapeHtml(title)}</strong>
        <div class="wmn-meta">${escapeHtml(signal?.event?.platform || "unknown")} · ${escapeHtml(signal?.event?.market_id || "unknown-market")} · ${escapeHtml(topic)} · ${formatTimestamp(signal.detected_at)}</div>
      </div>
      <div class="wmn-body">
        <div class="wmn-why">
          <span class="wmn-section-label">Why this matters</span>
          <p class="wmn-reason">${escapeHtml(whyThisMatters)}</p>
        </div>
        <div class="wmn-steps">
          <span class="wmn-section-label">Your next steps</span>
          <div class="wmn-step-chips">${nextSteps.map((item) => `<span class="wmn-step-chip">${escapeHtml(item)}</span>`).join("")}</div>
        </div>
      </div>
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
    tuningAdvisorEl.innerHTML = `<div class="empty">Waiting for enough analysed signals to recommend next steps.</div>`;
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
  const thresholdSummary = suggestedEntries.length
    ? suggestedEntries.map(([key, value]) => `<span class="tuning-threshold-item">${escapeHtml(key)} <strong>${escapeHtml(formatThresholdValue(key, value))}</strong> <span class="tuning-live">live ${escapeHtml(formatThresholdValue(key, applied[key]))}</span></span>`).join("")
    : "";

  // Derive a stable TB-id from the recommendation content
  const tbId = advisor.tb_id || (() => {
    const src = (advisor.global_recommendation || "") + (advisor.summary || "");
    let h = 0;
    for (let i = 0; i < src.length; i++) { h = (Math.imul(31, h) + src.charCodeAt(i)) | 0; }
    return `TB-${String(Math.abs(h) % 900 + 100)}`;
  })();
  const tbHtml = `<span class="tuning-tb-id">${escapeHtml(tbId)}</span>`;

  tuningAdvisorEl.innerHTML = `
    <div class="tuning-summary">${escapeHtml(advisor.summary || "")}</div>
    <div class="tuning-recommendation">${tbHtml}<strong>Next step:</strong> ${escapeHtml(advisor.global_recommendation || "")}</div>
    ${thresholdSummary ? `<div class="tuning-threshold-summary">${thresholdSummary}</div>` : ""}
    ${recs.length ? `<ul class="tuning-list">${recs.map(r => `<li>${escapeHtml(r)}</li>`).join("")}</ul>` : ""}
  `;
}

function renderSignals(signals) {
  renderTopicFilterRow(signals || []);
  const ordered = normalizeSignals(signals || []);

  if (!ordered.length) {
    const latestSignalAge = formatAgeFromNow(lastDashboardState?.telemetry?.latest_signal_at);
    const windowMinutes = lastDashboardState?.telemetry?.freshness_window_minutes;
    if (windowMinutes) {
      signalsEl.innerHTML = `<div class="empty">No signals in the ${windowMinutes}m window. Last signal ${escapeHtml(latestSignalAge)}.</div>`;
    } else {
      signalsEl.innerHTML = `<div class="empty">No spikes yet. Keep the page open or trigger the demo event.</div>`;
    }
    return;
  }

  signalsEl.innerHTML = ordered.map((signal) => {
    const freshness = signalFreshness(signal.detected_at);
    const analyst = signal.analyst || null;
    const tier = String(signal.tier || "watch");
    const scoreRaw = Number(signal.score || 0);
    // cap score at 10 for bar width; normalise to percentage
    const scoreBarPct = Math.min(100, Math.round((scoreRaw / 10) * 100));

    let analystTagHtml = "";
    if (analyst?.pending) {
      analystTagHtml = `<span class="sig-tag analyst-pending">reviewing</span>`;
    } else if (analyst) {
      const conf = analyst.confidence || "low";
      const ns = analyst.noise_or_signal || "uncertain";
      const nsClass = ns === "signal" ? "signal" : ns === "noise" ? "noise" : "uncertain";
      const confClass = conf === "high" ? "high-conf" : conf === "medium" ? "med-conf" : "low-conf";
      analystTagHtml = `
        <span class="sig-tag analyst-${nsClass}">${escapeHtml(ns)}</span>
        <span class="sig-tag analyst-${confClass}">${escapeHtml(conf)} conf</span>
      `;
    }

    return `
    <article class="signal-card tier-${escapeHtml(tier)}" data-signal-key="${escapeHtml(getSignalKey(signal))}">
      <div class="sig-row1">
        <strong class="sig-title">${escapeHtml(signal.event.title)}</strong>
        <div class="sig-tags">
          <span class="sig-tag tier-${escapeHtml(tier)}">${escapeHtml(tier)}</span>
          <span class="sig-tag ${freshness.className}">${escapeHtml(freshness.label)}</span>
          ${analystTagHtml}
        </div>
      </div>
      <div class="sig-meta">${escapeHtml(signal.event.platform)} · ${escapeHtml(signal.event.market_id)} · ${escapeHtml(signal.source_label || signal.event.source)} · ${formatTimestamp(signal.detected_at)}</div>
      <div class="sig-score-bar-wrap">
        <div class="sig-score-bar-track"><div class="sig-score-bar-fill" style="width:${scoreBarPct}%"></div></div>
        <span class="sig-score-val">${scoreRaw.toFixed(2)}</span>
        <span class="sig-tag score">score ${scoreRaw.toFixed(2)}</span>
      </div>
      <div class="sig-reason">${escapeHtml(summarizeReason(signal.reason))}</div>
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

function collapseFlowEvents(events) {
  const order = [];
  const groups = new Map();

  for (const event of events || []) {
    const signature = [
      event.platform,
      event.source,
      event.market_id,
      event.event_kind,
      event.trade_side || "",
      event.yes_price ?? "",
      event.live ? "live" : "demo",
    ].join("|");

    if (!groups.has(signature)) {
      groups.set(signature, {
        event,
        count: 1,
        totalVolume: Number(event.volume || 0),
      });
      order.push(signature);
    } else {
      const group = groups.get(signature);
      group.count += 1;
      group.totalVolume += Number(event.volume || 0);
    }
  }

  return order.map((signature) => groups.get(signature));
}

function collapseMarketsByLatest(markets) {
  const order = [];
  const groups = new Map();

  for (const market of markets || []) {
    const key = [market.platform, market.market_id].join("|");
    if (!groups.has(key)) {
      groups.set(key, { event: market, count: 1 });
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
      activityEl.innerHTML = `<div class="empty">No fresh events in the ${windowMinutes}m window. Last event ${escapeHtml(latestAge)}.</div>`;
    } else {
      activityEl.innerHTML = `<div class="empty">No live flow yet. Simulation or real feeds will start filling this stream.</div>`;
    }
    return;
  }

  const collapsed = collapseFlowEvents(activity);

  activityEl.innerHTML = `<div class="flow-list">${collapsed.map(({ event: item, count, totalVolume }) => {
    const freshness = flowFreshness(item.timestamp);
    const price = item.yes_price != null ? `<span class="flow-price">${formatPrice(item.yes_price)}</span>` : `<span class="flow-price">n/a</span>`;
    const volValue = totalVolume > 0 ? totalVolume : Number(item.volume || 0);
    const vol = `<span class="flow-vol">vol ${formatVolume(volValue)}</span>`;
    const sideLabel = item.event_kind === "trade" ? (item.trade_side || "—") : "—";
    const side = `<span class="flow-side">${escapeHtml(sideLabel)}</span>`;
    const kindClass = item.event_kind === "trade" ? "T" : "Q";
    const kind = `<span class="flow-kind ${kindClass}">${kindClass}</span>`;
    const dup = count > 1 ? `<span class="flow-dup">×${count}</span>` : `<span class="flow-dup"></span>`;
    const age = `<span class="flow-age ${freshness.className}">${escapeHtml(freshness.label)}</span>`;

    return `
      <div class="flow-row" data-market-id="${escapeHtml(item.market_id || "")}">
        ${kind}
        ${dup}
        <span class="flow-mid">${escapeHtml(item.market_id)}</span>
        ${price}
        ${vol}
        ${side}
        ${age}
      </div>
    `;
  }).join("")}</div>`;
}

function renderFeeds(state) {
  const feeds = state.feeds || {};
  const telemetry = state.telemetry || {};

  const pills = [];

  const pushPill = (label, tone = "info", withDot = false) => {
    pills.push(
      `<span class="nav-pill ${tone}">${withDot ? '<span class="dot"></span>' : ""}${escapeHtml(label)}</span>`,
    );
  };

  const freshnessWindow = telemetry.freshness_window_minutes;
  if (freshnessWindow) {
    pushPill(`window ${freshnessWindow}m`, "info");
  }

  // ── Kalshi WebSocket connection pill ──
  const kalshiFeed = feeds["kalshi-pykalshi"] || {};
  const kalshiRunning = Boolean(kalshiFeed.running);
  const kalshiDetail = kalshiFeed.detail || "";
  const kalshiWsMatch = kalshiDetail.match(/ws_msgs:(\d+)/);
  const kalshiWsActive = kalshiWsMatch && Number(kalshiWsMatch[1]) > 0;

  if (!kalshiRunning) {
    pushPill("kalshi offline", "danger", false);
  } else if (kalshiWsActive) {
    pushPill("kalshi connected", "ok", true);
  } else {
    pushPill("kalshi stale", "warn", false);
  }

  // ── Markets open pill — only visible when ticker/trade events are flowing ──
  const kalshiEventAge = formatAgeFromNow(telemetry.kalshi_last_event_at);
  if (kalshiRunning && kalshiEventAge !== "unknown" && !kalshiEventAge.includes("h")) {
    const marketsAgeMin = Number.parseInt(kalshiEventAge, 10);
    const marketsTone = Number.isFinite(marketsAgeMin) && freshnessWindow && marketsAgeMin > freshnessWindow ? "warn" : "ok";
    pushPill(`markets open ${kalshiEventAge}`, marketsTone, marketsTone === "ok");
  }

  pushPill(`tickers ${Number(telemetry.subscribed_tickers || 0)}`, "info");

  if (state.activity?.length) {
    const latestTs = state.activity[0]?.timestamp;
    const ageMinutes = latestTs ? Math.max(0, Math.floor((Date.now() - new Date(latestTs).getTime()) / 60000)) : null;
    const freshnessClass = ageMinutes !== null && ageMinutes <= 5 ? "ok" : ageMinutes !== null && ageMinutes <= 15 ? "warn" : "danger";
    const freshnessLabel = ageMinutes === null ? "fresh ?" : `fresh ${ageMinutes}m`;
    pushPill(freshnessLabel, freshnessClass, freshnessClass === "ok");
  }

  feedsEl.innerHTML = pills.join("");
}

function renderMarkets(markets, telemetry = {}, config = {}) {
  const targets = [marketsEl, dashboardMarketsEl].filter(Boolean);
  if (!targets.length) return;

  let html = "";

  const thead = `
    <thead>
      <tr>
        <th>Market</th>
        <th>Type</th>
        <th>Yes</th>
        <th>Volume</th>
        <th>Seen</th>
      </tr>
    </thead>
  `;

  if (!markets.length) {
    const mode = config.active_mode || "unknown";
    const windowMinutes = telemetry.freshness_window_minutes;
    const latestAge = formatAgeFromNow(telemetry.latest_event_at);
    const emptyCopy = mode === "live" && windowMinutes
      ? `No market snapshots in the ${windowMinutes}m window. Last market ${escapeHtml(latestAge)}.`
      : "No market events yet.";

    html = `
      <div class="market-table-scroll">
        <table class="market-table-compact">
          ${thead}
          <tbody>
            <tr><td colspan="5" class="empty">${emptyCopy}</td></tr>
          </tbody>
        </table>
      </div>
    `;
  } else {
    const collapsed = collapseMarketsByLatest(markets);

    const rows = collapsed.map(({ event: market, count }) => {
      const titleIsDuplicate = market.title === market.market_id || !market.title;
      const titleHtml = titleIsDuplicate
        ? `<div class="mkt-title">${escapeHtml(market.market_id)}</div>
           <div class="mkt-id">${escapeHtml(market.topic || "general")}</div>`
        : `<div class="mkt-title">${escapeHtml(market.title)}</div>
           <div class="mkt-id">${escapeHtml(market.market_id)} · ${escapeHtml(market.topic || "general")}</div>`;
      const kindLabel = market.event_kind === "trade" ? "T" : "Q";
      const countLabel = count > 1 ? ` ×${count}` : "";
      return `
      <tr>
        <td>${titleHtml}</td>
        <td class="mkt-cell mkt-kind">${kindLabel}${countLabel}</td>
        <td class="mkt-cell mkt-price">${formatPrice(market.yes_price)}</td>
        <td class="mkt-cell">${formatVolume(market.volume)}</td>
        <td class="mkt-cell">${formatTimestamp(market.timestamp)}</td>
      </tr>
    `;
    }).join("");

    html = `
      <div class="market-table-scroll">
        <table class="market-table-compact">
          ${thead}
          <tbody>${rows}</tbody>
        </table>
      </div>
    `;
  }

  targets.forEach((target) => {
    target.innerHTML = html;
  });
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
        ? freshness.label
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

  // Update panel badge with active count
  const tickerBadgeEl = document.getElementById("ticker-panel-badge");
  if (tickerBadgeEl) {
    tickerBadgeEl.textContent = trackedTickers.length
      ? `${trackedTickers.length} active`
      : "no tickers";
  }

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
    <div class="tracked-table-wrap">
      <table class="market-table-compact tracked-table-compact">
        <thead>
          <tr>
            <th>Market</th>
            <th>Yes</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          ${rows.map((row) => `
            <tr class="${row.statusClass === 'dead' ? 'tracked-row-dead' : ''}">
              <td class="tracked-market-cell">
                <span class="tracked-ticker-code">${escapeHtml(row.ticker)}</span>
                <span class="tracked-ticker-title">${escapeHtml(row.title)}</span>
              </td>
              <td class="mkt-cell mkt-price tracked-price-cell">${row.yesPrice != null ? formatPrice(row.yesPrice) : "n/a"}</td>
              <td class="tracked-status-cell"><span class="tracked-status-pill ${row.statusClass}">${escapeHtml(row.statusLabel)}</span></td>
              <td class="tracked-remove-cell"><button class="ticker-remove tracked-remove-btn" type="button" data-ticker="${escapeHtml(row.ticker)}" title="Remove ${escapeHtml(row.ticker)}" aria-label="Remove ${escapeHtml(row.ticker)}">×</button></td>
            </tr>
          `).join("")}
        </tbody>
      </table>
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
      categoryMessageEl.textContent = `No open series found for "${q}".`;
      return;
    }

    categoryMessageEl.textContent = `${results.length} series found. Choose one to track it.`;
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
    categoryMessageEl.textContent = "Series lookup failed — check network.";
  }
}

async function fetchAndRenderBacklog() {
  const bodyEl = document.getElementById("tuning-backlog-body");
  const appliedEl = document.getElementById("tb-stat-applied");
  const plannedEl = document.getElementById("tb-stat-planned");
  if (!bodyEl) return;

  try {
    const resp = await fetch("/api/tuning/backlog");
    const data = await resp.json();

    if (appliedEl) appliedEl.textContent = `${data.applied_count} applied`;
    if (plannedEl) plannedEl.textContent = `${data.planned_count} planned`;

    if (!data.snapshots || !data.snapshots.length) {
      bodyEl.innerHTML = `<div style="padding:20px 16px;color:var(--text-muted);font-size:0.8rem;">No backlog entries yet.</div>`;
      return;
    }

    const plannedIds = data.snapshots
      .flatMap(s => s.items)
      .filter(i => i.status === "planned")
      .slice(0, 3)
      .map(i => i.id);

    const priorityBar = plannedIds.length ? `
      <div class="tb-priority-bar">
        <span class="tb-priority-label">Next recommended:</span>
        ${plannedIds.map((id, n) => `<span class="tb-priority-chip">${n + 1} · ${escapeHtml(id)}</span>`).join("")}
      </div>` : "";

    const snapshotHtml = data.snapshots.map(snap => {
      const itemsHtml = snap.items.map(item => {
        const isPlanned = item.status === "planned";
        const isApplied = item.status === "applied";
        const rowClass = isApplied ? "tb-row tb-applied" : "tb-row tb-planned";
        const actionBtn = isPlanned
          ? `<button class="tb-apply-btn ${item.id === plannedIds[0] ? 'tb-apply-btn-primary' : ''}" data-tb-id="${escapeHtml(item.id)}">${item.id === plannedIds[0] ? 'Apply next' : 'Mark applied'}</button>`
          : "";
        return `
          <div class="${rowClass}">
            <div class="tb-id">${escapeHtml(item.id)}</div>
            <span class="tb-badge ${escapeHtml(item.status)}">${escapeHtml(item.status)}</span>
            <div class="tb-body">
              <div class="tb-rule">${escapeHtml(item.rule)}</div>
              ${item.detail ? `<div class="tb-detail">${escapeHtml(item.detail)}</div>` : ""}
              ${item.note ? `<div class="tb-note">${escapeHtml(item.note)}</div>` : ""}
            </div>
            <div class="tb-actions">${actionBtn}</div>
          </div>`;
      }).join("");

      return `
        <div class="tb-snapshot-hd">
          <span class="tb-snapshot-label">${escapeHtml(snap.label)}</span>
          ${snap.summary ? `<span class="tb-snapshot-summary">${escapeHtml(snap.summary)}</span>` : ""}
        </div>
        ${itemsHtml}`;
    }).join("");

    bodyEl.innerHTML = priorityBar + snapshotHtml;

    // Wire mark-applied buttons
    bodyEl.querySelectorAll(".tb-apply-btn[data-tb-id]").forEach(btn => {
      btn.addEventListener("click", async () => {
        const id = btn.dataset.tbId;
        btn.disabled = true;
        btn.textContent = "…";
        try {
          const r = await fetch("/api/tuning/mark-applied", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id }),
          });
          const result = await r.json();
          if (result.ok) {
            await fetchAndRenderBacklog(); // re-render with updated state
          } else {
            btn.disabled = false;
            btn.textContent = "Error";
          }
        } catch {
          btn.disabled = false;
          btn.textContent = "Failed";
        }
      });
    });

  } catch (err) {
    bodyEl.innerHTML = `<div style="padding:20px 16px;color:var(--text-muted);font-size:0.8rem;">Failed to load backlog.</div>`;
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
  fetchAndRenderBacklog();
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

const settingsRestartBtnEl = document.querySelector("#settings-restart-btn");
if (settingsRestartBtnEl) {
  settingsRestartBtnEl.addEventListener("click", async () => {
    if (!confirm("Restart the server now? The page will reload automatically.")) return;
    settingsRestartBtnEl.disabled = true;
    settingsRestartBtnEl.textContent = "Restarting…";
    try {
      await fetch("/api/admin/shutdown", { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });
    } catch { /* server shutting down — connection error is expected */ }
    // Poll until the server comes back, then reload
    const poll = setInterval(async () => {
      try {
        const r = await fetch("/api/health");
        if (r.ok) { clearInterval(poll); location.reload(); }
      } catch { /* still restarting */ }
    }, 1000);
  });
}

setActivePage(currentPage);
refresh();
setInterval(refresh, 3000);
