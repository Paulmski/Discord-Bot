# file app/__main__.py

# Should be incremented each release.
version_code = 'v1.0.3'
def main():
    import string
    from discord.ext.commands import Bot
    from discord.ext import tasks, commands
    import discord.utils
    import random
    import os
    from dotenv import load_dotenv
    import gsapi_builder
    import sheets_parser
    import logging
    import events as events
    import urllib
    import re

    random.seed()  # Seed the RNG.
    load_dotenv()

    # Getting environment variables.
    SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
    RANGE_NAME = os.getenv('RANGE_NAME')
    COURSE_SHEET = os.getenv('COURSE_SHEET')
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    ANNOUNCEMENT_CHANNEL = os.getenv('ANNOUNCEMENT_CHANNEL')
    GUILD_ID = int(os.getenv('GUILD_ID'))

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
        logging.info('Logged In')
        logging.info('Username: ' + bot.user.name)
        logging.debug(bot.user.id)
        logging.info('== Connection Successful ==')

    # Print that the bot is connected to the server.
    @bot.event
    async def on_connect():
        logging.info('=== Connecting To Server ===')

    @bot.command(pass_context=True)
    async def version(ctx):
        '''
        Show current version.
        '''
        await ctx.channel.send(version_code)

    # Flip a coin and tell the user what the result was.
    @bot.command(pass_context=True)
    async def coinflip(ctx):
        '''
        Flips a coin.
        According to Teare and Murray's "Probability of a tossed coin landing on edge", extrapolations from a physical simulation model suggests "that the probability of an American nickel landing on edge is approximately 1 in 6000 tosses."
        
        Murray, Daniel B., and Scott W. Teare. “Probability of a Tossed Coin Landing on Edge.” Physical Review E, vol. 48, no. 4, 1993, pp. 2547–2552., https://doi.org/10.1103/physreve.48.2547.
        '''
        rand = random.randint(0, 6000)
        if rand == 777:
            responses = ['Holy cow, it landed on it\'s side!', 'You won\'t believe this but it landed on its side!',
                         'Despite all odds, it landed on it\'s side!']
            random_response = random.choice([0, len(responses)])
            await ctx.channel.send(responses[random_response])
        elif rand % 2 == 0:
            await ctx.channel.send('Heads!')
        elif rand % 2 == 1:
            await ctx.channel.send('Tails!')

    # Command to to fetch due dates on demand.
    @bot.command(pass_context=True)
    async def homework(ctx):
        await fetcher.fetch_due_dates(channel_id=ctx.channel.id)
        logging.info(f'User {ctx.author} requested homework.')

    # Command to list the assignments for a specific class.
    @bot.command(pass_context=True)
    async def list(ctx, *args):
        '''
        Lists the upcoming assignments within 14 days.

        !list all             - Lists every assignment due in 14 days.
        !list [code]          - Lists the course's assignments due in 14 days.
        !list courses         - Lists all courses in the semester.
        !list courses <codes> - Lists all courses of the subjects provided (e.g. "!list courses math comp entr").
        '''
        
        if len(args) == 0:
            await ctx.channel.send(
                'Invalid code entered, make sure you have the right course code e.g. `!list comp1271`.')
            return
        if SPREADSHEET_ID is None or RANGE_NAME is None:
            await ctx.channel.send('Internal error, no spreadsheet or range specified.')
            logging.warning('No SPREADSHEET_ID or RANGE_NAME specified in .env.')
            return

        final_assignments = []
        code = args[0].upper().replace('-', '').replace(' ','')
        assignments = sheets_parser.fetch_assignments(service, SPREADSHEET_ID, RANGE_NAME)

        message = '' # Message containing all specified courses.
        if code == 'COURSES':
            courses = sheets_parser.fetch_courses(service, SPREADSHEET_ID, COURSE_SHEET)
            final_courses = []
            if args[-1].upper() == 'COURSES':
                for course in courses:
                    if course.code not in message:
                        message += '\n' + course.code + ' - ' + course.name
            else:
                # This section of code is currently O(n^2) if it can be optimized please do.
                for arg in args:
                    for course in courses:
                        if arg.upper() in course.code:
                            # Checks if the course has already been added to the message.
                            if  course.code not in message:
                                message += '\n' + course.code + ' - ' + course.name
            await ctx.channel.send(message)
            return

        # Remove all courses that don't have a matching course code and aren't within 14 days.
        for assignment in assignments:
            if (code == 'ALL' or assignment.code == code) and -1 <= assignment.days_left <= 14:
                final_assignments.append(assignment)

        # No matching assignments found.
        if final_assignments == []:
            await ctx.channel.send(f'Couldn\'t find any assignments matching the course code "{code}".')
            return

        title = 'Assignments for {}'.format(code)
        await fetcher.announce_assignments(final_assignments, title=title, channel=ctx.channel, delete_after=6 * 60 * 60.0)
        logging.info(f'User {ctx.author} requested assignments for {code}.')

    # Command to create, modify permissions for, or delete private study groups.
    @bot.command(pass_context=True)
    async def group(ctx, *args):
        '''
        Creates private study groups.

        !group create [group_name] @users - Creates a private study group and invites the mentions.
        !group delete [group_name]        - Deletes a private study group you are in.
        !group add    [group_name] @users - Adds mentioned users to a study group you are in.
        '''
        # Iterates through arguments to obtain the group name of command. As soon as it encounters a special character it exits and the remaining characters are the designated group name.
        group_name = ''
        for word in args[1:]:
            for character in word:
                if character in string.ascii_letters + string.digits + '-':
                    group_name += character
                else:
                    break
            else:
                group_name += '-'
                continue
            break
        group_name = group_name.strip('-').lower()

        if group_name == '':
            await ctx.send('Invalid group name.')
            return
        # Or if the user tries to make a command on an already existing text-channel...
        for channel in ctx.guild.text_channels:
            if channel.category.name != 'study-groups' and channel.name == group_name:
                await ctx.send('You cannot call `!group` using other channels as arguments.')
                logging.info(
                    f'User {ctx.author} attempted to {args[0]} a study group using an already-existing channel name, #{group_name}.')
                return

                # Command to create a study group.
        if args[0] == 'create':

            # Check if a study group with the same name already exists.
            for text_channel in ctx.guild.text_channels:
                if text_channel.name == group_name:
                    await ctx.send(f'Sorry, {group_name} already exists!')
                    return

            # Create study group category if it doesn't exist.
            study_category = None
            for category in ctx.guild.categories:
                if category.name == 'study-groups':
                    study_category = category
            if study_category is None:
                study_category = await ctx.guild.create_category('study-groups')

            # Create the new text and voice channels.
            text_channel = await ctx.guild.create_text_channel(group_name, category=study_category)
            voice_channel = await ctx.guild.create_voice_channel(group_name, category=study_category)

            # Set channel so that @everyone cannot see it.
            await text_channel.set_permissions(ctx.guild.default_role, read_messages=False)
            await voice_channel.set_permissions(ctx.guild.default_role, read_messages=False)

            for member in ctx.message.mentions:
                # Allow mentioned user to view channel.
                await text_channel.set_permissions(member, read_messages=True)
                await voice_channel.set_permissions(member, read_messages=True)

            await text_channel.set_permissions(ctx.author, read_messages=True)
            await voice_channel.set_permissions(ctx.author, read_messages=True)

            logging.info(f'User {ctx.author} successfully created private study group "{group_name}".')

        # Command to delete a study group text and voice channel.
        # Requires that the author already has read permissions for the channel.
        elif args[0] == 'delete':

            channel_name = group_name
            text_channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)

            # Check if text_channel exists.
            if text_channel is None:
                await ctx.send(f'Sorry, "{group_name}" doesn\'t exist!')
                return

            # Check if permissions are valid.
            overwrite = text_channel.overwrites_for(ctx.author)
            if overwrite.read_messages == False:
                await ctx.send(f'Sorry, you don\'t have permissions to delete "{group_name}".')
                return

            # Delete the text and voice channel.
            await text_channel.delete()
            voice_channel = discord.utils.get(ctx.guild.voice_channels, name=channel_name)
            await voice_channel.delete()

            logging.info(f'User {ctx.author} successfully deleted private study group "{channel_name}".')

        # Add a new user to an already existing study group.
        elif args[0] == 'add':

            channel_name = group_name.lower()
            text_channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
            voice_channel = discord.utils.get(ctx.guild.voice_channels, name=channel_name)

            if text_channel is None or voice_channel is None:
                await ctx.send('Sorry, that study group doesn\'t exist!')
                return

            # Check if author has permission to add a new member.
            overwrite = text_channel.overwrites_for(ctx.author)
            if overwrite.read_messages == False:
                await ctx.send('Sorry, you don\'t have permissions to add a new member to this study group')
                return

            # Give permissions for all mentioned members.
            for member in ctx.message.mentions:
                await text_channel.set_permissions(member, read_messages=True)
                await voice_channel.set_permissions(member, read_messages=True)

            logging.info(f'User {ctx.author} added members to private study group "{channel_name}": {[x.name for x in ctx.message.mentions]}')

    # Print the message back.
    @bot.command(pass_context=True)
    async def repeat(ctx, *, arg):
        '''
        Repeats what you say and then deletes the message after 60 seconds.

        !repeat After me.  - Bot responds with "After me."
        '''
        await ctx.send(arg, delete_after=60)

    # Command for user to search YouTube for a tutorial video.
    @bot.command(pass_context=True)
    async def search(ctx, *, arg):
        '''
        Searches for a YouTube tutorial video based on your search query.

        !search Python Django - Searches for a Python Django tutorial on YouTube and returns the URL.
        '''
        arg_space = urllib.parse.quote(arg)
        html = urllib.request.urlopen('https://www.youtube.com/results?search_query={}'.format(arg_space))
        video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
        await ctx.channel.send('https://www.youtube.com/watch?v=' + video_ids[0])

        logging.info(f'User {ctx.author} searched for {arg_space}.')

    # Only instantiate assignment fetcher and time scheduler if SPREADSHEET_ID and RANGE_NAME are specified.
    if SPREADSHEET_ID is not None and RANGE_NAME is not None:
        # Instantiate FetchDate and EventScheduler class.
        fetcher = events.FetchDate(service=service, bot=bot)
        scheduler = events.EventScheduler(service=service, bot=bot)
    else:
        logging.warning('No SPREADSHEET_ID or RANGE_NAME specified in .env.')

    # Run the bot using the DISCORD_TOKEN constant from .env.
    bot.run(DISCORD_TOKEN)


if __name__ == '__main__':
    main()
