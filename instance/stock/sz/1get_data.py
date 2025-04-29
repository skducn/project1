# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 执行两个文档数据
# 深圳交易证券所 https://www.szse.cn/market/trend/index.html
# https://stockpage.10jqka.com.cn/realHead_v2.html#hs_000120
#
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

from PO.OpenpyxlPO import *

from PO.WebPO import *

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
    varYMD1 = (Time_PO.getPreviousWorkingDay([2025, int(varMD2[:2]), int(varMD2[2:])])) # 2025-04-28
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

    # 判断两个文件是否存在
    if os.access(varYMD1file, os.F_OK) and os.access(varYMD2file, os.F_OK):

        try:
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

        except Exception as e:
            print(f"Error reading files: {e}")
            sys.exit(1)


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

        varTitle = str(varMD1) + " - " + str(varMD2)
        Color_PO.outColor([{"35": "sz > [" + varTitle + ']' + " > " + str(len(l_tmp))}])
        # print(l_tmp)  # ['000630', '000953', '001259',...
        print("d_stock =", d_tmp)  # {'000630': '铜陵有色', '000953': '河化股份',

    else:
        if os.access(varYMD1file, os.F_OK) == False :
            Color_PO.outColor([{"31": "errorrrrrrrrrr, " + str(varMD1) + " 文件不存在！"}])
        if os.access(varYMD2file, os.F_OK) == False :
            Color_PO.outColor([{"31": "errorrrrrrrrrr, " + str(varMD2) + " 文件不存在！"}])

if __name__ == "__main__":

    run()
