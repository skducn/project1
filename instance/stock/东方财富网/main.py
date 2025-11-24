# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 东方财富网
# https://quote.eastmoney.com/center/gridlist.html#gem_board
# 策略：2：20执行，输出txt，导入财富通， 去掉低成交量，5没有上20，20没有上55
# *****************************************************************

import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from multiprocessing import Pool, cpu_count
import time

from PO.ListPO import *
List_PO = ListPO()

from PO.TimePO import *
Time_PO = TimePO()

from PO.ColorPO import *
Color_PO = ColorPO()

from PO.WebPO import *
from PO.NewexcelPO import *
from PO.OpenpyxlPO import *


def xx(l_data, l_code):
    # lcode = ['000997','000992']
    # 特殊中文名处理，如 "新 大 陆"中间有空格
    # 获取，新大陆000997 的索引，删除后续2个元素
    for code in l_code:
        if code in l_data:
            index = l_data.index(code)  # 新 大 陆
            new_index = index + 1
            l_data.pop(new_index)
            l_data.pop(new_index)
    return l_data

def main(d_url):

    sum = ''
    for k, v in d_url.items():
        s = ''
        sign = 0
        l_l_data = []
        # pathFile = "/Users/linghuchong/Downloads/" + str(k) + ".xlsx"
        # NewexcelPO(pathFile)
        # Openpyxl_PO = OpenpyxlPO(pathFile)
        # Openpyxl_PO.appendRows([['序号','代码','名称','相关链接1','相关链接2','相关链接3','最新价','涨跌幅','涨跌额','成交量(手)','成交额','振幅','最高','最低','今开','昨收','量比','换手率','市盈率(动态)','市净率']])

        Web_PO = WebPO("chrome")
        Web_PO.openURL(v)
        # 1,关闭广告
        Web_PO.clkByX("/html/body/div[5]/img[1]")
        # 2,获取总页数
        varPage = Web_PO.getTextByX('//*[@id="mainc"]/div/div/div[4]/div/a[4]')
        # 3,遍历
        for j in range(1, int(varPage) + 1):
            # 跳到X页
            Web_PO.setTextEnterByX('//*[@id="mainc"]/div/div/div[4]/div/form/input[1]', j, 2)
            # 4,获取数据
            l_data = Web_PO.getTextByXs('//*[@id="mainc"]/div/div/div[4]/table/tbody')
            s_data = l_data[0]
            l_data = s_data.replace('\n', ' ').split()

            # 特殊中文名处理，如 "新 大 陆"中间有空格
            l_data = xx(l_data, ['000997','002186','002095','002183','002264'])

            # 每页20个票
            # ([['序号','代码','名称','相关链接1','相关链接2','相关链接3','最新价','涨跌幅','涨跌额','成交量(手)','成交额','振幅','最高','最低','今开','昨收','量比','换手率','市盈率(动态)','市净率']])
            for i in range(0, len(l_data), 20):
                l_l_data.append(l_data[i:i + 20])

            # print(91, l_l_data)
            for l_data in l_l_data:
                try:
                    # 5,判断涨跌幅 2% - 5%区间
                    l_data_7 = float(l_data[7].replace("%", ''))
                    # 代码小于 688000
                    # 价格在区间[10, 30]
                    # (最高价 -（最高价-最低价） * 0.35) > 最新价
                    # (最新价 > (最高价 -（最高价-最低价） * 0.5),
                    # 最低 >= (金开 - 金开 * 0.01)
                    if l_data_7 > 4.5:
                        ...
                    elif (l_data_7 >= 2.5 and l_data_7 <= 4.5) :
                        if int(l_data[1]) < 688000 and (float(l_data[6]) > 10 and float(l_data[6]) <= 30) and \
                            ((float(l_data[12]) - (float(l_data[12]) - float(l_data[13])) * 0.35) > float(l_data[6])) and \
                            (float(l_data[6]) > (float(l_data[12]) - (float(l_data[12]) - float(l_data[13])) * 0.5)) and \
                            (float(l_data[13]) > (float(l_data[14]) - (float(l_data[14]) * 0.01))):
                            s = l_data[1] + "," + s
                            # print(s)
                    else:
                        sign = 1
                        break
                except:
                    print(120, l_data)
                    sys.exit(0)
            l_l_data = []

            if sign == 1:
                print(k, s)
                sum = s + sum
                s = ''
                break

        Web_PO.cls()


    # 获取当天日期，如1118
    varDate = Time_PO.getMonth() + Time_PO.getDay()
    varFile = "/Users/linghuchong/Desktop/stock/all_" + str(varDate) + ".txt"
    # varFile = "/Users/linghuchong/Desktop/stock/" + str(k) + str(varDate) + ".txt"
    with open(varFile, "w", encoding="utf-8") as f:
        f.write(sum)



# 创业板
# varUrl = "https://quote.eastmoney.com/center/gridlist.html#gem_board"
# # 上证A股，注册制
# varUrl = "https://quote.eastmoney.com/center/gridlist.html#sh_a_board_zcz"
# # 上证A股，核准制
# varUrl = "https://quote.eastmoney.com/center/gridlist.html#sh_a_board_hzz"
# # 上证A股(全部)
# varUrl = "https://quote.eastmoney.com/center/gridlist.html#sh_a_board"

# d_url = {
#     "创业板": "https://quote.eastmoney.com/center/gridlist.html#gem_board"}

d_url = {
    "创业板": "https://quote.eastmoney.com/center/gridlist.html#gem_board",
    "上证A股(全部)": "https://quote.eastmoney.com/center/gridlist.html#sh_a_board",
    "深证A股(全部)": "https://quote.eastmoney.com/center/gridlist.html#sz_a_board"
}

main(d_url)

# 002438,001210,300218,301059,002824,001336,001311,300522,300446,001368,300755,001278,603217,605296,603153,603159,600475,300218,301059,300522,300446,300755,