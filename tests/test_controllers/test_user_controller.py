import pytest
from unittest.mock import patch, MagicMock
from controllers.user_controllers import (
    get_user,
    get_user_by_username,
    create_user,
    update_user,
    delete_user,
    all_users
)


# ✅ Test Case 1: Get User by ID (Success)
@patch("controllers.user_controllers.conn")
def test_get_user(mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1, "testuser", "password123")
    mock_conn.execute.return_value = mock_cursor

    get_user(1)  # Call the function

    mock_conn.execute.assert_called_once_with("SELECT * FROM users WHERE id = ?", (1,))
    mock_cursor.fetchone.assert_called_once()


# ✅ Test Case 2: Get User by Username (Success)
@patch("controllers.user_controllers.conn")
def test_get_user_by_username(mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1, "testuser", "password123")
    mock_conn.execute.return_value = mock_cursor

    user = get_user_by_username("testuser")

    assert user is not None
    assert user[1] == "testuser"
    mock_conn.execute.assert_called_once_with("SELECT * FROM users WHERE username = ?", ("testuser",))
    mock_cursor.fetchone.assert_called_once()


# ✅ Test Case 3: Get User by Username (User Not Found)
@patch("controllers.user_controllers.conn")
def test_get_user_by_username_not_found(mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.execute.return_value = mock_cursor

    user = get_user_by_username("nonexistent")

    assert user is None
    mock_conn.execute.assert_called_once_with("SELECT * FROM users WHERE username = ?", ("nonexistent",))


# ✅ Test Case 4: Create User (Success)
@patch("controllers.user_controllers.conn")
def test_create_user(mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None  # No existing user found
    mock_cursor.lastrowid = 1  # Simulating new user ID
    mock_conn.cursor.return_value = mock_cursor

    user = create_user("newuser", "securepassword")

    assert user is not None
    assert user["id"] == 1
    assert user["username"] == "newuser"
    mock_conn.cursor().execute.assert_any_call("SELECT id FROM users WHERE username = ?", ("newuser",))
    mock_conn.cursor().execute.assert_any_call("INSERT INTO users (username, password) VALUES (?, ?)", ("newuser", "securepassword"))


# ✅ Test Case 5: Create User (Username Already Exists)
@patch("controllers.user_controllers.conn")
def test_create_user_username_taken(mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)  # Simulating existing user
    mock_conn.cursor.return_value = mock_cursor

    user = create_user("existinguser", "securepassword")

    assert user is None  # User creation should fail
    mock_conn.cursor().execute.assert_called_once_with("SELECT id FROM users WHERE username = ?", ("existinguser",))


# ✅ Test Case 6: Update User (Success)
@patch("models.user.User.update")
def test_update_user(mock_update):
    update_user(1, "updateduser", "newpassword")

    mock_update.assert_called_once_with(1, "updateduser", "newpassword")


# ✅ Test Case 7: Get All Users
@patch("controllers.user_controllers.conn")
def test_all_users(mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        (1, "user1"),
        (2, "user2"),
    ]
    mock_conn.execute.return_value = mock_cursor

    all_users()

    mock_conn.execute.assert_called_once_with("SELECT * FROM users")
    mock_cursor.fetchall.assert_called_once()


# ✅ Test Case 8: Delete User (Success)
@patch("controllers.user_controllers.conn")
def test_delete_user(mock_conn):
    delete_user(1)

    mock_conn.execute.assert_called_once_with("DELETE FROM users WHERE id = ?", (1,))
    mock_conn.commit.assert_called_once()
