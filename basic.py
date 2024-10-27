import random
import aiosqlite
import asyncio
from datetime import datetime

# 初始化數據庫
async def init_db():
    async with aiosqlite.connect('database.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS checkins (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                checkin_count INTEGER,
                last_checkin DATE,
                output_fort_tdy1 INTEGER,
                output_fort_tdy2 INTEGER,
                output_fort_tdy3 INTEGER
            )
        ''')
        await db.commit()



def calculate(a,x,b,r=0):
    """簡單四則運算 (using +,-,*,/)"""
    match x:
        case "+":
            return round((a+b),r)
        case "-":
            return round((a-b),r)
        case "*":
            return round((a*b),r)
        case "/":
            return round((a/b),r)
        

        

# 定義計算今日運勢的函數
async def fortune_of_today(ctx):
    input = [0, 0, 0]
    output_fort_tdy = {1: "", 2: "", 3: ""}
    user_id = ctx.author.id
    username = str(ctx.author)
    today = datetime.utcnow().date()

    # 隨機生成財運、桃花和事業運勢
    for i in range(3):
        for j in range(3):
            input[j] += random.randint(0, 100)
    for i in range(3):
        input[i] = round(input[i] / 3)
    output_fort_tdy[1] = input[0]
    output_fort_tdy[2] = input[1]
    output_fort_tdy[3] = input[2]

    # 連接數據庫並更新或插入簽到記錄
    async with aiosqlite.connect('database.db') as db:
        async with db.execute('SELECT checkin_count, last_checkin, output_fort_tdy1, output_fort_tdy2, output_fort_tdy3 FROM checkins WHERE user_id = ?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                last_checkin_date = datetime.strptime(row[1], '%Y-%m-%d').date()
                if last_checkin_date < today:
                    await db.execute('UPDATE checkins SET checkin_count = checkin_count + 1, last_checkin = ?, output_fort_tdy1 = ?, output_fort_tdy2 = ?, output_fort_tdy3 = ? WHERE user_id = ?', 
                                      (today, user_id, output_fort_tdy[1], output_fort_tdy[2], output_fort_tdy[3]))
                    checked_in_today = False
                    last_checkin_date = today
                else:
                    output_fort_tdy[1] = row[2]
                    output_fort_tdy[2] = row[3]
                    output_fort_tdy[3] = row[4]
                    checked_in_today = True
            else:
                await db.execute('INSERT INTO checkins (user_id, username, checkin_count, last_checkin, output_fort_tdy1, output_fort_tdy2, output_fort_tdy3) VALUES (?, ?, 1, ?, ?, ?, ?)',
                                  (user_id, username, today, output_fort_tdy[1], output_fort_tdy[2], output_fort_tdy[3]))
                checked_in_today = False
        await db.commit()

    # 根據簽到狀態生成回應文本
    if checked_in_today:
        text = f'@{username} 你今儿已经测过了噢，别想糊弄我(′△｀)：\n財運：{output_fort_tdy[1]}\n桃花：{output_fort_tdy[2]}\n事業：{output_fort_tdy[3]}'

    else:
        text = f'@{username} 少女祈祷中(~▽~"")...您今天的運勢如下：\n財運：{output_fort_tdy[1]}\n桃花：{output_fort_tdy[2]}\n事業：{output_fort_tdy[3]}'

    return text