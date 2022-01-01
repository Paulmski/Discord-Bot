from classes.User import User

class Group():
    def __init__(self, ID=0, name="", owner=User()):
        self.ID = ID
        self.name = name
        self.owner = owner
        

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Invalid name must be a string not type: %s" % type(value))
        self._name = value
        
    
    
    @property()
    def ID(self):
        return self._ID
    
    @ID.setter
    def ID(self, value):
        if not isinstance(value, int):
            raise ValueError("Invalid ID must be a int not type: %s" % type(value))
        self._ID = value
        
        
    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise ValueError("Invalid owner must be a User not type: %s" % type(value))
        self._owner = value

