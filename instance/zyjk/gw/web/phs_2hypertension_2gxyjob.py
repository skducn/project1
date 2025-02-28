# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-8
# Description: 基本公卫 - 高血压管理 - 高血压随访
# 动态调用函数1
# s_func = 'phs_hypertension_gxyjob_query'
# getattr(Gw_PO, s_func)({"身份证号": "41052220000511081"})
# 动态调用函数2(有风险)
# s_func = 'Gw_PO.phs_hypertension_gxyjob_query({"身份证号": "41052220000511081"})'
# eval(s_func)
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName)
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')
# 登录
Gw_PO.login(Configparser_PO.HTTP("url"), Configparser_PO.ACCOUNT("user"), Configparser_PO.ACCOUNT("password"))
# 菜单
d_menu_basicPHS = {'健康档案概况': 'http://192.168.0.203:30080/phs/HealthRecord/ehrindex', '个人健康档案': 'http://192.168.0.203:30080/phs/HealthRecord/Personal', '家庭健康档案': 'http://192.168.0.203:30080/phs/HealthRecord/Family', '迁入申请': 'http://192.168.0.203:30080/phs/HealthRecord/Immigration', '迁出审核': 'http://192.168.0.203:30080/phs/HealthRecord/Exit', '档案交接': 'http://192.168.0.203:30080/phs/HealthRecord/handoverFile', '死亡管理': 'http://192.168.0.203:30080/phs/HealthRecord/DeathManagement', '区域档案查询': 'http://192.168.0.203:30080/phs/HealthRecord/regionalFile', '接诊信息查询': 'http://192.168.0.203:30080/phs/HealthRecord/Diagnosis', '就诊管理': 'http://192.168.0.203:30080/phs/HealthRecord/Visit', '高血压专项': 'http://192.168.0.203:30080/phs/Hypertension/gxyregister', '高血压随访': 'http://192.168.0.203:30080/phs/Hypertension/gxyjob', '高血压报病': 'http://192.168.0.203:30080/phs/Hypertension/gxybb', '糖尿病专项': 'http://192.168.0.203:30080/phs/Diabetes/tnbregister', '糖尿病随访': 'http://192.168.0.203:30080/phs/Diabetes/tnbjob', '糖尿病报病': 'http://192.168.0.203:30080/phs/Diabetes/tnbbb', '慢阻肺病登记': 'http://192.168.0.203:30080/phs/Copd/register', '慢阻肺病专项': 'http://192.168.0.203:30080/phs/Copd/project', '慢阻肺病随访': 'http://192.168.0.203:30080/phs/Copd/visit', '儿童概况': 'http://192.168.0.203:30080/phs/Child/etindex', '儿童健康档案': 'http://192.168.0.203:30080/phs/Child/etfiles', '中医体质辨识列表': 'http://192.168.0.203:30080/phs/Child/tcm', '中医体质辨识汇总': 'http://192.168.0.203:30080/phs/Child/tzbs', '儿童检查记录': 'http://192.168.0.203:30080/phs/Child/etjob', '孕产妇概况': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfindex', '孕产妇登记': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfregister', '孕产妇档案': 'http://192.168.0.203:30080/phs/MaternalRecord/ycffiles', '孕产妇随访': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfjob', '老年人概况': 'http://192.168.0.203:30080/phs/Snr/lnrindex', '老年人专项登记': 'http://192.168.0.203:30080/phs/Snr/special', '老年人专项管理': 'http://192.168.0.203:30080/phs/Snr/lnrfiles', '本年度未体检': 'http://192.168.0.203:30080/phs/Snr/unexamined', '老年人中医体质辨识': 'http://192.168.0.203:30080/phs/Snr/chMedicine', '老年人自理能力评估查询': 'http://192.168.0.203:30080/phs/Snr/selfCareAssess', '老年人抑郁评估查询': 'http://192.168.0.203:30080/phs/Snr/depressed', '简易智力检查查询': 'http://192.168.0.203:30080/phs/Snr/intelligence', '体检登记': 'http://192.168.0.203:30080/phs/HealthExamination/tjregister', '体检记录': 'http://192.168.0.203:30080/phs/HealthExamination/tjrecord', '未体检人员': 'http://192.168.0.203:30080/phs/HealthExamination/tjunexam', '肺结核患者概况': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhindex', '肺结核登记': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhregister', '肺结核管理': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhfiles', '残疾人概况': 'http://192.168.0.203:30080/phs/Disabled/cjrindex', '残疾人登记': 'http://192.168.0.203:30080/phs/Disabled/cjrregister', '残疾人管理': 'http://192.168.0.203:30080/phs/Disabled/cjrfiles', '严重精神障碍登记': 'http://192.168.0.203:30080/phs/MentalDisorder/jsregister', '严重精神障碍患者': 'http://192.168.0.203:30080/phs/MentalDisorder/jsfiles', '严重精神病障碍随访': 'http://192.168.0.203:30080/phs/MentalDisorder/jsjob', '严重精神障碍概况': 'http://192.168.0.203:30080/phs/MentalDisorder/jsindex', '健康教育活动': 'http://192.168.0.203:30080/phs/HealthEducation/HealthActivity', '本年度未评': 'http://192.168.0.203:30080/phs/hbp/noassessdata', '评分信息查询': 'http://192.168.0.203:30080/phs/hbp/assessdata'}
Web_PO.opnLabel(d_menu_basicPHS['高血压随访'])
Web_PO.swhLabel(1)



# todo 1 查询
Gw_PO.phs_hypertension_gxyjob_query({"身份证号": "340203195002048036"})
# Gw_PO.phs_hypertension_gxyjob_query({"姓名": "胡成", "身份证号": "230202194504020016", "管理机构": "招远市卫健局", "随访日期": [[2025, 1, 1], [2025, 1, 2]],
#                                      "随访医生": "zhangsan", "随访方式": "电话", "是否终止管理": "否", "随访评价结果": "不良反应", '数据源': '公卫随访',
#                                      "收缩压范围": [11, 12], "舒张压范围": [13, 14], "出生日期范围": [[2025, 2, 5], [2025, 2, 6]],
#                                      "现住址": ["泉山街道", "花园社区居民委员会", "123"]
#                                     })


# todo 2 导出
# Gw_PO.export("/Users/linghuchong/Desktop/gxyjob.xlsx")



# todo 3 详情 - 编辑（高血压随访记录）
Gw_PO.phs_hypertension_gxyjob_operation({'operate': '详情', 'option': {"身份证号": "340203195002048036"}})
Gw_PO.phs_hypertension_gxyjob_operation({'operate': '详情', 'operate2': '编辑', "data": {
      '随访日期': [2025, 2, 10], '随访方式': '网络', '症状': ['头痛头晕', {'其他': '123'}, '下肢水肿'],
      '血压': [11, 12], '身高': '177', '体重': [66, 77], '心率':'100', '其他': "测试一下",
      '日吸烟量':[11,14], '日饮酒量':[112,144],
      '运动频率实际': '每天', '运动频率目标': '不运动',
      '运动时长':[11, 23], '摄盐量分级实际': '轻', '摄盐量分级目标': '中', '随访饮食合理性评价': '合理', '心理调整评价结果': '差', '随访遵医行为': '一般',
      '辅助检查': '1212', '服药依从性': '间断', '药物不良反应': ['有','5555'], '随访评价结果': '不良反应', '下一步管理措施': "两次控制不满意转诊随访",
      '用药情况药物名称1':'阿莫西林100', '用药情况用法用量1每日':'每日一次', '用药情况用法用量1每次':'1',
      '用药情况药物名称2':'阿莫西林冲剂', '用药情况用法用量2每日':'每日二次', '用药情况用法用量2每次':'2',
      '用药情况药物名称3':'阿莫西林测试', '用药情况用法用量3每日':'每日三次', '用药情况用法用量3每次':'3',
      '用药调整意见药物名称1':'阿莫西林胶囊', '用药调整意见用法用量1每日':'一次性', '用药调整意见用法用量1每次':'4',
      '用药调整意见药物名称2':'阿莫西林钠克拉维酸钾（二叶克）', '用药调整意见用法用量2每日':'必要时', '用药调整意见用法用量2每次':'5',
      '用药调整意见药物名称3':'阿莫西林钠/克拉维酸钾', '用药调整意见用法用量3每日':'一次性', '用药调整意见用法用量3每次':'6',
      '转诊原因':'123', '转入医疗机构及科室':'456', '联系人':'789', '联系人电话':'1000', '结果':'到位', '备注':'nonono',
      '下次随访日期': [2025, 5, 9], '随访医生':'测试1', '居民签字': '张三丰'}})


# todo 4-3 编辑 - 新增(高血压随访记录)
# Gw_PO.phs_hypertension_gxyjob_operation({'operate': '编辑', 'option': {"身份证号": "340203195002048036"}})
# Gw_PO.phs_hypertension_gxyjob_operation({'operate': '编辑', 'operate2': '新增', "data": {
#       '随访日期': [2025, 2, 9], '随访方式': '网络', '症状': ['头痛头晕', {'其他': '123'}, '下肢水肿'],
#       '血压': [11, 12], '身高': '177', '体重': [66, 77], '心率':'100', '其他': "测试一下",
#       '日吸烟量':[11,14], '日饮酒量':[112,144],
#       '运动频率实际': '每天', '运动频率目标': '不运动',
#       '运动时长':[11, 23], '摄盐量分级实际': '轻', '摄盐量分级目标': '中', '随访饮食合理性评价': '合理', '心理调整评价结果': '差', '随访遵医行为': '一般',
#       '辅助检查': '1212', '服药依从性': '间断', '药物不良反应': ['有','5555'], '随访评价结果': '不良反应', '下一步管理措施': "两次控制不满意转诊随访",
#       '用药情况药物名称1':'阿莫西林100', '用药情况用法用量1每日':'每日一次', '用药情况用法用量1每次':'1',
#       '用药情况药物名称2':'阿莫西林冲剂', '用药情况用法用量2每日':'每日二次', '用药情况用法用量2每次':'2',
#       '用药情况药物名称3':'阿莫西林测试', '用药情况用法用量3每日':'每日三次', '用药情况用法用量3每次':'3',
#       '用药调整意见药物名称1':'阿莫西林胶囊', '用药调整意见用法用量1每日':'一次性', '用药调整意见用法用量1每次':'4',
#       '用药调整意见药物名称2':'阿莫西林钠克拉维酸钾（二叶克）', '用药调整意见用法用量2每日':'必要时', '用药调整意见用法用量2每次':'5',
#       '用药调整意见药物名称3':'阿莫西林钠/克拉维酸钾', '用药调整意见用法用量3每日':'一次性', '用药调整意见用法用量3每次':'6',
#       '转诊原因':'123', '转入医疗机构及科室':'456', '联系人':'789', '联系人电话':'1000', '结果':'到位', '备注':'nonono',
#       '下次随访日期': [2025, 5, 9], '随访医生':'测试1', '居民签字': '张三丰'}})


# # todo 4.2 编辑 - 引用上次新增(高血压随访记录)
# Gw_PO.phs_hypertension_gxyjob_operation({'operate': '编辑', 'option': {"身份证号": "340203195002048036"}})
# Gw_PO.phs_hypertension_gxyjob_operation({'operate': '编辑', 'operate2': '引入上次新增', "data": {'随访日期': [2025, 3, 9], '下次随访日期': [2025, 5, 9]}})




# # todo 5 删除
# Gw_PO.phs_hypertension_gxyjob_query({"身份证号": "310101200006036356"})
# Gw_PO.phs_hypertension_gxyjob_operation({'operate': '删除', 'option': {'随访日期': '2025-02-09'}})

