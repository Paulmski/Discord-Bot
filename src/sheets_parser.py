# file app/sheets_parser.py

import logging
from time import strftime
from datetime import datetime, timedelta
from classes.Assignment import Assignment
from classes.Course import Course

# Returns a dictionary containing assignment information.
def fetch_assignments(service, SPREADSHEET_ID, RANGE_NAME):

  

    # Use Google Sheets API to fetch due dates.
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get("values", [])

    # If no data was received, do not force any messages to be sent.
    if not values:
        logging.warning("No data found.")

    # Otherwise, create and return a dictionary containing assignment information.
    else:

        header = values[0] # Header row with column names (A1:E1)

        # Grab the indexes of the headers from A1:E1.
        index = {
            "code": header.index("Code"),
            "course": header.index("Course"),
            "assignment": header.index("Assignment"),
            "due_date": header.index("Due"),
            "days_left": header.index("Days Left"),
            "notes": header.index("Notes"),
            "course_name": header.index("Course")
            
        }

        # Declare assignments dictionary, will become an argument for announce_due_dates().
        assignments = []

        for row in values[1:]:
            # This means the row is missing a title and should be skipped (it is probably missing other key information).
         

            assignment = Assignment()
            assignment.parse_state(row, index)
            if assignment.name != '':
                assignments.append(assignment)
                

        return assignments

# Returns JSON payloads to schedule events via HTTP.
def fetch_courses(service, SPREADSHEET_ID, COURSE_SHEET):

    

    courses = []

    # Use Google Sheets API to fetch due dates.
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=COURSE_SHEET).execute()
    values = result.get("values", [])

    header = values[0] # Header row with column names.

    # Grab the indexes of the headers from A1:E1.
    index = {
        "code": header.index("Code"),
        "name": header.index("Name"),
        "day": header.index("Day"),
        "start_time": header.index("Time"),
        "end_time": header.index("Ends"),
        "room": header.index("Room"),
        "status": header.index("Status")
    }

    for row in values[1:]:

        course = Course()
        course.parse_state(row, index)
        courses.append(course)


    return courses
