'''This is the analytics module, it allows users to analyse their habit'''


from controllers.habit_controllers import get_habits_by_periodicity, get_habits_by_user_id
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
    # print(all_habits)
    sorted_by_streak = sorted(all_habits, key=lambda tup: tup[5], reverse=True)
    return sorted_by_streak[0]


    


def habit_streak():
    '''This function return the longest run streak for a given habit'''
    