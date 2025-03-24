'''This is the habit view'''


from rich import print
from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
from controllers.habit_controllers import get_habits_by_user_id, create_habit, edit_habit, delete_habit, mark_done, get_habit, get_longest_streak
import time
import sys
import json

console = Console()

def habits_view(user_id):
    '''This function shows the table of current user habits'''

    habits = get_habits_by_user_id(user_id)
    table = Table(title="Habits", show_lines=True, leading=1, row_styles=[""])
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    # table.add_column("Name")
    # table.add_column("Description")
    # table.add_column("Streak count")
    # table.add_column("Periodicity")
    table.add_column("Name", style="magenta")
    table.add_column("Description", style="green")
    table.add_column("Start date", justify="center", style="blue")
    table.add_column("Streak Count", justify="center", style="yellow")
    table.add_column("Periodicity", justify="center", style="blue")

    for habit in habits:
        table.add_row(str(habit[0]), habit[1], habit[2], habit[3], str(habit[5]), habit[6])
    print(table)
    input("Press ENTER to continue")

def add_habit_view(user_id):
    '''This function add habits to user'''

    console.clear()
    console.rule("[bold]Add Habit[/bold]")
    name = input("Name: ")
    description = input("Description: ")
    periodicity = Prompt.ask("Enter periodicity: ", choices=["daily", "weekly", "monthly", "yearly"], default="daily")
    new_habit = create_habit(name, description, user_id, periodicity)
    print(f"[green]Habit {new_habit['name']} created successfully![/green]")

    input("Press Enter to Continue")

def edit_habit_view(user_id):
    '''This function is used to edit a user habit'''

    console.rule("[cyan]Edit Habit[/cyan]")
    habits_view(user_id)
    habit_id = input("Enter the ID of the habit to edit: ").strip()

    if not habit_id:
        print("[red]Invalid habit ID provided.[/red]")
        return None

    habit = get_habit(habit_id)
    if habit is None:
        print(f"[red]Habit with ID {habit_id} not found.[/red]")
        return None  # Prevent returning None

    print("\nEditing habit:")
    print(f"ID: {habit['id']}")
    print(f"Name: {habit['name']}")
    print(f"Description: {habit['description']}")
    print(f"Periodicity: {habit['periodicity']}")

    name = input("New name: ") or habit['name']
    description = input("New description: ") or habit['description']
    periodicity = Prompt.ask("Enter periodicity: ", choices=["daily", "weekly", "monthly", "yearly"], default=habit['periodicity'])

    edit_habit(habit_id, name, description, periodicity)
    print(f"[green]Habit {habit_id} updated successfully![/green]")

    return periodicity  # Always return periodicity



def delete_habit_view(user_id):
    '''This function deletes a user habit'''

    habits_view(user_id)
    console.rule("[bold]Delete Habit[/bold]")
    habit_id = Prompt.ask("Enter the ID of the habit to delete ").strip()

    if not habit_id:
        print("[red]Invalid habit ID entered.[/red]")
        return

    if not get_habit(habit_id):  # Ensure habit exists before deleting
        print(f"[red]Habit with ID {habit_id} not found.[/red]")
        return

    try:
        delete_habit(habit_id)
        print(f"[green]Habit {habit_id} deleted successfully![/green]")
    except Exception as e:
        print(f"[red]Error deleting habit: {e}[/red]")

def track_habit_view(user_id):
    '''This function tracks the user habit'''
    
    habits_view(user_id)
    console.rule("[bold]Track Habit[/bold]")
    habit_id = Prompt.ask("Enter the ID of the habit to markdone from the table above ")
    mark_done(habit_id)
    print(f"[green]Habit {habit_id} tracked successfully![/green]")
    input()

def display_habits(user_id):
    '''Displays all habits, including predefined ones'''
    
    habits = get_habits_by_user_id(user_id)

    if not habits:
        print("[yellow]No habits found.[/yellow]")
        return

    table = Table(title="Your Habits")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Description", style="green")
    table.add_column("Periodicity", justify="center", style="blue")
    table.add_column("Streak Count", justify="center", style="yellow")

    for habit in habits:
        table.add_row(str(habit[0]), habit[1], habit[2], habit[3], str(habit[5]))

    console = Console()
    console.print(table)

def view_longest_streak():
    '''View of the longest run streak for a given habit'''

    habit_id = input("Enter the habit ID: ")
    longest_streak = get_longest_streak(habit_id)
    print(f"[green]Longest streak for habit {habit_id}: {longest_streak} days[/green]")

