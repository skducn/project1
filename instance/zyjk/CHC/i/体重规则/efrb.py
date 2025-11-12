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


# todo 步骤2, 测试规则库
# 2.1 测试所有
# Efrb_PO.EFRB({'id': 'all'})

# 2.2 测试单/多条规则
Efrb_PO.EFRB({'id': 1})

# Efrb_PO.EFRB({'id': 55}) # TZ_STZB044
# Efrb_PO.EFRB({'id': 56}) # TZ_STZB045
# Efrb_PO.EFRB({'id': [40, 49]})
# Efrb_PO.EFRB({'ER_code': 'TZ_STZB014'})
# Efrb_PO.EFRB({'ER_code': 'TZ_AGE001'})  # 17
# Efrb_PO.EFRB({'ER_code': 'TZ_STZB016'})
# Efrb_PO.EFRB({'id': 59, 'ER_code': 'TZ_STZB047'})  # 测试id=59 和 ER_code=TZ_STZB047 两条记录

# 2.3 测试多条连续规则
# Efrb_PO.EFRB({'id': [2, 3]})  # 测试 id =1,2,3 三条记录。
# Efrb_PO.EFRB({'ER_code': ['TZ_STZB046', 'TZ_STZB047']})  # 测试 TZ_STZB045，TZ_STZB046，TZ_STZB047， 三条记录。
# Efrb_PO.EFRB({'id': [1, 3], 'ER_code': ['TZ_STZB045', 'TZ_STZB047']})  # 测试 TZ_STZB045，TZ_STZB046，TZ_STZB047，id=1,2,3 六条记录。













