# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-06-15
# Description: stockapi 生成涨停板文档
# https://stockapi.com.cn/#/ZTPool 每天只能调用三次
# https://stockapi.com.cn/#/ma
# {"msg":"该接口无token用户单个ip每日可调用三次，请明日再来，若想无限制，请购买token，地址:https://stockapi.com.cn","code":60040}
# 实例：https://stockapi.com.cn/v1/base/ZTPool?date=2024-09-30
# http://www.kxdaili.com/dailiip.html free IP
# http://www.ip3366.net/free/?stype=1
# 实例：python3 cliGetRaisingLimit.py 2020-12-12 2021-03-12 1990-12-12
# *****************************************************************

import pandas as pd
import requests,os,platform,sys
sys.path.append("/Users/linghuchong/Downloads/51/Python/project/")
from PO.TimePO import *
Time_PO = TimePO()

# # 使用HTTP代理
# proxies = {
#     'http': 'http://183.164.242.168:8089'
# }

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


if len(sys.argv) == 1:
    # 没有参数
    # 获取当天
    l_date = []
elif len(sys.argv) == 2:
    # 一个参数
    # 1，获取历史日期的涨停板
    l_date = [sys.argv[1]]
    # l_date = ['2024-09-30']

elif len(sys.argv) == 3:
    # 2个参数
    # 1，获取历史日期的涨停板
    l_date = [sys.argv[1],sys.argv[2]]
    # l_date = ['2024-09-30', '2024-10-08']

elif len(sys.argv) == 4:
    # 3个参数
    # 1，获取历史日期的涨停板
    l_date = [sys.argv[1],sys.argv[2],sys.argv[3]]
    # l_date = ['2024-09-30', '2024-10-08', '2024-10-09']

else:
    print("error，参数溢出！")
# sys.exit(0)




if len(l_date) == 0:
    # 1，获取当天日期的涨停板
    varDateByMinus = Time_PO.getDateByMinus()  # 2025-1-29
    varDate = Time_PO.getDate()  # 20250129

    # 2，调用接口获取数据
    varUrl = 'https://stockapi.com.cn/v1/base/ZTPool?date=' + varDateByMinus
    # x = requests.get(varUrl, headers=headers, proxies=proxies)
    x = requests.get(varUrl, headers=headers)
    # print(x.text)
    d_ = x.json()
    # {"code":20000,"msg":"success","data":[{"code":"000002","name":"万  科Ａ","changeRatio":9.954751,"lastPrice":9.72,
    l_2 = []
    for i in range(len(d_['data'])):
        if int(d_["data"][i]["code"]) < 400000 or (int(d_["data"][i]["code"]) > 600000 and int(d_["data"][i]["code"]) < 680000):
            d_1 = d_['data'][i]
            l_2.append(d_1)
    df = pd.DataFrame(l_2)
    # print(df)
    #    code   name  changeRatio  lastPrice        amount   flowCapital  totalCapital  turnoverRatio  ceilingAmount firstCeilingTime lastCeilingTime  bombNum  lbNum industry        time                                                 gl                                        stockReason                           plateReason   plateName
    # 0  000002  万  科Ａ     9.954751       9.72  5.592762e+09  9.444862e+10  1.159665e+11       5.966146    382249400.0           092500          102951        5      3     房地产开  2024-09-30  房地产开发,广东板块,破净股,标准普尔,富时罗素,深证100R,MSCI中国,深股通,证金持...                  公司2023年实现合同销售金额3761亿元，累计获取开发项目40个                            一线城市集体放松限购         房地产
    # 1  000004   国华网安     9.986505

    # 3，生成文件
    folder_name = '7_stock'
    file_name = folder_name + '.xlsx'
    # 4，生成目录结构
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_dir = '{}/{}'.format(current_dir, folder_name)
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    file_dir_name = '{}/{}'.format(file_dir, file_name)
    # 5, 获取即时资金流入
    if os.path.isfile(file_dir_name):
        with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=varDate, index=False)
    else:
        with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, sheet_name=varDate, index=False)
    # 6，打开文档
    if platform.system() == "Darwin":
        os.system("open " + file_dir_name)

else:

    # 1，获取历史日期的涨停板
    for i in range(len(l_date)):
        l_1_date = l_date[i].split('-')
        # print(l_1_date) # ['2024', '09', '30']
        varDate = l_1_date[0] + l_1_date[1] + l_1_date[2]

        # 2，调用接口获取数据
        varUrl = 'https://stockapi.com.cn/v1/base/ZTPool?date=' + l_date[i]
        # x = requests.get(varUrl, headers=headers, proxies=proxies)
        x = requests.get(varUrl, headers=headers)
        d_ = x.json()
        # {"code":20000,"msg":"success","data":[{"code":"000002","name":"万  科Ａ","changeRatio":9.954751,"lastPrice":9.72,
        l_2 = []
        for i in range(len(d_['data'])):
            if int(d_["data"][i]["code"]) < 400000 or (int(d_["data"][i]["code"]) > 600000 and int(d_["data"][i]["code"]) < 680000):
                d_1 = d_['data'][i]
                l_2.append(d_1)
        df = pd.DataFrame(l_2)
        print(df)
        #    code   name  changeRatio  lastPrice        amount   flowCapital  totalCapital  turnoverRatio  ceilingAmount firstCeilingTime lastCeilingTime  bombNum  lbNum industry        time                                                 gl                                        stockReason                           plateReason   plateName
        # 0  000002  万  科Ａ     9.954751       9.72  5.592762e+09  9.444862e+10  1.159665e+11       5.966146    382249400.0           092500          102951        5      3     房地产开  2024-09-30  房地产开发,广东板块,破净股,标准普尔,富时罗素,深证100R,MSCI中国,深股通,证金持...                  公司2023年实现合同销售金额3761亿元，累计获取开发项目40个                            一线城市集体放松限购         房地产
        # 1  000004   国华网安     9.986505

        # 3，生成文件
        folder_name = '7_stock'
        file_name = folder_name + '.xlsx'
        # 4，生成目录结构
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_dir = '{}/{}'.format(current_dir, folder_name)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        file_dir_name = '{}/{}'.format(file_dir, file_name)
        # 5, 写数据
        if os.path.isfile(file_dir_name):
            with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=varDate, index=False)
        else:
            with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='w') as writer:
                df.to_excel(writer, sheet_name=varDate, index=False)
        # 6，打开文档
        if platform.system() == "Darwin":
            os.system("open " + file_dir_name)


