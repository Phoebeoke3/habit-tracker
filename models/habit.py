'''This is the file containing habit model'''

from datetime import datetime 
from sqlite3 import IntegrityError
import time
from db import cursor, conn
from datetime import datetime
from rich import print


class Habit:
    '''This is the Habit class'''

    def __init__(self, name, description, user_id, periodicity):
        '''Constructor method'''

        self.name = name
        self.description = description
        self.start_date = datetime.now()
        self.user_id = user_id
        self.streak_count = 0
        self.periodicity = periodicity
        self.last_completed_date = None


    def save(self):
        '''This function saves object to database'''
        
        try:
            sql = "INSERT INTO habits (name, description, start_date, user_id, streak_count, periodicity, last_completed_date) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, (self.name, self.description, self.start_date, self.user_id, self.streak_count, self.periodicity, self.last_completed_date))
            conn.commit()
        except IntegrityError as e:
            print(f"[red]Habit already exist![/red]")
            print(e)
        except Exception as e:
            print(f"[red]Error: {e}[/red]")
            
    
    def update(self, habit_id, name, description, start_date, end_date, user_id):
        '''This function updates the habit'''

        if not habit_id:
            print("[red]Habit ID is required![/red]")
            return

        sql = "SELECT * FROM habits WHERE id = ?"
        cursor = conn.execute(sql, (habit_id,))
        habit = cursor.fetchone()
        print(f"name: {name}")
        print(f"description: {description}")
        print(f"start_date: {start_date}")
        print(f"end_date: {end_date}")
        print(f"user_id: {user_id}")
        print("\n")
        print("The habit to be updated is: ", habit)
        print(f"ID: {habit[0]}")
        print(f"Name: {habit[1]}")
        print(f"Description: {habit[2]}")
        print(f"Start date: {habit[3]}")
        print(f"End date: {habit[4]}")
        print(f"User ID: {habit[5]}")
        if habit is None:
            print(f"[red]Habit {habit_id} not found![/red]")
            return

        if name != "":
            self.name = name
        else:
            self.name = habit[1]

        if description != "":
            self.description = description
        else:
            self.description = habit[2]

        if start_date != "":
            self.start_date = start_date
        else:
            self.start_date = habit[3]

        if end_date != "":
            self.end_date = end_date
        else:
            self.end_date = habit[4]

        if user_id != "":
            self.user_id = user_id
        else:
            self.user_id = habit[5]

        sql = "UPDATE habits SET name = ?, description = ?, start_date = ?, end_date = ?, user_id = ? WHERE id = ?"
        cursor.execute(sql, (self.name, self.description, self.start_date, self.end_date, self.user_id, habit_id))
        cursor.commit()
        print(f"[green]Habit {self.name} updated successfully![/green]")
