import json
import pytest
from unittest.mock import patch, mock_open
from controllers.auth_controllers import login, register, logout

# ✅ Test Case 1: Successful Login
@patch("controllers.user_controllers.get_user_by_username")
@patch("builtins.open", new_callable=mock_open)
def test_login_success(mock_open_file, mock_get_user):
    # 🔹 Ensure mock returns correct format
    mock_get_user.return_value = (1, "testuser", "password123")

    user = login("testuser", "password123")

    assert user is not None, f"Login should return a user dictionary, but got {user}"
    assert user["username"] == "testuser"
    assert user["password"] == "password123"

    # ✅ Ensure session file is updated
    mock_open_file.assert_called_once_with("session.json", "w")
    mock_open_file().write.assert_called_once()


# ✅ Test Case 2: Failed Login - Invalid Credentials
@patch("controllers.user_controllers.get_user_by_username")
def test_login_fail_invalid_credentials(mock_get_user):
    mock_get_user.return_value = (1, "testuser", "password123")

    user = login("testuser", "wrongpassword")

    assert user is None


# ✅ Test Case 3: Failed Login - User Not Found
@patch("controllers.user_controllers.get_user_by_username")
def test_login_fail_user_not_found(mock_get_user):
    mock_get_user.return_value = None  # Simulating user not found

    user = login("nonexistentuser", "password123")

    assert user is None


# ✅ Test Case 4: Successful Registration
@patch("controllers.user_controllers.create_user")
@patch("controllers.habit_controllers.assign_predefined_habits")
def test_register_success(mock_assign_habits, mock_create_user):
    # 🔹 Ensure mock returns valid user dictionary
    mock_create_user.return_value = {"id": 9, "username": "newuser", "password": "securepass"}

    user = register("newuser", "securepass")

    assert user is not None, f"Register should return a user dictionary, but got {user}"
    assert user["username"] == "newuser"
    assert user["id"] == 9

    # ✅ Ensure predefined habits are assigned
    mock_assign_habits.assert_called_once_with(user["id"])


# ✅ Test Case 5: Failed Registration
@patch("controllers.user_controllers.create_user", return_value=None)
def test_register_fail(mock_create_user):
    user = register("newuser", "securepass")

    assert user is None


# ✅ Test Case 6: Successful Logout
@patch("builtins.open", new_callable=mock_open)
def test_logout(mock_open_file):
    logout()

    mock_open_file.assert_called_once_with("session.json", "w")
    mock_open_file().write.assert_called_once_with("{}")
