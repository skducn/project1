# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-05-4
# Description:  6.2 数据处理与分析之 股票资金流入流出分析
#  www.akshare.xyz
# conda activate py310
# pip install aksare
# https://ke.qq.com/webcourse/index.html?r=1683165164078#cid=5835909&term_id=106048134&taid=13742039927164037&type=3072&source=PC_COURSE_DETAIL&vid=387702306340510660
# *****************************************************************

import pandas as pd
import numpy as np
import akshare as ak
import os, sys, platform
from time import sleep
pd.set_option('display.width', None)
from time import strftime, localtime

# 1，初始化数据
folder_name = '7涨停股池'
# l_date = ['20250106', '20250107', '20250108']
l_date = ['20250604', '20250605']
# l_date = ['20250603']
# print(l_date[0][:6])
# print(l_date[0][6:])
file_name = l_date[0][:6] + '.xlsx'
# file_name = folder_name + '.xlsx'

# 2，生成目录结构
current_dir = os.path.dirname(os.path.abspath(__file__))
file_dir = '{}/{}'.format(current_dir, folder_name)
if not os.path.isdir(file_dir):
    os.makedirs(file_dir)
file_dir_name = '{}/{}'.format(file_dir, file_name)


# 3, 获取即时资金流入
for i in l_date:
    data = ak.stock_zt_pool_em(date=i)
    print(data)
    json_data = data.to_json(orient="records", force_ascii=False)
    # print(json_data)
    fileName = str(i) + ".json"
    with open(fileName, "w", encoding="utf-8") as f:
    # with open("zt_pool_data.json", "w", encoding="utf-8") as f:
        f.write(json_data)

    if os.path.isfile(file_dir_name):
        with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            data.to_excel(writer, sheet_name=i[6:], index=False)
    else:
        with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='w') as writer:
            data.to_excel(writer, sheet_name=i[6:], index=False)

# # 4，打开文档
# if platform.system() == "Darwin":
#     os.system("open " + file_dir_name)
