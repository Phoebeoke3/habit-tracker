import pytest
import json
import os
from unittest.mock import patch, MagicMock, mock_open
from controllers.auth_controllers import login, register, logout

@pytest.fixture
def mock_get_user():
    with patch('controllers.auth_controllers.get_user_by_username') as mock:
        yield mock

@pytest.fixture
def mock_create_user():
    with patch('controllers.auth_controllers.create_user') as mock:
        yield mock

@pytest.fixture
def mock_assign_habits():
    with patch('controllers.auth_controllers.assign_predefined_habits') as mock:
        yield mock

def test_login_success(mock_get_user):
    """Test successful login."""
    # Mock user data
    mock_user = (1, "testuser", "testpass")
    mock_get_user.return_value = mock_user
    
    # Mock file operations
    m_open = mock_open()
    with patch("builtins.open", m_open):
        result = login("testuser", "testpass")
    
    # Verify result
    assert result is not None
    assert result["id"] == 1
    assert result["username"] == "testuser"
    assert result["password"] == "testpass"
    
    # Verify file operations
    m_open.assert_called_once_with("session.json", "w")
    m_open().write.assert_called_once()

def test_login_failure(mock_get_user):
    """Test login with wrong credentials."""
    # Mock user data
    mock_user = (1, "testuser", "testpass")
    mock_get_user.return_value = mock_user
    
    # Test with wrong password
    result = login("testuser", "wrongpass")
    assert result is None
    
    # Test with non-existent user
    mock_get_user.return_value = None
    result = login("nonexistent", "testpass")
    assert result is None

def test_register_success(mock_create_user, mock_assign_habits):
    """Test successful user registration."""
    # Mock user creation
    mock_user = {"id": 1, "username": "newuser"}
    mock_create_user.return_value = mock_user
    
    # Mock print to avoid side effects
    with patch("builtins.print"):
        result = register("newuser", "newpass")
    
    # Verify result
    assert result == mock_user
    mock_create_user.assert_called_once_with("newuser", "newpass")
    mock_assign_habits.assert_called_once_with(1)

def test_register_failure(mock_create_user):
    """Test registration failure."""
    # Mock failed user creation
    mock_create_user.return_value = None
    
    # Mock print to avoid side effects
    with patch("builtins.print"):
        result = register("existinguser", "pass")
    
    # Verify result
    assert result is None
    mock_create_user.assert_called_once_with("existinguser", "pass")

def test_logout():
    """Test logout functionality."""
    # Mock file operations
    m_open = mock_open()
    with patch("builtins.open", m_open):
        result = logout()
    
    # Verify file operations
    m_open.assert_called_once_with("session.json", "w")
    m_open().write.assert_called_once_with("{}")
    assert result is None 