"""Fixtures in this file are automatically accessible to all tests."""
import os
import sqlite3

import pytest


@pytest.fixture(scope='function')
def db(tmpdir):
    """Create a temporary DB connection for testing."""
    file = os.path.join(tmpdir.strpath, "test.db")

    conn = sqlite3.connect(file)
    conn.execute("CREATE TABLE users (id, name, password, last_logged)")
    conn.execute("CREATE TABLE entries (id, title, body, created, edited)")

    yield conn

    conn.close()
