import pytest
from unittest.mock import patch, MagicMock
from models.user import User
import sqlite3

def test_user_init():
    """Test User initialization."""
    user = User("testuser", "testpass")
    assert user.username == "testuser"
    assert user.password == "testpass"

def test_user_save_success(mock_db_connection):
    """Test successful user save."""
    mock_conn, mock_cursor = mock_db_connection
    
    # Create and save user
    user = User("testuser", "password")
    
    with patch("rich.print") as mock_rich_print:
        with patch("builtins.print") as mock_print:
            user.save()
    
    # Verify database operations - check conn.execute instead of cursor.execute
    mock_conn.execute.assert_called_once()
    mock_conn.commit.assert_called_once()

def test_user_save_integrity_error(mock_db_connection):
    """Test user save with integrity error."""
    mock_conn, mock_cursor = mock_db_connection
    
    # Mock integrity error - change to mock conn.execute
    from sqlite3 import IntegrityError
    mock_conn.execute.side_effect = IntegrityError("UNIQUE constraint failed")
    
    # Create and save user
    user = User("existinguser", "password")
    
    with patch("rich.print") as mock_rich_print:
        with patch("builtins.print") as mock_print:
            user.save()
        
    assert user.username == "existinguser"
