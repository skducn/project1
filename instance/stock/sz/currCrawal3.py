# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 时事爬取网站当天某股票收盘价，开盘价，成交量
# 需求，打开all.xlsx 获取上海股票代码，遍历获取上一日和当天的收盘价，开盘价，成交量，
# 判断，当天收盘价 大于 上一日的开盘价，且成交量小于上一日的票。
# 参考：https://quote.eastmoney.com/sz002494.html#fullScreenChart
# *****************************************************************

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from multiprocessing import Pool, cpu_count
import time

import tushare as ts
from PO.ListPO import *
List_PO = ListPO()


from PO.ColorPO import *
Color_PO = ColorPO()

# from PO.WebPO import *

# l_tmp = ['003042', '300004', '300069', '300096', '300103', '300132', '300162', '300193', '300195', '300220', '300224', '300293', '300335', '300340', '300354', '300363', '300373', '300376', '300388', '300389', '300404', '300407', '300425', '300434', '300440', '300455', '300456', '300474', '300510', '300513', '300546', '300549', '300582', '300585', '300594', '300604', '300606', '300612', '300623', '300633', '300637', '300639', '300640', '300650', '300655', '300669', '300692', '300701', '300705', '300707', '300708', '300726', '300736', '300740', '300747', '300748', '300784', '300791', '300804', '300821', '300826', '300829', '300830', '300839', '300848', '300851', '300860', '300861', '300865', '300868', '300885', '300886', '300889', '300891', '300894', '300897', '300915', '300927', '300957', '300966', '300967', '300985', '300998', '301019', '301035', '301036', '301056', '301059', '301075', '301077', '301078', '301100', '301123', '301175', '301197', '301211', '301223', '301226', '301230', '301235', '301268', '301269', '301297', '301322', '301332', '301383', '301386', '301387', '301388', '301390', '301395', '301507', '301520', '301522', '301539', '301555', '301581', '301588', '301592', '301613', '301622', '301631']

import requests

# 假设这是从开发者工具中找到的 AJAX 请求 URL
# url = 'https://example.com/api/data'

# 获取免费代理列表（这里假设你已经有一个代理列表）
# def get_free_proxies():
#     proxies = []
#     url = "https://www.89ip.cn/"
#     response = requests.get(url)
#     if response.status_code == 200:
#         import re
#         print(response.text)
#         proxies = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', response.text)
#         print(proxies)
#     return proxies
#
# get_free_proxies()
# sys.exit(0)

headers = {
    'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

params = {
    'param1': 'value1',
    'param2': 'value2'
}
# 183.164.243.2	8089

# 定义代理服务器地址
proxies = {
    'http': 'http://183.164.243.2:8089',
    'https': 'http://183.164.243.2:8089'
}

url = "https://stock.xueqiu.com/v5/stock/quote.json?symbol=SZ001382&extend=detail"

# 发送HTTP请求并使用代理
try:
    response = requests.get(url, proxies=proxies)
    print(response.text)
except requests.RequestException as e:
    print(f"请求出错: {e}")

# def aa():
#     l_3 = []
#     # print(s_tmp,type(s_tmp))
#     # s_tmp = "['003042', '300004']"
#     # l_tmp = eval(s_tmp)
#
#     l_tmp = ['001382', '002132']
#     for i in l_tmp:
#         Web_PO = WebPO("noChrome")
#         # varUrl = "https://stockpage.10jqka.com.cn/realHead_v2.html#hs_" + str(i)
#         varUrl = "https://xueqiu.com/S/SZ" + str(i)
#         Web_PO.openURL(varUrl)
#         print(varUrl)
#         sleep(1)
#
#         d_curr = {}
#         l_1 = Web_PO.getTextByXs("//div[@class='quote-container']")
#         # l_1 = Web_PO.getTextByXs("//table[@class='quote-info']")
#         print(l_1)
#         # d_curr['金开'] = l_1[0].replace('今开：','')
#         # d_curr['成交量'] = l_1[1].replace('成交量：','').replace('万','').strip()
#         #
#         # l_2 = Web_PO.getTextByXs("//div[@class='new_detail fl']/ul/li[2]/span")
#         # # print(l_2)
#         # d_curr['换手'] = l_2[2].replace('换手：', '').replace('%', '').strip()
#         #
#         # l_3 = Web_PO.getTextByXs("//div[@class='new_detail fl']/ul/li[3]/span")
#         # # print(l_3)
#         # d_curr['市净率'] = l_3[2].replace('市净率：', '').strip()
#         #
#         # l_4 = Web_PO.getTextByXs("//div[@class='new_detail fl']/ul/li[4]/span")
#         # # print(l_4)
#         # d_curr['市盈率'] = l_4[2].replace('市盈率(动)：', '').strip()
#         #
#         # print(d_curr)

#
# if __name__ == "__main__":
#
#     # aa(sys.argv[1])
#     # cd /Users/linghuchong/Downloads/51/Python/project/instance/stock/sz
#     # conda activate py310
#     # python cliRun.py "['003042', '300004']"
#     aa()
