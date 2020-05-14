import os
import discord
import asyncio
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ID = os.getenv('CLIENT_ID')
SECRET = os.getenv('SECRET')

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('isa!', 'i!', '!!'),
    description='I\'m here to just help keep things running smoothly'
)

bot.load_extension('cogs.covid')
bot.load_extension('cogs.welcome')
bot.load_extension('cogs.Stats')

@bot.event
async def on_ready():
    print(f"Beep boop {bot.user.name} has connected to Discord!\n")


@bot.command(name='events')
async def events(ctx):
    response = 'We don\'t have any upcoming events right now.\nCheck back later! \U0001F6A8'
    await ctx.send(response)


@bot.command()
async def info(ctx):
    embed = discord.Embed(title="ISA Bot", description="A member of ISA family :heart:", color=0xa8000d)

    # give info about you here
    embed.add_field(name="Creator", value="@External72")

    await ctx.send(embed=embed)

bot.run(TOKEN)
