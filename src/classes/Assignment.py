from datetime import date, datetime



# Class to represent all assignments
class Assignment():
    
    def __init__(self, code, name, due, note):
        self.code = code
        self.name = name
        self.due = due
        self.note = note
        
    # Course code 
    @property
    def code(self):
        return self._code
    
    @code.setter
    def code(self, code):
        if not isinstance(code, str):
            raise TypeError("Invalid code argument. Must be a string.")
        self._code = code
        
        
    # Name of course
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("Invalid name argument. Must be a string.")
        self._name = name
    
    
    # Due date of assignment     
    @property
    def due(self):
        return self._due
    
    @due.setter
    def due(self, due):
        if not isinstance(due, datetime):
            raise TypeError("Invalid name argument. Must be a datetime")
        self._due = due
    
    # Any notes on assignment 
    @property
    def note(self):
        return self.note
    
    @note.setter
    def note(self, note):
        if not isinstance(note, str):
            raise TypeError("Invalid note argument. Must be a string")
        self._note = note
            

