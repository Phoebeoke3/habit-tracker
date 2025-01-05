'''This is a module containing all authentication views'''

from pwinput import pwinput
from rich import print
from rich.console import Console
from rich.prompt import Prompt
import sys

console = Console()

def auth_view():
    console.rule("HABIT TRACKER")
    choice = Prompt.ask("Enter a command", choices=["login", "register", "exit"])
    if choice == "login":
        return login_view()
    elif choice == "register":
        return register_view()
    else:
        sys.exit()

def login_view():
    user = None
    console.clear()
    console.rule("Login")
    username = Prompt.ask("Enter username")
    password = pwinput("Enter password: ")
    user = {
        "username": username,
        "password": password
    }
    return user

def register_view():
    user = None
    console.clear()
    console.rule("Register")
    username = Prompt.ask("Enter username")
    password = pwinput("Enter password: ")
    user = {
        username: username,
        password: password
    }
    return login_view()