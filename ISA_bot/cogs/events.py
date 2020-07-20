import os
import requests
import discord
import asyncio
import random
import datetime
import copy
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
                type=discord.ActivityType.watching, name="for commands starting with !!, isa! or i!",
            ),
        )

    # No nonsense self role but requires a on emoji remove function
    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload):
    #     message_id = payload.message_id
    #     if message_id == 733615890293194752:
    #         guild_id = payload.guild_id
    #         guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)

    #         if payload.emoji.name == "🙋‍♂️":
    #             role = discord.utils.get(guild.roles, name="He/Him")
    #         if payload.emoji.name == "🙋‍♀️":
    #             role = discord.utils.get(guild.roles, name="She/Her")
    #         if payload.emoji.name == "🙋":
    #             role = discord.utils.get(guild.roles, name="Them/They")

    #         if role is not None:
    #             member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
    #             if member is not None:
    #                 await member.add_roles(role)
    #             else:
    #                 print("member not found")

    # NOTE: all the messages and their IDs are hard coded as of now and probably will be since this bot is only for one server.
    # IDEA: I can go ahead and store everything in a database or a JSON file but seems unnecessary as it'll be only extra steps.
    # IDEA: If in future it turns out to be useful function, a bot command can be made which asks for a message and emoji and their roles and posts it
    # while storing all IDs in JSON and reading from there.

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        if message_id == 734044027858452502:  # ID of the role message
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)

            roles = {
                "🙋‍♂️": "He/Him",
                "🙋‍♀️": "She/Her",
                "🙋": "They/Them",
            }

            if payload.emoji.name == "🙋‍♂️":
                role = discord.utils.get(guild.roles, name="He/Him")
            if payload.emoji.name == "🙋‍♀️":
                role = discord.utils.get(guild.roles, name="She/Her")
            if payload.emoji.name == "🙋":
                role = discord.utils.get(guild.roles, name="They/Them")

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    current_role = list(filter(lambda r: str(r) in list(roles.values()), payload.member.roles))
                    await member.remove_roles(*current_role)
                    await member.add_roles(role)
                    pronoun_message = await self.bot.get_channel(699675695231533126).fetch_message(
                        734044027858452502
                    )  # ID of role message or channel
                    await pronoun_message.remove_reaction(payload.emoji, payload.member)
                else:
                    print("member not found")

        if message_id == 734610164899905569:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)

            roles = {
                "👶": "👶 Freshman",
                "✌️": "✌️ Sophomore",
                "🍻": "🍻 Junior",
                "👑": "👑 Senior",
                "💀": "💀 SuperSenior",
                "👨‍🎓": "👨‍🎓 Alumna",
                "📜": "📜 Graduate School",
                "🍾": "🍾 PhD",
            }

            role = None

            for x in list(roles.keys()):
                if payload.emoji.name == x:
                    role = discord.utils.get(guild.roles, name=roles[x])
                    break

            if role is not None:
                current_role = list(filter(lambda r: str(r) in list(roles.values()), payload.member.roles))
                await payload.member.remove_roles(*current_role)
                await payload.member.add_roles(role)
                class_message = await self.bot.get_channel(699675695231533126).fetch_message(734610164899905569)
                if current_role:
                    for emoji, pre_role in roles.items():
                        if pre_role == str(current_role[0]):
                            await class_message.remove_reaction(emoji, payload.member)
                            break

            else:
                print("role not found")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message_id = payload.message_id
        if message_id == 734610164899905569:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)

            roles = {
                "👶": "👶 Freshman",
                "✌️": "✌️ Sophomore",
                "🍻": "🍻 Junior",
                "👑": "👑 Senior",
                "💀": "💀 SuperSenior",
                "👨‍🎓": "👨‍🎓 Alumna",
                "📜": "📜 Graduate School",
                "🍾": "🍾 PhD",
            }

            role = None

            for x in list(roles.keys()):
                if payload.emoji.name == x:
                    role = discord.utils.get(guild.roles, name=roles[x])
                    break

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
            else:
                print("role not found")

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     channel = discord.utils.get(member.guild.text_channels, name="welcome🔥")
    #     des = (
    #         f"Welcome {member.mention} to Indian Students Association's "
    #         f"official discord server!\n"
    #         f"Don't forget to check {(discord.utils.get(member.guild.channels, name='rules📃')).mention}"
    #         f"and {(discord.utils.get(member.guild.channels, name='faq')).mention}"
    #     )
    #     if channel:
    #         embed = discord.Embed(description=des, color=random.choice(self.bot.color_list))
    #         embed.set_thumbnail(url=member.avatar_url)
    #         embed.set_author(name=member.name, icon_url=member.avatar_url)
    #         embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
    #         embed.timestamp = datetime.datetime.utcnow()

    #         await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(events(bot))
