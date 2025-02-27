# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-21
# Description: 基本公卫 - 孕产妇管理 - 孕产妇登记
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
Web_PO.opnLabel(d_menu_basicPHS['孕产妇登记'])
Web_PO.swhLabel(1)



# todo 1 查询
# Gw_PO.phs_maternalRecord_ycfregister_query({"身份证号": "110101194301191302"})
Gw_PO.phs_maternalRecord_ycfregister_query({"管理机构": {"蚕庄卫生院": "蚕庄镇柳杭村卫生室"}, "档案状态": "在档", "姓名": "胡成", '年龄': [12, 14], "身份证号": "110101194301191302",'联系电话': '13817161514'})
# "管理机构": "招远市卫健局"
# "管理机构": "蚕庄卫生院"
# "管理机构": {"蚕庄卫生院": "蚕庄镇柳杭村卫生室"}

# todo 2 专项登记
# Gw_PO.phs_maternalRecord_ycfregister_operation({'operate': '新增登记及第一次产前随访', 'option': {"身份证号": "110101194301191302"}})
# 新增登记及第一次产前随访
# Gw_PO.phs_maternalRecord_ycfregister_operation({'operate': '新增登记及第一次产前随访', 'data': {
#     '填表日期': [2024, 1, 1], '是否高危产妇': '是', '丈夫姓名': '阿依达', '丈夫年龄': '43', '丈夫电话': '13611223344',
#     '孕次': '1', '产次': ['2', '3'], '末次月经': [2024, 2, 2], '孕周': ['4', '5'], '预产期': [2024, 3, 3],
#     '既往史': ['心脏病', {'其他': '1231'}],
#     '家族史': ['精神病史', {'其他': '456'}], '妇科手术史': {'有': '234234'},
#     '个人史': ['吸烟', {'其他': '4yyy'}], '孕产史': ['1','2','3','4','5','6'],
#     '身高(cm)': '166', '体重(kg)': '66', '体质指数(kg/m²)': '123', '血压(mmHg)': ['100', '98'],
#     '心脏': {'异常': '1'}, '肺部': {'异常': '2'}, '外阴': {'异常': '3'}, '阴道': {'异常': '4'}, '宫颈': {'异常': '5'}, '子宫': {'异常': '6'}, '附件': {'异常': '7'},
#     '血常规': {'血红蛋白值': '23', '白细胞计数值': '44', '血小板计数值': '235', '其他': '更好'},
#     '尿常规': {'尿蛋白': '+', '尿糖': '++', '尿酮体': '+++', '尿潜血': '++++', '其他': '5677'},
#     '血型': '不详', 'RH血型': 'Rh阳性', ' 血糖': '67',
#     '肝功能': {'血清谷丙转氨酶': '3434', '血清谷草转氨酶': '56', '白蛋白':'434', '总胆红素':'234', '结合胆红素':'66'},
#     '肾功能': {'血清肌酐': '77', '血尿素': '88'},
#     ' 阴道分泌物': ['滴虫', {'其他': '45'}], '阴道清洁度': 'III度',
#     '乙型肝炎五项': {'乙型肝炎表面抗原': '阳性', ' 乙型肝炎表面抗体': '不详', ' 乙型肝炎e抗原': '不详', ' 乙型肝炎e抗体': '不详', ' 乙型肝炎核心抗体': '不详'},
#     ' 梅毒血清学试验': '阳性', ' HIV抗体检测': '阳性',
#     'B超': 'ert', ' 其他': 'rtyrtyrtyrty',
#     '总体评估': {'异常': '234234'}, '保健指导': ['心理', '产前筛选宣传告知', {'其他':'23423'}], '建册情况': {'已在其他机构建册': '5t5t'},
#     '建册日期': [2025, 2, 6], '建册单位': '自己家',
#     '转诊': {'有': {'原因': '44', '机构及科室': '内科', '联系人': '张明全', '联系方式': '58776565', '结果': '到位'}},
#     '下次访视时间': [2025, 3, 5], '随访医生签名': '金浩1', '居民签名': 'peter'
# }})


# todo 3 更新居民健康档案

