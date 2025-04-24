# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 三高共管 - 心血管评估管理
# *****************************************************************
from GwPO_three import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO_three = GwPO_three(logName, '心血管评估管理')


# todo 1 查询
# Gw_PO_three.query({"身份证号": "370685198705183027"})
Gw_PO_three.query({"管理机构": "招远市卫健局", '是否仅查询机构': '是', "姓名": "胡成", "身份证号": "110101195901015999",'评估日期': [[2025,1,2],[2025,2,3]],
    '评估结果': '中危', "现住址":["泉山街道", "花园社区居民委员会","123"]})



# todo 2 详情
# Gw_PO_three.three_ThreeHighs_cardiovascularCheck_operation({'operate': '详情', 'option': {"身份证号": "370685198705183027"}})


# todo 3 编辑
# Gw_PO_three.three_ThreeHighs_cardiovascularCheck_operation({'operate': '编辑', 'option': {"身份证号": "370685198705183027"}})
# Gw_PO_three.three_ThreeHighs_cardiovascularCheck_operation({'operate': '编辑', 'data': {
#     ' 现居住区地区域 ': '南方', ' 现居住地类型 ':'农村',
#     ' 总胆固醇 ':['56', 'mg/dl'], ' 高密度脂蛋白胆固醇 ': ['78','mg/dl'],
#     ' 腰围 ':'45',' 当前血压水平 ':['90','87'],
#     ' 是否服用降压药 ':'否',' 是否患糖尿病 ':'否',
#     ' 现在是否吸烟 ': '否',' 心脑血管家族史(指父母兄弟姐妹中有人患有心肌梗死或脑卒中)': '否',
#     ' 评测结果 ': '高危', ' 评估时间 ': [2025,1,3]
# }})


# todo 4 删除
# Gw_PO_three.three_ThreeHighs_cardiovascularCheck_operation({'operate': '删除', 'option': {"身份证号": "370685198705183027"}})


