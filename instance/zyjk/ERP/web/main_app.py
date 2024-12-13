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

url = "https://syym.zy-health.net:9443/#/home"

# 登录app
# ErpApp_PO.login(url, "zhuyan", "Zy123456")
# ErpApp_PO.login(url, "xuewei", "Zy123456", "浦东01/闵行06【经理岗】")
ErpApp_PO.login(url, "xuewei", "Zy123456", "浦东01/闵行06/徐汇07【代表岗】")

# ErpApp_PO.Web_PO.scrollToBottom()
# ErpApp_PO.Web_PO.scrollToView("//a[@href='#/meeting']")
# ErpApp_PO.Web_PO.scrollToView("//a[last()]")  # 拖动到最后一个a标签

# ErpApp_PO.Web_PO.scrollByStep(200)
# ErpApp_PO.Web_PO.scrollByStep(200)
# ErpApp_PO.Web_PO.scrollByStep(200)
# ErpApp_PO.Web_PO.scrollByAuto(100)

# todo 首页
# todo 看板辖区
# 切换
# ErpApp_PO.switchArea("奉贤/金山", "嘉定02")  # 有bug


# todo 今日团队综合排名
# Top 排名
# ErpApp_PO.topRank([2023, 9, 6], "团队排名")
# ErpApp_PO.topRank([2023, 9, 6], "个人排名")
# 列表数据
# print(ErpApp_PO.todayRank())  # {'今日新增客户数': ['0人', '团队排名：1 / 9'], '实地工作拜访完成率': ['0.00%', '团队排名：1 / 9'], '双A客户拜访频率': ['0.00%', '团队排名：1 / 9'], '高潜客户拜访频率': ['0.00%', '团队排名：1 / 9']}


# todo 行为分析
# 获取团队拜访、团队会议、团队开发数据
# print(ErpApp_PO.behaviorAnalysis())  # {'今日团队拜访总人次': '0', '推广相关拜访人次': '0', '拜访达成目标人次': '0', '达成率': '0.00%', '定位匹配率': '0.00%', '双A客户拜访人次': '0', '双A客户拜访占比': '0.00%', '高潜客户拜访人次': '0', '高潜客户拜访占比': '0.00%', '会前客户拜访人次': '0', '会后客户跟进拜访人次': '0', '开发拜访人次': '0', '今日团队需执行会议场次': '0', '已完成会议场次': '9', '未完成会议场次': '8', '开发产品计划': '19', '锁定报告': '3', '完成率': '15.79%', '已评估能过会医院': '3', '开发达成率': '15.79%'}


# todo 业绩分析
# ErpApp_PO.getProduct("依叶")  # 可选 氨叶，整肠生，依叶
# ErpApp_PO.getProduct("整肠生")  # 可选 氨叶，整肠生，依叶


# todo 功能 - 医院管理
# ErpApp_PO.hospital({"搜索": " 上海广中      西路120号        ", "产品信息": "欣地平",
#                     "科室主任": {"李标": "支持"}, "药剂科主任": {"唐晓晶": "中立"}, "医务处长": {"萧屹": "反对"}, "业务院长": {"吴凤灵": "中立"}, "院长": {"王丽红": "中立"},
#                     "其他药事会成员": {"唐晓晶": "支持", "刘月月": "反对", "李剑": "中立"},
#                     "提单科室": "消化科", "提单规则": "只可会前提单", "提单状态": "考虑中", "过会规则": "需投票，过三分之二票数",
#                     "药剂科会前确认信息": "已收到报告，确认不上会", "药事会实际召开时间": [2034, 1, 31, 23, 59], "会前评估能否过会": "否", "经改进后能否过会": "否", "过会日期": [2020, 12, 1, 0, 0]})

# ErpApp_PO.hospital({"搜索": "奉贤区青村南路182号", "产品信息": "依叶",
#                     "科室主任": {"李标": "支持"}, "药剂科主任": {"唐晓晶": "中立"},"医务处长": {"萧屹": "反对"}, "业务院长": {"吴凤灵": "中立"}, "院长": {"王丽红": "中立"},
#                     "其他药事会成员": {"唐晓晶": "支持", "刘月月": "反对", "李剑": "中立"},
#                     "提单科室": "消化科", "提单规则": "只可会前提单", "提单状态": "考虑中", "过会规则": "需投票，过三分之二票数",
#                     "药剂科会前确认信息": "已收到报告，确认不上会", "药事会实际召开时间": [2034, 1, 31, 23, 59], "会前评估能否过会": "否", "经改进后能否过会": "否", "过会日期": [2020, 12, 1, 0, 0]})
#
# ErpApp_PO.Web_PO.scrollToBottom(5)

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
# ErpApp_PO.Web_PO.scrollToBottom()
# ErpApp_PO.Web_PO.clkByX("//a[@href='#/product']")
# 1 新增产品开发
# ErpApp_PO.new_product({"开发医院类型": "站点", "开发医院信息": "曹路社区", "开发产品名称": "依叶", "开发负责人1": "薛伟", "开发负责人2": "陈东升",
# "药事会计划开始日期": [2024, 10, 12], "药事会计划结束日期": [2024, 12, 12], "提单科室": "呼吸科"})

# # 2.1 获取拜访人数据
# d_data = ErpApp_PO.get_product_visitor({"标签": "跟进中", "搜索": "崇中心"})
# print("2.1 获取拜访人数据 =>", d_data)
# # 2.2 更新拜访人数据
# ErpApp_PO.set_product_visitor(d_data, {'拜访及态度': {'主要成员': {'科室主任': ['陈海群', '中立'], '药剂科主任': ['杨忠英', '反对'], '医务处长': ['陈海群', '支持'], '业务院长': ['陈健', '中立'], '院长': ['王旭辉', '支持']},
#                                          '其他药事会成员': [['郭震', '支持']]}})
# print("2.2 更新拜访人数据 => done")

# # # 3.1 获取开发跟进数据
# d_data = ErpApp_PO.get_product_devFollowUp({"标签": "跟进中", "搜索": "崇中心"})
# print("3.1 获取开发跟进数据 =>", d_data)
# # 3.2 更新开发跟进列表数据
# ErpApp_PO.set_product_devFollowUp({"开发次数": "二次开发", "提单科室": "神外", "提单规则": "可随时提单", "过会规则": ["需投票，过三分之二票数", "临床主任确认即可过会"],
#                                    "提单状态": "可随时提单，已承诺", "药剂科会前确认信息": "未收到报告", "药事会计划开始日期": [2024, 8, 10],
#                                    "药事会计划结束日期": [2024, 9, 10], "药事会实际召开时间": [2024, 12, 12, 16, 24], "会前评估能否过会": "否", "经改进后能否过会": "是",
#                                    "过会日期": [2024, 11, 12]})
# print("3.2 更新开发跟进数据 => done")

# # 4 获取产品开发详情
# d_data = ErpApp_PO.get_product_info({"标签": "跟进中", "搜索": "曹路"})
# d_data = ErpApp_PO.get_product_info({"标签": "跟进中", "搜索": "永"})
# d_data = ErpApp_PO.get_product_info({"标签": "跟进中", "搜索": "崇中心"})
# d_data = ErpApp_PO.get_product_info({"标签": "已结束", "搜索": "崇中心"})
# print("4 获取产品开发详情 =>", d_data)


#
# # todo 审批中心
ErpApp_PO.Web_PO.scrollToBottom()
ErpApp_PO.Web_PO.clkByX("//a[@href='#/approve']", 2)
# 1 获取未审批列表页数据
d_data = ErpApp_PO.get_approve_list({"标签": "未审批"})
print(d_data)

# # 2 获取已审批列表页数据
d_data = ErpApp_PO.get_approve_list({"标签": "已审批"})
print(d_data)

# # 3 获取未审批指定医院编号的审批详情
# d_data = ErpApp_PO.get_approve_searchInfo({"标签": "未审批", "搜索": "广医院", "编号": "CV339"})
# print(d_data)
#
# # 4 获取已审批指定医院编号的审批详情
# d_data = ErpApp_PO.get_approve_searchInfo({"标签": "已审批", "搜索": "广医院", "编号": "CV340"})
# print(d_data)






#
# # todo 工作计划
# ErpApp_PO.Web_PO.scrollToBottom()
# ErpApp_PO.Web_PO.clkByX("//a[@href='#/jobPlan']")
