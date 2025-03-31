# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 健康档案管理 - 就诊管理
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName, '就诊管理')


# todo 1 查询
Gw_PO.phs_healthrecord_visit_query({"管理机构": {"玲珑卫生院": "玲珑镇大蒋家村卫生室"}, "姓名": "zhangsan", "身份证号": "410522200005110812", "是否仅查询机构": "是",
                                    "就诊日期": [[2023, 5, 10], [2023, 5, 12]], "现住址": ["泉山街道", "花园区居委会", "123"]})


# # todo 2 导出
# Gw_PO.export("/Users/linghuchong/Desktop/phs_healthrecord_visit.xls")








