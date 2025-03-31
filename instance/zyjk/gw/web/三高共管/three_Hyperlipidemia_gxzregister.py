# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 高血脂管理 - 高血脂登记
# *****************************************************************
from GwPO_three import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO_three = GwPO_three(logName, '高血脂登记')


# todo 1 查询
# Gw_PO_three.query({"身份证号": "340203202407017263"})
Gw_PO_three.query({"管理机构": "招远市卫健局", '是否仅查询机构': '是', "姓名": "胡成", '年龄': [2, 5],
                   "身份证号": "370685199001012654", '联系电话': '58776544', '档案状态': '在档'})


# # todo 2 新增登记
Gw_PO_three.three_Hyperlipidemia_gxzregister_operation({'operate': '登记', 'option': {"身份证号": "340203202407017263"}})
Gw_PO_three.three_Hyperlipidemia_gxzregister_operation({'operate': '高血脂患者管理卡_修改', 'data': {
    '病例来源': '其他',
    '诊断依据': 'CT',
    '居住地址': ['上海市', '市辖区', '黄浦区', '外滩街道', '北京居委会','123'],
    '高血脂分层结果': '高危',
    '确诊日期': [2025,1,2], '是否终止管理': ['是', {'终止管理日期': [2025,2,5]}],
    '建卡时间': [2025,1,5], '建卡医生': '金浩1'
}})

