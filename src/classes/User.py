# Class to represent a user stored in database
class User():
    def __init__(self, ID=0, name=""):
        self.ID = ID
        self.name = name

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Invalid name must be a string not type: %s" % type(value))
        self._name = value
        
    # The ID must be the UUID of the user
    @property()
    def ID(self):
        return self._ID
    
    @ID.setter
    def ID(self, value):
        if not isinstance(value, int):
            raise ValueError("Invalid ID must be a int not type: %s" % type(value))
        self._ID = value
