from discord.ext import tasks, commands
import discord
from time import sleep
import os
from datetime import datetime
import logging
import sheets_parser
from discord.http import Route
from dotenv import load_dotenv

load_dotenv()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE_NAME = os.getenv("RANGE_NAME")
COURSE_SHEET = os.getenv("COURSE_SHEET")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ANNOUNCEMENT_CHANNEL = os.getenv("ANNOUNCEMENT_CHANNEL")
GUILD_ID = os.getenv("GUILD_ID")

# Declare the FetchDate class, inheriting methods from Cog.
class FetchDate(commands.Cog):
    def __init__(self, service, bot):
        self.service = service
        self.bot = bot
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
        assignments = sheets_parser.fetch_due_dates(self.service, SPREADSHEET_ID, RANGE_NAME)

        # Make a call to the @everyone event handler with the assignments dictionary passed as an argument.
        await self.announce_due_dates(assignments, channel_id=channel_id)

    @fetch_due_dates.before_loop
    async def before_fetch(self):
        logging.debug("Initiating data fetching.")

    # Declare a function to send an announcement to a hard-coded channel number in .env.
    async def announce_due_dates(self, due_date_dictionary, channel_id=None):
        # Preface with @everyone header.
        message = "@everyone"

        # Instantiate the Embed.
        embedded_message = discord.Embed(title="Due Dates For Today", colour=discord.Colour.from_rgb(160, 165, 25))

        await self.bot.wait_until_ready() # Bot needs to wait until ready to send message in correct channel.

        # Checks if a channel_id has been passed as an argument, then checks .env ANNOUNCEMENT_CHANNEL, then checks for announcements channel, otherwises returns error.
        if self.bot.get_channel(channel_id) != None:
            # If a channel ID is provided that means the function was called on demand, meaning @everyone should be avoided.
            message = ""
            channel = self.bot.get_channel(channel_id)
        elif self.bot.get_channel(int(ANNOUNCEMENT_CHANNEL)) != None:
            channel = self.bot.get_channel(int(ANNOUNCEMENT_CHANNEL))
        elif discord.utils.get(self.bot.get_all_channels(), name="announcements") != None:
            channel = discord.utils.get(self.bot.get_all_channels(), name="announcements")
        else:
            logging.error("Unable to find channel to send announcement to.")
            return

        # For every course in the due date dictionary...
        for course in due_date_dictionary.keys():
            if due_date_dictionary[course] == []:
                continue
            course_assignments = ""
            for assignment in due_date_dictionary[course]:

                # Parse the information from the assignment list.
                name = assignment[0]
                due_date = assignment[1]
                days_left = assignment[2]

                # Change days_left to a different code block color depending on days left.
                if days_left > 3:
                    days_left = f"```diff\n+ {days_left} days remaining.```"
                elif days_left > 0:
                    days_left = f"```fix\n- {days_left} days remaining.```"
                else:
                    days_left = f"```diff\n- {days_left} days remaining.```"

                notes = assignment[3]

                # Append the information to the course_assignments.
                if notes == "":
                    course_assignments += f"\n**{name}**\nDue on {due_date}, {datetime.now().year}.\n{days_left}\n"
                else:
                    course_assignments += f"\n**{name}**\nDue on {due_date}, {datetime.now().year}.\n{days_left}__Notes:__\n{notes}\n"
            
            # Add an extra embed field for every course.
            embedded_message.add_field(name=f"__{course}__", value=course_assignments + "", inline=False)

        # Add project information to bottom.
        embedded_message.add_field(name="", value="\nI am part of the Lakehead CS 2021 Guild's Discord-Bot project! [Contributions on GitHub are welcome!](https://github.com/Paulmski/Discord-Bot/blob/main/CONTRIBUTING.md)")
        
        # Send the message to the announcements channel.
        await channel.send(message, embed=embedded_message, delete_after=86400.0)

# Declare EventScheduler Cog.
class EventScheduler(commands.Cog):

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
        guild = self.bot.get_guild(int(GUILD_ID))
        logging.info(f"Scheduling to server {guild.name}.")

        # Get dictionary of daily event JSON payloads from sheets_parser.get_daily_schedule().
        schedule = sheets_parser.get_daily_schedule(self.service, SPREADSHEET_ID, COURSE_SHEET)

        if schedule == []:
            logging.info("No events were scheduled.")
        # Post events using HTTP.
        route = Route("POST", f"/guilds/{GUILD_ID}/scheduled-events", guild_id=GUILD_ID)
        for event in schedule:
            await self.bot.http.request(route, json=event)
            sleep(0.5) # Waiting 0.5 seconds to prevent API limiting.
            

    @schedule_events.before_loop
    async def before_scheduling(self):
        logging.debug("Initiating event scheduler.")