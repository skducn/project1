# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-12-28
# Description: bilibili视频下载
# todo 下载1080视频，需要登录后获取cookies 方法如下：
# 1，先手机安装bilibili客户端，并登录
# 2，执行getCookies.py脚本，弹出二维码，微信扫描后生成cookies，并保存在cookies.txt
# 3，BilibiliPO.py - downloadMore中的request中加入cookies
# 如：cookies = {'DedeUserID': '30441444', 'DedeUserID__ckMd5': '1107acbf0781861b', 'SESSDATA': '4b6f3ef6%2C1746514066%2Cadb80%2Ab2CjBDr8ZrxLKgX9k7slbKbE4ZXNu8J3T5B49a68yERhXGMbkdonV3wOLQY61Rq3GA2ggSVkRPMjJqOEd5N3BEV2V0cUdDeHhUV1gyTW9vTmJyUHRqVUZueENZLVdlYmgyNlVURDhObjRlam9RSEZOMzRRYWcwaTdBeHRYcUVteHhUUzNmdXVmSHlnIIEC', 'b_nut': '1730962066', 'bili_jct': '50b7d49715cb1f75bc87eaaeffa9ce4b', 'buvid3': 'CE581F46-82A3-6FD6-8D73-E212A46C1B1D66922infoc', 'sid': 'ff81ti6a'}
# request.get(url,header=header,cookies=cookies)
#***************************************************************

import sys
sys.path.append('../../')

from BilibiliPO import *
Bilibili_PO = BilibiliPO()


Bilibili_PO.downloadMore(sys.argv[1])





