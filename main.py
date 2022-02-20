import discord, datetime, time, os
from discord.ext import commands, tasks
from quart import Quart, redirect, url_for, render_template, request
from routes.utils import app
#bot client
activity = discord.Activity(type=discord.ActivityType.watching, name="Minecraft Servers")
bot = discord.Bot(activity=activity)
#setting color of bot
color=0x6bf414
#getting token from token file
with open("./secrets/token", "r") as f:
    token = f.read().strip()
#starting quart for website
app = Quart(__name__)
@app.route("/")
async def home():
  return await render_template("index.html", guilds=len(bot.guilds))
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
@bot.slash_command(description="Gives stats of the bot.")
async def ping(ctx):
    uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
    embed = discord.Embed(title=f"{bot.user.display_name} Stats", color=color)
    embed.set_author(name="Pong! 🏓")
    embed.add_field(name="Ping",value=f"`{round(bot.latency * 1000)}ms`",inline=True)
    embed.add_field(name="Uptime", value=f"`{uptime}`", inline=True)
    embed.add_field(name="Servers", value=f"`{len(bot.guilds)}`", inline=True)
    embed.add_field(name="Version", value="`0.2.0`", inline=True)
    await ctx.respond(embed=embed)

@bot.event
async def on_message(message):
    if message.content.startswith("<@!879790233099587595>"):
       channel=message.channel
       await channel.send("Please run the help command!")
       await message.add_reaction("👍")

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
def run():
  bot.loop.create_task(app.run_task('0.0.0.0', port=80))
  bot.run(token)
run()