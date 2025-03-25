# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-8
# Description: 基本公卫 - 高血压管理 - 高血压随访 应用
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
Web_PO.opnLabel(d_menu_basicPHS['高血压随访'])
Web_PO.swhLabel(1)


# todo 需求：检查所有记录，生成2025-02-17的随访日期，且下一次随访日期设置为2025-6-15
# 分析，遍历所有随访记录，如果没有2025-02-17的随访日期，就引用上一次随访新增；否则忽略。

# 格式化日期
visitDate = '2025-02-17'
l_visitDate = []
l_1 = visitDate.split("-")
for i in l_1:
    l_visitDate.append(int(i))
print(l_visitDate)  # [2025, 2, 17]

visitNextDate = '2025-06-15'
l_visitNextDate = []
l_1 = l_visitNextDate.split("-")
for i in l_1:
    l_visitNextDate.append(int(i))
print(l_visitNextDate)  # v[2025, 6, 15]


# 获取记录数和页数
# print(Gw_PO.pagination(1))  # {'totalRecord': 17, 'totalPage': 2, 'gotoPage': 2}
try:
    d_page = Gw_PO.pagination(1)
    total_pages = d_page.get('totalPage', 1)
except Exception as e:
    print(f"Error fetching pagination details: {e}")
    total_pages = 1


# 遍历所有页
for j in range(d_page['totalPage']):
    Gw_PO.pagination(j+1)
    sleep(2)
    ele2 = Web_PO.getSuperEleByX("//tbody", ".")
    i_recordCount = Web_PO.eleGetCountByTag(ele2, "tr")
    # print(i_recordCount)
    # 遍历所有的记录，点击编辑
    for i in range(i_recordCount):
        if Web_PO.eleIsEleExistByX(ele2, ".//tr[" + str(i+1) + "]/td[15]/div/button[2]"):
            print("第" + str(j+1) + "页, 第" + str(i+1) + "条，" + Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[1]/div/span"))
            Web_PO.eleClkByX(ele2, ".//tr[" + str(i+1) + "]/td[15]/div/button[2]")

            # 获取当前患者的所有随访日期
            Web_PO.zoom(50)
            ele = Web_PO.getEleByClassName("formList")
            l_followUp_date = Web_PO.eleGetShadowByXsByC(ele, ".//form/div[1]/div/div/div/input",'div:nth-last-of-type(1)')
            print('随访记录 => ', l_followUp_date)  # ['2025-02-21', '2025-02-19', '2025-02-14', '2025-02-13']
            Web_PO.zoom(100)

            # 检查随访日期 2025-02-17 是否存在
            if visitDate not in l_followUp_date:
                # 1，随访日期中没有 2025-02-17，引用上一次记录
                print("引入上次新增, ", visitDate)
                Gw_PO.phs_hypertension_gxyjob_operation({'operate': '编辑', 'index': {'operate2': '引入上次新增'},
                                                      "value": {'随访日期': l_visitDate, '下次随访日期': l_visitNextDate}})
            else:
                # 2，随访日期中有 2025-02-17，跳过
                print("跳过, ", visitDate)

            ele = Web_PO.getSuperEleByX("//span[text()='关闭']", ".")
            Web_PO.eleClkByX(ele, ".", 2)
        else:
            print("[warning, 无编辑], 第" + str(j+1) + "页, 第" + str(i+1) + "条，" + Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[1]/div/span"))


