# file app/__main__.py



def main():
    from discord.ext.commands import Bot
    import random
    import secrets
    import urllib.request
    import re

<<<<<<< HEAD

=======
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
>>>>>>> b0b441093059e636aad1d9ca942bb640f2eba191
    bot = Bot(command_prefix='!')


    #print bot info when it boots up
    @bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')

    #Confirm that bot is connected to server    
    @bot.event
    async def on_connect():
        print("--Connected to server--")

    #Coin Flip function
    @bot.command(pass_context=True)
    async def encourage(ctx):
        rand = random.choice([0,1])
        if rand == 0:
            await ctx.channel.send('Heads!')
        elif rand == 1:
            await ctx.channel.send('Tails!')

<<<<<<< HEAD
    # print message back
    @bot.command()
=======
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
            for text_channel in ctx.guild.text_channels:
                if text_channel.name == group_name:
                    await ctx.send('Sorry, that study group name already exists!')
                    return
                
            # Create study group category if it doesn't exist'
            study_category = None
            for category in ctx.guild.categories:
                if category.name == 'study-groups':
                    study_category = category
            if study_category is None:
                study_category = await ctx.guild.create_category('study-groups')
                    
            # Create new channel
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
            
            
        # Command to delete a study group text and voice channel.
        # Requires that the author already has read permissions for the channel.
        elif args[0] == 'delete': 
            channel_name = args[1].lower()
            text_channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
            # Check if text_channel exists
            if text_channel is None:
                await ctx.send('Sorry, that study group doesn\'t exist!')
                return
            overwrite = text_channel.overwrites_for(ctx.author)
            if overwrite.read_messages == False:
                await ctx.send('Sorry, you don\'t have permissions to delete this study group')
                return
            await text_channel.delete()
            
            voice_channel = discord.utils.get(ctx.guild.voice_channels, name=channel_name)
            await voice_channel.delete()
            
            
        # Add a new user to the study group.
        elif args[0] == 'add':
            channel_name = args[1].lower()
            
            text_channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
            voice_channel = discord.utils.get(ctx.guild.voice_channels, name=channel_name)
            if text_channel is None or voice_channel is None:
                await ctx.send('Sorry, that study group doesn\'t exist!')
                return
            
            overwrite = text_channel.overwrites_for(ctx.author)
            if overwrite.read_messages == False:
                await ctx.send('Sorry, you don\'t have permissions to add a new member to this study group')
                return
            # Give permissions for all mentioned members.
            for member in ctx.message.mentions:
                await text_channel.set_permissions(member, read_messages=True)
                await voice_channel.set_permissions(member, read_messages=True)
            
                
                


            
            
            
            
            
            
    # Print the message back.
    @bot.command(pass_context=True)
>>>>>>> b0b441093059e636aad1d9ca942bb640f2eba191
    async def repeat(ctx, *, arg):
        await ctx.send(arg)


       #Coin Flip function
    @bot.command(pass_context=True)
    async def coinflip(ctx):
        rand = random.choice([0,1])
        if rand == 0:
            await ctx.channel.send('Heads!')
        elif rand == 1:
            await ctx.channel.send('Tails!')

    @bot.command(pass_context=True)
    async def search(ctx, *, arg):
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query={}".format(arg))
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        await ctx.channel.send("https://www.youtube.com/watch?v=" + video_ids[0])    

    #Run bot
    bot.run(secrets.secretToken)

if __name__ == '__main__':
  main()