import os
import requests
import discord
import asyncio
from discord.ext import commands

class welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.channels, name='welcome🔥')
        await asyncio.sleep(2)
        if channel is not None:
            await channel.send(
                f"Welcome {member.mention} to Indian Students Association's "
                f"official discord server!\n"
                f"Don't forget to check {(discord.utils.get(member.guild.channels, name='rules📃')).mention}"
                f"and {(discord.utils.get(member.guild.channels, name='faq')).mention}"
            )


def setup(bot):
    bot.add_cog(welcome(bot))