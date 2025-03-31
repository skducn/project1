# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 高血脂管理 - 高血脂随访
# *****************************************************************
from GwPO_three import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO_three = GwPO_three(logName, '高血脂随访')


# todo 1 查询
Gw_PO_three.query({"身份证号": "110101199001012512"})
# Gw_PO_three.query({"姓名": "胡成", "身份证号": "110101199001012512", "管理机构": "招远市卫健局", '是否仅查询机构': '是',
#     '随访日期': [[2025,1,2],[2025,2,3]], '随访医生':'占三', '随访方式':'电话','是否终止管理': '是', '数据源': '三高随访',
#     '随访评价结果': '不良反应','出生日期': [[2025, 1, 12], [2025, 2, 13]],})


# todo 导出
# Gw_PO_three.export('../data/三高共管/GwPO_three_Hyperlipidemia_gxzsvisit.xlsx')


# # # todo 3。1 查看
Gw_PO_three.three_Hyperlipidemia_gxzsvisit_operation({'operate': '详情', 'option': {"身份证号": "110101199001012512"}})
Gw_PO_three.three_Hyperlipidemia_gxzsvisit_operation({'operate': '高血脂随访记录', 'data': {}})
