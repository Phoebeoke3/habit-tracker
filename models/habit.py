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
        
        try:
            sql = "SELECT * FROM habits WHERE id = ?"
            cursor.execute(sql, (habit_id,))
            habit = cursor.fetchone()
            
            if not habit:
                print("[red]Habit not found![/red]")
                return
            
            # Update the habit
            sql = """UPDATE habits 
                    SET name = ?, description = ?, start_date = ?, user_id = ? 
                    WHERE id = ?"""
            cursor.execute(sql, (name, description, start_date, user_id, habit_id))
            conn.commit()
            print(f"[green]Habit updated successfully![/green]")
        except Exception as e:
            print(f"[red]Error updating habit: {e}[/red]")
