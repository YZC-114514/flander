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
        

        

async def calculate_fortune():
    return [round(sum(random.randint(0, 100) for _ in range(3)) / 3) for _ in range(3)]

async def fortune_of_today(ctx):
    user_id = ctx.author.id
    username = str(ctx.author)
    today = datetime.today().date()

    fortunes = await calculate_fortune()
    output_fort_tdy = {1: fortunes[0], 2: fortunes[1], 3: fortunes[2]}
    
    async with aiosqlite.connect('database.db') as db:
        async with db.execute('SELECT checkin_count, last_checkin, output_fort_tdy1, output_fort_tdy2, output_fort_tdy3 FROM checkins WHERE user_id = ?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            checked_in_today = False
            
            if row:
                last_checkin_date = datetime.strptime(row[1], '%Y-%m-%d').date()
                if last_checkin_date < today:
                    await db.execute('UPDATE checkins SET checkin_count = checkin_count + 1, last_checkin = ?, output_fort_tdy1 = ?, output_fort_tdy2 = ?, output_fort_tdy3 = ? WHERE user_id = ?', 
                                      (today, output_fort_tdy[1], output_fort_tdy[2], output_fort_tdy[3], user_id))
                else:
                    output_fort_tdy[1] = row[2]
                    output_fort_tdy[2] = row[3]
                    output_fort_tdy[3] = row[4]
                    checked_in_today = True
            else:
                await db.execute('INSERT INTO checkins (user_id, username, checkin_count, last_checkin, output_fort_tdy1, output_fort_tdy2, output_fort_tdy3) VALUES (?, ?, 1, ?, ?, ?, ?)', 
                                  (user_id, username, today, output_fort_tdy[1], output_fort_tdy[2], output_fort_tdy[3]))

        await db.commit()

    text = (
        f'@{username} '
        f'{"你今儿已经测过了噢，别想糊弄我(′△｀)：" if checked_in_today else "少女祈祷中(~▽~"")...您今天的運勢如下："}\n'
        f'財運：{output_fort_tdy[1]}\n'
        f'桃花：{output_fort_tdy[2]}\n'
        f'事業：{output_fort_tdy[3]}'
    )

    return text