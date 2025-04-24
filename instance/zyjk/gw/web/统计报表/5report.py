# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-12-19
# Description: 公卫 - 统计报表
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
Gw_PO = GwPO_report(logName)
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('../config.ini')
# 登录
Gw_PO.login(Configparser_PO.HTTP("url"), Configparser_PO.ACCOUNT("user"), Configparser_PO.ACCOUNT("password"))
# 获取基本公卫二级菜单连接
Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li[5]", 2)  # 点击一级菜单统计报表
d_menu_basicPHS = Gw_PO.getMenu2Url()
print('d_menu_basicPHS =', d_menu_basicPHS)
# d_menu_basicPHS = {'城乡居民健康档案管理报表': 'http://192.168.0.203:30080/report/Statistics/report1', '高血压患者健康管理报表': 'http://192.168.0.203:30080/report/Statistics/report2', '糖尿病患者健康管理报表': 'http://192.168.0.203:30080/report/Statistics/report3', '老年人健康管理报表': 'http://192.168.0.203:30080/report/Statistics/report4', '0-6岁儿童健康管理报表': 'http://192.168.0.203:30080/report/Statistics/report5', '孕产妇健康管理报表': 'http://192.168.0.203:30080/report/Statistics/report6', '严重精神障碍患者健康管理报表': 'http://192.168.0.203:30080/report/Statistics/report7', '肺结核患者健康管理报表': 'http://192.168.0.203:30080/report/Statistics/report8', '中医药健康管理报表': 'http://192.168.0.203:30080/report/Statistics/report9', '健康教育报表': 'http://192.168.0.203:30080/report/Statistics/report10', '家医签约完成情况报表': 'http://192.168.0.203:30080/report/Statistics/report11', '重点人群签约统计报表': 'http://192.168.0.203:30080/report/Statistics/report12', '签约服务包统计报表': 'http://192.168.0.203:30080/report/Statistics/report13', '慢阻肺病报表': 'http://192.168.0.203:30080/report/Statistics/report19', '慢病管理业务监管': 'http://192.168.0.203:30080/report/Statistics2/report14', '妇幼保健业务监管(孕产妇)': 'http://192.168.0.203:30080/report/Statistics2/report15', '精神疾病业务监管': 'http://192.168.0.203:30080/report/Statistics2/report16', '儿童保健业务监管(新生儿)': 'http://192.168.0.203:30080/report/Statistics2/report17', '儿童保健业务监管(5岁以下)': 'http://192.168.0.203:30080/report/Statistics2/report18'}


# todo 5 统计报表

# todo 1.1, 数据统计 - 城乡居民健康档案管理报表
# Web_PO.opnLabel(d_menu_report['城乡居民健康档案管理报表'])
# Web_PO.swhLabel(1)

# todo 1.2, 数据统计 - 高血压患者健康管理报表
# Web_PO.opnLabel(d_menu_report['高血压患者健康管理报表'])
# Web_PO.swhLabel(2)

# todo 1.3, 数据统计 - 糖尿病患者健康管理报表
# Web_PO.opnLabel(d_menu_report['糖尿病患者健康管理报表'])
# Web_PO.swhLabel(1)

# todo 1.4, 数据统计 - 老年人健康管理报表
# Web_PO.opnLabel(d_menu_report['老年人健康管理报表'])
# Web_PO.swhLabel(2)

# todo 1.5, 数据统计 - 0-6岁儿童健康管理报表
# Web_PO.opnLabel(d_menu_report['0-6岁儿童健康管理报表'])
# Web_PO.swhLabel(1)

# todo 1.6, 数据统计 - 孕产妇健康管理报表
# Web_PO.opnLabel(d_menu_report['孕产妇健康管理报表'])
# Web_PO.swhLabel(2)

# todo 1.7, 数据统计 - 严重精神障碍患者健康管理报表
# Web_PO.opnLabel(d_menu_report['严重精神障碍患者健康管理报表'])

# todo 1.8, 数据统计 - 肺结核患者健康管理报表
# Web_PO.opnLabel(d_menu_report['肺结核患者健康管理报表'])
# Web_PO.swhLabel(2)

# todo 1.9, 数据统计 - 中医药健康管理报表
# Web_PO.opnLabel(d_menu_report['中医药健康管理报表'])
# Web_PO.swhLabel(2)

# todo 1.10, 数据统计 - 健康教育报表
# Web_PO.opnLabel(d_menu_report['健康教育报表'])
# Web_PO.swhLabel(2)

# todo 1.11, 数据统计 - 家医签约完成情况报表
# Web_PO.opnLabel(d_menu_report['家医签约完成情况报表'])
# Web_PO.swhLabel(2)

# todo 1.12, 数据统计 - 重点人群签约统计报表
# Web_PO.opnLabel(d_menu_report['重点人群签约统计报表'])
# Web_PO.swhLabel(2)

# todo 1.13, 数据统计 - 签约服务包统计报表
# Web_PO.opnLabel(d_menu_report['签约服务包统计报表'])
# Web_PO.swhLabel(2)

# todo 1.14, 数据统计 - 慢阻肺病报表
# Web_PO.opnLabel(d_menu_report['慢阻肺病报表'])
# Web_PO.swhLabel(2)



# todo 2.1, 区域卫生业务监控 - 慢病管理业务监管
# Web_PO.opnLabel(d_menu_report['慢病管理业务监管'])
# Web_PO.swhLabel(2)

# todo 2.2, 区域卫生业务监控 - 妇幼保健业务监管(孕产妇)
# Web_PO.opnLabel(d_menu_report['妇幼保健业务监管(孕产妇)'])
# Web_PO.swhLabel(2)

# todo 2.3, 区域卫生业务监控 - 精神疾病业务监管
# Web_PO.opnLabel(d_menu_report['精神疾病业务监管'])
# Web_PO.swhLabel(2)

# todo 2.4, 区域卫生业务监控 - 儿童保健业务监管(新生儿)
# Web_PO.opnLabel(d_menu_report['儿童保健业务监管(新生儿)'])
# Web_PO.swhLabel(2)

# todo 2.5, 区域卫生业务监控 - 儿童保健业务监管(5岁以下)
# Web_PO.opnLabel(d_menu_report['儿童保健业务监管(5岁以下)'])
# Web_PO.swhLabel(2)