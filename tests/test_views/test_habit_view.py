import pytest
from unittest.mock import patch, MagicMock
from views.habit_views import (
    habits_view, add_habit_view, edit_habit_view, 
    delete_habit_view, track_habit_view, display_habits, view_longest_streak
)
from controllers.habit_controllers import (
    get_habits_by_user_id, create_habit, edit_habit, 
    delete_habit, mark_done, get_habit, get_longest_streak
)

@pytest.fixture
def mock_habits():
    """Fixture to provide mock habits"""
    return [
        (1, "Workout", "Exercise daily", "2024-01-01", 1, 10, "daily"),
        (2, "Read", "Read a book", "2024-01-02", 2, 5, "weekly"),
    ]

def test_habits_view(mock_habits):
    """Test the habits_view function"""
    with patch("controllers.habit_controllers.get_habits_by_user_id", return_value=mock_habits):
        with patch("builtins.input", return_value=""):
            habits_view(1)  # No assertions needed since it's just printing output

def test_add_habit_view():
    """Test the add_habit_view function"""
    with patch("controllers.habit_controllers.create_habit", return_value={"name": "Test Habit"}):
        with patch("builtins.input", side_effect=["Test Habit", "Test Description", ""]):  # Added input for continuation
            with patch("rich.prompt.Prompt.ask", return_value="daily"):
                add_habit_view(1)  # No assertion needed since it prints output

def test_edit_habit_view():
    """Test the edit_habit_view function"""
    mock_habit = {
        "id": "1", "name": "Workout", "description": "Exercise", "start_date": "2024-01-01",
        "user_id": 1, "streak_count": 10, "periodicity": "daily"
    }

    with patch("controllers.habit_controllers.get_habit", return_value=mock_habit):
        with patch("controllers.habit_controllers.edit_habit") as mock_edit:
            with patch("builtins.input", side_effect=["1", "", "", "weekly"]):
                periodicity = edit_habit_view(1)
                assert periodicity == "weekly", f"Expected 'weekly', got {periodicity}"
                mock_edit.assert_called_once()

def test_delete_habit_view():
    """Test the delete_habit_view function"""
    with patch("controllers.habit_controllers.get_habits_by_user_id", return_value=[(1, "Workout", "Exercise daily", "2024-01-01", 1, 10, "daily")]):
        with patch("controllers.habit_controllers.get_habit", return_value={"id": "1", "name": "Workout"}):  # ✅ Ensure habit exists
            with patch("controllers.habit_controllers.delete_habit") as mock_delete:
                with patch("builtins.input", return_value="1"):
                    delete_habit_view(1)
                    mock_delete.assert_called_once_with("1")

def test_track_habit_view():
    """Test the track_habit_view function"""
    mock_habit = {
        "id": "1", "name": "Workout", "description": "Exercise daily", "start_date": "2024-01-01",
        "user_id": 1, "streak_count": 10, "periodicity": "daily"
    }

    with patch("controllers.habit_controllers.get_habit", return_value=mock_habit):
        with patch("controllers.habit_controllers.mark_done") as mock_mark:
            with patch("builtins.input", return_value="1"):
                track_habit_view(1)
                mock_mark.assert_called_once_with("1")

def test_display_habits(mock_habits):
    """Test the display_habits function"""
    with patch("controllers.habit_controllers.get_habits_by_user_id", return_value=mock_habits):
        display_habits(1)  # No assertions needed, just checking output

def test_view_longest_streak():
    """Test the view_longest_streak function"""
    with patch("controllers.habit_controllers.get_longest_streak", return_value=15):
        with patch("builtins.input", return_value="1"):
            view_longest_streak()
