# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-9-11
# Description: 区域平台 - 数据交换规则
# 【腾讯文档】数据交换之校验规则自动化
# https://docs.qq.com/sheet/DYmtpa2pTSUJhT0ZD?tab=xfisl0
# 接口文档 http://192.168.0.201:28801/doc.html
# 前端：http://192.168.0.213:1080/
# 【腾讯文档】区域平台数据质控流程  https://docs.qq.com/doc/DS2J0T1VsRlplWHF3
#***************************************************************

from PO.OpenpyxlPO import *
from PlatformRulePO import *
PlatformRule_PO = PlatformRulePO()
PlatformRule_PO.clsApp("Microsoft Excel")
Openpyxl_PO = OpenpyxlPO("数据交换规则.xlsx")

# 1,获取token
TOKEN = PlatformRule_PO.getToken("jh", "123456")
print(TOKEN)

# # todo 1，非空
# PlatformRule_PO.feikong('非空', Openpyxl_PO, TOKEN)

# # todo 2，日期
# PlatformRule_PO.riqi('日期', Openpyxl_PO, TOKEN)

# # todo 3,数字范围
# PlatformRule_PO.shuzifanwei('数字范围', Openpyxl_PO, TOKEN)
#
# # todo 4，值域
# 【腾讯文档】区域平台值域校验
# https://docs.qq.com/doc/DS1NkRkNMVnRIaFdL
# Sqlserver_PO.genRecord("TB_HIS_MZ_Reg", {"GTHBZ": None, "CREATETIMEDQC":"2023-09-18 12:12:12"})  # 自动生成数据
# Sqlserver_PO.genRecord("TB_HIS_MZ_Reg", {"GTHBZ": 1, "CREATETIMEDQC": "2023-09-18 12:12:12"})  # 自动生成数据
PlatformRule_PO.zhiyu('值阈', "2023-09-18", "2023-09-18", Openpyxl_PO, TOKEN)
#
# # todo 5，身份证
# PlatformRule_PO.shenfenzheng('身份证', Openpyxl_PO, TOKEN)
#
#
# # todo 6，关联表??
# # list = Openpyxl_PO.getRowValueByCol([4, 6, 10, 11], '关联表')
# # list.pop(0)
# # print(list)
#
#
Openpyxl_PO.open()

