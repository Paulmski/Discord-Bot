# from discord.ext import tasks, commands
# import discord
# from time import sleep
# import os
# from datetime import datetime
# import logging
# import sheets_parser
# from discord.http import Route
# from dotenv import load_dotenv
# from classes.Assignment import Assignment

# load_dotenv()
# SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
# RANGE_NAME = os.getenv("RANGE_NAME")
# COURSE_SHEET = os.getenv("COURSE_SHEET")
# DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# ANNOUNCEMENT_CHANNEL = os.getenv("ANNOUNCEMENT_CHANNEL")
# GUILD_ID = os.getenv("GUILD_ID")

# # Declare the FetchDate class, inheriting methods from Cog.
# class FetchDate(commands.Cog):
#     def __init__(self, service, bot):
#         self.service = service
#         self.bot = bot
#         self.fetch_due_dates.start()

#     # Declare a function to unload the fetch_due_date task.
#     def cog_unload(self):
#         self.fetch_due_dates.cancel()

#     # Declare the fetch_due_dates loop. Loop will fully execute every 24 hours.
#     @tasks.loop(minutes=60.0)
#     async def fetch_due_dates(self, channel_id=None):
#         if (datetime.now().hour != 6 and channel_id == None):
#             return
#         logging.info("Fetching due dates...")

#         # Pass Sheets service and metadata to sheets_parser.fetch_due_dates()
#         assignments = sheets_parser.fetch_assignments(self.service, SPREADSHEET_ID, RANGE_NAME)
#         final_assignments = []
#         for i, assignment in enumerate(assignments):
#             # Only assignments that are in the next 7 days will be shown.
#             if 0 <= assignment.days_left <= 7:
#                 final_assignments.append(assignment)

#         # Make a call to the @everyone event handler with the assignments array passed as an argument.
#         if final_assignments != []:
#             await self.announce_assignments(final_assignments, title="Due Dates For Today",
# channel_id=channel_id)
#         elif channel_id != None:
#             channel = self.bot.get_channel(channel_id)
#             await channel.send('Looks like there\'s no assignments in the next 7 days, you can relax... for now.')
        

#     @fetch_due_dates.before_loop
#     async def before_fetch(self):
#         logging.debug("Initiating data fetching.")

#     async def announce_assignments(self, due_dates, title: str, channel_id=None):
#         """Sends a Discord message with assignment due dates based on a Context channel or Announcements channel ID in .env."""

#         # Preface with @everyone header.
#         message = "@everyone"

#         # Instantiate the Embed.
#         embedded_message = discord.Embed(title=title, colour=discord.Colour.from_rgb(160, 165, 25))

#         await self.bot.wait_until_ready() # Bot needs to wait until ready to send message in correct channel.

#         # Checks if a channel_id has been passed as an argument, then checks .env ANNOUNCEMENT_CHANNEL, then checks for announcements channel, otherwises returns error.
#         if self.bot.get_channel(channel_id) != None:
#             # If a channel ID is provided that means the function was called on demand, meaning @everyone should be avoided.
#             message = ""
#             channel = self.bot.get_channel(channel_id)
#         elif self.bot.get_channel(int(ANNOUNCEMENT_CHANNEL)) != None:
#             channel = self.bot.get_channel(int(ANNOUNCEMENT_CHANNEL))
#         elif discord.utils.get(self.bot.get_all_channels(), name="announcements") != None:
#             channel = discord.utils.get(self.bot.get_all_channels(), name="announcements")
#         else:
#             logging.error("Unable to find channel to send announcement to.")
#             return
          
#         # For every course in the due date list...
#         course_assignments = ""
#         due_dates_count = len(due_dates) - 1
#         current_course = due_dates[0].course_name
#         code = due_dates[0].code

#         for i, assignment in enumerate(due_dates):
#             # Finish the course field if the course name has changed.
#             if assignment.course_name != current_course and assignment.course_name != "":
#                 embedded_message.add_field(name=f"__{code} - {current_course}__", value=course_assignments + "", inline=False)
#                 course_assignments = ""
#                 current_course = assignment.course_name
#                 code = assignment.code
#                 course_assignments += self.format_assignment(assignment)

#             # Finish the course field if it is the last Assignment element.
#             elif i == due_dates_count:
#                 course_assignments += self.format_assignment(assignment)
#                 embedded_message.add_field(name=f"__{code} - {current_course}__", value=course_assignments + "", inline=False)

#             # Otherwise, add the assignment to course_assignments as normal.
#             else:
#                 course_assignments += self.format_assignment(assignment)

#         # Add project information to bottom.
#         embedded_message.add_field(name="\n\nAbout Me", value="I am part of the Lakehead CS 2021 Guild's Discord-Bot project! [Contributions on GitHub are welcome!](https://github.com/Paulmski/Discord-Bot/blob/main/CONTRIBUTING.md)")
    
#         # Send the message to the announcements channel.
#         await channel.send(message, embed=embedded_message, delete_after=86400.0)

#     def format_assignment(self, assignment: Assignment):
#         """Formats an Assignment object to a string that will be displayed in a Discord Embed."""
#         # Parse the information from the assignment list.
#         name = assignment.name
#         due_date = assignment.due.strftime("%A, %B %d")
#         days_left = assignment.days_left

#         # Change days_left to a different code block color depending on days left.
#         if days_left > 3:
#             days_left = f"```diff\n+ {days_left} days remaining.```"
#         elif days_left > 0:
#             days_left = f"```fix\n- {days_left} days remaining.```"
#         else:
#             days_left = f"```diff\n- {days_left} days remaining.```"

#         notes = assignment.note

#         # Append the information to the course_assignments.
#         if notes == "":
#             return f"\n**{name}**\nDue on {due_date}, {datetime.now().year}.\n{days_left}\n"
#         else:
#             return f"\n**{name}**\nDue on {due_date}, {datetime.now().year}.\n{days_left}__Notes:__\n{notes}\n"

# # Declare EventScheduler Cog.
# class EventScheduler(commands.Cog):

#     def __init__(self, service, bot):
#         self.service = service
#         self.bot = bot
#         self.schedule_events.start()

#     # Declare a function to unload the schedule_events task.
#     def cog_unload(self):
#         self.schedule_events.cancel()

#     # Declare the schedule_events loop, which fully executes every 24 hours.
#     @tasks.loop(minutes=60.0)
#     async def schedule_events(self):
        
#         if (datetime.now().hour != 6):
#             return

#         await self.bot.wait_until_ready() # Bot needs to wait until ready, especially on the first iteration.
#         # Set the class' guild state (bot.get_guild() returns a Guild object)
#         guild = self.bot.get_guild(int(GUILD_ID))
#         logging.info(f"Scheduling to server {guild.name}.")

#         # Get dictionary of daily event JSON payloads from sheets_parser.get_daily_schedule().
#         schedule = sheets_parser.fetch_courses(self.service, SPREADSHEET_ID, COURSE_SHEET)

#         if schedule == []:
#             logging.info("No events were scheduled.")
#         # Post events using HTTP.
#         route = Route("POST", f"/guilds/{GUILD_ID}/scheduled-events", guild_id=GUILD_ID)

#         now = datetime.now()
#         current_day = now.strftime("%A") # Formatted for weekday's full name.
#         for course in schedule:
#             if course.day == current_day and course.start_time > now:
#                 event = course.to_json_event()
#                 await self.bot.http.request(route, json=event)
#                 sleep(0.5) # Waiting 0.5 seconds to prevent API limiting.
            
#     @schedule_events.before_loop
#     async def before_scheduling(self):
#         logging.debug("Initiating event scheduler.")