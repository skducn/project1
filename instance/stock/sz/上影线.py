# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-11-17
# Description: 获取当天上影线，放量，日周线（5穿21穿55），
# 步骤：
# 1，手工从深圳交易证券所下载每日数据源，深圳交易证券所 https://www.szse.cn/market/trend/index.html
# /Users/linghuchong/Downloads/51/Python/stock/sz/
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

XLSX = '/Users/linghuchong/Downloads/股票行情.xlsx'
if (os.access(XLSX, os.F_OK)):

    # 获取当天日期，如1118
    varDate = Time_PO.getMonth() + Time_PO.getDay()
    Openpyxl_PO = OpenpyxlPO(XLSX)
    row, col = (Openpyxl_PO.getTotalRowCol())  # [2917, 12]
    # # 交易日期	证券代码	证券简称	前收	开盘	最高	最低	今收	涨跌幅（%）	成交量(万股)	成交金额(万元)	市盈率
    # # ['2025-11-17', '000001', '平安银行', '11.75', '11.75', '11.75', '11.62', '11.67', '-0.68', '9,952.32', '116,141.62', '5.44']

    # todo 条件：
    # 1，条件是涨跌幅（%）>0, int(float(l_[8])) > 0
    # 2，上影线战实体0.35，(最高价-（最高价-最低价）* 0.35) > 收盘价 , ((float(l_[5]) - (float(l_[5]) - float(l_[6])) * 0.35) > float(l_[7]))
    # 3，(收盘价 > (最高价 -（最高价-最低价） * 0.5), (float(l_[7]) > (float(l_[5]) - (float(l_[5]) - float(l_[6])) * 0.5))
    # 4，下影线较短，最低价 > (开盘价 - 开盘价 * 0.01), float(l_[6]) > (float(l_[4]) - (float(l_[4]) * 0.01))
    # 5，价格，今收价格在区间[7,30] , float(l_[7]) < 30 and float(l_[7]) > 10:

    s = ''
    for i in range(2, row):
        l_ = Openpyxl_PO.getOneRow(i)
        if int(float(l_[8])) > 0:
            if ((float(l_[5]) - (float(l_[5]) - float(l_[6])) * 0.35) > float(l_[7])) and\
                    (float(l_[7]) > (float(l_[5]) - (float(l_[5]) - float(l_[6])) * 0.5)) and\
                    float(l_[6]) > (float(l_[4]) - (float(l_[4]) * 0.01)) and\
                    float(l_[7]) < 50 and float(l_[7]) > 10:
                print(l_[1], l_[2])
                s = l_[1] + "," + s
    print(s)

    # 打开文件并写入内容（w模式：覆盖原有内容，文件不存在则创建）
    varFile = "/Users/linghuchong/Desktop/stock/" + varDate + ".txt"
    with open(varFile, "w", encoding="utf-8") as f:
        f.write(s)

    # 删除文件
    os.remove(XLSX)
