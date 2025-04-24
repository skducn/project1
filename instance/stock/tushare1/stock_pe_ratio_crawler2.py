# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 获取股票的市盈率(动)和市净
# *****************************************************************
from PO.WebPO import *
# Web_PO = WebPO("Chrome")

def getStockInfo(varCode):
    Web_PO = WebPO("chrome")
    if int(varCode) < 599999:
        # Web_PO.openURL("https://quote.eastmoney.com/f1.html?newcode=0." + str(varCode))
        varUrl = "https://quote.eastmoney.com/sz" + str(varCode) + ".html#fullScreenChart"
    else:
        # Web_PO.openURL("https://quote.eastmoney.com/f1.html?newcode=1." + str(varCode))
        varUrl = "https://quote.eastmoney.com/sh" + str(varCode) + ".html#fullScreenChart"
    # print(varUrl)
    Web_PO.openURL(varUrl)

    # Web_PO.inIframeTopDiv()
    Web_PO.swhIframeByX("//html/body/div[5]/div[3]/iframe")

    ele = Web_PO.getEleById('h5chartheadwrap')
    l_1 = Web_PO.eleGetTextByXs(ele, './/table/tbody/tr[1]')
    print(l_1)
    sys.exit(0)
    # ele = Web_PO.getEleByClassName('clearfix hq-data-table fl')
    # l_1 = Web_PO.eleGetTextByXs(ele, './/tbody/tr')
    print(l_1[1])  # 今开:3.27 最高:3.29 涨停:3.56 换手:2.07% 成交量:28.92万 市盈:184.12 　总市值:45.69亿
    # print(l_1[1].split("市盈:")[1].split(" ")[0]) # 184.12
    PE = l_1[1].split("市盈:")[1].split(" ")[0]
    PE = l_1[1].split("市盈:")[1].split(" ")[0]
    TR = l_1[1].split("换手:")[1].split(" ")[0]

    l_2 = Web_PO.eleGetTextByXs(ele, '//tbody/tr[2]')
    # print(l_2[0])  # 昨收:3.24 最低:3.21 跌停:2.92 量比:1.00 成交额:9381万 市净:1.26 流通市值:45.62亿
    # print(l_2[0].split("市净:")[1].split(" ")[0])  # 1.26
    PB = l_2[0].split("市净:")[1].split(" ")[0]
    VR = l_2[0].split("量比:")[1].split(" ")[0]

    if float(PE) > 0 and float(PB) > 0:
        return PE, PB, TR, VR
    else:
        return 0, 0

(PE, PB, TR, VR) = getStockInfo('002132')
print(PE, PB, TR, VR)

