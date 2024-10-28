'''user_controllers holds function for creating, updating and deleting instances
of the user'''

from models.user import User

from models import storage


def get_user_by(id):
    '''This function gets user by id'''
    pass

def get_user_by(email):
    '''This function gets user by email'''
    pass

def create_user(username, email, password):
    '''This function creates the user profile'''
    pass


def get_all_users():
    '''This function get all the users'''
    users = storage.all("users")
    return users



