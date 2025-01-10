"""
A module containing all authentication controllers
(functions that processes user authentication)
"""

import json
from controllers.user_controllers import get_user_by_username, create_user


def login(username, password):
    """Login function"""

    user = get_user_by_username(username)
    if user and user[2] == password:
        user_dict = {
            "id": user[0],
            "username": user[1],
            "password": user[2]
        }
        json_user = json.dumps(user_dict) #Convert user object to json
        with open("session.json", "w") as f:
            f.write(json_user)
        return user
    return None

def register(username, password):
    user = create_user(username, password)
    if user:
        return user
    return None

def logout():
    with open("session.json", "w") as f:
        f.write("{}")
    return None