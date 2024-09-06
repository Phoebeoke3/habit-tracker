'''This is the user model'''

class User:
    '''This is the user class'''

    def __init__(self, id, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.id = id
    def __str__(self):
        ''' A fuction that returns the string representation of an object'''
        return f'''user 1
-----------------------------------
username:\t{self.username}
email:\t{self.email}
'''