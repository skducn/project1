# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-5-9
# Description: 体重管理1.0 评估因素判断规则自动化,
# 需求：体重管理1.18
# 【腾讯文档】体重管理1.18规则自动化
# https://docs.qq.com/sheet/DYmxVUGFZRWhTSHND?tab=rprd0r
# pip install pymssql==2.2.8
# pip install petl
# pip install sqlalchemy

#***************************************************************
# from WeightPO import *
# Weight_PO = WeightPO()

from DrwsPO import *
Drws_PO = DrwsPO()


# todo 1, excel导入db
# 评估因素规则库 Evaluation Factor Rule Base
# Weight_PO.excel2db_ER(Configparser_PO.FILE("case"), "ER", "a_weight10_ER")
# Weight_PO.EFRB(44)

# Weight_PO.EFRB(19)
# Weight_PO.EFRB(46)
# Weight_PO.EFRB(46, "n")

# Weight_PO.EFRB(1, {'categoryCode': 3, 'disease': '脑卒中'})  # 只测试1条


# todo 判定居民体重状态 Determine Residents' Weight Status
# Drws_PO.excel2db_DRWS()
Drws_PO.DRWS(1)



# Weight_PO.excel2db_HIRB(Configparser_PO.FILE("case"), "HIRB", "a_weight10_HIRB")
# Weight_PO.HIRB(94)  # 健康干预规则库（其他分类）Health Intervention Rule Base (Other Categories)
# Weight_PO.HIRB(107)  # 健康干预规则库（其他分类）Health Intervention Rule Base (Other Categories)







