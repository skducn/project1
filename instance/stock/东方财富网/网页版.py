# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2026-01-7
# Description: 东方财富网
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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


Web_PO = WebPO("chrome")
Web_PO.openURL("https://quote.eastmoney.com/zixuan/lite.html")
Web_PO.clkByX("/html/body/div[7]/img[1]",1)  # 广告
Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[2]/div/a[1]",3)  # 登陆
Web_PO.dwele('//span[@date-type="account" and text()="账号登录"]')   # 移动到登陆标签

Web_PO.setTextEnterByX("/html/body/div/div[2]/div/form[1]/div/div[1]/input", "13816109050")
Web_PO.setTextEnterByX("/html/body/div/div[2]/div/form[1]/div/div[2]/input", "Jinhao123")
Web_PO.clkByX("/html/body/div/div[2]/div/form[1]/div/div[4]/div/img[1]",2)  # 勾选
Web_PO.clkByX("/html/body/div/div[2]/div/form[1]/div/div[3]/div[1]/div/div[4]/div/div",2)  # 验证点击
Web_PO.quitIframe(2)


# 前5个自选板块
l_stock = Web_PO.getTextByXs("//ul[@id='zxggrouplist']/li")
# print(l_stock)  # ['自选股', 'BK4', '全固态电池', '光刻机', '深空通讯和数据链', 'HBM']
for i in range(3, 7):
    Web_PO.clkByX("/html/body/div[2]/div[3]/div[1]/div/ul[1]/li[" + str(i) + "]/a", 2)
    # # 获取行数股票
    # QTY_tr = Web_PO.getCountByXs("//table[@id='wltable']/tbody/tr")
    # print(l_stock[i-1], "-------------------------")
    # for i in range(QTY_tr):
    #     s_stock = Web_PO.getTextByX('/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i+1) + ']/td[4]/a')
    #     print(s_stock)

    # 资金流向
    Web_PO.clkByX("/html/body/div[2]/div[3]/div[2]/ul/li[2]")
    # 获取行数股票
    QTY_tr = Web_PO.getCountByXs("//table[@id='wltable']/tbody/tr")
    print(l_stock[i - 1], "-------------------------")
    for i in range(QTY_tr):
        s_code = Web_PO.getTextByX('/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[3]/a')  # 代码
        s_stock = Web_PO.getTextByX('/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[4]/a')  # 名称
        s_in = Web_PO.getTextByX('/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[8]/span')  # 主力净流入 > 2亿
        if "亿" in s_in:
            s_in = s_in.replace("亿", "")
        else:
            s_in = 0
        s_ultra_large = Web_PO.getTextByX('/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[10]/span')  # 超大但净占比 > 4%
        s_ultra_large = s_ultra_large[:-1]
        if float(s_in) > 2 and float(s_ultra_large) > 4:
            # print(s_code, s_stock, s_in, s_ultra_large)
            s_tmp = str(s_code) + " " + s_stock + ", 主力净流入:" + str(s_in) + "亿, 超大单净占比:" + str(s_ultra_large) + "%"
            Color_PO.outColor([{"35": s_tmp}])


# 更多组合
Web_PO.clkByX("/html/body/div[2]/div[3]/div[1]/div/ul[2]/li/div/a", 2)
l_more = Web_PO.getTextByXs("//ul[@class='moregroupul bscroll']/li")
# print(l_more) # ['商业航天', '医药商业', '玻璃基板', '锂矿概念']
QTY_more = Web_PO.getCountByXs("//ul[@class='moregroupul bscroll']/li")
# print(QTY_more)
for i in range(1, QTY_more + 1):
    Web_PO.clkByX("/html/body/div[2]/div[3]/div[1]/div/ul[2]/li/div/a", 2)
    Web_PO.clkByX("//ul[@class='moregroupul bscroll']/li[" + str(i) + "]", 2)
    # # 获取行数股票
    # QTY_tr = Web_PO.getCountByXs("//table[@id='wltable']/tbody/tr")
    # print(l_more[i-1], "-------------------------")
    # for i in range(QTY_tr):
    #     s_stock = Web_PO.getTextByX('/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i+1) + ']/td[4]/a')
    #     print(s_stock)

    # 资金流向
    Web_PO.clkByX("/html/body/div[2]/div[3]/div[2]/ul/li[2]")
    # 获取行数股票
    QTY_tr = Web_PO.getCountByXs("//table[@id='wltable']/tbody/tr")
    print(l_more[i - 1], "-------------------------")
    for i in range(QTY_tr):
        s_code = Web_PO.getTextByX('/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[3]/a')  # 代码
        s_stock = Web_PO.getTextByX('/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[4]/a')  # 名称
        s_in = Web_PO.getTextByX('/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[8]/span')  # 主力净流入 > 2亿
        if "亿" in s_in:
            s_in = s_in.replace("亿", "")
        else:
            s_in = 0
        s_ultra_large = Web_PO.getTextByX('/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[10]/span')  # 超大但净占比 > 4%
        s_ultra_large = s_ultra_large[:-1]
        if float(s_in) > 2 and float(s_ultra_large) > 4:
            # print(s_code, s_stock, "主力净流入:", s_in, "亿，超大但净占比", s_ultra_large, "%")
            s_tmp = str(s_code) + " " + s_stock + ", 主力净流入:" + str(s_in) + "亿, 超大单净占比:" + str(s_ultra_large) + "%"
            Color_PO.outColor([{"35": s_tmp}])







