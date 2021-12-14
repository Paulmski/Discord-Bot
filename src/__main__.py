# file app/__main__.py

def main():

    from discord.ext.commands import Bot
    from discord.ext import tasks, commands
    import discord.utils
    import random
    import secrets
    import os
    from dotenv import load_dotenv
    from datetime import datetime
    
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

    random.seed() # Seed the RNG.
    load_dotenv()

    # Enforcing read only scope for Google Sheets API.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # Getting environment variables.
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    RANGE_NAME = os.getenv("RANGE_NAME")
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    ANNOUNCEMENT_CHANNEL = os.getenv("ANNOUNCEMENT_CHANNEL")

    # Establish a connection to the Google Sheets API.
    # The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
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

    # Build the Google Sheets API service.
    service = build('sheets', 'v4', credentials=creds)

    # Instantiate the bot, with the ! prefix preferred.
    bot = Bot(command_prefix='!')

    # Print the bot information upon bootup.
    @bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')
     
    # Print that the bot is connected to the server.
    @bot.event
    async def on_connect():
        print("--Connected to server--")

    # Declare the FetchDate class, inheriting methods from Cog.
    class FetchDate(commands.Cog):
        def __init__(self):
            self.fetch_due_dates.start()

        # Declare a function to unload the fetch_due_date cog.
        def cog_unload(self):
            self.fetch_due_dates.cancel()

        # Declare the fetch_due_dates loop. Loop will run every 24 hours.
        @tasks.loop(minutes=30.0)
        async def fetch_due_dates(self):
            if (datetime.now().hour != 6):
                return
            print("Fetching due dates...")

            # Use Google Sheets API to fetch due dates.
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
            values = result.get('values', [])

            # If no data was received, do not force any messages to be sent. 
            if not values:
                print('No data found.')

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
            
            # Make a call to the @everyone event handler with the assignments dictionary passed as an argument.
            await announce_due_dates(assignments)

        @fetch_due_dates.before_loop
        async def before_fetch(self):
            print("Initiating data fetching.")

    # Declare a function to send an announcement to a hard-coded channel number in .env.
    @bot.event
    async def announce_due_dates(due_date_dictionary):
        # Preface with @everyone header.
        message = "@everyone\n*Due Dates For Today!*\n\n"

        await bot.wait_until_ready() # Bot needs to wait until ready to send message in correct channel.
        
        # If ANNOUNCEMENT_CHANNEL is in .env, send to the channel ID. Otherwise, send to a channel called #announcements.
        if ANNOUNCEMENT_CHANNEL != None:
            channel = bot.get_channel(int(ANNOUNCEMENT_CHANNEL))
        else:
            channel = discord.utils.get(bot.get_all_channels(), name="announcements")

        # For every course in the due date dictionary...
        for course in due_date_dictionary.keys():
            message += f"> {course}\n\n"
            for assignment in due_date_dictionary[course]:

                # Parse the information from the assignment list.
                name = assignment[0]
                due_date = assignment[1]
                days_left = assignment[2]
                notes = assignment[3]

                # Append the information to the final message.
                if notes == "":
                    message += f"**{name}**\nDue on {due_date}, {datetime.now().year}.\n_{days_left} days remaining._\n\n"
                else:
                    message += f"**{name}**\nDue on {due_date}, {datetime.now().year}.\n_{days_left} days remaining._\n__Notes:__\n{notes}\n\n"
        
        # Send the message to the announcements channel.
        await channel.send(message)

    # Flip a coin and tell the user what the result was.
    @bot.command(pass_context=True)
    async def coinflip(ctx):
        '''
        According to Teare and Murray's "Probability of a tossed coin landing on edge", extrapolations from a physical simulation model suggests "that the probability of an American nickel landing on edge is approximately 1 in 6000 tosses."
        Murray, Daniel B., and Scott W. Teare. “Probability of a Tossed Coin Landing on Edge.” Physical Review E, vol. 48, no. 4, 1993, pp. 2547–2552., https://doi.org/10.1103/physreve.48.2547. 
        '''
        rand = random.randint(0, 6000)
        if rand == 777:
            responses = ['Holy cow, it landed on it\'s side!', 'You won\'t believe this but it landed on its side!', 'Despite all odds, it landed on it\'s side!']
            random_response = random.choice([0, len(responses)])
            await ctx.channel.send(responses[random_response])
        elif rand % 2 == 0:
            await ctx.channel.send('Heads!')
        elif rand % 2 == 1:
            await ctx.channel.send('Tails!')

    # Command to make an announcement to whole server, but in a specific channel.
    @bot.command(pass_context=True)
    async def announce(ctx, subCommand: str, subSubCommand: str, arg: str):
        # Used to configure settings related to this command.
        if (subCommand == 'config'):
            # Used to configure which channel the bot should make announcements too.
            if (subSubCommand == 'channel'):
                # TODO: Allow for the ability to modify channel for announcement.
                channel = discord.utils.get(ctx.guild.channels, name=arg)
                await channel.send('This is the new announcement channel.')

    # Print the message back.
    @bot.command()
    async def repeat(ctx, *, arg):
        await ctx.send(arg)

    # Instantiate FetchDate class.
    fetcher = FetchDate()

    # Run the bot using the DISCORD_TOKEN constant from .env.
    # For developers running their own version of the bot, create a file called .env in the src directory, and assign the bot's token as a String to a constant called DISCORD_TOKEN.
    # Remember not to add the .env file when committing/pushing.
    bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
  main()
  