# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 深圳，获取上一日下跌且符合条件的票
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


# 序号	代码	名称	相关链接	最新价	涨跌幅	涨跌额	成交量(手)	成交额	振幅	最高	最低	今开	昨收	量比	换手率	市盈率(动态)	市净率
def run():

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
    run('0527.xlsx')

except Exception as e:
    print(f"发生错误: {e}")
    Log_PO.logger.error(f"发生错误: {e}")
