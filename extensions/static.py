from typing_extensions import Required
import hikari
import lightbulb
from lightbulb.decorators import command
import requests
import json

from datetime import datetime
from lightbulb import commands, context
from lightbulb.context.base import Context
from mcstatus import MinecraftServer

static_plugin = lightbulb.Plugin("Static")

color=0x6bf414

def latencyraw(ip):
    try:
        server = MinecraftServer.lookup(ip+":25565")
        status = server.status()
        ping="{}".format(status.latency)
        return ping
    except:
        return "Fail"

@static_plugin.command
@lightbulb.command("help", "Lists all commands and what they do.")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def help(ctx):
    embed = hikari.Embed(title="Help & Important Info",
                          
                          color=color)
    embed.set_thumbnail("https://me.technotalks.net/ProjectMSS.png")
    embed.add_field(name="Ping", 
					          value=f"Send latency", 
					          inline=False)
    embed.add_field(name="Developer", 
					          value=f"Sends info about the developer of this bot! Check it out if you want your own custom one!", 
					          inline=False)
    embed.add_field(name="Status", 
					          value=f"Gets the status of any MC Server! Make sure to put the correct ip of the server next to the command!", 
					          inline=False)
    embed.add_field(name="Latency", 
					          value=f"Get's the latency to a minecraft server with a provided ip in ms from the bot's host. ", 
					          inline=False)
    embed.add_field(name="\u200B",
                              value=f"💻 Developed by TechnoTalks, Support Server: [Join now!](https://discord.com/invite/8vNHAA36fR), Thank you for using {ctx.bot.get_me().username}!",
                              inline=False)
    await ctx.respond(embed=embed)

@static_plugin.command
@lightbulb.option("ip", "The ip of the server.", required=True)
@lightbulb.command("status", "Get the Status of any Minecraft Server.")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def status(ctx: context.Context):
    ip=ctx.options.ip if ctx.options.ip is not None else "Ip Not Provided"
    url = "https://api.mcsrvstat.us/2/{}".format(ip)
    thing = requests.get(url)
    data = json.loads(thing.content)
    if data["online"] == False:
        embed=hikari.Embed(title=f"Error {ip}", description="This server either does not exist or is not online. If you think this is an error, then please join the support server to report this!", color=0xff1a1a)
        await ctx.respond(embed=embed)
    else:
        motd=""
        for i in range(len(data["motd"]["clean"])):
            motd+=data["motd"]["clean"][i]

        embed=hikari.Embed(title="Status of {}".format(ip), description="{}".format(motd),color=color)
        embed.set_thumbnail(f"https://api.mcsrvstat.us/icon/{ip}")
        embed.add_field(name="Online:", value="{}".format(data["online"]), inline=True)
        embed.add_field(name="Player Count:", value="{}".format(data["players"]["online"]), inline=True)
        embed.add_field(name="Version:", value="{}".format(data["version"]), inline=True)
        await ctx.respond(embed=embed)

@static_plugin.command
@lightbulb.option("ip", "The ip of the server.", required=True)
@lightbulb.command("latency", "Get the latency to a Minecraft Server.")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def latency(ctx):
    ip=ctx.options.ip if ctx.options.ip is not None else "Ip Not Provided"
    result=latencyraw(ip)
    if result == "Fail":
        embed=hikari.Embed(title="Error", description="This server does not exist or is offline", color=0xff1a1a)
        await ctx.respond(embed=embed)
    else:
        embed=hikari.Embed(title=f"Latency to {ip}", description=f"{result}"+"ms", color=color)
        embed.set_thumbnail(f"https://api.mcsrvstat.us/icon/{ip}")
        embed.add_field(name="Note:", value="This result is the latency from the bot to the server.", inline=True)
        await ctx.respond(embed=embed)

@static_plugin.command
@lightbulb.command("dev", "Info about the developer!")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def dev(ctx):
  embed=hikari.Embed(title="About the author!", description="yea the guy who made this bot :D", color=0x00bfff)
  embed.set_author(name="TechnoTalks", url="https://me.technotalks.net/", icon="https://me.technotalks.net/PFP.png")
  embed.set_thumbnail("https://me.technotalks.net/PFP.png")
  embed.add_field(name="About me!", value="I'm an aspiring developer who really loves tech! I love to develop things and its just fun for me (*Most of the time). I love to make new things and see that its being used by actual people! For more about me visit: https://me.technotalks.net/about.html!", inline=False)
  embed.add_field(name="Website", value="https://me.technotalks.net/ (or click on my name above :D)", inline=False)
  embed.add_field(name="Want your own bot?", value="Visit my site for more details on how to get your own bot! https://me.technotalks.net/services.html", inline=False)
  embed.set_footer(text="Thanks for reading!")
  await ctx.respond(embed=embed)
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(static_plugin)