import json
import re
import requests


def bilibiliSearch(keyword):
    cookies = {
        'buvid3': 'FEBA361F-08F9-00C9-0191-698CE0023B3136553infoc',
    }
    headers = {
        'authority': 'api.bilibili.com',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36',
    }

    rsp = requests.get("https://api.bilibili.com/x/web-interface/search/type" \
                       "?&page=1&order=default&keyword=" + keyword + "&search_type=video", cookies=cookies, headers=headers)

    rspJson = json.loads(rsp.text)
    results = rspJson.get('data').get('result')[:3]
    resultDict = dict()
    for res in results:
        title = re.sub("<[^>]*>", "", res.get('title'))
        resultDict[title] = res.get("arcurl")
    return resultDict


if __name__ == '__main__':
    bilibiliSearch("沈梦瑶")
