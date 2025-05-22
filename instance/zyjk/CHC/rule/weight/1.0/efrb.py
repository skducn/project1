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

from EfrbPO import *
Efrb_PO = EfrbPO()


# todo 1, excel导入db
Efrb_PO.excel2db_EFRB()

# todo 2, 评估因素规则库 Evaluation Factor Rule Base
# Efrb_PO.EFRB("all")
Efrb_PO.EFRB(47)
# Efrb_PO.EFRB(18)
# Efrb_PO.EFRB(56)
# Weight_PO.EFRB(46, "n")

# Weight_PO.EFRB(1, {'categoryCode': 3, 'disease': '脑卒中'})  # 只测试1条









