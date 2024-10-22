
import discord,json
from discord.ext import commands
import random, nltk
from nltk.corpus import words

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
async def calculate(ctx,a:int,x:str,b:int):
    """簡單四則運算 (using +,-,*,/)"""
    match x:
        case "+":
            await ctx.send(a+b)
        case "-":
            await ctx.send(a-b)
        case "*":
            await ctx.send(a*b)
        case "/":
            await ctx.send(a/b)

nltk.download('words')
english_words = set(w.lower() for w in words.words())

@bot.hybrid_command()
async def wordle(ctx,l:int):
    """開啟一場wordle遊戲"""
    stoped = False
    target_word = random.choice([w for w in english_words if len(w) == l])
    # Create an empty dictionary to store the results
    result = {i: None for i in range(l)}
    time=0
    while True and time < 6:
        await ctx.send(f'单词长度为{l}，请发送单词 (發送/stop以終止遊戲):\n剩餘嘗試次數:{6-time}\n白色=不存在 黃色=位置錯誤 綠色=位置正確')
        time += 1
        # Get user's guess
        message = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        guess = message.content.lower()
        
        if guess == '/stop':
            await ctx.send(f'正確單詞是："{target_word}."')
            stoped = True
            break
        
        # Check each letter of the guess
        for i, letter in enumerate(guess):
            if letter == target_word[i]:
                result[i] = 'green'
            elif letter in target_word:
                result[i] = 'yellow'
            else:
                result[i] = 'gray'
        
        # Print the colored squares
        colored_squares = ''
        for color in result.values():
            if color == 'green':
                colored_squares += f':green_circle: '
            elif color == 'yellow':
                colored_squares += f':yellow_square: '
            else:
                colored_squares += f':white_large_square: '
        
        await ctx.send(f'{colored_squares}')
    if (time==6) and (stoped==False):
        await ctx.send(f'很遺憾本輪沒有人猜對，正確單詞是："{target_word}."')




bot.run(token)

