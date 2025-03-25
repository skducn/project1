# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-3-25
# Description: 基本公卫 - 统计报表 - 数据统计
# *****************************************************************
import sys,os
# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取 上层 目录的绝对路径
project_dir = os.path.abspath(os.path.join(current_dir, '..'))
# 将 上层 目录添加到 sys.path
sys.path.insert(0, project_dir)
from GwPO_report import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO_report = GwPO_report(logName)
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('../config.ini')
# 登录
Gw_PO_report.login(Configparser_PO.HTTP("url"), Configparser_PO.ACCOUNT("user"), Configparser_PO.ACCOUNT("password"))
# 菜单
d_menu_report = {'城乡居民健康档案管理报表': 'http://192.168.0.203:30080/report/Statistics/report1', '高血压患者健康管理报表': 'http://192.168.0.203:30080/report/Statistics/report2', '糖尿病患者健康管理报表': 'http://192.168.0.203:30080/report/Statistics/report3', '老年人健康管理报表': 'http://192.168.0.203:30080/report/Statistics/report4', '0-6岁儿童健康管理报表': 'http://192.168.0.203:30080/report/Statistics/report5', '孕产妇健康管理报表': 'http://192.168.0.203:30080/report/Statistics/report6', '严重精神障碍患者健康管理报表': 'http://192.168.0.203:30080/report/Statistics/report7', '肺结核患者健康管理报表': 'http://192.168.0.203:30080/report/Statistics/report8', '中医药健康管理报表': 'http://192.168.0.203:30080/report/Statistics/report9', '健康教育报表': 'http://192.168.0.203:30080/report/Statistics/report10', '家医签约完成情况报表': 'http://192.168.0.203:30080/report/Statistics/report11', '重点人群签约统计报表': 'http://192.168.0.203:30080/report/Statistics/report12', '签约服务包统计报表': 'http://192.168.0.203:30080/report/Statistics/report13', '慢阻肺病报表': 'http://192.168.0.203:30080/report/Statistics/report19', '健康档案调阅统计': 'http://192.168.0.203:30080/report/Statistics/report20', '慢病管理业务监管': 'http://192.168.0.203:30080/report/Statistics2/report14', '妇幼保健业务监管(孕产妇)': 'http://192.168.0.203:30080/report/Statistics2/report15', '精神疾病业务监管': 'http://192.168.0.203:30080/report/Statistics2/report16', '儿童保健业务监管(新生儿)': 'http://192.168.0.203:30080/report/Statistics2/report17', '儿童保健业务监管(5岁以下)': 'http://192.168.0.203:30080/report/Statistics2/report18'}
Web_PO.opnLabel(d_menu_report['签约服务包统计报表'])
Web_PO.swhLabel(1)



# todo 1 查询
# Gw_PO_report.queryReport({"管理机构": "东庄卫生院", "时间": [[2025,1,1],[2025,3,25]]})


# todo 2 导出
# Gw_PO_report.export("/Users/linghuchong/Desktop/签约服务包统计报表.xls")




