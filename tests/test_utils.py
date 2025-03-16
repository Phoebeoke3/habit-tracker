import pytest
from utils import sort_habits

def test_sort_habits():
    """Test that sort_habits correctly sorts habits by streak count."""
    # Create test habits with different streak counts (at index 5)
    habits = [
        (1, "Habit1", "Desc1", "2023-01-01", 1, 3, "daily", None),
        (2, "Habit2", "Desc2", "2023-01-01", 1, 5, "daily", None),
        (3, "Habit3", "Desc3", "2023-01-01", 1, 1, "daily", None)
    ]
    
    # Convert to list for testing as sort_habits uses sort() which modifies in place
    habits_list = list(habits)
    
    # Call the function
    result = sort_habits(habits_list)
    
    # Verify the habits are sorted by streak count (index 5)
    assert habits_list[0][5] == 1
    assert habits_list[1][5] == 3
    assert habits_list[2][5] == 5
    
    # Test that the function returns None (since sort() returns None)
    assert result is None 