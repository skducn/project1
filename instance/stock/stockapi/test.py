# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-01-29
# Description: stockapi 获取当天股票最低价和收盘价与7_stock.clsx文件比较，符合要求的写入文档最后一列
# https://stockapi.com.cn/#/ma
# {"msg":"该接口无token用户单个ip每日可调用三次，请明日再来，若想无限制，请购买token，地址:https://stockapi.com.cn","code":60040}
# https://stockapi.com.cn/v1/base/ZTPool?date=2024-09-30

# http://www.kxdaili.com/dailiip.html free IP
# http://www.ip3366.net/free/?stype=1
# https://zhuanlan.zhihu.com/p/4643609408
# *****************************************************************

import pandas as pd
import os, sys, platform
pd.set_option('display.width', None)
from time import strftime, localtime

import requests
import json
from PO.TimePO import *
Time_PO = TimePO()

# 获取
d_ = {"code":20000,"msg":"success","data":[{"code":"000002","name":"万  科Ａ","changeRatio":9.954751,"lastPrice":9.72,"amount":5592761856.000000,"flowCapital":94448616608.000000,"totalCapital":115966496379.000000,"turnoverRatio":5.966146,"ceilingAmount":382249400.000000,"firstCeilingTime":"092500","lastCeilingTime":"102951","bombNum":5,"lbNum":3,"industry":"房地产开","time":"2024-09-30","gl":"房地产开发,广东板块,破净股,标准普尔,富时罗素,深证100R,MSCI中国,深股通,证金持股,央视50_,融资融券,预亏预减,深成500,机构重仓,HS300_,AH股,REITs概念,装配建筑,租售同权,超级品牌,猪肉概念,智能家居,养老概念,深圳特区","stockReason":"公司2023年实现合同销售金额3761亿元，累计获取开发项目40个","plateReason":"一线城市集体放松限购","plateName":"房地产"},
{"code":"000004","name":"国华网安","changeRatio":9.986505,"lastPrice":16.3,"amount":636048464.000000,"flowCapital":2058495916.000000,"totalCapital":2157798597.000000,"turnoverRatio":32.134750,"ceilingAmount":3988593.000000,"firstCeilingTime":"145621","lastCeilingTime":"145621","bombNum":0,"lbNum":1,"industry":"软件开发","time":"2024-09-30","gl":"软件开发,广东板块,预盈预增,信创,鸿蒙概念,RCS概念,车联网(车路云),5G概念,网络安全,手游概念,物联网,深圳特区,网络游戏","stockReason":"1、国内移动应用安全头部企业，积极参与鸿蒙系统生态建设，目前已完成方舟编译器、鸿蒙系统以及HAP的适配工作；\n2、公司新投资设立公司车联网业务的下游客户主要包括行业平台客户、整车厂和政府主导的新一代车联网V2X等，公司为上述客户提供智能终端、智能驾驶辅助技术、感知设备以及V2X总体技术解决方案","plateReason":"黎巴嫩对讲机在多地发生爆炸+华为申请注册“鸿蒙甄选”、“鸿蒙优选”等商标","plateName":"网络安全+华为产业链"}]}

l_2 = []
for i in range(len(d_['data'])):
    if int(d_["data"][i]["code"]) < 400000 or (int(d_["data"][i]["code"]) > 600000 and int(d_["data"][i]["code"]) < 680000):
        d_1 = d_['data'][i]
        l_2.append(d_1)
df = pd.DataFrame(l_2)
print(df)

# # 1，初始化数据
folder_name = '7_stock'
l_date = ['20251213']
file_name = folder_name + '.xlsx'

# # 2，生成目录结构
current_dir = os.path.dirname(os.path.abspath(__file__))
file_dir = '{}/{}'.format(current_dir, folder_name)
if not os.path.isdir(file_dir):
    os.makedirs(file_dir)
file_dir_name = '{}/{}'.format(file_dir, file_name)

# # 3, 获取即时资金流入
for i in l_date:
    if os.path.isfile(file_dir_name):
        with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=i, index=False)
    else:
        with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, sheet_name=i, index=False)

# 4，打开文档
if platform.system() == "Darwin":
    os.system("open " + file_dir_name)
