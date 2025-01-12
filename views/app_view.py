'''This is the main application parent view'''

from views.auth_views import auth_view
from views.main_views import main_view
from rich.console import Console

console = Console()

def app_view(session):
    '''This is the main application view function'''

    user = session
    while True:
        console.clear()
        if not user:
            user = auth_view()
        else:
            user = main_view(user)


