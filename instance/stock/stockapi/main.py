# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-01-29
# Description: stockapi 获取当天股票最低价和收盘价与7_stock.clsx文件比较，符合要求的写入文档最后一列
# https://stockapi.com.cn/#/ma
# {"msg":"该接口无token用户单个ip每日可调用三次，请明日再来，若想无限制，请购买token，地址:https://stockapi.com.cn","code":60040}
# https://stockapi.com.cn/v1/base/ZTPool?date=2024-09-30

# http://www.kxdaili.com/dailiip.html free IP
# http://www.ip3366.net/free/?stype=1
# https://zhuanlan.zhihu.com/p/4643609408
# *****************************************************************

import pandas as pd
pd.set_option('display.width', None)

import requests
from PO.TimePO import *
Time_PO = TimePO()

from PO.OpenpyxlPO import *

# 1 读取excel文件,遍历每个sheet，获取code 和 lastPrice
Openpyxl_PO = OpenpyxlPO("/Users/linghuchong/Downloads/51/Python/project/instance/stock/stockapi/7_stock/7_stock.xlsx")
# Openpyxl_PO = OpenpyxlPO("/Users/linghuchong/Downloads/51/Python/project/instance/stock/stockapi/7_stock/7stockapi.xlsx")
l_sheet = Openpyxl_PO.getSheets()
# print(l_sheet)  # ['20251213', '20240930']
l_tmp = []

for i in l_sheet:
    varRC = Openpyxl_PO.getTotalRowCol(varSheet=i)
    # print(varRC)  # [3, 21]
    l_1 = Openpyxl_PO.getOneCol('A', varSheet=i)
    l_2 = Openpyxl_PO.getOneCol('D', varSheet=i)
    l_ = list(zip(l_1, l_2))
    l_.pop(0)
    # print(l_)  # [('300781', 70), ('300795', 39)]
    # varDate = Time_PO.getDateByMinus()
    varDate = '2025-01-27'
    # 设置标题为日期
    Openpyxl_PO.setCell(1, varRC[1] + 1, varDate, varSheet=i)

    for j in range(len(l_)):
        varUrl = 'https://stockapi.com.cn/v1/base/day?code=' + str(l_[j][0]) + '&endDate=' + str(varDate) + '&startDate=' + str(varDate) + '&calculationCycle=100'
        print(varUrl)
        x = requests.get(varUrl)
        d_1 = x.json()
        print("最低价：", d_1['data'][0]['low'], "收盘价：", d_1['data'][0]['close'])
        # if float(d_1['data'][0]['low']) <= l_[j][1] or float(d_1['data'][0]['close']) <= l_[j][1]:
        if (float(d_1['data'][0]['low']) <= l_[j][1] or float(d_1['data'][0]['close']) <= l_[j][1]) and float(d_1['data'][0]['low']) >= l_[j][1] * 0.1:

            # 遍历当前行，取消所有背景色
            for k in range(varRC[1]):
                Openpyxl_PO.setCellColor(j+2, k+1, "ffffff", varSheet=i)  # 设置白色

            # 用红色背景色设置值
            Openpyxl_PO.setCell(j+2, varRC[1]+1, "low" + d_1['data'][0]['low'] + ",close" + d_1['data'][0]['close'], varSheet=i)
            Openpyxl_PO.setCellColor(j+2, varRC[1]+1, "ff0000", varSheet=i)  # 设置红色
            Openpyxl_PO.setColWidth(j+2, 20, varSheet=i)  # 设置列宽

        Openpyxl_PO.save()








