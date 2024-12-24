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

ErpApp_PO.login(post="浦东01/闵行06【经理岗】")


# todo 今日团队综合排名
# 列表数据
# print(ErpApp_PO.todayRank())  # {'今日新增客户数': ['0人', '团队排名：1 / 9'], '实地工作拜访完成率': ['0.00%', '团队排名：1 / 9'], '双A客户拜访频率': ['0.00%', '团队排名：1 / 9'], '高潜客户拜访频率': ['0.00%', '团队排名：1 / 9']}

# Top 排名
print(ErpApp_PO.topRank({"开始日期": ['2023', '09', '06'], "结束日期": ['2024', '09', '06'], "排名": "团队排名"}))
# print(ErpApp_PO.topRank({"开始日期": ['2023', '09', '06'], "结束日期": ['2024', '09', '06'], "排名": "个人排名"}))

