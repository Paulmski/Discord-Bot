# file app/sheets_parser.py

import logging
from time import strftime
from discord.http import Route
from datetime import datetime

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
            "course": header.index("Course Name"),
            "assignment": header.index("Assignment Name"),
            "due_date": header.index("Due Date"),
            "days_until": header.index("Days Until Due Date"),
            "notes": header.index("Notes")
        }

        # Declare assignments dictionary, will become an argument for announce_due_dates().
        assignments = {}

        for row in values[1:]:
            # Should there be no IndexError raised...
            try:
                # If the class name has changed from the A column, change the current_class variable.
                if row[index["course"]] != "" and not (row[index["course"]].startswith("Room") or row[index["course"]].startswith("Meetings")):
                    course = row[index["course"]]

                # Assign the assignment name, due date, and days until due date.
                assignment = row[index["assignment"]]
                due_date = row[index["due_date"]]
                days_left = row[index["days_until"]]

                # If there are notes in this row, assign the value to notes.
                if len(row) == 5:
                    notes = row[index["notes"]]

                # Otherwise, just assign it as a blank value.
                else:
                    notes = ""

                # If the assignment is due in a week, add it to the final message to @everyone.
                if int(days_left) >= 0 and int(days_left) <= 7:
                    if course not in assignments.keys():
                        assignments[course] = []
                    assignments[course].append([assignment, due_date, days_left, notes])

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
        "course": header.index("Course Name"),
        "day": header.index("Day"),
        "time": header.index("Time"),
        "end_time": header.index("Ends"),
        "room": header.index("Room")
    }

    for row in values[1:]:
        if row[index["day"]] == current_day:
            events.append(
                {
                    "entity-type": "EXTERNAL",
                    "entity-metadata": f"Room {row[index['room']]}",
                    "name": row[index["course"]],
                    "privacy_level": 2, # Required value as per documentation.
                    "scheduled_start_time": now.strftime(f"%Y-%m-%d {row[index['time']]}"),
                    "scheduled_end_time": now.strftime(f"%Y-%m-%d {row[index['end_time']]}"),
                    "description": f"{row[index['course']]} will take place on {now.strftime('%B %d')} at {now.strftime('%I:%M%p')} in Room {row[index['room']]}."
                }
            )

    return events
