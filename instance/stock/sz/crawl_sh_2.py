# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description:深圳，第二轮筛选stock，实时查询匹配符合要求的stock
# 实时数据源：https://stockpage.10jqka.com.cn/realHead_v2.html#hs_002564
# 步骤：
# 1，读取 sz.json
# 2，与实时数据源进行匹配，筛选出服药要求的stock。
# 3，生成日志并保存到 sz.xlsx
# *****************************************************************
import sys
import os
import datetime
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
# jsonFile = Configparser_PO.DATA("jsonfile")  # 第一轮筛选stock的文件
excelFile = Configparser_PO.DATA("excelfile")  # 第二轮筛选stock后的文件
logFile = Configparser_PO.DATA("logfile")  # 日志文件
jsonFile = 'sh.json'


# # 创建一个日志记录器
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
#
# # 创建一个文件处理器
# file_handler = logging.FileHandler(logFile)
# # file_handler.setLevel(logging.DEBUG)
# file_handler.setLevel(logging.INFO)
#
# # 创建一个控制台处理器
# # console_handler = logging.StreamHandler()
# # console_handler.setLevel(logging.INFO)
#
# # 定义日志格式
# # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)
# # console_handler.setFormatter(formatter)
#
# # 将处理器添加到日志记录器
# logger.addHandler(file_handler)
# # logger.addHandler(console_handler)


# varUrl = "https://stockpage.10jqka.com.cn/realHead_v2.html#hs_" + str("000001")
# # print(varUrl)  https://stockpage.10jqka.com.cn/realHead_v2.html#hs_000001
# Web_PO = WebPO("noChrome")
# Web_PO.openURL(varUrl)
# sleep(1)
# d_curr = {}
#
# # 获取当前价格
# l_curr = Web_PO.getTextByXs("//div[@class='price_box fl icons_box']")
# l_curr = l_curr[0].split("\n")
# d_curr['现价'] = l_curr[0]
# d_curr['涨幅'] = l_curr[2].replace("%", "")
# print(d_curr)
# s_volume = Web_PO.getTextById("tamount")
# print(s_volume)  # 6581.8万

def run():

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
        for k, v in d_stock.items():
            print(k)
            code = v[1]
            name = v[2]
            volume = v[9].replace("万", "")
            yesterdayStartPrice = v[12]

            varUrl = "https://stockpage.10jqka.com.cn/realHead_v2.html#hs_" + str(code)
            # print(varUrl)  https://stockpage.10jqka.com.cn/realHead_v2.html#hs_000001
            Web_PO = WebPO("noChrome")
            Web_PO.openURL(varUrl)
            sleep(1)
            d_curr = {}

            # 获取当前价格
            l_curr = Web_PO.getTextByXs("//div[@class='price_box fl icons_box']")
            l_curr = l_curr[0].split("\n")
            d_curr['现价'] = l_curr[0]
            d_curr['涨幅'] = l_curr[2].replace("%", "")
            s_volume = Web_PO.getTextById("tamount")
            # print(s_volume)  # 6581.8万
            s_volume = s_volume.replace("万", "")
            d_curr['成交量'] = s_volume

            # l_1 = Web_PO.getTextByXs("//div[@class='new_detail fl']/ul/li[1]/span")
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

            if float(d_curr['换手']) > 1 and d_curr['市盈率'] != '亏损'  and\
                    float(d_curr['涨幅']) > 1 and float(d_curr['涨幅']) < 6 and\
                    float(d_curr['现价']) < 30 and float(d_curr['市盈率']) < 200 and\
                    d_curr['成交量'] < volume and int(d_curr['现价']) > yesterdayStartPrice:
                Color_PO.outColor([{"32": str(k) + ", https://xueqiu.com/S/SH" + str(code) + ", " + str(name)}])



    except Exception as e:
        Log_PO.logger.error(f"发生错误: {e}")


if __name__ == "__main__":

    run()
    # try:
    #
    #     # 获取当前时间
    #     now = datetime.datetime.now().time()
    #     # 创建一个表示 15:00 的时间对象
    #     target_time = datetime.time(15, 0)
    #     # 判断当前时间是否大于 15:00
    #     if now > target_time:
    #         run({"涨幅": [2, 9]})
    #         print("盘后结果")
    #     else:
    #         # 盘中执行
    #         run({"涨幅": [-3, 5]})
    #         print("done, 盘中结果.")
    #
    # except Exception as e:
    #
    #     print(f"发生错误: {e}")
    #
    #     Log_PO.logger.error(f"发生错误: {e}")
