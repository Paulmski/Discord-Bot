# file app/sheets_parser.py

import logging

def fetch_due_dates(service, SPREADSHEET_ID=None, RANGE_NAME=None):

    if (SPREADSHEET_ID == None or RANGE_NAME == None):
        logging.warning('SPREADSHEET_ID or RANGE_NAME not defined in .env')
        return {}

    # Use Google Sheets API to fetch due dates.
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    # If no data was received, do not force any messages to be sent.
    if not values:
        logging.warning('No data found.')

    # Otherwise, send a message to @everyone about what assignments are due within a week.
    else:

        header = values[0] # Header row with column names (A1:E1)

        # Grab the indexes of the headers from A1:E1.
        index = {
            'Course Name': header.index('Course Name'),
            'Assignment Name': header.index('Assignment Name'),
            'Due Date': header.index('Due Date'),
            'Days Until Due Date': header.index('Days Until Due Date'),
            'Notes': header.index('Notes')
        }

        # Declare assignments dictionary, will become an argument for announce_due_dates().
        assignments = {}

        for row in values[1:]:
            # Should there be no IndexError raised...
            try:
                # If the class name has changed from the A column, change the current_class variable.
                if row[index['Course Name']] != '':
                    course = row[index['Course Name']]

                # Assign the assignment name, due date, and days until due date.
                assignment = row[index['Assignment Name']]
                due_date = row[index['Due Date']]
                days_left = row[index['Days Until Due Date']]

                # If there are notes in this row, assign the value to notes.
                if len(row) == 5:
                    notes = row[index['Notes']]

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
