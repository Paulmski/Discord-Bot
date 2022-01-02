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
    import events as events
    import elections


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

    # Command to list the assignments for a specific class.
    @bot.command(pass_context=True)
    async def list(ctx, code=None):
        if code == None:
            await ctx.channel.send('Invalid code entered, make sure you have the right course code e.g. "!list comp1271".')
            return
        
        code = code.upper().replace('-', '').replace(' ','')
        assignments = sheets_parser.fetch_assignments(service, SPREADSHEET_ID, RANGE_NAME)
        final_assignments = []
        is_relevant = False

        # Remove all courses that don't have a matching course code and aren't within 14 days.
        for assignment in assignments:
            if code == 'ALL' and (0 <= assignment.days_left <= 14):
                final_assignments.append(assignment)
            elif (assignment.code == code or is_relevant) and (0 <= assignment.days_left <= 14):
                final_assignments.append(assignment)
                is_relevant = True
            else:
                is_relevant = False

        # No matching assignments found.
        if final_assignments == []:
            await ctx.channel.send('Couldn\'t find any assignments matching the course code "{}".'.format(code))
            return
        
        title = "Assignments for {}".format(code)
        await fetcher.announce_assignments(final_assignments, title=title, channel_id=ctx.channel.id)
        
        
        
        
        
    @bot.command(pass_context=True)
    async def group(ctx, *args):
        
        if args[0] == 'create':
            if args[1] is None or '@' in args[1]: 
                await ctx.send('Sorry, invalid group name.')
                return
            group_name = args[1].lower()
            # Check if a study group with the same name already exists.
            for channel in ctx.guild.text_channels:
                if channel.name == group_name:
                    await ctx.send('Sorry, that study group name already exists!')
                    return
        
                
            # Create new channel
            channel = await ctx.guild.create_text_channel(group_name)
            # Set channel so that @everyone cannot see it.
            await channel.set_permissions(ctx.guild.default_role, read_messages=False)
            
            
            for member in ctx.message.mentions:
                # Allow mentioned user to view channel.
                await channel.set_permissions(member, read_messages=True)
                
            
            await channel.set_permissions(ctx.author, read_messages=True)
            
            
    # Print the message back.
    @bot.command(pass_context=True)
    async def repeat(ctx, *, arg):
        await ctx.send(arg)

    # Instantiate FetchDate and EventScheduler class.
    fetcher = events.FetchDate(service=service, bot=bot)
    scheduler = events.EventScheduler(service=service, bot=bot)
    election = elections.ElectionSystem(bot=bot)

    # Run the bot using the DISCORD_TOKEN constant from .env.
    bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
  main()
