import logging
from datetime import date, datetime
from .parse_data import parse_data

# Class to represent all assignments
class Assignment():
    
    def __init__(self, code='', name='', due=datetime.now(), note='', course_name=''):
        self.code = code
        self.name = name
        self.due = due
        self.note = note
        self.course_name = course_name
        
    # Course code 
    @property
    def code(self):
        return self._code
    
    @code.setter
    def code(self, code):
        if not isinstance(code, str):
            raise TypeError('Invalid code argument. Must be a string.')
        self._code = code
        
    # Name of course
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError('Invalid name argument. Must be a string.')
        self._name = name
      
    # Due date of assignment     
    @property
    def due(self):
        return self._due
    
    @due.setter
    def due(self, due):
        if not isinstance(due, datetime):
            raise TypeError('Invalid due argument. Must be a datetime')
        self._due = due
    
    # Days left on assignment
    @property
    def days_left(self):
        delta = self.due - datetime.now()
        return delta.days + 1
    

    # Any notes on assignment 
    @property
    def note(self):
        return self._note
    
    @note.setter
    def note(self, note):
        if not isinstance(note, str):
            raise TypeError('Invalid note argument. Must be a string')
        self._note = note

    @property
    def course_name(self):
        return self._course_name

    @course_name.setter
    def course_name(self, course_name):
        if not isinstance(course_name, str):
            raise TypeError('Invalid course_name argument. Must be a string')
        self._course_name = course_name
            
    def parse_state(self, row_data, indexes):
        '''Parses values from Google Sheet rows to set the object's state.'''
        
        parsed_data = parse_data(row_data, indexes)

        # If due_date from the parsed_data is empty, it's must be an empty row.
        if parsed_data['due_date'] == None or parsed_data['due_date'] == '':
            return

        self.code = parsed_data['code']
        self.name = parsed_data['assignment']
        try:
            self.due = datetime.strptime(parsed_data['due_date'], '%B %d, %Y')
        except ValueError:
            try:
                self.due = datetime.strptime(parsed_data['due_date'], '%B %d')
                self.due = self.due.replace(self.due.year + (datetime.now().year - 1900))
            except ValueError:
                try:
                    self.due = datetime.strptime(parsed_data['due_date'], '%b %d')
                    self.due = self.due.replace(self.due.year + (datetime.now().year - 1900))
                except ValueError:
                    logging.warning('Unable to parse due_date {}'.format(parsed_data['due_date']))
                    return
        self.course_name = parsed_data['course_name']
        if parsed_data['notes'] != None:
            self.note = parsed_data['notes']
