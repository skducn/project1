# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-12-19
# Description: 公卫 - 基本公卫 - 健康教育
# *****************************************************************

import cProfile


from GwPO import *
Gw_PO = GwPO("./2_healthEducation.log")

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

# # todo 13.1, 健康教育 - 健康教育活动
Web_PO.opnLabel(d_menu_jbgw['健康教育活动'])
Web_PO.swhLabel(1)
ele2 = Web_PO.getSuperEleByX("//tbody", ".")

# 1 查询
# s_qty = Gw_PO.healthEducationActivity_query({"活动日期":[[2025,1,2], [2025,2,4]], "活动地点": "上海", "活动形式": "开展咨询活动", "活动主题": "普法宣传", "主讲人": "阿依达"})

# 2 新增
Gw_PO.healthEducationActivity_new({
                                   # '活动时间': [2025, 1, 3], '活动地点': "上海",
                                   # '活动形式': "开展咨询活动",
                                   # '活动主题': "普法宣传", '活动人数': "12", '组织者': "白嫖",
                                   # '主讲人': "阿依达", '主讲人单位': "上海白月光公司", '职称': "专家",
                                   # '接受健康教育人员类别': "妇女",
                                   '健康教育资源发放种类': "音像资料",
                                   '健康教育资源发放数量': "12",
                                   # '活动内容': "宣传教育",
                                   # '活动总结评价': "良好",
                                   '存档资料类型': ['图片', '签到表'],
                                   # '存档资料类型': ['/Users/john/Downloads/1.jpg', '/Users/john/Downloads/2.jpg'],
                                   # '填表人': 'test1', '负责人':'jh', '填表时间':[2025,3,4]
                                   })


