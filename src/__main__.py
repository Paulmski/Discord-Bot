# file app/__main__.py

def main():

    from discord.ext.commands import Bot
    from discord.ext import tasks, commands
    import discord.utils
    import random
    import secrets
    
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

    # Enforcing read only scope for Google Sheets API.
    # Add the Google Sheets spreadsheet to secrets.py.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SPREADSHEET_ID = secrets.SPREADSHEET_ID

    random.seed() # Seed the RNG.
    
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
            # TODO: Use Google Sheets API to fetch due dates.
            pass

        @fetch_due_dates.before_loop
        async def before_fetch(self):
            print("Initiating date fetching.")

    # Instantiate FetchDate class.
    fetcher = FetchDate()

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
    bot.run(secrets.DISCORD_TOKEN)

if __name__ == '__main__':
  main()
  