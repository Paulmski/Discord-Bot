from discord.ext import tasks, commands
import discord
from time import sleep
import os
from datetime import datetime, timedelta
import logging
import sheets_parser
from discord.http import Route
from dotenv import load_dotenv
from classes.Assignment import Assignment

load_dotenv()
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
RANGE_NAME = os.getenv('RANGE_NAME')
COURSE_SHEET = os.getenv('COURSE_SHEET')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
ANNOUNCEMENT_CHANNEL = os.getenv('ANNOUNCEMENT_CHANNEL')
GUILD_ID = os.getenv('GUILD_ID')

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
    @tasks.loop(minutes=60.00)
    async def fetch_due_dates(self):

        await self.bot.wait_until_ready()
        if (datetime.now().hour != 6):
            return
        channel = None
        # Check ANNOUNCEMENT_CHANNEL has been set otherwise use channel named announcements otherwise return error.
        if self.bot.get_channel(int(ANNOUNCEMENT_CHANNEL)) != None:
            channel = self.bot.get_channel(int(ANNOUNCEMENT_CHANNEL))
        elif discord.utils.get(self.bot.get_all_channels(), name='announcements') != None:
            channel = discord.utils.get(self.bot.get_all_channels(), name='announcements')
        else:
            logging.error('Unable to find channel to send announcement to.')
            return
        logging.info('Fetching due dates...')

        # Pass Sheets service and metadata to sheets_parser.fetch_due_dates()
        assignments = sheets_parser.fetch_assignments(self.service, SPREADSHEET_ID, RANGE_NAME)
        final_assignments = []
        for i, assignment in enumerate(assignments):
            # Only assignments that are in the next 14 days will be shown.
            if -1 <= assignment.days_left <= 7:
                final_assignments.append(assignment)

        # Make a call to the @everyone event handler with the assignments array passed as an argument.
        if final_assignments != []:
            # Delete the last announcement from this channel.
            title =  ':red_circle:Due Dates for Today:red_circle:'
            previous_messages = await channel.history(limit=10).flatten()
            
            for message in previous_messages:
                if len(message.embeds) > 0:
                    if message.embeds[0].title == title:
                        logging.info('Deleted previous Announcement message.')
                        await message.delete() 
                        sleep(4)
            await self.announce_assignments(final_assignments, title=':red_circle:Due Dates for Today:red_circle:', channel=channel)
        else:
            logging.info('No assignments found due soon.')
    @fetch_due_dates.before_loop
    async def before_fetch(self):
        logging.debug('Initiating data fetching.')
    
    
    # This function must be passed an array of assignments in which each assignment has its course code and course name
    async def announce_assignments(self, due_dates, title: str, channel: discord.TextChannel, delete_after=None):
        '''Sends a Discord message with assignment due dates based on a Context channel or Announcements channel ID in .env.'''

        # Instantiate the Embed.
        embedded_message = discord.Embed(title=title, colour=discord.Colour.from_rgb(160, 165, 25))

        await self.bot.wait_until_ready() # Bot needs to wait until ready to send message in correct channel.




          
        # For every course in the due date list...
        course_assignments = ''
        current_code = due_dates[0].code
        current_course_name = due_dates[0].course_name

        for i, assignment in enumerate(due_dates):

            # Default case where current assignment is the same course as the previous one.
            if assignment.code == current_code:
                course_assignments += self.format_assignment(assignment)

            # Default case when the assignment course differs from the previous one.
            else:
                embedded_message.add_field(name=f'__{current_code} - {current_course_name}__', value=course_assignments + '', inline=False)
                course_assignments = self.format_assignment(assignment)
                current_code = assignment.code
                current_course_name = assignment.course_name


        # Add the last field with the remaining course assignments.
        embedded_message.add_field(name=f'__{current_code} - {current_course_name}__', value=course_assignments + '', inline=False)
        
        # Add project information to bottom.
        embedded_message.add_field(name='\n\nAbout Me', value='I am part of the Lakehead CS 2021 Guild\'s Discord-Bot project! [Contributions on GitHub are welcome!](https://github.com/Paulmski/Discord-Bot/blob/main/CONTRIBUTING.md)')

        if isinstance(delete_after, float):
            await channel.send('', embed=embedded_message, delete_after=delete_after) 
        else:
            # Send the message to the announcements channel.
            await channel.send('', embed=embedded_message)

    def format_assignment(self, assignment: Assignment):
        '''
        Formats an Assignment object to a string that will be displayed in a Discord Embed.
        '''
        # Parse the information from the assignment list.
        name = assignment.name
        due_date = assignment.due.strftime('%A, %B %d')
        days_left = assignment.days_left

        # Change days_left to a different code block color depending on days left.
        if days_left > 3:
            days_left = f'```diff\n+ {days_left} days remaining.```'
        elif days_left > 0:
            days_left = f'```fix\n+ {days_left} days remaining.```'
        elif days_left == 0:
            days_left = '```diff\n Due today.```'
        else:
            days_left = f'```diff\n- {abs(days_left)} days late.```'

        notes = assignment.note

        # Append the information to the course_assignments.
        if notes == '':
            return f'\n**{name}**\nDue on {due_date}, {datetime.now().year}.\n{days_left}\n'
        else:
            return f'\n**{name}**\nDue on {due_date}, {datetime.now().year}.\n{days_left}__Notes:__\n{notes}\n'

# Declare EventScheduler Cog.
class EventScheduler(commands.Cog):

    def __init__(self, service, bot):
        self.service = service
        self.bot = bot
        self.schedule_events.start()
        self.purge_study_groups.start()

    # Declare a function to unload the schedule_events task.
    def cog_unload(self):
        self.schedule_events.cancel()
        self.purge_study_groups.cancel()

    # Declare the schedule_events loop, which fully executes every 24 hours.
    @tasks.loop(minutes=60.0)
    async def schedule_events(self):
        
        if (datetime.now().hour != 6):
            return
        
        await self.bot.wait_until_ready() # Bot needs to wait until ready, especially on the first iteration.
        # Set the class' guild state (bot.get_guild() returns a Guild object)
        guild = self.bot.get_guild(int(GUILD_ID))
        logging.info(f'Scheduling to server {guild.name}.')

        # Get dictionary of daily event JSON payloads from sheets_parser.get_daily_schedule().
        schedule = sheets_parser.fetch_courses(self.service, SPREADSHEET_ID, COURSE_SHEET)

        if schedule == []:
            logging.info('No events were scheduled.')
        # Post events using HTTP.
        route = Route('POST', f'/guilds/{GUILD_ID}/scheduled-events', guild_id=GUILD_ID)

        now = datetime.now() + timedelta(hours=5)
        current_day = now.strftime('%A') # Formatted for weekday's full name.
        for course in schedule:
            if course.day == current_day and course.start_time > now:
                event = course.to_json_event()
                await self.bot.http.request(route, json=event)
                sleep(0.5) # Waiting 0.5 seconds to prevent API limiting.
                
    @tasks.loop(minutes=1)
    async def purge_study_groups(self):

        guild = self.bot.get_guild(int(GUILD_ID))
        if guild is None: return

        for channel in guild.text_channels:
            if channel.category is None: continue
            if channel.category.name != 'study-groups': continue

            # Get the most recent message from channel if there is a message.
            messages = await channel.history(limit=1).flatten()
            last_message = None
            if len(messages) == 1:
                last_message = messages[0]

            if last_message is None: continue
            
            if (datetime.now() - last_message.created_at).total_seconds() > 13 * 24 * 60 * 60:
                channel.send_message('@everyone\nThis channel will be deleted if it is inactive for 1 more day.')
                
            if (datetime.now() - last_message.created_at).total_seconds() > 14 * 23 * 60 * 60:
                channel.send_message('@everyone\nThis channel will be deleted if it is inactive for 1 more hour.')
                
            # Study group inactive for 14 days will be deleted.
            if (datetime.now() - last_message.created_at).total_seconds() > 14 * 24 * 60 *60:
                voice_channel = discord.utils.get(guild.voice_channels, name=channel.name)
                await voice_channel.delete()
                await channel.delete()
                logging.info(f'Study group {channel.name} was removed due to inactivity.')
  
    @schedule_events.before_loop
    async def before_scheduling(self):
        logging.debug('Initiating event scheduler.')
