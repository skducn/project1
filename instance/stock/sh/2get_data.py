# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 执行两个文档数据
# 步骤：
# 1，2025-04-23.xlsx和2025-04-24.xlsx两个文件
# 2，执行 run("4-22", "4-23")
# 第一轮筛选逻辑：
# https://stockpage.10jqka.com.cn/realHead_v2.html#hs_000120
# https://www.sse.com.cn/market/price/report/
# *****************************************************************
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl.styles.stylesheet")

from PO.WebPO import *

from PO.OpenpyxlPO import *

from PO.TimePO import *
Time_PO = TimePO()

from PO.ColorPO import *
Color_PO = ColorPO()


def run():


    # 获取上一个交易日与上上交易日的数据
    varCurrMD = Time_PO.getMonth() + Time_PO.getDay()
    varYMD2 = (Time_PO.getPreviousWorkingDay([2025, int(varCurrMD[:2]), int(varCurrMD[2:])]))  # 2025-04-28
    l_varYMD2 = str(varYMD2).split("-")
    varMD2 = str(l_varYMD2[1]) + str(l_varYMD2[2])
    varYMD2file = varMD2 + ".xlsx"

    # 通过varMD2获取上一个工作日，如今天是0429，varMD2=0428
    # varYMD2file = varMD2 + ".xlsx"
    varYMD1 = (Time_PO.getPreviousWorkingDay([2025, int(varMD2[:2]), int(varMD2[2:])]))  # 2025-04-28
    l_varYMD1 = str(varYMD1).split("-")
    varMD1 = str(l_varYMD1[1]) + str(l_varYMD1[2])
    varYMD1file = varMD1 + ".xlsx"

    # print(varYMD1file)
    # print(varYMD2file)

    # 下载的数据文件放在project之外，不被git
    if os.name == "nt":
        varYMD1file = "D:\\51\\python\\stock\\sz\\" + varYMD1file
        varYMD2file = "D:\\51\\python\\stock\\sz\\" + varYMD2file
    else:
        varYMD1file = "/Users/linghuchong/Downloads/51/Python/stock/sz/" + varYMD1file
        varYMD2file = "/Users/linghuchong/Downloads/51/Python/stock/sz/" + varYMD2file


    # 判断文件是否存在
    if os.access(varYMD1file, os.F_OK) and os.access(varYMD2file, os.F_OK):

        l_result = []

        # 读取表格1
        Openpyxl_PO = OpenpyxlPO(varYMD1file)
        l_code = (Openpyxl_PO.getOneCol(2, 'Sheet1'))
        l_name = (Openpyxl_PO.getOneCol(3, 'Sheet1'))
        l_open = (Openpyxl_PO.getOneCol(11, 'Sheet1'))
        l_close = (Openpyxl_PO.getOneCol(5, 'Sheet1'))
        l_TV = (Openpyxl_PO.getOneCol(8, 'Sheet1'))
        l_code.pop(0)
        l_name.pop(0)
        l_open.pop(0)
        l_close.pop(0)
        l_TV.pop(0)

        # 读取表格2
        Openpyxl_PO2 = OpenpyxlPO(varYMD2file)
        l_code2 = (Openpyxl_PO2.getOneCol(2, 'Sheet1'))
        l_name2 = (Openpyxl_PO2.getOneCol(3, 'Sheet1'))
        l_open2 = (Openpyxl_PO2.getOneCol(11, 'Sheet1'))
        l_close2 = (Openpyxl_PO2.getOneCol(5, 'Sheet1'))
        l_TV2 = (Openpyxl_PO2.getOneCol(8, 'Sheet1'))
        l_code2.pop(0)
        l_name2.pop(0)
        l_open2.pop(0)
        l_close2.pop(0)
        l_TV2.pop(0)

        # 筛选符合条件的
        l_tmp = []
        d_tmp = {}
        for i in range(len(l_code)):
            for j in range(len(l_code2)):
                if l_code[i] == l_code2[j]:
                    if float(l_open[i]) > float(l_close[i]) and \
                            float(l_close2[j]) > ((float(l_open[i]) - float(l_close[i])) * 0.8 + float(l_close[i])) and \
                            float(l_TV[i]) > float(l_TV2[j]):
                        l_tmp.append(l_code[i])
                        d_tmp[l_code[i]] = l_name[i]

        varTitle = str(varMD1) + " - " + str(varMD2)
        Color_PO.outColor([{"35": "sh > [" + varTitle + ']' + " > " + str(len(l_tmp))}])
        # print(l_tmp)
        print("d_stock =", d_tmp)

    else:
        if os.access(varYMD1file, os.F_OK) == False:
            Color_PO.outColor([{"31": "errorrrrrrrrrr, " + str(varMD1) + " 文件不存在！"}])
        if os.access(varYMD2file, os.F_OK) == False:
            Color_PO.outColor([{"31": "errorrrrrrrrrr, " + str(varMD2) + " 文件不存在！"}])

if __name__ == "__main__":

    run()
