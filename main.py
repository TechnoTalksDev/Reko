import discord
import os
import json, requests
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

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

#Status Command
@client.command()
async def status(ctx, ip):
    url = "https://api.mcsrvstat.us/2/{}".format(ip)
    thing = requests.get(url)
    data = json.loads(thing.content)
    if data["online"] == False:
        await ctx.send("Error: This server either does not exist or is offline!")
    else:
        embed=discord.Embed(title="Status of {}".format(ip), description="{}".format(data["motd"]["clean"]),color=color)
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
        await ctx.send("Error: This server either does not exist or is offline!")
    else:
        embed=discord.Embed(title="Status of {}".format(ip), description="{}".format(data["motd"]["clean"]),color=color)
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
    embed = discord.Embed(title="Help",
                          description=f"{client.user.display_name} Commands",
                          color=color)
    embed.add_field(name="Ping", 
					          value=f"Send latency ({prefix}ping)", 
					          inline=False)
    embed.add_field(name="Developer", 
					          value=f"Sends info about the developer of this bot! Check it out if you want your own custom one! ({prefix}dev)", 
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
