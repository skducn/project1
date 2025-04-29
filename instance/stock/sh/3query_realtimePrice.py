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

import logging

excelFile = "4save_stock.xlsx"
logName = "5sh.log"


# 创建一个日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 创建一个文件处理器
file_handler = logging.FileHandler(logName)
# file_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.INFO)

# 创建一个控制台处理器
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.INFO)

# 定义日志格式
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
# console_handler.setFormatter(formatter)

# 将处理器添加到日志记录器
logger.addHandler(file_handler)
# logger.addHandler(console_handler)

def run(d_stock):

    try:

        # 第二轮筛选，将第一轮筛选出的股票与时事动态价格比较，得到符合条件的结果
        l_dd = []
        l_tmp = list(d_stock.keys())

        l_result = []

        # 获取上一个交易日与上上交易日的数据
        varCurrMD = Time_PO.getMonth() + Time_PO.getDay()
        varYMD2 = (Time_PO.getPreviousWorkingDay([2025, int(varCurrMD[:2]), int(varCurrMD[2:])]))  # 2025-04-28
        l_varYMD2 = str(varYMD2).split("-")
        varMD2 = str(l_varYMD2[1]) + str(l_varYMD2[2])

        # 通过varMD2获取上一个工作日，如今天是0429，varMD2=0428
        # varYMD2file = varMD2 + ".xlsx"
        varYMD1 = (Time_PO.getPreviousWorkingDay([2025, int(varMD2[:2]), int(varMD2[2:])]))  # 2025-04-28
        l_varYMD1 = str(varYMD1).split("-")
        varMD1 = str(l_varYMD1[1]) + str(l_varYMD1[2])

        varTitle = str(varMD1) + " - " + str(varMD2)
        l_result.append(varTitle)

        Color_PO.outColor([{"35": "sh > 实时查询 " + str(Time_PO.getDateTimeByDivide()) + " > " + varTitle +  " > " + str(len(d_stock)) }])
        logger.info("sz > 实时查询 " + str(Time_PO.getDateTimeByDivide()) + " > " + varTitle + " > " + str(len(d_stock)))
        logger.info(d_stock)

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

            if float(d_curr['换手']) > 3 and d_curr['市盈率'] != '亏损' and \
                    float(d_curr['涨幅']) > 2 and float(d_curr['涨幅']) < 9 and \
                    float(d_curr['现价']) < 30 and float(d_curr['市盈率']) < 100:
                # print(i + 1, d_curr, varUrl)
                l_dd.append(l_tmp[i])
                if float(d_curr['涨幅']) < 0:
                    Color_PO.outColor([{"32": str(i + 1) + "，" + str(d_curr) + "，" + "https://xueqiu.com/S/SH" + str(
                        l_tmp[i]) + " , " + d_tmp[str(l_tmp[i])]}])
                    varUrl = "https://xueqiu.com/S/SH" + str(l_tmp[i])
                    l_result.append(varUrl)
                else:
                    Color_PO.outColor([{"31": str(i + 1) + "，" + str(d_curr) + "，" + "https://xueqiu.com/S/SH" + str(
                        l_tmp[i]) + " , " + d_tmp[str(l_tmp[i])]}])
                    varUrl = "https://xueqiu.com/S/SH" + str(l_tmp[i])
                    l_result.append(varUrl)
                logger.info(str(d_curr) + " , " + "https://xueqiu.com/S/SZ" + str(l_tmp[i]) + " , " + d_stock[str(l_tmp[i])])

                Openpyxl_PO3 = OpenpyxlPO(excelFile)
                l_row_data = Openpyxl_PO3.getOneRow(1)
                # print(l_row_data)  # ['0423 ~ 0424', '0424 ~ 0425', '0425 - 04289', '0425 ~ 04289', '0425 ~ 04289']
                if varTitle not in l_row_data:
                    Openpyxl_PO3.insertCols({"a": l_result})
                else:
                    l_col = Openpyxl_PO3.getTitleColSeq([varTitle])
                    # print('第几列：',l_col)
                    l_col_data = Openpyxl_PO3.getOneCol(l_col[0])
                    # print(l_col_data)  # ['0425 - 0428', 'https://xueqiu.com/S/SZ002564', None, None, None, None, None, None, None, None, None, None, None, None, None]
                    l_col_data = List_PO.delDuplicateElement(l_col_data)
                    # print(l_col_data) # ['0425 - 0428', 'https://xueqiu.com/S/SZ002564'
                    for i in range(len(l_result)):
                        if l_result[i] not in l_col_data:
                            # print(len(l_col_data)+1, l_col[0], l_result[i])
                            Openpyxl_PO3.setCell(len(l_col_data) + 1, l_col[0], l_result[i])
                    Openpyxl_PO3.save()

        print("已保存", excelFile)

        if os.name == 'nt':
            os.system("start " + excelFile)
        else:
            os.system("open " + excelFile)

    except Exception as e:
        logger.error(f"发生错误: {e}")

if __name__ == "__main__":
    # 4-29
    # d_stock = {'000630': '铜陵有色', '000953': '河化股份', '001259': '利仁科技', '002165': '红 宝 丽',
    #            '002278': '神开股份', '002564': '天沃科技', '002592': 'ST八菱', '002827': '高争民爆', '002836': '新宏泽',
    #            '003007': '直真科技', '003017': '大洋生物', '300263': '隆华科技', '300442': '润泽科技',
    #            '300661': '圣邦股份', '300666': '江丰电子', '300789': '唐源电气', '300870': '欧陆通',
    #            '301119': '正强股份', '301335': '天元宠物', '301529': '福赛科技'}

    run(d_stock)
