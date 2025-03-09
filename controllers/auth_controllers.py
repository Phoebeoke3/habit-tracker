"""
A module containing all authentication controllers
(functions that processes user authentication)
"""

import json
from controllers.user_controllers import get_user_by_username, create_user
from controllers.habit_controllers import assign_predefined_habits
from controllers.user_controllers import create_user  

def login(username, password):
    """This is the login function"""

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
        return user_dict
    return None


def register(username, password):
    '''Registers a new user and assigns predefined habits'''
    
    user = create_user(username, password)
    if user:
        user_id = user["id"]  
        assign_predefined_habits(user_id)  # Assign predefined habits to the new user
        print(f"[green]User '{username}' registered successfully! Predefined habits assigned.[/green]")
        return user
    else:
        print("[red]Registration failed. Try again.[/red]")
        return None


def logout():
    '''This function logs out th current user session '''


    with open("session.json", "w") as f:
        f.write("{}")
    return None