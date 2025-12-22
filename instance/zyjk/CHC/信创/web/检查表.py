# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-12-22
# Description: 社区健康5G 信创1.0 - 检查表
# 需求：/Users/linghuchong/Desktop/智赢健康/信创/社区健康管理中心系统信创版本V1.0.docx
#***************************************************************
from PO.SqlserverPO import *
Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "utf8")
# Sqlserver_PO.desc()

from PO.OpenpyxlPO import *
Openpyxl_PO = OpenpyxlPO("./chc.xlsx")


rows = Openpyxl_PO.getTotalRowCol("CHC")[0]
for i in range(1, rows):
    print(Openpyxl_PO.getOneRow(i+1, "CHC"))
print("----------------------------------------------")
rows = Openpyxl_PO.getTotalRowCol("CHCCONFIG")[0]
for i in range(1, rows):
    print(Openpyxl_PO.getOneRow(i+1, "CHCCONFIG"))
print("----------------------------------------------")

rows = Openpyxl_PO.getTotalRowCol("CHCJOB")[0]
for i in range(1, rows):
    print(Openpyxl_PO.getOneRow(i+1, "CHCJOB"))



