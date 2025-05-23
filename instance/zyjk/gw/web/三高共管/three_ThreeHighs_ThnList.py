# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 三高共管 - 三高患者管理
# *****************************************************************
from GwPO_three import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO_three = GwPO_three(logName, '三高患者管理')


# todo 1 查询
# Gw_PO_three.three_ThreeHighs_ThnList_query({'三高分类': '两高'})
# Gw_PO_three.three_ThreeHighs_ThnList_query({'人群分类':['糖尿病','高血压']})
Gw_PO_three.query({"身份证号": "372922198510281068"})
# Gw_PO_three.query({"管理机构": "招远市卫健局", '是否仅查询机构': '是','档案状态': '在档', "姓名": "胡成", "身份证号": "372922198510281068",
#     '当年患者补充表': '是', '随访提醒分类': '常规随访',
#     "现住址":["泉山街道", "花园社区居民委员会","123"]})

# '人群分类':['糖尿病','高血压']

# todo 2 导出
# Gw_PO_three.export("/Users/linghuchong/Desktop/three_ThreeHighs_ThnList.xls")


# todo 3 随访 (三高患者评估_随访记录_新增随访)
# Gw_PO_three.three_ThreeHighs_ThnList_operation({'operate': '随访', 'option': {"身份证号": "372922198510281068"}})
# Gw_PO_three.three_ThreeHighs_ThnList_operation({'operate': '三高患者评估_随访记录_新增随访', 'data': {
#     '数据回传公卫随访表': ['高血压随访记录', '高血脂随访记录'],
#     '随访日期': [2025,2,3],'随访方式': '其他',
#     '高血压症状': ['恶心呕吐', {'其他': '123'}],
#     '糖尿病症状': ['感染', {'其他': '33'}],
#     '高血脂症状': ['失眠健忘', '口角歪斜'],
#     '体征': {'血压': ['1','2'], '体重': ['3','34'],'身高': '4','腰围': '5','心率': '6','足背动脉搏动': '未触及','其他体征': '7'},
#     '生活方式指导 ': {'日吸烟量': ['11','22'], '日饮酒量': ['33','44'],'运动': ['133','244', '333','444'], '日主食量': ['55','544'],'摄盐量分级': ['轻','中'],'心理调整': '差', '随访遵医行为评价': '一般'},
#     # '用药情况': [{'药品名称': '1', '用法用量': ['每日三次','1','2']}, {'药品名称': '2', '用法用量': ['每日二次','12','32']}],
#     '用药依从性': '间断', '药物不良反应': ['无','2323'], '低血糖反应': '偶尔',
#     '辅助检查': {'空腹血糖值':'1', '糖化血红蛋白': '2323', 'TG': '91','TC': '81','HDL-C': '71','LDL-C': '51','检查日期': [2025,3,4],'其他': '16'},
#     '本年度并发症筛查检查':['心电图', '肝功能'],
#     '本年度并发症评估结果':['脑血管病变', '眼底病变'],
#     '此次随访分类': [{'高血压患者': {'随访评价结果':'不良反应', '下一步管理措施': '紧急转诊','下次随访日期':[2025,1,5]}},{'高血脂患者': {'随访评价结果':'不良反应', '下一步管理措施': '紧急转诊','下次随访日期':[2025,1,5]}}],
#     # '用药调整情况': [{'药品名称': '不良反应', '用法用量': ['每日两次','1','2']}, {'药品名称':'不良反应', '用法用量': ['每日三次','4','5']}],
#     '转诊情况 ': {'转诊标志': '有', '转诊医疗机构及科室': '2', '转诊原因': '122', '联系人': '12', '联系人电话': '58776566', '转诊结果': '到位', '备注': '雨雨雨'},
#     '居民签名': '章三'
# }})

# todo 3 随访（三高患者评估_心血管评估记录_新增评估）
# Gw_PO_three.three_ThreeHighs_ThnList_operation({'operate': '随访', 'option': {"身份证号": "372922198510281068"}})
# Gw_PO_three.three_ThreeHighs_ThnList_operation({'operate': '三高患者评估_心血管评估记录_新增评估', 'data': {
#     ' 风险评估方式 ': '总体风险评估', ' 风险评估结果 ':'高危',
#     ' 享受医保政策情况 ':'大病统筹', ' 医保定点医院 ': ['基层医疗卫生机构', '444'],
#     ' 靶器官 ': {' 是否筛查 ': '是', ' 筛查日期 ': [2025,1,3], ' 筛查机构 ': '百慕大三角', ' 筛查内容 ': ['眼',{'其他':'123'}]},
#     ' 患者最关注并希望得到支持的方面 ': ['心理干预', {'其他':'456'}],
#     ' 居家健康支持 ': ['血糖仪', {'家庭成员支持帮助':'123123'}],
#     ' 自我管理小组 ': {'已参加(组员)': ['ee','rr','完成1期任务']},
#     ' 填表日期 ': [2025,1,6]
# }})


# todo 4 新增（慢性病患者医防融合信息表）
Gw_PO_three.three_ThreeHighs_ThnList_operation({'operate': '新增', 'option': {"身份证号": "372922198510281068"}})
Gw_PO_three.three_ThreeHighs_ThnList_operation({'operate': '慢性病患者医防融合信息表', 'data': {
    ' 风险评估方式 ': '总体风险评估', ' 风险评估结果 ':'高危',
    ' 享受医保政策情况 ':'大病统筹', ' 医保定点医院 ': ['基层医疗卫生机构', '444'],
    ' 靶器官 ': {' 是否筛查 ': '是', ' 筛查日期 ': [2025,1,3], ' 筛查机构 ': '百慕大三角', ' 筛查内容 ': ['眼',{'其他':'123'}]},
    ' 患者最关注并希望得到支持的方面 ': ['心理干预', {'其他':'456'}],
    ' 居家健康支持 ': ['血糖仪', {'家庭成员支持帮助':'123123'}],
    ' 自我管理小组 ': {'已参加(组员)': ['ee','rr','完成1期任务']},
    ' 填表日期 ': [2025,1,6]
}})


