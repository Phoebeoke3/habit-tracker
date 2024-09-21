'''This is the completion_record model'''

class Completion_record:
    '''This is the completion_record class'''
    def __init__(self, id, habit_id, completion_date):
        self.id = id
        self.habit_id = habit_id
        self.completion_date = completion_date
    def __str__(self):
        '''A method that returns the string of an object'''
        return f""" completion_record {self.id}
                  -------------------
                  habitID: \t {self.habit_id} 
                  completion: \t {self.completion_date}"""

            