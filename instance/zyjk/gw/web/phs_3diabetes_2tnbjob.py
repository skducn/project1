# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-10
# Description: 基本公卫 - 糖尿病管理 - 糖尿病随访
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
Web_PO.opnLabel(d_menu_basicPHS['糖尿病随访'])
Web_PO.swhLabel(1)



# todo 1 查询
Gw_PO.phs_diabetes_tnbjob_query({"身份证号": "370685202402190640"})
# Gw_PO.phs_diabetes_tnbjob_query({"姓名": "胡成", "身份证号": "230202194504020016", "管理机构": ["招远市卫健局"], "随访日期": [[2025, 1, 1], [2025, 1, 2]],
#                                  "随访医生": "zhangsan", "随访方式": "电话", "是否终止管理": "否", "空腹血糖": [11, 12],
#                                  "随访评价结果": "不良反应", "出生日期范围": [[2025, 2, 5], [2025, 2, 6]], '数据源': '公卫随访',
#                                  "现住址": ["泉山街道", "花园社区居民委员会", "123"]
#                                     })


# todo 2 导出(17.xls)
# Gw_PO.phs_diabetes_tnbjob_export("/Users/linghuchong/Desktop/1756")



# todo 3 详情
Gw_PO.phs_diabetes_tnbjob_operation([{'随访医生': 'test'}, '详情'])
# Gw_PO.phs_diabetes_tnbjob_operation([{' 管理级别 ': "二级", ' 是否终止管理 ': '是'}, '详情编辑'])
# Gw_PO.phs_diabetes_tnbjob_operation([{' 是否终止管理 ': '否', ' 终止管理日期 ': [2025, 2, 5], ' 终止管理原因 ': "nono",
#                                                ' 建卡时间 ': [2025, 2, 2], ' 建卡医生 ':"卫生院", ' 建卡医疗机构 ': "待定机构",
#                                                }, '详情编辑'])
# Gw_PO.phs_diabetes_tnbjob_operation([{' 居住住址 ': ['上海市', '市辖区', '虹口区', '广中路街道', '商业一村居委会', '多媒体100号'],
#                                                ' 确诊日期 ': [2024, 7, 1], ' 管理级别 ': "二级",
#                                                ' 是否终止管理 ': '否', ' 终止管理日期 ': [2025, 2, 5], ' 终止管理原因 ': "nono",
#                                                ' 建卡时间 ': [2025, 2, 2], ' 建卡医生 ':"卫生院", ' 建卡医疗机构 ': "待定机构"}, '详情编辑'])



# todo 4 删除
# Gw_PO.phs_diabetes_tnbjob_operation([{'随访医生': 'test'}, '删除'])
