'''This is the habit model'''

from models.base_model import BaseModel

class Habit(BaseModel):
    '''This is the habit class'''

    __table_name__= "habits"

    def __init__(self, name, description, frequency, streak_count):
        super().__init__()
        self.name = name
        self.description = description
        self.frequency = frequency
        self.streak_count = streak_count
    def __str__(self):
        '''A method that returns the string representation of an object '''
        return f''' habit {self.id}
                 ---------------
                 habit_name: \t {self.name}
                 habit_description: \t {self.description} 
                 habit_frequency: \t {self.frequency}
                 habit_streakcount: \t {self.streak_count} '''

