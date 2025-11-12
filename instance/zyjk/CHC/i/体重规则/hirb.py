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
#***************************************************************

from HirbPO import *
Hirb_PO = HirbPO()


# todo 步骤1, excel导入db
# Hirb_PO.excel2db_HIRB()


# todo 步骤2, 执行健康干预
# 2.1 测试所有
# Hirb_PO.HIRB("all")  # 测试所有

# 2.2 测试单行
# Hirb_PO.HIRB(112)
# Hirb_PO.HIRB(113)
# Hirb_PO.HIRB(114)
# Hirb_PO.HIRB(115)
# Hirb_PO.HIRB(116)
# Hirb_PO.HIRB(97)
# Hirb_PO.HIRB(108)
# Hirb_PO.HIRB(101)









