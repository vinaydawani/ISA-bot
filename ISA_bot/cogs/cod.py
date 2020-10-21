import requests
import asyncio
import discord
from discord.ext import commands
from bs4 import BeautifulSoup


class COD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.group(name="warzone", case_insensitive=True, invoke_without_command=True)
    @commands.cooldown(3, 10, commands.BucketType.member)
    async def warzone(self, ctx):
        await ctx.send_help(ctx.command)

    async def get_stats(self, ctx):
        pass

    @warzone.command(name="battle")
    async def _battle(self, ctx, game_tag: str):
        await ctx.send(game_tag)

    @warzone.command(name="psn")
    async def _psn(self, ctx, game_tag: str):
        pass

    @warzone.command(name="activision")
    async def _activision(self, ctx, game_tag: str):
        pass

    @warzone.command(name="xbox")
    async def _xbox(self, ctx, game_tag: str):
        pass


def setup(bot):
    bot.add_cog(COD(bot))
