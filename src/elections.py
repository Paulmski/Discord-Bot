from discord.ext import tasks, commands
import discord

class ElectionSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def start_vote(action):
        # TODO: Add voting embed here with reaction listener.
        pass

    def end_voting(did_vote_succeed):
        # TODO: Delete previous vote and forward the results to the appropriate function.
        pass
