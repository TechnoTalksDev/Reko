import discord
from discord.ext import commands, tasks
#bot client
bot = discord.Bot()
#setting color of bot
color=0x6bf414
#guilds to process slash commands
guilds=[846192394214965268]
#getting token from token file
with open("./secrets/token", "r") as f:
    token = f.read().strip()
#startup message
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
#ping command
@bot.slash_command(guild_ids=guilds, description="Latency of the bot to Discord")
async def ping(ctx):
    embed = discord.Embed(title=f"{bot.user.display_name} Latency", color=color)
    embed.set_author(name="Pong! 🏓")
    embed.add_field(name="Ping",
                    value=f"{round(bot.latency * 1000)}ms",
                    inline=False)
    await ctx.respond(embed=embed)
#reload extensions
@bot.slash_command(guild_ids=guilds, description="Reloads extensions.")
async def reload(ctx):
    await bot.reload_extension('extensions.static')
    await ctx.respond("Reloaded cog's and extensions.")
#loading extensions
bot.load_extension("extensions.static")
bot.load_extension("extensions.dc")
bot.load_extension("extensions.tasks")
#running bot
bot.run(token)