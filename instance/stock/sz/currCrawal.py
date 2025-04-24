# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 时事爬取网站当天某股票收盘价，开盘价，成交量
# 需求，打开all.xlsx 获取上海股票代码，遍历获取上一日和当天的收盘价，开盘价，成交量，
# 判断，当天收盘价 大于 上一日的开盘价，且成交量小于上一日的票。
# 参考：https://quote.eastmoney.com/sz002494.html#fullScreenChart
# *****************************************************************

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from multiprocessing import Pool, cpu_count
import time

import tushare as ts
from PO.ListPO import *
List_PO = ListPO()


from PO.ColorPO import *
Color_PO = ColorPO()

from PO.WebPO import *

# l_tmp = ['003042', '300004', '300069', '300096', '300103', '300132', '300162', '300193', '300195', '300220', '300224', '300293', '300335', '300340', '300354', '300363', '300373', '300376', '300388', '300389', '300404', '300407', '300425', '300434', '300440', '300455', '300456', '300474', '300510', '300513', '300546', '300549', '300582', '300585', '300594', '300604', '300606', '300612', '300623', '300633', '300637', '300639', '300640', '300650', '300655', '300669', '300692', '300701', '300705', '300707', '300708', '300726', '300736', '300740', '300747', '300748', '300784', '300791', '300804', '300821', '300826', '300829', '300830', '300839', '300848', '300851', '300860', '300861', '300865', '300868', '300885', '300886', '300889', '300891', '300894', '300897', '300915', '300927', '300957', '300966', '300967', '300985', '300998', '301019', '301035', '301036', '301056', '301059', '301075', '301077', '301078', '301100', '301123', '301175', '301197', '301211', '301223', '301226', '301230', '301235', '301268', '301269', '301297', '301322', '301332', '301383', '301386', '301387', '301388', '301390', '301395', '301507', '301520', '301522', '301539', '301555', '301581', '301588', '301592', '301613', '301622', '301631']

def aa():
    l_3 = []
    # print(s_tmp,type(s_tmp))
    # s_tmp = "['003042', '300004']"
    # l_tmp = eval(s_tmp)

    l_tmp = ['300004', '002132']
    for i in l_tmp:
        Web_PO = WebPO("noChrome")
        # varUrl = "https://quote.eastmoney.com/sz" + str(i) + ".html#fullScreenChart"
        varUrl = "https://quote.eastmoney.com/basic/h5chart-iframe.html?code=" + str(i)
        Web_PO.openURL(varUrl)
        print(varUrl)

# fsc_iframe
#         ele = Web_PO.getEleByClassName("fsc_iframe")
#         if Web_PO.isEleExistByX('//html/body/div[9]/div[3]/iframe'):
#             print(1111)
#             Web_PO.swhIframeByX("//div[@class='fsc_iframe']/iframe")
#
#             # Web_PO.swhIframeByX("//html/body/div[9]/div[3]/iframe")
#             ele = Web_PO.getEleById('h5chartheadwrapcyb')
#             l_1 = Web_PO.eleGetTextByXs(ele, './/table/tbody/tr[1]')
#             l_2 = Web_PO.eleGetTextByXs(ele, './/table/tbody/tr[2]')
#             print(l_1)
#             print(l_2)
#             hsl = l_1[0].split("换手：")[1].split("%")[0]
#             lb = l_2[0].split("量比：")[1].split(" 成交额")[0]
#             if float(hsl) > 3 and float(lb) > 1:
#                 print(i)
#                 l_3.append(i)
#         elif Web_PO.isEleExistByX('//html/body/div[5]/div[3]/iframe'):
            # /html/body/div[9]/div[3]/iframe
            # print(333)


        # Web_PO.swhIframeByX("//div[@class='fsc_iframe']/iframe", 3)

        # Web_PO.swhIframeByX("//html/body/div[5]/div[3]/iframe")
        if Web_PO.isEleExistById("h5chartheadwrap"):
            ele = Web_PO.getEleById('h5chartheadwrap')
            print(111)
        elif Web_PO.isEleExistById("h5chartheadwrapcyb"):
            print(222)
            # sleep(6)
            # 查找市盈率数据，根据网页结构，这里可能需要根据实际情况调整选择器
            # pe_ratio_element = Web_PO.getTextByX(By.XPATH, "//td[contains(text(), '市盈')]/following-sibling::td")
            # pe_ratio = pe_ratio_element.text.strip()
            # print(pe_ratio)
            # ele = Web_PO.getEleById('h5chartheadwrapcyb')
            # a = Web_PO.getTextByX("/html/body/div[2]/div/div/div[1]/div[1]/div[2]/table/tbody/tr[1]/td[1]",2)
            # print(a)
            # l_1 = Web_PO.eleGetTextByXs(ele, '//table')
            # print(l_1)
            sleep(4)
            # a = Web_PO.getTextByXs("//div[@class='hq-data clearfix']")
            a = Web_PO.getTextByXs("//div[@class='clearfix hq-data-table fl']")
            # a = Web_PO.getTextByX("//table/tbody/tr",2)
            print(a)

        # l_1 = Web_PO.eleGetTextByXs(ele, './/table/tbody/tr')
        # /html/body/div[2]/div/div/div[1]/div[1]/div[2]/table/tbody/tr[1]
        print(l_1)
        # /html/body/div[2]/div/div/div[1]/div[1]/div[2]/table/tbody/tr[1]/td[1]
        l_2 = Web_PO.eleGetTextByXs(ele, './/table/tbody/tr[2]')
        print(l_1)
        # open = l_1[0].split("今开：")[1].split("最高")[0]
        # TR = l_1[0].split("换手：")[1].split("%")[0]  # Turnover rate
        # TV = l_1[0].split("成交量：")[1].split("市盈")[0]  # trading volume
        # PER = l_1[0].split("市盈：")[1].split("总市值")[0]  # （price/earning ratio）
        #
        # print(l_2)
        # VR = l_2[0].split("量比：")[1].split(" 成交额")[0]  # Volume Ratio (VR)。
        #
        # print(open,TR,TV,PER,VR)
        # if float(hsl) > 3 and float(lb) > 1:
        #     print(i)
        #     l_3.append(i)

    # print(l_3)

if __name__ == "__main__":

    # aa(sys.argv[1])
    # cd /Users/linghuchong/Downloads/51/Python/project/instance/stock/sz
    # conda activate py310
    # python cliRun.py "['003042', '300004']"
    aa()
