# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-7
# Description: 基本公卫 - 慢性阻塞性肺病管理 - 慢阻肺病专项
# 动态调用函数1
# s_func = 'phs_diabetes_tnbregister_query'
# getattr(Gw_PO, s_func)({"身份证号": "41052220000511081"})
# 动态调用函数2(有风险)
# s_func = 'Gw_PO.phs_diabetes_tnbregister_query({"身份证号": "41052220000511081"})'
# eval(s_func)
# *****************************************************************
from GwPO import *
# logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
logName = f"./{os.path.splitext(os.path.basename(__file__))[0]}.log"
Gw_PO = GwPO(logName)
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')
# 登录
Gw_PO.login(Configparser_PO.HTTP("url"), Configparser_PO.ACCOUNT("user"), Configparser_PO.ACCOUNT("password"))
# 菜单
d_menu_basicPHS = {'健康档案概况': 'http://192.168.0.203:30080/phs/HealthRecord/ehrindex', '个人健康档案': 'http://192.168.0.203:30080/phs/HealthRecord/Personal', '家庭健康档案': 'http://192.168.0.203:30080/phs/HealthRecord/Family', '迁入申请': 'http://192.168.0.203:30080/phs/HealthRecord/Immigration', '迁出审核': 'http://192.168.0.203:30080/phs/HealthRecord/Exit', '档案交接': 'http://192.168.0.203:30080/phs/HealthRecord/handoverFile', '死亡管理': 'http://192.168.0.203:30080/phs/HealthRecord/DeathManagement', '区域档案查询': 'http://192.168.0.203:30080/phs/HealthRecord/regionalFile', '接诊信息查询': 'http://192.168.0.203:30080/phs/HealthRecord/Diagnosis', '就诊管理': 'http://192.168.0.203:30080/phs/HealthRecord/Visit', '高血压专项': 'http://192.168.0.203:30080/phs/Hypertension/gxyregister', '高血压随访': 'http://192.168.0.203:30080/phs/Hypertension/gxyjob', '高血压报病': 'http://192.168.0.203:30080/phs/Hypertension/gxybb', '糖尿病专项': 'http://192.168.0.203:30080/phs/Diabetes/tnbregister', '糖尿病随访': 'http://192.168.0.203:30080/phs/Diabetes/tnbjob', '糖尿病报病': 'http://192.168.0.203:30080/phs/Diabetes/tnbbb', '慢阻肺病登记': 'http://192.168.0.203:30080/phs/Copd/register', '慢阻肺病专项': 'http://192.168.0.203:30080/phs/Copd/project', '慢阻肺病随访': 'http://192.168.0.203:30080/phs/Copd/visit', '儿童概况': 'http://192.168.0.203:30080/phs/Child/etindex', '儿童健康档案': 'http://192.168.0.203:30080/phs/Child/etfiles', '中医体质辨识列表': 'http://192.168.0.203:30080/phs/Child/tcm', '中医体质辨识汇总': 'http://192.168.0.203:30080/phs/Child/tzbs', '儿童检查记录': 'http://192.168.0.203:30080/phs/Child/etjob', '孕产妇概况': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfindex', '孕产妇登记': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfregister', '孕产妇档案': 'http://192.168.0.203:30080/phs/MaternalRecord/ycffiles', '孕产妇随访': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfjob', '老年人概况': 'http://192.168.0.203:30080/phs/Snr/lnrindex', '老年人专项登记': 'http://192.168.0.203:30080/phs/Snr/special', '老年人专项管理': 'http://192.168.0.203:30080/phs/Snr/lnrfiles', '本年度未体检': 'http://192.168.0.203:30080/phs/Snr/unexamined', '老年人中医体质辨识': 'http://192.168.0.203:30080/phs/Snr/chMedicine', '老年人自理能力评估查询': 'http://192.168.0.203:30080/phs/Snr/selfCareAssess', '老年人抑郁评估查询': 'http://192.168.0.203:30080/phs/Snr/depressed', '简易智力检查查询': 'http://192.168.0.203:30080/phs/Snr/intelligence', '体检登记': 'http://192.168.0.203:30080/phs/HealthExamination/tjregister', '体检记录': 'http://192.168.0.203:30080/phs/HealthExamination/tjrecord', '未体检人员': 'http://192.168.0.203:30080/phs/HealthExamination/tjunexam', '肺结核患者概况': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhindex', '肺结核登记': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhregister', '肺结核管理': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhfiles', '残疾人概况': 'http://192.168.0.203:30080/phs/Disabled/cjrindex', '残疾人登记': 'http://192.168.0.203:30080/phs/Disabled/cjrregister', '残疾人管理': 'http://192.168.0.203:30080/phs/Disabled/cjrfiles', '严重精神障碍登记': 'http://192.168.0.203:30080/phs/MentalDisorder/jsregister', '严重精神障碍患者': 'http://192.168.0.203:30080/phs/MentalDisorder/jsfiles', '严重精神病障碍随访': 'http://192.168.0.203:30080/phs/MentalDisorder/jsjob', '严重精神障碍概况': 'http://192.168.0.203:30080/phs/MentalDisorder/jsindex', '健康教育活动': 'http://192.168.0.203:30080/phs/HealthEducation/HealthActivity', '本年度未评': 'http://192.168.0.203:30080/phs/hbp/noassessdata', '评分信息查询': 'http://192.168.0.203:30080/phs/hbp/assessdata'}
# varUrl = d_menu_basicPHS['慢阻肺病专项']
Web_PO.opnLabel(d_menu_basicPHS['慢阻肺病专项'])
Web_PO.swhLabel(1)



# todo 1 查询
Gw_PO.phs_copd_project_query({"身份证号": "370685198705183027"})
# Gw_PO.phs_copd_project_query({"姓名": "胡成", "身份证号": "110101193901013599",
#                               "上次随访日期": [[2025, 1, 1], [2025, 1, 2]], "下次随访日期": [[2025, 1, 3], [2025, 1, 4]],
#                               "建卡日期": [[2025, 2, 1], [2025, 2, 2]], "建档日期": [[2025, 2, 3], [2025, 2, 4]],
#                               "档案管理机构": ["招远市卫健局"], "档案状态": "在档",
#                               "是否终止管理": "否", "随访提醒分类": "常规管理", "建卡医生": "zhangsan",
#                               "出生日期范围": [[2025, 2, 5], [2025, 2, 6]], "现住址": ["泉山街道", "花园社区居民委员会", "123"],
#                               "随访评价结果": "不良反应"})

# todo 2 导出(.xls)
# Gw_PO.phs_copd_project_export("/Users/linghuchong/Desktop/333")


# todo 3 详情
# Gw_PO.phs_copd_project_operation({'operate': '详情', 'option': {"身份证号": "370685198705183027"}})
# Gw_PO.phs_copd_project_operation({'operate': '详情', 'index': {'operate2': '编辑'},
#                                    'value':{' 居住地址 ': ['上海市', '市辖区', '虹口区', '广中路街道', '商业一村居委会', '多媒体100号'],
#                                    ' 确诊日期 ': [2024, 7, 1],
#                                    ' 是否终止管理 ': '是', '终止管理日期': [2025, 2, 5], '终止管理原因': "nono",
#                                    '建卡时间': [2025, 2, 2], '建卡医生': "卫生院"}})




# todo 4 随访
Gw_PO.phs_copd_project_operation({'operate': '随访', 'option': {"身份证号": "370685198705183027"}})
Gw_PO.phs_copd_project_operation({'operate': '随访', 'index': {'operate2': '新增'},
                                   'value': {'随访日期': [2025, 2, 9], '随访方式': '网络', '症状': ['呼吸困难', {'其他': '123'}, '发热'],
                                   '口唇紫绀': '100', '外周水肿': '101', '呼吸频率': '12', '心率': '44', '体质指数': '55', '其他': "测试一下",
                                   '合并症': ['感染', {'其他': '12345'}, '肺癌'], '日吸烟量': '56',
                                   '运动本次': [11, 23], '运动目标':[12, 44],
                                   '心理调整': '一般', '遵医行为': '差',
                                   '疫苗免疫史':{'有': ['流感疫苗', '新冠病毒疫苗']}, 'SpO₂': '12', 'FEV1': '23', 'FVC': '55', 'FEV1/ FVC': '44',
                                   '用药情况药物名称1':'test1', '用药情况用法用量1每日':'每日一次', '用药情况用法用量1每次':'1',
                                   '用药情况药物名称2':'test2', '用药情况用法用量2每日':'每日二次', '用药情况用法用量2每次':'2',
                                   '用药情况药物名称3':'test3', '用药情况用法用量3每日':'每日三次', '用药情况用法用量3每次':'3',
                                   '服药依从性': '间断', '药物不良反应': ['有','5555'],
                                   '家庭氧疗': [2, 100, ['有', '456']], '无创呼吸机使用': [3, 300, ['有', '77']],
                                   '随访评价结果': '不良反应', '下一步管理措施': "两次控制不满意转诊随访",
                                   '用药调整意见药物名称1':'test4', '用药调整意见用法用量1每日':'一次性', '用药调整意见用法用量1每次':'4',
                                   '用药调整意见药物名称2':'test5', '用药调整意见用法用量2每日':'必要时', '用药调整意见用法用量2每次':'5',
                                   '用药调整意见药物名称3':'test6', '用药调整意见用法用量3每日':'一次性', '用药调整意见用法用量3每次':'6',
                                   '转诊原因':'123', '机构及科室':'456', '联系人及电话': ['lisi', '57665432'], '结果':'到位', '备注':'nonono',
                                   '下次随访日期': [2025, 2, 9], '随访医生': '测试1', '居民签字': '张三丰'}})
#
# Gw_PO.phs_hypertension_gxyregister_operation(['', '随访点击新增'])
#

# Gw_PO.phs_diabetes_tnbregister_operation({'operate': '随访', 'option': {'建卡日期': '2024-07-09'}})  # 无历史随访记录，编辑新增
# Gw_PO.phs_diabetes_tnbregister_operation({'operate': '随访', 'index': {'operate2': '新增'},
# Gw_PO.phs_hypertension_gxyregister_operation([{'随访日期': [2025, 3, 9], '随访方式': '网络', '症状': ['头痛头晕', {'其他': '123'}, '下肢水肿'],
#                                                '血压': [1, 2], '身高': '166', '体重': [33, 44], '心率':'90', '其他': "测试2下",
#                                                '日吸烟量':[5, 7], '日饮酒量':[110, 244],
#                                                '运动频率实际': '每天', '运动频率目标': '不运动',
#                                                '运动时长':[6, 22], '摄盐量分级实际': '轻', '摄盐量分级目标': '中', '随访饮食合理性评价': '合理', '心理调整评价结果': '差', '随访遵医行为': '一般',
#                                                '辅助检查': '1212', '服药依从性': '间断', '药物不良反应': ['有','5555'], '随访评价结果': '不良反应', '下一步管理措施': "两次控制不满意转诊随访",
#                                                '用药情况药物名称1':'test11', '用药情况用法用量1每日':'每日一次', '用药情况用法用量1每次':'11',
#                                                '用药情况药物名称2':'test22', '用药情况用法用量2每日':'每日二次', '用药情况用法用量2每次':'22',
#                                                '用药情况药物名称3':'test33', '用药情况用法用量3每日':'每日三次', '用药情况用法用量3每次':'33',
#                                                '用药调整意见药物名称1':'test44', '用药调整意见用法用量1每日':'一次性', '用药调整意见用法用量1每次':'44',
#                                                '用药调整意见药物名称2':'test55', '用药调整意见用法用量2每日':'必要时', '用药调整意见用法用量2每次':'55',
#                                                '用药调整意见药物名称3':'test66', '用药调整意见用法用量3每日':'一次性', '用药调整意见用法用量3每次':'66',
#                                                '转诊原因':'qqq', '转入医疗机构及科室':'www', '联系人':'eee', '联系人电话':'rrr', '结果':'不到位', '备注':'good',
#                                                '下次随访日期': [2025, 1, 19], '随访医生':'测试2', '居民签字': '李泽楷'}, '随访新增'])

