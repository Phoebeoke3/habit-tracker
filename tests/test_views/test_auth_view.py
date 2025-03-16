import pytest
import sys
from unittest.mock import patch
from views.auth_views import auth_view, login_view, register_view
from controllers.auth_controllers import login, register

# 🟢 Test: Authentication View - Login
@patch("views.auth_views.login_view", return_value={"id": 1, "username": "testuser"})
@patch("rich.prompt.Prompt.ask", return_value="login")
def test_auth_view_login(mock_prompt, mock_login_view):
    result = auth_view()
    assert result == {"id": 1, "username": "testuser"}  # ✅ Ensure login_view() is called


# 🟢 Test: Authentication View - Register
@patch("views.auth_views.register_view", return_value={"id": 2, "username": "newuser"})
@patch("rich.prompt.Prompt.ask", return_value="register")
def test_auth_view_register(mock_prompt, mock_register_view):
    result = auth_view()
    assert result == {"id": 2, "username": "newuser"}  # ✅ Ensure register_view() is called


# 🟢 Test: Authentication View - Exit
@patch("sys.exit")
@patch("rich.prompt.Prompt.ask", return_value="exit")
def test_auth_view_exit(mock_prompt, mock_exit):
    with pytest.raises(SystemExit):  # ✅ Expecting SystemExit
        auth_view()
    mock_exit.assert_called_once()  # ✅ Ensures sys.exit() was called


# 🟢 Test: Login View - Successful Login
@patch("controllers.auth_controllers.login", return_value={"id": 1, "username": "testuser"})
@patch("pwinput.pwinput", return_value="password123")
@patch("rich.prompt.Prompt.ask", return_value="testuser")
def test_login_view_success(mock_prompt, mock_pwinput, mock_login):
    result = login_view()
    assert result == {"id": 1, "username": "testuser"}  # ✅ Ensure login function returns a user


# 🔴 Test: Login View - Failed Login
@patch("controllers.auth_controllers.login", return_value=None)  # ❌ Simulate failed login
@patch("pwinput.pwinput", return_value="wrongpassword")
@patch("rich.prompt.Prompt.ask", return_value="testuser")
def test_login_view_fail(mock_prompt, mock_pwinput, mock_login):
    result = login_view()
    assert result is None  # ✅ Ensure login returns None on failure


# 🟢 Test: Register View - Successful Registration
@patch("controllers.auth_controllers.register", return_value={"id": 2, "username": "newuser"})
@patch("controllers.auth_controllers.login", return_value={"id": 2, "username": "newuser"})  # Auto-login after registration
@patch("pwinput.pwinput", return_value="securepass")
@patch("rich.prompt.Prompt.ask", return_value="newuser")
def test_register_view_success(mock_prompt, mock_pwinput, mock_register, mock_login):
    result = register_view()
    assert result == {"id": 2, "username": "newuser"}  # ✅ Ensure registration auto-logs in the user


# 🔴 Test: Register View - Failed Registration
@patch("controllers.auth_controllers.register", return_value=None)  # ❌ Simulate registration failure
@patch("controllers.auth_controllers.login", return_value=None)  # ❌ Simulate failed login after failed registration
@patch("pwinput.pwinput", return_value="weakpass")
@patch("rich.prompt.Prompt.ask", return_value="newuser")
def test_register_view_fail(mock_prompt, mock_pwinput, mock_register, mock_login):
    result = register_view()
    assert result is None  # ✅ Ensure failed registration prevents login
