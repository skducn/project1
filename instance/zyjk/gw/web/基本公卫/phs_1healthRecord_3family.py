# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 健康档案管理 - 家庭健康档案
# 动态调用函数1
# s_func = 'phs_healthrecord_family_query'
# getattr(Gw_PO, s_func)({"身份证号": "41052220000511081"})
# 动态调用函数2(有风险)
# s_func = 'Gw_PO.phs_healthrecord_family_query({"身份证号": "41052220000511081"})'
# eval(s_func)
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
Web_PO.opnLabel(d_menu_basicPHS['家庭健康档案'])
Web_PO.swhLabel(1)


# todo 1 查询
# Gw_PO.phs_healthrecord_family_query({"身份证号": "372922198510281068"})
Gw_PO.phs_healthrecord_family_query({"姓名": "丽丽"})
# Gw_PO.phs_healthrecord_family_query({"管理机构": "招远市卫健局", "是否仅查询机构": "是", "姓名": "胡成", "身份证号": "230202194504020016",
#     "现住址": "上海东方路1000号", "家庭住址": ["海阳市", "东村街道", "和平村委会"]})


# todo 2 导出
# Gw_PO.export("/Users/linghuchong/Desktop/family.xlsx")


# todo 3 姓名 (更新)
# Gw_PO.phs_healthrecord_family_operation({'operate': '姓名', 'option': {"姓名": "李丽丽", "档案编号": "372922198510281068"}})
# Gw_PO.phs_healthrecord_family_operation({'operate': '更新', 'data': {
#     ' 姓名 ': "李四", ' 性别 ': "女", ' 出生日期 ': [2024, 2, 2], ' 民族 ': "回族",
#     ' 现住址 ': ["上海市", "市辖区", "虹口区", "广中路街道", "商业一村居委会", "多媒体100号"],
#     ' 本人电话 ': "13815161718", ' 联系人姓名 ': "令狐冲", ' 联系人电话 ': "58771234", ' 常住类型 ': '非户籍',
#     ' 文化程度 ': "专科教育", ' 职业 ': "军人", ' 工作单位 ': "上海智赢", ' 婚姻状况 ': "离婚", ' 血型 ': '不详',
#     ' RH血型 ': 'Rh阳性',
#     ' 医疗费用支付方式 ': [['全自费', {'其他': '123'}], {'城镇职工基本医疗保险': '555', '城镇居民基本医疗保险': '666', '贫困救助': "777"}],
#     ' 药物过敏史 ': ['青霉素类抗生素', '含碘药品', {'其他药物过敏源': "12345"}],
#     ' 暴露史 ': ['化学品', '不详'],
#     ' 既往史 ': {'疾病': {"有": [['高血压', [2025, 1, 1]], ['冠心病', [2025, 2, 1]]]},
#               '手术': {'有': [['手术1', [2025, 1, 3]], ['手术2', [2025, 1, 4]], ['手术3', [2025, 2, 4]]]},
#               '外伤': {"有": [['外伤1', [2025, 4, 11]], ['外伤2', [2025, 5, 5]]]},
#               '输血': {"有": [['输血1', [2025, 3, 3]], ['输血2', [2025, 4, 4]]]}},
#     ' 家族史 ': {'有': [['高血压', '母亲'], ['高血压', '母亲'], ['脑卒中', '子女']]},
#     ' 遗传病史 ': {'有': {"疾病名称": '帕金森'}},
#     ' 残疾情况 ': [['听力残疾', '精神残疾', {'其他残疾': "90"}], {' 残疾证号 ': 'ab123'}],
#     ' 家庭情况 ': {' 与户主关系 ': '子', ' 户主姓名 ': "李四2", ' 户主身份证号 ': "310101198004110013", ' 家庭人口数 ': "4", ' 家庭结构 ': "3", ' 居住情况 ': '独居'},
#     ' 厨房排风设施 ': '烟囱', ' 燃料类型 ': '煤', ' 饮水 ': '自来水', ' 厕所 ': '马桶', ' 禽畜栏 ': '无',
#     ' 管理机构 ': '招远市卫健局', ' 档案是否开放 ': "否", ' 建档日期 ': [2025, 1, 16],
#     ' 更新方式 ': '门诊',' 更新内容 ': "测试三峡",
#     }})

# todo 3 姓名（获取）== 查看
# Gw_PO.phs_healthrecord_family_operation({'operate': '姓名', 'option': {"姓名": "王丽丽"}})
# Gw_PO.phs_healthrecord_family_operation({'operate': '姓名', 'option': {"身份证号": "370624195305061323"}})
# d_ = Gw_PO.phs_healthrecord_family_operation({'operate': '获取', 'data': {}})
# print(d_)  # {'身份证号码': ['372922198510281068'], '档案编号': ['37068500100100157'], ...


# todo 维护家庭成员
# Gw_PO.phs_healthrecord_family_maintenance({'option': {"姓名": "李丽丽"}, 'data': {"户主姓名": "zhangsan", "户主身份证号": "3101011980012343", "与户主关系": "户主"}})






