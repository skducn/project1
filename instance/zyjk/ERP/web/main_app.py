# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-12-3
# Description: 盛蕴ERP管理平台(测试环境)
# 手机端：https://syym.zy-health.net:9443/#/home  zhuyan/Zy123456
# PC端：http://192.168.0.202:28098/basicData/mainData/site
# admin/Zy123456
# zhuyan/Zy123456
# mysql：192.168.0.234，root，Zy_123456	zy_crmtest
# 【腾讯文档】项目信息表
# https://docs.qq.com/sheet/DYmZMVmFTeXFWRFpQ?tab=BB08J2
#***************************************************************

from ErpAppPO import *
ErpApp_PO = ErpAppPO()


# 登录app
ErpApp_PO.login("https://syym.zy-health.net:9443/#/home", "zhuyan", "Zy123456")

ErpApp_PO.Web_PO.scrollToBottom()
# ErpApp_PO.Web_PO.scrollToView("//a[@href='#/meeting']")
# ErpApp_PO.Web_PO.scrollToView("//a[last()]")  # 拖动到最后一个a标签

# ErpApp_PO.Web_PO.scrollByStep(200)
# ErpApp_PO.Web_PO.scrollByStep(200)
# ErpApp_PO.Web_PO.scrollByStep(200)
# ErpApp_PO.Web_PO.scrollByAuto(100)

ErpApp_PO.visit()
