'''This is a module containing functions to create or get session'''

import os
import json

SESSION_PATH = "session.json"

def get_session():
    '''This function returns the current logged in user'''

    user = None
    try:
        with open(SESSION_PATH, 'r') as file:
            user_json = file.read()
            user = json.loads(user_json)
    except FileNotFoundError as e:
        with open(SESSION_PATH, 'w') as file:
            file.write(json.dumps({}))
        user = {}  # Set user to empty dict after creating the file
    return user

def set_session(user):
    '''This function saves the current logged in user to file'''

    try:
        with open(SESSION_PATH, 'w') as file:
            user_json = json.dumps(user)
            file.write(user_json)
    except:
        pass


