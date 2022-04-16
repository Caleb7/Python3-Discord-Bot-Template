import config
import os, sys, discord, platform, subprocess
from discord.ext import commands


class Common(commands.Cog, name="common"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, context, *args):
        """
        0 args - Bot ping, 1 arg - ip or hostname
        """
        if len(args) == 0:
            ms = round(self.bot.latency*1000)
            await context.send(f'{ms}ms')
        
        if len(args) == 1:
            operating_system = platform.system().lower()
            modif = '-n' if operating_system == 'windows' else '-c'
            result = subprocess.check_output(['ping', modif, '1', args[0]])
            await context.send(f'{args[0]} - {result}')


def setup(bot):
    bot.add_cog(Common(bot))
