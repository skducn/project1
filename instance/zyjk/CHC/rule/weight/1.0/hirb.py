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

from HirbPO import *
Hirb_PO = HirbPO()


# todo 1, excel导入db
# Hirb_PO.excel2db_HIRB()


# todo 2, 健康干预 Health Intervention  Rule Base
# 执行所有测试
# Hirb_PO.HIRB("all")  # 测试所有

# 执行单行测试
Hirb_PO.HIRB(109)
# Hirb_PO.HIRB(106)
# Hirb_PO.HIRB(43)
# Hirb_PO.HIRB(44)
# Hirb_PO.HIRB(51)
# Hirb_PO.HIRB(97)
# Hirb_PO.HIRB(108)
# Hirb_PO.HIRB(101)









