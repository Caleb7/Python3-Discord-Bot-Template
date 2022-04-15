import config
import os, sys, discord, platform, subprocess
from discord.ext import commands
import requests


class BreakingBad(commands.Cog, name="breakingbad"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bb")
    async def bb(self, context, *args):
        """
        No length, print a random quote
        """
        #TODO: Add arguments to specify character
        if len(args) == 0:
            url = "https://www.breakingbadapi.com/api/quote/random"
            response = requests.get(url)
            data = response.json()
            quote = data[0]['quote']
            author = data[0]['author']
            await context.send(f'"{quote}" - {author}')


def setup(bot):
    bot.add_cog(BreakingBad(bot))
