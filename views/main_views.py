'''This contains main application view after user authentication'''

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich import print
import sys


console = Console()

def main_veiw(user):
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

    if command == "exit":
        sys.exit()
    

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
    table.add_row("6", "View Stats", "Views stats.")
    table.add_row("help", "help", "List all usable commands in a tabular form.")
    table.add_row("clear", "clear", "Clears the screen.")
    table.add_row("exit", "exit", "Quits the program.")
    table.add_row("quit", "quit", "Quits the program.")
    

    console.print(table)
        



