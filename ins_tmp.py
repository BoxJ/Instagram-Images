# -*- coding: utf-8 -*-
import os
import json
import requests
import urllib.parse
import random
import time

def getheaders():
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent=random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}
    return headers

def find_pic_url(after,tag_name):
    url = "https://www.instagram.com/graphql/query/?query_hash=174a5243287c5f3a7de741089750ab3b&variables="
    variables = {"tag_name": tag_name, "first": 4, "after": after}
    _variables = urllib.parse.quote(json.dumps(variables))
    url = url + _variables
    headers = getheaders()
    r_after=after
    try:
        data = requests.get(url=url, headers=headers, timeout=10).json()
        r_after = data['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
        print(str.format("拿到after:%s" % (r_after)))
        for d in data['data']['hashtag']['edge_hashtag_to_media']['edges']:
            imgurl = d['node']['display_url'].replace('https', 'http')
            print('找到链接:\n' + imgurl + '\n开始下载...')
            try:
                urllib.request.urlretrieve(imgurl,
                                           str.format("/Users/jingliang/Desktop/images/box-%ld.jpg" % (time.time() * 1000)))
                print('下载成功\n')
            except OSError as err:
                print("下载失败 OS error: {0}".format(err))
                continue
    except KeyError:
        print('返回的数据异常 - 直接return重试')
    return r_after


def download(url):
    # str.format("/Users/placefoto/Desktop/insImage/%ld.jpg" % (time.time() * 1000))
    urllib.request.urlretrieve(url, str.format("/Users/jingliang/Desktop/images/box-%ld.jpg" % (time.time() * 1000)), Schedule)
    # urllib.request.urlretrieve(url, "/Users/placefoto/Desktop/insImage/%ld.jpg",time.time()*1000)

def Schedule(a, b, c):
    # a:已经下载的数据块
    # b:数据块的大小
    # c:远程文件的大小

    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('>>> %.2f%%' % per)

if __name__ == '__main__':
    after = "QVFEZDlhY2NIN0s2bXliMy1BbGNMTTNPSndDb3FNSXV4ZzR0SHhrMjhseDFMcXFpR056ekY2RGx5bTdTWnF4eDZMbUVKcks2T0diWHBld05lcXZGdzV3RQ=="
    tag_name = "美女"
    # 如果没桌面上的 images文件夹就创建一个 jingliang是我的用户名 改成你自己的
    if not os.path.exists("/Users/jingliang/Desktop/images") :
        os.mkdir("/Users/jingliang/Desktop/images")

    r_after = find_pic_url(after, tag_name=tag_name)
    for i in range(20000):
        r_after = find_pic_url(r_after, tag_name=tag_name)