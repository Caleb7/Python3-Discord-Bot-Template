# Imports
import config, secrets
import discord, asyncio, os, platform, requests, sys, logging
from datetime import datetime
from discord.ext.commands import Bot
from discord.ext import commands

# This is set to True when bot is finished initializing
BOT_READY = False

# Declare intents
intents = discord.Intents.default()
intents.members = True

# Get bot handle
bot = Bot(command_prefix=config.BOT_PREFIXES)

# Remove help command, we have our own as a cog
bot.remove_command("help")

# Load cogs
for file in os.listdir("./Cogs/"):
	if file.endswith(".py"):
		cog = file[:-3]
		try:
			bot.load_extension(f"Cogs.{cog}")
			logging.info(f"Loaded cog '{cog}'")
		except Exception as e:
			cog = f"{type(e).__name__}: {e}"
			logging.error(f"Failed to load cog {cog}")


# On ready event
@bot.event
async def on_ready():
	global BOT_READY
	BOT_READY = True
	logging.info('Bot is Ready')


# On message event
@bot.event
async def on_message(message):
	if BOT_READY:
		# Ignore self
		if message.author == bot.user:
			logging.info(f'Ignored message, reason: Message origin is self')
			return
		# Ignore other bots
		if message.author == message.author.bot:
			logging.info(f'Ignored message, reason: Message origin is a bot')
			return
		# Dispatch messages to be handled via cogs
		await bot.process_commands(message)


# On command complete event, for logging
@bot.event
async def on_command_completion(ctx):
	if BOT_READY:
		full_command_name = ctx.command.qualified_name
		split = full_command_name.split(" ")
		executed_command = str(split[0])
		logging.info(f"Executed '{executed_command}' by {ctx.message.author} (ID: {ctx.message.author.id}) Raw: {ctx.message.content}")

# Run bot
bot.run(secrets.BOT_TOKEN)
