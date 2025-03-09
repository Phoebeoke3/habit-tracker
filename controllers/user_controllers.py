"""
A module containing all user controllers (funtions that processes user data)
"""
import sqlite3
from db import conn
from rich.table import Table
from rich.console import Console
from models.user import User

def get_user(user_id):
    sql = "SELECT * FROM users WHERE id = ?"
    cursor = conn.execute(sql, (user_id,))
    user = cursor.fetchone()
    
    print(f"User {user_id} details")
    print(f"ID: {user[0]}")
    print(f"Username: {user[1]}")
    print(f"Password: {user[2]}")

def get_user_by_username(username):
    sql = "SELECT * FROM users WHERE username = ?"
    cursor = conn.execute(sql, (username,))
    user = cursor.fetchone()
    return user

# def create_user(username, password):
#     user = User(username, password)
#     user.save()
#     return user



import sqlite3
from db import conn

def create_user(username, password):
    '''Creates a new user only if the username is not already taken'''
    
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        print(f"[red]Error: Username '{username}' is already taken. Please choose another one.[/red]")
        return None  # Return None to indicate registration failure

    # Insert new user if username is unique
    sql = "INSERT INTO users (username, password) VALUES (?, ?)"
    cursor.execute(sql, (username, password))
    conn.commit()

    # Retrieve the new user ID
    user_id = cursor.lastrowid

    return {"id": user_id, "username": username}  # Return user as a dictionary


def update_user(user_id, username, password):
    user = User(username, password)
    user.update(user_id, username, password)

def all_users():
    sql = "SELECT * FROM users"
    cursor = conn.execute(sql)
    users = cursor.fetchall()

    table = Table(title="Users")

    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Username")
    
    for user in users:
        table.add_row(str(user[0]), user[1])
    
    console = Console()
    console.print(table)

def delete_user(user_id):
    pass