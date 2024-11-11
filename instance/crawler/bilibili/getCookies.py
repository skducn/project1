# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-12-28
# Description: 获取bilibili的cookies
# pip3 install qrcode
# https://blog.csdn.net/knighthood2001/article/details/139400553?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ECtr-1-139400553-blog-141756272.235%5Ev43%5Epc_blog_bottom_relevance_base8&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ECtr-1-139400553-blog-141756272.235%5Ev43%5Epc_blog_bottom_relevance_base8&utm_relevant_index=2
# todo 下载1080视频，需要登录后获取cookies 方法如下：
# 1，先手机安装bilibili客户端，并登录
# 2，执行getCookies.py脚本，弹出二维码，微信扫描后生成cookies，并保存在cookies.txt
# 3，BilibiliPO.py - download_video中的request中加入cookies
# 如：cookies = {'DedeUserID': '30441444', 'DedeUserID__ckMd5': '1107acbf0781861b', 'SESSDATA': '4b6f3ef6%2C1746514066%2Cadb80%2Ab2CjBDr8ZrxLKgX9k7slbKbE4ZXNu8J3T5B49a68yERhXGMbkdonV3wOLQY61Rq3GA2ggSVkRPMjJqOEd5N3BEV2V0cUdDeHhUV1gyTW9vTmJyUHRqVUZueENZLVdlYmgyNlVURDhObjRlam9RSEZOMzRRYWcwaTdBeHRYcUVteHhUUzNmdXVmSHlnIIEC', 'b_nut': '1730962066', 'bili_jct': '50b7d49715cb1f75bc87eaaeffa9ce4b', 'buvid3': 'CE581F46-82A3-6FD6-8D73-E212A46C1B1D66922infoc', 'sid': 'ff81ti6a'}
# request.get(url,header=header,cookies=cookies)
#***************************************************************

import requests
import time
from qrcode import QRCode
from PIL import Image
url = 'https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main-fe-header'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'Referer': 'https://www.bilibili.com/',
    'Origin': 'https://www.bilibili.com'
}

response = requests.get(url=url, headers=headers).json()
print(response)
qrcode_key = response['data']['qrcode_key']
print(qrcode_key)
# 创建二维码对象
qr = QRCode()
# 设置二维码的数据
qr.add_data(response['data']['url'])
# 生成二维码图片
img = qr.make_image()
img = img.resize((200, 200), resample=Image.BICUBIC)
# 展示图片
img.show()

check_login_url = f'https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}&source=main-fe-header'
# 创建一个Session对象
session = requests.Session()
while 1:
    data = session.get(url=check_login_url, headers=headers).json()
    print(data)
    if data['data']['code'] == 0:
        # 使用Session发起请求
        response = session.get('https://www.bilibili.com/', headers=headers)
        # Session会自动处理cookies
        print(session.cookies.get_dict())
        # 保存cookies
        with open('cookies.txt', 'w') as f:
            f.write(str(session.cookies.get_dict()))
        break

    time.sleep(1)

