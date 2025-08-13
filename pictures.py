import json, requests
url = "https://image.anosu.top/pixiv/json"

async def pictures(r18,keywords):
    r18text = "?r18=" + str(r18)
    key =  "&keyword=" + keywords
    picurl = url+r18text+key
    params = {'return': 'json'}
    res = requests.get(picurl, params=params).json()
    return(json.dumps(res, indent=2))
