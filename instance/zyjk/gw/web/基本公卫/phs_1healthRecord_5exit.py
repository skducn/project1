# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 健康档案管理 - 迁出审核
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName, '迁出审核')


# todo 1 查询

Gw_PO.phs_healthrecord_exit_query({"姓名": "李明明", "身份证号": "110101195901018874", "申请日期": [[2025, 1, 1], [2025, 1, 2]], "申请人": "test",
                                   "管理机构": "招远市卫健局", "是否仅查询机构": "是", "状态": "已批准"})
# ' 管理机构 ': "金岭镇卫生院"
# ' 管理机构 ': {"金岭镇卫生院": "金岭镇山上候家村卫生室"}


# todo 2 同意
# Gw_PO.phs_healthrecord_exit_operation()
# getattr(Gw_PO, s_func + '_query')({"身份证号": "110101195901018874"})  # 查询
# getattr(Gw_PO, s_func + '_operation')('同意')


# todo 3 拒绝
# getattr(Gw_PO, s_func + '_query')({"身份证号": "110101195901018874"})  # 查询
# getattr(Gw_PO, s_func + '_operation')('拒绝')






