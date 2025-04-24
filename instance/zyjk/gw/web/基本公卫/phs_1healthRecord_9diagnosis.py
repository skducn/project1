# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 健康档案管理 - 接诊信息查询
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName, '接诊信息查询')


# todo 1 查询
Gw_PO.phs_healthrecord_diagnosis_query({"身份证号": "41052220000511081"})
# Gw_PO.phs_healthrecord_diagnosis_query({"姓名": "zhangsan", "身份证号": "410522200005110812", "就诊日期": [[2025, 1, 10], [2025, 2, 12]], "导入状态": "已导入", "管理机构": {"玲珑卫生院": "玲珑镇大蒋家村卫生室"}})









