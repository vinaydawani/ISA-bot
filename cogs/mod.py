import os
import requests
import asyncio
import datetime
import copy
import random
from typing import Optional
import discord
from discord.ext import commands
from utils import colors, checks


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
    async def ban(self, ctx, member: discord.Member = None, del: int = 0, *, reason=None):
        if member is None:
            await ctx.send("You probably haven't entered something correctly\n```!!kick <member> <reason>```")
        try:
            await ctx.guild.ban(member, reason=self.whats_the_reason(ctx, reason), delete_message_days=min(del, 7))
            await ctx.send(embed=self.make_embed(ctx, member, action='ban', custom=reason))
        except discord.HTTPException:
            await self.send_embedded(ctx, "Uh Ho! Something not quite right happened.")

    # TODO: fix unban command
    @commands.command()
    @checks.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            await ctx.send("You probably haven't entered something correctly\n```!!kick <member> <reason>```")
        try:
            await ctx.guild.unban(member, reason=self.whats_the_reason(ctx, reason))
            await ctx.send(embed=self.make_embed(ctx, member, action='ban', custom=reason))
        except discord.HTTPException:
            await self.send_embedded(ctx, "Uh Ho! Something not quite right happened.")

# TODO: mute, unmute, purge, presence

def setup(bot):
    bot.add_cog(mod(bot))
