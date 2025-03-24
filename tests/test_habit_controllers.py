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
    last_completed = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
    mock_habit = (1, "Test Habit", "Test Description", "2023-01-01", 1, 5, "daily", last_completed)
    mock_cursor.fetchone.return_value = mock_habit
    
    # Reset commit call count before test
    mock_conn.commit.reset_mock()
    
    # Mark habit done
    with patch("builtins.print"):
        with patch("controllers.habit_controllers.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime.now()
            mock_datetime.strptime.return_value = datetime.strptime(last_completed, '%Y-%m-%d %H:%M:%S')
            mark_done(1)
    
    # Verify database operations
    assert mock_conn.execute.call_count >= 2  # At least 2 calls (SELECT and UPDATE)
    mock_conn.commit.assert_called_once()  # Should only commit once

def test_get_longest_streak(mock_db_connection):
    """Test getting longest streak considering both current and broken streaks."""
    mock_conn, mock_cursor = mock_db_connection
    
    # Test case 1: Current streak is higher
    mock_conn.execute.return_value = mock_cursor
    mock_cursor.fetchone.side_effect = [
        (5,),  # Current streak from habits table
        (3,),  # Max broken streak from streak_count table
    ]
    
    result = get_longest_streak(1)
    assert result == 5
    
    # Verify correct SQL queries were executed
    assert mock_conn.execute.call_count == 2
    mock_conn.execute.assert_any_call("SELECT streak_count FROM habits WHERE id = ?", (1,))
    mock_conn.execute.assert_any_call("SELECT MAX(count) FROM streak_count WHERE habit_id = ?", (1,))

def test_get_longest_streak_broken_higher(mock_db_connection):
    """Test getting longest streak when broken streak is higher."""
    mock_conn, mock_cursor = mock_db_connection
    
    mock_conn.execute.return_value = mock_cursor
    mock_cursor.fetchone.side_effect = [
        (3,),  # Current streak from habits table
        (7,),  # Max broken streak from streak_count table
    ]
    
    result = get_longest_streak(1)
    assert result == 7

def test_get_longest_streak_no_streaks(mock_db_connection):
    """Test getting longest streak when no streaks exist."""
    mock_conn, mock_cursor = mock_db_connection
    
    mock_conn.execute.return_value = mock_cursor
    mock_cursor.fetchone.side_effect = [
        None,  # No current streak
        (None,),  # No broken streaks
    ]
    
    result = get_longest_streak(1)
    assert result == 0

# def test_get_longest_streak_error(mock_db_connection):
#     """Test error handling in get_longest_streak."""
#     mock_conn, mock_cursor = mock_db_connection
    
#     # Reset execute mock before test
#     mock_conn.execute.reset_mock()
    
#     # Simulate database error
#     mock_conn.execute.side_effect = Exception("Database error")
    
#     # Patch rich_print instead of print
#     with patch("controllers.habit_controllers.rich_print") as mock_print:
#         result = get_longest_streak(1)
    
#     assert result == 0
#     mock_print.assert_called_once_with("[red]Error fetching highest streak: Database error[/red]") 