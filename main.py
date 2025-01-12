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
    

   
