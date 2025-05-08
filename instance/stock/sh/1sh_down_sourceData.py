# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 下载上海a股数据
# 上海证交所官网：https://www.sse.com.cn/market/price/report/
# 当天收盘后下载数据，如：保存文件0429.xlsx
# for nt = "d:\\51\\python\\stock\\sh\\0429.xlsx
# for mac = "/Users/linghuchong/Downloads/51/Python/stock/sh/0429.xlsx
# 操作流程：
# 打开https://www.sse.com.cn/market/price/report/，共68页，已完成 1，已完成 2 ... 保存到文件
# *****************************************************************

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from PO.FilePO import *
File_PO = FilePO()

from PO.ListPO import *
List_PO = ListPO()

from PO.ColorPO import *
Color_PO = ColorPO()

from PO.TimePO import *
Time_PO = TimePO()

from PO.WebPO import *

from PO.OpenpyxlPO import *

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')
from PO.LogPO import *
Log_PO = LogPO(filename=Configparser_PO.DATA("logfile"), level="info")


def run():

    # 1，打开页面，获取数据
    Web_PO = WebPO("noChrome")
    # Web_PO = WebPO("chrome")
    varUrl = "https://www.sse.com.cn/market/price/report/"
    Web_PO.openURL(varUrl)
    sleep(4)

    # 2，选择股票类型
    Web_PO.clkByX("/html/body/div[8]/div/div[1]/div/div[3]/div[2]/div/button", 1)
    Web_PO.clkByX("//div[@class='dropdown-menu show']/div/ul/li[2]")
    Web_PO.clkByX("//div[@class='pagination-box']/ul")

    # 3，获取当天日期作为文件名
    # l_time = Web_PO.getTextByXs("//h2[@class='title_lev2']")
    # fileName = l_time[0].split("更新时间：")[1].split(" ")[0]
    # fileName = fileName + ".xlsx"
    varTodayFile2 = Time_PO.getMonth() + Time_PO.getDay() + ".xlsx"
    # File_PO.renameFile(fileName, varTodayFile2)
    if os.name == "nt":
        pathFile = "d:\\51\\python\\stock\\sh\\" + varTodayFile2
    else:
        pathFile = "/Users/linghuchong/Downloads/51/Python/stock/sh/" + varTodayFile2
    Openpyxl_PO = OpenpyxlPO(pathFile)

    # 4，获取page数量
    l_page = Web_PO.getTextByXs("//div[@class='pagination-box']/ul")
    page = int(l_page[0].split("\n")[7])
    print("【共", page, "页】")
    Log_PO.logger.info("【共" + str(page) + "页】")


    # 4，设置标题
    Openpyxl_PO.appendRows([['序号','证券代码','证券简称','类型','最新','涨跌幅','涨跌','成交量(手)','成交额(万元)','前收','开盘','最高','最低']])

    for i in range(page):
        # 5，获取第N页数据
        Web_PO.setTextByX("/html/body/div[8]/div/div[2]/div/div[1]/div[2]/span[1]/input", i+1)
        Web_PO.clkByX("/html/body/div[8]/div/div[2]/div/div[1]/div[2]/span[2]/a", 1)
        l_all = Web_PO.getTextByXs("//tr")
        # print(l_all)
        l_all.pop(0)
        print(">", i+1, "/ " + str(page))
        Log_PO.logger.info("> " + str(i+1) + "/" + str(page))
        for j in range(len(l_all)):
            l_tmp = l_all[j].split(" ")
            # print(l_tmp)
            l_4 = []
            l_4.append(l_tmp)
            Openpyxl_PO.appendRows(l_4)
        Openpyxl_PO.save()


if __name__ == "__main__":

    try:
        run()
        os.system("open /Users/linghuchong/Downloads/51/Python/stock/sh")
        os.system("python 2sh_save_json.py")

    except Exception as e:
        print(f"发生错误: {e}")
        Log_PO.logger.error(f"发生错误: {e}")

