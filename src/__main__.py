# file app/__main__.py

def main():
    import datetime
    import requests
    import math
    from discord.ext.commands import Bot
    import time
    import json
    import random


    bot = Bot(command_prefix='!')





    @bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')


                    
    @bot.command(pass_context=True)
    async def coinflip(ctx):
        rand = random.choice([0,1])
        print(rand)
        if rand == 0:
            await ctx.channel.send('Heads!')
        elif rand == 1:
            await ctx.channel.send('Tails!')
    



if __name__ == '__main__':
  main()