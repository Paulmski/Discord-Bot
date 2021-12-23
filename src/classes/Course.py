from datetime import datetime



# Class to represent course information.
class Course():

    
 
               
    def __init__(self, code, name, note, start_time, end_time, room):
        self.code = code
        self.name = name
        self.note = note
        self.start_time = start_time
        self.end_time = end_time
        self.room = room
    
    
    
    
    
    
    
    
    
    
    
    
    # Setter and getter methods to maintain variable type integrity.
    @property
    def code(self):
        return self._price
    
    @code.setter
    def code(self, code):
        if not isinstance(code, str):
            raise TypeError("Invalid code argument. Must be a string")
        self._price = code
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("Invalid name argument. Must be a string")
        self._name = name
        
    @property
    def start_time(self):
        return self._start_time
    
    @start_time.setter
    def start_time(self, start_time):
        if not isinstance(start_time, datetime):
            raise TypeError("Invalid start_time argument. Must be a datetime")
        self._start_time = start_time
    
    @property
    def end_time(self):
        return self._end_time
    
    @end_time.setter
    def end_time(self, end_time):
        if not isinstance(end_time, datetime):
            print('hello')
            raise TypeError("Invalid end_time argument. Must be a datetime")
        self._end_time = end_time
            
    @property
    def note(self):
        return self._note
    
    @note.setter
    def note(self, note):
        if not isinstance(note, str):
            raise TypeError("Invalid note argument. Must be a string")
        self._room = note
            
    @property
    def room(self):
        return self._room

    @room.setter
    def room(self, room):
        if not isinstance(room, str):
            raise TypeError("Invalid note argument. Must be a string")
        self._room = room
        
    
    
    