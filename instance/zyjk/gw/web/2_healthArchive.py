# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-12-19
# Description: 公卫 - 基本公卫 - 健康档案管理
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

# todo 1.1, 健康档案管理 - 个人健康档案
Web_PO.opnLabel(d_menu_basicPHS['个人健康档案'])
Web_PO.swhLabel(1)
# 列表页数据，匹配登录账号所在机构
# 如：10082账号所属机构（大秦家镇小杨家村卫生室，370685008001）
# select * from PHUSERS.dbo.t_ehr_info where MANAGE_ORG_CODE = (select org_sub_code from ZYCONFIG.dbo.sys_user where USER_NAME ='10082')

# 1 查询
# Gw_PO.personalHealthRecord_query({"身份证号": "110101199001015000"})
# Gw_PO.personalHealthRecord_query({"姓名": "胡成", "性别": "男", "身份证号": "230202194504020016", "出生日期范围": [[2025, 1, 1], [2025, 1, 2]],"人群分类": ["残疾人","孕产妇"], "档案是否开放": "否",
#                             "档案状态": "已死亡", "血型": "不详", "年龄": [1, 5], "常住类型": "户籍", "是否签约": "是", "是否残疾": "否",
#                             "今年是否体检": "否", "既往史": ["脑卒中","高血压"], "今年体检日期": [[2025, 2, 1], [2025, 2, 2]], "今年是否已更新": "是",
#                             "今年更新日期": [[2025, 1, 3], [2025, 1, 5]], "医疗费用支付方式": "全公费", "建档日期": [[2025, 1, 1], [2025, 1, 8]], "档案缺失项目": "性别", "建档人": "ceshi",
#                             "管理机构": ["招远市卫健局"], "现住址": ["泉山街道", "花园社区居民委员会", "123"], "本人电话": "1382121212"})

# 2 查看
# Gw_PO.personalHealthRecord_query({"身份证号": "110101199001015000"}) # 查询
# Gw_PO.personalHealthRecord_operation('查看')
# d_info = Gw_PO.personalHealthRecord_detail()
# print(d_info)

# 3 姓名
# Gw_PO.personalHealthRecord_query({"身份证号": "110101199001015000"}) # 查询
# Gw_PO.personalHealthRecord_operation('姓名')
# d_info = Gw_PO.personalHealthRecord_info()
# print(d_info)


# 3 更新
# Gw_PO.personalHealthRecord_query({"身份证号": "110101199001015000"})  # 查询
# Gw_PO.personalHealthRecord_operation('更新')
# Gw_PO.personalHealthRecord_modify(File_PO.jsonfile2dict(folder + "/01.json"))
# Gw_PO.personalHealthRecord_modify({' 与户主关系 ': '子', ' 性别 ': "女", ' 民族 ': "回族", ' 文化程度 ': "专科教育", ' 职业 ': "军人", ' 婚姻状况 ': "离婚", ' 档案是否开放 ': "否",
#                                    ' 户主姓名 ': "李四2", ' 户主身份证号 ': "310101198004110013", ' 家庭人口数 ': "4", ' 家庭结构 ': "3", ' 居住情况 ': '独居',
#                                    ' 姓名 ': "李四", ' 本人电话 ': "13815161718", ' 联系人姓名 ': "令狐冲", ' 联系人电话 ': "58771234", ' 工作单位 ': "上海智赢", ' 残疾证号 ': 'ab123', ' 更新内容 ': "测试三峡",
#                                    ' 出生日期 ': [1946, 2, 2], ' 建档日期 ': [2025, 1, 16],
#                                    ' 常住类型 ': '非户籍', ' 血型 ': '不详', ' RH血型 ': 'Rh阳性', ' 更新方式 ': '门诊',
#                                    ' 厨房排风设施 ': '烟囱', ' 燃料类型 ': '煤', ' 饮水 ': '自来水', ' 厕所 ': '马桶', ' 禽畜栏 ': '无',
#                                    ' 管理机构 ': ["金岭镇卫生院", "金岭镇山上候家村卫生室"],
#                                    ' 现住址 ': ["上海市", "市辖区", "虹口区", "广中路街道", "商业一村居委会", "多媒体100号"],
#                                    ' 药物过敏史 ': ['青霉素类抗生素', '含碘药品', ['其他药物过敏源', "12345"]],
#                                    ' 暴露史 ': ['化学品', '不详'],
#                                    ' 医疗费用支付方式 ':[['城镇职工基本医疗保险','555'], ['城镇居民基本医疗保险', '666'], ['贫困救助',"777"],'全自费', ['其他','123']],
#                                    ' 残疾情况 ': ['听力残疾', '精神残疾', ['其他残疾', "90"]],
#                                    ' 遗传病史 ': ['有', '帕金森'],
#                                    ' 家族史 ': ['有', ['高血压', '母亲']],
#                                    ' 既往史 ': {'疾病': [['高血压',[2025, 1, 1]]],
#                                              '手术': [['手术1',[2025, 1, 3]], ['手术2', [2025, 1, 4]]],
#                                              '外伤': 'clear',
#                                              '输血': 'remain'}})

# ' 既往史 ': {'疾病': '无'}
# ' 既往史 ': {'疾病': [['高血压',[2025,2,12]],['糖尿病',[2025,3,14]]]}
# ' 既往史 ': {'疾病': [['高血压',[2025, 1, 1]], ['糖尿病', [2025, 1, 2]]],
#                                              '手术': [['手术1',[2025, 1, 3]], ['手术2', [2025, 1, 4]]],
#                                              '外伤': [['外伤1',[2025, 1, 5]], ['外伤2', [2025, 1, 6]]],
#                                              '输血': [['输血1',[2025, 1, 7]]]}
# ' 既往史 ': {'疾病': 'remain',
#                                              '手术': [['手术1',[2025, 1, 3]], ['手术2', [2025, 1, 4]], ['手术3', [2025, 1, 5]]],
#                                              '外伤': [['外伤1',[2025, 1, 5]], ['外伤2', [2025, 1, 6]]],
#                                              '输血': [['输血1',[2025, 1, 7]]]}
# ' 遗传病史 ': '无'
# ' 遗传病史 ':['有', '帕金森']
# ' 家族史 ': '无'
# ' 家族史 ': ['有', ['高血压', '母亲', '糖尿病', '父亲']]

# ' 管理机构 ': ["招远市卫健局"]
# ' 管理机构 ': ["金岭镇卫生院"]
# ' 管理机构 ': ["金岭镇卫生院", "金岭镇山上候家村卫生室"]


# 4 终结
Gw_PO.personalHealthRecord_query({"身份证号": "110101199001015000"})  # 查询
Gw_PO.personalHealthRecord_operation(['终结', {'暂不管理': {'暂不管理原因': '住院', '暂不管理日期': [2025, 1, 2]}}])
# Gw_PO.personalHealthRecord_operation(['终结', {'已死亡': {'档案注销日期': [2025, 1, 3], '死亡日期': [2025, 1, 3]}}])

# 5 更新历史
# Gw_PO.personalHealthRecord_operation('更新历史')


