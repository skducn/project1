# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-12-19
# Description: 公卫 - 基本公卫 - 迁入申请
# *****************************************************************

import os
folder = "./" + os.path.basename(__file__).split('.')[0]
logName = folder + ".log"

from GwPO import *
Gw_PO = GwPO(logName)

from PO.FilePO import *
File_PO = FilePO()

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')

d_menu_basicPHS = {'健康档案概况': 'http://192.168.0.203:30080/phs/HealthRecord/ehrindex', '个人健康档案': 'http://192.168.0.203:30080/phs/HealthRecord/Personal', '家庭健康档案': 'http://192.168.0.203:30080/phs/HealthRecord/Family', '迁入申请': 'http://192.168.0.203:30080/phs/HealthRecord/Immigration', '迁出审核': 'http://192.168.0.203:30080/phs/HealthRecord/Exit', '档案交接': 'http://192.168.0.203:30080/phs/HealthRecord/handoverFile', '死亡管理': 'http://192.168.0.203:30080/phs/HealthRecord/DeathManagement', '区域档案查询': 'http://192.168.0.203:30080/phs/HealthRecord/regionalFile', '接诊信息查询': 'http://192.168.0.203:30080/phs/HealthRecord/Diagnosis', '就诊管理': 'http://192.168.0.203:30080/phs/HealthRecord/Visit', '高血压专项': 'http://192.168.0.203:30080/phs/Hypertension/gxyregister', '高血压随访': 'http://192.168.0.203:30080/phs/Hypertension/gxyjob', '高血压报病': 'http://192.168.0.203:30080/phs/Hypertension/gxybb', '糖尿病专项': 'http://192.168.0.203:30080/phs/Diabetes/tnbregister', '糖尿病随访': 'http://192.168.0.203:30080/phs/Diabetes/tnbjob', '糖尿病报病': 'http://192.168.0.203:30080/phs/Diabetes/tnbbb', '慢阻肺病登记': 'http://192.168.0.203:30080/phs/Copd/register', '慢阻肺病专项': 'http://192.168.0.203:30080/phs/Copd/project', '慢阻肺病随访': 'http://192.168.0.203:30080/phs/Copd/visit', '儿童概况': 'http://192.168.0.203:30080/phs/Child/etindex', '儿童健康档案': 'http://192.168.0.203:30080/phs/Child/etfiles', '中医体质辨识列表': 'http://192.168.0.203:30080/phs/Child/tcm', '中医体质辨识汇总': 'http://192.168.0.203:30080/phs/Child/tzbs', '儿童检查记录': 'http://192.168.0.203:30080/phs/Child/etjob', '孕产妇概况': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfindex', '孕产妇登记': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfregister', '孕产妇档案': 'http://192.168.0.203:30080/phs/MaternalRecord/ycffiles', '孕产妇随访': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfjob', '老年人概况': 'http://192.168.0.203:30080/phs/Snr/lnrindex', '老年人专项登记': 'http://192.168.0.203:30080/phs/Snr/special', '老年人专项管理': 'http://192.168.0.203:30080/phs/Snr/lnrfiles', '本年度未体检': 'http://192.168.0.203:30080/phs/Snr/unexamined', '老年人中医体质辨识': 'http://192.168.0.203:30080/phs/Snr/chMedicine', '老年人自理能力评估查询': 'http://192.168.0.203:30080/phs/Snr/selfCareAssess', '老年人抑郁评估查询': 'http://192.168.0.203:30080/phs/Snr/depressed', '简易智力检查查询': 'http://192.168.0.203:30080/phs/Snr/intelligence', '体检登记': 'http://192.168.0.203:30080/phs/HealthExamination/tjregister', '体检记录': 'http://192.168.0.203:30080/phs/HealthExamination/tjrecord', '未体检人员': 'http://192.168.0.203:30080/phs/HealthExamination/tjunexam', '肺结核患者概况': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhindex', '肺结核登记': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhregister', '肺结核管理': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhfiles', '残疾人概况': 'http://192.168.0.203:30080/phs/Disabled/cjrindex', '残疾人登记': 'http://192.168.0.203:30080/phs/Disabled/cjrregister', '残疾人管理': 'http://192.168.0.203:30080/phs/Disabled/cjrfiles', '严重精神障碍登记': 'http://192.168.0.203:30080/phs/MentalDisorder/jsregister', '严重精神障碍患者': 'http://192.168.0.203:30080/phs/MentalDisorder/jsfiles', '严重精神病障碍随访': 'http://192.168.0.203:30080/phs/MentalDisorder/jsjob', '严重精神障碍概况': 'http://192.168.0.203:30080/phs/MentalDisorder/jsindex', '健康教育活动': 'http://192.168.0.203:30080/phs/HealthEducation/HealthActivity', '本年度未评': 'http://192.168.0.203:30080/phs/hbp/noassessdata', '评分信息查询': 'http://192.168.0.203:30080/phs/hbp/assessdata'}


# 1，登录
Gw_PO.login(Configparser_PO.HTTP("url"), Configparser_PO.ACCOUNT("user"), Configparser_PO.ACCOUNT("password"))


# todo 2 基本公卫

# todo 4, 健康档案管理 - 迁入申请
Web_PO.opnLabel(d_menu_basicPHS['迁入申请'])
Web_PO.swhLabel(1)

# 1 查询
# Gw_PO.movingIn_query({"姓名": "六四", "身份证号": "370685196005183025", "申请日期": [[2025, 1, 1], [2025, 1, 2]],
#                       "申请机构": ["招远市卫健局"], "申请人": "test", "状态": "已批准"})

# 2 查看
# Gw_PO.movingIn_query({"身份证号": "370685196005183025"})  # 查询
# Gw_PO.movingIn_operation('查看')
# d_info = Gw_PO.movingIn_detail()
# print(d_info) # {'申请信息': {'姓名': '六四', '性别': '女', '身份证号': '370685196005183025', '现住址': '山东省烟台市招远市南炉社区居民委员会fdsa', '联系电话': '15800000002', '建档单位': '大秦家卫生院', '申请单位': '妇幼保健院', '申请人': 'xiao', '管理机构': '妇幼保健院', '建档日期': '2024-11-28', '申请日期': '2024-11-29', '申请原因': 'fasd'}, '审批结果': '同意', '审批信息': {'审核日期': '2024-11-29', '审核人': '1'}}

# # 3 撤回
# Gw_PO.movingIn_query({"身份证号": "110101195901018874"})  # 查询
# Gw_PO.movingIn_operation('撤回')

# 4 新增
# Gw_PO.movingIn_new({"身份证号": "370685196005183025", '勾选': ['六四'], "申请迁入原因": "不知道test123", "迁入地址": ['山东省', '烟台市', '招远市', '辛庄镇', '小宋家村民委员会', '甲方100号']})
# Gw_PO.movingIn_new({"身份证号": "370685196005183025", '勾选': '所有人', "申请迁入原因": "不知道test123", "迁入地址": ['山东省', '烟台市', '招远市', '辛庄镇', '小宋家村民委员会', '甲方100号']})






