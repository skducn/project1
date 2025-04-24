# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-3-25
# Description: 基本公卫 - 统计报表 - 区域卫生业务监控
# *****************************************************************
from GwPO_report import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO_report = GwPO_report(logName, '妇幼保健业务监管(孕产妇)')


# todo 1 查询
Gw_PO_report.queryReport({"所属机构": "东庄卫生院", " 年度： ": '2024'})


# todo 2 导出
Gw_PO_report.export("/Users/linghuchong/Desktop/妇幼保健业务监管(孕产妇).xls")




