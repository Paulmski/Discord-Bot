# file app/__main__.py

def main():
    from discord.ext.commands import Bot
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

    # print message back
    @bot.command()
    async def repeat(ctx, *, arg):
        await ctx.send(arg)

    #Run bot
    bot.run(secrets.secretToken)

    



if __name__ == '__main__':
  main()