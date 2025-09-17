﻿# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-5-9
# Description: 体重管理1.0 - 判定居民体重状态 Determine Residents' Weight Status (a_weight10_DRWS)
# 需求：体重管理 v1.18
# pip install pymssql==2.2.8
# pip install petl
# pip install sqlalchemy
#***************************************************************
from DrwsPO import *
Drws_PO = DrwsPO()

# todo 步骤1：将需求文档（腾讯文档）保存到excel
# 【腾讯文档】体重管理1.18规则自动化 - 判定居民体重状态DRWS
# https://docs.qq.com/sheet/DYmxVUGFZRWhTSHND?tab=k1ge3c
# 将在线文档，判定居民体重状态DRWS 保存到excel（weidht10.xlsx中 a_weight10_DRWS）


# todo 步骤2：将excel导入db
Drws_PO.excel2db_DRWS()


# todo 步骤3：测试取值条件
# 3.1 测试所有
# Drws_PO.DRWS('all')

# 3.2 测试单行
Drws_PO.DRWS(1)














