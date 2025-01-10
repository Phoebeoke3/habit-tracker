'''This is a file containing the user model'''

from db import conn
from sqlite3 import IntegrityError
from rich import print

class User:
    '''This is the User class'''

    def __init__(self, username, password):
        '''Constructor method'''
        
        self.username = username
        self.password = password

    def save(self):
        '''This function saves the object to database'''

        try:
            sql = "INSERT INTO users (username, password) VALUES (?, ?)"
            conn.execute(sql, (self.username, self.password))
            conn.commit()
            print(f"[green]User {self.username} created successfully![/green]")
        except IntegrityError:
            print(f"[red]Username already exist![/red]")
    
    