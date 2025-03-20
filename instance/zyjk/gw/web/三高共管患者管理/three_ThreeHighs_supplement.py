# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 三高共管 - 医防融合信息表
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
Web_PO.opnLabel(d_menu_basicPHS['医防融合信息表'])
Web_PO.swhLabel(1)



# todo 1 查询
# Gw_PO_three.query({"身份证号": "372922198510281068"})
# Gw_PO_three.query({"管理机构": "招远市卫健局", '档案状态': '在档', "姓名": "胡成", "身份证号": "372922198510281068", '填表日期': [[2025,1,2],[2025,2,3]],
#     "现住址":["泉山街道", "花园社区居民委员会","123"]})


# todo 2 导出
# Gw_PO_three.export("/Users/linghuchong/Desktop/three_ThreeHighs_supplement.xls")


# todo 3 修改
# Gw_PO_three.three_ThreeHighs_supplement_operation({'operate': '修改', 'option': {"身份证号": "372922198510281068"}})
# Gw_PO_three.three_ThreeHighs_supplement_operation({'operate': '修改', 'data': {
#     ' 风险评估方式 ': '总体风险评估', ' 风险评估结果 ':'高危',
#     ' 享受医保政策情况 ':'大病统筹', ' 医保定点医院 ': ['基层医疗卫生机构', '444'],
#     ' 靶器官 ': {' 是否筛查 ': '是', ' 筛查日期 ': [2025,1,3], ' 筛查机构 ': '百慕大三角', ' 筛查内容 ': ['眼',{'其他':'123'}]},
#     ' 患者最关注并希望得到支持的方面 ': ['心理干预', {'其他':'456'}],
#     ' 居家健康支持 ': ['血糖仪', {'家庭成员支持帮助':'123123'}],
#     ' 自我管理小组 ': {'已参加(组员)': ['ee','rr','完成1期任务']},
#     ' 填表日期 ': [2025,1,6]
# }})


# todo 4 删除
# Gw_PO_three.three_ThreeHighs_supplement_operation({'operate': '删除', 'option': {"身份证号": "372922198510281068"}})


