import json
from pixivpy3 import AppPixivAPI

f = open('config.json')
data = json.load(f)
token = data["pixiv"]

#login
api = AppPixivAPI()
api.set_auth(token)


# 搜尋圖片
def search_pixiv_images(keyword, max_results=10):
    for i in range(max_results):
        json_result = api.search_illust(keyword)
        if json_result and hasattr(json_result, 'illusts') and json_result.illusts:
            illust = json_result.illusts[0]
            print(f"插圖 ID: {illust.id}")
            print(f"標題: {illust.title}")
            print(f"作者: {illust.user.name}")
            print(f"圖片 URL: {illust.image_urls['large']}")
        else:
            print("未找到插圖或 API 請求失敗。")

    

# 使用關鍵字搜尋圖片
search_pixiv_images("東方")