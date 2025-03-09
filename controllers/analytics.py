'''This is the analytics module, it allows users to analyse their habit'''


from controllers.habit_controllers import get_habits_by_periodicity, get_habits_by_user_id, get_longest_streak
from datetime import datetime, timedelta
from utils import sort_habits

def get_all_tracked_habits(user_id):
    '''This function return a list of all currently tracked habits'''

    all_habits = get_habits_by_user_id(user_id)
    habits = [habit for habit in all_habits if habit[5] > 0]
    return habits

def all_habits_by_periodicity(user_id, periodicity):
    '''This function returns a list of all habits with the same periodicity for a particular user'''

    habits = get_habits_by_periodicity(user_id, periodicity)
    return habits

def longest_habit_streak(user_id):
    '''This function return the longest run streak of all defined habits'''

    all_habits = get_habits_by_user_id(user_id)
    
    sorted_by_streak = sorted(all_habits, key=lambda tup: tup[5], reverse=True)
    return sorted_by_streak[0]


def view_longest_streak():
    '''This function return the longest run streak for a given habit'''

    habit_id = input("Enter the habit ID: ")
    longest_streak = get_longest_streak(habit_id)
    
    print(f"[green]Longest streak for habit {habit_id}: {longest_streak} days[/green]")

