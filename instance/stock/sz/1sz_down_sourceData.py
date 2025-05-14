# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 深圳，第一轮筛选stock
# 步骤：
# 1，手工从深圳交易证券所下载每日数据源，深圳交易证券所 https://www.szse.cn/market/trend/index.html
# 2，匹配连续2天（如0422.xlsx和0423.xlsx两个文件）的数据，筛选出符合要求的stock
# /Users/linghuchong/Downloads/51/Python/stock
# 3，保存到sz.json
# *****************************************************************
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl.styles.stylesheet")

from PO.OpenpyxlPO import *

from PO.WebPO import *

from PO.TimePO import *
Time_PO = TimePO()

from PO.ColorPO import *
Color_PO = ColorPO()




varUrl = "https://www.szse.cn/market/trend/index.html"
Web_PO = WebPO("chrome")
Web_PO.openURL(varUrl)

# 选择时间
Web_PO.clkByX("/html/body/div[5]/div/div/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/input")
Web_PO.clkByX("/html/body/div[5]/div/div/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/ul/div[2]/div/div/table/tbody/tr[1]/td[2]/div")

Web_PO.clkByX("/html/body/div[5]/div/div/div[2]/div[2]/div[2]/div[2]/div/div[3]/div/input")
Web_PO.clkByX("/html/body/div[5]/div/div/div[2]/div[2]/div[2]/div[2]/div/div[3]/div/ul/div[2]/div/div/table/tbody/tr[1]/td[2]/div")

# 查询和下载
Web_PO.clkByX("/html/body/div[5]/div/div/div[2]/div[2]/div[2]/div[2]/div/div[6]/button")
Web_PO.clkByX("/html/body/div[5]/div/div/div[2]/div[2]/div[2]/div[4]/div/div[1]/div[2]/a")

Web_PO.exportExistFile('/Users/linghuchong/Desktop/ttt.xlsx')
