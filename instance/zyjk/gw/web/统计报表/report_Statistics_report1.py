# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-3-25
# Description: 基本公卫 - 统计报表 - 数据统计
# *****************************************************************
from GwPO_report import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO_report = GwPO_report(logName, '城乡居民健康档案管理报表')


# todo 1 查询
Gw_PO_report.queryReport({"管理机构": "张星卫生院", "时间": [[2025,1,1],[2025,3,25]]})


# todo 2 导出
Gw_PO_report.export("/Users/linghuchong/Desktop/report_Statistics_report1.xls")




