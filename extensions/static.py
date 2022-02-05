from discord.commands import slash_command
from discord.ext import commands
from discord.commands import Option
import discord
import requests
import json
from mcstatus import MinecraftServer
from main import guilds
#color of bot
color=0x6bf414
#function to get server latency
def latencyraw(ip):
    try:
        server = MinecraftServer.lookup(ip)
        status = server.status()
        ping="{}".format(status.latency)
        return ping
    except:
        return "Fail"
#Static Cog
class Static(commands.Cog):
    #init function to setup bot class
    def __init__(self, bot):
        self.bot=bot
    #help command
    @slash_command(guild_ids=guilds, description="Lists all the commands of the bot and their uses")
    async def help(self, ctx):
        #really weird embed formatting idk why
        embed = discord.Embed(title="Help & Important Info", description="Lists all the commands and their uses! If you need more assistance or have found a bug then please join the Support Server: [Join now!](https://discord.com/invite/8vNHAA36fR).",color=color)

        embed.set_thumbnail(url="https://me.technotalks.net/ProjectMSS.png"),

        embed.add_field(name="Ping", 
                                value=f"Send latency", 
                                inline=False)
        embed.add_field(name="Developer", 
                                value=f"Sends info about the developer of this bot! Check it out if you want your own custom one!", 
                                inline=False)
        embed.add_field(name="Status", 
                                value=f"Get's the status of any MC Server! Make sure to put the correct ip of the server next to the command!", 
                                inline=False)
        embed.add_field(name="Latency", 
                                value=f"Get's the latency to a minecraft server with a provided ip in ms from the bot's host. ", 
                                inline=False)
        embed.add_field(name="Server", 
                                value=f"Get's the status of the set MC Server! This is set by the server admins and is used like a hotkey!", 
                                inline=False)
        embed.add_field(name="ServerSetup [*Admin Only Command*]", 
                                value=f"This command sets the server for the above listed Server command. This command requires the Adminstrator permission!", 
                                inline=False)
        embed.add_field(name="\u200B",
                                value=f"💻 Developed by TechnoTalks, Support Server: [Join now!](https://discord.com/invite/8vNHAA36fR), Thank you for using {self.bot.user.display_name}!",
                                inline=False)
        await ctx.respond(embed=embed)
    #dev command self advertising go brrr
    @slash_command(guild_ids=guilds, description="Information about the developer!")
    async def dev(self, ctx):
        embed=discord.Embed(title="About the developer!", description="yea the guy who made this bot :D", color=0x00bfff)
        embed.set_author(name="TechnoTalks", url="https://me.technotalks.net/", icon_url="https://me.technotalks.net/PFP.png",)
        embed.set_thumbnail(url="https://me.technotalks.net/PFP.png")
        embed.add_field(name="About me!", value="I'm an aspiring developer who really loves tech! I love to develop things and its just fun for me (*Most of the time). I love to make new things and see that its being used by actual people! For more about me visit: https://me.technotalks.net/about.html!", inline=False)
        embed.add_field(name="Website", value="https://me.technotalks.net/ (or click on my name above :D)", inline=False)
        embed.add_field(name="Want your own bot?", value="Visit my site for more details on how to get your own bot! https://me.technotalks.net/services.html", inline=False)
        embed.set_footer(text="Thanks for reading!")
        await ctx.respond(embed=embed)

    @slash_command(guild_ids=guilds, description= "Get the Status of any Minecraft Server.")
    async def status(self, ctx, ip: Option(str, "The ip of the server.", required=True)):
        url = "https://api.mcsrvstat.us/2/{}".format(ip)
        thing = requests.get(url)
        data = json.loads(thing.content)
        if data["online"] == False:
            embed=discord.Embed(title=f"Error {ip}", description="This server either does not exist or is not online. If you think this is an error, then please join the support server to report this!", color=0xff1a1a)
            await ctx.respond(embed=embed)
        else:
            motd=""
            for i in range(len(data["motd"]["clean"])):
                motd+=data["motd"]["clean"][i]
            
            embed=discord.Embed(title="Status of {}".format(ip), description="{}".format(motd),color=color)
            embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{ip}")
            embed.add_field(name="Online:", value="{}".format(data["online"]), inline=True)
            embed.add_field(name="Player Count:", value="{}".format(data["players"]["online"]), inline=True)
            embed.add_field(name="Version:", value="{}".format(data["version"]), inline=True)
            await ctx.respond(embed=embed)
    @slash_command(guild_ids=guilds, description="Get the latency to a Minecraft Server.")
    async def latency(self, ctx: discord.ApplicationContext, ip: Option(str, "IP of the MC server", required=True)):
        result=latencyraw(ip)
        if result == "Fail":
            embed=discord.Embed(title="Error", description="This server does not exist or is offline", color=0xff1a1a)
            await ctx.respond(embed=embed)
        else:
            embed=discord.Embed(title=f"Latency to {ip}", description=f"{result}"+"ms", color=color)
            embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{ip}")
            embed.add_field(name="Note:", value="This result is the latency from the bot to the server.", inline=True)
            await ctx.respond(embed=embed)

def setup(bot):
    print("Loading extension Static")
    bot.add_cog(Static(bot))
def teardown(bot):
    print("Unloading extension Static")