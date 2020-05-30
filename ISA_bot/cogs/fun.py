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
    """weird, silly and fun commands that will probably make to smile"""

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command(name="yesno", aliases=["yn"])
    async def yesorno(self, ctx):
        """gives a gif with yes or no"""
        r = requests.get("https://yesno.wtf/api")
        j = r.json()

        embed = discord.Embed(title=j["answer"])
        embed.set_image(url=j["image"])
        embed.set_footer(text=f"Sent by {ctx.author}")
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command(aliases=["tf", "face"])
    async def textface(self, ctx, Type=None):
        """gives out a funny textface"""
        if Type is None:
            await ctx.send(
                "That is NOT one of the dank textfaces in here yet. Use: *textface list to get a list of textfaces you can use."
            )
        else:
            if Type.lower() == "lenny":
                await ctx.send("( ͡° ͜ʖ ͡°)")
            elif Type.lower() == "tableflip":
                await ctx.send("(ノಠ益ಠ)ノ彡┻━┻")
            elif Type.lower() == "shrug":
                await ctx.send(r"¯\_(ツ)_/¯")
            elif Type.lower() == "bignose":
                await ctx.send("(͡ ͡° ͜ つ ͡͡°)")
            elif Type.lower() == "iwant":
                await ctx.send("ლ(´ڡ`ლ)")
            elif Type.lower() == "musicdude":
                await ctx.send("ヾ⌐*_*ノ♪")
            elif Type.lower() == "wot":
                await ctx.send("ლ,ᔑ•ﺪ͟͠•ᔐ.ლ")
            elif Type.lower() == "bomb":
                await ctx.send("(´・ω・)っ由")
            elif Type.lower() == "orlly":
                await ctx.send("﴾͡๏̯͡๏﴿ O'RLY?")
            elif Type.lower() == "money":
                await ctx.send("[̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲̅]")
            elif Type.lower() == "list":
                em = discord.Embed(color=random.choice(self.bot.color_list), title="List of Textfaces")
                em.description = "Choose from the following: lenny, tableflip, shrug, bignose, iwant, musicdude, wot, bomb, orlly, money. Type *textface [face]."
                em.set_footer(text="Don't you dare question my names for the textfaces.")
                await ctx.send(embed=em)
            else:
                await send_embedded(
                    ctx,
                    "That is NOT one of the dank textfaces in here yet. Use !!textface list to see a list of the textfaces.",
                )
        await ctx.message.delete()

    @commands.group(case_insensitive=True, invoke_without_command=True)
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def cat(self, ctx):
        """cats! cats everywhere!"""
        await ctx.send_help(ctx.command)

    async def get_cat(self, ctx, r):
        if r.status_code == 200:
            j = r.json()
        else:
            return await send_embedded(ctx, f"Error {r.status_code} in fetching the image. Try again later please.")

        embed = discord.Embed(title="A wild cat has appeared :cat:", color=random.choice(self.bot.color_list))
        embed.set_image(url=j[0]["url"])
        embed.set_footer(text=f"Image requested by {ctx.author}\nFetched from TheCatApi")
        await ctx.send(embed=embed)
        await ctx.message.delete(delay=60.0)

    @cat.command(name="gif")
    async def gif(self, ctx):
        """yes a cat gif"""
        header = {"x-api-key": self.bot.config["keys"]["cat_api"]}
        r = requests.get(url="https://api.thecatapi.com/v1/images/search?mime_types=gif", headers=header)
        await self.get_cat(ctx, r)

    @cat.command(name="pic")
    async def pic(self, ctx):
        """yes a cat pic"""
        header = {"x-api-key": self.bot.config["keys"]["cat_api"]}
        r = requests.get(url="https://api.thecatapi.com/v1/images/search?mime_types=jpg,png", headers=header)
        print(r)
        await self.get_cat(ctx, r)

    @commands.group(case_insensitive=True, invoke_without_command=True)
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def dog(self, ctx):
        """doggo doggo doggo"""
        await ctx.send_help(ctx.command)

    # IDEA: Allow people to list breeds and search by breeds
    async def get_dog(self, ctx, r):
        if r.status_code == 200:
            j = r.json()
        else:
            return await send_embedded(ctx, f"Error {r.status_code} in fetching the image. Try again later please.")

        embed = discord.Embed(title="OMG a doggo :dog:", color=random.choice(self.bot.color_list))
        embed.set_image(url=j[0]["url"])
        embed.set_footer(text=f"Image requested by {ctx.author}\nFetched from TheDogApi")
        await ctx.send(embed=embed)
        await ctx.message.delete(delay=60.0)

    @dog.command(name="gif")
    async def _gif(self, ctx):
        """A dog gif"""
        header = {"x-api-key": self.bot.config["keys"]["dog_api"]}
        r = requests.get(url="https://api.thedogapi.com/v1/images/search?mime_types=gif", headers=header)
        await self.get_dog(ctx, r)

    @dog.command(name="pic")
    async def _pic(self, ctx):
        """a dog pic"""
        header = {"x-api-key": self.bot.config["keys"]["dog_api"]}
        r = requests.get(url="https://api.thedogapi.com/v1/images/search?mime_types=jpg,png", headers=header)
        await self.get_dog(ctx, r)

    # REVIEW: check if command is working or not
    # NOTE: extend the limit to get more gifs if ever needed
    @commands.command(name="giphy", aliases=["giffy", "jiff"])
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def giphy(self, ctx, *, search=None):
        """gets a random gif from giphy"""
        head = {"api_key": self.bot.config["keys"]["giphy_api"]}

        if search is None:
            r = requests.get(url="http://api.giphy.com/v1/gifs/trending", headers=head)
        else:
            search.replace(" ", "+")
            url = f"http://api.giphy.com/v1/gifs/search?q={search}"
            r = requests.get(url=url, headers=head)

        if r.status_code == 200:
            j = r.json()
        else:
            return await send_embedded(ctx, f"Error {r.status_code} in fetching the image. Try again later please.")

        rand = random.choice(j["data"])
        gif_title = rand["title"]
        gif_url = rand["images"]["downsized_large"]["url"]

        embed = discord.Embed(
            title=gif_title, color=random.choice(self.bot.color_list), description=f"requested by {ctx.author}"
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Powered by GIPHY")
        await ctx.send(embed=embed)

    # https://nekos.life/api/v2/img/slap
    # api for various stuff including nsfw content

    # NOTE: othher gif APIs include gfycat and tenor

    @commands.command(name="memes", aliases=["meme", "meem"])
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def memes(self, ctx):
        """get a meme from r/me_irl, r/dankmemes and r/memes"""
        r = requests.get(url="https://meme-api.herokuapp.com/gimme")

        if r.status_code == 200:
            j = r.json()
        else:
            return await send_embedded(ctx, f"Error {r.status_code} in fetching the image. Try again later please.")

        sub = j["subreddit"]
        embed = discord.Embed(
            title=j["title"], description=f"posted on r/{sub}", color=random.choice(self.bot.color_list)
        )
        embed.set_image(url=j["url"])
        embed.set_footer(text=f"Requested by {ctx.author} 👾")
        await ctx.send(embed=embed)

    # TODO: Reddit command to fetch memes and gifs from reddit


def setup(bot):
    bot.add_cog(fun(bot))
