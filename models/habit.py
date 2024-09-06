'''This is the habit model'''


class Habit:
    '''This is the habit class'''
    def __init__(self, id, name, description, frequency, streak_count):
        self.id = id
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

