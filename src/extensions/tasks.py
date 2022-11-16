from asyncio import tasks
from pydoc import doc
import random, discord, datetime, motor, motor.motor_asyncio, os, sys, coloredlogs, logging, traceback, io, base64, time
import src.utilities as utilities
from discord.commands import slash_command
from discord.commands import Option
from discord.ext import commands, tasks
from dotenv import load_dotenv
from colorama import Fore
from mcstatus import JavaServer
import matplotlib.pyplot as plt

#intialize error_logger & error_message
coloredlogs.install(level="INFO", fmt="%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s")
logger = logging.getLogger("Reko")
file_handler = logging.FileHandler("SEVERE.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s"))
logger.addHandler(file_handler)

#intialize mongodb
db = utilities.Mongo().db

tracking_coll = db.tracking

botstats_coll = db.botstats

sp_coll = db.sp
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
        #self.track.start()
        self.status.start()
        self.bot_stats.start()
        self.panel.start()

    def cog_unload(self):
        #cancel tasks on cog unload
        self.tick.cancel()
        #self.track.cancel()
        self.status.cancel()
        self.bot_stats.cancel()
        self.panel.cancel()
    #Looped Tasks
    @tasks.loop(seconds=30.0)
    async def tick(self):
        tick = str(self.index)

        logger.info("Tick: "+tick+f" {round(self.bot.latency * 1000)}ms")

        self.index += 1
    #player tracking   
    @tasks.loop(seconds=10.0)
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
                #logger.info(f"{guild_id}, {ip}, {port}, {channel_id}")
            except:
                continue
            if channel == None:
                return
            #print(f"[Tasks] (Debug) IP:{ip}, Port: {port}, Port Type: {type(port)} ")
            
            try:
                server = JavaServer(ip, port, 4)
                status = await server.async_status()
                player_count = status.players.online
                logger.info("Got player count in tracking")
                try:
                    query = [True, await server.async_query()]
                except:
                    query = [False]
                    pass
                #logger.info(player_count)
            
            except Exception as e: 
                await channel.send(embed=utilities.ErrorMessage.unreachable_server(ip))
                #logger.info(f"Player Tracking failed to connect to server {ip}!")
                continue
            #player_count = info["players"]["online"]
            current = {guild_id: [player_count]}
            #logger.info(current)
            message = ""
            if guild_id in guild_cache:
                
                if player_count != guild_cache[guild_id][0]:

                    if player_count > guild_cache[guild_id][0]:
                        
                        if player_count - guild_cache[guild_id][0] == 1:
                            message = f"> A player has **joined** the server! 😁"

                        else:
                            players = player_count - guild_cache[guild_id][0]
                            message = f"> **{players}** players have **joined** the server! 😁"

                    elif player_count < guild_cache[guild_id][0]:

                        if guild_cache[guild_id][0] - player_count == 1:
                            message = f"> A player has **left** the server! 😢"
                        
                        else:
                            players = guild_cache[guild_id][0] - player_count
                            message = f"> **{players}** players have **left** the server! 😢"
                    
                    guild_cache.update(current)
                    async for last_message in channel.history(limit=10):
                        if last_message.author == self.bot.user:
                            break
                    try:
                        await last_message.edit(content=message)
                    except:
                        await channel.send(message)

            else:
                guild_cache.update(current)
    
    #Server panel
    @tasks.loop(seconds=20.0)
    async def panel(self):
        coll = sp_coll
        cursor = coll.find().sort([('_id', 1)])
        docs = await cursor.to_list(length=None)

        for guild in docs:
            try:
                guild_id = guild["_id"]
                ip = guild["ip"]
                port = guild["port"]
                channel_id = guild["channel"]
                data = guild["data"]
                channel = self.bot.get_channel(channel_id)
            except:
                await channel.send(embed=utilities.ErrorMessage.unreachable_server(ip))
                continue
            
            try:
                server = JavaServer.lookup(ip, 3)
                status = await server.async_status()
            except:
                await channel.send(embed=utilities.unreachable_server(ip))
                return
        
            embed = await utilities.StatusCore.default(ip, status, [False])
            plot_time = time.time()
            #charting and data
            plt.style.use(["dark_background", "fast"])
            fig, ax = plt.subplots()

            data.pop(0)
            data.append(status.players.online)
            findguild = await sp_coll.find_one({"_id": guild_id})
            if findguild:
                await sp_coll.delete_many(findguild)
            await sp_coll.insert_one({"_id": guild_id, "ip": ip, "channel": channel_id, "port": port, "data": data})
            
            a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            b = data

            for x, y in zip(a, b):
                if y != 0:
                    label = "{:.0f}".format(y)
                    plt.annotate(label, (x, y), textcoords="offset points", xytext=(0,10), ha="center")

            ax.plot(a, b, "#6bf414")
            ax.set_ylabel("Player Count")
            ax.set_xlabel("Last 10 minutes")
            buf = io.BytesIO()

            plt.savefig(buf, format="PNG")
            buf.seek(0)
            discord_chart = discord.File(fp=buf, filename="chart.png")
            #discord_chart = discord.File(io.BytesIO(chart.encode()), filename=f"chart.png")

            embed.set_image(url=f"attachment://chart.png")
            plot_time = str(round(time.time()-plot_time, 4)*1000)
            embed.set_footer(text = f"Rendered chart in {plot_time}ms")

            try:
                async for message in channel.history(limit=10):
                    if message.author == self.bot.user:
                        #await message.edit(embed=None)
                        await message.edit(embed=embed, file=discord_chart)
                        break
            except:
                pass

            #await channel.send(embed=embed)

    #status
    @tasks.loop(seconds=60.0)
    async def status(self):
        choice=random.randint(1,4)
        
        if choice == 1:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Beta Release 🤖"))
        
        elif choice == 2:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="LoFi"))
        
        elif choice ==  3:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Minecraft Servers"))
        
        else:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Minecraft"))
   
    #Push bot stats to mongodb
    @tasks.loop(minutes = 3)
    async def bot_stats(self):
        coll = botstats_coll
        findguild= await coll.find_one({"_id": self.bot.application_id})
        
        if findguild:
            await coll.delete_many(findguild)
        users = 0
        for guild in self.bot.guilds:
            users += guild.member_count
        
        commands_run = None

        logger.info(f"Uploading bot stats... guild_count: {len(self.bot.guilds)}, users: {users}, commands_run: {commands_run} ")
        await coll.insert_one({"_id": self.bot.application_id, "guild_count": len(self.bot.guilds), "users": users, "commands_run": commands_run})
    
    @tick.before_loop
    async def before_tick(self):
        await self.bot.wait_until_ready()
    @tick.error
    async def tickerror(self, error):
        logger.critical("TICK TASK HAS FAILED")
        logger.critical(traceback.format_exc())
        return
    """
    @track.before_loop
    async def before_track(self):
        await self.bot.wait_until_ready()
    @track.error
    async def trackerror(self, error):
        logger.error("Error in tracking")
        logger.error(traceback.format_exc())
        return
    """
    @status.before_loop
    async def before_status(self):
        await self.bot.wait_until_ready()
    @status.error
    async def statuserror(self, error):
        logger.error("Error in updating Status")
        logger.error(traceback.format_exc())
        return

    @bot_stats.before_loop
    async def before_bot_stats(self):
        await self.bot.wait_until_ready()
    @bot_stats.error
    async def bot_statuserror(self, error):
        logger.error("Error in uploading bot stats")
        logger.error(traceback.format_exc())
        return

    @panel.before_loop
    async def before_panel(self):
        await self.bot.wait_until_ready()
    @panel.error
    async def bot_panel(self, error):
        logger.error("Error in uploading bot stats")
        logger.error(traceback.format_exc())
        return

def setup(bot):
    logger.info("Extension [Tasks] loading...")
    bot.add_cog(tasksCog(bot))
def teardown(bot):
    logger.info("Extension [Tasks] unloading...")