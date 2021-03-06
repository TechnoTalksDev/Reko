import discord, json, requests, motor, motor.motor_asyncio, os, socket, sys
import src.utilities as utilities
from pkg_resources import require
from discord.commands import slash_command , Option
from discord.ext import commands
from discord.ui import Button, View
from discord.ext.commands import MissingPermissions
from dotenv import load_dotenv
from mcstatus import JavaServer
#error logger
error_logger = utilities.ErrorLogger("Custom Commands")
#intialize mongodb
db = utilities.Mongo().db

hotkey_coll = db.hotkey
tracking_coll = db.tracking
uc_coll = db.uc

#accent color
color=0x6bf414

features = [
    {"name": "player_tracking", "friendly_name": "Tracking", "db": tracking_coll, "description": "**Track player joins and leaves** of your set server! (Player names coming soon!)"}, 
    {"name": "server_command", "friendly_name": "/server", "db": hotkey_coll, "description": "Easily check the status of the set server **without having to manually type the ip** every time!"},
    {"name": "uc", "friendly_name": "Updating Chart", "db": uc_coll, "description": "**Coming Soon!**"}]

class resetView(View):
    def __init__(self, data, ctx, value):
        super().__init__(timeout=15)
        self.data=data
        self.ctx=ctx
        self.value=value
    
    @discord.ui.button(label="Reset", style=discord.ButtonStyle.danger, emoji="<:reset:941872105618812978>")
    async def reset_button_callback(self, button, interaction):
        if self.value == "Tracking":
            await tracking_coll.delete_many(self.data)
        elif self.value == "/server":
            await hotkey_coll.delete_many(self.data)
        else:
            print("[Custom] Stored Feature Data NOT RECOGNIZED")
            print(self.value)
        await interaction.response.edit_message(content="Previously stored configuration cleared! Please run the setup command again...", view=None)
    async def reset_on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.ctx.interaction.edit_original_message(content="*This prompt has expired please run the command again*", view=self)

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
                view=resetView(findguild, self.ctx, self.feature)
                await interaction.response.send_message("You have already setup this feature... Hit the reset button bellow to clear the configuration of the selected feature. (*Dismiss this message to cancel*)", view=view)
        elif self.feature == "Tracking":
            findguild= await tracking_coll.find_one({"_id": sid})
            if not findguild:
                channel = discord.utils.get(interaction.guild.channels, name=self.children[2].value)
                try:
                    channel_id = channel.id
                    await tracking_coll.insert_one({"_id":sid, "trackip": self.children[0].value, "trackchannel": channel_id, "trackport": int(self.children[1].value)})
                    await interaction.response.send_message(f"Tracking server `{self.children[0].value}:{self.children[1].value}` in <#{channel_id}>")
                except AttributeError:
                    await interaction.response.send_message("> Please provide a **valid channel name**! ????\n> *(Valid channel names do not include the # ex. 'tracking' NOT '#tracking')*")
            else:
                view=resetView(findguild, self.ctx, self.feature)
                await interaction.response.send_message("You have already setup this feature... Hit the reset button bellow to clear the configuration of the selected feature. (*Dismiss this message to cancel*)", view=view)
        else:
            await interaction.response.send_message(embed=utilities.ErrorMessage.error_message())
        
class setupView(View):
    options = []
    for feature in features:
        options.append(discord.SelectOption(label=feature["friendly_name"], description=feature["description"].replace("*", "")))
    
    def __init__(self, ctx):
        super().__init__(timeout=15)
        self.ctx=ctx
        self.feature = None
    @discord.ui.select( 
        placeholder = "Choose a feature to setup!", #
        min_values = 1, 
        max_values = 1, 
        options = options
    )
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        await interaction.response.defer()
        self.feature = select.values[0]

    @discord.ui.button(label="Setup", style=discord.ButtonStyle.success, emoji="??????")
    async def button_callback(self, button, interaction):
        if interaction.user != self.ctx.user:
            await interaction.send_message("You didn't run this command!", ephemeral=True)
        else:
            if self.feature is not None:
                if self.feature == "/server":
                    findguild= await hotkey_coll.find_one({"_id": interaction.guild_id})
                    if findguild:
                        view=resetView(findguild, self.ctx, self.feature)
                        await interaction.response.send_message("You have already setup this feature... Hit the reset button bellow to clear the configuration of the selected feature. (*Dismiss this message to cancel*)", view=view, ephemeral=True)
                    else:
                        button.disabled = True
                        await self.ctx.interaction.edit_original_message(view = self)
                        await interaction.response.send_modal(setupModal(ctx=self.ctx, feature=self.feature, title="Reko Setup"))
                elif self.feature == "Tracking":
                    findguild= await tracking_coll.find_one({"_id": interaction.guild_id})
                    if findguild:
                        view=resetView(findguild, self.ctx, self.feature)
                        await interaction.response.send_message("You have already setup this feature... Hit the reset button bellow to clear the configuration of the selected feature. (*Dismiss this message to cancel*)", view=view, ephemeral=True)
                    else:
                        button.disabled = True
                        await self.ctx.interaction.edit_original_message(view = self)
                        await interaction.response.send_modal(setupModal(ctx=self.ctx, feature=self.feature, title="Reko Setup"))
                else:
                    await interaction.response.send_message("This feature is still a work in progress and is not complete!", ephemeral=True)           
            else:
                await interaction.response.send_message("Please select the feature you would like to setup first!")
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.ctx.interaction.edit_original_message(view=self)

class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @slash_command(description="Setup Reko for your server!")
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        embed=discord.Embed(title="Setup up Reko for your server! ", description="Please select the feature you would like to setup with the **select menu** and then hit the **green setup button** to set it up for your server!", color=color)
        embed.set_thumbnail(url="https://www.technotalks.net/static/main/images/Reko_Circular-removebg-preview.png")
        embed.set_author(name=f"Customizable features of Reko")
        
        for feature in features:
            embed.add_field(name="__"+feature["friendly_name"]+"__", value=feature["description"], inline=False)
        
        embed.add_field(name="\u200B", value="Please report bugs in the [support server](https://discord.gg/8vNHAA36fR)! It really helps the bot grow!")
        view=setupView(ctx)
        await ctx.respond(embed=embed, view=view)
    @setup.error
    async def setuperror(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond(f"You are missing the required permission: **{error.missing_permissions[0].capitalize()}**, to run this command!")
        else:
            error_logger.log("Setup Command", error, sys.exc_info()[-1])
            await ctx.respond(embed=utilities.ErrorMessage.error_message())

    @slash_command(description="Gets status of hotkeyed server!")
    async def server(self, ctx):
        await ctx.defer()

        inputid=ctx.guild_id
        #sip=read_json(inputid)
        findguild = await hotkey_coll.find_one({"_id":inputid})

        if not findguild:
           await ctx.respond("This command has **not been setup properly** please ask the __admins/mods__ to run **/setup** to setup this command!")    
        else:
            try:
                ip=findguild["mcip"]
                try:
                    server = JavaServer.lookup(ip, 3)
                    status = await server.async_status()
                except:
                    await ctx.respond(embed=utilities.unreachable_server(ip))
                    return
                #get motd
                motd = utilities.StatusCore.motd_cleanser(status.description)

                embed=discord.Embed(title=f"Status of {ip}", description=f"{motd}",color=color)
                embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{ip}")
                try:
                    ip_addr = socket.gethostbyname(ip)
                    embed.add_field(name="IP: ", value=f"`{ip_addr}`")
                except: pass
                embed.add_field(name="Player Count:", value=f"`{status.players.online}`", inline=True)
                embed.add_field(name="Version:", value=f"`{status.version.name}`", inline=True)
                if status.players.sample != None and status.players.sample != []:
                    player_list=""
                    for player in status.players.sample:
                        player_list += player.name.replace(".", "")+", "
                    embed.add_field(name="Player list:", value=f"`{player_list[:-2]}`", inline=False)
                await ctx.respond(embed=embed)
            except KeyError:
                await ctx.respond("This command has **not been setup properly** please ask the __admins/mods to run__ **/setup** to setup this command!")

    @server.error
    async def servererror(self, ctx, error):
        error_logger.log("Server Command", error, sys.exc_info()[-1])
        await ctx.respond(embed=utilities.ErrorMessage.error_message())
        raise error
        
def setup(bot):
    print("[Custom] Loading extension...")
    bot.add_cog(Custom(bot))
def teardown(bot):
    print("[Custom] Unloading extension...")