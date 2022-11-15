from inspect import Traceback
import colorama, discord, motor, asyncio, os, motor.motor_asyncio, socket
from colorama import Fore
from dotenv import load_dotenv
from mcstatus import JavaServer

colorama.init(True)

load_dotenv("src/secrets/.env")

color = 0x6bf414

class ErrorMessage():
    def default():
        defaultMessage = "If the issue continues, **please report this** in our **[support server](https://discord.com/invite/8vNHAA36fR)**!"
        
        embed = discord.Embed(title = "❤️‍🔥 Uh oh something went wrong!", color=0xff1a1a)
        embed.add_field(name = "Please try again!", value = defaultMessage)

        return embed

    def unreachable_server(ip):
        embed = discord.Embed(title = "❌ Offline Server", color=0xff1a1a)
        embed.set_thumbnail(url="https://www.technotalks.net/static/main/images/offline_icon.png")
        embed.add_field(name = f"{ip} is unreachable", value = "The server may **be offline** or may **not exist**")
        embed.add_field(name = "Please try again", value = "If you think this is an error and, if the issue continues, **please report this** in our **[support server](https://discord.com/invite/8vNHAA36fR)**!", inline=False)
        return embed

class Mongo():
    def __init__(self):
        mongo_link=os.getenv("MONGO_LINK")
        
        cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_link, connect=True, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)

        self.db = cluster.reko

    def get_collection(self, collection_name:str):
        try: 
            coll = self.db[collection_name]
            return coll
        except:
            return None

class StatusCore():
    def motd_cleanser(motd:str):
        mc_codes = ["§0", "§1", "§2", "§3", "§4", "§5", "§6", "§7", "§8", "§9", "§a", "§b", "§c", "§d", "§e", "§f","§g", "§l", "§n", "§k"]
        
        for code in mc_codes:
            motd = motd.replace(code, "")

        motd = motd.replace(" ", "‎ ")

        return motd

    async def getLatency(ip):
        try:
            server = JavaServer.lookup(ip, 10)
            status = await server.async_status()
            ping = status.latency
            return ping
        except Exception as e:
            return

    async def default(ip, status, query):
        motd = StatusCore.motd_cleanser(status.description)

        embed=discord.Embed(title=f"✅ {ip}", description=f"**{motd}**",color=color)    
        embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{ip}")
        #-------------------------------without query-------------------------------------
        if True != query[0]:
            embed.add_field(name="Player Count:", value=f"`{status.players.online}/{status.players.max}`", inline=True)
            
            latency_result = await StatusCore.getLatency(ip)
            if latency_result != None:
                embed.add_field(name="Latency/Ping", value=f"`{round(latency_result, 2)}ms`", inline=True)

            if status.players.sample != None and status.players.sample != []:
                player_list=""
                
                for player in status.players.sample:
                    player_list += player.name.replace(".", "")+", "
                
                embed.add_field(name="Player list:", value=f"`{player_list[:-2]}`", inline=True)

            try:
                ip_addr = socket.gethostbyname(ip)
                embed.add_field(name="IP: ", value=f"`{ip_addr}`", inline=True)
            except: pass
            
            embed.add_field(name="Version:", value=f"`{status.version.name}`", inline=True)
            embed.add_field(name="Query:", value=f"`{query[0]}`")
        #------------------------------------------------------------------------------------
        else:
            embed.add_field(name="Player Count:", value=f"`{query[1].players.online}/{query[1].players.max}`", inline=True)
            
            latency_result = await StatusCore.getLatency(ip)
            if latency_result != None:
                embed.add_field(name="Latency/Ping", value=f"`{round(latency_result, 2)}ms`", inline=True)

            if query[1].players.names != None and query[1].players.names != []:
                player_list=""
                
                for player in query[1].players.names:
                    player_list += player.name.replace(".", "")+", "
                
                embed.add_field(name="Player list:", value=f"`{player_list[:-2]}`", inline=True)
            try:
                ip_addr = socket.gethostbyname(ip)
                embed.add_field(name="IP: ", value=f"`{ip_addr}`", inline=True)
            except: pass
            
            embed.add_field(name="Version:", value=f"`{status.version.name}`", inline=True)

            embed.add_field(name="Query:", value=f"`{query[0]}`")

            plugins = ""
            for plugin in query[1].software.plugins:
                plugins += plugin+", "

            embed.add_field(name="Plugins", value=f"`{plugins}`")

        return embed
