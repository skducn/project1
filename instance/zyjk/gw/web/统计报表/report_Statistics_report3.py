# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-3-25
# Description: 基本公卫 - 统计报表 - 数据统计
# *****************************************************************
from GwPO_report import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO_report = GwPO_report(logName, '糖尿病患者健康管理报表')


# todo 1 查询
# Gw_PO_report.queryReport({"管理机构": "东庄卫生院", "时间": [[2025,1,1],[2025,3,25]]})


# todo 2 导出
# Gw_PO_report.export("/Users/linghuchong/Desktop/糖尿病患者健康管理报表.xls")




