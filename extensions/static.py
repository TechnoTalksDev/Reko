import discord, requests, json, geocoder, os
from discord.commands import slash_command
from discord.ext import commands
from discord.commands import Option
from mcstatus import MinecraftServer
from staticmap import StaticMap, CircleMarker
#from main import guilds
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
#function to get maps
def get_map(ip):
    g = geocoder.ip(ip)
    coords = g.latlng
    #create map
    tiles_url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    m = StaticMap(500, 500, url_template=tiles_url)
    #create marker for location
    marker_outline = CircleMarker((coords[1], coords[0]), "white", 18)
    marker = CircleMarker((coords[1], coords[0]), "#6bf414", 12)
    #add marker
    m.add_marker(marker_outline)
    m.add_marker(marker)
    #render the map and save it
    image = m.render(zoom=5)
    image.save("extensions/maps/"+ip+".png")
#Static Cog
class Static(commands.Cog):
    #init function to setup bot class
    def __init__(self, bot):
        self.bot=bot
    #help command
    @slash_command(description="Lists all the commands of the bot and their uses")
    async def help(self, ctx):
        embed=discord.Embed(title="Help & Important Info!", description="Lists all the commands and their uses! If you need more assistance, have found a bug, or have a suggestion, then please join the Support Server: [Join now!](https://discord.com/invite/8vNHAA36fR).", color=0x35d232)
        embed.set_thumbnail(url="https://me.technotalks.net/ProjectMSS.png")
        embed.add_field(name="__Commands__", value="`Ping`: Various stats of the bot \n`Developer`: Sends info about the developer of this bot\n`Status`: Get's the status of any MC Server\n`Latency`: Get's the latency to a minecraft server in *ms*\n`Server`: Get's the status of the set MC Server, *set by /serversetup*\n`Serversetup [*Admin ONLY Command*]`: This command is used to setup the guild specific features\n`Location`: Get the approximate location of a Minecraft server", inline=True)
        embed.add_field(name="\u200B", value=f"💻 Developed by TechnoTalks, Support Server: [Join now!](https://discord.com/invite/8vNHAA36fR), Thank you for using {self.bot.user.display_name}!", inline=False)
        await ctx.respond(embed=embed)
    #dev command self advertising go brrr
    @slash_command(description="Information about the developer!")
    async def dev(self, ctx):
        embed=discord.Embed(title="About the developer!", description="yea the guy who made this bot :D", color=0x00bfff)
        embed.set_author(name="TechnoTalks", url="https://me.technotalks.net/", icon_url="https://me.technotalks.net/PFP.png",)
        embed.set_thumbnail(url="https://me.technotalks.net/PFP.png")
        embed.add_field(name="About me!", value="I'm an aspiring developer who really loves tech! I love to develop things and its just fun for me (*Most of the time). I love to make new things and see that its being used by actual people! For more about me visit: https://me.technotalks.net/about.html!", inline=False)
        embed.add_field(name="Website", value="https://me.technotalks.net/ (or click on my name above :D)", inline=False)
        embed.add_field(name="Want your own bot?", value="Visit my site for more details on how to get your own bot! https://me.technotalks.net/services.html", inline=False)
        embed.set_footer(text="Thanks for reading!")
        await ctx.respond(embed=embed)

    @slash_command(description= "Get the Status of any Minecraft Server.")
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
            embed.add_field(name="IP: ", value="`{}`".format(data["ip"]))
            embed.add_field(name="Player Count:", value="`{}`".format(data["players"]["online"]), inline=True)
            embed.add_field(name="Version:", value="`{}`".format(data["version"]), inline=True)
            await ctx.respond(embed=embed)
    @status.error
    async def statuserror(self, ctx, error):
        await ctx.respond("Something went wrong...")
        raise error
    @slash_command(description="Get the latency to a Minecraft Server.")
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
    @latency.error
    async def latencyerror(self, ctx, error):
        await ctx.respond("Something went wrong...")
        raise error
    
    @slash_command(description="Get the aproximate location of a server!")
    async def location(self, ctx, ip: Option(str, "IP of the desired server", required=True)):
        await ctx.defer()
        url = "https://api.mcsrvstat.us/2/{}".format(ip)
        thing = requests.get(url)
        data = json.loads(thing.content)
        raw_ip = data["ip"]
        get_map(raw_ip)
        embed=discord.Embed(title=f"Approximate location of {ip}", description="Please note that proxies, and ip spoofing exists, so this location may not be accurate!", color=color)
        image=discord.File(f"extensions/maps/{raw_ip}.png")
        embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{ip}")
        embed.set_image(url=f"attachment://{raw_ip}.png")
        embed.set_footer(text="This is an approximate result and may not represent reality.")
        await ctx.respond(embed=embed, file=image)
        os.remove(f"extensions/maps/{raw_ip}.png")
    @location.error
    async def locationerror(self, ctx, error):
        await ctx.respond("> **Something went wrong...** 😭 Please make sure the server IP is correct. ")
        if isinstance(error, PermissionError):
            print("Image access 'denied' by windows (Command should be fine)")
        else:
            print(error)
            #raise error

def setup(bot):
    print("Loading extension Static")
    bot.add_cog(Static(bot))
def teardown(bot):
    print("Unloading extension Static")