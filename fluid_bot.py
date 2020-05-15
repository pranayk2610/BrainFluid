import discord
import json
from discord.ext import commands
from config import TOKEN

with open('guild_prefs.json') as f:
    prefixes = json.load(f)
default_pref = "bf."

async def prefix_callable(bot, msg):
    guild = msg.guild
    if guild:
        prefUsed = prefixes.get(str(guild.id), default_pref)
        if prefUsed != default_pref:
            return [default_pref, prefUsed]
        else:
            return default_pref
    else:
        return default_pref

bot = commands.Bot(command_prefix=prefix_callable)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

def is_me(m):
    return not m.pinned

@bot.command(aliases=['del', 'd'])
async def delete(ctx, num: int):
    if num > 50:
        await ctx.send("What are you fucking gay")
    else:
        await ctx.channel.purge(limit=num, check=is_me)

@bot.command(aliases=['sp'])
async def setprefix(ctx, pref=''):
    if len(pref) > 10:
        await ctx.send("Too long dumbo")
    elif prefixes.get(ctx.message.guild.id) == None:
        data = {"{}".format(ctx.message.guild.id): '{}'.format(pref)}
        prefixes.update(data)
        with open('guild_prefs.json', 'w') as f:
            json.dump(prefixes, f, indent=0)
    else:
        prefixes[ctx.guild.id] = pref or default_pref
        with open('guild_prefs.json', 'w') as f:
            json.dump(prefixes, f, indent=0)

bot.run(TOKEN)