# file app/sheets_parser.py

import logging
from time import strftime
from datetime import datetime, timedelta
from classes.Assignment import Assignment
from classes.Course import Course

# Returns a dictionary containing assignment information.
def fetch_due_dates(service, SPREADSHEET_ID=None, RANGE_NAME=None):

    if (SPREADSHEET_ID == None or RANGE_NAME == None):
        logging.warning("SPREADSHEET_ID or RANGE_NAME not defined in .env")
        return None

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
            "notes": header.index("Notes")
        }

        # Declare assignments dictionary, will become an argument for announce_due_dates().
        assignments = {}

        for row in values[1:]:
            # Should there be no IndexError raised...
            try:

                # If the class name has changed from the A column, change the current course.
                if row[index["course"]] != "":
                    course = row[index["course"]]
                    assignments[course] = []

                assignment = Assignment()
                assignment.parse_values(row, index)

                if assignment.days_left >= 0 and assignment.days_left <= 7:
                    assignments[course].append([assignment.name, assignment.due.strftime("%B %d"), assignment.days_left, assignment.note])

            # Otherwise, pass.
            except IndexError:
                pass

        return assignments

# Returns JSON payloads to schedule events via HTTP.
def get_daily_schedule(service, SPREADSHEET_ID=None, COURSE_SHEET=None):

    if (SPREADSHEET_ID == None or COURSE_SHEET == None):
        logging.warning("SPREADSHEET_ID and COURSE_SHEET range not defined in .env.")
        return None

    events = []

    # Use Google Sheets API to fetch due dates.
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=COURSE_SHEET).execute()
    values = result.get("values", [])

    header = values[0] # Header row with column names.
    now = datetime.now()
    current_day = now.strftime("%A") # Formatted for weekday's full name.

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
        if row[index["day"]] == current_day:

            course = Course()
            course.parse_state(row, index)

            # Only returns events that are in the future.
            # Convert c_class GMT state to EST (GMT-05:00)
            if course.start_time + timedelta(hours=-5) < now:
                continue
            
            events.append(
                {
                    "entity_type": 3, # Value 3 is EXTERNAL events.
                    "entity_metadata": { "location": f"Room {course.room}" },
                    "name": f"{course.code} - {course.name}",
                    "privacy_level": 2, # Required value as per documentation.
                    "scheduled_start_time": str(course.start_time),
                    "scheduled_end_time": str(course.end_time),
                    "description": course.description
                }
            )

    return events
