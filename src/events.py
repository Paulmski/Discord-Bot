from discord.ext import tasks, commands
from time import sleep
import os
from datetime import datetime
import logging
import sheets_parser
from discord.http import Route
from dotenv import load_dotenv

# Declare the FetchDate class, inheriting methods from Cog.
class FetchDate(commands.Cog):
    def __init__(self):
        self.fetch_due_dates.start()

    # Declare a function to unload the fetch_due_date task.
    def cog_unload(self):
        self.fetch_due_dates.cancel()

    # Declare the fetch_due_dates loop. Loop will fully execute every 24 hours.
    @tasks.loop(minutes=60.0)
    async def fetch_due_dates(self, channel_id=None):
        if (datetime.now().hour != 6 and channel_id == None):
            return
        logging.info("Fetching due dates...")

        # Pass Sheets service and metadata to sheets_parser.fetch_due_dates()
        assignments = sheets_parser.fetch_due_dates(self.service, self.SPREADSHEET_ID, self.RANGE_NAME)

        # Make a call to the @everyone event handler with the assignments dictionary passed as an argument.
        await self.announce_due_dates(assignments, channel_id=channel_id)

    @fetch_due_dates.before_loop
    async def before_fetch(self):
        logging.debug("Initiating data fetching.")










# Declare EventScheduler Cog.
class EventScheduler(commands.Cog):
    load_dotenv()
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    RANGE_NAME = os.getenv("RANGE_NAME")
    COURSE_SHEET = os.getenv("COURSE_SHEET")
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    ANNOUNCEMENT_CHANNEL = os.getenv("ANNOUNCEMENT_CHANNEL")
    GUILD_ID = os.getenv("GUILD_ID")
   

    def __init__(self, service, bot):
        self.service = service
        self.bot = bot
        self.schedule_events.start()

    # Declare a function to unload the schedule_events task.
    def cog_unload(self):
        self.schedule_events.cancel()

    # Declare the schedule_events loop, which fully executes every 24 hours.
    @tasks.loop(minutes=60.0)
    async def schedule_events(self):
        
       
        
        if (datetime.now().hour != 6):
            return

        await self.bot.wait_until_ready() # Bot needs to wait until ready, especially on the first iteration.
        # Set the class' guild state (bot.get_guild() returns a Guild object)
        guild = self.bot.get_guild(int(self.GUILD_ID))
        logging.info(f"Scheduling to server {guild.name}.")

        # Get dictionary of daily event JSON payloads from sheets_parser.get_daily_schedule().
        schedule = sheets_parser.get_daily_schedule(self.service, self.SPREADSHEET_ID, self.COURSE_SHEET)
        print(schedule)
        # Post events using HTTP.
        route = Route("POST", f"/guilds/{self.GUILD_ID}/scheduled-events", guild_id=self.GUILD_ID)
        for event in schedule:
            await self.bot.http.request(route, json=event)
            sleep(0.5) # Waiting 0.5 seconds to prevent API limiting.
            

    @schedule_events.before_loop
    async def before_scheduling(self):
        logging.debug("Initiating event scheduler.")