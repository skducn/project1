# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-7-25
# Description: cookies鉴权自动化
# 测试环境 # http://192.168.0.243:8010/#/login
# 'cs', '12345678'
#***************************************************************
from PO.WebPO import *
Web_PO = WebPO("chromeCookies")
Web_PO.openUrlByCookies('http://192.168.0.243:8010/', 'cookies.json', 'http://192.168.0.243:8010/#/SignManage/signAssess')
Web_PO.opnLabel('http://192.168.0.243:8010/#/SignManage/service')
Web_PO.swhLabel(0)


