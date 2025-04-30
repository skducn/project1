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
import os,json
from PO.OpenpyxlPO import *

jsonFile = 'test.json'

# 1, 读取 JSON 文件
try:
    # 打开 JSON 文件
    with open(jsonFile, 'r', encoding='utf-8') as file:
        # 使用 json.load 函数将文件内容转换为字典
        d_stock = json.load(file)
    print("成功读取数据：")
    print(d_stock)
except FileNotFoundError:
    print(f"错误：未找到文件 {jsonFile}")
except json.JSONDecodeError:
    print(f"错误：无法解析 {jsonFile} 中的 JSON 数据")
except Exception as e:
    print(f"发生未知错误：{e}")

print(d_stock)

Openpyxl_PO = OpenpyxlPO("d:\\51\\python\\stock\\sh\\0428.xlsx")
Openpyxl_PO.insertRows(d_stock)

