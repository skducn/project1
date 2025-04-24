# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 时事爬取网站当天某股票收盘价，开盘价，成交量
# 需求，打开all.xlsx 获取上海股票代码，遍历获取上一日和当天的收盘价，开盘价，成交量，
# 判断，当天收盘价 大于 上一日的开盘价，且成交量小于上一日的票。
# 参考：https://quote.eastmoney.com/sz002494.html#fullScreenChart
# https://www.sse.com.cn/market/price/report/
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

from PO.WebPO import *
from PO.OpenpyxlPO import *

def genData():

    # 1，打开页面，获取数据
    Web_PO = WebPO("noChrome")
    varUrl = "https://www.sse.com.cn/market/price/report/"
    Web_PO.openURL(varUrl)
    sleep(4)
    # 选择股票类型
    Web_PO.clkByX("/html/body/div[8]/div/div[1]/div/div[3]/div[2]/div/button", 1)
    Web_PO.clkByX("//div[@class='dropdown-menu show']/div/ul/li[2]")
    Web_PO.clkByX("//div[@class='pagination-box']/ul")

    # 2，获取当天日期作为文件名
    l_time = Web_PO.getTextByXs("//h2[@class='title_lev2']")
    fileName = l_time[0].split("更新时间：")[1].split(" ")[0]
    fileName = fileName + ".xlsx"
    Openpyxl_PO = OpenpyxlPO(fileName)

    # 3，获取page数量
    l_page = Web_PO.getTextByXs("//div[@class='pagination-box']/ul")
    # print(l_page[0].split("\n"))
    # print(l_page[0].split("\n")[7])
    page = int(l_page[0].split("\n")[7])
    print("【共", page, "页】")

    # 4，设置标题
    Openpyxl_PO.appendRows([['序号','证券代码','证券简称','类型','最新','涨跌幅','涨跌','成交量(手)','成交额(万元)','前收','开盘','最高','最低']])

    for i in range(page):
        # 5，获取第N页数据
        Web_PO.setTextByX("/html/body/div[8]/div/div[2]/div/div[1]/div[2]/span[1]/input", i+1)
        Web_PO.clkByX("/html/body/div[8]/div/div[2]/div/div[1]/div[2]/span[2]/a", 1)
        l_all = Web_PO.getTextByXs("//tr")
        # print(l_all)
        l_all.pop(0)
        print("已完成 =>", i+1)
        for j in range(len(l_all)):
            l_tmp = l_all[j].split(" ")
            # print(l_tmp)
            l_4 = []
            l_4.append(l_tmp)
            Openpyxl_PO.appendRows(l_4)
        Openpyxl_PO.save()


if __name__ == "__main__":

    genData()
