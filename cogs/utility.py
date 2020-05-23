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
from utils import colors, converters
from utils.global_utils import confirm_prompt, send_embedded
from utils.paginator import Pages

class utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command()
    async def feedback(self, ctx, *, content: str = None):
        if content == None:
            return await send_embedded(ctx, "**ERROR :x:**: Please enter a feedback like !!feedback [content]")
        else:
            channel = discord.utils.get(ctx.guild.text_channels, name='board-general')
            try:
                embed = discord.Embed(title='Feedback',
                                        color=random.choice(self.bot.color_list),
                                        description=content)
                embed.set_author(name=f"Sent by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
                embed.set_footer(text=f"Sent in #{ctx.channel.name}", icon_url=ctx.guild.icon_url)
                await channel.send(embed=embed)
                await ctx.message.delete(delay=5.0)
                await send_embedded(ctx, "Thank you for sending the feedback :smiley:")
            except Exception as e:
                await send_embedded(ctx, f"**Error** {e.__class__.__name__} - {e}")

    @commands.command(name='urban', aliases=['ud'])
    async def _urban_dictionary(self, ctx, *, word=None):
        if word is None:
            return await send_embedded(ctx, "**ERROR :x:**: You are missing the word! Please enter a command like !!urban [word]")
        else:
            r = requests.get(f'http://api.urbandictionary.com/v0/define?term={word}')
            j = r.json()
            _list = []
            for x in j['list']:
                _list.append(f"{x['definition']} \n\n*{x['example']}* \n\n**Votes**\n:thumbsup: {x['thumbs_up']}  :thumbsdown: {x['thumbs_down']} \n\nDefinition written by {x['author']}")
            ud = Pages(ctx, entries=_list, per_page=1)
            await ud.paginate()

    @commands.command()
    async def timer(self, ctx, secs: int = None):
        if secs is None:
            return await send_embedded(ctx, "**ERROR :x:**: You are missing the time! Please enter a command like !!timer [seconds]")
        else:
            await send_embedded(ctx, "Timer has started baby :timer:")
            await asyncio.sleep(float(secs))
            await send_embedded(ctx, f"Time's up {ctx.author.mention} :bell:")

    # TODO: A news command or whole entire cog

def setup(bot):
    bot.add_cog(utility(bot))
