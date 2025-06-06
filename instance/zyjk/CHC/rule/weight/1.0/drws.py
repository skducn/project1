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
from DrwsPO import *
Drws_PO = DrwsPO()


# todo 1, excel导入db
# Drws_PO.excel2db_DRWS()


# todo 2, 判定居民体重状态 Determine Residents' Weight Status
# 执行所有测试
# Drws_PO.DRWS('all')

# 测试单行
Drws_PO.DRWS(16)







