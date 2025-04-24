# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-7-25
# Description: 社区健康管理中心CHC - 鉴权自动化 - 执行
# 测试环境 # http://192.168.0.243:8010/#/login 'cs', '12345678'
#***************************************************************
from ChcPO_quanqu import *

# 1, 生成1genAuthorization.json （可执行1genAuthorization.py手工生成）
ChcPO_quanqu('不打开浏览器，自动生成1genAuthorization.json')

# 2，访问受保护页面1
# from PO.WebPO import *
Web_PO = WebPO("chromeCookies")
Web_PO.openUrlByAuth(Configparser_PO.AUTHORIZATION("file"), Configparser_PO.AUTHORIZATION("url_prefix"), Configparser_PO.AUTHORIZATION("url_prefix") + '/#/SignManage/signAssess')
# 3，访问受保护页面2（同一个浏览器）
# Web_PO.opnLabel(Configparser_PO.AUTHORIZATION("url_prefix") + '/#/SignManage/service')
# Web_PO.swhLabel(0)

# 4，访问受保护页面3（重现打开一个浏览器）
Web_PO = WebPO("chromeCookies")
Web_PO.openUrlByAuth(Configparser_PO.AUTHORIZATION("file"), Configparser_PO.AUTHORIZATION("url_prefix"), Configparser_PO.AUTHORIZATION("url_prefix") + '/#/UserManage/interface')
Web_PO.openURL(Configparser_PO.AUTHORIZATION("url_prefix") + '/#/UserManage/interface')


