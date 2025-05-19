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
from WeightPO import *
Weight_PO = WeightPO()

# from PO.LogPO import *
# Log_PO = LogPO(filename='log.log', level="info")

# todo 1, excel导入db
# 评估因素规则库 Evaluation Factor Rule Base
# Weight_PO.excel2db_ER(Configparser_PO.FILE("case"), "ER", "a_weight10_ER")
# Weight_PO.EFRB(54)


# 判定居民体重状态 Determine Residents' Weight Status
# Weight_PO.excel2db_WS(Configparser_PO.FILE("case"), "WEIGHT_STATUS", "a_weight10_WS")
# Weight_PO.DRWS(8)


# Weight_PO.excel2db_HIRB(Configparser_PO.FILE("case"), "HIRB", "a_weight10_HIRB")
Weight_PO.HIRB(1)  # 健康干预规则库（其他分类）Health Intervention Rule Base (Other Categories)







