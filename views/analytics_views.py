'''This is the analytics view'''


from rich import print
from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
from controllers.habit_controllers import get_habits_by_user_id
from controllers.analytics import all_habits_by_periodicity, get_all_tracked_habits, longest_habit_streak, get_longest_streak
import sys

console = Console()

def analytics_view(user_id):
    '''This is the main view function after authentication '''
    
    console.clear()
    
    print("\n")
    print(f"[cyan]Analyse Habit [/cyan]".center(100))
   
    print("\n")
    analytics_menu_view()
    command = input("Enter a command: ") 
    if command == "exit" or command == "quit":
        sys.exit()
    elif command == "logout" or command == "0":
        # logout()
        return None
    elif command == "1":
        tracked_habits_view(user_id)
        
    elif command == "2":
        habit_periodicity_view(user_id)
        
    elif command == "3":
        longest_habit_streak_view(user_id)
        
    elif command == "4":
       view_longest_streak(user_id)

   
        
def tracked_habits_view(user_id):
    '''This function shows the table of currently tracked user habits'''

    habits = get_all_tracked_habits(user_id)
    table = Table(title="Habits", show_lines=True, leading=1, row_styles=[""])
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Description", style="green")
    table.add_column("Start date", justify="center", style="blue")
    table.add_column("Streak Count", justify="center", style="yellow")
    table.add_column("Periodicity", justify="center", style="blue")
    table.add_column("Last Completed Date", justify="center", style="yellow")
    for habit in habits:
        table.add_row(str(habit[0]), habit[1], habit[2], habit[3], str(habit[5]), habit[6], habit[7])
    print(table)
    input("Press ENTER to continue")


def habit_periodicity_view(user_id):
    '''This function is the view that returns a list of all habits with the same periodicity for a particular user'''

    console.rule("[cyan]Get Habit Based on Periodicity[/cyan]")
    
    periodicity = Prompt.ask("Enter periodicity: ", choices=["daily", "weekly", "monthly", "yearly"], default="daily")

    try:
        habits = all_habits_by_periodicity(user_id, periodicity)
        table = Table(title=f"{periodicity.capitalize()} Habit(s)", show_lines=True, leading=1, row_styles=[""])
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Description", style="green")
        table.add_column("Start date", justify="center", style="blue")
        table.add_column("Streak Count", justify="center", style="yellow")
        table.add_column("Periodicity", justify="center", style="blue")
        table.add_column("Last Completed Date", justify="center", style="yellow")
        for habit in habits:
            table.add_row(str(habit[0]), habit[1], habit[2], habit[3], str(habit[5]), habit[6], habit[7])
        print(table)
    except Exception as e:
        print(f"[red]{e}[/red]")
    input("Press ENTER to continue")
    return

def longest_habit_streak_view(user_id):
    '''This function view return the longest run streak of all defined habits'''

    console.rule("[cyan]Habit with longest streak[/cyan]")

    try:
        habit = longest_habit_streak(user_id)

        table = Table(title="", show_lines=True)
        table.add_column("Name", style="bold cyan")
        table.add_column("Description", style="italic magenta")
        table.add_column("Date", style="green")
        table.add_column("Streak Count", style="bold yellow")
        table.add_column("Periodicity", style="bold blue")
        table.add_column("Last Completed Date", style="bold green")

        table.add_row(habit[1], habit[2], habit[3], str(habit[5]), str(habit[6]), str(habit[7]))

        console.print(table)
       
    except Exception as e:
        print(f"[red]{e}[/red]")
    input("Press ENTER to continue")
    return

def view_longest_streak(user_id):
    '''This is the function view that return the longest run streak of a given habit'''

    console.rule("[cyan]Longest streak[/cyan]")
    # Fetch all habits for the user
    habits = get_habits_by_user_id(user_id)

    table = Table(title="Habits")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Description", style="green")
    table.add_column("Start Date", style="cyan")
    table.add_column("Streak Count", justify="center", style="yellow")
    table.add_column("Periodicity", justify="center", style="blue")
    table.add_column("Last Completion Date", style="green")

    for habit in habits:
            table.add_row(str(habit[0]), habit[1], habit[2], habit[3], str(habit[5]), habit[6], habit[7])
    console.print(table)
    if not habits:
        print("[red]No habits found for this user.[/red]")
        # return

    try:
        # Prompt user for habit ID
        habit_id = input("\nEnter the habit ID to check longest streak: ").strip()

        if not habit_id.isdigit():
            print("[red]Invalid input. Please enter a valid numeric Habit ID.[/red]")
            input("\nPress ENTER to return to analytics menu...")  # Pause
            return  # Exit function early

        habit_id = int(habit_id)
        longest_streak = get_longest_streak(habit_id)

        print(f"\n[green]Longest streak for Habit ID {habit_id}: {longest_streak} days[/green]")
        input("\nPress ENTER to return to main menu...")  # Pause before returning

    except Exception as e:
        print(f"[red]Error: {e}[/red]")  # Show error message
        input("\nPress ENTER to return to main menu...")  # Pause before returning


def analytics_menu_view():
    '''This function shows a list of analytics command a user can enter '''

    table = Table(title="List of analytics commands")

    table.add_column("Command", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Description", justify="centre", style="green")

    table.add_row("0", "Back", "Go back to main view.")
    table.add_row("1", "Tracked Habit", "Return a list of all currently tracked habits.")
    table.add_row("2", "Habit Period", "Return a list of all habits with the same periodicity.")
    table.add_row("3", "Longest Habit Streak", "Return the longest run streak of all defined habits.")
    table.add_row("4", "Habit Streak", "Return the longest run streak for a given habit.")
    table.add_row("help", "help", "List all usable commands in a tabular form.")
    table.add_row("exit", "exit", "Quits the program.")
    table.add_row("quit", "quit", "Quits the program.")
    

    console.print(table)
        




    