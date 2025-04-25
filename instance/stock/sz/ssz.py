# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 执行两个文档数据
# 深圳交易证券所 https://www.szse.cn/market/trend/index.html
# 步骤：
# 1，获取0422.xlsx和0423.xlsx两个文件，从深圳交易证券所下载
# 2，执行 run("0423")  0423是文件名0423.xlsx
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

from PO.TimePO import *
Time_PO = TimePO()

def run(varMD2):

    # 通过varMD2获取上一个工作日，如0424获取到0423
    varYMD2file = varMD2 + ".xlsx"
    varYMD1 = (Time_PO.getPreviousWorkingDay([2025, int(varMD2[:2]), int(varMD2[2:])])) # 2025-04-23
    l_varYMD1 = str(varYMD1).split("-")
    varMD1 = str(l_varYMD1[1]) + str(l_varYMD1[2])
    varYMD1file = varMD1 + ".xlsx"

    # 判断两个文件是否存在
    if os.access(varYMD1file, os.F_OK) and os.access(varYMD2file, os.F_OK):

        l_result = []

        # 读取文件1
        Openpyxl_PO = OpenpyxlPO(varYMD1file)
        l_code = (Openpyxl_PO.getOneCol(2, '股票行情'))
        l_name = (Openpyxl_PO.getOneCol(3, '股票行情'))
        l_open = (Openpyxl_PO.getOneCol(5, '股票行情'))
        l_close = (Openpyxl_PO.getOneCol(8, '股票行情'))
        l_TV = (Openpyxl_PO.getOneCol(10, '股票行情'))
        l_TV_1 = []
        for i in range(len(l_TV)):
            l_TV_1.append(l_TV[i].replace(",", ""))
        l_PE = (Openpyxl_PO.getOneCol(12, '股票行情'))
        l_code.pop(0)
        l_name.pop(0)
        l_open.pop(0)
        l_close.pop(0)
        l_TV_1.pop(0)
        l_PE.pop(0)

        # 读取文件2
        Openpyxl_PO2 = OpenpyxlPO(varYMD2file)
        l_code2 = (Openpyxl_PO2.getOneCol(2, '股票行情'))
        l_name2 = (Openpyxl_PO2.getOneCol(3, '股票行情'))
        l_open2 = (Openpyxl_PO2.getOneCol(5, '股票行情'))
        l_close2 = (Openpyxl_PO2.getOneCol(8, '股票行情'))
        l_TV2 = (Openpyxl_PO2.getOneCol(10, '股票行情'))
        l_TV_2 = []
        for i in range(len(l_TV2)):
            l_TV_2.append(l_TV2[i].replace(",", ""))
        l_PE2 = (Openpyxl_PO2.getOneCol(12, '股票行情'))
        l_PE2_2 = []
        for i in range(len(l_PE2)):
            l_PE2_2.append(l_PE2[i].replace(",", ""))
        l_code2.pop(0)
        l_name2.pop(0)
        l_open2.pop(0)
        l_close2.pop(0)
        l_TV_2.pop(0)
        l_PE2.pop(0)
        l_PE2_2.pop(0)

        # 第一轮筛选，两文件比较筛选符合条件的股票列表
        l_tmp = []
        d_tmp = {}
        for i in range(len(l_code)):
            for j in range(len(l_code2)):
                if l_code[i] == l_code2[j]:
                    if float(l_open[i]) > float(l_close[i]) and\
                            float(l_close2[j]) > ((float(l_open[i]) - float(l_close[i])) * 0.8 + float(l_close[i])) and\
                            float(l_TV_1[i]) > float(l_TV_2[j]) and float(l_PE2_2[i]) > 1:
                        if int(l_code[i]) > 300000 or int(l_code[i]) < 100000:
                            l_tmp.append(l_code[i])
                            d_tmp[l_code[i]] = l_name[i]
        varData = str(varMD1) + " ~ " + str(varMD2)
        l_result.append(varData)
        Color_PO.outColor([{"35": "sz => [" + str(varMD1) + ' ~ ' + str(varMD2) + ']' + " => "+ str(len(l_tmp)) + "条"}])
        # print(len(l_tmp)) # [0424 ~ 0425] => 114条

        # 第二轮筛选，将第一轮筛选出的股票与时事动态价格比较，得到符合条件的结果
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
                    float(d_curr['涨幅']) > 2 and float(d_curr['涨幅']) < 9 and\
                    float(d_curr['现价']) < 30 and float(d_curr['市盈率']) < 100:
                # print(i + 1, d_curr, varUrl)
                l_dd.append(l_tmp[i])
                if float(d_curr['涨幅']) < 0:
                    Color_PO.outColor([{"32": str(i + 1) + " , " + str(d_curr) + " , " + "https://xueqiu.com/S/SZ" + str(l_tmp[i]) + " , " + d_tmp[str(l_tmp[i])]}])
                    varUrl = "https://xueqiu.com/S/SZ" + str(l_tmp[i])
                    l_result.append(varUrl)
                else:
                    Color_PO.outColor([{"31": str(i + 1) + " , " + str(d_curr) + " , " + "https://xueqiu.com/S/SZ" + str(l_tmp[i]) + " , " + d_tmp[str(l_tmp[i])]}])
                    varUrl = "https://xueqiu.com/S/SZ" + str(l_tmp[i])
                    l_result.append(varUrl)

        Openpyxl_PO3 = OpenpyxlPO("history_sz.xlsx")
        Openpyxl_PO3.appendCols([l_result])
    else:
        if os.access(varYMD1file, os.F_OK) == False :
            Color_PO.outColor([{"31": "errorrrrrrrrrr, " + str(varMD1) + " 文件不存在！"}])
        if os.access(varYMD2file, os.F_OK) == False :
            Color_PO.outColor([{"31": "errorrrrrrrrrr, " + str(varMD2) + " 文件不存在！"}])

if __name__ == "__main__":

    run(Time_PO.getMonth() + Time_PO.getDay())
