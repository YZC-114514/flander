import random



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
        

def fortune_of_today():
    input = [0, 0, 0]
    output_fort_tdy = {"財運":"","桃花":"","事業":"","評價":""}
    
    for i in range(3):
        for j in range(3):
            input[j] += random.randint(0,100)
    
    for i in range(3):
        input[i] =  round(input[i]/3)

    output_fort_tdy["財運"] = input[0]
    output_fort_tdy['桃花'] = input[1]
    output_fort_tdy['事業'] = input[2]

    return output_fort_tdy