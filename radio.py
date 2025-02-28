import asyncio
import math
import cmath



def ant_cal(freq, type="Dipole", elm=0):
    match type:
        case "Dipole":
            length = round(300 / freq, 3)
            return f"length:{round(length / 2, 2)} m"
        
        case "J":
            wavelength = round(300 / freq, 5)
            A_L = round(0.75 * wavelength,2)
            B_L = round(0.25 * wavelength,2)
            C_L = round(0.02 * wavelength,2)
            D_L_J = round(0.0125 * wavelength,2)
            rtn = f"Radiating Element: {A_L} m\nMatching Section: {B_L} m\nFeed Point Location: {C_L} m\nSpacing: {D_L_J} m"
            return rtn

        case "Yagi":
            wavelength = round(300 / freq, 5)
            D_E_L = 300 * 0.475 / freq
            R_L = round(D_E_L * 1.05, 2)
            D_L = round(D_E_L * 0.95, 2)
            spec = wavelength * 0.2
            gain_exp = round((10 * math.log(elm)) + 2.15, 2) if elm > 0 else "Invalid element count"
            rtn = f"Driver Element Length: {D_E_L} m\nReflector Length: {R_L} m\nDirector Length: {D_L} m\nSpacing: {spec} m\nExpected Gain: {gain_exp} db"
            return rtn



async def imped_cal(ctx,bot,n,freq,connected):
    if connected !="P" and connected!="S":
        await ctx.send('Error: Invalid input! please tried again. ')
        return
    
    else:
            if connected == "S": imped = complex(0,0)
            else: y_total = complex(0,0)
            for i in range(n):
                await ctx.send("請輸入元件類別 R:電阻，C:電容，I:電感")
                try:
                    message = await bot.wait_for('message', timeout=60)
                    type = message.content.strip()
                except asyncio.TimeoutError:
                    await ctx.send('超時，請重新開始。')
                    return
                match type:
                    case "R":
                        await ctx.send("請輸入電阻值：")
                        try:
                            message = await bot.wait_for('message', timeout=60)
                            r = float(message.content.strip())
                            z = complex(r, 0)
                        except asyncio.TimeoutError:
                            await ctx.send('超時，請重新開始。')
                            return
                        

                    case "C":
                        await ctx.send("請輸入電感值：")
                        try:
                            message = await bot.wait_for('message', timeout=60)
                            capacity = float(message.content.strip())
                            z = complex(0,-1/(2*math.pi*float(freq)*capacity))
                        except asyncio.TimeoutError:
                            await ctx.send('超時，請重新開始。')
                            return
                        
                    case "I":
                        await ctx.send("請輸入電抗值：")
                        try:
                            message = await bot.wait_for('message', timeout=60)
                            induct = float(message.content.strip())
                            z = complex(0,round(math.pi*2*induct*float(freq)))
                        except asyncio.TimeoutError:
                            await ctx.send('超時，請重新開始。')
                            return
                
                if connected == "S": imped += z
                else: y_total += 1 / z
            
            if connected == "P":
                if y_total == 0:
                    await ctx.send("錯誤：並聯元件導納總和為零。")
                    return
                imped = 1 / y_total
        
    rtn =  f"總阻抗為：{imped.real:.4f}+{imped.imag:.4f}i Ω\n等效於：{abs(imped):.4f} ∠{cmath.phase(imped):.4f} rad"     
    await ctx.send(rtn)