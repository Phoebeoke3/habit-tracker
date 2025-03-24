'''This contains main application view after user authentication'''

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich import print
from controllers.auth_controllers import logout
from views.habit_views import habits_view, add_habit_view, edit_habit_view, delete_habit_view, track_habit_view
from views.analytics_views import analytics_view
from utils.test_data_generator import generate_predefined_test_data
import sys


console = Console()

def main_view(user):
    '''This is the main view function after authentication '''
    
    console.clear()
    # username = user.username
    print("\n")
    print(f"[cyan]Welcome to Habit Tracker {user["username"].capitalize()} [/cyan]".center(100))
    # print("Enter [green]help[/green] for a list of commands!".center(100))
    # print(user)
    print("\n")
    help_view()
    command = input("Enter a command: ") 
    user_id = str(user["id"])
    if command == "exit" or command == "quit":
        sys.exit()
    elif command == "logout" or command == "0":
        logout()
        return None
    elif command == "1":
        habits_view(user_id)
    elif command == "2":
        add_habit_view(user_id)
    elif command == "3":
        edit_habit_view(user_id)
    elif command == "4":
        delete_habit_view(user_id)
    elif command == "5":
        track_habit_view(user_id)
    elif command == "6":
        analytics_view(user_id)
    elif command == "7":
        if generate_predefined_test_data(user["id"]):
            print("\n[green]You can now use the analytics features to explore the generated data![/green]")
        input("\nPress Enter to continue...")
        
    return user    

def help_view():
    '''This function shows a list of command a user can enter '''

    table = Table(title="List of commands")

    table.add_column("Command", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Description", justify="centre", style="green")

    table.add_row("0", "Logout", "Logs out the user.")
    table.add_row("1", "Habits", "Shows the user's habits.")
    table.add_row("2", "Add Habit", "Adds a new habit.")
    table.add_row("3", "Edit Habit", "Edits a habit.")
    table.add_row("4", "Delete Habit", "Deletes a habit.")
    table.add_row("5", "Track Habit", "Tracks a habit.")
    table.add_row("6", "Analyse Habit", "Habit Analyses.")
    table.add_row("7", "Generate Test Data", "Generates predefined test data.")
    table.add_row("help", "help", "List all usable commands in a tabular form.")
    table.add_row("clear", "clear", "Clears the screen.")
    table.add_row("exit", "exit", "Quits the program.")
    table.add_row("quit", "quit", "Quits the program.")
    

    console.print(table)
        



