# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-7-25
# Description: 公卫 - 鉴权自动化 - 执行
# 测试环境 # http://192.168.0.203:30080/#/login
#***************************************************************
from GwPO_sign import *

# 1, 生成1genAuthorization.json （可执行1genCookies.py手工生成）
Gw_PO_sign = GwPO_sign('不打开浏览器，自动生成1genCookies.json')

# 2，访问受保护页面1
from PO.WebPO import *
Web_PO = WebPO("chromeCookies")
Web_PO.openUrlByAuth(Configparser_PO.AUTH("cookie_file"), Configparser_PO.AUTH("url_prefix"), Configparser_PO.AUTH("url_prefix") + '/Sign/jmsign/qyfile')
# 3，访问受保护页面2（同一个浏览器）
# Web_PO.opnLabel(Configparser_PO.AUTH("url_prefix") + '/Sign/jmsign/qyservice')
# Web_PO.swhLabel(0)

# 4，访问受保护页面3（重现打开一个浏览器）
Web_PO = WebPO("chromeCookies")
Web_PO.openUrlByAuth(Configparser_PO.AUTH("cookie_file"), Configparser_PO.AUTH("url_prefix"), Configparser_PO.AUTH("url_prefix") + '/Sign/jmsign/qyservice')
Web_PO.openURL(Configparser_PO.AUTH("url_prefix") + '/Sign/jmsign/qyservice')
