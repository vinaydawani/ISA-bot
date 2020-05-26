import os
import requests
import discord
import asyncio
import random
import datetime
from discord.ext import commands


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Beep boop {self.bot.user.name} has connected to Discord!\n")
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="for commands starting with !!, isa! or i!",
            ),
        )

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     channel = discord.utils.get(member.guild.channels, name='welcome🔥')
    #     await asyncio.sleep(2)
    #     if channel is not None:
    #         await channel.send(
    #             f"Welcome {member.mention} to Indian Students Association's "
    #             f"official discord server!\n"
    #             f"Don't forget to check {(discord.utils.get(member.guild.channels, name='rules📃')).mention}"
    #             f"and {(discord.utils.get(member.guild.channels, name='faq')).mention}"
    #         )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="welcome🔥")
        des = (
            f"Welcome {member.mention} to Indian Students Association's "
            f"official discord server!\n"
            f"Don't forget to check {(discord.utils.get(member.guild.channels, name='rules📃')).mention}"
            f"and {(discord.utils.get(member.guild.channels, name='faq')).mention}"
        )
        if channel:
            embed = discord.Embed(
                description=des, color=random.choice(self.bot.color_list)
            )
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(events(bot))
