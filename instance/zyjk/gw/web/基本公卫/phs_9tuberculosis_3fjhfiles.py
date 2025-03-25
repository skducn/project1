# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-3-12
# Description: 基本公卫 - 肺结核患者管理 - 肺结核管理
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
Web_PO.opnLabel(d_menu_basicPHS['肺结核管理'])
Web_PO.swhLabel(1)


# todo 1 查询
Gw_PO.phs_tuberculosis_fjhfiles_query({"姓名": "测试11"})
# Gw_PO.phs_tuberculosis_fjhfiles_query({"姓名": "胡成", "身份证号": "110101195901015999", '上次随访日期':[[2025,1,1],[2025,3,2]], "管理机构": "招远市卫健局",
#     '是否仅查询机构': '是', "档案状态": "在档", "登记时年龄": [2, 5],
#     '登记日期':[[2025,2,2],[2025,2,4]], "管理状态": "未结案", '患者类型':'初治', '痰菌情况':'未查痰',
#     '停止治疗原因': '丢失','随访提醒分类': '常规管理', '随访日期': [[2025,4,1],[2025,4,2]]})

# todo 2 导出
# Gw_PO.export("/Users/linghuchong/Desktop/phs_tuberculosis_fjhfiles.xls")

# 操作
Gw_PO.phs_tuberculosis_fjhfiles_operation({'operate': '访视记录', 'option': {"姓名": "测试11"}})


# todo 3.1 操作 - 访视记录 - 入户随访(编辑)
# Gw_PO.phs_tuberculosis_fjhfiles_operation({'operate': '入户随访之编辑', 'data': {
#     '随访日期': [2025,1,2], '随访方式':'家庭','患者类型':'复治','痰菌情况':'阴性','耐药情况':'未检测','症状及体征':['咳嗽咳痰',{'其他':'123'}],
#     '用药':{'化疗方案':'12','用法':'间歇','药品剂型':'注射剂'},'督导人员选择': {'其他': '555'},'家庭居住环境':{'单独的居室':'有', '通风情况':'差'},
#     '生活方式评估':{'吸烟':[1,3],'饮酒':[4,6]},
#     '健康教育及培训':{'取药地点、时间':['上海家里',[2025,3,4]],'服药记录卡的填写':'未掌握','服药方法及药品存放':'未掌握','肺结核治疗疗程':'未掌握','不规律服药危害':'未掌握',
#     '服药后不良反应及处理':'未掌握','治疗期间复诊查痰':'未掌握','外出期间如何坚持服药':'未掌握','生活习惯及注意事项':'未掌握','密切接触者检查':'未掌握'},
#     '下次随访日期':[2025,3,5],'随访医生':'金浩1','患者（家属）签字':'zhanzhang'
# }})


# todo 3.2 操作 - 访视记录 - 入户随访(删除)
# Gw_PO.phs_tuberculosis_fjhfiles_operation({'operate': '入户随访之删除', 'data': {}})


# todo 4.1 操作 - 访视记录 - 历次随访（新增随访）- 停止治疗
# Gw_PO.phs_tuberculosis_fjhfiles_operation({'operate': '历次随访之新增随访', 'data': {
#     '随访日期': [2025,1,8], '治疗月序':'5',
#     '督导人员选择': '其他' ,'随访方式':'家庭',
#     '症状及体征':['咳嗽咳痰',{'其他':'123'}],
#     '生活方式评估':{'吸烟':[1,3],'饮酒':[4,6]},
#     '用药':{'化疗方案':'12','用法':'间歇','药品剂型':'注射剂', '漏服药次数':'12'},
#     '药物不良反应': {'有':'123'}, '并发症或合并症':{'有':'12333'},
#     '转诊': {'转诊':'有', '机构及科别': '阿里机构', '原因':'343', '2周内随访,随访结果':'ggg'},
#     '处理意见':'退热贴',
#     '是否停止治疗': '否',
#     '停止治疗及原因':{'出现停止治疗时间':[2025,1,2], '停止治疗原因':'完成疗程'},
#     '全程管理情况':{'应访视患者':'3','实际访视':'4','患者在疗程,应服药':'5','实际服药':'66','评估医生签名':'金浩1'},
#     '下次随访时间':[2025,3,5],'随访医生签名':'1','患者（家属）签字':'zhanzhang'
# }})

# todo 4.2 操作 - 访视记录 - 历次随访（结案）
Gw_PO.phs_tuberculosis_fjhfiles_operation({'operate': '历次随访之结案', 'data': {
    '结案原因：': {'其他': '123'}
}})
