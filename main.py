import discord
from discord.ext import commands, tasks
import datetime, time
#bot client
activity = discord.Activity(type=discord.ActivityType.watching, name="Minecraft Servers")
bot = discord.Bot(activity=activity, debug_guilds=[846192394214965268, 923355914495475732, 866018599557791755])
#setting color of bot
color=0x6bf414
#guilds to process slash commands this is just a placeholder to make it easier for me
guilds=[846192394214965268, 923355914495475732, 866018599557791755]
#getting token from token file
with open("./secrets/token", "r") as f:
    token = f.read().strip()
#startup message
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    global startTime
    startTime=time.time()

#loading extensions
bot.load_extension("extensions.static")
bot.load_extension("extensions.dc")
bot.load_extension("extensions.tasks")

#ping command
@bot.slash_command(description="Latency of the bot to Discord")
async def ping(ctx):
    uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
    embed = discord.Embed(title=f"{bot.user.display_name} Stats", color=color)
    embed.set_author(name="Pong! 🏓")
    embed.add_field(name="Ping",value=f"`{round(bot.latency * 1000)}ms`",inline=True)
    embed.add_field(name="Uptime", value=f"`{uptime}`", inline=True)
    embed.add_field(name="Servers", value=f"`{len(bot.guilds)}`")
    await ctx.respond(embed=embed)

@bot.event
async def on_message(message):
    if message.content.startswith("<@!879790233099587595>"):
       channel=message.channel
       await channel.send("Please run the help command!")
       await message.add_reaction("👍")
#reload extensions
@bot.slash_command(description="Reloads extensions.")
@discord.is_owner()
async def reload(ctx):
    bot.reload_extension("extensions.static")
    bot.reload_extension("extensions.dc")
    bot.reload_extension("extensions.tasks")
    print("Done reloading!")
    await ctx.respond("Reloaded cog's and extensions.")
@reload.error
async def reloaderror(ctx, error):
    await ctx.respond("Something went wrong...")
    raise error
#running bot
bot.run(token)