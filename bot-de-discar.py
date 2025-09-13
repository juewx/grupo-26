import os
import sys
import asyncio

# --- Manejo de errores para dependencias ---
try:
    import discord
    from discord.ext import commands
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Error: Falta una dependencia. Instala con 'pip install discord.py python-dotenv'.\n{e}")
    sys.exit(1)

# --- Manejo de errores para módulos locales ---
errores_modulos = []
try:
    import maid
except ImportError:
    errores_modulos.append("maid.py")
try:
    import ensender_ojos
except ImportError:
    errores_modulos.append("ensender_ojos.py")
try:
    import detesion_de_color as cyberpi
except ImportError:
    errores_modulos.append("detesion_de_color.py")

if errores_modulos:
    print(f"Error: Faltan los siguientes módulos locales: {', '.join(errores_modulos)}")
    sys.exit(1)

# --- Función para verificar si el robot detecta rojo ---
def robot_funcionando():
    try:
        return cyberpi.quad_rgb_sensor.is_color("L1", "red") or cyberpi.quad_rgb_sensor.is_color("R1", "red")
    except Exception as e:
        print(f"Advertencia: No se pudo verificar el estado del robot. {e}")
        return False

# --- Cargar variables de entorno ---
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')

# --- Validación de variables de entorno ---
errores_env = []
if not TOKEN:
    errores_env.append("DISCORD_TOKEN")
if not GUILD:
    errores_env.append("DISCORD_GUILD")
if not CHANNEL_ID:
    errores_env.append("DISCORD_CHANNEL_ID")

if errores_env:
    print(f"Error: Faltan las siguientes variables en el archivo .env: {', '.join(errores_env)}")
    sys.exit(1)

try:
    CHANNEL_ID = int(CHANNEL_ID)
except ValueError:
    print("Error: DISCORD_CHANNEL_ID debe ser un número.")
    sys.exit(1)

# --- Configuración de intents y bot ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

maid_task = None
ensender_ojos_task = None

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    guild = discord.utils.get(bot.guilds, name=GUILD)
    if guild:
        print(f'{bot.user} is connected to the following guild:\n'
              f'{guild.name}(id: {guild.id})')
    else:
        print(f"No se encontró el servidor '{GUILD}'")
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
    try:
        while True:
            maid.main()
            await asyncio.sleep(0.1)
    except Exception as e:
        print(f"Error en maid.main(): {e}")

async def run_ensender_ojos():
    try:
        while True:
            ensender_ojos.main()
            await asyncio.sleep(0.1)
    except Exception as e:
        print(f"Error en ensender_ojos.main(): {e}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"Error al ejecutar el comando: {error.original}")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando no reconocido.")
    else:
        await ctx.send(f"Error: {error}")

bot.run(TOKEN)