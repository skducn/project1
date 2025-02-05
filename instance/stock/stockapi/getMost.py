# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-01-29
# Description: stockapi 获取最多涨停板的票
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

# 1 读取excel文件,遍历每个sheet，获取code和name
Openpyxl_PO = OpenpyxlPO("/Users/linghuchong/Downloads/51/Python/project/instance/stock/stockapi/7_stock/7_stock.xlsx")
l_sheet = Openpyxl_PO.getSheets()
# print(l_sheet)  # ['20251213', '20240930']
l_tmp = []
d_code_name = {}
for i in l_sheet:
    l_1 = Openpyxl_PO.getOneCol('A', varSheet=i)
    l_2 = Openpyxl_PO.getOneCol('B', varSheet=i)
    d_ = dict(zip(l_1, l_2))
    d_code_name.update(d_)
    l_tmp = l_tmp + l_1
# print(l_tmp)

print(d_code_name)  # {'code': 'name', '000002': '万  科Ａ', '000004':

l_all = List_PO.getDuplicationCount(l_tmp)
print(l_all)  # [('code', 4), ('002423', 4), ('000158', 3),

d_2 = {}
for i in range(len(l_all)):
    if l_all[i][0] in d_code_name:
        if l_all[i][1] > 2:
            print(l_all[i][0], d_code_name[l_all[i][0]])









