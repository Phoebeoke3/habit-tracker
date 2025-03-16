import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from controllers.habit_controllers import (
    get_habit, get_habits_by_user_id, get_habits_by_periodicity,
    create_habit, delete_habit, edit_habit, mark_done, get_longest_streak,
    assign_predefined_habits
)

def test_get_habit_success(mock_db_connection):
    """Test successfully getting a habit."""
    mock_conn, mock_cursor = mock_db_connection
    
    # Mock habit data
    mock_habit = (1, "Test Habit", "Test Description", "2023-01-01", 1, 5, "daily", "2023-01-05")
    mock_cursor.fetchone.return_value = mock_habit
    
    # Get habit
    habit = get_habit(1)
    
    # Verify database operation
    mock_conn.execute.assert_called_once()
    
    # Verify returned habit
    assert habit["id"] == 1
    assert habit["name"] == "Test Habit"
    assert habit["description"] == "Test Description"
    assert habit["streak_count"] == 5
    assert habit["periodicity"] == "daily"

def test_get_habit_failure(mock_db_connection):
    """Test getting a non-existent habit."""
    mock_conn, mock_cursor = mock_db_connection
    
    # Mock no habit found
    mock_cursor.fetchone.return_value = None
    
    # Attempt to get non-existent habit
    with pytest.raises(Exception) as exc_info:
        get_habit(999)
    
    assert "Habit with ID 999 is not found" in str(exc_info.value)

def test_get_habits_by_user_id(mock_db_connection):
    """Test getting habits by user ID."""
    mock_conn, mock_cursor = mock_db_connection
    
    # Mock habits data
    mock_habits = [
        (1, "Habit 1", "Desc 1", "2023-01-01", 1, 5, "daily", None),
        (2, "Habit 2", "Desc 2", "2023-01-01", 1, 3, "weekly", None)
    ]
    mock_cursor.fetchall.return_value = mock_habits
    
    # Get habits
    habits = get_habits_by_user_id(1)
    
    # Verify database operation
    mock_conn.execute.assert_called_once()
    
    # Verify returned habits
    assert habits == mock_habits

def test_get_habits_by_periodicity(mock_db_connection):
    """Test getting habits by periodicity."""
    mock_conn, mock_cursor = mock_db_connection
    
    # Mock habits data
    mock_habits = [
        (1, "Habit 1", "Desc 1", "2023-01-01", 1, 5, "daily", None)
    ]
    mock_cursor.fetchall.return_value = mock_habits
    
    # Get habits
    habits = get_habits_by_periodicity(1, "daily")
    
    # Verify database operation
    mock_conn.execute.assert_called_once()
    
    # Verify returned habits
    assert habits == mock_habits

def test_create_habit(mock_db_connection):
    """Test creating a habit."""
    mock_conn, mock_cursor = mock_db_connection
    
    # Create habit
    with patch("controllers.habit_controllers.datetime") as mock_datetime:
        mock_datetime.now.return_value.strftime.return_value = "2023-01-01 12:00:00"
        habit = create_habit("New Habit", "New Description", 1, "daily")
    
    # Verify database operations
    mock_conn.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    
    # Verify returned habit
    assert habit["name"] == "New Habit"
    assert habit["description"] == "New Description"
    assert habit["user_id"] == 1
    assert habit["periodicity"] == "daily"
    assert habit["start_date"] == "2023-01-01 12:00:00"

def test_mark_done_new_streak(mock_db_connection):
    """Test marking a habit done for the first time."""
    mock_conn, mock_cursor = mock_db_connection
    
    # Mock habit data with streak_count 0
    mock_habit = (1, "Test Habit", "Test Description", "2023-01-01", 1, 0, "daily", None)
    mock_cursor.fetchone.return_value = mock_habit
    
    # Mark habit done
    with patch("builtins.print"):
        with patch("controllers.habit_controllers.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 1, 5)
            mark_done(1)
    
    # Verify database operations
    assert mock_conn.execute.call_count == 2  # SELECT and UPDATE
    mock_conn.commit.assert_called_once()
    
    # Verify habit was updated with streak_count 1
    assert mock_conn.execute.call_args_list[1][0][1][0] == 1  # streak_count in UPDATE

def test_mark_done_continuing_streak(mock_db_connection):
    """Test marking a habit done continuing a streak."""
    mock_conn, mock_cursor = mock_db_connection
    
    # Mock habit data with existing streak
    # Use a date from several days ago to avoid "already completed today" message
    last_completed = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
    mock_habit = (1, "Test Habit", "Test Description", "2023-01-01", 1, 5, "daily", last_completed)
    mock_cursor.fetchone.return_value = mock_habit
    
    # Mark habit done
    with patch("builtins.print"):
        with patch("controllers.habit_controllers.datetime") as mock_datetime:
            # Set current date to a different day than last completion
            mock_datetime.now.return_value = datetime.now()
            mock_datetime.strptime.return_value = datetime.strptime(last_completed, '%Y-%m-%d %H:%M:%S')
            mark_done(1)
    
    # Verify database operations - check conn.execute instead of cursor.execute
    assert mock_conn.execute.call_count >= 2  # At least 2 calls (SELECT and UPDATE)
    mock_conn.commit.assert_called_once()

def test_get_longest_streak(mock_db_connection):
    """Test getting the longest streak for a habit."""
    mock_conn, mock_cursor = mock_db_connection
    
    # Mock completion dates
    mock_dates = [
        ("2023-01-01 12:00:00",),
        ("2023-01-02 12:00:00",),
        ("2023-01-03 12:00:00",),
        ("2023-01-05 12:00:00",),  # Gap here
        ("2023-01-06 12:00:00",)
    ]
    mock_cursor.fetchall.return_value = mock_dates
    
    # Get longest streak
    with patch("controllers.habit_controllers.datetime") as mock_datetime:
        mock_datetime.strptime.side_effect = lambda date, fmt: datetime.strptime(date, fmt)
        longest_streak = get_longest_streak(1)
    
    # Verify database operation
    mock_conn.execute.assert_called_once()
    
    # Verify returned streak
    assert longest_streak == 3  # The first 3 dates are consecutive 