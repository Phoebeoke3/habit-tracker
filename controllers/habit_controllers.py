"""
A module containing all habit controllers (funtions that processes habit data)
"""

from db import conn
from rich.table import Table
from rich.console import Console
from rich import print
from models.habit import Habit
from datetime import datetime

def get_habit(habit_id):
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
        "periodicity": habit[6]
    }

def get_habits_by_user_id(user_id):
    sql = "SELECT * FROM habits WHERE user_id = ?"
    cursor = conn.execute(sql, (user_id))
    habits = cursor.fetchall()
    return habits

def create_habit(name, description, user_id, periodicity):
    habit = Habit(name, description, user_id, periodicity)
    habit.save()
    return habit

def all_habits():
    sql = "SELECT * FROM habits"
    cursor = conn.execute(sql)
    return cursor.fetchall()

def delete_habit(habit_id):
    sql = "DELETE FROM habits WHERE id = ?"
    cursor = conn.execute(sql, (habit_id,))
    conn.commit()

def edit_habit(habit_id, name, description, periodicity):
    sql = "UPDATE habits SET name = ?, description = ?, periodicity = ? WHERE id = ?"
    cursor = conn.execute(sql, (name, description, periodicity, habit_id))
    conn.commit()

def mark_done(habit_id):
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

def view_stats():
    pass