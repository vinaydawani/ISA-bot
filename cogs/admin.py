import os
import requests
import asyncio
import datetime
import discord
from discord.ext import commands

class admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='load')
    @commands.is_owner()
    async def loadcog(self, ctx, cog: str):
        if cog is '':
            await ctx.send("Please enter a cog to load it")
        else:
            msg = await ctx.send(f"Loading cog `{cog}`... :arrows_counterclockwise:")
            try:
                self.bot.load_extension(f"cogs.{cog}")
                await msg.edit(content="Cog loaded successfully! :white_check_mark:")
            except Exception as e:
                await msg.edit(content=f"**Error** {e.__class__.__name__} - {e}")

    @commands.command(name='unload')
    @commands.is_owner()
    async def unloadcog(self, ctx, cog: str):
        if cog is '':
            await ctx.send("Please enter a cog to unload it")
        else:
            msg = await ctx.send(f"Unloading cog `{cog}`... :arrows_counterclockwise:")
            try:
                self.bot.unload_extension(f"cogs.{cog}")
                await msg.edit(content="Cog unloaded successfully! :white_check_mark:")
            except Exception as e:
                await msg.edit(content=f"**Error** {e.__class__.__name__} - {e}")

    @commands.command(name='reload')
    @commands.is_owner()
    async def reloadcog(self, ctx, cog: str):
        if cog is '':
            await ctx.send("Please enter a cog to reload it")
        else:
            msg = await ctx.send(f"Reloading cog `{cog}`... :arrows_counterclockwise:")
            try:
                self.bot.reload_extension(f"cogs.{cog}")
                await msg.edit(content="Cog reloaded successfully! :white_check_mark:")
            except Exception as e:
                await msg.edit(content=f"**Error** {e.__class__.__name__} - {e}")


def setup(bot):
    bot.add_cog(admin(bot))
