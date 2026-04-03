-- Trade Hunter SQLite Schema
-- Events, signals, feed health, and market metadata

-- Events: normalized market event records from all sources
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    platform TEXT NOT NULL,
    market_id TEXT NOT NULL,
    title TEXT NOT NULL,
    event_kind TEXT NOT NULL,
    yes_price REAL,
    no_price REAL,
    volume REAL,
    volume_kind TEXT NOT NULL,
    trade_size REAL,
    trade_side TEXT,
    liquidity REAL,
    live INTEGER NOT NULL DEFAULT 1,
    topic TEXT,
    market_url TEXT,
    timestamp TEXT NOT NULL,
    metadata_json TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_events_market_id ON events(market_id);
CREATE INDEX IF NOT EXISTS idx_events_source ON events(source);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_events_platform ON events(platform);

-- Signals: spike detector output
CREATE TABLE IF NOT EXISTS signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_id TEXT NOT NULL,
    score REAL NOT NULL,
    volume_delta REAL NOT NULL,
    price_move REAL NOT NULL,
    baseline_volume_delta REAL NOT NULL,
    reason TEXT NOT NULL,
    tier TEXT NOT NULL,
    topic TEXT,
    source_label TEXT,
    detected_at TEXT NOT NULL,
    event_id INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_signals_detected_at ON signals(detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_signals_market_id ON signals(market_id);

-- Feed health: status tracking for all feeds
CREATE TABLE IF NOT EXISTS feed_health (
    feed_name TEXT PRIMARY KEY,
    running INTEGER NOT NULL DEFAULT 0,
    detail TEXT,
    last_event_at TEXT,
    error_count INTEGER NOT NULL DEFAULT 0,
    reconnects INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Markets: aggregated market metadata
CREATE TABLE IF NOT EXISTS markets (
    market_id TEXT PRIMARY KEY,
    platform TEXT NOT NULL,
    title TEXT NOT NULL,
    last_event_at TEXT NOT NULL,
    total_events INTEGER NOT NULL DEFAULT 0,
    last_yes_price REAL,
    last_volume REAL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_markets_last_event_at ON markets(last_event_at DESC);
CREATE INDEX IF NOT EXISTS idx_markets_platform ON markets(platform);
