import discord
from discord.commands import slash_command , Option
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import json
import requests
import motor
import motor.motor_asyncio
from main import guilds

#mongodb setup
cluster = motor.motor_asyncio.AsyncIOMotorClient("10.0.0.210", 27017)
db=cluster.discord
collection=db.mss

color=0x6bf414

class dc(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @slash_command(guild_ids=guilds, description="Setup your custom server hotkey!")
    @commands.has_permissions(administrator=True)
    async def serversetup(self, ctx, ip: Option(str, "The ip of the server.", required=True)):
        sid=ctx.guild_id
        findguild= await collection.find_one({"_id": sid})
        if not findguild:
            await collection.insert_one({"_id":sid, "mcip": ip})
            await ctx.respond("The server command is setup!")
        elif ip=="reset":
            await collection.delete_many(findguild)
            await ctx.respond("Previously stored IP cleared!")
        else:
            await ctx.respond("You have already setup an ip... Run this command again with `reset` as the ip value to clear the stored ip.")
    @serversetup.error
    async def serversetuperror(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond(f"You are missing the required permission: **{error.missing_permissions[0].capitalize()}**, to run this command!")
        else:
            await ctx.respond("Something went wrong...")
            raise error
    @slash_command(guild_ids=guilds, description="Get's status of hotkeyed server!")
    async def server(self, ctx):
        inputid=ctx.guild_id
        #sip=read_json(inputid)
        findguild=await collection.find_one({"_id":inputid})
        if not findguild:
           await ctx.respond("This command has not been setup properly please ask the admins to run /serversetup to setup this command!")    
        else:
            sip=findguild["mcip"]
            url = "https://api.mcsrvstat.us/2/{}".format(sip)
            thing = requests.get(url)
            data = json.loads(thing.content)
            if data["online"] == False:
                embed=discord.Embed(title=f"IP Error: {sip}", description="This server either does not exist or is not online. If you think this is an error, then please join the support server to report this!", color=0xff1a1a)
                await ctx.respond(embed=embed)
            else:
                motd=""
                for i in range(len(data["motd"]["clean"])):
                    motd+=data["motd"]["clean"][i]
                embed=discord.Embed(title="Status of {}".format(sip), description="{}".format(motd),color=color)
                embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{sip}")
                embed.add_field(name="Online:", value="{}".format(data["online"]), inline=True)
                embed.add_field(name="Player Count:", value="{}".format(data["players"]["online"]), inline=True)
                embed.add_field(name="Version:", value="{}".format(data["version"]), inline=True)
                await ctx.respond(embed=embed)
    @server.error
    async def servererror(self, ctx, error):
        await ctx.respond("Something went wrong...")
        raise error
def setup(bot):
    print("Loading extension DataCommands...")
    bot.add_cog(dc(bot))
def teardown(bot):
    print("Unloading extension DataCommands...")