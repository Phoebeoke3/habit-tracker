'''Entry file'''

from utils.session import get_session
from views.app_view import app_view

if __name__ == "__main__":
    user = get_session()
    app_view(user)