import pytest
from unittest.mock import patch, MagicMock
import sys
from views.main_views import main_view
from controllers.auth_controllers import logout


@pytest.fixture
def mock_user():
    return {"id": 1, "username": "testuser"}


# 🟢 Test: Display Habits
@patch("views.habit_views.habits_view", return_value=None)
@patch("builtins.input", return_value="1")
def test_main_view_habits(mock_input, mock_habits_view, mock_user):
    main_view(mock_user)
    mock_habits_view.assert_called_once_with(str(mock_user["id"]))


# 🟢 Test: Add Habit
@patch("views.habit_views.add_habit_view", return_value=None)
@patch("builtins.input", return_value="2")
def test_main_view_add_habit(mock_input, mock_add_habit_view, mock_user):
    main_view(mock_user)
    mock_add_habit_view.assert_called_once_with(str(mock_user["id"]))


# 🟢 Test: Edit Habit
@patch("views.habit_views.edit_habit_view", return_value=None)
@patch("builtins.input", return_value="3")
def test_main_view_edit_habit(mock_input, mock_edit_habit_view, mock_user):
    main_view(mock_user)
    mock_edit_habit_view.assert_called_once_with(str(mock_user["id"]))


# 🟢 Test: Delete Habit
@patch("views.habit_views.delete_habit_view", return_value=None)
@patch("builtins.input", return_value="4")
def test_main_view_delete_habit(mock_input, mock_delete_habit_view, mock_user):
    main_view(mock_user)
    mock_delete_habit_view.assert_called_once_with(str(mock_user["id"]))


# 🟢 Test: Track Habit
@patch("views.habit_views.track_habit_view", return_value=None)
@patch("builtins.input", return_value="5")
def test_main_view_track_habit(mock_input, mock_track_habit_view, mock_user):
    main_view(mock_user)
    mock_track_habit_view.assert_called_once_with(str(mock_user["id"]))


# 🟢 Test: Analytics View
@patch("views.analytics_views.analytics_view", return_value=None)
@patch("builtins.input", return_value="6")
def test_main_view_analytics(mock_input, mock_analytics_view, mock_user):
    main_view(mock_user)
    mock_analytics_view.assert_called_once_with(str(mock_user["id"]))


# 🟢 Test: Logout
@patch("controllers.auth_controllers.logout", return_value=None)
@patch("builtins.input", return_value="logout")
def test_main_view_logout(mock_input, mock_logout, mock_user):
    result = main_view(mock_user)
    mock_logout.assert_called_once()  # ✅ Ensures logout was called once
    assert result is None  # ✅ Ensures main_view() returns None after logout


# 🟢 Test: Exit Command (sys.exit)
@patch("builtins.input", return_value="quit")
@patch("sys.exit")
def test_main_view_exit(mock_exit, mock_input, mock_user):
    with pytest.raises(SystemExit):  # ✅ Expecting SystemExit
        main_view(mock_user)
    mock_exit.assert_called_once()  # ✅ Ensures sys.exit() was called
