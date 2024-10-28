import typer
from controllers.user_controllers import get_all_users
from rich.console import Console
from rich.table import Table

# Initialize the Typer app
app = typer.Typer()

# initialize Console object
console = Console()

# Define a command to greet users
@app.command()
def greet(name: str):
    """
    Greet a user.
    """
    typer.echo(f"Hello {name}!")

# Define a command to add two numbers
@app.command()
def add(a: int, b: int):
    """
    Add two numbers.
    """
    result = a + b
    typer.echo(f"The result of {a} + {b} is {result}")

@app.command()
def user(name: str):
    '''This function gets all objects based on table name'''
    
    if not name:
        typer.echo("object name required")
        return 
    table = Table(title="Users")
    table.add_column("id")
    table.add_column("username")
    table.add_column("email")
    users = get_all_users()
    for user in users:
        # typer.echo(dict(user))
        table.add_row(user[0], user[1], user[2])
    console.print(table)
# Interactive mode
def interactive_mode():
    """
    Start interactive mode.
    """
    while True:
        # Prompt user for input command
        command = input("Enter command (or type 'exit' to quit): ").strip().split()

        if not command:
            continue
        elif command[0] == "exit":
            typer.echo("Exiting interactive mode.")
            break
        else:
            try:
                # Execute the commands by passing the list of commands to typer
                app(command)
            except SystemExit:
                # Catch SystemExit to prevent the app from stopping the loop
                pass

if __name__ == "__main__":
    # Start in interactive mode
    interactive_mode()
