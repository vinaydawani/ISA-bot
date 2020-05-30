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
    """gets stats for coronavirus"""

    def __init__(self, bot):
        self.bot = bot

    confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    recovered_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

    confirmed_df = pd.read_csv(confirmed_url, error_bad_lines=False).dropna(axis=1, how="all")
    deaths_df = pd.read_csv(deaths_url, error_bad_lines=False).dropna(axis=1, how="all")
    recovered_df = pd.read_csv(recovered_url, error_bad_lines=False).dropna(axis=1, how="all")

    wom = "https://www.worldometers.info/coronavirus/"
    us_wom = "https://www.worldometers.info/coronavirus/country/us/"
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }  # Not necessary but useful

    r_wom = requests.get(wom, headers=header)
    r_us_wom = requests.get(us_wom, headers=header)

    r_wom_clean = r_wom.text
    r_wom_clean = r_wom_clean.replace(" !important;display:none;", "")

    df = pd.read_html(r_wom_clean)[0].replace(np.nan, 0).replace(",", "", regex=True)
    us_df = pd.read_html(r_us_wom.text)[0].replace(np.nan, 0).replace(",", "", regex=True)

    def get_loc(self, location, val):
        loc_df = self.df[self.df["Country,Other"].str.match(location, na=False)][val].values[0]
        return loc_df

    def get_total(self, val):
        all_df = self.df[self.df["Country,Other"].str.match("Total:", na=False)][val].values[0]
        return all_df

    @commands.command(name="covid", aliases=["coronavirus"])
    @commands.cooldown(2, 15, commands.BucketType.user)
    async def covid(self, ctx, location="ALL"):
        """retuns the stats of novel coronavirus cases given the country"""

        # Check and convert thhe name of location if necessary
        if len(location) == 2 or len(location) == 3:
            location = location.upper()
        else:
            location = location.title()

        if location in alpha2:
            location = alpha2[location]
        elif location in alpha3:
            location = alpha3[location]
        elif location in alt_names:
            location = alt_names[location]

        # Checking and parsing the Data
        if location == "ALL" or (location in alpha2.values()):

            if location == "ALL":
                conf = self.get_total("TotalCases")
                death = self.get_total("TotalDeaths")
                new_conf = self.get_total("NewCases")
                new_death = self.get_total("NewDeaths")
                active = self.get_total("ActiveCases")
                recovered = self.get_total("TotalRecovered")
                serious = self.get_total("Serious,Critical")

            else:
                conf = self.get_loc(location, "TotalCases")
                death = self.get_loc(location, "TotalDeaths")
                new_conf = self.get_loc(location, "NewCases")
                new_death = self.get_loc(location, "NewDeaths")
                active = self.get_loc(location, "ActiveCases")
                recovered = self.get_loc(location, "TotalRecovered")
                serious = self.get_loc(location, "Serious,Critical")

            name = f"Coronavirus Cases | {location}"
            img = "https://lh3.googleusercontent.com/proxy/MqV-IVThACM7kYgDDF8Zle_McVLAWctkCUpleMWRJzLypYjrKpgdu1Z_8H8nONFLdr7DVO3WPp-3iaPHwXvdjAo_De8Lwu1k66l3y5r-_xVSso9yw_UEesB8OG5txpA"

            description = f"Novel Coronavirus statistics in {location} as requested by {ctx.author.mention}"

            if int(new_conf) > 0:
                new_conf = f"(+{int(new_conf)})"
            elif new_conf == 0:
                new_conf = ""

            if int(new_death) > 0:
                new_death = f"(+{int(new_death)})"
            elif new_death == 0:
                new_death = ""

            if not conf == 0:
                mort = round((int(death) / int(conf) * 100), 2)
                rec = round((int(recovered) / int(conf) * 100), 2)

            embed = discord.Embed(
                description=description, color=discord.Colour.dark_red(), timestamp=datetime.utcnow(),
            )

            embed.set_author(
                name=name, icon_url=img, url="https://www.worldometers.info/coronavirus/",
            )
            embed.add_field(name="Confirmed", value=f"**{int(conf)}** {new_conf}")
            embed.add_field(name="Deaths", value=f"**{int(death)}** {new_death}")
            embed.add_field(name="Recovered", value=f"**{int(recovered)}**")
            embed.add_field(name="Active", value=f"**{int(active)}**")
            embed.add_field(name="Critical", value=f"**{int(serious)}**")
            embed.add_field(name="Recovery Rate", value=f"**{rec}**")
            embed.add_field(name="Mortality Rate", value=f"**{mort}**")
            embed.set_footer(text="Data from Worldometer")

            await ctx.send(embed=embed)

        else:
            await ctx.send("There is no available data for this location | Use **!!help** for more info on commands")


def setup(bot):
    bot.add_cog(covid(bot))
