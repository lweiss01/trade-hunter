"""SQLite database connection and initialization."""
from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import DATA_ROOT, ASSET_ROOT

SCHEMA_PATH = ASSET_ROOT / "app" / "schema.sql"
DEFAULT_DB_PATH = DATA_ROOT / "trade_hunter.db"

_SIGNAL_COLUMN_MIGRATIONS: dict[str, str] = {
    "baseline_1h": "ALTER TABLE signals ADD COLUMN baseline_1h REAL",
    "baseline_24h": "ALTER TABLE signals ADD COLUMN baseline_24h REAL",
    "price_move_1m": "ALTER TABLE signals ADD COLUMN price_move_1m REAL",
    "price_move_5m": "ALTER TABLE signals ADD COLUMN price_move_5m REAL",
    "price_move_30m": "ALTER TABLE signals ADD COLUMN price_move_30m REAL",
    "leading_events_json": "ALTER TABLE signals ADD COLUMN leading_events_json TEXT",
}


def _quarantine_corrupt_database(path: Path) -> None:
    if not path.exists() or str(path) == ":memory:":
        return

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    quarantine_path = path.with_name(f"{path.stem}.corrupt-{stamp}{path.suffix}")
    path.replace(quarantine_path)

    for suffix in ("-wal", "-shm"):
        sidecar = Path(f"{path}{suffix}")
        if sidecar.exists():
            sidecar.replace(path.with_name(f"{sidecar.name}.corrupt-{stamp}"))


def _ensure_signal_columns(conn: sqlite3.Connection) -> None:
    """Backfill newer signal columns into existing local databases."""
    existing_columns = {
        row["name"]
        for row in conn.execute("PRAGMA table_info(signals)").fetchall()
    }
    for column, statement in _SIGNAL_COLUMN_MIGRATIONS.items():
        if column not in existing_columns:
            conn.execute(statement)


def _ensure_database_integrity(conn: sqlite3.Connection) -> None:
    row = conn.execute("PRAGMA quick_check").fetchone()
    result = row[0] if row else "missing quick_check result"
    if result != "ok":
        raise sqlite3.DatabaseError(f"database integrity check failed: {result}")


def connect(db_path: str | Path | None = None, *, in_memory: bool = False) -> sqlite3.Connection:
    """
    Connect to SQLite database and initialize schema.
    
    Args:
        db_path: Path to database file. Defaults to trade_hunter.db in user data dir.
        in_memory: Use ":memory:" database for testing.
    
    Returns:
        sqlite3.Connection with row_factory and foreign keys enabled.
    """
    if in_memory:
        path = ":memory:"
    elif db_path:
        path = str(db_path)
    elif os.getenv("PYTEST_CURRENT_TEST"):
        path = ":memory:"
    else:
        path = str(DEFAULT_DB_PATH)

    if path != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)

    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    def open_and_initialize() -> sqlite3.Connection:
        conn: sqlite3.Connection | None = None
        conn = sqlite3.connect(path, check_same_thread=False, timeout=30.0)
        try:
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA busy_timeout = 30000")
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA synchronous = NORMAL")
            conn.executescript(schema_sql)
            _ensure_signal_columns(conn)
            _ensure_database_integrity(conn)
            conn.commit()
            return conn
        except sqlite3.DatabaseError:
            conn.close()
            raise

    try:
        return open_and_initialize()
    except sqlite3.DatabaseError:
        if path == ":memory:" or db_path or os.getenv("PYTEST_CURRENT_TEST"):
            raise
        _quarantine_corrupt_database(Path(path))
        return open_and_initialize()


def dict_from_row(row: sqlite3.Row) -> dict[str, Any]:
    """Convert sqlite3.Row to dict."""
    return {key: row[key] for key in row.keys()}
