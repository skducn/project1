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
# Weight_PO.excel2db_ER(Configparser_PO.FILE("case"), "ER", "a_weight10_ER")
# Weight_PO.excel2db_IR(Configparser_PO.FILE("case"), "IR", "a_weight10_IR")
# Weight_PO.excel2db_WS(Configparser_PO.FILE("case"), "WEIGHT_STATUS", "a_weight10_WS")

# # todo 2, 运行主程序
# Weight_PO.testWS(Configparser_PO.DB_SQL("table"), 'error')  # 执行错误记录
# Weight_PO.main(Configparser_PO.DB("tableER"), 'all')  # 执行全部记录

Weight_PO.WS(Configparser_PO.DB("tableWS"))  # 执行全部记录








