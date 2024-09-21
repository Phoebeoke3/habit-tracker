from models.user import User

# edafe = User('EDAFE','edafe@gmail.com','eDafepassword')
# print(edafe)
from models.habit import Habit

# new_habit = Habit(id= 1, name='exercise', description='running', frequency='daily', streak_count=5)
# print(new_habit)

from models.user import User
from models.completion_record import Completion_record
from datetime import datetime
new_completion = Completion_record(id= 1, habit_id= 1, completion_date=datetime.utcnow())

# print(new_completion)
nero = User("nero1", "nero1@gmail.com", "" )
nero.save()
