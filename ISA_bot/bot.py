__version__ = "1.2.0"
__author__ = "vinay dawani"

import os
import discord
import asyncio
import requests
import yaml
from discord.ext import commands
from dotenv import load_dotenv
from utils.colors import colors

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
ID = os.getenv("CLIENT_ID")
SECRET = os.getenv("SECRET")

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("isa!", "i!", "!!"),
    description="I'm here to just help keep things running smoothly",
)

with open("config.yaml") as x:
    bot.config = yaml.safe_load(x)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and not filename.startswith("_"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.color_list = [c for c in colors.values()]
bot.version = __version__

# TODO: make a separate file for isa related queries
@bot.command(name="events")
async def events(ctx):
    response = "We don't have any upcoming events right now.\nCheck back later! \U0001F6A8"
    await ctx.send(response)


bot.run(TOKEN)
