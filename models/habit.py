'''This is the file containing habit model'''

from datetime import datetime 

class Habit:
    '''This is the Habit class'''

    def __init__(self, name, description, user_id, periodicity):
        '''Constructor method'''

        self.name = name
        self.description = description
        self.start_date = datetime.now()
        self.user_id = user_id
        self.streak_count = 0
        self.periodicity = periodicity
        self.last_completed_date = None
