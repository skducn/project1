# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 执行两个文档数据
# 步骤：
# 1，2025-04-23.xlsx和2025-04-24.xlsx两个文件
# 2，执行 run("4-22", "4-23")
# 第一轮筛选逻辑：
# *****************************************************************
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl.styles.stylesheet")

from PO.ColorPO import *
Color_PO = ColorPO()

from PO.WebPO import *
from PO.OpenpyxlPO import *

def run(file1, file2):

    file11 = file1 + ".xlsx"
    file22 = file2 + ".xlsx"

    # 判断文件是否存在
    if os.access(file11, os.F_OK) and os.access(file22, os.F_OK):

        # 读取
        Openpyxl_PO = OpenpyxlPO(file11)
        l_code = (Openpyxl_PO.getOneCol(2, '股票行情'))
        l_open = (Openpyxl_PO.getOneCol(5, '股票行情'))
        l_close = (Openpyxl_PO.getOneCol(8, '股票行情'))
        l_TV = (Openpyxl_PO.getOneCol(10, '股票行情'))
        l_TV_1 = []
        for i in range(len(l_TV)):
            l_TV_1.append(l_TV[i].replace(",", ""))
        # print(l_TV_1)
        l_PE = (Openpyxl_PO.getOneCol(12, '股票行情'))

        Openpyxl_PO2 = OpenpyxlPO(file22)
        l_code2 = (Openpyxl_PO2.getOneCol(2, '股票行情'))
        l_open2 = (Openpyxl_PO2.getOneCol(5, '股票行情'))
        l_close2 = (Openpyxl_PO2.getOneCol(8, '股票行情'))
        l_TV2 = (Openpyxl_PO2.getOneCol(10, '股票行情'))
        l_TV_2 = []
        for i in range(len(l_TV2)):
            l_TV_2.append(l_TV2[i].replace(",", ""))
        # print(l_TV_2)
        l_PE2 = (Openpyxl_PO2.getOneCol(12, '股票行情'))
        l_PE2_2 = []
        for i in range(len(l_PE2)):
            l_PE2_2.append(l_PE2[i].replace(",", ""))

        # 去掉标题
        l_code.pop(0)  # ['600000', '600004', ...
        l_open.pop(0)
        l_close.pop(0)
        l_TV_1.pop(0)
        l_PE.pop(0)
        l_code2.pop(0) # ['600000', '600004', ...
        l_open2.pop(0)
        l_close2.pop(0)
        l_TV_2.pop(0)
        l_PE2.pop(0)
        l_PE2_2.pop(0)

        # 筛选符合条件的
        if len(l_code) == len(l_code2):
            s = 0
            l_tmp = []
            for i in range(len(l_code)):
                if l_code[i] == l_code2[i]:
                    if float(l_open[i]) > float(l_close[i]) and\
                            float(l_close2[i]) > ((float(l_open[i]) - float(l_close[i])) * 0.8 + float(l_close[i])) and\
                            float(l_TV_1[i]) > float(l_TV_2[i]) and float(l_PE2_2[i]) > 1:
                        # print(l_code[i], float(l_PE2_2[i]))
                    # if float(l_open[index]) > float(l_close[index]) and float(l_close2[index]) > float(l_open[index]) and float(l_TV_1[index]) > float(l_TV_2[index]) and float(l_PE2[index]) > 0:
                    #     varUrl = "https://quote.eastmoney.com/sz" + str(l_code[i]) + ".html#fullScreenChart"

                        if int(l_code[i]) > 300000 or int(l_code[i]) < 100000:
                            # Color_PO.consoleColor2({"35": str(s) + ", " + str(i) + ", " + str(l_code[i])})
                            l_tmp.append(l_code[i])
                        s = s + 1

        Color_PO.outColor([{"35": "[" + str(file1) + ' ~ ' + str(file2) + ']' + " => "+ str(len(l_tmp)) + "条"}])
        # print(len(l_tmp))
        l_dd = []
        for i in range(len(l_tmp)):
            varUrl = "https://stockpage.10jqka.com.cn/realHead_v2.html#hs_" + str(l_tmp[i])
            Web_PO = WebPO("noChrome")
            Web_PO.openURL(varUrl)
            sleep(1)
            d_curr = {}

            # 获取当前价格
            l_curr = Web_PO.getTextByXs("//div[@class='price_box fl icons_box']")
            l_curr = l_curr[0].split("\n")
            d_curr['现价'] = l_curr[0]
            d_curr['涨幅'] = l_curr[2].replace("%", "")

            l_1 = Web_PO.getTextByXs("//div[@class='new_detail fl']/ul/li[1]/span")
            # print(l_1)
            # d_curr['今开'] = l_1[0].replace('今开：','')
            # d_curr['成交量'] = l_1[1].replace('成交量：','').replace('万','').strip()

            l_2 = Web_PO.getTextByXs("//div[@class='new_detail fl']/ul/li[2]/span")
            # print(l_2)
            d_curr['换手'] = l_2[2].replace('换手：', '').replace('%', '').strip()

            # l_3 = Web_PO.getTextByXs("//div[@class='new_detail fl']/ul/li[3]/span")
            # print(l_3)
            # d_curr['市净率'] = l_3[2].replace('市净率：', '').strip()

            l_4 = Web_PO.getTextByXs("//div[@class='new_detail fl']/ul/li[4]/span")
            # print(l_4)
            d_curr['市盈率'] = l_4[2].replace('市盈率(动)：', '').strip()

            if float(d_curr['换手']) > 3 and d_curr['市盈率'] != '亏损'  and\
                    float(d_curr['涨幅']) > 3 and float(d_curr['涨幅']) < 9 and\
                    float(d_curr['现价']) < 30 and float(d_curr['市盈率']) < 100:
                # print(i + 1, d_curr, varUrl)
                l_dd.append(l_tmp[i])
                if float(d_curr['涨幅']) < 0:
                    Color_PO.outColor([{"32": str(i + 1) + "，" + str(d_curr) + "，" + "https://xueqiu.com/S/SZ" + str(l_tmp[i])}])
                else:
                    Color_PO.outColor([{"31": str(i + 1) + "，" + str(d_curr) + "，" + "https://xueqiu.com/S/SZ" + str(l_tmp[i])}])
    else:
        if os.access(file1, os.F_OK) == False :
            Color_PO.outColor([{"31": "errorrrrrrrrrr, " + str(file1) + " 文件不存在！"}])
        if os.access(file2, os.F_OK) == False :
            Color_PO.outColor([{"31": "errorrrrrrrrrr, " + str(file2) + " 文件不存在！"}])

if __name__ == "__main__":

    run("4-22", "4-23")
