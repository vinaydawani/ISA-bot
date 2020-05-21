import os
import requests
import asyncio
import datetime
import copy
import random
from collections import Counter
from typing import Optional, Union
import discord
from discord.ext import commands
from utils import colors, checks, converters, errors
from utils.global_functions import confirm_prompt

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
        elif isinstance(error, commands.MissingPermissions):
            return await self.send_embedded(ctx, "You don't have the permission to pull this one off broh!!")

    @commands.command()
    @commands.guild_only()
    @checks.has_permissions(ban_members = True)
    async def lockdown(self, ctx, action):
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

# Purge commands --------------------------------------------------------------------------------------------
    async def to_purge(self, ctx, limit, check, *, before=None, after=None):
        if limit > 150:
            return await self.send_embedded(ctx, "limit of messages that can be deleted is 150!")

        try:
            purged = await ctx.channel.purge(limit=limit, before=ctx.message, check=check)
        except discord.Forbidden:
            return await ctx.send("I do not have permissions to carry out this command")
        except discord.HTTPException as e:
            return await ctx.send(f"**Error:** {e}")

        authors = Counter(str(msg.author) for msg in purged)
        purged = len(purged)
        desc = [f"Deleted {purged} message(s)"]

        if purged:
            desc.append('')
            spammers = sorted(authors.items(), key=lambda t: t[1], reverse=True)
            desc.extend(f'**{name}**: {count}' for name, count in spammers)

        embed = discord.Embed(color=random.choice(self.bot.color_list), description='\n'.join(desc))
        await ctx.send(embed=embed, delete_after=15)

    @commands.group(case_insensitive=True, invoke_without_command=False)
    @checks.is_mod()
    @checks.is_admin()
    @checks.has_permissions(manage_messages = True)
    async def purge(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await self.send_embedded(ctx, "An argument is missing!")
        elif isinstance(error, commands.MissingPermissions):
            return await self.send_embedded(ctx, "You don't have the permission to pull it off broh!!")

    @purge.command(name='user')
    async def _user(self, ctx, member: discord.Member, search: int = 10):
        await self.to_purge(ctx, search, lambda m: m.author == member)
        await ctx.message.add_reaction('\U00002705')

    @purge.command(name='all')
    async def _all(self, ctx, search: int = 20):
        if not await confirm_prompt(ctx, f"Delete {search} messages?"):
            return
        await self.to_purge(ctx, search, lambda m: True)
        await ctx.message.add_reaction('\U00002705')

    @purge.command(name='clean')
    @commands.is_owner()
    async def _clean(self, ctx, search: int = 500):
        if not await confirm_prompt(ctx, f"Delete **all** messages?"):
            return
        await self.to_purge(ctx, search, lambda m: True)
        await ctx.message.add_reaction('\U00002705')

    @purge.command(name='content')
    async def _equals(self, ctx, *, substr):
        await self.to_purge(ctx, 50, lambda m: m.content == substr)
        await ctx.message.add_reaction('\U00002705')

    @purge.command(name='contains')
    async def _contains(self, ctx, *, substr):
        await self.to_purge(ctx, 50, lambda m: substr in m.content)
        await ctx.message.add_reaction('\U00002705')

### Purge commans end ------------------------------------------------------------------------------------

# TODO: mute, unmute, presence

def setup(bot):
    bot.add_cog(mod(bot))
