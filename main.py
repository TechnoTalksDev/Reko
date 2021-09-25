#    .-. .-. .-.   . .-. .-. .-.   .  . .-. .-. 
#    |-' |(  | |   | |-  |    |    |\/| `-. `-. 
#    '   ' ' `-' `-' `-' `-'  '    '  ` `-' `-' 
# A veristile Minecraft Server Status bot for Discord.
#
# TO DO:
#   Error Handling
#   Database for server registering
#   Fancying up
#   Hosting setup
#
# IN PROGRESS:
#   Latency Command
#
# DONE: 
import discord
import os
import json, requests
import latencyr
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from icmplib import ping
from ping3 import ping
from mcstatus import MinecraftServer

prefix = "="

client = commands.Bot(command_prefix=f"{prefix}", help_command=None)

slash = SlashCommand(client, sync_commands=True)

#Set Color, enter hex number after the 0x
color = 0x6bf414

#Online
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Minecraft Servers'))
    print(f"Logged in as {client.user.display_name}!")

#Slash Ping
@slash.slash(description="Gives the latency of the bot!")
async def ping(ctx):
    embed = discord.Embed(title=f"{client.user.display_name}", color=color)
    embed.set_author(name="Pong! 🏓")
    embed.add_field(name="Ping",
                    value=f"{round(client.latency * 1000)}ms",
                    inline=False)
    await ctx.send(embed=embed)

#Latency 
@client.command()
async def latency(ctx, ip):
    result=latencyr.latencyr(ip)
    if result == "Fail":
        embed=discord.Embed(title="Error", description="This server does not exist or is offline", color=0xff1a1a)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title=f"Latency to {ip}", description=f"{result}"+"ms", color=color)
        embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{ip}")
        embed.add_field(name="Note:", value="This result may not exactly match your ping", inline=True)
        await ctx.send(embed=embed)

#Status Command
@client.command()
async def status(ctx, ip):
    #print("Ip:"+ip)
    #if ip == "":
        #await ctx.send("Please try again and, provide an IP")
    url = "https://api.mcsrvstat.us/2/{}".format(ip)
    thing = requests.get(url)
    data = json.loads(thing.content)
    if data["online"] == False:
        embed=discord.Embed(title="Error {}".format(ip), description="This server either does not exist or is not online. If you think this is an error, then please join the support server to report this!", color=0xff1a1a)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Status of {}".format(ip), description="{}".format(data["motd"]["clean"]),color=color)
        embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{ip}")
        embed.add_field(name="Online:", value="{}".format(data["online"]), inline=True)
        embed.add_field(name="Player Count:", value="{}".format(data["players"]["online"]), inline=True)
        embed.add_field(name="Version:", value="{}".format(data["version"]), inline=True)
        await ctx.send(embed=embed)

#Slash Status Command
@slash.slash(description="Get the Status of any Minecraft Server!")
async def status(ctx, ip):
    url = "https://api.mcsrvstat.us/2/{}".format(ip)
    thing = requests.get(url)
    data = json.loads(thing.content)
    if data["online"] == False:
        embed=discord.Embed(title="Error {ip}", description="This server either does not exist or is not online. If you think this is an error, then please join the support server to report this!", color=0xff1a1a)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Status of {}".format(ip), description="{}".format(data["motd"]["clean"]),color=color)
        embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{ip}")
        embed.add_field(name="Online:", value="{}".format(data["online"]), inline=True)
        embed.add_field(name="Player Count:", value="{}".format(data["players"]["online"]), inline=True)
        embed.add_field(name="Version:", value="{}".format(data["version"]), inline=True)
        await ctx.send(embed=embed)
#Dev
@client.command()
async def dev(ctx):
  embed=discord.Embed(title="About the author!", description="yea the guy who made this bot :D", color=0x00bfff)
  embed.set_author(name="TechnoTalks", url="https://me.technotalks.net/", icon_url="https://me.technotalks.net/PFP.png")
  embed.set_thumbnail(url="https://me.technotalks.net/PFP.png")
  embed.add_field(name="About me!", value="I'm an aspiring developer who really loves tech! I love developing so much that it never feels like work, that's one of the reasons I offer my services for free!* I love to make new things and see that its being used by actual people! For more about me visit: https://me.technotalks.net/about.html!", inline=False)
  embed.add_field(name="Website", value="https://me.technotalks.net/ (or click on my name above :D)", inline=False)
  embed.add_field(name="Want your own bot?", value="Visit my site for more details on how to get your own bot! https://me.technotalks.net/services.html", inline=False)
  embed.set_footer(text="Thanks for reading!")
  await ctx.send(embed=embed)

#Ping
@client.command()
async def ping(ctx):
    embed = discord.Embed(title=f"{client.user.display_name}", color=color)
    embed.set_author(name="Pong! 🏓")
    embed.add_field(name="Ping",
                    value=f"{round(client.latency * 1000)}ms",
                    inline=False)
    await ctx.send(embed=embed)


#Help
@client.command()
async def help(ctx):
    embed = discord.Embed(title="Help & Important Info",
                          description=f"{client.user.display_name} Commands. Note all of these commands (excluding those marked with *) are avalible as / commands. This is a more streamlined way to use MineCord because it allows you to see what input is required and what all the commands do. You can also view all of MineCord's commands by typing / and then clicking on MineCord's profile picture on the menu that comes up! If slash commands aren't working try the normal prefix command!",
                          color=color)
    embed.set_thumbnail(url="https://me.technotalks.net/ProjectMSS.png")
    embed.add_field(name="Ping", 
					          value=f"Send latency ({prefix}ping)", 
					          inline=False)
    embed.add_field(name="Developer", 
					          value=f"Sends info about the developer of this bot! Check it out if you want your own custom one! ({prefix}dev)", 
					          inline=False)
    embed.add_field(name="Status", 
					          value=f"Gets the status of any MC Server! Make sure to put the correct ip of the server next to the command! ({prefix}status + IP)", 
					          inline=False)
    embed.add_field(name="\u200B",
                              value=f"💻 Developed by TechnoTalks, Support Server: [Join now!](https://discord.com/invite/8vNHAA36fR), Thank you for using {client.user.display_name}!",
                              inline=False)
    await ctx.send(embed=embed)

#Slash Help
@slash.slash(description="Shows Commands and other Usefull info!")
async def help(ctx):
    embed = discord.Embed(title="Help & Important Info",
                          description=f"{client.user.display_name} Commands. Note all of these commands (excluding those marked with *) are avalible as / commands. This is a more streamlined way to use MineCord because it allows you to see what input is required and what all the commands do. You can also view all of MineCord's commands by typing / and then clicking on MineCord's profile picture on the menu that comes up! If slash commands aren't working try the normal prefix command!",
                          color=color)
    embed.set_thumbnail(url="https://me.technotalks.net/ProjectMSS.png")
    embed.add_field(name="Ping", 
					          value=f"Send latency ({prefix}ping)", 
					          inline=False)
    embed.add_field(name="Developer", 
					          value=f"Sends info about the developer of this bot! Check it out if you want your own custom one! ({prefix}dev)", 
					          inline=False)
    embed.add_field(name="Status", 
					          value=f"Gets the status of any MC Server! Make sure to put the correct ip of the server next to the command! ({prefix}status + IP)", 
					          inline=False)
    embed.add_field(name="\u200B",
                              value=f"💻 Developed by TechnoTalks, Support Server: [Join now!](https://discord.com/invite/8vNHAA36fR), Thank you for using {client.user.display_name}!",
                              inline=False)
    await ctx.send(embed=embed)

#Unrecognized Command
@client.event
async def on_message_error(ctx, error):
    print("message error")
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        print("its a wrong command")
        await ctx.send("Unregcognized Command | Please run {prefix}help for acceptable commands!")

client.run("ODc5NzkwMjMzMDk5NTg3NTk1.YSU2gQ.IgilPEdgxKbQe5KpRInQeAfPNFs")
