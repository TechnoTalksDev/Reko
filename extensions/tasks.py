from asyncio import tasks
import random
import discord
from discord.commands import slash_command
from discord.commands import Option
from discord.ext import commands, tasks

color=0x6bf414

class tasksCog(commands.Cog):
    #init function
    def __init__(self, bot):
        self.bot = bot
        #ticks from start counter
        self.index = 0
        #self.{name of async looped function}
        self.tick.start()
        self.chart.start()
        self.status.start()

    def cog_unload(self):
        #cancel tasks on cog unload
        self.tick.cancel()
        self.chart.cancel()
        self.status.cancel()
    #Looped Tasks
    @tasks.loop(seconds=30.0)
    async def tick(self):
        channel_id=923308480847282236
        channel = self.bot.get_channel(channel_id)
        tick = str(self.index)
        await channel.send("Tick: "+tick+"\n"+f"{round(self.bot.latency * 1000)}ms")
        self.index += 1
    @tasks.loop(seconds=30.0)
    async def chart(self):
        channel_id=939974897025810464
        channel = self.bot.get_channel(channel_id)
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
    #Make sure to wait before bot start to begin looping tasks
    @tick.before_loop
    async def before_tick(self):
        #print('Waiting for bot start...')
        await self.bot.wait_until_ready()
    @tick.error
    async def tickerror(self):
        print("[Tick]: Error in tick task. Most probably a awaiting error.")
    @chart.before_loop
    async def before_chart(self):
        #print('Waiting for bot start...')
        await self.bot.wait_until_ready()
    @chart.error
    async def charterror(self):
        print("[Chart]: Error in chart task. Most probably a awaiting error.")
    @status.before_loop
    async def before_status(self):
        await self.bot.wait_until_ready()
    @status.error
    async def statuserror(self):
        print("[Status]: Error in status task. Most probably a awaiting error.")

def setup(bot):
    print("Loading extension Tasks...")
    bot.add_cog(tasksCog(bot))
def teardown(bot):
    print("Unloading extension Tasks")