import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import equipo_26.maid as maid
import equipo_26.ensender_ojos as ensender_ojos
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
maid_task = None
ensender_ojos_task = None
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(f'{bot.user} is connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})')
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f'{bot.user} has connected to Discord!')
@bot.command(name='start_maid', help='Starts the maid line-following behavior.')
async def start_maid(ctx):
    global maid_task
    if maid_task is None or maid_task.done():
        maid_task = asyncio.create_task(run_maid())
        await ctx.send('Maid line-following behavior started.')
    else:
        await ctx.send('Maid line-following behavior is already running.')
@bot.command(name='stop_maid', help='Stops the maid line-following behavior.')
async def stop_maid(ctx):
    global maid_task
    if maid_task is not None and not maid_task.done():
        maid_task.cancel()
        await ctx.send('Maid line-following behavior stopped.')
    else:
        await ctx.send('Maid line-following behavior is not running.')
@bot.command(name='start_ensender_ojos', help='Starts the eye movement behavior.')
async def start_ensender_ojos(ctx):
    global ensender_ojos_task
    if ensender_ojos_task is None or ensender_ojos_task.done():
        ensender_ojos_task = asyncio.create_task(run_ensender_ojos())
        await ctx.send('Eye movement behavior started.')
    else:
        await ctx.send('Eye movement behavior is already running.')
@bot.command(name='stop_ensender_ojos', help='Stops the eye movement behavior.')
async def stop_ensender_ojos(ctx):
    global ensender_ojos_task
    if ensender_ojos_task is not None and not ensender_ojos_task.done():
        ensender_ojos_task.cancel()
        await ctx.send('Eye movement behavior stopped.')
    else:
        await ctx.send('Eye movement behavior is not running.')
async def run_maid():
    while True:
        maid.main()
        await asyncio.sleep(0.1)
async def run_ensender_ojos():
    while True:
        ensender_ojos.main()
        await asyncio.sleep(0.1)
bot.run(TOKEN)