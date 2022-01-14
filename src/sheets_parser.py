# file app/sheets_parser.py

import logging
from time import strftime
from datetime import datetime, timedelta
from classes.Assignment import Assignment
from classes.Course import Course

def fetch_assignments(service, SPREADSHEET_ID, RANGE_NAME):
    '''
    Uses the Google Sheet API to get every row in the Assignments workbook as a list.
    '''

    # Use Google Sheets API to fetch due dates.
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    # If no data was received, do not force any messages to be sent.
    if not values:
        logging.warning('No data found.')

    # Otherwise, create and return a list containing assignment information.
    else:

        header = values[0] # Header row with column names (A1:E1)

        # Grab the indexes of the headers from A1:E1.
        index = {
            'code': header.index('Code'),
            'course': header.index('Course'),
            'assignment': header.index('Assignment'),
            'due_date': header.index('Due'),
            'days_left': header.index('Days Left'),
            'notes': header.index('Notes'),
            'course_name': header.index('Course')
        }

        # Declare assignments list, will become an argument for announce_assignments() in events.py.
        assignments = []

        current_course = ''
        current_code = ''
        # Remove all courses that don't have a matching course code and aren't within 14 days.
        for row in values[1:]:
            assignment = Assignment()
            assignment.parse_state(row, index)

            # If the assignment doesn't have a name, it's not a valid entry.
            if assignment.name == '':
                continue

            if assignment.code != '':
                current_code = assignment.code
            else:
                assignment.code = current_code
            if assignment.course_name != '':
                current_course = assignment.course_name
            else:
                assignment.course_name = current_course
                
            assignments.append(assignment)

        return assignments

def fetch_courses(service, SPREADSHEET_ID, COURSE_SHEET):
    '''Returns a list of JSON payloads used to schedule events via HTTP.'''
    
    courses = []

    # Use Google Sheets API to fetch due dates.
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=COURSE_SHEET).execute()
    values = result.get('values', [])

    header = values[0] # Header row with column names.

    # Grab the indexes of the headers from A1:E1.
    index = {
        'code': header.index('Code'),
        'name': header.index('Name'),
        'day': header.index('Day'),
        'start_time': header.index('Time'),
        'end_time': header.index('Ends'),
        'room': header.index('Room'),
        'status': header.index('Status')
    }

    for row in values[1:]:
        course = Course()
        course.parse_state(row, index)
        courses.append(course)

    return courses
