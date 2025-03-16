import pytest
from unittest.mock import patch, MagicMock
from models.habit import Habit
from datetime import datetime

def test_habit_init():
    """Test Habit initialization."""
    habit = Habit("Test Habit", "Test Description", 1, "daily")
    
    assert habit.name == "Test Habit"
    assert habit.description == "Test Description"
    assert habit.user_id == 1
    assert habit.periodicity == "daily"
    assert habit.streak_count == 0
    assert habit.last_completed_date is None
    assert isinstance(habit.start_date, datetime)

def test_habit_save_success(mock_db_connection):
    """Test successful habit save."""
    mock_conn, mock_cursor = mock_db_connection
    
    # Create and save habit
    habit = Habit("Test Habit", "Test Description", 1, "daily")
    
    with patch("builtins.print"):
        habit.save()
    
    # Verify database operations - using cursor.execute not conn.execute
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()

def test_habit_save_integrity_error(mock_db_connection):
    """Test habit save with integrity error."""
    mock_conn, mock_cursor = mock_db_connection
    
    # Mock integrity error
    from sqlite3 import IntegrityError
    mock_cursor.execute.side_effect = IntegrityError("UNIQUE constraint failed")
    
    # Create and save habit
    habit = Habit("Test Habit", "Test Description", 1, "daily")
    
    assert habit.name == "Test Habit"

def test_habit_update(mock_db_connection):
    """Test habit update method."""
    mock_conn, mock_cursor = mock_db_connection
    
    # Mock habit retrieval
    mock_cursor.fetchone.return_value = (
        1, "Old Name", "Old Description", "2023-01-01", 1, 5, "daily", None
    )
    
    # Create habit and update it
    habit = Habit("Ignored", "Ignored", 1, "daily")
    
    with patch("builtins.print"):
        habit.update(1, "New Name", "New Description", "2023-02-01", "2023-12-15", 2)
    
    # Verify database operations
    assert mock_cursor.execute.call_count == 2  # SELECT and UPDATE
    mock_conn.commit.assert_called_once() 