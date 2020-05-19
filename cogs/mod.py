import os
import requests
import asyncio
import datetime
import copy
import random
from typing import Optional
import discord
from discord.ext import commands

class mod(commands.Cog):
    pass

def setup(bot):
    bot.add_cog(mod(bot))
