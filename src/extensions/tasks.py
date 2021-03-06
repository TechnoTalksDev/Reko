from asyncio import tasks
from pydoc import doc
import random, discord, datetime, motor, motor.motor_asyncio, os, sys
import src.utilities as utilities
from discord.commands import slash_command
from discord.commands import Option
from discord.ext import commands, tasks
from dotenv import load_dotenv
from colorama import Fore
from mcstatus import JavaServer

#intialize error_logger & error_message
error_logger = utilities.ErrorLogger("Tasks")

#intialize mongodb
db = utilities.Mongo().db

tracking_coll = db.tracking

botstats_coll = db.botstats
#bot accent color
color=0x6bf414
#cache for tracking
guild_cache = {
    "Example": [datetime.datetime.now, ["TechnoTalks, garvinator123"]]
}


class tasksCog(commands.Cog):
    #init function
    def __init__(self, bot):
        self.bot = bot
        #ticks from start counter
        self.index = 0
        #self.{name of async looped function}
        self.tick.start()
        self.track.start()
        self.status.start()
        self.bot_stats.start()

    def cog_unload(self):
        #cancel tasks on cog unload
        self.tick.cancel()
        self.track.cancel()
        self.status.cancel()
        self.bot_stats.cancel()
    #Looped Tasks
    @tasks.loop(seconds=30.0)
    async def tick(self):
        tick = str(self.index)
        
        print("\n[Reko] {"+datetime.datetime.now().strftime("%H:%M:%S")+"} Tick: "+tick+f" {round(self.bot.latency * 1000)}ms")

        self.index += 1
    #player tracking   
    @tasks.loop(seconds=5.0)
    async def track(self):
        coll = tracking_coll
        cursor = coll.find().sort([('_id', 1)])
        docs = await cursor.to_list(length=None)

        for guild in docs:
            try:
                guild_id = guild["_id"]
                ip = guild["trackip"]
                port = guild["trackport"]
                channel_id = guild["trackchannel"]
                channel =  self.bot.get_channel(channel_id)
            except:
                continue
            if channel == None:
                return
            #print(f"[Tasks] (Debug) IP:{ip}, Port: {port}, Port Type: {type(port)} ")
            
            try:
                server = JavaServer(ip, port, 4)
                status = await server.async_status()
                player_count = status.players.online
            
            except Exception as e: 
                await channel.send(embed=utilities.ErrorMessage.error_message())
                error_logger.log("Player Tracking", e, sys.exc_info()[-1], "Failed to connect to server")
                continue
            #player_count = info["players"]["online"]
            current = {guild_id: [player_count]}
            
            if guild_id in guild_cache:
                
                if player_count != guild_cache[guild_id][0]:

                    if player_count > guild_cache[guild_id][0]:
                        
                        if player_count - guild_cache[guild_id][0] == 1:
                            await channel.send(f"> A player has **joined** the server! ????")

                        else:
                            players = player_count - guild_cache[guild_id][0]
                            await channel.send(f"> **{players}** players have **joined** the server! ????")

                    elif player_count < guild_cache[guild_id][0]:

                        if guild_cache[guild_id][0] - player_count == 1:
                            await channel.send(f"> A player has **left** the server! ????")
                        
                        else:
                            players = guild_cache[guild_id][0] - player_count
                            await channel.send(f"> **{players}** players have **left** the server! ????")
                    
                    guild_cache.update(current)

            else:
                guild_cache.update(current)
    #status
    @tasks.loop(seconds=60.0)
    async def status(self):
        choice=random.randint(1,4)
        
        if choice == 1:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Beta Release ????"))
        
        elif choice == 2:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="LoFi"))
        
        elif choice ==  3:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Minecraft Servers"))
        
        else:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Minecraft"))
   
    #Push bot stats to mongodb
    @tasks.loop(seconds=30.0)
    async def bot_stats(self):
        coll = botstats_coll
        findguild= await coll.find_one({"_id": self.bot.application_id})
        
        if findguild:
            await coll.delete_many(findguild)
        
        await coll.insert_one({"_id": self.bot.application_id, "guild_count": len(self.bot.guilds), "users": len(self.bot.users), "commands_run": "Unknown"})
    
    @tick.before_loop
    async def before_tick(self):
        await self.bot.wait_until_ready()
    @tick.error
    async def tickerror(self, error):
        error_logger.log("Tick", error, sys.exc_info()[-1])
        return
    
    @track.before_loop
    async def before_track(self):
        await self.bot.wait_until_ready()
    @track.error
    async def trackerror(self, error):
        error_logger.log("Tracking", error, sys.exc_info()[-1])
        return
    
    @status.before_loop
    async def before_status(self):
        await self.bot.wait_until_ready()
    @status.error
    async def statuserror(self, error):
        error_logger.log("Status", error, sys.exc_info()[-1])
        return

    @bot_stats.before_loop
    async def before_bot_stats(self):
        await self.bot.wait_until_ready()
    @bot_stats.error
    async def bot_statuserror(self, error):
        error_logger.log("Bot Stats", error, sys.exc_info()[-1])
        return

def setup(bot):
    print("[Tasks] Loading extension...")
    bot.add_cog(tasksCog(bot))
def teardown(bot):
    print("[Tasks] Unloading extension...")