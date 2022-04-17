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
        Get a random quote from Breaking Bad
        .bb death - Get a random death fact from Breaking Bad
        """
        #TODO: Add arguments to specify character for quote or death fact
        if len(args) == 0:
            url = "https://www.breakingbadapi.com/api/quote/random"
            response = requests.get(url)
            data = response.json()
            quote = data[0]['quote']
            author = data[0]['author']
            await context.send(f'"{quote}" - {author}')

        if len(args) == 1:
            # Random Death Fact
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
                embed = discord.Embed(title=f"{death}", description=f"{death_cause}", color=0x00ff00)
                embed.add_field(name="Nickname", value=f"{death_nickname}", inline=False)
                embed.add_field(name="Responsible", value=f"{death_responsible}", inline=False)
                embed.add_field(name="Last Words", value=f"{death_last_words}", inline=False)
                embed.set_image(url=f"{death_img}")
                await context.send(embed=embed)

    @commands.command(name="bb-characters")
    async def bb_characters(self, context, *args):
        """
        Get a list of all characters from Breaking Bad
        .bb-characters - Get a list of all characters from Breaking Bad
        """
        url = "https://www.breakingbadapi.com/api/characters"
        response = requests.get(url)
        data = response.json()
        characters = []
        for character in data:
            characters.append(character['name'])
        await context.send(f"{', '.join(characters)}")


def setup(bot):
    bot.add_cog(BreakingBad(bot))
