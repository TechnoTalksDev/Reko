from inspect import Traceback
import colorama, discord, motor, asyncio, os, motor.motor_asyncio
from colorama import Fore
from dotenv import load_dotenv

colorama.init(True)

try:
    load_dotenv("src\secrets\.env")
except: pass

class ErrorLogger():
    def __init__(self, category = str, defaultMessage = "Uh oh, something went wrong"):
        self.category = category
        self.defaultMessage = defaultMessage

    def log(self, feature=None ,error=Exception, tracebackObject=Traceback, additionalContext = None):
        print(f"[{self.category}] {Fore.RED}{self.defaultMessage} {Fore.RESET}-> {Fore.BLUE}{feature} {Fore.RESET}| {Fore.BLACK}Error: {Fore.RED}{error} {Fore.RESET}| {Fore.LIGHTGREEN_EX}Line #: {Fore.RESET}{tracebackObject.tb_lineno} | {Fore.CYAN}Info: {additionalContext}")

def error_message():
    defaultMessage = "If the issue continues, **please report this** in our **[support server](https://discord.com/invite/8vNHAA36fR)**!"
    
    embed = discord.Embed(title = "❤️‍🔥 Uh oh something went wrong!", color=0xff1a1a)
    embed.add_field(name = "Please try again!", value = defaultMessage)

    return embed

def unreachable_server(ip):
    embed = discord.Embed(title = "❌ Server did not respond", color=0xff1a1a)
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
    