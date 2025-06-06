"""
A module containing all habit controllers (funtions that processes habit data)
"""

import json
import os
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
    

def get_habits_by_user_id(user_id):
    '''Fetches all habits for a user, including predefined ones'''
    try:
        sql = "SELECT * FROM habits WHERE user_id = ? OR user_id IS NULL"
        cursor = conn.execute(sql, (user_id,))
        habits = cursor.fetchall()
        updated_habits = []

       
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
    '''This is the controller function that allows the user to modify a habit'''
    
    # Validate periodicity
    valid_periodicities = ["daily", "weekly", "monthly", "yearly"]
    if periodicity not in valid_periodicities:
        raise ValueError(f"Periodicity must be one of: {', '.join(valid_periodicities)}")

    # Check if habit exists first
    cursor = conn.cursor()  # Get cursor first
    cursor.execute("SELECT * FROM habits WHERE id = ?", (habit_id,))  # Use cursor.execute
    habit = cursor.fetchone()
    if not habit:
        raise Exception(f"Habit with ID {habit_id} not found")

    # Update the habit
    sql = "UPDATE habits SET name = ?, description = ?, periodicity = ? WHERE id = ?"
    cursor.execute(sql, (name, description, periodicity, habit_id))  # Use cursor.execute
    conn.commit()

    return {
        "id": habit_id,
        "name": name,
        "description": description,
        "periodicity": periodicity
    }

def mark_done(habit_id):
    '''This is the controller function that marks a habit as done'''

    sql = "SELECT * FROM habits WHERE id = ?"
    cursor = conn.execute(sql, (habit_id,))
    habit = cursor.fetchone()
    if habit is None:  #Prevent NoneType error
        print(f"[red]Habit with ID {habit_id} not found. Please check the habit ID and try again.[/red]")
        return  # Stop execution if habit does not exist
    
    streak_count = habit[5]
    periodicity = habit[6]  
    last_completed_date = habit[7]

    update_habit_streak(habit_id=habit_id, streak_count=streak_count, last_completed_date=last_completed_date, periodicity=periodicity, active_update=True)
   


def get_longest_streak(habit_id):
    '''Returns the highest streak ever for a habit, including current and broken streaks'''
   
    try:
        # Get current streak
        sql_current = "SELECT streak_count FROM habits WHERE id = ?"
        cursor = conn.execute(sql_current, (habit_id,))
        result = cursor.fetchone()
        
        # Handle case where habit doesn't exist
        if result is None:
            return 0
            
        current_streak = result[0]

        # Get max broken streak from streak_count table
        sql_broken = "SELECT MAX(count) FROM streak_count WHERE habit_id = ?"
        cursor = conn.execute(sql_broken, (habit_id,))
        result = cursor.fetchone()
        
        # Handle case where no broken streaks exist
        if result is None or result[0] is None:
            return current_streak
            
        max_broken_streak = result[0]
        
        # Return the highest of both
        return max(current_streak, max_broken_streak)
    
    except Exception as e:
        print(f"[red]Error fetching highest streak: {e}[/red]")
        return 0


def update_habit_streak(habit_id, streak_count, last_completed_date, periodicity, active_update=False):
    '''This function checks and update the streak count'''

    try:
        period = {
            "daily": 1,
            "weekly": 7,
            "monthly": 30,
            "yearly": 365
        }
        
        # If no previous completion date or streak is 0, start a new streak
        if active_update and streak_count == 0 or last_completed_date is None:
            streak_count = 1
        else:
            try:
                # Try to parse the datetime - handle potential format variations
                try:
                    last_date = datetime.strptime(last_completed_date, '%Y-%m-%d %H:%M:%S.%f')
                except ValueError:
                    last_date = datetime.strptime(last_completed_date, '%Y-%m-%d %H:%M:%S')
                
                days_since_completion = (datetime.now() - last_date).days
                
                # Within period - already completed
                if active_update and days_since_completion < period[periodicity]:
                    print("[yellow]Habit already completed![/yellow]")
                    return
                    
                # Completed within period - continue streak
                elif active_update and days_since_completion >= period[periodicity] and days_since_completion < period[periodicity] * 2:
                    streak_count += 1
                    
                elif days_since_completion >= period[periodicity] * 2:
                    # Save the broken streak before resetting
                    try:
                        conn.execute(
                            "INSERT INTO streak_count (habit_id, count, last_completed_date) VALUES (?, ?, ?)",
                            (habit_id, streak_count, last_completed_date)
                        )
                        # Remove the commit here since we'll commit everything at once
                        print(f"[red]Streak broken! Logged a streak of {streak_count} days.[/red]")
                    except Exception as e:
                        print(f"[red]Error saving to streak_count table: {e}[/red]")
                    
                    streak_count = 0  # Reset streak
                    
            except Exception as e:
                print(f"[red]Error processing date: {e}[/red]")
                
        # Update the habit's streak count and last completed date
        sql = "UPDATE habits SET streak_count = ?, last_completed_date = ? WHERE id = ?"
        conn.execute(sql, (streak_count, datetime.now(), habit_id))
        
        # Single commit for all database operations
        conn.commit()
        
        if active_update:
            print(f"[green]Habit marked as done! Current streak: {streak_count}[/green]")
            
        return {
            "streak_count": streak_count,
            "last_completed_date": last_completed_date,
            "periodicity": periodicity
        }
            
    except Exception as e:
        print(f"[red]Error updating streak: {e}[/red]")
        return None



# File to store streak data
DATA_FILE = 'streak_data.json'

# Load or initialize data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        'current_streak': 0,
        'last_date': None,
        'broken_streaks': []
    }

# Save data to file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_broken_streaks(habit_id):
    '''Returns all broken streaks for a habit'''

    sql = "SELECT broken_at, streak_count FROM broken_streaks WHERE habit_id = ? ORDER BY broken_at DESC"
    cursor = conn.execute(sql, (habit_id,))
    return cursor.fetchall()
