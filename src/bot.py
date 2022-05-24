import discord, datetime, time, os, psutil, sys
import src.utilities as utilities
from discord.ext import commands
from dotenv import load_dotenv
from psutil._common import bytes2human
from colorama import init, Fore
#bot client
activity = discord.Activity(type=discord.ActivityType.watching, name="Minecraft Servers")
bot = discord.Bot(activity=activity)
#intializing error logger
error_logger=utilities.ErrorLogger("Reko")
#setting color of bot
init(True)
color=0x6bf414
#getting token from env
try:
    load_dotenv("secrets\.env")
except: pass
token = os.getenv("TOKEN")
#version
version = "v0.5.4-beta"
print(Fore.GREEN+"REKO "+version+"\nEnviroment: ")
#process of bot
process = psutil.Process(os.getpid())
#startup message
@bot.event
async def on_ready():
    print(Fore.LIGHTBLUE_EX+
""".-. .-. .-. . . . . .-.   .-. .-. .   . . .-. 
 |  |-  |   |-| |\| | |    |  |-| |   |<  `-. 
 '  `-' `-' ' ` ' ` `-'    '  ` ' `-' ' ` `-'
presents: """)
    print(f"[Reko] Logged in as {bot.user}")
    global startTime
    startTime=time.time()

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
    embed.add_field(name="Version", value=f"`{version}`", inline=True)
    embed.add_field(name="RAM", value=f"`{bytes2human(process.memory_info().rss)} used`", inline=True)
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
    bot.reload_extension("extensions.static")
    bot.reload_extension("extensions.dc")
    bot.reload_extension("extensions.tasks")
    await ctx.respond("Reloaded cog's and extensions.")
@reload.error
async def reloaderror(ctx, error):
    await ctx.respond(embed=utilities.error_message())
    if error == discord.ext.commands.errors.NotOwner or error == "You do not own this bot.":
        return
    #print(f"[Reload] Error with reloading the bot: {error}, Line #: {sys.exc_info()[-1].tb_lineno}")
    #print(str(sys.exc_info())+"\n"+str(sys.exc_info()[-1])+"\n")
    #print(type(sys.exc_info()[-1]))
    error_logger.log("Reload Command", error, sys.exc_info()[-1])

@bot.slash_command(description="Kill the bot", guild_ids=[846192394214965268])
@commands.is_owner()
async def kill(ctx):
    print("\n[Reko] BYE!!! (Killed through command)")
    await ctx.respond("Bye!")         
    await bot.close()
@kill.error
async def killerror(ctx, error):
    await ctx.respond(embed=utilities.error_message())
    if error == "You do not own this bot.":
        return
    error_logger.log("Kill Command", error, sys.exc_info()[-1])