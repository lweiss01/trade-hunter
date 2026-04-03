"""SQLite database connection and initialization."""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "app" / "schema.sql"
DEFAULT_DB_PATH = ROOT / "trade_hunter.db"


def connect(db_path: str | Path | None = None, *, in_memory: bool = False) -> sqlite3.Connection:
    """
    Connect to SQLite database and initialize schema.
    
    Args:
        db_path: Path to database file. Defaults to trade_hunter.db in project root.
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
    
    conn = sqlite3.connect(path, check_same_thread=False, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 30000")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    
    # Initialize schema
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.executescript(schema_sql)
    conn.commit()
    
    return conn


def dict_from_row(row: sqlite3.Row) -> dict[str, Any]:
    """Convert sqlite3.Row to dict."""
    return {key: row[key] for key in row.keys()}
