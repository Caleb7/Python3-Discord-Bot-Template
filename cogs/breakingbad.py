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

        if len(args) == 1:
            if args[0] == "death":
                url = "https://www.breakingbadapi.com/api/random-death"
                response = requests.get(url)
                data = response.json()
                death = data['death']
                death_cause = data['cause']
                death_responsible = data['responsible']
                death_last_words = data['last_words']
                death_nickname = data['nickname']
                death_img = data['img']
                # Send embed
                embed = discord.Embed(title=f"{death}", description=f"Death Cause: {death_cause}", color=0x00ff00)
                embed.add_field(name="Nickname", value=f"{death_nickname}", inline=False)
                embed.add_field(name="Responsible", value=f"{death_responsible}", inline=False)
                embed.add_field(name="Last Words", value=f"{death_last_words}", inline=False)
                embed.set_image(url=f"{death_img}")
                await context.send(embed=embed)
                

                


def setup(bot):
    bot.add_cog(BreakingBad(bot))
