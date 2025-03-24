import pytest
from datetime import datetime
from utils.test_data_generator import generate_predefined_test_data
from unittest.mock import patch

def test_generate_predefined_test_data(test_db):
    """Test generating predefined test data."""
    # Create test user
    cursor = test_db.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("testuser", "password")
    )
    test_db.commit()
    user_id = cursor.lastrowid
    
    # Patch the database connection for the generator
    with patch('utils.test_data_generator.conn', test_db), \
         patch('utils.test_data_generator.cursor', test_db.cursor()):
        # Generate test data
        habits = generate_predefined_test_data(user_id)
    
    assert habits is not None
    assert len(habits) == 5  # All 5 predefined habits
    
    # Verify each habit's data
    expected_data = {
        "Drink Water": {"max_streak": 12},
        "Gym": {"max_streak": 3},
        "Read": {"max_streak": 5},
        "Meditate": {"max_streak": 10},
        "Church": {"max_streak": 2}
    }
    
    for habit in habits:
        habit_name = habit["name"]
        assert habit_name in expected_data
        assert habit["max_streak"] == expected_data[habit_name]["max_streak"]
        
        # Verify streak history exists
        cursor.execute(
            "SELECT COUNT(*) FROM streak_count WHERE habit_id = ?", 
            (habit["id"],)
        )
        completion_count = cursor.fetchone()[0]
        assert completion_count > 0

def test_generate_predefined_test_data_error_handling(test_db):
    """Test error handling in test data generation."""
    # Test with non-existent user ID
    with patch('utils.test_data_generator.conn', test_db), \
         patch('utils.test_data_generator.cursor', test_db.cursor()):
        result = generate_predefined_test_data(999)
        assert result is None

def test_generate_predefined_test_data_db_error(test_db):
    """Test database error handling."""
    cursor = test_db.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("testuser", "password")
    )
    test_db.commit()
    user_id = cursor.lastrowid

    # Simulate database error by dropping the habits table
    cursor.execute("DROP TABLE habits")
    
    with patch('utils.test_data_generator.conn', test_db), \
         patch('utils.test_data_generator.cursor', test_db.cursor()):
        result = generate_predefined_test_data(user_id)
        assert result is None 