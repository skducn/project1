# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-10
# Description: 基本公卫 - 慢性阻塞性肺病管理 - 慢阻肺病随访
# *****************************************************************
import sys,os
# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取 上层 目录的绝对路径
project_dir = os.path.abspath(os.path.join(current_dir, '..'))
# 将 上层 目录添加到 sys.path
sys.path.insert(0, project_dir)
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName)
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('../config.ini')
# 登录
Gw_PO.login(Configparser_PO.HTTP("url"), Configparser_PO.ACCOUNT("user"), Configparser_PO.ACCOUNT("password"))
# 菜单
d_menu_basicPHS = {'健康档案概况': 'http://192.168.0.203:30080/phs/HealthRecord/ehrindex', '个人健康档案': 'http://192.168.0.203:30080/phs/HealthRecord/Personal', '家庭健康档案': 'http://192.168.0.203:30080/phs/HealthRecord/Family', '迁入申请': 'http://192.168.0.203:30080/phs/HealthRecord/Immigration', '迁出审核': 'http://192.168.0.203:30080/phs/HealthRecord/Exit', '档案交接': 'http://192.168.0.203:30080/phs/HealthRecord/handoverFile', '死亡管理': 'http://192.168.0.203:30080/phs/HealthRecord/DeathManagement', '区域档案查询': 'http://192.168.0.203:30080/phs/HealthRecord/regionalFile', '接诊信息查询': 'http://192.168.0.203:30080/phs/HealthRecord/Diagnosis', '就诊管理': 'http://192.168.0.203:30080/phs/HealthRecord/Visit', '高血压专项': 'http://192.168.0.203:30080/phs/Hypertension/gxyregister', '高血压随访': 'http://192.168.0.203:30080/phs/Hypertension/gxyjob', '高血压报病': 'http://192.168.0.203:30080/phs/Hypertension/gxybb', '糖尿病专项': 'http://192.168.0.203:30080/phs/Diabetes/tnbregister', '糖尿病随访': 'http://192.168.0.203:30080/phs/Diabetes/tnbjob', '糖尿病报病': 'http://192.168.0.203:30080/phs/Diabetes/tnbbb', '慢阻肺病登记': 'http://192.168.0.203:30080/phs/Copd/register', '慢阻肺病专项': 'http://192.168.0.203:30080/phs/Copd/project', '慢阻肺病随访': 'http://192.168.0.203:30080/phs/Copd/visit', '儿童概况': 'http://192.168.0.203:30080/phs/Child/etindex', '儿童健康档案': 'http://192.168.0.203:30080/phs/Child/etfiles', '中医体质辨识列表': 'http://192.168.0.203:30080/phs/Child/tcm', '中医体质辨识汇总': 'http://192.168.0.203:30080/phs/Child/tzbs', '儿童检查记录': 'http://192.168.0.203:30080/phs/Child/etjob', '孕产妇概况': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfindex', '孕产妇登记': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfregister', '孕产妇档案': 'http://192.168.0.203:30080/phs/MaternalRecord/ycffiles', '孕产妇随访': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfjob', '老年人概况': 'http://192.168.0.203:30080/phs/Snr/lnrindex', '老年人专项登记': 'http://192.168.0.203:30080/phs/Snr/special', '老年人专项管理': 'http://192.168.0.203:30080/phs/Snr/lnrfiles', '本年度未体检': 'http://192.168.0.203:30080/phs/Snr/unexamined', '老年人中医体质辨识': 'http://192.168.0.203:30080/phs/Snr/chMedicine', '老年人自理能力评估查询': 'http://192.168.0.203:30080/phs/Snr/selfCareAssess', '老年人抑郁评估查询': 'http://192.168.0.203:30080/phs/Snr/depressed', '简易智力检查查询': 'http://192.168.0.203:30080/phs/Snr/intelligence', '体检登记': 'http://192.168.0.203:30080/phs/HealthExamination/tjregister', '体检记录': 'http://192.168.0.203:30080/phs/HealthExamination/tjrecord', '未体检人员': 'http://192.168.0.203:30080/phs/HealthExamination/tjunexam', '肺结核患者概况': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhindex', '肺结核登记': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhregister', '肺结核管理': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhfiles', '残疾人概况': 'http://192.168.0.203:30080/phs/Disabled/cjrindex', '残疾人登记': 'http://192.168.0.203:30080/phs/Disabled/cjrregister', '残疾人管理': 'http://192.168.0.203:30080/phs/Disabled/cjrfiles', '严重精神障碍登记': 'http://192.168.0.203:30080/phs/MentalDisorder/jsregister', '严重精神障碍患者': 'http://192.168.0.203:30080/phs/MentalDisorder/jsfiles', '严重精神病障碍随访': 'http://192.168.0.203:30080/phs/MentalDisorder/jsjob', '严重精神障碍概况': 'http://192.168.0.203:30080/phs/MentalDisorder/jsindex', '健康教育活动': 'http://192.168.0.203:30080/phs/HealthEducation/HealthActivity', '本年度未评': 'http://192.168.0.203:30080/phs/hbp/noassessdata', '评分信息查询': 'http://192.168.0.203:30080/phs/hbp/assessdata'}
Web_PO.opnLabel(d_menu_basicPHS['慢阻肺病随访'])
Web_PO.swhLabel(1)



# todo 1 查询
# Gw_PO.phs_copd_visit_query({"身份证号": "340203202407016690"})
# Gw_PO.phs_copd_visit_query({"姓名": "胡成", "身份证号": "340203202407016690", "管理机构": "招远市卫健局",
#                             "随访日期": [[2025, 1, 1], [2025, 1, 2]], "随访医生": "zhangsan", "随访方式": "电话", "是否终止管理": "否", '血氧饱和度': [12, 33],
#                             "空腹血糖": [11, 12], "随访评价结果": "不良反应", "出生日期范围": [[2025, 2, 5], [2025, 2, 6]],
#                             '数据源': '公卫随访', "现住址": ["泉山街道", "花园社区居民委员会", "123"]
#                                     })


# todo 2 导出(17.xls)
# Gw_PO.phs_copd_visit_export("/Users/linghuchong/Desktop/phs_copd_visit.xls")



# todo 3 详情
Gw_PO.phs_copd_visit_operation({'operate': '详情', 'option': {"身份证号": "340203202407016690"}})


# todo 3 编辑 - 新增
Gw_PO.phs_copd_visit_operation({'operate': '编辑', 'option': {"身份证号": "370685198705183027"}})
Gw_PO.phs_copd_visit_operation({'operate': '编辑', 'index': {'operate2': '新增'},
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


# todo 3 编辑 - 引入上次新增
Gw_PO.phs_copd_visit_operation({'operate': '编辑', 'option': {"身份证号": "340203202407016690"}})
Gw_PO.phs_copd_visit_operation({'operate': '编辑', 'index': {'operate2': '引入上次新增'},
                                   'value': {'随访日期': [2025, 2, 9], '下次随访日期': [2025, 2, 9]}})


# todo 4 删除
# Gw_PO.phs_copd_visit_operation([{'随访医生': 'test'}, '删除'])

# # todo 5 删除
Gw_PO.phs_copd_visit_query({"身份证号": "370685202402190640"})
Gw_PO.phs_copd_visit_operation({'operate': '删除', 'option': {'随访日期': '2025-02-09'}})

