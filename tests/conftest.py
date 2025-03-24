import os
import sys
import pytest
import sqlite3
import json
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

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

@pytest.fixture
def four_weeks_habit_data():
    """Test fixture providing 4 weeks of tracking data for predefined habits."""
    start_date = datetime(2024, 1, 1)  # Starting from January 1st, 2024
    
    return {
        "Drink Water": {
            "description": "Drink 2 litres of water daily",
            "periodicity": "daily",
            "start_date": start_date.strftime('%Y-%m-%d %H:%M:%S'),
            "completions": [
                # Week 1 - Perfect week
                {"date": "2024-01-01", "streak": 1},
                {"date": "2024-01-02", "streak": 2},
                {"date": "2024-01-03", "streak": 3},
                {"date": "2024-01-04", "streak": 4},
                {"date": "2024-01-05", "streak": 5},
                {"date": "2024-01-06", "streak": 6},
                {"date": "2024-01-07", "streak": 7},
                # Week 2 - Missed weekend
                {"date": "2024-01-08", "streak": 8},
                {"date": "2024-01-09", "streak": 9},
                {"date": "2024-01-10", "streak": 10},
                {"date": "2024-01-11", "streak": 11},
                {"date": "2024-01-12", "streak": 12},
                # Week 3 - Workdays only
                {"date": "2024-01-15", "streak": 1},
                {"date": "2024-01-16", "streak": 2},
                {"date": "2024-01-17", "streak": 3},
                {"date": "2024-01-18", "streak": 4},
                {"date": "2024-01-19", "streak": 5},
                # Week 4 - Inconsistent
                {"date": "2024-01-22", "streak": 1},
                {"date": "2024-01-23", "streak": 2},
                {"date": "2024-01-25", "streak": 1}
            ],
            "expected_max_streak": 12
        },
        
        "Gym": {
            "description": "Workout for at least 30 minutes",
            "periodicity": "daily",
            "start_date": start_date.strftime('%Y-%m-%d %H:%M:%S'),
            "completions": [
                # Week 1 - Monday/Wednesday/Friday
                {"date": "2024-01-01", "streak": 1},
                {"date": "2024-01-03", "streak": 1},
                {"date": "2024-01-05", "streak": 1},
                # Week 2 - Monday/Wednesday/Friday
                {"date": "2024-01-08", "streak": 1},
                {"date": "2024-01-10", "streak": 1},
                {"date": "2024-01-12", "streak": 1},
                # Week 3 - Extra session
                {"date": "2024-01-15", "streak": 1},
                {"date": "2024-01-17", "streak": 1},
                {"date": "2024-01-18", "streak": 2},
                {"date": "2024-01-19", "streak": 3},
                # Week 4 - Missed sessions
                {"date": "2024-01-22", "streak": 1},
                {"date": "2024-01-26", "streak": 1}
            ],
            "expected_max_streak": 3
        },
        
        "Read": {
            "description": "Read a book for 20 minutes",
            "periodicity": "daily",
            "start_date": start_date.strftime('%Y-%m-%d %H:%M:%S'),
            "completions": [
                # Week 1 - Evening routine
                {"date": "2024-01-01", "streak": 1},
                {"date": "2024-01-02", "streak": 2},
                {"date": "2024-01-03", "streak": 3},
                {"date": "2024-01-04", "streak": 4},
                # Week 2 - Busy week
                {"date": "2024-01-08", "streak": 1},
                {"date": "2024-01-09", "streak": 2},
                # Week 3 - Better routine
                {"date": "2024-01-15", "streak": 1},
                {"date": "2024-01-16", "streak": 2},
                {"date": "2024-01-17", "streak": 3},
                {"date": "2024-01-18", "streak": 4},
                {"date": "2024-01-19", "streak": 5},
                # Week 4 - Maintained routine
                {"date": "2024-01-22", "streak": 1},
                {"date": "2024-01-23", "streak": 2},
                {"date": "2024-01-24", "streak": 3},
                {"date": "2024-01-25", "streak": 4},
                {"date": "2024-01-26", "streak": 5}
            ],
            "expected_max_streak": 5
        },
        
        "Meditate": {
            "description": "Practice mindfulness for 10 minutes",
            "periodicity": "daily",
            "start_date": start_date.strftime('%Y-%m-%d %H:%M:%S'),
            "completions": [
                # Week 1 - Learning the habit
                {"date": "2024-01-01", "streak": 1},
                {"date": "2024-01-03", "streak": 1},
                # Week 2 - More consistent
                {"date": "2024-01-08", "streak": 1},
                {"date": "2024-01-09", "streak": 2},
                {"date": "2024-01-10", "streak": 3},
                # Week 3 - Perfect week
                {"date": "2024-01-15", "streak": 1},
                {"date": "2024-01-16", "streak": 2},
                {"date": "2024-01-17", "streak": 3},
                {"date": "2024-01-18", "streak": 4},
                {"date": "2024-01-19", "streak": 5},
                {"date": "2024-01-20", "streak": 6},
                {"date": "2024-01-21", "streak": 7},
                # Week 4 - Maintained momentum
                {"date": "2024-01-22", "streak": 8},
                {"date": "2024-01-23", "streak": 9},
                {"date": "2024-01-24", "streak": 10}
            ],
            "expected_max_streak": 10
        },
        
        "Church": {
            "description": "Attend church service weekly",
            "periodicity": "weekly",
            "start_date": start_date.strftime('%Y-%m-%d %H:%M:%S'),
            "completions": [
                # Week 1
                {"date": "2024-01-07", "streak": 1},
                # Week 2
                {"date": "2024-01-14", "streak": 2},
                # Week 3 - Missed
                # Week 4
                {"date": "2024-01-28", "streak": 1}
            ],
            "expected_max_streak": 2
        }
    } 