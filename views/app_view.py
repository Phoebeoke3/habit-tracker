'''This is the main application parent view'''

from views.auth_views import auth_view
from rich.console import Console

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
            input("Press enter to enter infinite loop")

