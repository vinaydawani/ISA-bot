import requests
import asyncio
import discord
from datetime import datetime
import random
from discord.ext import commands
from bs4 import BeautifulSoup
from utils import colors
from utils.global_utils import send_embedded


class COD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.group(name="warzone", case_insensitive=True, invoke_without_command=True)
    @commands.cooldown(3, 10, commands.BucketType.member)
    async def warzone(self, ctx):
        await ctx.send_help(ctx.command)

    async def get_stats(self, ctx, URL, game_tag):
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        warzone_stats = soup.find("div", class_="segment-stats")

        if warzone_stats is None:
            await send_embedded(ctx, "No data available for this username.\nPlease enter a valid username!")
            return

        titles = warzone_stats.find_all("span", class_="name")
        values = warzone_stats.find_all("span", class_="value")

        title_list = [_.text for _ in titles]
        value_list = [_.text for _ in values]

        stats = {k: v for (k, v) in zip(title_list, value_list)}

        clean_stats = {
            _: stats[_]
            for _ in ("Wins", "Top 5", "Top 10", "K/D Ratio", "Damage/game", "Win %", "Kills", "Deaths", "Downs",)
        }

        await self.make_embed(ctx, clean_stats, URL, game_tag)

    async def make_embed(self, ctx, clean_stats, URL, game_tag):
        description = f"Call of Duty: Warzone statistics as requested by {ctx.author.mention}"
        # img = "https://profile.callofduty.com/resources/cod/images/shared-logo.jpg"
        img = "https://i.pinimg.com/originals/af/3f/1c/af3f1c8d937fe7d65d03cb897ace169e.jpg"

        embed = discord.Embed(description=description, color=discord.Colour(0xA8000D), timestamp=datetime.utcnow(),)
        embed.set_author(name=game_tag, icon_url=img, url=URL)
        # embed.add_field(name=list(stats.keys())[0], value=stats["Wins"])
        for (name, val) in clean_stats.items():
            embed.add_field(name=name, value=val)
        embed.set_footer(text="Data from cod.tracker.gg")

        await ctx.send(embed=embed)

    @warzone.command(name="battle")
    async def _battle(self, ctx, game_tag: str):
        tag, identifier = game_tag.split("#")
        URL = f"https://cod.tracker.gg/warzone/profile/battlenet/{tag}%23{identifier}/overview"
        await self.get_stats(ctx, URL, game_tag)

    @warzone.command(name="psn")
    async def _psn(self, ctx, game_tag: str):
        URL = f"https://cod.tracker.gg/warzone/profile/psn/{game_tag}/overview"
        await self.get_stats(ctx, URL, game_tag)

    @warzone.command(name="activision")
    async def _activision(self, ctx, *, game_tag: str):
        game_tag = game_tag.translate(str.maketrans({" ": "%20", "#": "%23"}))
        URL = f"https://cod.tracker.gg/warzone/profile/atvi/{game_tag}/overview"
        await self.get_stats(ctx, URL, game_tag)

    @warzone.command(name="xbox")
    async def _xbox(self, ctx, *, game_tag: str):
        game_tag = game_tag.translate(str.maketrans({" ": "%20"}))
        URL = f"https://cod.tracker.gg/warzone/profile/xbl/{game_tag}/overview"
        await self.get_stats(ctx, URL, game_tag)

    @_battle.error
    @_psn.error
    @_activision.error
    @_xbox.error
    async def _error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await send_embedded(ctx, "The game tag is missing!")
        elif isinstance(error, commands.BadArgument):
            await send_embedded(ctx, "The game tag is missing!")


def setup(bot):
    bot.add_cog(COD(bot))
