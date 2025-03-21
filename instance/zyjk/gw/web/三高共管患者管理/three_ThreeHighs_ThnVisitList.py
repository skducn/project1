# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 三高共管 - 三高随访管理
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
Web_PO.opnLabel(d_menu_basicPHS['三高随访管理'])
Web_PO.swhLabel(1)



# todo 1 查询
# Gw_PO_three.query({"身份证号": "370685198705183027"})
# Gw_PO_three.query({"管理机构": "招远市卫健局", '档案状态': '在档', "姓名": "胡成", "身份证号": "372922198510281068", '随访日期': [[2025,1,2],[2025,2,3]],
#     '随访评估结果（高血压）': '控制满意','随访评估结果（糖尿病）': '控制不满意','随访评估结果（高血脂）': '不良反应',
#     "现住址":["泉山街道", "花园社区居民委员会","123"]})


# todo 2 导出
# Gw_PO_three.export("/Users/linghuchong/Desktop/three_ThreeHighs_ThnVisitList.xls")


# todo 3 详情（新增）
Gw_PO_three.three_ThreeHighs_ThnVisitList_operation({'operate': '详情', 'option': {"身份证号": "370685198705183027"}})
Gw_PO_three.three_ThreeHighs_ThnVisitList_operation({'operate': '新增随访', 'data': {
'随访日期': [2025,2,3],'随访方式': '其他','高血压症状': ['恶心呕吐', {'其他': '123'}], '糖尿病症状': ['感染', {'其他': '33'}],'高血脂症状': ['失眠健忘', '口角歪斜'],
    '体征': {'血压': ['1','2'], '体重': '3','身高': '4','腰围': '5','心率': '6','足背动脉搏动': '未触及','其他体征': '7'},
    '生活方式指导': {'日吸烟量': ['11','22'], '日饮酒量': ['33','44'],'运动': ['133','244', '333','444'], '日主食量': ['55','544'],'摄盐量分级': ['晴','中'],'心理调整': '差','随访遵医行为评价': '一般'},
    # '用药情况': [{'药品名称1': '1', '用法用量': ['每日三次','1','2']},{'药品名称1': '2', '用法用量': ['每日二次','12','32']}],
    '用药依从性': '间断', '药物不良反应': ['无','2323'], '低血糖反应': '偶尔',
    '辅助检查': {'空腹血糖值':'1', '糖化血红蛋白': '2323', 'TG': '91','TC': '81','HDL-C': '71','LDL-C': '51','检查日期': [2025,3,4],'其他': '16'},
    '本年度并发症筛查检查':['心电图', '肝功能'],
    '本年度并发症评估结果':['脑血管病变', '眼底病变'],
    '此次随访分类': [{'高血脂患者': {'随访评价结果':'不良反应', '下一步管理措施': '紧急转诊','下次随访日期':[2025,1,5]}},{'高血脂患者': {'随访评价结果':'不良反应', '下一步管理措施': '紧急转诊','下次随访日期':[2025,1,5]}}],
    # '用药调整情况': [{'药品名称': '不良反应', '用法用量': ['每日两次','1','2']}, {'药品名称':'不良反应', '用法用量': ['每日三次','4','5']}],
    '转诊情况': {'转诊标志': '有', '转诊医疗机构及科室': '2', '转诊原因': '122', '联系人': '12', '联系人电话': '58776566', '转诊结果': '到位', '备注': '雨雨雨'},
    '居民签名': '章三'
}})

# todo 3 编辑
Gw_PO_three.three_ThreeHighs_ThnVisitList_operation({'operate': '编辑', 'option': {"身份证号": "370685198705183027"}})
Gw_PO_three.three_ThreeHighs_ThnVisitList_operation({'operate': '三高患者评估_心血管评估记录_新增评估', 'data': {
    ' 风险评估方式 ': '总体风险评估', ' 风险评估结果 ':'高危',
    ' 享受医保政策情况 ':'大病统筹', ' 医保定点医院 ': ['基层医疗卫生机构', '444'],
    ' 靶器官 ': {' 是否筛查 ': '是', ' 筛查日期 ': [2025,1,3], ' 筛查机构 ': '百慕大三角', ' 筛查内容 ': ['眼',{'其他':'123'}]},
    ' 患者最关注并希望得到支持的方面 ': ['心理干预', {'其他':'456'}],
    ' 居家健康支持 ': ['血糖仪', {'家庭成员支持帮助':'123123'}],
    ' 自我管理小组 ': {'已参加(组员)': ['ee','rr','完成1期任务']},
    ' 填表日期 ': [2025,1,6]
}})


# todo 4 删除
# Gw_PO_three.three_ThreeHighs_ThnVisitList_operation({'operate': '删除', 'option': {"身份证号": "370685198705183027"}})



