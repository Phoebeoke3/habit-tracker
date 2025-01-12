'''This is the habit view'''


from rich import print
from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
from controllers.habit_controllers import get_habits_by_user_id, create_habit, edit_habit, delete_habit, mark_done, get_habit
import time
import sys

console = Console()

def habits_view(user_id):
    '''This function shows the table of current user habits'''

    habits = get_habits_by_user_id(user_id)
    table = Table(title="Habits", show_lines=True, leading=1, row_styles=["dim", ""])
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name")
    table.add_column("Description")
    table.add_column("Start date")
    table.add_column("Streak count")
    table.add_column("Periodicity")
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
    print(f"[green]Habit {new_habit.name} created successfully![/green]")
    time.sleep(3)

def edit_habit_view(user_id):
    '''This function is used to edit user habit'''

    # console.clear()
    console.rule("[cyan]Edit Habit[/cyan]")
    habits_view(user_id)
    habit_id = input("Enter the ID of the habit to edit: ")
    habit = get_habit(habit_id)
    print("\n")
    print("The habit to be updated is: ")
    print(f"ID: {habit['id']}")
    print(f"Name: {habit['name']}")
    print(f"Description: {habit['description']}")
    print(f"Start date: {habit['start_date']}")
    print(f"User ID: {habit['user_id']}")
    print(f"Streak count: {habit['streak_count']}")
    print(f"Periodicity: {habit['periodicity']}")
    print("\n")
    name = input("Name: ") or habit['name']
    description = input("Description: ") or habit['description']
    periodicity = Prompt.ask("Enter periodicity: ", choices=["daily", "weekly", "monthly", "yearly"], default=habit['periodicity'])
    edit_habit(habit_id, name, description, periodicity)
    print(f"[green]Habit {habit_id} updated successfully![/green]")
    # while True:
        # print("1.\tdaily")
        # print("2.\tweekly")
        # print("3.\tmonthly")
        # print("4.\tyearly")
        # choice = input("Enter your choice: ")
        # if choice == "1":
        #     periodicity = "daily"
        #     break
        # elif choice == "2":
        #     periodicity = "weekly"
        #     break
        # elif choice == "3":
        #     periodicity = "monthly"
        #     break
        # elif choice == "4":
        #     periodicity = "yearly"
        #     break
        # else:
        #     print("[red]Invalid choice![/red]")
    return periodicity

def delete_habit_view():
    '''This function '''
    console.rule("[bold]Delete Habit[/bold]")
    habit_id = Prompt.ask("Enter the ID of the habit to delete: ")
    delete_habit(habit_id)
    print(f"[green]Habit {habit_id} deleted successfully![/green]")

def track_habit():
    console.rule("[bold]Track Habit[/bold]")
    habit_id = Prompt.ask("Enter the ID of the habit to markdone from the table above: ")
    mark_done(habit_id)
    print(f"[green]Habit {habit_id} tracked successfully![/green]")
    time.sleep(3)
