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

import requests,time
import json
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
    print(varRC)
    l_1 = Openpyxl_PO.getOneCol('A', varSheet=i)
    l_2 = Openpyxl_PO.getOneCol('D', varSheet=i)
    l_ = list(zip(l_1, l_2))
    l_.pop(0)
    # del d_['code']
    print(l_)  # [('300781', 70), ('300795', 39)]
    Openpyxl_PO.setColWidth(20,15, varSheet=i)
    Openpyxl_PO.setColWidth(21,20, varSheet=i)
    Openpyxl_PO.save()

    # Openpyxl_PO.setCellColor(2, 5, "000000",varSheet=i)  # 设置白色








