# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-5-9
# Description: 体重管理1.0 - 评估因素规则库 Evaluation Factor Rule Base (a_weight10_EFRB)
# 需求：体重管理1.18
# 【腾讯文档】体重管理1.18规则自动化
# https://docs.qq.com/sheet/DYmxVUGFZRWhTSHND?tab=rprd0r
# pip install pymssql==2.2.8
# pip install petl
# pip install sqlalchemy

# todo 注意：测试数据库CHC , a_weight10_EFRB， 因为要调用QYYH表。
# select * from CHC.dbo.WEIGHT_REPORT where ID = 2
# select WEIGHT_STATUS from CHC.dbo.QYYH where SFZH = '420204202201011268'
# select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 2
# 测试数据id=2，sfzh=420204202201011268
#***************************************************************
from EfrbPO import *
Efrb_PO = EfrbPO()

# # todo excel导入db
# Efrb_PO.excel2db_EFRB()


# todo 执行所有
# Efrb_PO.EFRB()


# todo 执行单条
Efrb_PO.EFRB({'id': 60})
# Efrb_PO.EFRB({'ER_code': 'TZ_STZB011'})
# Efrb_PO.EFRB({'ER_code': 'TZ_AGE003'})
# Efrb_PO.EFRB({'ER_code': 'TZ_AGE004'})
# Efrb_PO.EFRB({'ER_code': 'TZ_STZB022'})
# Efrb_PO.EFRB({'ER_code': 'TZ_RQFL004'})
# Efrb_PO.EFRB({'id': 50, 'ER_code': 'TZ_STZB047'})  # 测试id=59 和 ER_code=TZ_STZB047 两条记录


# todo 执行多条
# Efrb_PO.EFRB({'id': [3, 59]})  # 测试 51 和 59，2条规则
# Efrb_PO.EFRB({'ER_code': ['TZ_STZB046', 'TZ_STZB048']})  # 测试 TZ_STZB046，TZ_STZB048 ， 2条规则
# Efrb_PO.EFRB({'id': [1, 3], 'ER_code': ['TZ_STZB045', 'TZ_STZB047']})  # 测试 TZ_STZB045，TZ_STZB047，id=1,3 ，4条规则


# todo 执行连续多条（id区间，EFRB([起始，步长])）
# Efrb_PO.EFRB([49, 3])  # 测试 4 到 9， 连续5条规则
# Efrb_PO.EFRB([53, 5])  # 测试 4 到 9， 连续5条规则



# todo 有错误,待验证
# Efrb_PO.EFRB({'ER_code': [
#     "TZ_STZB007",
#     "TZ_STZB008",
#     "TZ_STZB009",
#     "TZ_STZB011",
#     "TZ_AGE001",
#     "TZ_AGE002",
#     "TZ_AGE003",
#     "TZ_AGE004"
# ]})








