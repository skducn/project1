# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-12-19
# Description: 公卫 - 基本公卫 - 健康行为积分
# *****************************************************************

import cProfile


from GwPO import *
Gw_PO = GwPO("./2_healthBehaviorScore.log")

from PO.FilePO import *
File_PO = FilePO()

from PO.PandasPO import *
Pandas_PO = PandasPO()


# 1，登录
Gw_PO.login('http://192.168.0.203:30080/#/login', '11011', 'HHkk2327447')
# cProfile.run("Gw_PO.login('http://192.168.0.203:30080/#/login', '11011', 'HHkk2327447')")
# sys.exit(0)

# 获取基本公卫二级菜单连接
Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li[2]", 2)  # 点击一级菜单基本公卫
d_menu_jbgw = Gw_PO.getMenu2Url()
print('基本公卫 =>', d_menu_jbgw)
Gw_PO.logger.info(d_menu_jbgw)
# 基本公卫 => {'健康档案概况': 'http://192.168.0.203:30080/phs/HealthRecord/ehrindex', '个人健康档案': 'http://192.168.0.203:30080/phs/HealthRecord/Personal', '家庭健康档案': 'http://192.168.0.203:30080/phs/HealthRecord/Family', '迁入申请': 'http://192.168.0.203:30080/phs/HealthRecord/Immigration', '迁出审核': 'http://192.168.0.203:30080/phs/HealthRecord/Exit', '档案交接': 'http://192.168.0.203:30080/phs/HealthRecord/handoverFile', '死亡管理': 'http://192.168.0.203:30080/phs/HealthRecord/DeathManagement', '区域档案查询': 'http://192.168.0.203:30080/phs/HealthRecord/regionalFile', '接诊信息查询': 'http://192.168.0.203:30080/phs/HealthRecord/Diagnosis', '就诊管理': 'http://192.168.0.203:30080/phs/HealthRecord/Visit', '高血压专项': 'http://192.168.0.203:30080/phs/Hypertension/gxyregister', '高血压随访': 'http://192.168.0.203:30080/phs/Hypertension/gxyjob', '高血压报病': 'http://192.168.0.203:30080/phs/Hypertension/gxybb', '糖尿病专项': 'http://192.168.0.203:30080/phs/Diabetes/tnbregister', '糖尿病随访': 'http://192.168.0.203:30080/phs/Diabetes/tnbjob', '糖尿病报病': 'http://192.168.0.203:30080/phs/Diabetes/tnbbb', '慢阻肺病登记': 'http://192.168.0.203:30080/phs/Copd/register', '慢阻肺病专项': 'http://192.168.0.203:30080/phs/Copd/project', '慢阻肺病随访': 'http://192.168.0.203:30080/phs/Copd/visit', '儿童概况': 'http://192.168.0.203:30080/phs/Child/etindex', '儿童健康档案': 'http://192.168.0.203:30080/phs/Child/etfiles', '中医体质辨识列表': 'http://192.168.0.203:30080/phs/Child/tcm', '中医体质辨识汇总': 'http://192.168.0.203:30080/phs/Child/tzbs', '儿童检查记录': 'http://192.168.0.203:30080/phs/Child/etjob', '孕产妇概况': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfindex', '孕产妇登记': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfregister', '孕产妇档案': 'http://192.168.0.203:30080/phs/MaternalRecord/ycffiles', '孕产妇随访': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfjob', '老年人概况': 'http://192.168.0.203:30080/phs/Snr/lnrindex', '老年人专项登记': 'http://192.168.0.203:30080/phs/Snr/special', '老年人专项管理': 'http://192.168.0.203:30080/phs/Snr/lnrfiles', '本年度未体检': 'http://192.168.0.203:30080/phs/Snr/unexamined', '老年人中医体质辨识': 'http://192.168.0.203:30080/phs/Snr/chMedicine', '老年人自理能力评估查询': 'http://192.168.0.203:30080/phs/Snr/selfCareAssess', '老年人抑郁评估查询': 'http://192.168.0.203:30080/phs/Snr/depressed', '简易智力检查查询': 'http://192.168.0.203:30080/phs/Snr/intelligence', '体检登记': 'http://192.168.0.203:30080/phs/HealthExamination/tjregister', '体检记录': 'http://192.168.0.203:30080/phs/HealthExamination/tjrecord', '未体检人员': 'http://192.168.0.203:30080/phs/HealthExamination/tjunexam', '肺结核患者概况': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhindex', '肺结核登记': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhregister', '肺结核管理': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhfiles', '残疾人概况': 'http://192.168.0.203:30080/phs/Disabled/cjrindex', '残疾人登记': 'http://192.168.0.203:30080/phs/Disabled/cjrregister', '残疾人管理': 'http://192.168.0.203:30080/phs/Disabled/cjrfiles', '严重精神障碍登记': 'http://192.168.0.203:30080/phs/MentalDisorder/jsregister', '严重精神障碍患者': 'http://192.168.0.203:30080/phs/MentalDisorder/jsfiles', '严重精神病障碍随访': 'http://192.168.0.203:30080/phs/MentalDisorder/jsjob', '严重精神障碍概况': 'http://192.168.0.203:30080/phs/MentalDisorder/jsindex', '健康教育活动': 'http://192.168.0.203:30080/phs/HealthEducation/HealthActivity', '本年度未评': 'http://192.168.0.203:30080/phs/hbp/noassessdata', '评分信息查询': 'http://192.168.0.203:30080/phs/hbp/assessdata'}


# todo 1 基本公卫

# # todo 13.1, 健康行为积分 - 本年度未评
# Web_PO.opnLabel(d_menu_jbgw['本年度未评'])
# Web_PO.swhLabel(1)
# ele2 = Web_PO.getSuperEleByX("//tbody", ".")

# 1 查询
s_qty = Gw_PO.noScored_query({"身份证号":"110101199001012256", "人群分类": ["残疾人", "儿童"]})
# s_qty = Gw_PO.noScored_query({"管理机构":["玲珑卫生院", "玲珑镇大蒋家村卫生室"], "档案状态": "在档", "姓名": "刘长春", "身份证号":"110101199001012256",
#                      "现住址":["泉山街道", "花园社区居民委员会","123"], "人群分类": ["残疾人", "儿童"]})

# 2 新增
# 判断查询数量，并点击新增
# if s_qty == 1: Web_PO.eleClkByX(ele2, ".//button", 2)
# (use to testing)
# Web_PO.opnLabel("http://192.168.0.203:30080/phs/hbp/components/add?id&ehrId=375&singInfoId&type=edit&routeType=1")
# Web_PO.swhLabel(2)
# 新增详情页
# Gw_PO.noScored_new({'评分日期': [2025, 1, 3], '是否兑换': "是"})
# Gw_PO.noScored_new({"积分": [[['所有人', '1', '健康素养'], [2025,1,2], 10], [["所有人", '5', "查询档案"], [2025,2,2],2], [["高血压、糖尿病病友", '13', "按时用药"],[2025,4,1],1]],
#                      '评分日期': [2025, 1, 3], '是否兑换': "是"})

# 3 批量评分
# 点击批量评分，先选择记录，点击批量评分
# Gw_PO.noScored_batch({'身份证号': ['340203202407017263']})
# Gw_PO.noScored_batch({'身份证号': ['110101194301191302', '340203202407018290']}
# Gw_PO.noScored_batch({'身份证号': "all"})

# 翻页用于批量评分
# Web_PO.setTextBackspaceEnterByX("/html/body/div[1]/div/div[3]/section/div/main/div[3]/div/span[3]/div/input", 2)  # 切换到第2页
# Web_PO.setTextBackspaceEnterByX("/html/body/div[1]/div/div[3]/section/div/main/div[3]/div/span[3]/div/input", 12) # 切换到第12页
# Web_PO.setTextBackspaceEnterByX("/html/body/div[1]/div/div[3]/section/div/main/div[3]/div/span[3]/div/input", 13) # 切换到第13页
# Web_PO.setTextBackspaceEnterByX("/html/body/div[1]/div/div[3]/section/div/main/div[3]/div/span[3]/div/input", 4) # 切换到第4页




# # todo 13.2, 健康行为积分 - 评分信息查询
# Web_PO.opnLabel(d_menu_jbgw['评分信息查询'])
# Web_PO.swhLabel(1)
# ele2 = Web_PO.getSuperEleByX("//tbody", ".")
#
# # 1 查询
# s_qty = Gw_PO.scoreInformation_query({"身份证号": "340203202407017263"})
# s_qty = Gw_PO.scoreInformation_query({"管理机构":["玲珑卫生院", "玲珑镇大蒋家村卫生室"], "档案状态": "在档", "姓名": "刘长春", "身份证号":"110101199001012256",
#                                   "得分范围": [1,30], "评分日期":[[2025,1,2],[2025,1,3]], "现住址":["泉山街道", "花园社区居民委员会","123"], "是否兑换": "是",
#                                   "人群分类": ["残疾人", "儿童"]})

# # 2 修改
# if s_qty == 1: Web_PO.eleClkByX(ele2, ".//button[2]", 2)
# # 修改页(null)
# Gw_PO.scoreInformation_modify({"积分": [[['所有人', '1', '健康素养'], [2025,1,2], 10], [["所有人", '5', "查询档案"], [2025,2,2],2]],
#                      '评分日期': [2025, 1, 3], '是否兑换': "是"})

# 3 详情
# # 判断查询数量，并点击详情
# if s_qty == 1: Web_PO.eleClkByX(ele2, ".//button[1]", 2)
# # 详情页(null)
Gw_PO.scoreInformation_detail()