# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 上海，第二轮筛选stock, 保存到sh.xlsx
# 上海证交所官网：https://www.sse.com.cn/market/price/report/
# 第一轮筛选逻辑：
# 匹配数据 https://stockpage.10jqka.com.cn/realHead_v2.html#hs_000120
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

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')
from PO.LogPO import *
Log_PO = LogPO(filename=Configparser_PO.DATA("logfile"), level="info")
jsonFile = Configparser_PO.DATA("jsonfile")  # 第一轮筛选stock的文件
excelFile = Configparser_PO.DATA("excelfile")  # 第二轮筛选stock后的文件


def run(d_data):

    # 1, 读取 JSON 文件
    try:
        # 打开 JSON 文件
        with open(jsonFile, 'r', encoding='utf-8') as file:
            # 使用 json.load 函数将文件内容转换为字典
            d_stock = json.load(file)
        print("成功读取数据：", d_stock)
    except FileNotFoundError:
        print(f"错误：未找到文件 {jsonFile}")
    except json.JSONDecodeError:
        print(f"错误：无法解析 {jsonFile} 中的 JSON 数据")
    except Exception as e:
        print(f"发生未知错误：{e}")

    try:
        # 第二轮筛选，将第一轮筛选出的股票与时事动态价格比较，得到符合条件的结果
        l_dd = []
        l_tmp = list(d_stock.keys())
        l_result = []

        varTitle = d_stock['date']
        varTitle = varTitle.replace(".xlsx","")
        # print(varTitle)
        l_result.append(varTitle)

        Color_PO.outColor([{"35": "sh > 实时查询 " + str(Time_PO.getDateTimeByDivide()) + " > " + varTitle +  " > " + str(len(d_stock)) + "个" }])
        Log_PO.logger.info("sz > 实时查询 " + str(Time_PO.getDateTimeByDivide()) + " > " + varTitle + " > " + str(len(d_stock)))
        Log_PO.logger.info(d_stock)

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
                    float(d_curr['涨幅']) > d_data['涨幅'][0] and float(d_curr['涨幅']) < d_data['涨幅'][1] and \
                    float(d_curr['现价']) < 30 and float(d_curr['市盈率']) < 100:
                # print(i + 1, d_curr, varUrl)
                l_dd.append(l_tmp[i])
                if float(d_curr['涨幅']) < 0:
                    Color_PO.outColor([{"32": str(i + 1) + "，" + str(d_curr) + "，" + "https://xueqiu.com/S/SH" + str(
                        l_tmp[i]) + " , " + d_stock[str(l_tmp[i])]}])
                    varUrl = "https://xueqiu.com/S/SH" + str(l_tmp[i])
                    l_result.append(varUrl)
                else:
                    Color_PO.outColor([{"31": str(i + 1) + "，" + str(d_curr) + "，" + "https://xueqiu.com/S/SH" + str(
                        l_tmp[i]) + " , " + d_stock[str(l_tmp[i])]}])
                    varUrl = "https://xueqiu.com/S/SH" + str(l_tmp[i])
                    l_result.append(varUrl)
                Log_PO.logger.info(str(d_curr) + " , " + "https://xueqiu.com/S/SZ" + str(l_tmp[i]) + " , " + d_stock[str(l_tmp[i])])

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
        Log_PO.logger.info("已保存" + excelFile)

        if os.name == 'nt':
            os.system("start " + excelFile)
        else:
            os.system("open " + excelFile)

    except Exception as e:
        Log_PO.logger.error(f"发生错误: {e}")

if __name__ == "__main__":

    try:
        # 收盘后，下载数据后执行
        # run({"涨幅": [2,9]})

        # 盘中执行
        run({"涨幅": [-3, 5]})

    except Exception as e:
        print(f"发生错误: {e}")
        Log_PO.logger.error(f"发生错误: {e}")
