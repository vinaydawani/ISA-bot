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
from utils.global_utils import confirm_prompt, send_embedded


class mod(commands.Cog):
    """ commands for the mods 👀"""

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    def whats_the_reason(self, ctx, reason: str):
        if reason:
            res = f"{ctx.author.mention}: {reason}"
        else:
            res = f"Action done by {ctx.author.mention} (ID: {ctx.author.id})"

        if len(res) > 500:
            raise commands.BadArgument("Reason too long bro!")
        return res

    def make_embed(self, ctx, member, action, custom=None):
        desc = {
            "ban": "has been banned",
            "kick": "has been kicked",
            "soft": "has been soft banned",
            "mute": "has been muted",
            "unban": "has been unbanned",
        }
        what_happen = f"{member} {desc[action]}"

        embed = discord.Embed(color=random.choice(self.bot.color_list), title="",)
        if custom is None:
            embed.description = f"{what_happen}"
        else:
            embed.description = f"Reason: {custom}"
        embed.set_author(name=f"{member} {desc[action]}")
        if not desc[action] == "has been unbanned":
            embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Action performed by {ctx.author}")
        return embed

    @commands.command()
    @checks.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        """kicks a user"""
        if member is None:
            await ctx.send("You probably haven't entered something correctly\n```!!kick <member> <reason>```")
        try:
            await ctx.guild.kick(member, reason=self.whats_the_reason(ctx, reason))
            await ctx.send(embed=self.make_embed(ctx, member, action="kick", custom=reason))
        except discord.HTTPException:
            await send_embedded(ctx, "Uh Ho! Something not quite right happened.")

    @commands.command()
    @checks.has_permissions(ban_members=True)
    async def ban(
        self, ctx, member: discord.Member = None, deleted: Optional[int] = 0, *, reason=None,
    ):
        """bans an user"""
        if member is None:
            await ctx.send("You probably haven't entered something correctly\n```!!kick <member> <reason>```")
        try:
            await ctx.guild.ban(
                member, reason=self.whats_the_reason(ctx, reason), delete_message_days=min(deleted, 7),
            )
            await ctx.send(embed=self.make_embed(ctx, member, action="ban", custom=reason))
        except discord.HTTPException:
            await send_embedded(ctx, "Uh Ho! Something not quite right happened.")

    @commands.command()
    @checks.has_permissions(ban_members=True)
    async def unban(self, ctx, member: converters.BannedMember, *, reason=None):
        """unban an user"""
        if member is None:
            await ctx.send("You probably haven't entered something correctly\n```!!kick <member> <reason>```")
        try:
            await ctx.guild.unban(member.user, reason=self.whats_the_reason(ctx, reason))
            await ctx.send(embed=self.make_embed(ctx, member, action="unban", custom=reason))
        except discord.HTTPException:
            await send_embedded(ctx, "Uh Ho! Something not quite right happened.")

    @commands.command()
    @checks.has_permissions(ban_members=True)
    @checks.has_permissions(kick_members=True)
    async def softban(self, ctx, member: converters.MemberID, *, reason=None):
        """softbans an user"""
        if member is None:
            await ctx.send("You probably haven't entered something correctly\n```!!kick <member> <reason>```")
        try:
            await ctx.guild.ban(member, reason=self.whats_the_reason(ctx, reason))
            await ctx.guild.unban(member, reason=self.whats_the_reason(ctx, reason))
            await ctx.send(embed=self.make_embed(ctx, member, action="soft", custom=reason))
        except discord.HTTPException:
            await send_embedded(ctx, "Uh Ho! Something not quite right happened.")

    @ban.error
    @unban.error
    @kick.error
    @softban.error
    async def _error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await send_embedded(ctx, "Please check the arguments as one of it might be wrong.")
        elif isinstance(error, commands.MissingPermissions):
            return await send_embedded(ctx, "You don't have the permission to pull this one off broh!!")

    @commands.command()
    @checks.has_permissions(manage_emojis=True)
    async def react(self, ctx, emoji, messageID: int):
        msg = await ctx.fetch_message(messageID)
        await msg.add_reaction(emoji)
        await ctx.message.delete(delay=5)

    @react.error
    async def react_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            return await send_embedded(ctx, "Can't do that!")

    @commands.command()
    @commands.guild_only()
    @checks.has_permissions(ban_members=True)
    async def lockdown(self, ctx, action):
        """LOCKDOWN"""
        if action.lower() == "on":
            msg = await ctx.send("Locking down the channel...")
            await ctx.channel.set_permissions(discord.utils.get(ctx.guild.roles, id=ctx.guild.id), send_messages=False)
            return await msg.edit(content="The channel has been successfully locked down. :lock: ")
        elif action.lower() == "off":
            msg = await ctx.send("Unlocking the channel...")
            await ctx.channel.set_permissions(discord.utils.get(ctx.guild.roles, id=ctx.guild.id), send_messages=True)
            return await msg.edit(content="The channel has been successfully unlocked. :unlock: ")
        else:
            return await send_embedded(ctx, "Lockdown command:\n!!lockdown [on/off]")

    @lockdown.error
    async def lockdown_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await send_embedded(ctx, "Please check the arguments as one of it might be wrong.")
        elif isinstance(error, commands.MissingPermissions):
            return await send_embedded(ctx, "You don't have the permission to pull this one off broh!!")

    # Purge commands --------------------------------------------------------------------------------------------
    async def to_purge(self, ctx, limit, check, *, before=None, after=None):
        if limit > 150:
            return await send_embedded(ctx, "limit of messages that can be deleted is 150!")

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
            desc.append("")
            spammers = sorted(authors.items(), key=lambda t: t[1], reverse=True)
            desc.extend(f"**{name}**: {count}" for name, count in spammers)

        embed = discord.Embed(color=random.choice(self.bot.color_list), description="\n".join(desc))
        await ctx.send(embed=embed, delete_after=15)

    @commands.group(case_insensitive=True, invoke_without_command=False)
    @checks.is_mod()
    @checks.is_admin()
    @checks.has_permissions(manage_messages=True)
    async def purge(self, ctx):
        """purges messages on the basis of subcommands"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await send_embedded(ctx, "An argument is missing!")
        elif isinstance(error, commands.MissingPermissions):
            return await send_embedded(ctx, "You don't have the permission to pull it off broh!!")

    @purge.command(name="user")
    async def _user(self, ctx, member: discord.Member, search: int = 10):
        """purge message by certain user"""
        await self.to_purge(ctx, search, lambda m: m.author == member)
        await ctx.message.add_reaction("\U00002705")

    @purge.command(name="all")
    async def _all(self, ctx, search: int = 20):
        """deletes given ammount of messages"""
        if not await confirm_prompt(ctx, f"Delete {search} messages?"):
            return
        await self.to_purge(ctx, search, lambda m: True)
        await ctx.message.add_reaction("\U00002705")

    @purge.command(name="clean")
    @commands.is_owner()
    async def _clean(self, ctx, search: int = 149):
        """deletes last 150 messages"""
        if not await confirm_prompt(ctx, f"Delete **all** messages?"):
            return
        await self.to_purge(ctx, search, lambda m: True)
        await ctx.message.add_reaction("\U00002705")

    @purge.command(name="content")
    async def _equals(self, ctx, *, substr):
        """deletes messages equal to a given string"""
        await self.to_purge(ctx, 50, lambda m: m.content == substr)
        await ctx.message.add_reaction("\U00002705")

    @purge.command(name="contains")
    async def _contains(self, ctx, *, substr):
        """deletes message with a specific string in it"""
        await self.to_purge(ctx, 50, lambda m: substr in m.content)
        await ctx.message.add_reaction("\U00002705")

    ### Purge commans end ------------------------------------------------------------------------------------

    @commands.command()
    @checks.has_permissions(administrator=True)
    async def dm(self, ctx, member: discord.Member, *, msg: str):
        try:
            await member.send(msg)
            await ctx.message.delete()
            await send_embedded(ctx, f"DM to {member} has been sent!")
        except commands.MissingPermissions:
            await send_embedded(ctx, f"You dont have the permissions mah dude!")

    ### Presence tools -------------------------------------

    @commands.group(name="presence", invoke_without_command=True, case_insensitive=True)
    @checks.is_admin()
    async def change_presence(self, ctx):
        """change rich presence of the bot"""
        await ctx.send_help(ctx.command)

    @change_presence.command(aliases=["l"])
    async def listen(self, ctx, *, name):
        if ctx.guild is None:
            botmember = self.bot.guilds[0].me
        else:
            botmember = ctx.me
        status = botmember.status
        await self.bot.change_presence(
            activity=discord.Activity(name=name, type=discord.ActivityType.listening), status=status,
        )
        await ctx.message.add_reaction("\u2705")
        await ctx.message.delete(delay=15.0)

    @change_presence.command(aliases=["p"])
    async def playing(self, ctx, *, name):
        if ctx.guild is None:
            botmember = self.bot.guilds[0].me
        else:
            botmember = ctx.me
        status = botmember.status
        await self.bot.change_presence(activity=discord.Game(name=name), status=status)
        await ctx.message.add_reaction("\u2705")
        await ctx.message.delete(delay=15.0)

    @change_presence.command(aliases=["s"])
    async def streaming(self, ctx, name, url=None):
        if ctx.guild is None:
            botmember = self.bot.guilds[0].me
        else:
            botmember = ctx.me
        status = botmember.status
        # url = url or 'https://www.twitch.tv/directory'
        if name and (url == None):
            url = f"https://www.twitch.tv/{name}"
        await self.bot.change_presence(
            activity=discord.Streaming(name=name, url=url, twitch_name=name), status=status,
        )
        await ctx.message.add_reaction("\u2705")
        await ctx.message.delete(delay=15.0)

    @change_presence.command(aliases=["w"])
    async def watching(self, ctx, *, name):
        if ctx.guild is None:
            botmember = self.bot.guilds[0].me
        else:
            botmember = ctx.me
        status = botmember.status
        await self.bot.change_presence(
            activity=discord.Activity(name=name, type=discord.ActivityType.watching), status=status,
        )
        await ctx.message.add_reaction("\u2705")
        await ctx.message.delete(delay=15.0)

    @change_presence.command()
    async def status(self, ctx, status):
        """change status of the bot"""
        stata = {
            "online": discord.Status.online,
            "offline": discord.Status.invisible,
            "invis": discord.Status.invisible,
            "invisible": discord.Status.invisible,
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd,
        }
        status = status.lower()
        if status not in stata:
            return await ctx.send(f'Not a valid status! Choose: [{", ".join(stata.keys())}]')
        if ctx.guild is None:
            botmember = self.bot.guilds[0].me
        else:
            botmember = ctx.me
        activity = botmember.activity
        await self.bot.change_presence(status=stata[status], activity=activity)
        await ctx.message.add_reaction("\u2705")
        await ctx.message.delete(delay=15.0)

    @change_presence.command()
    async def clear(self, ctx):
        """clears rich presence"""
        await self.bot.change_presence()
        await ctx.message.add_reaction("\u2705")
        await ctx.message.delete(delay=15.0)

    @change_presence.command()
    async def reset(self, ctx):
        """sets a generic rich presence"""
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name="you for feedback :)")
        )
        await ctx.message.add_reaction("\u2705")
        await ctx.message.delete(delay=15.0)


def setup(bot):
    bot.add_cog(mod(bot))
