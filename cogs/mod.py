import os
import requests
import asyncio
import datetime
import copy
import random
from typing import Optional, Union
import discord
from discord.ext import commands
from utils import colors, checks, converters, errors


class mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    def whats_the_reason(self, ctx, reason: str):
        if reason:
            res = f'{ctx.author.mention}: {reason}'
        else:
            res = f'Action done by {ctx.author.mention} (ID: {ctx.author.id})'

        if len(res) > 500:
            raise commands.BadArgument("Reason too long bro!")
        return res

    async def send_embedded(self, ctx, content):
        embed = discord.Embed(color=random.choice(self.bot.color_list), description=content)
        await ctx.send(embed=embed)

    def make_embed(self, ctx, member, action, custom=None):
        desc = {
            'ban': 'has been banned',
            'kick': 'has been kicked',
            'soft': 'has been soft banned',
            'mute': 'has been muted',
            'unban': 'has been unbanned'
        }
        what_happen = f'{member} {desc[action]}'

        embed = discord.Embed(
            color=random.choice(self.bot.color_list),
            title='',
        )
        if custom is None:
            embed.description = f'{what_happen}'
        else:
            embed.description = f'Reason: {custom}'
        embed.set_author(name=f"{member} {desc[action]}")
        if not desc[action] == 'has been unbanned':
            embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Action performed by {ctx.author}")
        return embed

    @commands.command()
    @checks.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            await ctx.send("You probably haven't entered something correctly\n```!!kick <member> <reason>```")
        try:
            await ctx.guild.kick(member, reason=self.whats_the_reason(ctx, reason))
            await ctx.send(embed=self.make_embed(ctx, member, action='kick', custom=reason))
        except discord.HTTPException:
            await self.send_embedded(ctx, "Uh Ho! Something not quite right happened.")

    @commands.command()
    @checks.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, deleted: Optional[int] = 0, *, reason=None):
        if member is None:
            await ctx.send("You probably haven't entered something correctly\n```!!kick <member> <reason>```")
        try:
            await ctx.guild.ban(member, reason=self.whats_the_reason(ctx, reason), delete_message_days=min(deleted, 7))
            await ctx.send(embed=self.make_embed(ctx, member, action='ban', custom=reason))
        except discord.HTTPException:
            await self.send_embedded(ctx, "Uh Ho! Something not quite right happened.")

    @commands.command()
    @checks.has_permissions(ban_members=True)
    async def unban(self, ctx, member: converters.BannedMember, *, reason=None):
        if member is None:
            await ctx.send("You probably haven't entered something correctly\n```!!kick <member> <reason>```")
        try:
            await ctx.guild.unban(member.user, reason=self.whats_the_reason(ctx, reason))
            await ctx.send(embed=self.make_embed(ctx, member, action='unban', custom=reason))
        except discord.HTTPException:
            await self.send_embedded(ctx, "Uh Ho! Something not quite right happened.")

    @commands.command()
    @checks.has_permissions(ban_members=True)
    @checks.has_permissions(kick_members=True)
    async def softban(self, ctx, member: converters.MemberID, *, reason=None):
        if member is None:
            await ctx.send("You probably haven't entered something correctly\n```!!kick <member> <reason>```")
        try:
            await ctx.guild.ban(member, reason=self.whats_the_reason(ctx, reason))
            await ctx.guild.unban(member, reason=self.whats_the_reason(ctx, reason))
            await ctx.send(embed=self.make_embed(ctx, member, action='soft', custom=reason))
        except discord.HTTPException:
            await self.send_embedded(ctx, "Uh Ho! Something not quite right happened.")

    @ban.error
    @unban.error
    @kick.error
    @softban.error
    async def _error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.send_embedded(ctx, "Please check the arguments as one of it might be wrong.")

# TODO: mute, unmute, purge, presence

    @commands.command()
    @commands.guild_only()
    @checks.has_permissions(ban_members = True)
    async def lockdown(self, ctx, action):
        """Prevents anyone from chatting in the current channel."""
        if action.lower() == 'on':
            msg = await ctx.send("Locking down the channel...")
            await ctx.channel.set_permissions(discord.utils.get(ctx.guild.roles, id=ctx.guild.id), send_messages=False)
            return await msg.edit(content="The channel has been successfully locked down. :lock: ")
        elif action.lower() == 'off':
            msg = await ctx.send("Unlocking the channel...")
            await ctx.channel.set_permissions(discord.utils.get(ctx.guild.roles, id=ctx.guild.id), send_messages=True)
            return await msg.edit(content="The channel has been successfully unlocked. :unlock: ")
        else:
            return await self.send_embedded(ctx, "Lockdown command:\n!!lockdown [on/off]")

def setup(bot):
    bot.add_cog(mod(bot))
