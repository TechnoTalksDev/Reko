import hikari
import lightbulb

from lightbulb import commands, context
from lightbulb import help_command


with open("./secrets/token", "r") as f:
    token = f.read().strip()

bot = lightbulb.BotApp(
    token,
    prefix="+",
    default_enabled_guilds=(846192394214965268, 866018599557791755),
    help_class=None,
)

bot.load_extensions_from("./extensions/", must_exist=True)

color=0x6bf414

@bot.command
@lightbulb.command("ping", description="The bot's ping")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
#async def ping(ctx: context.Context) -> None:
    #await ctx.respond(f"Pong! Latency: {bot.heartbeat_latency*1000:.2f}ms")
async def ping(ctx):
    embed = hikari.Embed(title=f"{bot.get_me().username} Latency", color=color)
    embed.set_author(name="Pong! 🏓")
    embed.add_field(name="Ping",
                    value=f"{round(bot.heartbeat_latency * 1000)}ms",
                    inline=False)
    await ctx.respond(embed=embed)