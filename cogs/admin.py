import os
import requests
import asyncio
import datetime
import discord
from discord.ext import commands

class admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(admin(bot))
