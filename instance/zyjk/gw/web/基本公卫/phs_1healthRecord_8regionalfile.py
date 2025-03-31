# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 健康档案管理 - 区域档案查询
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName, '区域档案查询')


# todo 1 查询
Gw_PO.phs_healthrecord_regionalfile_query({"身份证号": "41052220000511081"})








