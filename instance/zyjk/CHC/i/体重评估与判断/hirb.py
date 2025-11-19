# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-5-9
# Description: 体重管理1.0 - 健康干预规则库 Health Intervention Rule Base (a_weight_HIRB)
# 需求：体重管理1.18
# 【腾讯文档】体重管理1.18规则自动化
# https://docs.qq.com/sheet/DYmxVUGFZRWhTSHND?tab=rprd0r
# pip install pymssql==2.2.8
# pip install petl
# pip install sqlalchemy

# todo 注意执行前config.ini中设置run_n = off
# 执行反向用例(执行健康干预HIRB时需要设置off)
# run_n = off
#***************************************************************
from HirbPO import *
Hirb_PO = HirbPO()

# todo 步骤1, excel导入db
# Hirb_PO.excel2db_HIRB()



# todo 1执行所有
# Hirb_PO.HIRB()

# todo 2执行错误
# Hirb_PO.HIRB("error")

# todo 3执行连续多条（id区间，EFRB([起始，步长])） ？？？
# Hirb_PO.HIRB([105, 3])  # 测试 4 到 9， 连续5条规则
# Hirb_PO.HIRB([53, 5])  # 测试 4 到 9， 连续5条规则

# todo 4执行单条
Hirb_PO.HIRB({'id': 109})
# Hirb_PO.HIRB({'IR_code': 'TZ_AGE002'})
# Hirb_PO.HIRB({'IR_code': 'TZ_YD053'})
# Hirb_PO.HIRB({'IR_code': 'TZ_YD054'})
# Hirb_PO.HIRB({'IR_code': 'TZ_YD049'})
# Hirb_PO.HIRB({'IR_code': 'TZ_AGE003'})
# Hirb_PO.HIRB({'IR_code': 'TZ_AGE004'})
# Hirb_PO.HIRB({'IR_code': 'TZ_STZB022'})
# Hirb_PO.HIRB({'IR_code': 'TZ_RQFL004'})
# Hirb_PO.HIRB({'id': 115, 'IR_code': 'TZ_YD054'})

# todo 5执行多条
# Hirb_PO.HIRB({'id': [102, 114]})  # 测试 51 和 59，2条规则
# Hirb_PO.HIRB({'IR_code': ['TZ_YS052', 'TZ_YS053']})  # 测试 TZ_STZB046，TZ_STZB048 ， 2条规则
# Hirb_PO.HIRB({'id': [1, 3], 'IR_code': ['TZ_STZB045', 'TZ_STZB047']})  # 测试 TZ_STZB045，TZ_STZB047，id=1,3 ，4条规则





