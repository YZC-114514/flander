
import discord
import json
from discord.ext import commands


f = open('config.json')
data = json.load(f)
token = data["flander"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = "|", intents=intents)

@bot.command()
@commands.has_permissions(administrator = True)
async def tongbu(ctx):
    await bot.tree.sync()
    await ctx.send('同步完成')

@bot.hybrid_command()
async def ping(ctx):
    """檢查在線狀況"""
    await ctx.send("芙蘭朵露已上線")


bot.run(token)
