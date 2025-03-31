# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 健康档案管理 - 死亡管理
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName, '死亡管理')


# todo 1 查询
# Gw_PO.phs_healthrecord_deathmanagement_query({"姓名": "zhangsan", "身份证号": "410522200005110812", "死亡日期": [[2023, 5, 10], [2023, 5, 12]],
#                                               "现住址": ["泉山街道", "花园区居委会", "123"]})
# Gw_PO.phs_healthrecord_deathmanagement_query({"身份证号": "370624194304300623"} )
Gw_PO.phs_healthrecord_deathmanagement_query({"姓名": "001"})


# todo 2 导出 xls
# Gw_PO.export("/Users/linghuchong/Desktop/deathManagement")


# todo 3 档案查看
d_ = Gw_PO.phs_healthrecord_deathmanagement_operation({'operate': '档案查看', 'option': {"身份证号": "110101193801014594"}})
print(d_)










