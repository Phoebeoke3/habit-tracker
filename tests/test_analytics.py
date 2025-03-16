import pytest
from unittest.mock import patch, MagicMock
from controllers.analytics import (
    get_all_tracked_habits, all_habits_by_periodicity,
    longest_habit_streak, view_longest_streak
)

def test_get_all_tracked_habits():
    """Test getting all tracked habits (streak > 0)."""
    # Mock habits data
    mock_habits = [
        (1, "Habit 1", "Desc 1", "2023-01-01", 1, 5, "daily", None),  # Tracked
        (2, "Habit 2", "Desc 2", "2023-01-01", 1, 0, "daily", None),  # Not tracked
        (3, "Habit 3", "Desc 3", "2023-01-01", 1, 3, "weekly", None)  # Tracked
    ]
    
    # Mock get_habits_by_user_id
    with patch("controllers.analytics.get_habits_by_user_id", return_value=mock_habits):
        tracked_habits = get_all_tracked_habits(1)
    
    # Verify only habits with streak > 0 are returned
    assert len(tracked_habits) == 2
    assert tracked_habits[0][0] == 1
    assert tracked_habits[1][0] == 3

def test_all_habits_by_periodicity():
    """Test getting habits by periodicity."""
    # Mock habits data
    mock_habits = [
        (1, "Habit 1", "Desc 1", "2023-01-01", 1, 5, "daily", None)
    ]
    
    # Mock get_habits_by_periodicity
    with patch("controllers.analytics.get_habits_by_periodicity", return_value=mock_habits):
        habits = all_habits_by_periodicity(1, "daily")
    
    # Verify returned habits
    assert habits == mock_habits

def test_longest_habit_streak():
    """Test getting habit with longest streak."""
    # Mock habits data with different streak counts
    mock_habits = [
        (1, "Habit 1", "Desc 1", "2023-01-01", 1, 5, "daily", None),
        (2, "Habit 2", "Desc 2", "2023-01-01", 1, 10, "daily", None),  # Longest
        (3, "Habit 3", "Desc 3", "2023-01-01", 1, 3, "weekly", None)
    ]
    
    # Mock get_habits_by_user_id
    with patch("controllers.analytics.get_habits_by_user_id", return_value=mock_habits):
        longest = longest_habit_streak(1)
    
    # Verify the habit with longest streak is returned
    assert longest[0] == 2
    assert longest[5] == 10

def test_view_longest_streak():
    """Test view_longest_streak function."""
    # Mock input and get_longest_streak
    with patch("builtins.input", return_value="1"):
        with patch("controllers.analytics.get_longest_streak", return_value=7):
            with patch("builtins.print") as mock_print:
                view_longest_streak()
    
    # Verify print was called with expected message
    mock_print.assert_called_with("[green]Longest streak for habit 1: 7 days[/green]") 