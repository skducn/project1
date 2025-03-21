# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 冠心病患者管理 - 冠心病管理
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
Web_PO.opnLabel(d_menu_basicPHS['冠心病管理'])
Web_PO.swhLabel(1)



# todo 1 查询
Gw_PO_three.query({"身份证号": "110101195907066009"})
# Gw_PO_three.query({'登记日期':[[2024,7,2],[2024,10,30]]})
# Gw_PO_three.query({"管理机构": "招远市卫健局", '是否仅查询机构': '是', "姓名": "胡成", "身份证号": "370685198705183027",
#     '上次随访日期': [[2025,1,2],[2025,1,3]], '管理状态': '管理中',  '登记时年龄': [2, 5],
#     '登记日期':[[2025,2,2],[2025,2,3]], '随访提醒分类':'两周内随访', '档案状态': '在档',
#     "现住址": ["泉山街道", "花园社区居民委员会", "123"]
#     })



# todo 2 访视记录
Gw_PO_three.three_Coronary_CHDfiles_operation({'operate': '访视记录', 'option': {"身份证号": "110101195907066009"}})

# todo 2.1 专项记录
# Gw_PO_three.three_Coronary_CHDfiles_operation({'operate': '个人专项档案_专项记录_修改', 'data': {
#     '冠心病诊断': '冠心病猝死',
#     '诊断依据': 'CT',
#     '发病日期': [2025,1,2], '确认日期': [2025,1,3],'确诊医院':'阿里医院', '是否首次发病': '是',
#     '登记日期': [2025,1,4],'开始管理时间': [2025,1,5]
# }})

# Gw_PO_three.three_Coronary_CHDfiles_operation({'operate': '个人专项档案_评估记录_新增评估', 'data': {
    # '冠心病诊断': '冠心病猝死',
    # '诊断依据': 'CT',
    # '发病日期': [2025,1,2], '确认日期': [2025,1,3],'确诊医院':'阿里医院', '是否首次发病': '是',
    # '登记日期': [2025,1,4],'开始管理时间': [2025,1,5]
# }})

# Gw_PO_three.three_Coronary_CHDfiles_operation({'operate': '个人专项档案_专项记录_结案', 'data': {
#     '结案原因': {'其他': '123'},
# }})

# Gw_PO_three.three_Coronary_CHDfiles_operation({'operate': '个人专项档案_专项记录_删除', 'data': {}})

# todo 2.2 评估记录
# Gw_PO_three.three_Coronary_CHDfiles_operation({'operate': '个人专项档案_评估记录_新增评估', 'data': {
#     '危险因素控制效果': '较好', '药物治疗效果': '很好',
#     '非药物治疗效果': '一般', '病情转归': '其他',
#     '危险级别转归': '中危险组', '异常详述': '阿里医院',
#     '评估结果': '阿发放', '指导意见': '2121',
#     '评估医生': '金浩1', '评估日期': [2025,1,4],
#     '录入人': '1', '录入日期': [2025,1,5]
# }})
# Gw_PO_three.three_Coronary_CHDfiles_operation({'operate': '个人专项档案_评估记录_结案', 'data': {
#     '结案原因': {'其他': '123'},
# }})

# todo 2.3 随访记录
Gw_PO_three.three_Coronary_CHDfiles_operation({'operate': '个人专项档案_随访记录_新增随访', 'data': {
    '随访日期': '', '随访方式': '其他',
    '冠心病类型': '猝死性',
    '目前症状': ['心慌', '其他'],
    '体征': {'血压': ['100', '89'], '体重': '66', '身高': '170', '空腹血糖': '10', '心率': '110','其他': '13100'},
    '生活方式': {'日吸烟量': '44', '日饮酒量': '55', '运动频率': '10', '每次持续时间': '210', '摄盐量': '中', '心理调整': '一般', '遵医行为': '差劲'},
    '服药依从性': '不服药',
    '特殊治疗': ['外科手术治疗', '介入治疗'],
    '非药物治疗措施': ['限盐', '减少体重'],
    '此次随访分类': '并发症',
    '健康评价': '玩儿',
    '下次随访时间': [2025,1,5], '医生签名': 'sy',
    '居民（家属）签名': 'sk'
}})
# Gw_PO_three.three_Coronary_CHDfiles_operation({'operate': '个人专项档案_随访记录_结案', 'data': {
#     '结案原因': {'其他': '123'},
# }})