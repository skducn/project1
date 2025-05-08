# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 深圳，第一轮筛选stock
# 步骤：
# 1，手工从深圳交易证券所下载每日数据源，深圳交易证券所 https://www.szse.cn/market/trend/index.html
# 2，匹配连续2天（如0422.xlsx和0423.xlsx两个文件）的数据，筛选出符合要求的stock
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

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')
from PO.LogPO import *
Log_PO = LogPO(filename=Configparser_PO.DATA("logfile"), level="info")
jsonFile = Configparser_PO.DATA("jsonfile")  # 第一轮筛选stock的文件


def run(varYMD1file='', varYMD2file=''):



    # 获取上一个交易日与上上交易日的数据
    if varYMD2file == '':
        varCurrMD = Time_PO.getMonth() + Time_PO.getDay()
        varYMD2 = (Time_PO.getPreviousWorkingDay([2025, int(varCurrMD[:2]), int(varCurrMD[2:])]))  # 2025-04-28
        l_varYMD2 = str(varYMD2).split("-")
        varMD2 = str(l_varYMD2[1]) + str(l_varYMD2[2])
        varYMD2file = varMD2 + ".xlsx"

    if varYMD1file == '':
        # 通过varMD2获取上一个工作日，如今天是0429，varMD2=0428
        # varYMD2file = varMD2 + ".xlsx"
        varYMD1 = (Time_PO.getPreviousWorkingDay([2025, int(varMD2[:2]), int(varMD2[2:])])) # 2025-04-28
        l_varYMD1 = str(varYMD1).split("-")
        varMD1 = str(l_varYMD1[1]) + str(l_varYMD1[2])
        varYMD1file = varMD1 + ".xlsx"



    # 下载的数据文件放在project之外，不被git
    if os.name == "nt":
        varYMD1file_path = Configparser_PO.PATH("nt") + varYMD1file
        varYMD2file_path = Configparser_PO.PATH("nt") + varYMD2file
    else:
        varYMD1file_path = Configparser_PO.PATH("mac") + varYMD1file
        varYMD2file_path = Configparser_PO.PATH("mac") + varYMD2file

    print(varYMD1file_path)
    print(varYMD2file_path)

    # 判断两个文件是否存在
    if os.access(varYMD1file_path, os.F_OK) and os.access(varYMD2file_path, os.F_OK):

        try:
            # 读取文件1
            Openpyxl_PO = OpenpyxlPO(varYMD1file_path)
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
            Openpyxl_PO2 = OpenpyxlPO(varYMD2file_path)
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

        varTitle = str(varYMD1file) + " - " + str(varYMD2file)
        Color_PO.outColor([{"35": "sz > [" + varTitle + ']' + " > " + str(len(l_tmp)) + "个"}])
        Log_PO.logger.info("sz > [" + varTitle + ']' + " > " + str(len(l_tmp)))

        d_tmp['date'] = varTitle
        print("d_stock =", d_tmp)
        # Log_PO.logger.info("d_stock =" +  str(d_tmp))
        Log_PO.logger.warning("d_stock =" + str(d_tmp))

        try:
            # 打开文件并写入 JSON 数据
            with open(jsonFile, 'w', encoding='utf-8') as file:
                # 使用 json.dump 将字典写入文件
                json.dump(d_tmp, file, ensure_ascii=False, indent=4)
            # print(f"数据已成功保存到 {jsonFile}")
            Color_PO.outColor([{"35": f"数据已成功保存到 {jsonFile}"}])
        except Exception as e:
            print(f"保存文件时出现错误: {e}")


    else:
        if os.access(varYMD1file_path, os.F_OK) == False :
            Color_PO.outColor([{"31": "errorrrrrrrrrr, " + str(varYMD1file) + " 文件不存在！"}])
        if os.access(varYMD2file_path, os.F_OK) == False :
            Color_PO.outColor([{"31": "errorrrrrrrrrr, " + str(varYMD2file) + " 文件不存在！"}])


try:
    # run()
    run("0506.xlsx", '0507.xlsx')

except Exception as e:
    print(f"发生错误: {e}")
    Log_PO.logger.error(f"发生错误: {e}")
