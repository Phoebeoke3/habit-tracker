from datetime import datetime, timedelta
from models.habit import Habit
from db import conn, cursor
from rich import print

def generate_predefined_test_data(user_id):
    """Generate 4 weeks of test data for all predefined habits"""
    
    # Check if user exists first
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if not cursor.fetchone():
        print(f"[red]Error: User with ID {user_id} does not exist[/red]")
        return None
    
    start_date = datetime(2024, 1, 1)  # Start from January 1st, 2024
    
    predefined_habits = {
        "Drink Water": {
            "description": "Drink 2 litres of water daily",
            "periodicity": "daily",
            "completion_days": [
                # Week 1 - Perfect week (7/7)
                1, 2, 3, 4, 5, 6, 7,
                # Week 2 - Missed weekend (5/7)
                8, 9, 10, 11, 12,
                # Week 3 - Workdays only (5/7)
                15, 16, 17, 18, 19,
                # Week 4 - Inconsistent (3/7)
                22, 23, 25
            ],
            "expected_max_streak": 12  # From week 1-2 continuous
        },
        "Gym": {
            "description": "Workout for at least 30 minutes",
            "periodicity": "daily",
            "completion_days": [
                # Week 1 - MWF pattern (3/7)
                1, 3, 5,
                # Week 2 - MWF pattern (3/7)
                8, 10, 12,
                # Week 3 - Extra sessions (4/7)
                15, 17, 18, 19,
                # Week 4 - Reduced sessions (2/7)
                22, 26
            ],
            "expected_max_streak": 3  # Best streak in week 3
        },
        "Read": {
            "description": "Read a book for 20 minutes",
            "periodicity": "daily",
            "completion_days": [
                # Week 1 - Strong start (4/7)
                1, 2, 3, 4,
                # Week 2 - Busy week (2/7)
                8, 9,
                # Week 3 - Better routine (5/7)
                15, 16, 17, 18, 19,
                # Week 4 - Maintained (5/7)
                22, 23, 24, 25, 26
            ],
            "expected_max_streak": 5  # Achieved in weeks 3 and 4
        },
        "Meditate": {
            "description": "Practice mindfulness for 10 minutes",
            "periodicity": "daily",
            "completion_days": [
                # Week 1 - Learning (2/7)
                1, 3,
                # Week 2 - Building (3/7)
                8, 9, 10,
                # Week 3 - Perfect (7/7)
                15, 16, 17, 18, 19, 20, 21,
                # Week 4 - Strong (3/3 before breaking)
                22, 23, 24
            ],
            "expected_max_streak": 10  # From week 3 into week 4
        },
        "Church": {
            "description": "Attend church service weekly",
            "periodicity": "weekly",
            "completion_days": [
                # Week 1
                7,
                # Week 2
                14,
                # Week 3 - Missed
                # Week 4
                28
            ],
            "expected_max_streak": 2  # Weeks 1-2 continuous
        }
    }

    try:
        created_habits = []
        last_date = None
        
        for habit_name, details in predefined_habits.items():
            # Create the habit
            cursor.execute("""
                INSERT INTO habits (name, description, start_date, user_id, streak_count, 
                                  periodicity, last_completed_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                habit_name,
                details["description"],
                start_date.strftime('%Y-%m-%d %H:%M:%S'),
                user_id,
                0,
                details["periodicity"],
                None
            ))
            habit_id = cursor.lastrowid
            
            # Add completion records
            current_streak = 0
            max_streak = 0
            
            for day in details["completion_days"]:
                completion_date = start_date + timedelta(days=day-1)
                
                if last_date is None or (
                    (details["periodicity"] == "daily" and (completion_date - last_date).days == 1) or
                    (details["periodicity"] == "weekly" and (completion_date - last_date).days <= 7)
                ):
                    current_streak += 1
                else:
                    current_streak = 1
                
                max_streak = max(max_streak, current_streak)
                last_date = completion_date
                
                # Record completion
                cursor.execute("""
                    INSERT INTO streak_count (habit_id, count, last_completed_date)
                    VALUES (?, ?, ?)
                """, (
                    habit_id,
                    current_streak,
                    completion_date.strftime('%Y-%m-%d %H:%M:%S')
                ))
                
                # Update habit's current streak and last completion
                cursor.execute("""
                    UPDATE habits 
                    SET streak_count = ?, last_completed_date = ?
                    WHERE id = ?
                """, (
                    current_streak,
                    completion_date.strftime('%Y-%m-%d %H:%M:%S'),
                    habit_id
                ))
            
            created_habits.append({
                "id": habit_id,
                "name": habit_name,
                "final_streak": current_streak,
                "max_streak": max_streak,
                "expected_max": details["expected_max_streak"]
            })
        
        conn.commit()
        
        # Print summary
        print("\n[green]Test data generated successfully![/green]")
        print("\n[cyan]Habit Summary:[/cyan]")
        for habit in created_habits:
            print(f"\n[yellow]{habit['name']}[/yellow]")
            print(f"  Final Streak: {habit['final_streak']}")
            print(f"  Max Streak: {habit['max_streak']}")
            print(f"  Expected Max: {habit['expected_max']}")
            
        return created_habits
        
    except Exception as e:
        conn.rollback()
        print(f"[red]Error generating test data: {e}[/red]")
        return None 