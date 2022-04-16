import config
import os, sys, discord
from discord.ext import commands


class Help(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, context):
        """
        List commands
        """
        prefix = config.BOT_PREFIXES
        if not isinstance(prefix, str):
            prefix = prefix[0]
        embed = discord.Embed(title="Help", description="List of available commands:", color=config.success)
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            cmds = cog.get_commands()
            command_list = [cmds.name for cmds in cmds]
            command_description = [cmds.help for cmds in cmds]
            help_text = '\n'.join(f'{prefix}{n} - {h}' for n, h in zip(command_list, command_description))
            embed.add_field(name=i.capitalize(), value=f'```{help_text}```', inline=False)
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
