import random

def fortune(x=0,y=0,z=0):
    input = [0, 0, 0]
    sum = 0
    fortune = ["","",""]
    output_fort_chi = {"天宮":"","地宮":"","人宮":""}
    if (x==y==z==0):
        for i in range(0,2):
            input[i] = random.randint(1,6)
    else: 
        input[0] = x
        input[1] = y
        input[2] = z

    for i in range(3):
        sum += input[i]-1
        match (sum%6):
            case 0:
                fortune[i] = "大安 木"
            case 1:
                fortune[i] = "留戀 土"
            case 2:
                fortune[i] = "速喜 火"
            case 3:
                fortune[i] = "赤口 金"
            case 4:
                fortune[i] = "小吉 水"
            case 5:
                fortune[i] = "空亡 土"

    output_fort_chi["天宮"] = fortune[0]
    output_fort_chi['地宮'] = fortune[1]
    output_fort_chi['人宮'] = fortune[2]
    return output_fort_chi