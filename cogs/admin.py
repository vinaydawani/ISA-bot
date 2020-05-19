import os
import requests
import asyncio
import datetime
import copy
import random
from typing import Optional
import discord
from discord.ext import commands

class GlobalChannel(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            return await commands.TextChannelConverter().convert(ctx, argument)
        except commands.BadArgument:
            # Not found... so fall back to ID + global lookup
            try:
                channel_id = int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f'Could not find a channel by ID {argument!r}.')
            else:
                channel = ctx.bot.get_channel(channel_id)
                if channel is None:
                    raise commands.BadArgument(f'Could not find a channel by ID {argument!r}.')
                return

class admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def send_embedded(self, ctx, content):
        embed = discord.Embed(color=random.choice(self.bot.color_list), description=content)
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def loadcog(self, ctx, cog: str = None):
        if cog is None:
            await ctx.send("Please enter a cog to load it")
        else:
            msg = await ctx.send(f"Loading cog `{cog}`... :arrows_counterclockwise:")
            try:
                self.bot.load_extension(f"cogs.{cog}")
                await msg.edit(content="Cog loaded successfully! :white_check_mark:")
            except Exception as e:
                await msg.edit(content=f"**Error** {e.__class__.__name__} - {e}")

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unloadcog(self, ctx, cog: str = None):
        if cog is None:
            await ctx.send("Please enter a cog to unload it")
        else:
            msg = await ctx.send(f"Unloading cog `{cog}`... :arrows_counterclockwise:")
            try:
                self.bot.unload_extension(f"cogs.{cog}")
                await msg.edit(content="Cog unloaded successfully! :white_check_mark:")
            except Exception as e:
                await msg.edit(content=f"**Error** {e.__class__.__name__} - {e}")

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reloadcog(self, ctx, cog: str = None):
        if cog is None:
            await ctx.send("Please enter a cog to reload it")
        else:
            msg = await ctx.send(f"Reloading cog `{cog}`... :arrows_counterclockwise:")
            try:
                self.bot.reload_extension(f"cogs.{cog}")
                await msg.edit(content="Cog reloaded successfully! :white_check_mark:")
            except Exception as e:
                await msg.edit(content=f"**Error** {e.__class__.__name__} - {e}")

    @commands.command(hidden=True)
    async def extensions(self, ctx):
        """Lists the currently loaded extensions."""
        await self.send_embedded(ctx, '\n'.join(sorted([i for i in self.bot.extensions.keys()])))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def spam(selp, ctx, amount, *, content: str):
        await ctx.message.delete()
        for spam in range(int(amount)):
            await ctx.send(content)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def botsay(self, ctx, channel: Optional[GlobalChannel], embed: bool, *, stuff: str):
        msg = copy.copy(ctx.message)
        channel = channel or ctx.channel
        msg.channel = channel
        msg.content =  stuff
        new = await self.bot.get_context(msg, cls=type(ctx))
        if embed:
            await self.send_embedded(new, stuff)
        else:
            await new.send(stuff)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def sudo(self, ctx, channel: Optional[GlobalChannel], who: discord.User, *, command: str):
        msg = copy.copy(ctx.message)
        channel = channel or ctx.channel
        msg.channel = channel
        msg.author = channel.guild.get_member(who.id) or who
        msg.content = ctx.prefix + command
        new = await self.bot.get_context(msg, cls=type(ctx))
        await self.bot.invoke(new)

def setup(bot):
    bot.add_cog(admin(bot))
