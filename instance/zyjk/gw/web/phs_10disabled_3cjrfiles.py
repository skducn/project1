# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-3-13
# Description: 基本公卫 - 残疾人健康管理 - 残疾人管理
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName)
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')
# 登录
Gw_PO.login(Configparser_PO.HTTP("url"), Configparser_PO.ACCOUNT("user"), Configparser_PO.ACCOUNT("password"))
# 菜单
d_menu_basicPHS = {'健康档案概况': ' http://192.168.0.203:30080/phs/HealthRecord/ehrindex', '个人健康档案': 'http://192.168.0.203:30080/phs/HealthRecord/Personal', '家庭健康档案': 'http://192.168.0.203:30080/phs/HealthRecord/Family', '迁入申请': 'http://192.168.0.203:30080/phs/HealthRecord/Immigration', '迁出审核': 'http://192.168.0.203:30080/phs/HealthRecord/Exit', '档案交接': 'http://192.168.0.203:30080/phs/HealthRecord/handoverFile', '死亡管理': 'http://192.168.0.203:30080/phs/HealthRecord/DeathManagement', '区域档案查询': 'http://192.168.0.203:30080/phs/HealthRecord/regionalFile', '接诊信息查询': 'http://192.168.0.203:30080/phs/HealthRecord/Diagnosis', '就诊管理': 'http://192.168.0.203:30080/phs/HealthRecord/Visit', '高血压专项': 'http://192.168.0.203:30080/phs/Hypertension/gxyregister', '高血压随访': 'http://192.168.0.203:30080/phs/Hypertension/gxyjob', '高血压报病': 'http://192.168.0.203:30080/phs/Hypertension/gxybb', '糖尿病专项': 'http://192.168.0.203:30080/phs/Diabetes/tnbregister', '糖尿病随访': 'http://192.168.0.203:30080/phs/Diabetes/tnbjob', '糖尿病报病': 'http://192.168.0.203:30080/phs/Diabetes/tnbbb', '慢阻肺病登记': 'http://192.168.0.203:30080/phs/Copd/register', '慢阻肺病专项': 'http://192.168.0.203:30080/phs/Copd/project', '慢阻肺病随访': 'http://192.168.0.203:30080/phs/Copd/visit', '儿童概况': 'http://192.168.0.203:30080/phs/Child/etindex', '儿童健康档案': 'http://192.168.0.203:30080/phs/Child/etfiles', '中医体质辨识列表': 'http://192.168.0.203:30080/phs/Child/tcm', '中医体质辨识汇总': 'http://192.168.0.203:30080/phs/Child/tzbs', '儿童检查记录': 'http://192.168.0.203:30080/phs/Child/etjob', '孕产妇概况': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfindex', '孕产妇登记': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfregister', '孕产妇档案': 'http://192.168.0.203:30080/phs/MaternalRecord/ycffiles', '孕产妇随访': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfjob', '老年人概况': 'http://192.168.0.203:30080/phs/Snr/lnrindex', '老年人专项登记': 'http://192.168.0.203:30080/phs/Snr/special', '老年人专项管理': 'http://192.168.0.203:30080/phs/Snr/lnrfiles', '本年度未体检': 'http://192.168.0.203:30080/phs/Snr/unexamined', '老年人中医体质辨识': 'http://192.168.0.203:30080/phs/Snr/chMedicine', '老年人自理能力评估查询': 'http://192.168.0.203:30080/phs/Snr/selfCareAssess', '老年人抑郁评估查询': 'http://192.168.0.203:30080/phs/Snr/depressed', '简易智力检查查询': 'http://192.168.0.203:30080/phs/Snr/intelligence', '体检登记': 'http://192.168.0.203:30080/phs/HealthExamination/tjregister', '体检记录': 'http://192.168.0.203:30080/phs/HealthExamination/tjrecord', '未体检人员': 'http://192.168.0.203:30080/phs/HealthExamination/tjunexam', '肺结核患者概况': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhindex', '肺结核登记': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhregister', '肺结核管理': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhfiles', '残疾人概况': 'http://192.168.0.203:30080/phs/Disabled/cjrindex', '残疾人登记': 'http://192.168.0.203:30080/phs/Disabled/cjrregister', '残疾人管理': 'http://192.168.0.203:30080/phs/Disabled/cjrfiles', '严重精神障碍登记': 'http://192.168.0.203:30080/phs/MentalDisorder/jsregister', '严重精神障碍患者': 'http://192.168.0.203:30080/phs/MentalDisorder/jsfiles', '严重精神病障碍随访': 'http://192.168.0.203:30080/phs/MentalDisorder/jsjob', '严重精神障碍概况': 'http://192.168.0.203:30080/phs/MentalDisorder/jsindex', '健康教育活动': 'http://192.168.0.203:30080/phs/HealthEducation/HealthActivity', '本年度未评': 'http://192.168.0.203:30080/phs/hbp/noassessdata', '评分信息查询': 'http://192.168.0.203:30080/phs/hbp/assessdata'}
Web_PO.opnLabel(d_menu_basicPHS['残疾人管理'])
Web_PO.swhLabel(1)


# todo 1 查询
Gw_PO.phs_disabled_cjrfiles_query({"姓名": "1"})
# Gw_PO.phs_disabled_cjrfiles_query({"管理机构": "招远市卫健局", '是否仅查询机构': '是', "档案状态": "在档", "姓名": "胡成",
#     "身份证号": "110101195901015999", "登记机构": "玲珑卫生院", "管理状态": "未结案", '残疾人证号': 'A123', '管理等级':'三级',
#     '主要残疾类型':'听力残疾','随访提醒分类':'常规管理','登记日期': [[2025,1,1],[2025,3,2]],
#     "登记时年龄": [2, 5],'上次随访日期':[[2025,4,1],[2025,5,2]],
#     '现住址':['泉山街道', '花园社区居民委员会','123']})


# todo 2 导出
# Gw_PO.export("/Users/linghuchong/Desktop/3cjrfiles.xls")


# 操作
Gw_PO.phs_disabled_cjrfiles_operation({'operate': '访视记录', 'option': {"身份证号": "110101195907066009"}})

# todo 3.1 操作 - 访视记录 - 专项登记(编辑)
# Gw_PO.phs_disabled_cjrfiles_operation({'operate': '专项登记之编辑', 'data': {
#     '残疾人证号 ': 'A123', '致残时间 ': [2025,1,4], '自理程度 ': '部分自理', ' 生活来源 ': '家庭供养', ' 监护人 ': '没有', ' 与残疾人关系 ': '女儿',
#     ' 当前状态 ': '其他',' 管理等级 ': '三级',' 功能障碍 ': '324324',
#     ' 致残原因 ': ['遗传', '其他'],' 主要残疾类型 ': ['无残疾'], ' 多重残疾类型 ': ['视力残疾','其他残疾'], ' 残疾程度 ': '二级',
#     ' 赡养老人数 ':'1', ' 抚养子女数 ': '2',' 特长 ': '碎觉', ' 主要情况 ': 'dssdf', '培训经历 ':'热热热', '备注 ':'大是大非水电费',
#     ' 登记人':'金浩1',' 登记时间':[2025,3,5],' 居民（家属）签字':'zhanzhang'
# }})



# todo 3.2.1 操作 - 访视记录 - 随访记录（新增）
# Gw_PO.phs_disabled_cjrfiles_operation({'operate': '随访记录之新增', 'data': {
#     ' 主要残疾 ': ['视力残疾', '其他残疾'], ' 多重残疾 ': ['无残疾'], ' 残疾程度 ': '三级',' 随访日期 ': [2025,2,3],' 随访方式 ':'家庭',
#     ' 体征 ': {' 体征 ':[12, 34],'体重':'66','心率':'67','其他':'555'},
#     ' 就业情况 ': {' 康复训练情况 ': '444', ' 功能训练 ': [6,7,8,9],' 训练场地 ': '家庭',' 训练效果 ': '无效', ' 康复目标 ': {'其他':'3333'}, ' 遵医行为 ': '一般'},
#     ' 转诊 ': {' 转诊原因 ':'有12', ' 转诊机构及科室 ': '阿里机构'},
#     ' 此次随访分类 ': '并发症',
#     ' 下次随访时间 ':[2025,3,5], ' 随访医生签名 ':'1', ' 患者(家属)签名 ': 'zhanzhang'
# }})

# todo 3.2.2 操作 - 访视记录 - 随访记录（引入上一次数据）
# Gw_PO.phs_disabled_cjrfiles_operation({'operate': '随访记录之引入上一次数据'})

# todo 3.2.3 操作 - 访视记录 - 随访记录（结案）
# Gw_PO.phs_disabled_cjrfiles_operation({'operate': '随访记录之结案', 'data': {
#     '结案原因：': {'其他': '123'}
# }})



# todo 3.3.1 操作 - 访视记录 - 康复需求登记（新增）
# Gw_PO.phs_disabled_cjrfiles_operation({'operate': '康复需求登记之新增', 'data': {
#     ' 康复医疗服务 ': ['住院', '医疗'],
#     ' 听力语言 ': '是', ' 听力服务项目 ': ['双语训练', '其他'],' 听力语言器具名称 ': ['助听器', '会话交流用具'],
#     ' 视力 ': '是', ' 视力服务项目 ': ['日常生活技能训练', '其他'], ' 视力辅助器具 ': ['助视器', '盲人报时用具'],
#     ' 肢体 ': '是', ' 肢体服务项目 ': ['运行功能训练', '其他'], ' 肢体器具名称 ': ['生活自助器具', '其他器具'],
#     ' 智力 ': '是', ' 智力器具名称 ': ['识图片', '启智用具'], ' 智力服务项目 ': ['认知能力训练', '其他'],
#     ' 是否精神功能训练 ': '是',' 精神服务项目 ': ['社会适应训练', '其他'],
#     ' 精神器具名称 ': ['文体用品'],
#     ' 知识普及 ': ['家长学校', '其他'],
#     ' 心理服务 ': ['心理咨询', '其他'],
#     ' 转介服务 ': ['生活保障', '其他'],
#     ' 其他需求 ': '123',
#     ' 登记人 ': '1', ' 登记时间 ':[2025,3,5], ' 居民签名 ': 'zhanzhang', ' 家属签名 ':'hello'
# }})

# todo 3.3.2 操作 - 访视记录 - 康复需求登记（引入上一次数据）
# Gw_PO.phs_disabled_cjrfiles_operation({'operate': '康复需求登记之引入上一次数据'})

# # todo 3.3.3 操作 - 访视记录 - 康复需求登记（结案）
# Gw_PO.phs_disabled_cjrfiles_operation({'operate': '康复需求登记之结案', 'data': {
#     '结案原因：': {'其他': '123'}
# }})



# todo 3.4.1 操作 - 访视记录 - 健教记录（新增）
# Gw_PO.phs_disabled_cjrfiles_operation({'operate': '健教记录之新增', 'data': {
#     ' 教育内容 ': '123',
#     ' 健教医生 ': '222', ' 健教日期 ': [2025,3,1],
#     ' 登记人 ': '1', ' 登记日期 ':[2025,3,5], ' 居民签名 ': 'zhanzhang', ' 家属签名 ':'hello'
# }})

# todo 3.4.2 操作 - 访视记录 - 健教记录（引入上一次数据）
# Gw_PO.phs_disabled_cjrfiles_operation({'operate': '健教记录之引入上一次数据'})

# # todo 3.4.3 操作 - 访视记录 - 健教记录（结案）
# Gw_PO.phs_disabled_cjrfiles_operation({'operate': '健教记录之结案', 'data': {
#     '结案原因：': {'其他': '123'}
# }})



# # todo 3.5.1 操作 - 访视记录 - 服务登记（新增）
# Gw_PO.phs_disabled_cjrfiles_operation({'operate': '服务登记之新增', 'data': {
#     ' 康复医疗服务信息 ': ['住院', '医疗'],
#     ' 是否视力功能训练 ': '是', ' 视力功能训练 ': ['日常生活技能训练', '其他'], ' 视力辅助器具 ': ['助视器', '盲杖'],
#     ' 是否听力语言训练 ': '是', ' 听力功能项目 ': ['双语悬链', '其他'], ' 听力辅助器具 ': ['助听器', '人工耳蜗'],
#     ' 是否肢体功能训练 ': '是', ' 肢体功能训练 ': ['运行功能训练', '其他'], ' 肢体辅助器具 ': ['生活自助器具', '其他器具'],
#     ' 是否智力功能训练 ': '是', ' 智力辅助器具 ': ['识图片', '启智用具'], ' 智力功能训练 ': ['认知能力训练', '其他'],
#     ' 是否精神功能训练 ': '是', ' 精神器具名称 ': ['文体用品'], ' 精神功能训练 ': ['社会适应训练', '其他'],
#     ' 其他器具服务 ': ['购买', '信息'],
#     ' 心理服务 ': ['心理咨询', '其他'],
#     ' 知识普及 ': ['家长学校', '其他'],
#     ' 转介服务 ': ['生活保障', '其他'],
#     ' 其他服务 ': '123',
#     ' 服务方式 ': ['日间照料', '其他'],
#     ' 康复情况 ': '无效',
#     ' 下次服务计划 ': '12121212',
#     ' 下次服务方式 ': ['家庭康复', '其他'],
#     ' 服务备注 ': '332323',
#     ' 服务日期 ':[2025,3,5], ' 服务场所 ': '机构', ' 下次服务日期 ':[2025,3,6], ' 服务医生 ': '7',
#     ' 居民签名 ': 'zhanzhang', ' 家属签名 ':'hello'
# }})

# todo 3.5.2 操作 - 访视记录 - 服务登记（引入上一次数据）
# Gw_PO.phs_disabled_cjrfiles_operation({'operate': '服务登记之引入上一次数据'})

# # # todo 3.5.3 操作 - 访视记录 - 服务登记（结案）
# Gw_PO.phs_disabled_cjrfiles_operation({'operate': '服务登记之结案', 'data': {
#     '结案原因：': {'其他': '123'}
# }})



# todo 3.6.1 操作 - 访视记录 - 服务评估（新增）
# Gw_PO.phs_disabled_cjrfiles_operation({'operate': '服务评估之新增', 'data': {
#     ' 评估年度 ': '2024.3', ' 康复满意程度 ': '满意',
#     ' 残疾人或监护人 ': '阿里', ' 服务医生 ': '222',
#     ' 服务效果 ': '较差', ' 下次服务日期 ': [2025,3,1],
#     ' 下年度服务建议 ': '6456456',
#     ' 评估人 ': '222', ' 评估日期 ': [2025,3,3], ' 登记人 ': '1', ' 登记日期 ':[2025,3,5],
#     ' 居民签名 ': 'zhanzhang', ' 家属签名 ':'hello'
# }})

# todo 3.6.2 操作 - 访视记录 - 服务评估（引入上一次数据）
# Gw_PO.phs_disabled_cjrfiles_operation({'operate': '服务评估之引入上一次数据'})

# # todo 3.6.3 操作 - 访视记录 - 服务评估（结案）
# Gw_PO.phs_disabled_cjrfiles_operation({'operate': '服务评估之结案', 'data': {
#     '结案原因：': {'其他': '123'}
# }})
