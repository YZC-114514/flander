import discord
import random, nltk,asyncio
from nltk.corpus import words

nltk.download('words')
english_words = set(w.lower() for w in words.words())

async def wordle(bot,ctx,l):
    stoped = False
    target_word = random.choice([w for w in english_words if len(w) == l])
    # Create an empty dictionary to store the results
    result = {i: None for i in range(l)}
    time=0
    while True and time < 6:
        await ctx.send(f'单词长度为{l}，请发送单词 (發送/stop以終止遊戲):\n剩餘嘗試次數:{6-time}\n白色=不存在 黃色=位置錯誤 綠色=位置正確')
        time += 1
        # Get user's guess
        try:
            message = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=300)
        except asyncio.TimeoutError:
            await ctx.send('遊戲超時，請重新開始。')
            return

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
        if guess==target_word: 
            await ctx.send(f"恭喜你,答對了")
            break
    if (time==6) and (stoped==False):
        await ctx.send(f'很遺憾本輪沒有人猜對，正確單詞是："{target_word}."')



async def rock_paper_scissors(ctx,bot):
    while (input!="stop"):
        await ctx.send("選擇你要出什麼吧!\n stop 終止遊戲")
        try:
            input = await bot.wait_for('input', timeout=120)
        except asyncio.TimeoutError:
            await ctx.send('遊戲超時，請重新開始。')
            return
        reslut = "Un"
        choice = {"剪刀","石頭","布"}
        flander_choose = random.sample(choice,1)
        if input==flander_choose: reslut = "平局"
        else: 
            match input:
                case "剪刀":
                    if flander_choose == "石頭": reslut = "你輸了"
                    else: reslut = "你贏了"
                case "石頭":
                    if flander_choose == "布": reslut = "你輸了"
                    else: reslut = "你贏了"
                case "布":
                    if flander_choose =="剪刀": reslut = "你輸了"
                    else: reslut = "你贏了"
            await ctx.send(f"你出了{input}, 芙蘭朵露出了{flander_choose}, 結果為：{reslut}")
        if input=="stop":
            if reslut == "你贏了": 
                return "一贏了就跑，輸不起是吧"
            elif reslut == "你輸了":
                return "雑魚～  雑魚～"
            else: return "這次就放過你了~ 下不為例"
            
    

