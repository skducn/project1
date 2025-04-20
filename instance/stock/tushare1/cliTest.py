# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 获取某股票某日的收盘价，开盘价，成交量
# 需求，打开all.xlsx 获取上海股票代码，遍历获取上一日和当天的收盘价，开盘价，成交量，
# 判断，当天收盘价 大于 上一日的开盘价，且成交量小于上一日的票。
# *****************************************************************
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import tushare as ts
from PO.ListPO import *
List_PO = ListPO()

from PO.ColorPO import *
Color_PO = ColorPO()

from PO.OpenpyxlPO import *

# 初始化tushare pro接口，需要你自己的token
pro = ts.pro_api('894e80b70503f5cda0d86f75820c5871ff391cf7344e55931169bb2a')

# 获取上交所股票代码和名称
# data = pro.stock_basic(exchange='SSE', list_status='L', fields='ts_code,symbol,name')
# 获取深交所股票代码和名称
# data = pro.stock_basic(exchange='SZSE', list_status='L', fields='symbol,name')
# # 打印结果
# for index, row in data.iterrows():
#     print(f"股票代码: {row['symbol']}, 股票名称: {row['name']}")
#
# sys.exit(0)


Openpyxl_PO = OpenpyxlPO("all.xlsx")
# print(Openpyxl_PO.getOneCol(1, 'sh1'))  # ['600000, 浦发银行', '600004, 白云机场',...
l_sh_stock = (Openpyxl_PO.getOneCol(1, 'sh1'))
d_sh_stock = {}
for i in l_sh_stock:
    d_sh_stock[str(i).split(",")[0]] = str(i).split(",")[1].strip()
# print(d_sh_stock)

d_stock = {key: value for key, value in d_sh_stock.items() if 'ST' not in value}
# print(d_stock)  # {'600000': '浦发银行', '600004': '白云机场',
# 股票代码
l_code = list(d_stock.keys())  # ['600000', '600004', ...

# print(l_code)

# sys.exit(0)

# 排除ST
# 600234, *ST科新
# 600287, ST舜天
# 600289, *ST信通
# 600358, ST联合
# 600360, ST华微
# 600365, ST通葡
# 600599, ST熊猫
# 600603, ST广物
# 600608, ST沪科
# 600671, ST目药
# 600711, ST盛屯
# 600715, *ST文投
# 600804, *ST鹏博
# 600811, *ST东方
# 600831, ST广网
# 603003, *ST龙宇
# 603007, ST花王
# 603363, *ST傲农
# 603377, ST东时
# 603557, ST起步
# 603559, *ST通脉
# 603828, ST柯利达
# 603869, ST智知
# 603959, ST百利

# 股票代码
# l_code = ['600590', '601699']



def getPrice(trade_date1, trade_date2):
    d_ = {}
    d_all = {}
    for index,i in enumerate(l_code):
        ts_code = str(i) + '.SH'
        sleep(1)
        # print(index, ts_code)
        # 判断上一日和当日是否有值）（忽略停牌等）
        # l_code.remove('600590')
        try:
        # df3 = pro.daily_basic(ts_code=ts_code, trade_date=trade_date1, fields='ts_code,trade_date,pe,pe_ttm')
        # print(f"静态市盈率: {df3['pe'].values[0]}", f"动态市盈率: {df3['pe_ttm'].values[0]}")

            df = pro.daily(ts_code=ts_code, trade_date=trade_date1)
            df2 = pro.daily(ts_code=ts_code, trade_date=trade_date2)
            # print(index, ts_code, trade_date1,df['open'].values[0],df['close'].values[0],df['vol'].values[0],trade_date2,df2['open'].values[0],df2['close'].values[0],df2['vol'].values[0])
            # 331 600475.SH 20250407 8.9 8.34 156918.28 20250408 8.41 8.56 97768.28
            d_['last_date'] = trade_date1
            d_['last_open'] = df['open'].values[0]
            d_['last_close'] = df['close'].values[0]
            d_['last_vol'] = df['vol'].values[0]
            d_['next_date'] = trade_date2
            d_['next_open'] = df2['open'].values[0]
            d_['next_close'] = df2['close'].values[0]
            d_['next_vol'] = df2['vol'].values[0]
            # 判断，当天收盘价 大于 上一日的开盘价，且成交量小于上一日的票，且股价小于20
            if d_['last_open'] > d_['last_close'] and d_['next_close'] > ((d_['last_open'] - d_['last_close'])*0.8 + d_['last_close']) and d_['last_vol'] > d_['next_vol'] and d_['next_close'] < 30:
                Color_PO.consoleColor2({"35": str(index) + ", " + str(trade_date1) + " ~ " + str(trade_date2) + " => " + str(i)})
            d_all[i] = d_
            d_ = {}
        except:
            # Color_PO.consoleColor2({"31": "【warning】, " + str(i) + "，在" + str(trade_date1) + ' ~ ' + str(trade_date2) + "其中有一天停牌！"})
            pass
    return d_all


# d_all = getPrice('20250415', '20250416')
d_all = getPrice(sys.argv[1], sys.argv[2])
# print(d_all)
# print(getPrice('20250407','20250408'))
# d_tmp = {'601698': {'last_date': '20250407', 'last_open': 18.93, 'last_close': 17.8, 'last_vol': 435026.29, 'next_date': '20250408', 'next_open': 17.82,
#                     'next_close': 19.58, 'next_vol': 326117.31},
#          '601699': {'last_date': '20250407', 'last_open': 11.96, 'last_close': 11.15, 'last_vol': 337220.06, 'next_date': '20250408', 'next_open': 11.15,
#                     'next_close': 11.61, 'next_vol': 258629.51}}


# # 判断，当天收盘价 大于 上一日的开盘价，且成交量小于上一日的票。
# for k, v in d_all.items():
#     if v['next_close'] > v['last_open'] and v['last_vol'] > v['next_vol']:
#         print("OK", k)



