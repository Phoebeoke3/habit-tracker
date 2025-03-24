# Habit-tracker 

Habit Tracker is a command-line interface (CLI) application that allows users to create, edit, and track habits. It provides a user-friendly interface for managing daily tasks and habits.

## Features

- User authentication: Users can create an account and log in to access their habits.

- Habit creation: Users can create new habits and set goals and reminders for each habit.
- Habit tracking: Users can mark habits as completed or incomplete on a daily or weekly basis.
- Habit editing: Users can edit habits, change goals, and set reminders.
- Habit deletion: Users can delete habits if they no longer need them.
- Interactive menu: The application provides a user-friendly menu for navigation and interaction.
- Command-line interface: The application is designed to be run from the command line, making it easy to use and accessible for users.
- User-friendly interface: The application provides a clear and easy-to-use interface for users to create, edit, and track habits.
- Database integration: The application uses a SQLite database to store user data and habits.

## Installation

To install Habit Tracker , follow these steps:

1. Clone the repository: 

    ```bash
    git clone https://github.com/phoebeoke3/habit-tracker.git
    ```

2. Navigate to the project directory: 

    ```bash
    cd habit-tracker
    ```
3. Setup virtual environment: 

    For Windows:
    
    ```bash
    python -m venv venv
    venv\Scripts\activate
    
    ```

    For Mac/ Linux:

     ```bash
    python -m venv venv
    source venv/Scripts/activate
    ```

4. Install dependencies: 

    ```bash
    pip install -r requirements.txt
    ```

5. Run the application: 

    ```bash
    python main.py
    ```

## Testing

For testing, a unittest file has been created which can be run by running pytest from command line.

These test covers:

-Habit creation and initialization
-Data retrieval and filtering
-Streak tracking and calculations
-Database operations
-Analytics functionality
-Data sorting and organization
-Error handling
-Date/time handling
