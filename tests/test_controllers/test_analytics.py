import pytest
from unittest.mock import patch, MagicMock
from analytics import (
    get_all_tracked_habits,
    all_habits_by_periodicity,
    longest_habit_streak,
    view_longest_streak
)
from controllers.habit_controllers import (
    get_habits_by_periodicity,
    get_habits_by_user_id,
    get_longest_streak
)


# ✅ Test Case 1: Get All Tracked Habits (Only Habits with Streak > 0)
@patch("controllers.habit_controllers.get_habits_by_user_id")
def test_get_all_tracked_habits(mock_get_habits):
    mock_get_habits.return_value = [
        (1, "Workout", "Exercise daily", "2024-01-01", 1, 5, "daily"),
        (2, "Read", "Read for 20 minutes", "2024-01-01", 1, 0, "daily"),  # No streak
        (3, "Meditate", "Mindfulness practice", "2024-01-01", 1, 3, "daily"),
    ]

    tracked_habits = get_all_tracked_habits(1)

    assert len(tracked_habits) == 2
    assert all(habit[5] > 0 for habit in tracked_habits)
    mock_get_habits.assert_called_once_with(1)


# ✅ Test Case 2: Get All Habits by Periodicity (Success)
@patch("controllers.habit_controllers.get_habits_by_periodicity")
def test_all_habits_by_periodicity(mock_get_habits):
    mock_get_habits.return_value = [
        (1, "Workout", "Exercise daily", "2024-01-01", 1, 5, "daily"),
        (2, "Read", "Read for 20 minutes", "2024-01-01", 1, 2, "daily"),
    ]

    habits = all_habits_by_periodicity(1, "daily")

    assert len(habits) == 2
    mock_get_habits.assert_called_once_with(1, "daily")


# ✅ Test Case 3: Get Longest Habit Streak
@patch("controllers.habit_controllers.get_habits_by_user_id")
def test_longest_habit_streak(mock_get_habits):
    mock_get_habits.return_value = [
        (1, "Workout", "Exercise daily", "2024-01-01", 1, 5, "daily"),
        (2, "Read", "Read for 20 minutes", "2024-01-01", 1, 10, "daily"),
        (3, "Meditate", "Mindfulness practice", "2024-01-01", 1, 3, "daily"),
    ]

    longest_streak_habit = longest_habit_streak(1)

    assert longest_streak_habit[5] == 10  # Should return the habit with the longest streak
    mock_get_habits.assert_called_once_with(1)


# ✅ Test Case 4: View Longest Streak (Mocking Input)
@patch("builtins.input", return_value="1")
@patch("controllers.habit_controllers.get_longest_streak", return_value=15)
def test_view_longest_streak(mock_get_streak, mock_input, capsys):
    view_longest_streak()  # Call the function

    mock_input.assert_called_once()
    mock_get_streak.assert_called_once_with("1")

    captured = capsys.readouterr()
    assert "Longest streak for habit 1: 15 days" in captured.out
