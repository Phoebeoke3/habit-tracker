# Habit-tracker 

Habit Tracker is a command-line interface (CLI) application that allows users to create, edit, and track habits. It provides a user-friendly interface for managing daily tasks and habits.

## Features

### User Management
- Secure user authentication system
- Individual user profiles
- Predefined habit templates for new users

### Habit Management
- Create, edit, and delete habits
- Mark habits as complete/incomplete
- Daily and weekly habit tracking
- Customizable habit descriptions
- Streak tracking system

### Analytics
- View currently tracked habits
- Filter habits by periodicity
- Track longest running streaks
- Analyse habit completion patterns

### Interface
- User-friendly CLI with coloured output
- Interactive menu system
- Clear command structure
- Real-time feedback


## Technical Requirements

- Python 3.7+
- SQLite3
- Virtual Environment


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

## Usage

### Main Commands
- `1` - View all habits
- `2` - Add new habit
- `3` - Edit habit
- `4` - Delete habit
- `5` - Track habit
- `6` - View analytics
- `0` - Logout
- `exit/quit` - Exit application

### Analytics Commands
- `1` - View tracked habits
- `2` - View habits by periodicity
- `3` - View longest streak across all habits
- `4` - View streak for specific habit


## Testing

For testing, a unittest file has been created which can be run by running pytest from the command line.


Run tests using pytest:
```bash
pytest
```

Test coverage includes:
- Habit creation and initialization
- Habit modification and deletion
- Data retrieval and filtering
- Streak tracking calculations
- Database operations
- Analytics functionality
- Error handling
- Integration testing

## Project Structure
```
habit-tracker/
├── controllers/
│   ├── auth_controllers.py
│   ├── habit_controllers.py
│   └── analytics.py
├── models/
│   ├── habit.py
│   └── user.py
├── views/
│   ├── auth_views.py
│   ├── habit_views.py
│   ├── analytics_views.py
│   └── main_views.py
├── tests/
│   ├── conftest.py
│   ├── test_integration.py
│   └── test_analytics.py
├── db.py
├── main.py
└── requirements.txt
```

## Dependencies
- rich: Terminal formatting and tables
- pytest: Testing framework
- python-dotenv: Environment variable management
- pwinput: Secure password input
- sqlite3: Database management
