# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 上海，盘中，输出缩量反包的票
# 实时数据源：https://stockpage.10jqka.com.cn/realHead_v2.html#hs_002564
# 步骤：
# 1，读取 sh.json
# 2，与实时数据源进行匹配，筛选出服药要求的stock。
# *****************************************************************
import sys
import os
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl.styles.stylesheet")

from PO.WebPO import *

from PO.ColorPO import *
Color_PO = ColorPO()

jsonFile = "all.json"

from PO.LogPO import *
# Log_PO = LogPO(filename=Configparser_PO.DATA("logfile"), level="info")


def run():

    # 1, 读取 JSON 文件
    try:
        with open(jsonFile, 'r', encoding='utf-8') as file:
            d_all = json.load(file)
        # print("成功读取数据：", d_all)
    except FileNotFoundError:
        print(f"错误：未找到文件 {jsonFile}")
    except json.JSONDecodeError:
        print(f"错误：无法解析 {jsonFile} 中的 JSON 数据")
    except Exception as e:
        print(f"发生未知错误：{e}")

    # try:
    count = len(d_all)
    for index, (k, v) in enumerate(d_all.items(), start=1):
        print(index, "/", count)
        # print(v)  # {'date': '2025-06-06', 'code': '600844', 'name': '丹化科技', 'todayStartPrice': '3.06', 'yesterdayEndPrice': '3.05', 'volume': '55.51万'}
        code = v['code']
        name = v['name']
        volume = v['volume'].replace("万", "")
        if float(v['todayStartPrice']) > float(v['yesterdayEndPrice']):
            price = v['yesterdayEndPrice']
        else:
            price = v['todayStartPrice']

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

        # d_curr['昨天成交量'] = volume
        # d_curr['昨天现价'] = yesterdayStartPrice
        # print("d_curr =>", d_curr)
        # if float(d_curr['换手']) > 0 and d_curr['市盈率'] != '亏损'  and\
        if float(d_curr['涨幅']) > 1 and float(d_curr['涨幅']) < 5 and\
            float(d_curr['现价']) < 30 and float(d_curr['市盈率']) < 800 and\
            d_curr['成交量'] < volume and float(d_curr['现价']) > float(price):
            if int(k) > 600000:
                Color_PO.outColor([{"31": str(k) + ", https://xueqiu.com/S/SH" + str(code) + ", " + str(name)}])
            else:
                Color_PO.outColor([{"31": str(k) + ", https://xueqiu.com/S/SZ" + str(code) + ", " + str(name)}])

    # except Exception as e:
    #     print(f"发生错误: {e}")
    #     Log_PO.logger.error(f"发生错误: {e}")


if __name__ == "__main__":

    run()


