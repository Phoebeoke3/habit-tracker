def sort_habits(habits):
  '''This function sorts habit'''


  def sort_key(habit):
    '''This is the sort key function'''
    return habit[5] #This return the streak count, which have the index number "5" in the habit tuple
    
  return habits.sort(key=sort_key)