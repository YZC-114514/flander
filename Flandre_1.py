
import discord,json,aiosqlite
from discord.ext import commands, tasks
import fortune as ft
import basic as bc
import game as gm
import radio

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True


f = open('config.json')
data = json.load(f)
token = data["flander"]


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = "|", intents=intents)




#初始化數據庫
@bot.event
async def on_ready():
    print(f'{bot.user} 已連接到 Discord!')
    await bot.tree.sync()
    print("同步成功")
    await bc.init_db()


#從不同的庫裡面調用不同的指令
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
async def fortune_chi(ctx, x:int=0, y:int=0, z:int=0):
    """小六壬起卦"""
    await ctx.send(ft.fortune(x,y,z))

@bot.hybrid_command()
async def ant_cal(ctx, f:int=144 ,type:str="Dipole", elm:int=0):
    """天線參數計算: Diople=半波偶極子天線; J=J型天線; Yagi=八木天線"""
    await ctx.send(radio.ant_cal(f,type,elm))

@bot.hybrid_command()
async def total_impedance(ctx, f, connected, n:int = 1):
    """建議電路的總阻抗計算： P=並聯 S=串聯"""
    await radio.imped_cal(ctx,bot,n,f,connected)

@bot.hybrid_command()
async def fortune_tdy(ctx):
    """查查你今天的運勢吧"""
    text = await bc.fortune_of_today(ctx)
    await ctx.send(text)

@bot.hybrid_command()
async def psr(ctx):
    """"和芙蘭一起玩石頭剪刀布吧 輸入: 布 /剪刀 / 石頭"""
    await gm.rock_paper_scissors(ctx,bot)




bot.run(token)

