# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-11-17
# Description: 获取当天上影线，放量，日周线（5穿21穿55），
# 步骤：
# 1，手工从深圳交易证券所下载每日数据源，深圳交易证券所 https://www.szse.cn/market/trend/index.html
# 2，遍历数据，（最高价-最低价）* 0。65 < 收盘价
# 3，输出。
# 备注： 获取历史成交量，需要下载历史数据源
# *****************************************************************
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl.styles.stylesheet")

from PO.OpenpyxlPO import *


from PO.TimePO import *
Time_PO = TimePO()

from PO.ColorPO import *
Color_PO = ColorPO()


Openpyxl_PO = OpenpyxlPO("/Users/linghuchong/Downloads/51/Python/stock/sz/股票行情.xlsx")

row, col = (Openpyxl_PO.getTotalRowCol())  # [2917, 12]
# print(Openpyxl_PO.getOneRow(2))
# l_ = Openpyxl_PO.getOneRow(2)
# # 交易日期	证券代码	证券简称	前收	开盘	最高	最低	今收	涨跌幅（%）	成交量(万股)	成交金额(万元)	市盈率
# # ['2025-11-17', '000001', '平安银行', '11.75', '11.75', '11.75', '11.62', '11.67', '-0.68', '9,952.32', '116,141.62', '5.44']
# # 条件是涨跌幅（%） >0,
# # (最高价-（最高价-最低价）* 0。35) > 收盘价  and # 收盘价 > (最高价-（最高价-最低价）*0。5)
# if l_[8] > 0 :
#     if ((l_[5] - (l_[5] - l_[6])*0.35) > l_[7]) and (l_[7] > (l_[5]-(l_[5] - l_[6])*0.5)):
#         print(l_[1],l_[2],l_[9])

for i in range(2,row):
    # print(Openpyxl_PO.getOneRow(i))
    l_ = Openpyxl_PO.getOneRow(i)
    if int(float(l_[8])) > 0:
        if ((float(l_[5]) - (float(l_[5]) - float(l_[6])) * 0.35) > float(l_[7])) and\
                (float(l_[7]) > (float(l_[5]) - (float(l_[5]) - float(l_[6])) * 0.5)) and\
                float(l_[6]) > (float(l_[4]) - (float(l_[4]) * 0.01)) and\
                float(l_[7]) < 30 and float(l_[7]) > 10:
            print(l_[1], l_[2], l_[9])

# 000158 常山北明 9,738.86
# 000657 中钨高新 7,857.92
# 000681 视觉中国 3,317.42
# 002037 保利联合 1,214.94
# 002068 黑猫股份 6,086.51
# 002095 生 意 宝 471.57
# 002209 达 意 隆 3,162.08
# 002984 森麒麟 1,644.29
# 300161 华中数控 431.06
# 300170 汉得信息 5,445.94
# 300174 元力股份 2,191.69
# 300184 力源信息 2,944.51
# 300252 金信诺 2,698.67
# 300293 蓝英装备 397.25
# 300333 兆日科技 3,870.73
# 300337 银邦股份 3,419.04
# 300397 天和防务 7,564.15
# 300465 高伟达 4,960.51
# 300490 华自科技 6,220.38
# 300499 高澜股份 1,752.84
# 300523 辰安科技 411.97
# 300525 博思软件 3,723.98
# 300581 晨曦航空 6,619.62
# 300602 飞荣达 1,613.95
# 300721 怡达股份 786.68
# 300762 上海瀚讯 3,661.72
# 301019 宁波色母 1,831.17
# 301059 金三江 510.64
# 301172 君逸数码 736.45
# 301193 家联科技 356.09
# 301265 华新环保 452.48
# 301566 达利凯普 993.95

