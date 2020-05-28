import os
import re
import requests
import datetime
import random
import discord
from discord.ext import commands
from typing import Optional
from utils.global_utils import send_embedded
from utils import colors


class about(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await send_embedded(ctx, f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def info(self, ctx, args: str = None):
        if str != "short":
            embed = discord.Embed(
                title="ISA_bot",
                color=0xA8000D,
                description="I'm a member of ISA family ❤️",
                timestamp=datetime.datetime.utcnow(),
            )
            embed.add_field(name="Command prefix", value="`!!`, `isa!`, `i!` or `@mention`")
            embed.add_field(
                name="\ud83c\udfa5Quick examples:", value="[Simple commands](https://i.imgur.com/BqgJZuQ.gif)"
            )
            embed.set_image(url="https://i.imgur.com/rO9MzrP.jpg")
            embed.add_field(
                name="\ud83d\udd17 Bot source code", value="[Github Link](https://github.com/vinaydawani/ISA-bot)"
            )
            embed.set_footer(text="Made by @External72#5255")
            await ctx.send(embed=embed)
        else:
            await send_embedded(ctx, "[Github Link](https://github.com/vinaydawani/ISA-bot)")

        await ctx.message.delete(delay=5)


def setup(bot):
    bot.add_cog(about(bot))
