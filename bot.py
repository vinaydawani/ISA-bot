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
bot.load_extension('cogs.events')
# bot.load_extension('cogs.Stats')

bot.colors = {
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_NAVY': 0x2C3E50
}
bot.color_list = [c for c in bot.colors.values()]

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
