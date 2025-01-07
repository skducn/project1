# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-12-3
# Description: 盛蕴ERP管理平台(测试环境) , 基础服务 - 产品管理
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

# todo 产品信息管理
Erp_PO.newLabel(d_menu_url["产品信息管理"], 1)
# 1 查询
# d_ = Erp_PO.product_search({"产品编码": "CP101", "产品名称": "依叶", "品规编码": "CP101PG10", "品规": "10mg:0.8mg*7T",
#                             "剂型类别": "素片", "产品类型": "药品", "启用状态": "启用", "最后更新时间": [2024, 11, 6, 2024, 12, 29]})
# d_ = Erp_PO.product_search({"产品编码": "CP101", "产品名称": "依叶"})
# print(d_)  # {'id': 'CP101', 'qty': 1}

# 2 新增(依赖于查询)
d_ = Erp_PO.product_search({"产品编码": "CP1013", "产品名称": "依叶4"})
print(d_) # {'id': None, 'qty': None}
d_ = Erp_PO.product_add(d_['qty'], {"产品名称": "alt", "通用名称": "爱乐团心电", "产品类型": "心电", "产品观念": ["1,qqq"],
                                       "产品品规信息": [{"品规": "10mg", "剂型类别": "素片", "计量单位": "个", "零售价格": "100", "成本价格": "33", "产品有效期": "12个月", "启用状态": "启用", "备注信息": "测试1峡"},
                                                 {"品规": "11mg", "剂型类别": "胶囊", "计量单位": "天", "零售价格": "200", "成本价格": "44", "产品有效期": "6个月", "启用状态": "停用", "备注信息": "测试2峡"},
                                                 {"品规": "12mg", "剂型类别": "针剂", "计量单位": "支", "零售价格": "300", "成本价格": "55", "产品有效期": "36个月", "启用状态": "启用", "备注信息": "测试3峡"}]
                                    })





