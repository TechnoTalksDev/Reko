import discord, json, requests, motor, motor.motor_asyncio, os
from pkg_resources import require
from discord.commands import slash_command , Option
from discord.ext import commands
from discord.ui import Button, View
from discord.ext.commands import MissingPermissions
from dotenv import load_dotenv
#mongodb setup
try:
    load_dotenv("src\secrets\.env")
except: pass
mongo_password=os.getenv("MONGO_PASSWORD")
cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://TechnoTalks:"+mongo_password+"@main.rpbbi.mongodb.net/reko?retryWrites=true&w=majority")
db = cluster.reko
hotkey_coll = db.hotkey
tracking_coll = db.tracking
uc_coll = db.uc

color=0x6bf414


class resetView(View):
    def __init__(self, data, ctx, value):
        super().__init__(timeout=15)
        self.data=data
        self.ctx=ctx
        self.value=value
    
    @discord.ui.button(label="Reset", style=discord.ButtonStyle.danger, emoji="<:reset:941872105618812978>")
    async def button_callback(self, button, interaction):
        if self.value == "track":
            await tracking_coll.delete_many(self.data)
        await interaction.response.edit_message(content="Previously stored configuration cleared! Please run the setup command again...", view=None)
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.ctx.interaction.edit_original_message(content="You have already setup this feature... Hit the reset button bellow (*The button has expired please run the command again*)", view=self)

class setupModal(discord.ui.Modal):
    def __init__(self, ctx, feature, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ctx = ctx
        self.feature = feature
        if self.feature == "/server":
            self.add_item(discord.ui.InputText(label="Hotkeyed server for /server command"))
        elif self.feature == "Tracking":
            self.add_item(discord.ui.InputText(label="IP to track joins, playtime, and leaves"))
            self.add_item(discord.ui.InputText(label="Port of the server", value="25565"))
            self.add_item(discord.ui.InputText(label="Name of the channel to send tracking messages"))
        else:
            self.add_item(discord.ui.InputText(label="Server ip for updating chart"))

    async def callback(self, interaction: discord.Interaction):
        sid=interaction.guild_id
        if self.feature == "/server":
            findguild= await hotkey_coll.find_one({"_id": sid})
            if not findguild:
                await hotkey_coll.insert_one({"_id":sid, "mcip": self.children[0].value})
                await interaction.response.send_message("The server command is setup!")
            else:
                view=resetView(findguild, self.ctx)
                await interaction.response.send_message("You have already setup this feature... Hit the reset button bellow to clear the configuration of the selected feature.", view=view)
        elif self.feature == "Tracking":
            findguild= await tracking_coll.find_one({"_id": sid})
            if not findguild:
                channel = discord.utils.get(interaction.guild.channels, name=self.children[2].value)
                try:
                    channel_id = channel.id
                    await tracking_coll.insert_one({"_id":sid, "trackip": self.children[0].value, "trackchannel": channel_id, "trackport": int(self.children[1].value)})
                    await interaction.response.send_message(f"Tracking server `{self.children[0].value}:{self.children[1].value}` in <#{channel_id}>")
                except AttributeError:
                    await interaction.response.send_message("> Please provide a **valid channel name**! 😭\n> *(Valid channel names do not include the # ex. 'tracking' NOT '#tracking')*")
            else:
                view=resetView(findguild, self.ctx, "track")
                await interaction.response.send_message("You have already setup this feature... Hit the reset button bellow to clear the configuration of the selected feature.", view=view)
        

class setupView(View):
    def __init__(self, ctx):
        super().__init__(timeout=15)
        self.ctx=ctx
        self.feature = None

    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a feature to setup!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maxmimum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="/server",
                description="Easily get the status of this server"
            ),
            discord.SelectOption(
                label="Tracking",
                description="Track joins and leaves of a server"
            ),
            discord.SelectOption(
                label="Updating chart",
                description="View an chart of your selected server"
            )
        ]
    )
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        self.feature = select.values[0]

    @discord.ui.button(label="Setup", style=discord.ButtonStyle.success, emoji="⚙️")
    async def button_callback(self, button, interaction):
        if self.feature is not None:
            if self.feature == "/server":
                findguild= await hotkey_coll.find_one({"_id": interaction.guild_id})
                if findguild:
                    view=resetView(findguild, self.ctx)
                    await interaction.response.send_message("You have already setup this feature... Hit the reset button bellow to clear the configuration of the selected feature.", view=view)
                else:
                    button.disabled = True
                    await self.ctx.interaction.edit_original_message(view = self)
                    await interaction.response.send_modal(setupModal(ctx=self.ctx, feature=self.feature, title="Reko Setup"))
            elif self.feature == "Tracking":
                findguild= await tracking_coll.find_one({"_id": interaction.guild_id})
                if findguild:
                    view=resetView(findguild, self.ctx, "track")
                    await interaction.response.send_message("You have already setup this feature... Hit the reset button bellow to clear the configuration of the selected feature.", view=view)
                else:
                    button.disabled = True
                    await self.ctx.interaction.edit_original_message(view = self)
                    await interaction.response.send_modal(setupModal(ctx=self.ctx, feature=self.feature, title="Reko Setup"))
        else:
            await interaction.response.send_message("Please select the feature you would like to setup first!")
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.ctx.interaction.edit_original_message(view=self)

class dc(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @slash_command(description="Setup Reko for your server!")
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        embed=discord.Embed(title="A simple Minecraft Server Status bot! ", color=color)
        embed.set_thumbnail(url="https://me.technotalks.net/ProjectMSS.png")
        embed.set_author(name=f"Welcome to {self.bot.user.display_name}!")
        embed.add_field(name="/server ", value="Please hit the setup button bellow to setup this command... To setup this command manually please run this command and provide an ip for the desired server. (ex. `/setup ip:mc.hypixel.net` )", inline=True)
        embed.add_field(name="Tracking", value="Track player !", inline=False)
        embed.add_field(name="Updating Chart", value="Coming Soon!", inline=False)
        view=setupView(ctx)
        await ctx.respond(embed=embed, view=view)
    @setup.error
    async def setuperror(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond(f"You are missing the required permission: **{error.missing_permissions[0].capitalize()}**, to run this command!")
        else:
            await ctx.respond("Something went wrong...")
            raise error
    @slash_command(description="Get's status of hotkeyed server!")
    async def server(self, ctx):
        inputid=ctx.guild_id
        #sip=read_json(inputid)
        findguild=await hotkey_coll.find_one({"_id":inputid})

        if not findguild:
           await ctx.respond("This command has not been setup properly please ask the admins to run /setup to setup this command!")    
        else:
            try:
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
                    embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{sip.strip()}")
                    embed.add_field(name="IP: ", value="`{}`".format(data["ip"]))
                    embed.add_field(name="Player Count:", value="`{}`".format(data["players"]["online"]), inline=True)
                    embed.add_field(name="Version:", value="`{}`".format(data["version"]), inline=True)
                    try:
                        player_list = ""
                        for i in data["players"]["list"]:
                            player_list = player_list + f"{i}, "
                        embed.add_field(name="Player list:", value="`{}`".format(player_list[:-2]), inline=False)
                    except: 
                        pass
                    await ctx.respond(embed=embed)
            except KeyError:
                await ctx.respond("This command has not been setup properly please ask the admins to run /setup to setup this command!")

    @server.error
    async def servererror(self, ctx, error):
        await ctx.respond("Something went wrong...")
        raise error
def setup(bot):
    print("[DataCommands] Loading extension...")
    bot.add_cog(dc(bot))
def teardown(bot):
    print("[DataCommands] Unloading extension...")