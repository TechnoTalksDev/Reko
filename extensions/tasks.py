from asyncio import tasks
import discord
from discord.commands import slash_command
from discord.commands import Option
from discord.ext import commands, tasks

guilds=[846192394214965268]

color=0x6bf414

class tasksCog(commands.Cog):
    #init function
    def __init__(self, bot):
        #ticks from start counter
        self.index = 0
        self.bot = bot
        #self.{name of async looped function}
        self.tick.start()

    def cog_unload(self):
        #cancel tasks on cog unload
        self.tick.cancel()
    #Looped Tasks
    @tasks.loop(seconds=15.0)
    async def tick(self):
        channel_id=923308480847282236
        channel = self.bot.get_channel(channel_id)
        tick = str(self.index)
        await channel.send("Tick: "+tick+"\n"+f"{round(self.bot.latency * 1000)}ms")
        #print(channel)
        self.index += 1
    #Make sure to wait before bot start to begin looping tasks
    @tick.before_loop
    async def before_tick(self):
        print('Waiting for bot start...')
        await self.bot.wait_until_ready()

def setup(bot):
    print("Loading extension Tasks...")
    bot.add_cog(tasksCog(bot))
def teardown(bot):
    print("Unloading extension Tasks")