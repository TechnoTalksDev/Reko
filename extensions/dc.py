import discord
from discord.commands import slash_command , Option
from discord.ext import commands
from discord.ui import Button, View
from discord.ext.commands import MissingPermissions
import json, requests, motor, motor.motor_asyncio
#from main import guilds

#mongodb setup
with open("./secrets/mongo_password", "r") as f:
    mongo_password = f.read().strip()
cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://TechnoTalks:"+mongo_password+"@main.rpbbi.mongodb.net/discord?retryWrites=true&w=majority")
db=cluster.discord
collection=db.reko

color=0x6bf414


class resetView(View):
    def __init__(self, data, ctx):
        super().__init__(timeout=15)
        self.data=data
        self.ctx=ctx
    
    @discord.ui.button(label="Reset", style=discord.ButtonStyle.danger, emoji="<:reset:941872105618812978>")
    async def button_callback(self, button, interaction):
        await collection.delete_many(self.data)
        await interaction.response.edit_message(content="Previously stored IP cleared!", view=None)
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.ctx.interaction.edit_original_message(content="You have already setup an ip... Hit the reset button bellow (*The button has expired please run the command again*) or, run this command again with `reset` as the ip value, to clear the stored ip.", view=self)

class dc(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @slash_command(description="Setup MSS for your server!")
    @commands.has_permissions(administrator=True)
    async def serversetup(self, ctx, ip: Option(str, "The ip of the server.", required=False), channel: Option(str, "Channel for updating chart.", required=False)):
        if ip==None:
            embed=discord.Embed(title="A simple Minecraft Server Status bot! ", color=color)
            embed.set_thumbnail(url="https://me.technotalks.net/ProjectMSS.png")
            embed.set_author(name=f"Welcome to {self.bot.user.display_name}!")
            embed.add_field(name="/server ", value="To setup this command please run this command and provide an ip for the desired server. (ex. `/serversetup ip:mc.hypixel.net` )", inline=True)
            embed.add_field(name="Updating Chart", value="Coming Soon!", inline=False)
            await ctx.respond(embed=embed)
        else:
            sid=ctx.guild_id
            findguild= await collection.find_one({"_id": sid})
            if not findguild:
                await collection.insert_one({"_id":sid, "mcip": ip})
                await ctx.respond("The server command is setup!")
            elif ip=="reset":
                await collection.delete_many(findguild)
                await ctx.respond("Previously stored IP cleared!")
            else:
                view=resetView(findguild, ctx)
                await ctx.respond("You have already setup an ip... Hit the reset button bellow or, run this command again with `reset` as the ip value, to clear the stored ip.", view=view)
    @serversetup.error
    async def serversetuperror(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond(f"You are missing the required permission: **{error.missing_permissions[0].capitalize()}**, to run this command!")
        else:
            await ctx.respond("Something went wrong...")
            raise error
    @slash_command(description="Get's status of hotkeyed server!")
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