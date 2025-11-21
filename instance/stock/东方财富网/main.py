# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 东方财富网
# https://quote.eastmoney.com/center/gridlist.html#gem_board
# *****************************************************************

import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from multiprocessing import Pool, cpu_count
import time

from PO.ListPO import *
List_PO = ListPO()

from PO.ColorPO import *
Color_PO = ColorPO()

from PO.WebPO import *
from PO.NewexcelPO import *
from PO.OpenpyxlPO import *

Newexcel_PO = NewexcelPO("/Users/linghuchong/Downloads/创业板.xlsx")

Openpyxl_PO = OpenpyxlPO("/Users/linghuchong/Downloads/创业板.xlsx")
Openpyxl_PO.appendRows([['序号','代码','名称','相关链接1','相关链接2','相关链接3','最新价','涨跌幅','涨跌额','成交量(手)','成交额','振幅','最高','最低','今开','昨收','量比','换手率','市盈率(动态)','市净率']])


Web_PO = WebPO("chrome")
varUrl = "https://quote.eastmoney.com/center/gridlist.html#gem_board"
Web_PO.openURL(varUrl)

# 1,关闭广告
Web_PO.clkByX("/html/body/div[5]/img[1]")

# 2,获取总页数
varPage = Web_PO.getTextByX('//*[@id="mainc"]/div/div/div[4]/div/a[4]')
print(varPage)

# for i in range(varPage):

# # 跳到X页
# Web_PO.setTextEnterByX('//*[@id="mainc"]/div/div/div[4]/div/form/input[1]', 3,2)
# Web_PO.setTextEnterByX('//*[@id="mainc"]/div/div/div[4]/div/form/input[1]', 5,2)
# Web_PO.setTextEnterByX('//*[@id="mainc"]/div/div/div[4]/div/form/input[1]', 15,2)



l_data = Web_PO.getTextByXs('//*[@id="mainc"]/div/div/div[4]/table/tbody')
l_l_data = []
s_data = l_data[0]
l_data = s_data.replace('\n', ' ').split()
for i in range(0, len(l_data),20):
    l_l_data.append(l_data[i:i+20]  )

print(l_l_data)  # [['1', '301171', '易点天下', '股吧', '资金流', '数据', '39.97', '19.99%', '6.66', '145.78万', '55.40亿', '14.32%', '39.97', '35.20', '35.20', '33.31', '3.00', '38.27%', '69.49', '5.04'], ['2', '300087',...
 # [['1', '301171', '易点天下', '股吧', '资金流', '数据', '39.97', '19.99%', '6.66', '145.78万', '55.40亿', '14.32%', '39.97', '35.20', '35.20', '33.31', '3.00', '38.27%', '69.49', '5.04'], ['2', '300087',...
Openpyxl_PO.appendRows(l_l_data)


