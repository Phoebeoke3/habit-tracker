import os
import sys
import pytest
import sqlite3
import json
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_db_connection():
    """Mock database connection for testing."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.execute.return_value = mock_cursor
    
    with patch('db.conn', mock_conn):
        with patch('db.cursor', mock_cursor):
            with patch('models.habit.conn', mock_conn):
                with patch('models.habit.cursor', mock_cursor):
                    with patch('models.user.conn', mock_conn):
                        with patch('controllers.habit_controllers.conn', mock_conn):
                            yield mock_conn, mock_cursor

@pytest.fixture
def test_user():
    """Sample user data for testing."""
    return {
        "id": 1,
        "username": "testuser",
        "password": "testpass"
    }

@pytest.fixture
def test_habit():
    """Sample habit data for testing."""
    return (1, "Test Habit", "Test Description", "2023-01-01 00:00:00", 1, 5, "daily", "2023-01-05 00:00:00")

@pytest.fixture
def mock_session_file(tmp_path):
    """Creates a temporary session file for testing."""
    session_file = tmp_path / "session.json"
    session_file.write_text("{}")
    
    with patch('utils.session.SESSION_PATH', str(session_file)):
        yield session_file 