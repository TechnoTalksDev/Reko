import hikari
import lightbulb
from lightbulb.checks import has_guild_permissions
from lightbulb.decorators import command
import requests
import json

from lightbulb import commands, context
from lightbulb.context.base import Context
from mcstatus import MinecraftServer

datacommands_plugin = lightbulb.Plugin("DataCommands")

color=0x6bf414

datafile="data.json"
def write_json(new_data, filename=datafile):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        #print(len(file_data["data"]))
        for i in range(len(file_data["data"])):
            #print(new_data["serverid"])
            if file_data["data"][i]["serverid"]==new_data["serverid"]:
                error="duplicate"
                return error
        file_data["data"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)
def read_json(inputid, filename=datafile):
    #print("INPUT: "+str(inputid))
    with open(filename, "r+") as file:
        file_data = json.load(file)
    #print(file_data["data"][0])
    for i in range(len(file_data["data"])):
        if file_data["data"][i]["serverid"] == inputid:
            outputr=file_data["data"][i]["mcip"]
            #print("------")
            #print(outputr)
            #print("------")
            return outputr
    return "SETUP_ERROR"
def delete_entry(inputid, filename=datafile):
    #print("INPUT: "+str(inputid))
    with open(filename, "r+") as file:
        file_data = json.load(file)
    #print(file_data["data"][0])
    for i in range(len(file_data["data"])):
        if file_data["data"][i]["serverid"] == inputid:
            file_data["data"].pop(i)
            with open(filename, "w") as file:
                file.seek(0)
                json.dump(file_data, file, indent=4)
            return "Previously stored IP cleared!"

@datacommands_plugin.command
@lightbulb.option("ip", "The ip of the server.", required=True)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command("serversetup", "Setup your custom server hotkey!")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def serversetup(ctx: context.Context):
    ip=ctx.options.ip if ctx.options.ip is not None else "Ip Not Provided"
    sid=ctx.guild_id
    #print(sid)
    d={"serverid": sid, "mcip": ip}
    #print(d)
    if ip=="reset": 
        await ctx.respond(delete_entry(sid))
    elif write_json(d)=="duplicate":
        await ctx.respond("You have already setup an ip... Run this command again with `reset` as the ip value to clear the stored ip.")
    else:
        await ctx.respond("The server command is setup!")

@datacommands_plugin.command
@lightbulb.command("server", "Gets status of hotekyed server!")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def server(ctx: context.Context):
    inputid=ctx.guild_id
    sip=read_json(inputid)
    #print(type(sip))
    #print(sip)
    if sip == "SETUP_ERROR":
        await ctx.respond("This command has not been setup properly please ask the admins to run /serversetup to setup this command!")
    else:
        url = "https://api.mcsrvstat.us/2/{}".format(sip)
        thing = requests.get(url)
        data = json.loads(thing.content)
        if data["online"] == False:
            embed=hikari.Embed(title=f"IP Error: {sip}", description="This server either does not exist or is not online. If you think this is an error, then please join the support server to report this!", color=0xff1a1a)
            await ctx.respond(embed=embed)
        else:
            motd=""
            for i in range(len(data["motd"]["clean"])):
                motd+=data["motd"]["clean"][i]
            embed=hikari.Embed(title="Status of {}".format(sip), description="{}".format(motd),color=color)
            embed.set_thumbnail(f"https://api.mcsrvstat.us/icon/{sip}")
            embed.add_field(name="Online:", value="{}".format(data["online"]), inline=True)
            embed.add_field(name="Player Count:", value="{}".format(data["players"]["online"]), inline=True)
            embed.add_field(name="Version:", value="{}".format(data["version"]), inline=True)
            await ctx.respond(embed=embed)

@serversetup.set_error_handler
async def on_serversetup_error(event: lightbulb.CommandErrorEvent) -> bool:
    exc = event.exception.__cause__ or event.exception
    ctx = event.context

    if isinstance(exc, lightbulb.MissingRequiredPermission ):
        await ctx.respond(f"You must have the `{exc.missing_perms}` permission to run this command.")
        return True

    return False


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(datacommands_plugin)