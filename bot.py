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

# TODO: make a separate file for isa related queries
@bot.command(name="events")
async def events(ctx):
	response = (
		"We don't have any upcoming events right now.\nCheck back later! \U0001F6A8"
	)
	await ctx.send(response)


# TODO: make a help cog with help and info functions
@bot.command()
async def info(ctx):
	embed = discord.Embed(
		title="ISA Bot", description="A member of ISA family :heart:", color=0xA8000D
	)

	# give info about you here
	embed.add_field(name="Creator", value="@External72")

	await ctx.send(embed=embed)


bot.run(TOKEN)
