'''This is the user model'''

from models.base_model import BaseModel


class User(BaseModel):
    '''This is the user class'''

    __table_name__ = "users"
    habits = []

    def __init__(self, username, email, password):
        super().__init__()
        self.username = username
        self.email = email
        self.password = password
        # self.id = id
    def __str__(self):
        ''' A fuction that returns the string representation of an object'''
        return f''' user {self.id}
-----------------------------------
username:\t{self.username}
email:\t{self.email}
'''