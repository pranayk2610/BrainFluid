import discord
import json
from discord.ext import commands
import googletrans
import logging
import random
from config import TOKEN

description = '''
I'm just a bot for fun
'''

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

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

bot = commands.Bot(command_prefix=prefix_callable, description=description)

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

def is_me(m):
    return not m.pinned

@bot.command(aliases=['del', 'd'], help="Delete messages from a channel")
async def delete(ctx, num: int):
    if num > 50:
        await ctx.send("Too much power")
    else:
        await ctx.channel.purge(limit=num, check=is_me)

@bot.command(aliases=['latency'], help="Check latency of bot")
async def ping(ctx):
    num = round(bot.latency * 1000)
    if num < 50:
        await ctx.send(f'{num}ms: Discord is speed')
    elif num < 150:
        await ctx.send(f'{num}ms: Discord sux')
    else:
        await ctx.send(f'{num}ms: Use Skype')

@bot.command(aliases=['sp'], help="Change the command prefix")
async def setprefix(ctx, pref=''):
    if len(pref) > 10:
        await ctx.send("Why would you use that")
    elif len(pref) == 0:
        await ctx.send("Its blank you idiot")
    elif prefixes.get(ctx.message.guild.id) == None:
        data = {"{}".format(ctx.message.guild.id): '{}'.format(pref)}
        prefixes.update(data)
        with open('guild_prefs.json', 'w') as f:
            json.dump(prefixes, f, indent=0)
    else:
        prefixes[ctx.guild.id] = pref or default_pref
        with open('guild_prefs.json', 'w') as f:
            json.dump(prefixes, f, indent=0)

@bot.command(aliases=['t'], help="Translates messages")
async def translate(ctx, source: str, dest: str, *, message: str):
    source = source.lower()
    dest = dest.lower()
    trans = googletrans.Translator()
    if googletrans.LANGUAGES.get(source) == None and googletrans.LANGCODES.get(source) == None:
        await ctx.send("Can't translate from that")
    elif googletrans.LANGUAGES.get(dest) == None and googletrans.LANGCODES.get(dest) == None:
        await ctx.send("Can't translate to that")
    else: 
        result = trans.translate(message, dest, source)
        embed = discord.Embed(title='Translated', colour=0x4284F3)
        embed.add_field(name=f'From {source.title()}', value=result.origin, inline=False)
        embed.add_field(name=f'To {dest.title()}', value=result.text, inline=False)
        if dest != 'english' and dest != 'en':
            embed.add_field(name=f'Pronounced', value=result.pronunciation, inline=False)
        await ctx.send(embed=embed)

@bot.command(help="Gives it to you straight. Or gay")
async def gay(ctx, *, msg: str):
    if "trap" in msg:
        await ctx.send("Bruh thats hella gay")
    else:
        num = random.randint(0,1)
        if num:
            await ctx.send("Sounds reasonably not gay")
        else:
            await ctx.send("Bruh thats hella gay")

@delete.error
async def delete_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Does that look like a number to you")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('What am I gonna delete')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("You KNOW thats not a command")

bot.run(TOKEN)