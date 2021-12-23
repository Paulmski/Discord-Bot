from datetime import datetime, timedelta
from .parse_data import parse_data

# Class to represent course information.
class Course():
      
    def __init__(self, code="", name="", day="", description="", start_time=datetime.now(), end_time=datetime.now(), room=""):
        self.code = code
        self.name = name
        self.day = day
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.room = room
    
    # Setter and getter methods to maintain variable type integrity.
    @property
    def code(self):
        return self._code
    
    @code.setter
    def code(self, code):
        if not isinstance(code, str):
            raise TypeError("Invalid code argument. Must be a string")
        self._code = code
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("Invalid name argument. Must be a string")
        self._name = name

    @property
    def day(self):
        return self._day
    
    @day.setter
    def day(self, day):
        if not isinstance(day, str):
            raise TypeError("Invalid day argument. Must be a string")
        self._room = day

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description):
        if not isinstance(description, str):
            raise TypeError("Invalid description argument. Must be a string")
        self._room = description
        
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
            raise TypeError("Invalid end_time argument. Must be a datetime")
        self._end_time = end_time
            
    @property
    def room(self):
        return self._room

    @room.setter
    def room(self, room):
        if not isinstance(room, str):
            raise TypeError("Invalid day argument. Must be a string")
        self._room = room
    
    # Set values based on arguments.
    def parse_state(self, row_data, indexes):

        parsed_data = parse_data(row_data, indexes)
        now = datetime.now()

        # Convert EST times to GMT times conforming with ISO8601 formatting.
        # Timezone translation UTC-05:00 to UTC+00:00.
        gmt_start_time = datetime.strptime(now.strftime(f"%Y-%m-%dT") + parsed_data["start_time"], "%Y-%m-%dT%H:%M") + timedelta(hours=5)
        gmt_end_time = datetime.strptime(now.strftime(f"%Y-%m-%dT") + parsed_data['end_time'], "%Y-%m-%dT%H:%M") + timedelta(hours=5)
            
        # 12-hour time conversions.
        th_start_time = datetime.strptime(parsed_data["start_time"], "%H:%M").strftime("%I:%M%p")
        th_end_time = datetime.strptime(parsed_data["end_time"], "%H:%M").strftime("%I:%M%p")

        self._code = parsed_data["code"]
        self._name = parsed_data["name"]
        self._day = parsed_data["day"]
        self._start_time = gmt_start_time
        self._end_time = gmt_end_time
        self._room = parsed_data["room"]
        self._status = parsed_data["status"]
        self._description = f"{self.code} - {self.name} will take place on {gmt_start_time.strftime('%A, %B %d')} from {th_start_time} to {th_end_time} in Room {self.room}."
