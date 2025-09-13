import os
import asyncio

# Importaciones de librerías externas
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Importaciones de módulos locales
import maid
import ensender_ojos
import detesion_de_color as cyberpi

# --- NUEVO: función para verificar si el robot detecta rojo ---
def robot_funcionando():
    try:
        return cyberpi.quad_rgb_sensor.is_color("L1", "red") or cyberpi.quad_rgb_sensor.is_color("R1", "red")
    except Exception:
        return False
# -------------------------------------------------------------

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

# Configuración de intents y bot
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
    if channel is not None:
        await channel.send(f'{bot.user} has connected to Discord!')
    else:
        print(f'No se encontró el canal con ID {CHANNEL_ID}')

@bot.command(name='start_maid', help='Inicia el seguimiento de línea (maid).')
async def start_maid(ctx):
    global maid_task
    if robot_funcionando():
        await ctx.send('El robot está funcionando correctamente. El bot solo se activa en caso de emergencia.')
        return
    if maid_task is None or maid_task.done():
        maid_task = asyncio.create_task(run_maid())
        await ctx.send('Maid line-following behavior started.')
    else:
        await ctx.send('Maid line-following behavior is already running.')

@bot.command(name='stop_maid', help='Detiene el seguimiento de línea (maid).')
async def stop_maid(ctx):
    global maid_task
    if maid_task is not None and not maid_task.done():
        maid_task.cancel()
        await ctx.send('Maid line-following behavior stopped.')
    else:
        await ctx.send('Maid line-following behavior is not running.')

@bot.command(name='start_ensender_ojos', help='Inicia el movimiento de ojos.')
async def start_ensender_ojos(ctx):
    global ensender_ojos_task
    if robot_funcionando():
        await ctx.send('El robot está funcionando correctamente. El bot solo se activa en caso de emergencia.')
        return
    if ensender_ojos_task is None or ensender_ojos_task.done():
        ensender_ojos_task = asyncio.create_task(run_ensender_ojos())
        await ctx.send('Eye movement behavior started.')
    else:
        await ctx.send('Eye movement behavior is already running.')

@bot.command(name='stop_ensender_ojos', help='Detiene el movimiento de ojos.')
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