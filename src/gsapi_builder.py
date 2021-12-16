# file app/gsapi_builder.py

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

# Enforcing read only scope for Google Sheets API.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Establish a connection to the Google Sheets API.
# The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
def build_service():   
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If token.json does not exist, log in manually.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials in token.json for the next run.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('sheets', 'v4', credentials=creds)
    