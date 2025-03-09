
"""
A module containing all habit controllers (funtions that processes habit data)
"""

from db import conn
from rich.table import Table
from rich.console import Console
from rich import print
from models.habit import Habit
from datetime import datetime, timedelta

def get_habit(habit_id):
    '''This function is used to get habit by the habit id'''

    try:
        sql = "SELECT * FROM habits WHERE id = ?"
        cursor = conn.execute(sql, (habit_id,))
        habit = cursor.fetchone()

        return {
            "id": habit[0],
            "name": habit[1],
            "description": habit[2],
            "start_date": habit[3],
            "user_id": habit[4],
            "streak_count": habit[5],
            "periodicity": habit[6],
            "last_completed_date": habit[7],
            
        }
    except:
        raise Exception(f"Habit with ID {habit_id} is not found")
    

# def get_habits_by_user_id(user_id):
#     '''This function gets habit by user id'''

#     try:
#         sql = "SELECT * FROM habits WHERE user_id = ?"
#         cursor = conn.execute(sql, (user_id))
#         habits = cursor.fetchall()
#         return habits
#     except:
#         raise Exception(f"User with ID {user_id} is not found")
def get_habits_by_user_id(user_id):
    '''Fetches all habits for a user, including predefined ones'''
    try:
        sql = "SELECT * FROM habits WHERE user_id = ? OR user_id IS NULL"
        cursor = conn.execute(sql, (user_id,))
        habits = cursor.fetchall()
        return habits
    except Exception as e:
        raise Exception(f"Error fetching habits for User ID {user_id}: {str(e)}")


def get_habits_by_periodicity(user_id, periodicity):
    '''This function gets habit by user id'''

    try:
        sql = "SELECT * FROM habits WHERE user_id = ? AND periodicity = ?"
        cursor = conn.execute(sql, (user_id, periodicity))
        habits = cursor.fetchall()
        return habits
    except:
        raise Exception(f"User with ID {user_id} is not found")


# def create_habit(name, description, user_id, periodicity):
#     '''This is the controller function used to create habit '''

    # habit = Habit(name, description, user_id, periodicity)
    # habit.save()
    # return habit
def assign_predefined_habits(user_id):
    '''Assigns predefined habits to a new user'''

    predefined_habits = [
        ("Drink Water", "Drink 2 litres of water daily", "daily"),
        ("Gym", "Workout for at least 30 minutes", "daily"),
        ("Read", "Read a book for 20 minutes", "daily"),
        ("Meditate", "Practice mindfulness for 10 minutes", "daily"),
        ("Church", "Attend church service weekly", "weekly")
    ]
    start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Set the current timestamp

    for name, description, periodicity in predefined_habits:
        conn.execute(
            "INSERT INTO habits (name, description, periodicity, streak_count, last_completed_date, start_date, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, description, periodicity, 0, None, start_date, user_id),
        )
    
    conn.commit()
    print(f"[green]Predefined habits assigned to User ID {user_id}![/green]")



def create_habit(name, description, user_id, periodicity):
    '''Creates a new habit for a user and assigns a default start_date'''
    
    start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Set current timestamp

    sql = "INSERT INTO habits (name, description, user_id, periodicity, streak_count, last_completed_date, start_date) VALUES (?, ?, ?, ?, ?, ?, ?)"
    conn.execute(sql, (name, description, user_id, periodicity, 0, None, start_date))  # Include start_date
    conn.commit()

    return {"name": name, "description": description, "user_id": user_id, "periodicity": periodicity, "start_date": start_date}

def all_habits():
    '''This is the controller function to returns all the user habit'''

    sql = "SELECT * FROM habits"
    cursor = conn.execute(sql)
    return cursor.fetchall()

def delete_habit(habit_id):
    '''This is the controller function deletes a user habit'''

    sql = "DELETE FROM habits WHERE id = ?"
    cursor = conn.execute(sql, (habit_id,))
    conn.commit()

def edit_habit(habit_id, name, description, periodicity):
    '''This is the controller function allows the user to modify a habit'''

    sql = "UPDATE habits SET name = ?, description = ?, periodicity = ? WHERE id = ?"
    cursor = conn.execute(sql, (name, description, periodicity, habit_id))
    conn.commit()

def mark_done(habit_id):
    '''This is the controller function mark a habit as done'''

    sql = "SELECT * FROM habits WHERE id = ?"
    cursor = conn.execute(sql, (habit_id,))
    habit = cursor.fetchone()
    print(habit)
    streak_count = habit[5]
    periodicty = habit[6]
    last_completed_date = habit[7]
    period = {
        "daily": 1,
        "weekly": 7,
        "monthly": 30,
        "yearly": 365
    }

    if streak_count == 0:
        streak_count += 1
    elif last_completed_date and (datetime.now() - datetime.strptime(last_completed_date, '%Y-%m-%d %H:%M:%S.%f')).days > period[periodicty] and (datetime.now() - datetime.strptime(last_completed_date, '%Y-%m-%d %H:%M:%S.%f')).days <= period[periodicty] * 2:
        streak_count += 1
    elif last_completed_date and (datetime.now() - datetime.strptime(last_completed_date, '%Y-%m-%d %H:%M:%S.%f')).days > period[periodicty] * 2:
        streak_count = 0
    else:
        print("[yellow]Habit already completed today![/yellow]")
        return
    sql = "UPDATE habits SET streak_count = ?, last_completed_date = ? WHERE id = ?"
    cursor = conn.execute(sql, (streak_count, datetime.now(), habit_id))
    conn.commit()



def get_longest_streak(habit_id):
    '''Returns the longest consecutive streak for a given habit'''

    # Fetch all completion dates for the habit, sorted in ascending order
    sql = "SELECT last_completed_date FROM habit_completions WHERE habit_id = ? ORDER BY last_completed_date ASC"
    cursor = conn.execute(sql, (habit_id,))
    completion_dates = [row[0] for row in cursor.fetchall()]

    if not completion_dates:
        return 0  # No recorded completions

    # Convert string dates to datetime objects
    completion_dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in completion_dates]

    longest_streak = 1
    current_streak = 1

    # Iterate through completion dates to check consecutive days
    for i in range(1, len(completion_dates)):
        if (completion_dates[i] - completion_dates[i - 1]).days == 1:  # Consecutive days
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 1  # Reset streak if a gap exists

    return longest_streak


