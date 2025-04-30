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

os.system("open /Users/linghuchong/Downloads/51/Python/stock/sh")
