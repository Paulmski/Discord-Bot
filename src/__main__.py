# file app/__main__.py

def main():
    from discord.ext.commands import Bot
    import discord.utils
    import random
    import secrets


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
    async def coinflip(ctx):
        rand = random.choice([0,1])
        if rand == 0:
            await ctx.channel.send('Heads!')
        elif rand == 1:
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



    # print message back
    @bot.command()
    async def repeat(ctx, *, arg):
        await ctx.send(arg)

    #Run bot
    bot.run(secrets.secretToken)

    



if __name__ == '__main__':
  main()