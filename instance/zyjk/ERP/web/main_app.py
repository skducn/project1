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

# 奉贤区青村南路182号

# todo 医院管理
# ErpApp_PO.hospital({"搜索": " 上海广中      西路120号        ", "产品信息": "欣地平",
#                     "科室主任": {"李标": "支持"}, "药剂科主任": {"唐晓晶": "中立"},"医务处长": {"萧屹": "反对"}, "业务院长": {"吴凤灵": "中立"}, "院长": {"王丽红": "中立"},
#                     "其他药事会成员": {"唐晓晶": "支持", "刘月月": "反对", "李剑": "中立"},
#                     "提单科室": "消化科", "提单规则": "只可会前提单", "提单状态": "考虑中", "过会规则": "需投票，过三分之二票数",
#                     "药剂科会前确认信息": "已收到报告，确认不上会", "药事会实际召开时间": [2034, 1, 31, 23, 59], "会前评估能否过会": "否", "经改进后能否过会": "否", "过会日期": [2020, 12, 1, 0, 0]})

ErpApp_PO.hospital({"搜索": "奉贤区青村南路182号", "产品信息": "依叶",
                    "科室主任": {"李标": "支持"}, "药剂科主任": {"唐晓晶": "中立"},"医务处长": {"萧屹": "反对"}, "业务院长": {"吴凤灵": "中立"}, "院长": {"王丽红": "中立"},
                    "其他药事会成员": {"唐晓晶": "支持", "刘月月": "反对", "李剑": "中立"},
                    "提单科室": "消化科", "提单规则": "只可会前提单", "提单状态": "考虑中", "过会规则": "需投票，过三分之二票数",
                    "药剂科会前确认信息": "已收到报告，确认不上会", "药事会实际召开时间": [2034, 1, 31, 23, 59], "会前评估能否过会": "否", "经改进后能否过会": "否", "过会日期": [2020, 12, 1, 0, 0]})

ErpApp_PO.Web_PO.scrollToBottom(5)

# # todo 客户管理
# ErpApp_PO.customer()
# ErpApp_PO.Web_PO.scrollToBottom(5)
#
# # todo 拜访管理
# ErpApp_PO.visit()
# ErpApp_PO.Web_PO.scrollToBottom(5)
#
# # todo 协防管理
# ErpApp_PO.withVisit()
# ErpApp_PO.Web_PO.scrollToBottom(5)
#
# # todo 会议管理
# ErpApp_PO.meeting()
# ErpApp_PO.Web_PO.scrollToBottom(5)
#
# # todo 产品开发
# ErpApp_PO.product()
# ErpApp_PO.Web_PO.scrollToBottom(5)
#
# # todo 审批中心
# ErpApp_PO.approve()
# ErpApp_PO.Web_PO.scrollToBottom(5)
#
# # todo 工作计划
# ErpApp_PO.jobPlan()
# ErpApp_PO.Web_PO.scrollToBottom(5)