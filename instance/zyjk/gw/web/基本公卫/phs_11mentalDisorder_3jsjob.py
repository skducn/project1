# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-3-19
# Description: 基本公卫 - 严重精神障碍健康管理 - 严重精神病障碍随访
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
Web_PO.opnLabel(d_menu_basicPHS['严重精神病障碍随访'])
Web_PO.swhLabel(1)


# todo 1 查询
Gw_PO.phs_memtalDisorder_jsjob_query({"身份证号": "370685201705080014"})
# Gw_PO.phs_memtalDisorder_jsjob_query({"管理机构": "招远市卫健局", '是否仅查询机构': '是', "姓名": "胡成",  "身份证号": "370685201705080014",
#     '随访日期': [[2025,3,1], [2025,3,2]]})


# todo 2 导出(.xls)
# Gw_PO.export("/Users/linghuchong/Desktop/phs_memtalDisorder_jsjob.xlsx")


# todo 3.1 操作 - 编辑
Gw_PO.phs_memtalDisorder_jsjob_operation({'operate': '编辑', 'option': {"身份证号": "370685201705080014"}})
Gw_PO.phs_memtalDisorder_jsjob_operation({'operate': '编辑', 'data': {
    ' 随访日期 ': [2025,3,19], ' 本次随访形式 ': '家庭',
    ' 若失访，原因 ': {'其他': '123'},
    ' 如死亡 ': {'死亡日期': [2025,3,5], '死亡原因': {'躯体疾病(':['肿瘤','脑血管病']}},
    ' 危险性评估 ': '4级',
    ' 目前症状 ': [{'其他':'444'}],
    ' 自知力 ': '自知力缺失',
    ' 睡眠情况 ': '一般', ' 饮食情况 ': '良好',
    ' 社会功能情况 ': {'个人生活料理':'部分自理','家务劳动':'较差','生产劳动及工作':'良好','学习能力':'一般','社会人际交往':'较差'},
    ' 危险行为 ': {'有':['1','2','3','4','5','6']},
    ' 两次随访期间 关锁情况 ': '关锁',
    ' 两次随访期间 住院情况 ': '目前正在住院', ' 末次出院日期 ':[2025,2,13],
    ' 实验室检查 ':{'有':'234234'},
    ' 用药情况 ':[],
    ' 用药依从性 ': '间断', ' 药物不良反应 ': {'有': '123213'},
    ' 治疗效果 ': '其他',
    ' 康复措施 ': ['生活劳动能力', {'其他':'werwer'}],
    ' 随访评价结果 ': '稳定',
    ' 通知联席部门 ': {'是': {'公安部门/社区综治 中心受理人姓名': ['章三', '里斯'], '电话':['58667655','13812122334']}},
    ' 转诊 ': {'是': {'转诊原因': '研究中', '转诊机构':'阿里机构', '转诊诊室': '内科'}},
    ' 调整用药情况 ': [{'药品名称': '三九感冒灵', '用法用量': ['每天一次', '22']}, {'药品名称': '活心丸', '用法用量': ['每天二次', '4']}, {'药品名称': '活血理伤丸', '用法用量': ['每天一次', '7']}],
    ' 下次随访日期 ': [2025,4,5], ' 随访医师': '金浩1', ' 随访医疗机构 ':'33',' 患者（家属）签名 ':'44'
}})

# todo 3.2 操作 - 删除
# Gw_PO.phs_memtalDisorder_jsjob_operation({'operate': '删除', 'option': {"身份证号": "370685201705080014"}})
