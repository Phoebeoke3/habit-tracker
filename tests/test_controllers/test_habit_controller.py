import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from controllers.habit_controllers import (
    get_habit, get_habits_by_user_id, get_habits_by_periodicity, create_habit,
    delete_habit, edit_habit, mark_done, get_longest_streak
)

### ✅ Mock database connection
@pytest.fixture
def mock_db():
    with patch("controllers.habit_controllers.conn") as mock_conn:
        yield mock_conn


### ✅ Test `get_habit`
def test_get_habit(mock_db):
    """Test fetching a habit by ID"""
    mock_db.execute.return_value.fetchone.return_value = (
        1, "Workout", "Exercise daily", "2024-01-01", 1, 5, "daily", "2024-03-10"
    )

    habit = get_habit(1)
    assert habit["id"] == 1
    assert habit["name"] == "Workout"
    assert habit["streak_count"] == 5

    mock_db.execute.assert_called_once_with("SELECT * FROM habits WHERE id = ?", (1,))


def test_get_habit_not_found(mock_db):
    """Test when habit ID does not exist"""
    mock_db.execute.return_value.fetchone.return_value = None

    with pytest.raises(Exception, match="Habit with ID 1 is not found"):
        get_habit(1)


### ✅ Test `get_habits_by_user_id`
def test_get_habits_by_user_id(mock_db):
    """Test fetching habits for a user"""
    mock_db.execute.return_value.fetchall.return_value = [
        (1, "Workout", "Exercise daily", "2024-01-01", 1, 5, "daily", "2024-03-10"),
        (2, "Read", "Read for 30 minutes", "2024-01-01", 1, 3, "daily", "2024-03-10")
    ]

    habits = get_habits_by_user_id(1)
    assert len(habits) == 2
    assert habits[0][1] == "Workout"
    assert habits[1][1] == "Read"

    mock_db.execute.assert_called_once_with("SELECT * FROM habits WHERE user_id = ? OR user_id IS NULL", (1,))


### ✅ Test `create_habit`
def test_create_habit(mock_db):
    """Test creating a new habit"""
    mock_db.execute.return_value = None  # Simulate successful DB execution

    habit = create_habit("Meditate", "Practice mindfulness", 1, "daily")
    assert habit["name"] == "Meditate"
    assert habit["periodicity"] == "daily"

    mock_db.execute.assert_called_once()
    mock_db.commit.assert_called_once()


### ✅ Test `edit_habit`
def test_edit_habit(mock_db):
    """Test editing an existing habit"""
    edit_habit(1, "Morning Run", "Run 5km every day", "daily")

    mock_db.execute.assert_called_once_with(
        "UPDATE habits SET name = ?, description = ?, periodicity = ? WHERE id = ?",
        ("Morning Run", "Run 5km every day", "daily", 1)
    )
    mock_db.commit.assert_called_once()


### ✅ Test `delete_habit`
def test_delete_habit(mock_db):
    """Test deleting a habit"""
    delete_habit(1)

    mock_db.execute.assert_called_once_with("DELETE FROM habits WHERE id = ?", (1,))
    mock_db.commit.assert_called_once()


### ✅ Test `mark_done`
def test_mark_done(mock_db):
    """Test marking a habit as done"""
    # ✅ Provide a full timestamp with time and microseconds
    mock_db.execute.return_value.fetchone.return_value = (
        1, "Workout", "Exercise daily", "2024-01-01", 1, 5, "daily", "2024-03-09 12:00:00.000000"
    )

    mark_done(1)

    mock_db.execute.assert_called_with(
        "UPDATE habits SET streak_count = ?, last_completed_date = ? WHERE id = ?",
        (6, mock_db.execute.call_args[0][1], 1)
    )
    mock_db.commit.assert_called_once()


def test_mark_done_habit_not_found(mock_db):
    """Test marking a non-existing habit as done"""
    mock_db.execute.return_value.fetchone.return_value = None

    mark_done(1)

    mock_db.execute.assert_called_once_with("SELECT * FROM habits WHERE id = ?", (1,))


### ✅ Test `get_longest_streak`
def test_get_longest_streak(mock_db):
    """Test retrieving longest streak of a habit"""
    mock_db.execute.return_value.fetchall.return_value = [
        ("2024-03-01 10:00:00",), ("2024-03-02 10:00:00",), ("2024-03-03 10:00:00",)
    ]

    streak = get_longest_streak(1)
    assert streak == 3

    mock_db.execute.assert_called_once_with(
        "SELECT last_completed_date FROM habit_completions WHERE habit_id = ? ORDER BY last_completed_date ASC",
        (1,)
    )


def test_get_longest_streak_no_completions(mock_db):
    """Test retrieving longest streak when no completions exist"""
    mock_db.execute.return_value.fetchall.return_value = []

    streak = get_longest_streak(1)
    assert streak == 0

    mock_db.execute.assert_called_once_with(
        "SELECT last_completed_date FROM habit_completions WHERE habit_id = ? ORDER BY last_completed_date ASC",
        (1,)
    )
