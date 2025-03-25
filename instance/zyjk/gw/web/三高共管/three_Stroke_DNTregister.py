# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 脑卒中患者管理 - 脑卒中登记
# *****************************************************************
import sys,os
# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取 上层 目录的绝对路径
project_dir = os.path.abspath(os.path.join(current_dir, '..'))
# 将 上层 目录添加到 sys.path
sys.path.insert(0, project_dir)
from GwPO_three import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO_three = GwPO_three(logName)
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('../config.ini')
# 登录
Gw_PO_three.login(Configparser_PO.HTTP("url"), Configparser_PO.ACCOUNT("user"), Configparser_PO.ACCOUNT("password"))
# 菜单
d_menu_basicPHS = {'三高共管概况': 'http://192.168.0.203:30080/three/ThreeHighs/general', '医防融合信息表': 'http://192.168.0.203:30080/three/ThreeHighs/supplement', '三高随访管理': 'http://192.168.0.203:30080/three/ThreeHighs/ThnVisitList', '心血管评估管理': 'http://192.168.0.203:30080/three/ThreeHighs/cardiovascularCheck', '并发症管理': 'http://192.168.0.203:30080/three/ThreeHighs/Complications', '三高患者管理': 'http://192.168.0.203:30080/three/ThreeHighs/ThnList', '冠心病登记': 'http://192.168.0.203:30080/three/Coronary/CHDregister', '冠心病管理': 'http://192.168.0.203:30080/three/Coronary/CHDfiles', '脑卒中登记': 'http://192.168.0.203:30080/three/Stroke/DNTregister', '脑卒中管理': 'http://192.168.0.203:30080/three/Stroke/DNTfiles', '高血脂登记': 'http://192.168.0.203:30080/three/Hyperlipidemia/gxzregister', '高血脂专项': 'http://192.168.0.203:30080/three/Hyperlipidemia/gxzspecial', '高血脂随访': 'http://192.168.0.203:30080/three/Hyperlipidemia/gxzsvisit'}
Web_PO.opnLabel(d_menu_basicPHS['脑卒中登记'])
Web_PO.swhLabel(1)



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

