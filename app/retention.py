"""Data retention policy for events and signals."""
from __future__ import annotations

import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from . import db


def cleanup_old_events(db_path: str | Path | None, retention_days: int) -> dict[str, Any]:
    """
    Delete events and signals older than retention_days.
    
    Args:
        db_path: Path to database file (None for default)
        retention_days: Number of days to retain data
    
    Returns:
        dict with rows_deleted, retention_days, executed_at
    """
    conn = db.connect(db_path) if db_path else db.connect()
    cursor = conn.cursor()
    
    cutoff = datetime.now(UTC) - timedelta(days=retention_days)
    cutoff_iso = cutoff.isoformat()
    
    # Delete old events (signals will cascade via FK)
    cursor.execute("DELETE FROM events WHERE timestamp < ?", (cutoff_iso,))
    events_deleted = cursor.rowcount
    
    # Delete old signals (orphaned signals without event_id)
    cursor.execute("DELETE FROM signals WHERE detected_at < ?", (cutoff_iso,))
    signals_deleted = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return {
        "events_deleted": events_deleted,
        "signals_deleted": signals_deleted,
        "retention_days": retention_days,
        "executed_at": datetime.now(UTC).isoformat(),
    }
