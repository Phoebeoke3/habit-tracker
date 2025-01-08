'''This is the main application parent view'''

from views.auth_views import auth_view
from rich.console import Console
from views.main_views import main_veiw

console = Console()

def app_view(session):
    '''This is the main application view function'''

    user = session
    while True:
        console.clear()
        print(user)

        if not user:
            user = auth_view()
        else:
            main_veiw(user)
            input()

