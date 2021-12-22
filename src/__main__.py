# file app/__main__.py

def main():

    from discord.ext.commands import Bot
    from discord.ext import tasks, commands
    import discord.utils
    from discord.http import Route
    import random
    import os
    from dotenv import load_dotenv
    import gsapi_builder
    import sheets_parser
    from datetime import datetime
    from time import sleep
    import logging
    import events

    random.seed() # Seed the RNG.
    load_dotenv()

    # Getting environment variables.
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    RANGE_NAME = os.getenv("RANGE_NAME")
    COURSE_SHEET = os.getenv("COURSE_SHEET")
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    ANNOUNCEMENT_CHANNEL = os.getenv("ANNOUNCEMENT_CHANNEL")
    GUILD_ID = int(os.getenv("GUILD_ID"))

    # Logging formating to view time stamps and level of log information
    logging.basicConfig(
         format='%(asctime)s %(levelname)-8s %(message)s',
         level=logging.INFO,
         datefmt='%Y-%m-%d %H:%M:%S')

    # Build the Google Sheets API service.
    service = gsapi_builder.build_service()

    # Instantiate the bot, with the ! prefix preferred.
    bot = Bot(command_prefix='!')

    # Print the bot information upon bootup.
    @bot.event
    async def on_ready():
        logging.info('\nLogged in as\n' + bot.user.name)
        logging.debug(bot.user.id)
        print('------')

    # Print that the bot is connected to the server.
    @bot.event
    async def on_connect():
        logging.info("--Connected to server--")

    # Declare a function to send an announcement to a hard-coded channel number in .env.
    @bot.event
    async def announce_due_dates(due_date_dictionary, channel_id=None):
        # Preface with @everyone header.
        message = "@everyone"

        # Instantiate the Embed.
        embedded_message = discord.Embed(title="Due Dates For Today", colour=discord.Colour.from_rgb(160, 165, 25))

        await bot.wait_until_ready() # Bot needs to wait until ready to send message in correct channel.

        # Checks if a channel_id has been passed as an argument, then checks .env ANNOUNCEMENT_CHANNEL, then checks for announcements channel, otherwises returns error.
        if bot.get_channel(channel_id) != None:
            # If a channel ID is provided that means the function was called on demand, meaning @everyone should be avoided.
            message = ""
            channel = bot.get_channel(channel_id)
        elif bot.get_channel(int(ANNOUNCEMENT_CHANNEL)) != None:
            channel = bot.get_channel(int(ANNOUNCEMENT_CHANNEL))
        elif discord.utils.get(bot.get_all_channels(), name="announcements") != None:
            channel = discord.utils.get(bot.get_all_channels(), name="announcements")
        else:
            logging.error("Unable to find channel to send announcement to.")
            return

        # For every course in the due date dictionary...
        for course in due_date_dictionary.keys():
            course_assignments = ""
            for assignment in due_date_dictionary[course]:

                # Parse the information from the assignment list.
                name = assignment[0]
                due_date = assignment[1]
                days_left = int(assignment[2])

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
                    course_assignments += f"\n**{name}**\nDue on {due_date}, {datetime.now().year}.\n{days_left}\n\n"
                else:
                    course_assignments += f"\n**{name}**\nDue on {due_date}, {datetime.now().year}.\n{days_left}__Notes:__\n{notes}\n"
            
            # Add an extra embed field for the every course.
            embedded_message.add_field(name=f"__{course}__", value=course_assignments + "", inline=False)

        # Add project information to bottom.
        embedded_message.add_field(name="", value="\nI am part of the Lakehead CS 2021 Guild's Discord-Bot project! [Contributions on GitHub are welcome!](https://github.com/Paulmski/Discord-Bot/blob/main/CONTRIBUTING.md)")
        
        # Send the message to the announcements channel.
        await channel.send(message, embed=embedded_message, delete_after=86400.0)

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

    # Command to to fetch due dates on demand.
    @bot.command(pass_context=True)
    async def homework(ctx):
        await fetcher.fetch_due_dates(channel_id=ctx.channel.id)


    # Print the message back.
    @bot.command()
    async def repeat(ctx, *, arg):
        await ctx.send(arg)

    # Instantiate FetchDate and EventScheduler class.
    fetcher = events.FetchDate()
    scheduler = events.EventScheduler(service=service, bot=bot)

    # Run the bot using the DISCORD_TOKEN constant from .env.
    bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
  main()
