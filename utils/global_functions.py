import discord
from discord.ext import commands

async def confirm_prompt(ctx: commands.Context, msg):
    """Asks author for confirmation, returns True if confirmed, False if user typed abort or timed out"""
    cont = False

    def confirm(msg):
        nonlocal cont
        if ctx.author.id != msg.author.id or ctx.channel.id != msg.channel.id:
            return False
        if msg.content in ('**confirm**', '**Confirm**', 'confirm', 'Confirm'):
            cont = True
            return True
        elif msg.content in ('**abort**', '**Abort**', 'abort', 'Abort'):
            cont = False  # don't continue
            return True
        return False  # author typed something else in the same channel, keep waiting

    prompt = await ctx.send(f'{msg}\n'
                            f'Please type **confirm** within 1 minute to continue or type **abort** if you change your mind.')

    try:
        reply = await ctx.bot.wait_for('message', check=confirm, timeout=60)
        await reply.delete()
    except TimeoutError:
        await ctx.send('1 minute has passed. Aborting...', delete_after=5)
        return False
    except discord.HTTPException:
        pass
    finally:
        await prompt.delete()

    if not cont:  # Author typed abort, don't continue
        await ctx.send('Aborting...', delete_after=5)

    return cont

def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    return content.strip('` \n')

async def is_image(ctx, url, gif=False):
    image_formats = ('image/png', 'image/jpeg', 'image/jpg')
    if gif:
        image_formats += ('image/gif',)
    try:
        async with ctx.bot.session.head(url) as resp:
            return resp.headers['Content-Type'] in image_formats
    except (InvalidURL, KeyError):
        return False
