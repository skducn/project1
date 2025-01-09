# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-12-3
# Description: 盛蕴ERP管理平台(测试环境) , 基础服务 - 组织架构管理
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
# todo 部门管理（无法操作列表启动状态）
# Erp_PO.newLabel(d_menu_url["部门管理"], 1)
# 1 查询
# Erp_PO.department_search({"周期版本": "HCO00002842", "部门信息": "六院东分地址", "上级部门信息": "一级医院", "启用状态": "启用",
#                         "最后更新时间": ["2024-12-06","2024-12-29"]})



#***************************************************************
# todo 岗位管理（无法操作列表启动状态）

# Erp_PO.newLabel(d_menu_url["岗位管理"], 1)
# 1 查询
# Erp_PO.post_search({"周期版本": "202412版本", "岗位信息": "超级管理员", "岗位类型": "销售岗", "所属部门信息": "上海智赢健康科技有限公司",
#                          "岗位部门关系ID": "GWBM0000001", "启用状态": "启用", "最后更新时间": ["2024-12-06","2024-12-29"]}, "销售岗销售类别":"耗材")



#***************************************************************
# todo 员工管理 （无法搜索员工信息，职位还是职称）
Erp_PO.newLabel(d_menu_url["员工管理"], 1)
# 1 查询
d_ = Erp_PO.staff_search({"员工信息": "朱燕", "联系方式": "17710909010", "职位": "推广代表", "是否在职": "在职",
                        "入职日期": [2025, 1, 1, 2025, 1, 11], "离职日期": [2025, 2, 1, 2025, 2, 11], "主管信息": "朱燕", "启用状态": "启用",
                        "最后更新时间": [2025, 1, 1, 2025, 1, 12]})
print(d_)  # {'id': '100076', 'qty': 1}

# 2 新增(依赖于查询)
# d_ = Erp_PO.staff_search({"联系方式": "13611990901"})
# print(d_) # {'id': None, 'qty': None}
# Erp_PO.staff_add(d_['qty'], {"员工姓名": "提1", "省份": "上海", "城市": "上海市", "性别": "男", "联系方式": "17710909010",
#                    "邮箱": "ti@163.com","职称": "推广代表", "是否在职": "离职", "入职日期": "2025-01-08", "主管信息": "朱燕",
#                      "启用状态": "启用", "备注信息": "测试二下"})

# 3 修改(依赖于查询)
# d_ = Erp_PO.staff_search({"联系方式": "13611990909"})
# print(d_)  # {'id': '100076', 'qty': 1}
# Erp_PO.staff_edit(d_['qty'], {"员工姓名": "提23", "省份": "天津", "城市": "天津市", "性别": "女", "联系方式": "13611990909", "邮箱": "gege@263.com",
#                     "职称": "财务总监", "是否在职": "离职", "入职日期": "2025-01-02", "离职日期": "2025-01-03", "启用状态": "停用", "主管信息": "刘廷", "备注信息": "测试一下123"})
# # 在职状态下，不可选离职日期
# Erp_PO.staff_edit(d_['qty'], {"员工姓名": "提23", "省份": "天津", "城市": "天津市", "性别": "女", "联系方式": "13611990909", "邮箱": "gege@263.com",
#                     "职称": "财务总监", "是否在职": "在职", "入职日期": "2025-01-02", "启用状态": "停用", "主管信息": "刘廷", "备注信息": "测试一下123"})

# 4 详情
# d_ = Erp_PO.staff_search({"联系方式": "13611990909"})
# print(d_)  # {'id': '100076', 'qty': 1}
# Erp_PO.staff_info(d_['qty'])

# 5 导出

#***************************************************************

# todo 岗位与员工管理
# Erp_PO.newLabel(d_menu_url["岗位与员工管理"], 1)



#***************************************************************

# todo 部门与岗位管理
# Erp_PO.newLabel(d_menu_url["部门与岗位管理"], 1)

