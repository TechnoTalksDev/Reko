import discord, requests, json, geocoder, os, socket, sys, io
import src.utilities as utilities
from discord.commands import slash_command
from discord.ext import commands
from discord.commands import Option
from mcstatus import JavaServer
from staticmap import StaticMap, CircleMarker
#from main import guilds
#color of bot
color=0x6bf414
#function to get server latency
async def latencyraw(ip):
    try:
        server = JavaServer.lookup(ip, 10)
        status = await server.async_status()
        ping = status.latency
        return ping
    except Exception as e:
        return
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
    
    with io.BytesIO() as image_binary:
        image.save(image_binary, format="PNG")
        image_binary.seek(0)
        discord_image=discord.File(fp=image_binary, filename="image.png")
    return coords, discord_image
#General Cog
class General(commands.Cog):
    
    #init function to setup bot instance
    def __init__(self, bot):
        self.bot=bot
    
    #help command
    @slash_command(description="Lists all the commands of the bot and their uses")
    async def help(self, ctx):
        embed=discord.Embed(title="Help & Important Info!", description="Lists all the commands and their uses! If you need more assistance, have found a bug, or have a suggestion, then please join the Support Server: [Join now!](https://discord.com/invite/8vNHAA36fR).", color=0x35d232)
        
        embed.set_thumbnail(url="https://www.technotalks.net/ProjectMSS.png")
        
        embed.add_field(name="__Commands__", value="`Ping`: Various stats of the bot \n`Developer`: Sends info about the developer of this bot\n`Status`: Gets the status of any MC Server\n`Latency`: Gets the latency to a minecraft server in *ms*\n`Server`: Gets the status of the set MC Server, *set by /setup*\n`Setup [*Admin ONLY Command*]`: This command is used to setup the guild specific features\n`Location`: Get the approximate location of a Minecraft server", inline=True)
        
        embed.add_field(name="\u200B", value=f"💻 Developed by TechnoTalks, Support Server: [Join now!](https://discord.com/invite/8vNHAA36fR), Thank you for using {self.bot.user.display_name}!", inline=False)
        
        await ctx.respond(embed=embed)
    @help.error
    async def help_error(self, ctx, error):
        #tell the user their was an error
        await ctx.respond("> **Something went wrong...** 😭 Please try again!")
        #log the error and line number
        print(f"[General] Help command error: {error}, Line #: {sys.exc_info()[-1].tb_lineno}")
    #dev command self advertising go brrr
    @slash_command(description="Information about the developer!")
    async def dev(self, ctx):
        embed=discord.Embed(title="O whats this...", description="yea the guy who made this bot :D", color=0x00bfff)
        
        embed.set_author(name="TechnoTalks", url="https://www.technotalks.net/", icon_url="https://www.technotalks.net/static/main/images/TT.png",)
        
        embed.set_thumbnail(url="https://www.technotalks.net/static/main/images/TT.png")
        
        embed.add_field(name="Website", value="https://www.technotalks.net/ (or click on my name above :D)", inline=False)
        
        embed.add_field(name="Want your own bot?", value="I make custom discord bot's so if you would like one head to [my site](https://www.technotalks.net/)!", inline=False)
        
        embed.set_footer(text="Thanks for reading!")
        await ctx.respond(embed=embed)
    @dev.error
    async def dev_error(self, ctx, error):
        #tell the user their was an error
        await ctx.respond("> **Something went wrong...** 😭 Please try again!")
        #log the error and line number
        print(f"[General] Dev command error: {error}, Line #: {sys.exc_info()[-1].tb_lineno}")
    #status command
    @slash_command(description= "Get the Status of any Minecraft Server.")
    async def status(self, ctx, ip: Option(str, "The ip of the server.", required=True)):
        await ctx.defer()
        
        try:
            server = JavaServer.lookup(ip, 3)
            status = await server.async_status()

        except:
            await ctx.respond(embed=utilities.unreachable_server(ip))
            return
        
        #get motd
        mc_codes = ["§0", "§1", "§2", "§3", "§4", "§5", "§6", "§7", "§8", "§9", "§a", "§b", "§c", "§d", "§e", "§f","§g", "§l", "§n", "§k"]
        motd = status.description
        
        for code in mc_codes:
            motd = motd.replace(code, "")
        motd = motd.replace(" ", "‎ ")
        print(motd)

        embed=discord.Embed(title=f"✅ {ip}", description=f"**{motd}**",color=color)
        embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{ip}")
        
        embed.add_field(name="Player Count:", value=f"`{status.players.online}/{status.players.max}`", inline=False)
        
        if status.players.sample != None and status.players.sample != []:
            player_list=""
            
            for player in status.players.sample:
                player_list += player.name.replace(".", "")+", "
            
            embed.add_field(name="Player list:", value=f"`{player_list[:-2]}`", inline=False)

        try:
            ip_addr = socket.gethostbyname(ip)
            embed.add_field(name="IP: ", value=f"`{ip_addr}`")
        except: pass
        
        embed.add_field(name="Version:", value=f"`{status.version.name}`", inline=True)
        
        await ctx.respond(embed=embed)
    @status.error
    async def statuserror(self, ctx, error):
        #tell the user their was an error
        await ctx.respond("> **Something went wrong...** 😭 Please make sure the server IP is correct. ")
        #log the error and line number
        print(f"[General] Status command error: {error}, Line #: {sys.exc_info()[-1].tb_lineno}")

    @slash_command(description="Get the latency to a Minecraft Server.")
    async def latency(self, ctx: discord.ApplicationContext, ip: Option(str, "IP of the MC server", required=True)):
        await ctx.defer()
        
        result= await latencyraw(ip)
        
        if result == None:
            embed=discord.Embed(title="Error", description="This server does not exist or is offline", color=0xff1a1a)
            
            await ctx.respond(embed=embed)
        
        else:
            embed=discord.Embed(title=f"Latency to {ip}", description=f"{result}"+"ms", color=color)
            
            embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{ip}")
            
            embed.add_field(name="Note:", value="This result is the latency from the bot to the server.", inline=True)
            
            await ctx.respond(embed=embed)
    @latency.error
    async def latencyerror(self, ctx, error):
        #tell the user their was an error
        await ctx.respond("> **Something went wrong...** 😭 Please make sure the server IP is correct. ")
        #log the error and line number
        print(f"[General] Latency command error: {error}, Line #: {sys.exc_info()[-1].tb_lineno}")
    
    @slash_command(description="Get the aproximate location of a server!")
    async def location(self, ctx, ip: Option(str, "IP of the desired server", required=True)):
        await ctx.defer()
        
        #get ip of the server
        raw_ip = socket.gethostbyname(ip)
        
        #generate map and store coords and image file
        map = get_map(raw_ip)
        coords = map[0]
        image = map[1]
        #create embed
        embed=discord.Embed(title=f"Approximate location of {ip}", color=color)
        
        embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{ip}")
        
        embed.add_field(name="Latitude & Longitude", value=f"__Lat__: {coords[0]} __Long__: {coords[1]}")
        
        embed.set_image(url=f"attachment://image.png")
        
        embed.set_footer(text="Please note that proxies, and ip spoofing exists, so this location may not be accurate!")
        
        #send embed
        await ctx.respond(embed=embed, file=image)
        #clean up
        image.close() #Dosent seem to affect memory usuage?
    @location.error
    async def locationerror(self, ctx, error):
        #tell the user their was an error
        await ctx.respond("> **Something went wrong...** 😭 Please make sure the server IP is correct. ")
        #log the error and line number
        print(f"[General] Location command error: {error}, Line #: {sys.exc_info()[-1].tb_lineno}")
    
def setup(bot):
    print("[General] Loading extension...")
    bot.add_cog(General(bot))
def teardown(bot):
    print("[General] Unloading extension...")