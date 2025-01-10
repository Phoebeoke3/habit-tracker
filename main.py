'''Entry file'''


import json
from pwinput import pwinput
from rich import print
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from controllers.auth_controllers import logout
from controllers.user_controllers import create_user, update_user, delete_user, all_users, get_user
from utils.session import get_session
from views.app_view import app_view
from views.auth_views import auth_view
from views.main_views import main_view, help_view

console = Console()


if __name__ == "__main__":
    user = get_session()
    app_view(user)
    
def run():
    user = None
    with open("session.json", "r") as f:
        user = json.load(f)

    if not user:
        user = auth_view()

    if not user:
        print("[red]Authentication failed![/red]")
        return
    else:
        while True:
            main_view()
            command = input("Enter a command: ")
            if command == "help":
                help_view()
            elif command == "exit":
                break
            elif command == "quit":
                break
            elif command == "clear":
                console.clear()
            elif command == "0":
                console.clear()
                logout()
                user = None
                user = auth_view()
                if user:
                    continue
            elif command == "1":
                app_view(user["id"])
            else:
                print("\n[yellow]Command not found[/yellow]")
        print("Goodbye!")

if __name__ == "__main__":
    run()
    from db import conn
    conn.close()

if __name__ == "__main__":
    user = get_session()
    app_view(user)