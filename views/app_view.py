'''This is the main application parent view'''

from rich import print
from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
from views.auth_views import auth_view
from views.main_views import main_view
from controllers.habit_controllers import all_habits, create_habit, edit_habit, delete_habit, mark_done, get_habit
import time
import sys


console = Console()

def app_view(session):
    '''This is the main application view function'''

    user = session
    while True:
        console.clear()
        habits = all_habits()
        table = Table(title="Habits", show_lines=True, leading=1, row_styles=["dim", ""])
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Name")
        table.add_column("Description")
        table.add_column("Start date")
        table.add_column("Streak count")
        table.add_column("Periodicity")
        with Live(table, refresh_per_second=4):
            for habit in habits:
                time.sleep(0.2)  # arbitrary delay
                table.add_row(str(habit[0]), habit[1], habit[2], habit[3], str(habit[5]), habit[6])
        command = Prompt.ask("Enter a command: ", choices=["back", "create", "edit", "delete", "track", "quit"], default="create")
        if command == "back":
            break
        elif command == "create":
            add_habit(id)
        elif command == "edit":
            edit_habit_view()
        elif command == "delete":
            delete_habit_view()
        elif command == "track":
            track_habit()
        elif command == "quit":
            sys.exit()
        print(user)

        if not user:
            user = auth_view()
        else:
            main_view(user)
            input()


def add_habit(user_id):
    console.clear()
    console.rule("[bold]Add Habit[/bold]")
    name = input("Name: ")
    description = input("Description: ")
    periodicity = Prompt.ask("Enter periodicity: ", choices=["daily", "weekly", "monthly", "yearly"], default="daily")
    new_habit = create_habit(name, description, user_id, periodicity)
    print(f"[green]Habit {new_habit.name} created successfully![/green]")
    time.sleep(3)

def edit_habit_view():
    # console.clear()
    console.rule("[cyan]Edit Habit[/cyan]")
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
