# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-3-11
# Description: 基本公卫 - 老年人健康管理 - 简易智力检查查询
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
Web_PO.opnLabel(d_menu_basicPHS['简易智力检查查询'])
Web_PO.swhLabel(1)


# todo 1 查询
Gw_PO.phs_snr_intelligence_query({"身份证号": "110101195901015999"})
# Gw_PO.phs_snr_intelligence_query({"姓名": "胡成", "身份证号": "110101195901015999", '出生日期': [[2025,1,1],[2025,2,2]], '评估日期': [[2025,1,13],[2025,2,12]],
#     "管理机构": "招远市卫健局", '是否仅查询机构': '是',"现住址": ["泉山街道", "花园社区居民委员会", "123"]})



# todo 2 导出
# Gw_PO.export("/Users/linghuchong/Desktop/phs_snr_intelligence.xls")


# todo 3 操作 - 详情
# Gw_PO.phs_snr_intelligence_operation({'operate': '详情', 'option': {"身份证号": "110101193801014615"}})


# todo 4 操作 - 编辑 (简易智力检查查询)
# Gw_PO.phs_snr_intelligence_operation({'operate': '编辑', 'option': {"身份证号": "110101195901015999"}})
# Gw_PO.phs_snr_intelligence_operation({'operate': '编辑', 'data': {
#     "1.时间定力 (5)": {"今年是哪一年?": "0", "现在是什么季节": "0", "现在是几月份": "0", "今天是几号": "0", "今天是星期几": "0"},
#     "2.地点定向力 (5)": {"我们现在在哪个国家?": "0", "我们现在在哪个城市": "0", "我们现在在城市的哪一部分": "0", "我们现在在哪个建筑物": "0", "我们现在在第几层": "0"},
#     "3.即刻回忆 (3)": {"皮球": "0", "国旗": "0", "树": "0"},
#     "4.注意力与计算力 (5)": {"100减7等于? 93": "0", "100减7等于? 86": "0", "100减7等于? 79": "0", "100减7等于? 72": "0", "100减7等于? 65": "0"},
#     "5.回忆能力 (3)": {"皮球": "0", "国旗": "0", "树": "0"},
#     "6.命名能力 (2)": {"问:这是什么? 展示 (铅笔)": "0", "问:这是什么? 展示 (手表)": "0"},
#     "7.语言重复能力 (1)": {"说:我现在让你重复我说的。准备好了吗？瑞雪兆丰年。你说一遍 ": "0"},
#     "8.理解力 (3)": {"左手拿着这张纸": "0", "把它对折": "0", "把它放在你的右腿上": "0"},
#     "9.阅读能力 (1)": {"闭上你的眼睛": "0"},
#     "10.写的能力 (1)": {"说:写一个句子。": "0"},
#     "11.画画的能力 (1)": {"说:照下图画。 ": "0"}
# }})

# # todo 5 操作 - 删除
Gw_PO.phs_snr_intelligence_operation({'operate': '删除', 'option': {"身份证号": "110101195901015999"}})

