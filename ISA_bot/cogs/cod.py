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

    async def get_stats(self, ctx, URL):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        warzone_stats = soup.find("div", class_="segment-stats")

        titles = warzone_stats.find_all("span", class_="name")
        values = warzone_stats.find_all("span", class_="value")

        title_list = [_.text for _ in titles]
        value_list = [_.text for _ in values]

        stats = {k: v for (k, v) in zip(title_list, value_list)}

        await ctx.send(stats)

    async def make_embed(self, ctx, stats):
        pass

    @warzone.command(name="battle")
    async def _battle(self, ctx, game_tag: str):
        tag, identifier = game_tag.split("#")
        URL = f"https://cod.tracker.gg/warzone/profile/battlenet/{tag}%23{identifier}/overview"
        await self.get_stats(ctx, URL)

    @warzone.command(name="psn")
    async def _psn(self, ctx, game_tag: str):
        URL = f"https://cod.tracker.gg/warzone/profile/psn/{game_tag}/overview"
        await self.get_stats(ctx, URL)

    @warzone.command(name="activision")
    async def _activision(self, ctx, *, game_tag: str):
        game_tag = game_tag.translate(str.maketrans({" ": "%20", "#": "%23"}))
        URL = f"https://cod.tracker.gg/warzone/profile/atvi/{game_tag}/overview"
        await self.get_stats(ctx, URL)

    @warzone.command(name="xbox")
    async def _xbox(self, ctx, *, game_tag: str):
        game_tag = game_tag.translate(str.maketrans({" ": "%20"}))
        URL = f"https://cod.tracker.gg/warzone/profile/xbl/{game_tag}/overview"
        await self.get_stats(ctx, URL)


def setup(bot):
    bot.add_cog(COD(bot))
