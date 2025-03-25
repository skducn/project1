# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-3-17
# Description: 基本公卫 - 严重精神障碍健康管理 - 严重精神障碍患者
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
Web_PO.opnLabel(d_menu_basicPHS['严重精神障碍患者'])
Web_PO.swhLabel(1)


# todo 1 查询
Gw_PO.phs_memtalDisorder_jsfiles_query({"身份证号": "370685198705183027"})
# Gw_PO.phs_memtalDisorder_jsfiles_query({"管理机构": "招远市卫健局", '是否仅查询机构': '是', "档案状态": "在档", "姓名": "胡成",  "身份证号": "110101195901015999",
#     '服药依从性':'间断', '管理状态':'管理中','随访提醒分类':'常规管理','重性精神疾病分类':'其他',
#     '上次随访时间': [[2025,1,1], [2025,2,2]], '登记时年龄': [2, 5],
#     '登记日期':[[2025,3,1], [2025,3,2]], '现住址': ['梦芝街道','玲珑社区居民委员会','123']})


# todo 2 导出(.xls)
# Gw_PO.export("/Users/linghuchong/Desktop/phs_memtalDisorder_jsfiles.xlsx")


# # # # todo 3 操作 - 访视记录（编辑患者登记）
Gw_PO.phs_memtalDisorder_jsfiles_operation({'operate': '访视记录', 'option': {"身份证号": "370685198705183027"}})
# Gw_PO.phs_memtalDisorder_jsfiles_operation({'operate': '访视记录之编辑患者登记', 'data': {
#     '监护人姓名 ': 'A123', ' 与患者关系 ': '本人',
#     '监护人地址 ': '上海浦东南路111号', ' 监护人电话 ': '13819181716',
#     '辖区村(居)委联系人 ': '女儿guo',' 联系人电话 ': '123813233445',
#     '户别 ': '农村', '就业情况 ': '农民',
#     '知情同意 ': '不同意参加管理', ' 签字 ': '无残疾', ' 签字日期':[2025,2,3],
#     ' 重性精神疾病分类 ': '其他', ' 初次发病时间 ': [2025,3,3],
#     ' 既往主要症状 ': ['猜疑', {'其他':'123'}], ' 既往关锁情况 ': '关锁',
#     ' 既往治疗情况 ': {'门诊': '未治', '住院':'5'},
#     ' 目前诊断情况 ': {'诊断':'3213', '确诊医院':'213', '确诊日期':[2025,2,13]},
#     ' 最近一次治疗效果 ': '其他', ' 危险行为 ':{'有':['1','2','3','4','5','6']}, ' 经济状况 ': '非贫困',
#     ' 专科医生的意见（如果有请记录）':'金浩1',' 建卡日期':[2025,3,5], ' 建卡医疗机构':'sfdsf'
# }})


# # # # todo 3 操作 - 访视记录（新增随访记录）
# Gw_PO.phs_memtalDisorder_jsfiles_operation({'operate': '访视记录之新增随访记录', 'data': {
#     ' 随访日期 ': [2025,3,19], ' 本次随访形式 ': '家庭',
#     ' 若失访，原因 ': {'其他': '123'},
#     ' 如死亡 ': {'死亡日期': [2025,3,5], '死亡原因': {'躯体疾病(':['肿瘤','脑血管病']}},
#     ' 危险性评估 ': '4级',
#     ' 目前症状 ': [{'其他':'444'}],
#     ' 自知力 ': '自知力缺失',
#     ' 睡眠情况 ': '一般', ' 饮食情况 ': '良好',
#     ' 社会功能情况 ': {'个人生活料理':'部分自理','家务劳动':'较差','生产劳动及工作':'良好','学习能力':'一般','社会人际交往':'较差'},
#     ' 危险行为 ': {'有':['1','2','3','4','5','6']},
#     ' 两次随访期间 关锁情况 ': '关锁',
#     ' 两次随访期间 住院情况 ': '目前正在住院', ' 末次出院日期 ':[2025,2,13],
#     ' 实验室检查 ':{'有':'234234'},
#     ' 用药情况 ':[{'药品名称': '女金丸', '用法用量':['每天三次','22']}, {'药品名称': '活心丸', '用法用量':['每天二次','44']}],
#     ' 用药依从性 ': '间断', ' 药物不良反应 ': {'有': '123213'},
#     ' 治疗效果 ': '其他',
#     ' 康复措施 ': ['生活劳动能力', {'其他':'werwer'}],
#     ' 随访评价结果 ': '稳定',
#     ' 通知联席部门 ': {'是': {'公安部门/社区综治 中心受理人姓名': ['章三', '里斯'], '电话':['58667655','13812122334']}},
#     ' 转诊 ': {'是': {'转诊原因': '研究中', '转诊机构':'阿里机构', '转诊诊室': '内科'}},
#     ' 调整用药情况 ': [{'药品名称': '三九感冒灵', '用法用量': ['每天一次', '22']}, {'药品名称': '活心丸', '用法用量': ['每天二次', '4']}, {'药品名称': '活血理伤丸', '用法用量': ['每天一次', '7']}],
#     ' 下次随访日期 ': [2025,4,5], ' 随访医师': '金浩1', ' 随访医疗机构 ':'33',' 患者（家属）签名 ':'44'
# }})

# todo 4.2 操作 - 访视记录 - 历次随访（结案）
Gw_PO.phs_memtalDisorder_jsfiles_operation({'operate': '访视记录之结案随访记录', 'data': {
    '结案原因：': {'其他': '123'}
}})