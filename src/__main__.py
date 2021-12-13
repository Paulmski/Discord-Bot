# file app/__main__.py

def main():

    from discord.ext.commands import Bot
    from discord.ext import tasks, commands
    import discord.utils
    import random
    import secrets
    import os
    from dotenv import load_dotenv
    
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
    ANNOUNCEMENTS = int(os.getenv("ANNOUNCEMENTS"))

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

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

        # Declare a function to unload fetch_due_date cog.
        def cog_unload(self):
            self.fetch_due_dates.cancel()

        # fetch_due_dates loop.
        @tasks.loop(seconds=10.0)
        async def fetch_due_dates(self):
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
                header = values[0]             # Header row with column names (A1:E1)
                current_class = values[1][0]   # Name of the first class.

                # Grab the indexes of the headers from A1:E1.
                index = {
                    'Course Name': header.index('Course Name'),
                    'Assignment Name': header.index('Assignment Name'),
                    'Due Date': header.index('Due Date'),
                    'Days Until Due Date': header.index('Days Until Due Date'),
                    'Notes': header.index('Notes')
                }

                assignments = {}

                for row in values[1:]:
                    # Should there be no IndexError raised...
                    try:
                        # If the class name has changed from the A column, change the current_class variable.
                        if row[index['Course Name']] != '':
                            current_class = row[index['Course Name']]
                            assignments[current_class] = []

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
                            # print(current_class, assignment, due_date, days_left, notes)
                            assignments[current_class].append([assignment, due_date, days_left, notes])
                    
                    # Otherwise, print the row that caused the error.
                    except IndexError:
                        #print("Faulty row: ", row)
                        pass
            
            # Make a call to the @everyone event handler with the assignments dictionary passed as an argument.
            await announce_due_dates(assignments)

        @fetch_due_dates.before_loop
        async def before_fetch(self):
            print("Initiating data fetching.")

    # Instantiate FetchDate class.
    fetcher = FetchDate()

    # Declare a function to send an announcement to a hard-coded channel number in .env.
    @bot.event
    async def announce_due_dates(due_dictionary):
        await bot.wait_until_ready()
        channel = bot.get_channel(ANNOUNCEMENTS)
        await channel.send("@everyone booba")

    # Flip a coin and tell the user what the result was.
    @bot.command(pass_context=True)
    async def coinflip(ctx):
        '''
        According to Teare and Murray's "Probability of a tossed coin landing on edge", extrapolations from a physical simulation model
        suggests "that the probability of an American nickel landing on edge is approximately 1 in 6000 tosses."
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
                # TODO:(Allow for the ability to modify channel for announcement)
                channel = discord.utils.get(ctx.guild.channels, name=arg)
                await channel.send('This is the new announcement channel.')

    # Print the message back.
    @bot.command()
    async def repeat(ctx, *, arg):
        await ctx.send(arg)

    # Run the bot using the DISCORD_TOKEN constant from secrets.py.
    # For developers running their own version of the bot, create a secrets.py file to the src directory, and put the DISCORD_TOKEN as a variable.
    # Remember not to add the secrets.py file when committing/pushing.
    bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
  main()
  