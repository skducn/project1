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


# todo 步骤1, excel导入db
# Efrb_PO.excel2db_EFRB()


# todo 步骤2, 测试规则库
# 2.1 测试所有
Efrb_PO.EFRB('all')

# 2.2 测试单行
# 1.23.1
# Efrb_PO.EFRB(13)  # v1.25，
# Efrb_PO.EFRB(22)  # v1.25，
# Efrb_PO.EFRB(23)  # v1.25，
# Efrb_PO.EFRB(59)  # v1.25，
# Efrb_PO.EFRB(60)  # v1.25，
# Efrb_PO.EFRB(61)  # v1.25，

# Efrb_PO.EFRB(7)  # (14<= 年龄＜14.5 and 22.3<= BMI and 性别=男) or (14.5<= 年龄＜15 and 22.6<= BMI and 性别=男) or (15<= 年龄＜15.5 and 22.9<= BMI and 性别=男) or (15.5<= 年龄＜16 and 23.1<= BMI and 性别=男) or (16<= 年龄＜16.5 and 23.3<= BMI and 性别=男) or (16.5<= 年龄＜17 and 23.5<= BMI and 性别=男) or (17<= 年龄＜17.5 and 23.7<= BMI and 性别=男) or (17.5<= 年龄＜18 and 23.8<= BMI and 性别=男) or (14<= 年龄＜14.5 and 22.8<= BMI and 性别=女) or (14.5<= 年龄＜15 and 23.0<= BMI and 性别=女) or (15<= 年龄＜15.5 and 23.2<= BMI and 性别=女) or (15.5<= 年龄＜16 and 23.4<= BMI and 性别=女) or (16<= 年龄＜16.5 and 23.6<= BMI and 性别=女) or (16.5<= 年龄＜17 and 23.7<= BMI and 性别=女) or (17<= 年龄＜17.5 and 23.8<= BMI and 性别=女) or (17.5<= 年龄＜18 and 23.9<= BMI and 性别=女)
# Efrb_PO.EFRB(55)  # 年龄>=4 and 年龄＜10
# Efrb_PO.EFRB(56)  # 年龄=10
# Efrb_PO.EFRB(1)  # 糖尿病
# Efrb_PO.EFRB(48)  # 3
# Efrb_PO.EFRB(54)  # 年龄≤3










