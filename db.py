'''This is the Database set up module'''


import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to an SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(DATABASE_URL)

# # Create a cursor object using the cursor() method
cursor = conn.cursor()

# # Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL UNIQUE,
    password text NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS habits
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    description text NOT NULL,
    start_date text NOT NULL,
    user_id INTEGER NOT NULL,
    streak_count INTEGER NOT NULL,
    periodicity text NOT NULL,
    last_completed_date text,
    FOREIGN KEY (user_id) REFERENCES users(id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS streak_count 
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER NOT NULL,
    count INTEGER,
    last_completed_date TEXT NOT NULL,
    FOREIGN KEY (habit_id) REFERENCES habits(id))''')



def initialize_predefined_habits():
    predefined_habits = [
        ("Drink Water", "Drink 2 litres of water daily", "daily"),
        ("Gym", "Workout for at least 30 minutes", "daily"),
        ("Read", "Read a book for 20 minutes", "daily"),
        ("Meditate", "Practice mindfulness for 10 minutes", "daily"),
        ("Church", "Attend church service weekly", "weekly")
    ]

    cursor = conn.execute("SELECT COUNT(*) FROM habits")
    if cursor.fetchone()[0] == 0:  # Only insert if no habits exist
        for name, description, periodicity in predefined_habits:
            conn.execute(
                "INSERT INTO habits (name, description, periodicity, streak_count, last_completed_date, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                (name, description, periodicity, 0, None, None),
            )
        conn.commit()
        print("[green]Predefined habits have been initialized![/green]")




# # Insert a row of data
# cursor.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# # Save (commit) the changes
# conn.commit()

# # Close the connection
# conn.close()