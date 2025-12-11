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
    # 名字分成2个
    # lcode = ['000025']
    # 特殊中文名处理，如 "特', '力Ａ"中间有空格
    # 获取，特', '力Ａ 000025的索引，删除后续个元素
    for code in l_code:
        if code in l_data:
            index = l_data.index(code)
            new_index = index + 1
            l_data.pop(new_index)
    return l_data

def xxx(l_data, l_code):
    # 名字分成3个
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

        Web_PO = WebPO("chrome")
        Web_PO.openURL(v)
        # 1,关闭广告
        Web_PO.clkByX("/html/body/div[5]/img[1]")
        # 2,获取总页数
        varPage = Web_PO.getTextByX('//*[@id="mainc"]/div/div/div[4]/div/a[4]')
        varPage = int(varPage) - 1
        # for j in range(varPage, 0 , -1):
        #     # 跳到X页
        #     Web_PO.setTextEnterByX('//*[@id="mainc"]/div/div/div[4]/div/form/input[1]', j, 2)
        #
        # sys.exit(0)
        # 3,遍历
        for j in range(varPage, 0 , -1):
            # 跳到X页
            Web_PO.setTextEnterByX('//*[@id="mainc"]/div/div/div[4]/div/form/input[1]', j, 2)
            # 4,获取数据
            l_data = Web_PO.getTextByXs('//*[@id="mainc"]/div/div/div[4]/table/tbody')
            s_data = l_data[0]
            l_data = s_data.replace('\n', ' ').split()

            varFile = "/Users/linghuchong/Downloads/51/Python/project/instance/stock/东方财富网/name2.ini"
            with open(varFile, "r", encoding="utf-8") as f:
                # 读取所有内容 + 替换换行符 + 去除首尾空白
                content = f.read().replace("\n", "").strip()
            result_list = [s.strip().strip("'") for s in content.split(",") if s.strip()]
            l_data = xx(l_data, result_list)

            # 特殊中文名处理，如 "新 大 陆"中间有空格
            # l_data = xx(l_data, ['000025', '000528'])  # 处理名称拆封为2
            varFile = "/Users/linghuchong/Downloads/51/Python/project/instance/stock/东方财富网/name3.ini"
            with open(varFile, "r", encoding="utf-8") as f:
                # 读取所有内容 + 替换换行符 + 去除首尾空白
                content = f.read().replace("\n", "").strip()
            result_list = [s.strip().strip("'") for s in content.split(",") if s.strip()]
            l_data = xxx(l_data,result_list)
            # l_data = xxx(l_data, ['000997','002186','002095','002183','002264','002209','002029','000735','002136', '000514',
            #   '0002161','0002181','000061','002040','002224','002183','000635','002215','000402'])  #  # 处理名称拆封为3

            # 每页20个票
            # ([['序号','代码','名称','相关链接1','相关链接2','相关链接3','最新价','涨跌幅','涨跌额','成交量(手)','成交额','振幅','最高','最低','今开','昨收','量比','换手率','市盈率(动态)','市净率']])
            for i in range(0, len(l_data), 20):
                l_l_data.append(l_data[i:i + 20])

            # print(91, l_l_data)
            for l_data in l_l_data:
                try:
                    # 判断条件：
                    l_data_7 = float(l_data[7].replace("%", ''))
                    # 涨跌幅 -8% - -2% 区间
                    # 代码小于 688000
                    # 最新价（收盘）在区间 [5, 20]
                    #   最高价 > 最低价 ,  (最高价-最低价)>0.3
                    # 最新价（收盘）在区间 [20, 40]
                    #   最高价 > 最低价 ,  (最高价-最低价)>1

                    if l_data_7 < -8:
                        ...
                    elif (l_data_7 > -8 and l_data_7 <= -2) :
                        # print(l_data[2])
                        if int(l_data[1]) < 688000 and "ST" not in l_data[2]:
                            if (float(l_data[6]) > 5 and float(l_data[6]) <= 20) and \
                                (float(l_data[12]) > float(l_data[13]) and (float(l_data[12]) - float(l_data[13])) > 0.3 ) :
                                s = l_data[1] + "," + s
                            elif (float(l_data[6]) > 20 and float(l_data[6]) <= 40) and \
                                (float(l_data[12]) > float(l_data[13]) and (float(l_data[12]) - float(l_data[13])) > 1 ) :
                                s = l_data[1] + "," + s
                            elif (float(l_data[6]) > 40 and float(l_data[6]) <= 60) and \
                                (float(l_data[12]) > float(l_data[13]) and (float(l_data[12]) - float(l_data[13])) > 1.5 ) :
                                s = l_data[1] + "," + s
                    else:

                        sign = 1
                        break
                except:
                    print(109, l_data)
                    if l_data[4] == '股吧':
                        varFile = "/Users/linghuchong/Downloads/51/Python/project/instance/stock/东方财富网/name2.ini"
                        with open(varFile, "a", encoding="utf-8") as f:
                            f.write(",'" + l_data[1] + "'")
                    elif l_data[5] == '股吧':
                        varFile = "/Users/linghuchong/Downloads/51/Python/project/instance/stock/东方财富网/name3.ini"
                        with open(varFile, "a", encoding="utf-8") as f:
                            f.write(",'" + l_data[1] + "'")
                    main(d_url)
                    # sys.exit(0)
            l_l_data = []

            if sign == 1:
                print(141, k, s)
                sum = s + sum
                s = ''
                break

        Web_PO.cls()


    # 获取当天日期，如1118
    varDate = Time_PO.getMonth() + Time_PO.getDay()
    varFile = "/Users/linghuchong/Desktop/stock/all_" + str(varDate) + ".txt"
    with open(varFile, "w", encoding="utf-8") as f:
        f.write(sum)



# # 上证A股，注册制
# varUrl = "https://quote.eastmoney.com/center/gridlist.html#sh_a_board_zcz"
# # 上证A股，核准制
# varUrl = "https://quote.eastmoney.com/center/gridlist.html#sh_a_board_hzz"
# # 上证A股(全部)
# varUrl = "https://quote.eastmoney.com/center/gridlist.html#sh_a_board"


d_url = {
    "创业板": "https://quote.eastmoney.com/center/gridlist.html#gem_board",
    "上证A股(全部)": "https://quote.eastmoney.com/center/gridlist.html#sh_a_board",
    "深证A股(全部)": "https://quote.eastmoney.com/center/gridlist.html#sz_a_board"
}

main(d_url)

