"""Pytest configuration and fixtures."""
from __future__ import annotations

import pytest
import sqlite3

from app import db


@pytest.fixture
def test_db() -> sqlite3.Connection:
    """Create an in-memory test database with schema initialized."""
    conn = db.connect(in_memory=True)
    yield conn
    conn.close()


@pytest.fixture
def test_db_path(tmp_path):
    """Create a temporary database file for testing."""
    db_path = tmp_path / "test.db"
    conn = db.connect(db_path)
    yield conn, db_path
    conn.close()
