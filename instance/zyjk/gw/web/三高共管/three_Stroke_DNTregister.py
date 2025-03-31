# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 脑卒中患者管理 - 脑卒中登记
# *****************************************************************
from GwPO_three import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO_three = GwPO_three(logName, '脑卒中登记')


# todo 1 查询
Gw_PO_three.query({"身份证号": "370685199001012654"})
# Gw_PO_three.query({"管理机构": "招远市卫健局", '是否仅查询机构': '是', "姓名": "胡成", '年龄': [2, 5],
#                    "身份证号": "370685199001012654", '联系电话': '58776544', '档案状态': '在档'})



# # todo 2 新增登记
Gw_PO_three.three_Stroke_DNTregister_operation({'operate': '新增登记', 'option': {"身份证号": "370685199001012654"}})
Gw_PO_three.three_Stroke_DNTregister_operation({'operate': '个人专项档案_脑卒中患者登记', 'data': {
    '脑卒中诊断': '脑出血',
    '诊断依据': 'CT',
    '诊断分类': '脑栓塞',
    '发病日期': [2025,1,2], '确认日期': [2025,1,3], '确诊医院': '阿里医院', '是否首次发病': '是',
    '登记日期': [2025,1,4],'开始管理时间': [2025,1,5]
}})

