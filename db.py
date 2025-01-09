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

# # Insert a row of data
# cursor.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# # Save (commit) the changes
# conn.commit()

# # Close the connection
# conn.close()