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

from ErpPO import *
Erp_PO = ErpPO()


# 登录
Erp_PO.login("http://192.168.0.202:28098/login?redirect=/index", "zhuyan", "Zy123456")

# 获取所有子菜单Url字典
# d_menu_url = Erp_PO.getMenuUrl()
# print(d_menu_url)  # {'': 'http://192.168.0.202:28098/', '首页': 'http://192.168.0.202:28098/index', '医院管理': 'http://192.168.0.202:28098/mainData/mainData/hospital', '站点管理': 'http://192.168.0.202:28098/mainData/mainData/site', '经销商管理': 'http://192.168.0.202:28098/mainData/mainData/dealer', '客户管理': 'http://192.168.0.202:28098/mainData/mainData/customer', '商业公司管理': 'http://192.168.0.202:28098/mainData/mainData/business', '部门管理': 'http://192.168.0.202:28098/mainData/structure/department', '岗位管理': 'http://192.168.0.202:28098/mainData/structure/job', '员工管理': 'http://192.168.0.202:28098/mainData/structure/employee', '岗位与员工管理': 'http://192.168.0.202:28098/mainData/structure/jobAndEmployee', '部门与岗位管理': 'http://192.168.0.202:28098/mainData/structure/departAndJob', '辖区分配': 'http://192.168.0.202:28098/mainData/area/distribution', '辖区医院关系': 'http://192.168.0.202:28098/mainData/area/areaAndHospital', '辖区客户关系': 'http://192.168.0.202:28098/mainData/area/areaAndCustomer', '辖区产品关系': 'http://192.168.0.202:28098/mainData/area/areaAndProduct', '辖区关系转接': 'http://192.168.0.202:28098/mainData/area/areaAndTransfer', '辖区关系总表': 'http://192.168.0.202:28098/mainData/area/areaGeneralRelation', '产品信息管理': 'http://192.168.0.202:28098/mainData/productManagement/productInfo', '病例收集': 'http://192.168.0.202:28098/businessData/medicalHistoryManagement/medicalHistorylist', '产品开发管理': 'http://192.168.0.202:28098/businessData/developmentManagement/productDevelopment', '依叶潜力管理': 'http://192.168.0.202:28098/businessData/potential/yiye', '氨叶潜力管理': 'http://192.168.0.202:28098/businessData/potential/anye', '整肠生潜力管理': 'http://192.168.0.202:28098/businessData/potential/zcs', '患者数管理': 'http://192.168.0.202:28098/businessData/potential/patients', '指标查询': 'http://192.168.0.202:28098/businessData/kpiManagement/kpiQuery', '拜访列表': 'http://192.168.0.202:28098/behavioralData/visitManagement/visitList', '协访列表': 'http://192.168.0.202:28098/behavioralData/helpManagement/helpList', '会议列表': 'http://192.168.0.202:28098/behavioralData/meetingManagement/meetingList', '工作计划': 'http://192.168.0.202:28098/behavioralData/scheduleManagement/workPlan', '审批中心': 'http://192.168.0.202:28098/dataMaintenance/approvalManagement/approvalcenter', '标签列表': 'http://192.168.0.202:28098/dataMaintenance/labelManagement/labelList', '机构别名管理': 'http://192.168.0.202:28098/dataMaintenance/aliasManagement/organizationList', '产品别名管理': 'http://192.168.0.202:28098/dataMaintenance/aliasManagement/productAliasList', '地址别名管理': 'http://192.168.0.202:28098/dataMaintenance/aliasManagement/addressAliasList', '消息模板配置': 'http://192.168.0.202:28098/dataMaintenance/notificationCenter/msgTemplateConfig', '手动消息推送': 'http://192.168.0.202:28098/dataMaintenance/notificationCenter/manualMsgPush', '自动消息推送': 'http://192.168.0.202:28098/dataMaintenance/notificationCenter/automaticMsgPush', '原始流向': 'http://192.168.0.202:28098/businessManagement/originalFlowDirection', '标准流向': 'http://192.168.0.202:28098/businessManagement/standardFlowDirection', '商业合同管理': 'http://192.168.0.202:28098/businessManagement/commercialContract', '医院库存': 'http://192.168.0.202:28098/businessManagement/hospitalInventory', '纯销管理': 'http://192.168.0.202:28098/businessManagement/netSaleManagement', '拜访分析报表': 'http://192.168.0.202:28098/statisticalManagement/visitAnalysisReport', '投入产出分析报表': 'http://192.168.0.202:28098/statisticalManagement/inputOutputAnalysisReport', '协访分析报表': 'http://192.168.0.202:28098/statisticalManagement/helpAnalysisReport', '用户管理': 'http://192.168.0.202:28098/system/user', '角色管理': 'http://192.168.0.202:28098/system/role', '菜单管理': 'http://192.168.0.202:28098/system/menu', '参数管理': 'http://192.168.0.202:28098/system/parameter', '名称转换查询': 'http://192.168.0.202:28098/system/nameConversionQuery', '定时任务': 'http://192.168.0.202:28098/monitor/timedTask'}
d_menu_url = {'': 'http://192.168.0.202:28098/', '首页': 'http://192.168.0.202:28098/index', '医院管理': 'http://192.168.0.202:28098/mainData/mainData/hospital', '站点管理': 'http://192.168.0.202:28098/mainData/mainData/site', '经销商管理': 'http://192.168.0.202:28098/mainData/mainData/dealer', '客户管理': 'http://192.168.0.202:28098/mainData/mainData/customer', '商业公司管理': 'http://192.168.0.202:28098/mainData/mainData/business', '部门管理': 'http://192.168.0.202:28098/mainData/structure/department', '岗位管理': 'http://192.168.0.202:28098/mainData/structure/job', '员工管理': 'http://192.168.0.202:28098/mainData/structure/employee', '岗位与员工管理': 'http://192.168.0.202:28098/mainData/structure/jobAndEmployee', '部门与岗位管理': 'http://192.168.0.202:28098/mainData/structure/departAndJob', '辖区分配': 'http://192.168.0.202:28098/mainData/area/distribution', '辖区医院关系': 'http://192.168.0.202:28098/mainData/area/areaAndHospital', '辖区客户关系': 'http://192.168.0.202:28098/mainData/area/areaAndCustomer', '辖区产品关系': 'http://192.168.0.202:28098/mainData/area/areaAndProduct', '辖区关系转接': 'http://192.168.0.202:28098/mainData/area/areaAndTransfer', '辖区关系总表': 'http://192.168.0.202:28098/mainData/area/areaGeneralRelation', '产品信息管理': 'http://192.168.0.202:28098/mainData/productManagement/productInfo', '病例收集': 'http://192.168.0.202:28098/businessData/medicalHistoryManagement/medicalHistorylist', '产品开发管理': 'http://192.168.0.202:28098/businessData/developmentManagement/productDevelopment', '依叶潜力管理': 'http://192.168.0.202:28098/businessData/potential/yiye', '氨叶潜力管理': 'http://192.168.0.202:28098/businessData/potential/anye', '整肠生潜力管理': 'http://192.168.0.202:28098/businessData/potential/zcs', '患者数管理': 'http://192.168.0.202:28098/businessData/potential/patients', '指标查询': 'http://192.168.0.202:28098/businessData/kpiManagement/kpiQuery', '拜访列表': 'http://192.168.0.202:28098/behavioralData/visitManagement/visitList', '协访列表': 'http://192.168.0.202:28098/behavioralData/helpManagement/helpList', '会议列表': 'http://192.168.0.202:28098/behavioralData/meetingManagement/meetingList', '工作计划': 'http://192.168.0.202:28098/behavioralData/scheduleManagement/workPlan', '审批中心': 'http://192.168.0.202:28098/dataMaintenance/approvalManagement/approvalcenter', '标签列表': 'http://192.168.0.202:28098/dataMaintenance/labelManagement/labelList', '机构别名管理': 'http://192.168.0.202:28098/dataMaintenance/aliasManagement/organizationList', '产品别名管理': 'http://192.168.0.202:28098/dataMaintenance/aliasManagement/productAliasList', '地址别名管理': 'http://192.168.0.202:28098/dataMaintenance/aliasManagement/addressAliasList', '消息模板配置': 'http://192.168.0.202:28098/dataMaintenance/notificationCenter/msgTemplateConfig', '手动消息推送': 'http://192.168.0.202:28098/dataMaintenance/notificationCenter/manualMsgPush', '自动消息推送': 'http://192.168.0.202:28098/dataMaintenance/notificationCenter/automaticMsgPush', '原始流向': 'http://192.168.0.202:28098/businessManagement/originalFlowDirection', '标准流向': 'http://192.168.0.202:28098/businessManagement/standardFlowDirection', '商业合同管理': 'http://192.168.0.202:28098/businessManagement/commercialContract', '医院库存': 'http://192.168.0.202:28098/businessManagement/hospitalInventory', '纯销管理': 'http://192.168.0.202:28098/businessManagement/netSaleManagement', '拜访分析报表': 'http://192.168.0.202:28098/statisticalManagement/visitAnalysisReport', '投入产出分析报表': 'http://192.168.0.202:28098/statisticalManagement/inputOutputAnalysisReport', '协访分析报表': 'http://192.168.0.202:28098/statisticalManagement/helpAnalysisReport', '用户管理': 'http://192.168.0.202:28098/system/user', '角色管理': 'http://192.168.0.202:28098/system/role', '菜单管理': 'http://192.168.0.202:28098/system/menu', '参数管理': 'http://192.168.0.202:28098/system/parameter', '名称转换查询': 'http://192.168.0.202:28098/system/nameConversionQuery', '定时任务': 'http://192.168.0.202:28098/monitor/timedTask'}

#***************************************************************

# todo 基础服务 - 主数据管理 - 医院管理
# Erp_PO.newLabel(d_menu_url["医院管理"], 1)
# 1 查询
# Erp_PO.hospital_search({"医院编码": "HCO00002842", "医院名称": "六院东分地址", "医院级别": "一级医院",
#                         "省份": "上海", "城市": "上海市", "区县": "浦东新区", "启用状态": "启用",
#                         "最后更新时间": ["2024-12-06","2024-12-29"]})
# Erp_PO.hospital_search({"医院名称": "上海市青浦区中医医院"})
# Erp_PO.hospital_search({"医院名称": "上海市青浦区中医医院", "启用状态": "启用", "最后更新时间": ["2024-12-06","2024-12-15"]})
# Erp_PO.hospital_search({"省份": "河北省"})
# Erp_PO.hospital_search({"医院编码": "HCO00000001", "医院名称": "闵服务", "省份": "河北省"})

# 2 重置
# Erp_PO.hospital_reset()

# 3 新增，并获取新增后的医院编码
# Erp_PO.hospital_add({"医院全称": "上海自动化医院", "医院简称": "上自院", "医院类型": "分院", "医院级别": "民营",
#                      "省份": "上海", "启用状态": "启用", "城市": "上海市", "区县": "浦东新区", "详细地址": "上海广中西路多媒体大厦",
#                      "获取方式": "自动获取", "邮政编码": "200120", "电话": "021-58771234", "邮箱": "zy@163.com", "网址": "http://www.zy.com", "床位数": "111", "门诊量": "10000",
#                      "备注信息": "自动化测试用，请勿删除"})

# 4 列表字段设置
# Erp_PO.hospital_setup(3, {"医院编码": {"字段宽度设置": "200", "列表是否显示": "否", "详情是否显示": "否", "是否固定": "是"},
#                        "省份": {"字段宽度设置": "100", "列表是否显示": "否", "详情是否显示": "否", "是否固定": "是"}})


# 5 修改
# Erp_PO.hospital_edit({"医院名称": "上海自动化医院"},
#                      {"医院全称": "天津自动化医院1", "医院简称": "天自院1", "医院类型": "总院", "医院级别": "二级医院",
#                       "省份": "天津", "启用状态": "启用", "城市": "天津市", "区县": "南开区", "详细地址": "天津市南开区卫津路94号",
#                       "获取方式": "自动获取", "邮政编码": "300392", "电话": "022-23729426", "邮箱": "nk@163.com", "网址": "http://www.nk.com", "床位数": "50", "门诊量": "20000",
#                       "备注信息": "自动化测试用，请勿删除1"}
#                     )

# 6 详情
# Erp_PO.hospital_info({"医院名称": "天津自动化医院1"})



#***************************************************************

# todo 基础服务 - 主数据管理 - 经销商管理
# Erp_PO.newLabel(d_menu_url["经销商管理"], 1)
# 1 查询
# Erp_PO.dealer_search({"经销商编码": "HCO00002842", "经销商名称": "百慕大自动优质经销商", "经销商级别": "一级",
#                         "省份": "上海", "城市": "上海市", "区县": "浦东新区", "启用状态": "启用",
#                         "最后更新时间": ["2024-12-06","2024-12-29"]})

# 2 重置
# Erp_PO.hospital_reset()

# # 3 新增，并获取新增后的经销商编码
# Erp_PO.dealer_add({"经销商名称": "百慕大自动优质经销商",
#                      "省份": "上海", "城市": "上海市", "区县": "浦东新区", "详细地址": "上海浦东南路1000号", "联系电话": "021-58776522",
#                      "启用状态": "启用", "经销商级别": "一级",
#                      "备注信息": "测试一下"})

# 4 列表字段设置
# Erp_PO.hospital_setup(5, {"经销商编码": {"字段宽度设置": "200", "列表是否显示": "否", "详情是否显示": "否", "是否固定": "是"},
#                        "联系电话": {"字段宽度设置": "100", "列表是否显示": "否", "详情是否显示": "否", "是否固定": "是"}})

# 5 修改
# Erp_PO.dealer_edit({"经销商名称": "百慕大自动优质经销商"},
#                    {"经销商名称": "百慕大自动优质经销商1",
#                     "省份": "天津", "城市": "天津市", "区县": "南开区", "详细地址": "天津市南开区卫津路94号", "联系电话": "022-23729427",
#                     "启用状态": "停用", "经销商级别": "二级",
#                     "备注信息": "测试一下123"}
#                     )

# 6 详情
# Erp_PO.dealer_info({"经销商名称": "百慕大自动优质经销商1"})

#***************************************************************

# todo 基础服务 - 主数据管理 - 商业公司管理
Erp_PO.newLabel(d_menu_url["商业公司管理"], 1)

# 1 查询
# Erp_PO.business_search({"商业公司编码": "COM00004", "商业公司全称": "阿依达商业自动化有限公司", "联系人": "张三",
#                         "启用状态": "启用", "最后更新时间": ["2025-1-1", "2025-1-3"]})


# # 3 新增，并获取新增后的经销商编码
# 联系人电话 无法填写固定电话
# Erp_PO.business_add({"商业公司全称": "阿依达商业自动化有限公司", "商业公司简称": "ayt自动化", "商业公司地址": "上海东方路100号", "联系人": "张三", "联系人电话": "13816109040",
#                      "合同开始日期": "2020-12-12", "合同结束日期": "2020-12-22", "合同编号": "AGT111", "许可证编号": "tg1234567","许可证有效期": "2020-10-01", "营业执照编号": "Tg66666",
#                      "营业执照有效期": "2024-12-16", "企业类别": "经营", "启用状态": "启用", "生产(经营)范围": "电子化工类", "备注信息": "商业伙伴信息"
#                      })


# 4 列表字段设置（未处理）
# Erp_PO.business_setup(3, {"经销商编码": {"字段宽度设置": "200", "列表是否显示": "否", "详情是否显示": "否", "是否固定": "是"},
#                        "联系电话": {"字段宽度设置": "100", "列表是否显示": "否", "详情是否显示": "否", "是否固定": "是"}})

# 5 修改
# Erp_PO.business_edit({"商业公司全称": "阿依达商业自动化有限公司"},
#                      {"商业公司全称": "阿依达商业自动化有限公司3", "商业公司简称": "ayt自动化3", "商业公司地址": "上海东方路100号3", "联系人": "张三3",
#                       "联系人电话": "13816109041",
#                       "合同开始日期": "2019-12-12", "合同结束日期": "2023-12-22", "合同编号": "AGT1119", "许可证编号": "tg12345679","许可证有效期": "2020-10-12", "营业执照编号": "Tg666669",
#                       "营业执照有效期": "2024-12-16", "企业类别": "经营", "启用状态": "启用", "生产(经营)范围": "电子化工类9", "备注信息": "商业伙伴信息9"
#                       }
#                     )

# 6 详情
Erp_PO.business_info({"商业公司全称": "阿依达商业自动化有限公司3"})