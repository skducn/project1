# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 健康档案管理 - 个人健康档案
# 动态调用函数1
# s_func = 'phs_healthrecord_personal_query'
# getattr(Gw_PO, s_func)({"身份证号": "41052220000511081"})
# 动态调用函数2(有风险)
# s_func = 'Gw_PO.phs_healthrecord_personal_query({"身份证号": "41052220000511081"})'
# eval(s_func)
# *****************************************************************
import sys,os
# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取 上层 目录的绝对路径
project_dir = os.path.abspath(os.path.join(current_dir, ".."))
# 将 上层 目录添加到 sys.path
sys.path.insert(0, project_dir)
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName)
from ConfigparserPO import *
Configparser_PO = ConfigparserPO("../config.ini")
# 登录
Gw_PO.login(Configparser_PO.HTTP("url"), Configparser_PO.ACCOUNT("user"), Configparser_PO.ACCOUNT("password"))
# 菜单
d_menu_basicPHS = {"健康档案概况": "http://192.168.0.203:30080/phs/HealthRecord/ehrindex", "个人健康档案": "http://192.168.0.203:30080/phs/HealthRecord/Personal", "家庭健康档案": "http://192.168.0.203:30080/phs/HealthRecord/Family", "迁入申请": "http://192.168.0.203:30080/phs/HealthRecord/Immigration", "迁出审核": "http://192.168.0.203:30080/phs/HealthRecord/Exit", "档案交接": "http://192.168.0.203:30080/phs/HealthRecord/handoverFile", "死亡管理": "http://192.168.0.203:30080/phs/HealthRecord/DeathManagement", "区域档案查询": "http://192.168.0.203:30080/phs/HealthRecord/regionalFile", "接诊信息查询": "http://192.168.0.203:30080/phs/HealthRecord/Diagnosis", "就诊管理": "http://192.168.0.203:30080/phs/HealthRecord/Visit", "高血压专项": "http://192.168.0.203:30080/phs/Hypertension/gxyregister", "高血压随访": "http://192.168.0.203:30080/phs/Hypertension/gxyjob", "高血压报病": "http://192.168.0.203:30080/phs/Hypertension/gxybb", "糖尿病专项": "http://192.168.0.203:30080/phs/Diabetes/tnbregister", "糖尿病随访": "http://192.168.0.203:30080/phs/Diabetes/tnbjob", "糖尿病报病": "http://192.168.0.203:30080/phs/Diabetes/tnbbb", "慢阻肺病登记": "http://192.168.0.203:30080/phs/Copd/register", "慢阻肺病专项": "http://192.168.0.203:30080/phs/Copd/project", "慢阻肺病随访": "http://192.168.0.203:30080/phs/Copd/visit", "儿童概况": "http://192.168.0.203:30080/phs/Child/etindex", "儿童健康档案": "http://192.168.0.203:30080/phs/Child/etfiles", "中医体质辨识列表": "http://192.168.0.203:30080/phs/Child/tcm", "中医体质辨识汇总": "http://192.168.0.203:30080/phs/Child/tzbs", "儿童检查记录": "http://192.168.0.203:30080/phs/Child/etjob", "孕产妇概况": "http://192.168.0.203:30080/phs/MaternalRecord/ycfindex", "孕产妇登记": "http://192.168.0.203:30080/phs/MaternalRecord/ycfregister", "孕产妇档案": "http://192.168.0.203:30080/phs/MaternalRecord/ycffiles", "孕产妇随访": "http://192.168.0.203:30080/phs/MaternalRecord/ycfjob", "老年人概况": "http://192.168.0.203:30080/phs/Snr/lnrindex", "老年人专项登记": "http://192.168.0.203:30080/phs/Snr/special", "老年人专项管理": "http://192.168.0.203:30080/phs/Snr/lnrfiles", "本年度未体检": "http://192.168.0.203:30080/phs/Snr/unexamined", "老年人中医体质辨识": "http://192.168.0.203:30080/phs/Snr/chMedicine", "老年人自理能力评估查询": "http://192.168.0.203:30080/phs/Snr/selfCareAssess", "老年人抑郁评估查询": "http://192.168.0.203:30080/phs/Snr/depressed", "简易智力检查查询": "http://192.168.0.203:30080/phs/Snr/intelligence", "体检登记": "http://192.168.0.203:30080/phs/HealthExamination/tjregister", "体检记录": "http://192.168.0.203:30080/phs/HealthExamination/tjrecord", "未体检人员": "http://192.168.0.203:30080/phs/HealthExamination/tjunexam", "肺结核患者概况": "http://192.168.0.203:30080/phs/Tuberculosis/fjhindex", "肺结核登记": "http://192.168.0.203:30080/phs/Tuberculosis/fjhregister", "肺结核管理": "http://192.168.0.203:30080/phs/Tuberculosis/fjhfiles", "残疾人概况": "http://192.168.0.203:30080/phs/Disabled/cjrindex", "残疾人登记": "http://192.168.0.203:30080/phs/Disabled/cjrregister", "残疾人管理": "http://192.168.0.203:30080/phs/Disabled/cjrfiles", "严重精神障碍登记": "http://192.168.0.203:30080/phs/MentalDisorder/jsregister", "严重精神障碍患者": "http://192.168.0.203:30080/phs/MentalDisorder/jsfiles", "严重精神病障碍随访": "http://192.168.0.203:30080/phs/MentalDisorder/jsjob", "严重精神障碍概况": "http://192.168.0.203:30080/phs/MentalDisorder/jsindex", "健康教育活动": "http://192.168.0.203:30080/phs/HealthEducation/HealthActivity", "本年度未评": "http://192.168.0.203:30080/phs/hbp/noassessdata", "评分信息查询": "http://192.168.0.203:30080/phs/hbp/assessdata"}
Web_PO.opnLabel(d_menu_basicPHS["个人健康档案"])
Web_PO.swhLabel(1)
Web_PO.quit()


# getattr(Gw_PO, s_func + '_query')({"身份证号": "110101199001015000"})  # 查询
# getattr(Gw_PO, s_func + '_operation')('更新')
# getattr(Gw_PO, s_func + '_modify')(File_PO.jsonfile2dict(folder + "/01.json"))

# 列表页数据，匹配登录账号所在机构
# 如：10082账号所属机构（大秦家镇小杨家村卫生室，370685008001）
# select * from PHUSERS.dbo.t_ehr_info where MANAGE_ORG_CODE = (select org_sub_code from ZYCONFIG.dbo.sys_user where USER_NAME ='10082')


# todo 1 查询
# Gw_PO.phs_healthrecord_personal_query({"姓名": "李丽丽"})
# Gw_PO.phs_healthrecord_personal_query({"身份证号": "372922198510281068"})
# Gw_PO.phs_healthrecord_personal_query({"管理机构": "招远市卫健局"})
# Gw_PO.phs_healthrecord_personal_query({"管理机构": "玲珑卫生院"})
# Gw_PO.phs_healthrecord_personal_query({"管理机构": {"玲珑卫生院": "玲珑镇罗山李家村卫生室"}})
# Gw_PO.phs_healthrecord_personal_query({"姓名": "胡成", "性别": "男", "身份证号": "110101194301191302", "出生日期范围": [[2025, 1, 1], [2025, 1, 2]],"人群分类": ["残疾人","孕产妇"], "档案是否开放": "否",
#                             "档案状态": "已死亡", "血型": "不详", "年龄": [1, 5], "常住类型": "户籍", "是否签约": "是", "是否残疾": "否",
#                             "今年是否体检": "否", "既往史": ["脑卒中","高血压"], "今年体检日期": [[2025, 2, 1], [2025, 2, 2]], "今年是否已更新": "是",
#                             "今年更新日期": [[2025, 1, 3], [2025, 1, 5]], "医疗费用支付方式": "全公费", "建档日期": [[2025, 1, 1], [2025, 1, 8]], "档案缺失项目": "性别", "建档人": "ceshi",
#                             "管理机构": "招远市卫健局", "现住址": ["泉山街道", "花园社区居民委员会", "123"], "本人电话": "1382121212"})


# todo 2 导出
# Gw_PO.export("/Users/linghuchong/Desktop/healthread.xls")


# todo 3 新增
# 表：T_EHR_INFO
# Gw_PO.phs_healthrecord_personal_new({"button": "仅保存", "data": {
#     "身份证号码": Data_PO.getIdCard(),
#     "姓名": Data_PO.getChineseName(), "民族": "回族",
#     "现住址": ["上海市", "市辖区", "虹口区", "广中路街道", "商业一村居委会", "多媒体100号"],
#     "本人电话": Data_PO.getPhone(), "联系人姓名": Data_PO.getChineseName(), "联系人电话": Data_PO.getPhone(), "常住类型": "非户籍",
#     "文化程度": "专科教育", "职业": "军人", "工作单位": "上海智赢", "婚姻状况": "离婚", "血型": "不详",
#     "RH血型": "Rh阳性",
#     "医疗费用支付方式": [["全自费", {"其他": "123"}], {"城镇职工基本医疗保险": "555", "城镇居民基本医疗保险": "666", "贫困救助": "777"}],
#     "药物过敏史": ["青霉素类抗生素", "含碘药品", {"其他药物过敏源": "12345"}],
#     "暴露史": ["化学品", "不详","其他"],
#     "既往史": {"疾病": {"有": [["高血压", [2025, 1, 1]], ["冠心病", [2025, 2, 1]]]},
#               "手术": {"有": [["手术1", [2025, 1, 3]], ["手术2", [2025, 1, 4]], ["手术3", [2025, 2, 4]]]},
#               "外伤": {"有": [["外伤1", [2025, 4, 11]], ["外伤2", [2025, 5, 5]]]},
#               "输血": {"有": [["输血1", [2025, 3, 3]], ["输血2", [2025, 4, 4]]]}},
#     "家族史": {"有": [["高血压", "母亲"], ["糖尿病", "父亲"], ["脑卒中", "子女"]]},
#     "遗传病史": {"有": {"疾病名称": "帕金森"}},
#     "残疾情况": [["听力残疾", "精神残疾", {"其他残疾": "90"}], {"残疾证号": "ab123"}],
#     "家庭情况": {"与户主关系": "子", "户主姓名": Data_PO.getChineseName(), "户主身份证号": Data_PO.getIdCard(), "家庭人口数": "4", "家庭结构": "3", "居住情况": "独居"},
#     "生活环境": {"厨房排风设施": "烟囱", "燃料类型": "煤", "饮水": "井水", "厕所": "马桶", "禽畜栏": "室外"},
#     "管理机构": "招远市卫健局", "档案是否开放": "否",
#     "建档日期": [int(Time_PO.getYear()), int(Time_PO.getMonth()), int(Time_PO.getDay())]
#     }})


# '更新方式": "门诊", "更新内容": "测试三峡"
# Gw_PO.phs_healthrecord_personal_new({"button": "保存复核"})
# Gw_PO.phs_healthrecord_personal_new({"button": "取消"})



# todo 操作 - 查看
# d_ = Gw_PO.phs_healthrecord_personal_operation({"operate": " 查看 ", "option": {"身份证号": "372922198510281068"}})
# print(d_)
# Gw_PO.phs_healthrecord_personal_operation({"operate": " 查看 ", "option": {"姓名": "李丽丽", "档案编号": "37068500100100157"}})


# todo 操作 - 更新
# Gw_PO.phs_healthrecord_personal_operation({"operate": " 更新 ", "option": {"姓名": "李丽丽", "档案编号": "37068500000000047"}})
# Gw_PO.phs_healthrecord_personal_operation({"operate": " 更新 ", "operate2": "仅保存", "data": {
#     ' 姓名 ": "李四", " 性别 ": "女", " 出生日期 ": [2024, 2, 2], " 民族 ": "回族",
#     ' 现住址 ": ["上海市", "市辖区", "虹口区", "广中路街道", "商业一村居委会", "多媒体100号"],
#     ' 本人电话 ": "13815161718", " 联系人姓名 ": "令狐冲", " 联系人电话 ": "58771234", " 常住类型 ": "非户籍",
#     ' 文化程度 ": "专科教育", " 职业 ": "军人", " 工作单位 ": "上海智赢", " 婚姻状况 ": "离婚", " 血型 ": "不详",
#     ' RH血型 ": "Rh阳性",
#     ' 医疗费用支付方式 ": [["全自费", {"其他": "123"}], {"城镇职工基本医疗保险": "555", "城镇居民基本医疗保险": "666", "贫困救助": "777"}],
#     ' 药物过敏史 ": ["青霉素类抗生素", "含碘药品", {"其他药物过敏源": "12345"}],
#     ' 暴露史 ": ["化学品", "不详"],
#     ' 既往史 ": {"疾病": {"有": [["高血压", [2025, 1, 1]], ["冠心病", [2025, 2, 1]]]},
#               '手术": {"有": [["手术1", [2025, 1, 3]], ["手术2", [2025, 1, 4]], ["手术3", [2025, 2, 4]]]},
#               '外伤": {"有": [["外伤1", [2025, 4, 11]], ["外伤2", [2025, 5, 5]]]},
#               '输血": {"有": [["输血1", [2025, 3, 3]], ["输血2", [2025, 4, 4]]]}},
#     ' 家族史 ": {"有": [["高血压", "母亲"], ["高血压", "母亲"], ["脑卒中", "子女"]]},
#     ' 遗传病史 ": {"有": {"疾病名称": "帕金森"}},
#     ' 残疾情况 ": [["听力残疾", "精神残疾", {"其他残疾": "90"}], {" 残疾证号 ": "ab123"}],
#     ' 家庭情况 ": {" 与户主关系 ": "子", " 户主姓名 ": "李四2", " 户主身份证号 ": "310101198004110013", " 家庭人口数 ": "4", " 家庭结构 ": "3", " 居住情况 ": "独居"},
#     ' 厨房排风设施 ": "烟囱", " 燃料类型 ": "煤", " 饮水 ": "自来水", " 厕所 ": "马桶", " 禽畜栏 ": "无",
#     ' 管理机构 ": "招远市卫健局", " 档案是否开放 ": "否", " 建档日期 ": [2025, 1, 16],
#     ' 更新方式 ": "门诊",' 更新内容 ": "测试三峡",
#     }})

# ' 既往史 ": {"疾病": {"有": [["高血压", [2025, 1, 1]], ["冠心病", [2025, 2, 1]]]},
# ' 既往史 ": {"疾病": {"无": ""},
# ' 家族史 ": {"无": ""},
# ' 家族史 ": {"有": [["高血压", "母亲"], ["高血压", "母亲"], ["脑卒中", "子女"]]},
# ' 遗传病史 ": {"无": ""}
# ' 遗传病史 ":{"有": {"疾病名称": "帕金森"}},
# ' 管理机构 ": "招远市卫健局"
# ' 管理机构 ": "金岭镇卫生院"
# ' 管理机构 ": {"金岭镇卫生院": "金岭镇山上候家村卫生室"}


# todo 操作 - 终结
# Gw_PO.phs_healthrecord_personal_operation({"operate": " 终结 ", "option": {"姓名": "李丽丽", "档案编号": "37068500000000047"}})
# Gw_PO.phs_healthrecord_personal_operation({"operate": " 终结 ", "data": {
#     '档案状态": {"暂不管理": {"暂不管理原因": "住院", "暂不管理日期": [2025, 1, 2]}}
#     }})
# Gw_PO.phs_healthrecord_personal_operation({"operate": " 终结 ", "data": {
#     '档案状态": {"已死亡": {"档案注销日期": [2025, 1, 3], "死亡日期": [2025, 1, 3]}}
#     }})


# todo 操作 - 更新历史
# Gw_PO.phs_healthrecord_personal_operation({"operate": "更新历史", "option": {"姓名": "李丽丽", "档案编号": "37068500000000047"}})
# Gw_PO.phs_healthrecord_personal_operation({"operate": "更新历史", "data": {}
#     })


# # todo 3 姓名 (更新)
# Gw_PO.phs_healthrecord_personal_operation({"operate": "姓名", "option": {"姓名": "李丽丽", "档案编号": "37068500000000047"}})
# Gw_PO.phs_healthrecord_personal_operation({"operate": "姓名", "operate2": "更新", "data": {
#     ' 姓名 ": "李四", " 性别 ": "女", " 出生日期 ": [2024, 2, 2], " 民族 ": "回族",
#     ' 现住址 ": ["上海市", "市辖区", "虹口区", "广中路街道", "商业一村居委会", "多媒体100号"],
#     ' 本人电话 ": "13815161718", " 联系人姓名 ": "令狐冲", " 联系人电话 ": "58771234", " 常住类型 ": "非户籍",
#     ' 文化程度 ": "专科教育", " 职业 ": "军人", " 工作单位 ": "上海智赢", " 婚姻状况 ": "离婚", " 血型 ": "不详",
#     ' RH血型 ": "Rh阳性",
#     ' 医疗费用支付方式 ": [["全自费", {"其他": "123"}], {"城镇职工基本医疗保险": "555", "城镇居民基本医疗保险": "666", "贫困救助": "777"}],
#     ' 药物过敏史 ": ["青霉素类抗生素", "含碘药品", {"其他药物过敏源": "12345"}],
#     ' 暴露史 ": ["化学品", "不详"],
#     ' 既往史 ": {"疾病": {"有": [["高血压", [2025, 1, 1]], ["冠心病", [2025, 2, 1]]]},
#               '手术": {"有": [["手术1", [2025, 1, 3]], ["手术2", [2025, 1, 4]], ["手术3", [2025, 2, 4]]]},
#               '外伤": {"有": [["外伤1", [2025, 4, 11]], ["外伤2", [2025, 5, 5]]]},
#               '输血": {"有": [["输血1", [2025, 3, 3]], ["输血2", [2025, 4, 4]]]}},
#     ' 家族史 ": {"有": [["高血压", "母亲"], ["高血压", "母亲"], ["脑卒中", "子女"]]},
#     ' 遗传病史 ": {"有": {"疾病名称": "帕金森"}},
#     ' 残疾情况 ": [["听力残疾", "精神残疾", {"其他残疾": "90"}], {" 残疾证号 ": "ab123"}],
#     ' 家庭情况 ": {" 与户主关系 ": "子", " 户主姓名 ": "李四2", " 户主身份证号 ": "310101198004110013", " 家庭人口数 ": "4", " 家庭结构 ": "3", " 居住情况 ": "独居"},
#     ' 厨房排风设施 ": "烟囱", " 燃料类型 ": "煤", " 饮水 ": "自来水", " 厕所 ": "马桶", " 禽畜栏 ": "无",
#     ' 管理机构 ": "招远市卫健局", " 档案是否开放 ": "否", " 建档日期 ": [2025, 1, 16],
#     ' 更新方式 ": "门诊",' 更新内容 ": "测试三峡",
#     }})

# todo 3 姓名（获取）
# Gw_PO.phs_healthrecord_personal_operation({"operate": "姓名", "option": {"姓名": "李丽丽", "档案编号": "37068500100100157"}})
# # Gw_PO.phs_healthrecord_personal_operation({"operate": "姓名", "option": {"姓名": "陈美"}})
# d_ = Gw_PO.phs_healthrecord_personal_operation({"operate": "姓名", "operate2": "获取", "data": {}})
# print(d_)  # {"身份证号码": ["372922198510281068"], "档案编号": ["37068500100100157"], ...