from inspect import Traceback
import colorama, discord, motor, asyncio, os, motor.motor_asyncio, socket
from colorama import Fore
from dotenv import load_dotenv

colorama.init(True)

load_dotenv("src/secrets/.env")

color = 0x6bf414

class ErrorLogger():
    def __init__(self, category = str, defaultMessage = "Uh oh, something went wrong"):
        self.category = category
        self.defaultMessage = defaultMessage

    def log(self, feature=None ,error=Exception, tracebackObject=Traceback, additionalContext = None):
        print(f"[{self.category}] {Fore.RED}{self.defaultMessage} {Fore.RESET}-> {Fore.BLUE}{feature} {Fore.RESET}| {Fore.BLACK}Error: {Fore.RED}{error} {Fore.RESET}| {Fore.LIGHTGREEN_EX}Line #: {Fore.RESET}{tracebackObject.tb_lineno} | {Fore.CYAN}Info: {additionalContext}")

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

    def default(status, motd = True, count = True, list = True, ip = True, version = True):
        motd = StatusCore.motd_cleanser(status.description)

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
