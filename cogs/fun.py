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

class fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command(name='yesno', aliases=['yn'])
    async def yesorno(self, ctx):
        r = requests.get('https://yesno.wtf/api')
        j = r.json()

        embed = discord.Embed(title=j['answer'])
        embed.set_image(url=j['image'])
        embed.set_footer(text=f"Sent by {ctx.author}")
        await ctx.message.delete()
        await ctx.send(embed=embed)


    @commands.command(aliases=['tf', 'face'])
    async def textface(self, ctx, Type=None):
        if Type is None:
            await ctx.send('That is NOT one of the dank textfaces in here yet. Use: *textface list to get a list of textfaces you can use.')
        else:
            if Type.lower() == 'lenny':
              await ctx.send('( ͡° ͜ʖ ͡°)')
            elif Type.lower() == 'tableflip':
              await ctx.send('(ノಠ益ಠ)ノ彡┻━┻')
            elif Type.lower() == 'shrug':
              await ctx.send('¯\_(ツ)_/¯')
            elif Type.lower() == 'bignose':
              await ctx.send('(͡ ͡° ͜ つ ͡͡°)')
            elif Type.lower() == 'iwant':
              await ctx.send('ლ(´ڡ`ლ)')
            elif Type.lower() == 'musicdude':
              await ctx.send('ヾ⌐*_*ノ♪')
            elif Type.lower() == 'wot':
              await ctx.send('ლ,ᔑ•ﺪ͟͠•ᔐ.ლ')
            elif Type.lower() == 'bomb':
              await ctx.send('(´・ω・)っ由')
            elif Type.lower() == 'orlly':
              await ctx.send("﴾͡๏̯͡๏﴿ O'RLY?")
            elif Type.lower() == 'money':
              await ctx.send('[̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲̅]')
            elif Type.lower() == 'list':
              color = discord.Color(value=0x00ff00)
              em = discord.Embed(color=color, title='List of Textfaces')
              em.description = 'Choose from the following: lenny, tableflip, shrug, bignose, iwant, musicdude, wot, bomb, orlly, money. Type *textface [face].'
              em.set_footer(text="Don't you dare question my names for the textfaces.")
              await ctx.send(embed=em)
            else:
              await send_embedded(ctx, 'That is NOT one of the dank textfaces in here yet. Use !!textface list to see a list of the textfaces.')

    @commands.group(case_insensitive=True, invoke_without_command=True)
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def cat(self, ctx):
        await ctx.send_help(ctx.command)

    async def get_cat(self, ctx, r):
        if r.status_code == 200:
            j = r.json()
        else:
            return await send_embedded(ctx, f"Error {r.status_code} in fetching the image. Try again later please.")

        embed = discord.Embed(title="A wild cat has appeared :cat:",
                                color=random.choice(self.bot.color_list))
        embed.set_image(url=j[0]['url'])
        embed.set_footer(text=f"Image requested by {ctx.author}\nFetched from TheCatApi")
        await ctx.send(embed=embed)
        await ctx.message.delete(delay=60.0)

    @cat.command(name='gif')
    async def _gif(self, ctx):
        header = {"x-api-key": self.bot.config['keys']['cat_api']}
        r = requests.get(url='https://api.thecatapi.com/v1/images/search?mime_types=gif', headers=header)
        await self.get_cat(ctx, r)

    @cat.command(name='pic')
    async def _pic(self, ctx):
        header = {"x-api-key": self.bot.config['keys']['cat_api']}
        r = requests.get(url='https://api.thecatapi.com/v1/images/search?mime_types=jpg,png', headers=header)
        await self.get_cat(ctx, r)

    @commands.group(case_insensitive=True, invoke_without_command=True)
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def dog(self, ctx):
        await ctx.send_help(ctx.command)

    # IDEA: Allow people to list breeds and search by breeds
    async def get_dog(self, ctx, r):
        if r.status_code == 200:
            j = r.json()
        else:
            return await send_embedded(ctx, f"Error {r.status_code} in fetching the image. Try again later please.")

        embed = discord.Embed(title="OMG a doggo :dog:",
                                color=random.choice(self.bot.color_list))
        embed.set_image(url=j[0]['url'])
        embed.set_footer(text=f"Image requested by {ctx.author}\nFetched from TheCatApi")
        await ctx.send(embed=embed)
        await ctx.message.delete(delay=60.0)

    @dog.command(name='gif')
    async def _gif(self, ctx):
        header = {"x-api-key": self.bot.config['keys']['dog_api']}
        r = requests.get(url='https://api.thedogapi.com/images/search?mime_types=gif', headers=header)
        await self.get_dog(ctx, r)

    @dog.command(name='pic')
    async def _pic(self, ctx):
        header = {"x-api-key": self.bot.config['keys']['dog_api']}
        r = requests.get(url='https://api.thedogapi.com/images/search?mime_types=jpg,png', headers=header)
        await self.get_dog(ctx, r)

    # https://nekos.life/api/v2/img/slap
    # api for various stuff including nsfw content

def setup(bot):
    bot.add_cog(fun(bot))
