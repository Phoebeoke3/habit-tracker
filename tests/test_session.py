import pytest
import json
from unittest.mock import patch, mock_open
from utils.session import get_session, set_session

def test_get_session_existing_file():
    """Test getting session when file exists."""
    # Mock existing session file
    mock_content = '{"id": 1, "username": "testuser"}'
    with patch("builtins.open", mock_open(read_data=mock_content)):
        session = get_session()
    
    assert session == {"id": 1, "username": "testuser"}

def test_get_session_file_not_found():
    """Test getting session when file doesn't exist."""
    # Mock file not found error
    m_open = mock_open()
    m_open.side_effect = [FileNotFoundError, mock_open().return_value]
    
    with patch("builtins.open", m_open):
        session = get_session()
    
    # Verify a new file was created with empty content
    assert m_open.call_count == 2
    m_open.assert_any_call("session.json", "r")
    m_open.assert_any_call("session.json", "w")
    assert session == {}

def test_set_session():
    """Test setting a session."""
    # Mock user data
    user = {"id": 1, "username": "testuser"}
    
    # Mock file operations
    m_open = mock_open()
    with patch("builtins.open", m_open):
        set_session(user)
    
    # Verify file operations
    m_open.assert_called_once_with("session.json", "w")
    expected_json = json.dumps(user)
    m_open().write.assert_called_once_with(expected_json)

def test_set_session_exception():
    """Test setting a session with exception."""
    # Mock user data
    user = {"id": 1, "username": "testuser"}
    
    # Mock file operations with exception
    m_open = mock_open()
    m_open.side_effect = Exception("Mocked error")
    
    with patch("builtins.open", m_open):
        # Should not raise exception
        set_session(user) 