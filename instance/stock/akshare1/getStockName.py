# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-05-4
# Description:   www.akshare.xyz
# conda activate py310
# pip install aksare
# https://ke.qq.com/webcourse/index.html?r=1683091325369#cid=5835909&term_id=106048134&taid=13742014157360261&type=3072&source=PC_COURSE_DETAIL&vid=387702306339866276
# *****************************************************************
import os,json

def getStockName(fileName):
    fileName1 = fileName + ".json"
    if os.path.exists(fileName1):
        with open(fileName1, 'r', encoding='utf-8') as file:
            d_all = json.load(file)

    # print(d_all)
    s_ = ''
    for d_ in d_all:
        print(d_)
        s_ = s_ + d_['名称'] + ","

    print(s_)
    # 保存到 "/Users/linghuchong/Desktop/stock/"，用于导入
    with open("/Users/linghuchong/Desktop/stock/" + fileName + ".txt", 'w', encoding='utf-8') as file:
        file.write(s_)

# getStockName("20250603")
getStockName("20250604")
getStockName("20250605")