from models.user import User

# edafe = User('EDAFE','edafe@gmail.com','eDafepassword')
# print(edafe)
from models.habit import Habit

new_habit = Habit(id= 1, name='exercise', description='running', frequency='daily', streak_count=5)
print(new_habit)