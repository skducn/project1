# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-7
# Description: 基本公卫 - 糖尿病管理 - 糖尿病专项
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
Web_PO.opnLabel(d_menu_basicPHS['糖尿病专项'])
Web_PO.swhLabel(1)



# todo 1 查询
Gw_PO.phs_diabetes_tnbregister_query({"身份证号": "370685202402190640"})
# Gw_PO.phs_diabetes_tnbregister_query({"姓名": "胡成", "身份证号": "370685202402190640",
#                                       "上次随访日期": [[2025, 1, 1], [2025, 1, 2]],"下次随访日期": [[2025, 1, 3], [2025, 1, 4]],
#                                       "建卡日期": [[2025, 2, 1], [2025, 2, 2]], "建档日期": [[2025, 2, 3], [2025, 2, 4]],
#                                       "档案管理机构": "招远市卫健局", "档案状态": "在档",
#                                       "是否终止管理": "否", "随访提醒分类": "常规管理", "建卡医生": "zhangsan",
#                                       "出生日期范围": [[2025, 2, 5], [2025, 2, 6]], "现住址": ["泉山街道", "花园社区居民委员会", "123"],
#                                       "随访评价结果": "不良反应" })


# todo 2 导出(.xls)
# Gw_PO.export("/Users/linghuchong/Desktop/phs_diabetes_tnbregister.xlsx")



# todo 3 详情 - 编辑(糖尿病患者管理卡)
# Gw_PO.phs_diabetes_tnbregister_operation({'operate': '详情', 'option': {'建卡日期': '2025-02-02'}})
# Gw_PO.phs_diabetes_tnbregister_operation({'operate': '详情', 'operate2': '编辑', 'data': {
#     ' 居住地址 ': ['上海市', '市辖区', '虹口区', '广中路街道', '商业一村居委会', '多媒体100号'],
#     ' 确诊日期 ': [2024, 2, 2], ' 是否终止管理 ': '否',
#     '建卡时间': [2025, 2, 2], '建卡医生': "卫生院"
#     }})



# # todo 4 评估 - 新增(糖尿病患者评估)
# Gw_PO.phs_diabetes_tnbregister_operation({'operate': '评估', 'option': {'建卡日期': '2025-02-02'}})
# Gw_PO.phs_diabetes_tnbregister_operation({'operate': '评估', 'operate2': '新增', 'data': {
#     ' 空腹血糖 ': '理想', ' 餐后血糖 ': "良好", ' 糖化血红蛋白 ': '差', ' 血压评价 ': '差',
#     ' BMI评价 ': '理想', ' 总胆固醇 ': "良好", ' 高密度脂蛋白胆固醇 ': '差', ' 低密度脂蛋白胆固醇 ': '差',
#     ' 吸烟 ': '改善', ' 饮酒 ': "恶化", ' 体育锻炼 ': '不变', ' 食盐摄入量 ': '不变',
#     ' 遵医行为 ': '改善', ' 饮食 ': "恶化", ' 心理状态 ': '不变', '管理程度': '强化管理',
#     ' 降糖效果 ': '血糖异常', ' 总体评价 ': "良好",
#     '评估日期': [2024, 7, 1]}})


# todo 5.1 随访 - 新增(糖尿病随访记录)
# Gw_PO.phs_diabetes_tnbregister_operation({'operate': '随访', 'option': {'建卡日期': '2025-02-02'}})  # 有历史随访记录，点击新增
# # Gw_PO.phs_diabetes_tnbregister_operation({'operate': '随访', 'option': {'建卡日期': '2024-07-09'}})  # 无历史随访记录，编辑新增
# Gw_PO.phs_diabetes_tnbregister_operation({'operate': '随访', 'operate2': '新增', 'data': {
#     '随访日期': [2025, 2, 9], '随访方式': '网络', '症状': ['头痛头晕', {'其他': '123'}, '下肢水肿'],
#     '血压': [11, 12], '身高': '177', '体重': [66, 77], '足背动脉搏动':'未检测', '其他': "测试一下",
#     '日吸烟量':[11,14], '日饮酒量':[112,144],
#     '运动频率实际': '每天', '运动频率目标': '不运动',
#     '运动时长':[11, 23],
#     '日主食量': [1, 5], '饮食情况': '不控制', '心理调整评价结果': '差', '随访遵医行为': '一般',
#     '辅助检查': '1212', '服药情况': '完全遵医嘱', '药物不良反应': ['有','5555'], '随访评价结果': '不良反应', '下一步管理措施': "两次控制不满意转诊随访",
#     '用药情况药物名称1':'阿莫西林100', '用药情况用法用量1每日':'每日一次', '用药情况用法用量1每次':'1',
#     '用药情况药物名称2':'阿莫西林冲剂', '用药情况用法用量2每日':'每日二次', '用药情况用法用量2每次':'2',
#     '用药情况药物名称3':'阿莫西林测试', '用药情况用法用量3每日':'每日三次', '用药情况用法用量3每次':'3',
#     '用药调整意见药物名称1':'阿莫西林胶囊', '用药调整意见用法用量1每日':'一次性', '用药调整意见用法用量1每次':'4',
#     '用药调整意见药物名称2':'阿莫西林钠克拉维酸钾（二叶克）', '用药调整意见用法用量2每日':'必要时', '用药调整意见用法用量2每次':'5',
#     '用药调整意见药物名称3':'阿莫西林钠/克拉维酸钾', '用药调整意见用法用量3每日':'一次性', '用药调整意见用法用量3每次':'6',
#     '转诊原因':'123', '转入医疗机构及科室':'456', '联系人':'789', '联系人电话':'1000', '结果':'到位', '备注':'nonono',
#     '下次随访日期': [2025, 2, 9], '随访医生':'测试1', '居民签字': '张三丰'}})


# todo 5.2 随访 - 引入上次新增(糖尿病随访记录)
# Gw_PO.phs_diabetes_tnbregister_operation({'operate': '随访', 'option': {'建卡日期': '2025-02-02'}})
# Gw_PO.phs_diabetes_tnbregister_operation({'operate': '随访', 'operate2': '引入上次新增', "data": {
#     '随访日期': [2025, 2, 9], '下次随访日期': [2025, 5, 9]}})


# todo 6 姓名 (更新)
# Gw_PO.phs_diabetes_tnbregister_operation({'operate': '姓名', 'option': {'建卡日期': '2025-02-02'}})
# Gw_PO.phs_diabetes_tnbregister_operation({'operate': '姓名', 'operate2': '更新', 'data': {
#     '随访日期': [2025, 2, 9], '随访方式': '网络', '症状': ['头痛头晕', {'其他': '123'}, '下肢水肿'],
#     '血压': [11, 12], '身高': '177', '体重': [66, 77], '足背动脉搏动':'未检测', '其他': "测试一下",
#     '日吸烟量':[11,14], '日饮酒量':[112,144],
#     '运动频率实际': '每天', '运动频率目标': '不运动',
#     '运动时长':[11, 23],
#     '日主食量': [1, 5], '饮食情况': '不控制', '心理调整评价结果': '差', '随访遵医行为': '一般',
#     '辅助检查': '1212', '服药情况': '完全遵医嘱', '药物不良反应': ['有','5555'], '随访评价结果': '不良反应', '下一步管理措施': "两次控制不满意转诊随访",
#     '用药情况药物名称1':'阿莫西林100', '用药情况用法用量1每日':'每日一次', '用药情况用法用量1每次':'1',
#     '用药情况药物名称2':'阿莫西林冲剂', '用药情况用法用量2每日':'每日二次', '用药情况用法用量2每次':'2',
#     '用药情况药物名称3':'阿莫西林测试', '用药情况用法用量3每日':'每日三次', '用药情况用法用量3每次':'3',
#     '用药调整意见药物名称1':'阿莫西林胶囊', '用药调整意见用法用量1每日':'一次性', '用药调整意见用法用量1每次':'4',
#     '用药调整意见药物名称2':'阿莫西林钠克拉维酸钾（二叶克）', '用药调整意见用法用量2每日':'必要时', '用药调整意见用法用量2每次':'5',
#     '用药调整意见药物名称3':'阿莫西林钠/克拉维酸钾', '用药调整意见用法用量3每日':'一次性', '用药调整意见用法用量3每次':'6',
#     '转诊原因':'123', '转入医疗机构及科室':'456', '联系人':'789', '联系人电话':'1000', '结果':'到位', '备注':'nonono',
#     '下次随访日期': [2025, 2, 9], '随访医生':'测试1', '居民签字': '张三丰'}})


# todo 6 姓名（获取）
Gw_PO.phs_diabetes_tnbregister_operation({'operate': '姓名', 'option': {'建卡日期': '2025-02-02'}})
d_ = Gw_PO.phs_diabetes_tnbregister_operation({'operate': '姓名', 'operate2': '获取', 'data': {}})
print(d_)  # {'身份证号码': ['372922198510281068'], '档案编号': ['37068500100100157'], ...

