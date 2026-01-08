# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2026-01-7
# Description: 东方财富网 BK4 获取所有板块当天 主力净流入， 超大单净占比
# https://quote.eastmoney.com/zixuan/lite.html
# 获取页面数据
# *****************************************************************

import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from multiprocessing import Pool, cpu_count
import time

from PO.ListPO import *
List_PO = ListPO()

from PO.TimePO import *
Time_PO = TimePO()

from PO.ColorPO import *
Color_PO = ColorPO()

from PO.WebPO import *
from PO.NewexcelPO import *
from PO.OpenpyxlPO import *


# todo 登录
Web_PO = WebPO("chrome")
Web_PO.openURL("https://quote.eastmoney.com/zixuan/lite.html")
Web_PO.clkByX("/html/body/div[7]/img[1]", 1)  # 广告
Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[2]/div/a[1]", 2)  # 登陆
Web_PO.dwele('//span[@date-type="account" and text()="账号登录"]')   # 移动到登陆标签
Web_PO.setTextEnterByX("/html/body/div/div[2]/div/form[1]/div/div[1]/input", "13816109050")
Web_PO.setTextEnterByX("/html/body/div/div[2]/div/form[1]/div/div[2]/input", "Jinhao123")
Web_PO.clkByX("/html/body/div/div[2]/div/form[1]/div/div[4]/div/img[1]", 2)  # 勾选
Web_PO.clkByX("/html/body/div/div[2]/div/form[1]/div/div[3]/div[1]/div/div[4]/div/div", 2)  # 验证点击
Web_PO.quitIframe(1)


# 前5个自选板块
l_stock = Web_PO.getTextByXs("//ul[@id='zxggrouplist']/li")
# print(l_stock)  # ['自选股', 'BK4', '全固态电池', '光刻机', '深空通讯和数据链', 'HBM']
Web_PO.clkByX("/html/body/div[2]/div[3]/div[1]/div/ul[1]/li[2]/a", 2)  # BK4
Web_PO.clkByX("/html/body/div[2]/div[3]/div[2]/ul/li[2]")  # 资金流向
Web_PO.clkByX("/html/body/div[2]/div[3]/div[3]/table/thead/tr/th[8]/a")  # 主力净流入
# Web_PO.clkByX("/html/body/div[2]/div[3]/div[3]/table/thead/tr/th[10]/a")  # 超大单净占比

# 获取行数股票
QTY_tr = Web_PO.getCountByXs("//table[@id='wltable']/tbody/tr")
for i in range(QTY_tr):
    s_code = Web_PO.getTextByX('/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[3]/a')  # 代码
    s_stock = Web_PO.getTextByX('/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[4]/a')  # 名称
    s_in = Web_PO.getTextByX('/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[8]/span')  # 主力净流入
    if "亿" in s_in:
        s_in = s_in.replace("亿", "")
    else:
        s_in = 0
    s_ultra_large = Web_PO.getTextByX('/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[10]/span')  # 超大但净占比
    s_ultra_large = s_ultra_large[:-1]
    # # 主力净流入 > 2亿 ， 超大但净占比 > 4%
    if float(s_in) > 2 and float(s_ultra_large) > 4:
        s_tmp = str(s_code) + " " + s_stock + ", 主力净流入:" + str(s_in) + "亿, 超大单净占比:" + str(s_ultra_large) + "%"
        Color_PO.outColor([{"35": s_tmp}])
    if float(s_in) < 0 :
        break




