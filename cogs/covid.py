import os
import requests
import discord
import asyncio
from discord.ext import commands

class covid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def getCovidInfo(self, country):
        response = requests.get("https://api.covid19api.com/summary")

        if response.status_code == 200:
            countries = response.json()["Countries"]
            country = country
            for data in countries:
                if data["Country"].lower() == country.lower():
                    totalConfirmed = data["TotalConfirmed"]
                    totalDeath = data["TotalDeaths"]
                    return {"totalConfirmed": totalConfirmed, "totalDeath": totalDeath}
        else:
            return

    async def send_embedded(self, ctx, content):
        embed = discord.Embed(color=0x00ff00, description=content)
        await ctx.send(embed=embed)

    @commands.command(name='covid')
    async def display_covid(self, ctx, *country):
        name = " ".join(country)
        try:
            info = self.getCovidInfo(name)
            tC = info["totalConfirmed"]
            tD = info["totalDeath"]
            await self.send_embedded(ctx, f"-{name}- \n  Total Case: {tC} \n  Total Death: {tD}")
        except:
            await self.send_embedded(ctx, "You did not specify a country (!covid india)")

def setup(bot):
    bot.add_cog(covid(bot))
