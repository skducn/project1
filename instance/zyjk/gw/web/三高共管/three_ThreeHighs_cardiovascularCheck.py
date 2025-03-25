# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 三高共管 - 心血管评估管理
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
Web_PO.opnLabel(d_menu_basicPHS['心血管评估管理'])
Web_PO.swhLabel(1)



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


