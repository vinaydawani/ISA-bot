import os
import requests
import asyncio
import datetime
import copy
from typing import Optional
import discord
from discord.ext import commands

class admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='load')
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

    @commands.command(name='unload')
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

    @commands.command(name='reload')
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

    @commands.command(alias='say', hidden=True)
    @commands.is_owner()
    async def spam(selp, ctx, amount, *, content: str):
        await ctx.message.delete()
        for spam in range(int(amount)):
            await ctx.send(content)

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


'''
    async def say_permissions(self, ctx, member, channel):
		permissions = channel.permissions_for(member)
		e = discord.Embed(colour=member.colour)
		avatar = member.avatar_url_as(static_format='png')
		e.set_author(name=str(member), url=avatar)
		allowed, denied = [], []
		for name, value in permissions:
			name = name.replace('_', ' ').replace('guild', 'server').title()
			if value:
				allowed.append(name)
			else:
				denied.append(name)

		e.add_field(name='Allowed', value='\n'.join(allowed))
		e.add_field(name='Denied', value='\n'.join(denied))
		await ctx.send(embed=e)

	@commands.command()
	@commands.guild_only()
	@commands.is_owner()
	async def permissions(self, ctx, member: discord.Member = None, channel: discord.TextChannel = None):
		"""Shows a member's permissions in a specific channel.

		If no channel is given then it uses the current one.

		You cannot use this in private messages. If no member is given then
		the info returned will be yours.
		"""
		channel = channel or ctx.channel
		if member is None:
			member = ctx.author

		await self.say_permissions(ctx, member, channel)
'''

def setup(bot):
    bot.add_cog(admin(bot))
