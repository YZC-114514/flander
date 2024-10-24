
import discord,json
from discord.ext import commands
import fortune as ft
import basic as bc
import game as gm

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

@bot.hybrid_command()
async def calculate(ctx,a:float,x:str,b:float,corr:int):
    """簡單四則運算 (using +,-,*,/)"""
    await ctx.send(bc.calculate(a,x,b,corr))

@bot.hybrid_command()
async def wordle(ctx,l:int):
    """開啟一場wordle遊戲"""
    await gm.wordle(bot,ctx,l)
    
@bot.hybrid_command()
async def psr(ctx):
    """"和芙蘭朵露一起玩剪刀石頭布吧"""
    await gm.rock_paper_scissors(ctx,bot)

@bot.hybrid_command()
async def fortune_chi(ctx, x:int=0, y:int=0, z:int=0):
    """小六壬起卦"""
    await ctx.send(ft.fortune(x,y,z))

@bot.hybrid_command()
async def fortune_tdy(ctx):
    """查查你今的運勢吧"""
    await ctx.send(bc.fortune_of_today())

bot.run(token)

