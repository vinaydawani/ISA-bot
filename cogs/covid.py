import os
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import discord
import asyncio
from datetime import datetime
from discord.ext import commands
from utils.codes import states, alt_names, alpha2, alpha3, JHU_names

class covid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    confirmed_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    deaths_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    recovered_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'


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
