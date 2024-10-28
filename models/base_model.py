'''This is the base model module'''

from uuid import uuid4
import models

class BaseModel:
    '''This is the base class'''

    def __init__(self):
       self.id = str(uuid4())

    def save(self):
        models.storage.save(self)