from click import help_option
import discord, datetime, time, os, psutil, sys, coloredlogs, logging, traceback
import src.utilities as utilities
from discord.ext import commands
from dotenv import load_dotenv
from psutil._common import bytes2human
from colorama import init, Fore
#bot client
activity = discord.Activity(type=discord.ActivityType.watching, name="Minecraft Servers")
#bot = discord.Bot(activity=activity, debug_guilds=[846192394214965268])
bot = discord.Bot(activity=activity)
#we need to know what the fuck is happening so logging
coloredlogs.install(level="INFO", fmt="%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s")
logger = logging.getLogger("Reko")
file_handler = logging.FileHandler("SEVERE.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s"))
logger.addHandler(file_handler)
#setting color of bot
init(True)
color=0x6bf414
#getting token from env
try:
    load_dotenv("secrets\.env")
except: pass
token = os.getenv("TOKEN")
#version
version = ""
logger.info(Fore.GREEN+"REKO "+version+"\nEnviroment: ")
#process of bot
process = psutil.Process(os.getpid())

global commands_run
commands_run = 0

logger.info(f"Commands_run: {commands_run}")

#startup message
@bot.event
async def on_ready():
    print(Fore.LIGHTBLUE_EX+
""".-. .-. .-. . . . . .-.   .-. .-. .   . . .-. 
 |  |-  |   |-| |\| | |    |  |-| |   |<  `-. 
 '  `-' `-' ' ` ' ` `-'    '  ` ' `-' ' ` `-'
presents: """)
    logger.info(f"Logged in as {bot.user}")
    global startTime
    startTime=time.time()
    global socketHandler
    socketHandler= utilities.webSocketHandler()

#loading extensions
bot.load_extension("src.extensions.general")
bot.load_extension("src.extensions.custom")
bot.load_extension("src.extensions.tasks")

#ping command
@bot.slash_command(description="Gives stats of the bot.")
async def ping(ctx):
    uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
    embed = discord.Embed(title=f"{bot.user.display_name} Stats", color=color)
    embed.set_author(name="Pong! 🏓")
    embed.set_thumbnail(url="https://www.technotalks.net/static/main/images/Reko_Circular-removebg-preview.png")
    embed.add_field(name="Ping",value=f"`{round(bot.latency * 1000)}ms`",inline=True)
    embed.add_field(name="Uptime", value=f"`{uptime}`", inline=True)
    embed.add_field(name="Guilds", value=f"`{len(bot.guilds)}`", inline=True)
    users = 0
    for guild in bot.guilds:
        users += guild.member_count
    embed.add_field(name="Users", value=f"`{users}`", inline=True)
    #embed.add_field(name="Version", value=f"`{version}`", inline=True)
    embed.add_field(name="RAM", value=f"`{bytes2human(process.memory_info().rss)} used`", inline=True)
    embed.add_field(name="Commands Run", value=f"`{commands_run}`", inline=True)
    await ctx.respond(embed=embed)

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.name == "general":
            embed=discord.Embed(title="Thanks for inviting me!", description="Run `/help` to see all my commands and their uses!", color=0x59f406)
            embed.set_thumbnail(url="https://me.technotalks.net/ProjectMSS.png")
            embed.add_field(name="\u200B", value="Try `/status` to check the status of a server immediately!", inline=False)
            embed.add_field(name="\u200B", value="Please note that this is a **BETA**! Please report any bugs (*or suggestions!*) in my server [Join Now](https://discord.com/invite/8vNHAA36fR)", inline=True)
            embed.set_footer(text="Have fun! 🕶️")
            await channel.send(embed=embed)
        elif channel.permissions_for(guild.me).send_messages:
            embed=discord.Embed(title="Thanks for inviting me!", description="Run `/help` to see all my commands and their uses!", color=0x59f406)
            embed.set_thumbnail(url="https://me.technotalks.net/ProjectMSS.png")
            embed.add_field(name="\u200B", value="Try `/status` to check the status of a server immediately!", inline=False)
            embed.add_field(name="\u200B", value="Please note that this is a **BETA**! Please report any bugs (*or suggestions!*) in my server [Join Now](https://discord.com/invite/8vNHAA36fR)", inline=True)
            embed.set_footer(text="Have fun! 🕶️")
            await channel.send(embed=embed)
        break    

#owner commands
@bot.slash_command(description="Reloads extensions.", guild_ids=[846192394214965268])
@commands.is_owner()
async def reload(ctx):
    await bot.sync_commands()
    bot.reload_extension("extensions.static")
    bot.reload_extension("extensions.dc")
    bot.reload_extension("extensions.tasks")
    await bot.sync_commands()
    await ctx.respond("Reloaded cog's and extensions.")
@reload.error
async def reloaderror(ctx, error):
    await ctx.respond(embed=utilities.ErrorMessage.error_message())
    if error == discord.ext.commands.errors.NotOwner or error == "You do not own this bot.":
        return
    #print(f"[Reload] Error with reloading the bot: {error}, Line #: {sys.exc_info()[-1].tb_lineno}")
    #print(str(sys.exc_info())+"\n"+str(sys.exc_info()[-1])+"\n")
    #print(type(sys.exc_info()[-1]))
    logger.error("Reload Command error")
    logger.error(traceback.format_exc())

@bot.slash_command(description="Kill the bot", guild_ids=[846192394214965268])
@commands.is_owner()
async def kill(ctx):
    logger.critical("BYE!!! (Killed through command)")
    await ctx.respond("Bye!")         
    await bot.close()
@kill.error
async def killerror(ctx, error):
    await ctx.respond(embed=utilities.ErrorMessage.error_message())
    if error == "You do not own this bot.":
        return
    logger.error("Error in Kill Command")
    logger.error(traceback.format_exc())