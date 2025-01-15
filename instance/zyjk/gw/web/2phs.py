# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-12-19
# Description: 公卫 - 基本公卫
# *****************************************************************

from GwPO import *
Gw_PO = GwPO("./2phs.log")


# 1，登录
Gw_PO.login('http://192.168.0.203:30080/#/login', '11011', 'HHkk2327447')

# 获取基本公卫二级菜单连接
Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li[2]", 2)  # 点击一级菜单基本公卫
d_menu_jbgw = Gw_PO.getMenu2Url()
print('基本公卫 =>', d_menu_jbgw)
Gw_PO.logger.info(d_menu_jbgw)


# 基本公卫 => {'健康档案概况': 'http://192.168.0.203:30080/phs/HealthRecord/ehrindex', '个人健康档案': 'http://192.168.0.203:30080/phs/HealthRecord/Personal', '家庭健康档案': 'http://192.168.0.203:30080/phs/HealthRecord/Family', '迁入申请': 'http://192.168.0.203:30080/phs/HealthRecord/Immigration', '迁出审核': 'http://192.168.0.203:30080/phs/HealthRecord/Exit', '档案交接': 'http://192.168.0.203:30080/phs/HealthRecord/handoverFile', '死亡管理': 'http://192.168.0.203:30080/phs/HealthRecord/DeathManagement', '区域档案查询': 'http://192.168.0.203:30080/phs/HealthRecord/regionalFile', '接诊信息查询': 'http://192.168.0.203:30080/phs/HealthRecord/Diagnosis', '就诊管理': 'http://192.168.0.203:30080/phs/HealthRecord/Visit', '高血压专项': 'http://192.168.0.203:30080/phs/Hypertension/gxyregister', '高血压随访': 'http://192.168.0.203:30080/phs/Hypertension/gxyjob', '高血压报病': 'http://192.168.0.203:30080/phs/Hypertension/gxybb', '糖尿病专项': 'http://192.168.0.203:30080/phs/Diabetes/tnbregister', '糖尿病随访': 'http://192.168.0.203:30080/phs/Diabetes/tnbjob', '糖尿病报病': 'http://192.168.0.203:30080/phs/Diabetes/tnbbb', '慢阻肺病登记': 'http://192.168.0.203:30080/phs/Copd/register', '慢阻肺病专项': 'http://192.168.0.203:30080/phs/Copd/project', '慢阻肺病随访': 'http://192.168.0.203:30080/phs/Copd/visit', '儿童概况': 'http://192.168.0.203:30080/phs/Child/etindex', '儿童健康档案': 'http://192.168.0.203:30080/phs/Child/etfiles', '中医体质辨识列表': 'http://192.168.0.203:30080/phs/Child/tcm', '中医体质辨识汇总': 'http://192.168.0.203:30080/phs/Child/tzbs', '儿童检查记录': 'http://192.168.0.203:30080/phs/Child/etjob', '孕产妇概况': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfindex', '孕产妇登记': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfregister', '孕产妇档案': 'http://192.168.0.203:30080/phs/MaternalRecord/ycffiles', '孕产妇随访': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfjob', '老年人概况': 'http://192.168.0.203:30080/phs/Snr/lnrindex', '老年人专项登记': 'http://192.168.0.203:30080/phs/Snr/special', '老年人专项管理': 'http://192.168.0.203:30080/phs/Snr/lnrfiles', '本年度未体检': 'http://192.168.0.203:30080/phs/Snr/unexamined', '老年人中医体质辨识': 'http://192.168.0.203:30080/phs/Snr/chMedicine', '老年人自理能力评估查询': 'http://192.168.0.203:30080/phs/Snr/selfCareAssess', '老年人抑郁评估查询': 'http://192.168.0.203:30080/phs/Snr/depressed', '简易智力检查查询': 'http://192.168.0.203:30080/phs/Snr/intelligence', '体检登记': 'http://192.168.0.203:30080/phs/HealthExamination/tjregister', '体检记录': 'http://192.168.0.203:30080/phs/HealthExamination/tjrecord', '未体检人员': 'http://192.168.0.203:30080/phs/HealthExamination/tjunexam', '肺结核患者概况': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhindex', '肺结核登记': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhregister', '肺结核管理': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhfiles', '残疾人概况': 'http://192.168.0.203:30080/phs/Disabled/cjrindex', '残疾人登记': 'http://192.168.0.203:30080/phs/Disabled/cjrregister', '残疾人管理': 'http://192.168.0.203:30080/phs/Disabled/cjrfiles', '严重精神障碍登记': 'http://192.168.0.203:30080/phs/MentalDisorder/jsregister', '严重精神障碍患者': 'http://192.168.0.203:30080/phs/MentalDisorder/jsfiles', '严重精神病障碍随访': 'http://192.168.0.203:30080/phs/MentalDisorder/jsjob', '严重精神障碍概况': 'http://192.168.0.203:30080/phs/MentalDisorder/jsindex', '健康教育活动': 'http://192.168.0.203:30080/phs/HealthEducation/HealthActivity', '本年度未评': 'http://192.168.0.203:30080/phs/hbp/noassessdata', '评分信息查询': 'http://192.168.0.203:30080/phs/hbp/assessdata'}

# 删除之前请求信息
# Web_PO.delRequests()

# # 获取当前页面除以下之外的所有请求地址
# Web_PO.requestsExcept(['.js','.css','.png','.ico'])

# # 健康档案概况解码参数
# encrypt_data = (Web_PO.requests('/tEhrInfo/getEhrHomeInfo?0='))
# print('/tEhrInfo/getEhrHomeInfo?0=' + Gw_PO.decrypt(encrypt_data))  # /tEhrInfo/getEhrHomeInfo?0={"orgCode":""}


# # 2.1.1, 请选择
# # Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[1]/div/div/input", 2)
# # Web_PO.clkByX("/html/body/div[2]/div[2]/div/div/div[1]/ul/li/label", 2)
# # Web_PO.clkByX("/html/body/div[2]/div[2]/div/div[2]/div[1]/ul/li[3]/label", 2)
# # Web_PO.clkByX("/html/body/div[2]/div[2]/div/div[3]/div[1]/ul/li/label", 2)
# # Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[1]", 2)
# Web_PO.cls()
# Web_PO.swhLabel(0)

# todo 1 基本公卫

# # todo 1.1, 健康档案管理 - 健康档案概况
# Web_PO.opnLabel(d_menu_jbgw['健康档案概况'])
# Web_PO.swhLabel(1)

# todo 1.2, 健康档案管理 - 个人健康档案
# Web_PO.opnLabel(d_menu_jbgw['个人健康档案'])
# Web_PO.swhLabel(1)
# 列表页数据，匹配登录账号所在机构
# 如：10082账号所属机构（大秦家镇小杨家村卫生室，370685008001）
# select * from PHUSERS.dbo.t_ehr_info where MANAGE_ORG_CODE = (select org_sub_code from ZYCONFIG.dbo.sys_user where USER_NAME ='10082')

# 1.2.1 查询，返回一条结果，姓名的链接
# varUrl = Gw_PO.personalHealthRecord_s({"姓名": "胡成", "性别": "男", "身份证号": "230202194504020016", "出生日期范围": [[2025,1,1], [2027,3,1]],"人群分类":["残疾人","孕产妇"],"档案是否开放":"否",
#                             "档案状态":"已死亡","血型":"不详","年龄":[1,5],"常住类型":"户籍","是否签约":"是","是否残疾":"否",
#                             "今年是否体检":"否","既往史":["脑卒中"],"今年体检日期":[[2025,2,1], [2027,4,1]],"今年是否已更新":"是",
#                             "今年更新日期":[[2025,5,1], [2027,5,5]],"医疗费用支付方式":"全公费","建档日期":[[2025,6,1], [2027,7,5]],"档案缺失项目":"性别","建档人":"ceshi",
#                             "管理机构":["招远市卫健局"],"现住址":["泉山街道", "花园社区居民委员会", "123"],"本人电话":"1382121212"})
# varUrl = Gw_PO.personalHealthRecord_s({"姓名": "胡成", "性别": "男", "身份证号": "230202194504020016", "出生日期范围": [[2025,1,1], [2027,3,1]],"人群分类":"残疾人","档案是否开放":"否",
#                             "档案状态":"已死亡","血型":"不详","年龄":[1,5],"常住类型":"户籍","是否签约":"是","是否残疾":"否",
#                             "今年是否体检":"否","既往史":"脑卒中","今年体检日期":[[2025,2,1], [2027,4,1]],"今年是否已更新":"是",
#                             "今年更新日期":[[2025,5,1], [2027,5,5]],"医疗费用支付方式":"全公费","建档日期":[[2025,6,1], [2027,7,5]],"档案缺失项目":"性别","建档人":"ceshi",
#                             "管理机构":["玲珑卫生院"],"现住址":["泉山街道", "花园社区居民委员会","123"],"本人电话":"1382121212"})
# varUrl = Gw_PO.personalHealthRecord_s({"身份证号": "110107199001016298"})
#
# # 1.2.1 姓名 - 居民健康档案
# Gw_PO.personalHealthRecord_operation('姓名')
# d_info = Gw_PO.personalHealthRecord_info()
# print(d_info)

# 1.2.2 查看 - 居民健康档案
# Gw_PO.personalHealthRecord_operation('查看')
# d_info = Gw_PO.personalHealthRecord_check()
# print(d_info)


# 1.2.3 更新 - 居民健康档案
# Gw_PO.personalHealthRecord_operation('更新')
# Gw_PO.personalHealthRecord_update({' 与户主关系 ': '子', ' 性别 ': "女", ' 民族 ': "回族", ' 文化程度 ': "专科教育", ' 职业 ': "军人", ' 婚姻状况 ': "离婚", ' 档案是否开放 ': "否",
#                                    ' 户主姓名 ': "李四2", ' 户主身份证号 ': "310101198004110013", ' 家庭人口数 ': "4", ' 家庭结构 ': "3", ' 居住情况 ': '独居',
#                                    ' 姓名 ': "李四", ' 本人电话 ': "13815161718", ' 联系人姓名 ': "令狐冲", ' 联系人电话 ': "58771234", ' 工作单位 ': "上海智赢", ' 残疾证号 ': 'ab123', ' 更新内容 ': "测试三峡",
#                                    ' 出生日期 ': [1946, 2, 2], ' 建档日期 ': [2025, 1, 16],
#                                    ' 常住类型 ': '非户籍', ' 血型 ': '不详', ' RH血型 ': 'Rh阳性', ' 更新方式 ': '门诊',
#                                    ' 厨房排风设施 ': '烟囱', ' 燃料类型 ': '煤', ' 饮水 ': '自来水', ' 厕所 ': '马桶', ' 禽畜栏 ': '无',
#                                    ' 管理机构 ': ["金岭镇卫生院", "金岭镇山上候家村卫生室"],
#                                    ' 现住址 ': ["上海市", "市辖区", "虹口区", "广中路街道", "商业一村居委会", "多媒体100号"],
#                                    ' 药物过敏史 ': ['青霉素类抗生素', '含碘药品', ['其他药物过敏源', "12345"]],
#                                    ' 暴露史 ': ['化学品', '不详'],
#                                    ' 医疗费用支付方式 ':[['城镇职工基本医疗保险','555'], ['城镇居民基本医疗保险', '666'], ['贫困救助',"777"],'全自费', ['其他','123']],
#                                    ' 残疾情况 ': ['听力残疾', '精神残疾', ['其他残疾', "90"]],
#                                    ' 遗传病史 ': ['有', '帕金森'],
#                                    ' 家族史 ': ['有', ['高血压', '母亲']],
#                                    ' 既往史 ': {'疾病': [['高血压',[2025, 1, 1]]],
#                                              '手术': [['手术1',[2025, 1, 3]], ['手术2', [2025, 1, 4]]],
#                                              '外伤': 'clear',
#                                              '输血': 'remain'} })

# ' 既往史 ': {'疾病': '无'}
# ' 既往史 ': {'疾病': [['高血压',[2025,2,12]],['糖尿病',[2025,3,14]]]}
# ' 既往史 ': {'疾病': [['高血压',[2025, 1, 1]], ['糖尿病', [2025, 1, 2]]],
#                                              '手术': [['手术1',[2025, 1, 3]], ['手术2', [2025, 1, 4]]],
#                                              '外伤': [['外伤1',[2025, 1, 5]], ['外伤2', [2025, 1, 6]]],
#                                              '输血': [['输血1',[2025, 1, 7]]]}
# ' 既往史 ': {'疾病': 'remain',
#                                              '手术': [['手术1',[2025, 1, 3]], ['手术2', [2025, 1, 4]], ['手术3', [2025, 1, 5]]],
#                                              '外伤': [['外伤1',[2025, 1, 5]], ['外伤2', [2025, 1, 6]]],
#                                              '输血': [['输血1',[2025, 1, 7]]]}
# ' 遗传病史 ': '无'
# ' 遗传病史 ':['有', '帕金森']
# ' 家族史 ': '无'
# ' 家族史 ': ['有', ['高血压', '母亲', '糖尿病', '父亲']]

# ' 管理机构 ': ["招远市卫健局"]
# ' 管理机构 ': ["金岭镇卫生院"]
# ' 管理机构 ': ["金岭镇卫生院", "金岭镇山上候家村卫生室"]


# 1.2.3 终结 - 居民健康档案
# Gw_PO.personalHealthRecord_operation(['终结', {'暂不管理': ['住院', [2025,1,2]]}])
# Gw_PO.personalHealthRecord_operation(['终结', {'已死亡': [[2025,1,3], [2025,1,1]]}])

# 1.2.4 更新历史 - 居民健康档案
# Gw_PO.personalHealthRecord_operation('更新历史')


# Gw_PO.personalHealthRecord_s({"人群分类":["残疾人", "孕产妇"],"既往史":["脑卒中"],"本人电话":"1382121212"})
# Gw_PO.personalHealthRecord_s({"姓名": "胡成", "性别": "男", "身份证号": "230202194504020016", "出生日期范围": [[2025,1,1], [2027,3,1]],"人群分类":"残疾人","档案是否开放":"否",
#                             "档案状态":"已死亡","血型":"不详","年龄":[1,5],"常住类型":"户籍","是否签约":"是","是否残疾":"否",
#                             "今年是否体检":"否","既往史":"脑卒中","今年体检日期":[[2025,2,1], [2027,4,1]],"今年是否已更新":"是",
#                             "今年更新日期":[[2025,5,1], [2027,5,5]],"医疗费用支付方式":"全公费","建档日期":[[2025,6,1], [2027,7,5]],"档案缺失项目":"性别","建档人":"ceshi",
#                             "管理机构":["玲珑卫生院", "玲珑镇大蒋家村卫生室"],"现住址":["泉山街道", "花园社区居民委员会","123"],"本人电话":"1382121212"})
# # # 已建专项
# Gw_PO.yjzx('高血压专项','专项登记')
# # Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div[2]", 2)  # 随访记录
# # # 高血压随访记录
# # l_div = Web_PO.getTextListByX("//td/div")
# # l_div = List_PO.dels(l_div, '')
# # l_div = List_PO.dels(l_div, '详情\n编辑\n删除')
# # print(l_div) # ['刘斌龙卫健委', '111 mmHg', '11 mmHg', '门诊', '2024-06-26', '控制满意', '2024-09-24', '公卫随访']
# Gw_PO.yjzx('糖尿病专项','专项登记')
# # Gw_PO.yjzx('高血脂专项','专项登记')

# # todo 1.3, 健康档案管理 - 家庭健康档案
# Web_PO.opnLabel(d_menu_jbgw['家庭健康档案'])
# Web_PO.swhLabel(3)
# # # 获取列表中用户的居民健康档案
# # # Gw_PO.runUser('all')
# # Gw_PO.runUser('测试')
# # # Gw_PO.runUser('黎明', '测试')
#
# # todo 1.4, 健康档案管理 - 迁入申请
# Web_PO.opnLabel(d_menu_jbgw['迁入申请'])
# Web_PO.swhLabel(3)
#
# # todo 1.5, 健康档案管理 - 迁出审核
# Web_PO.opnLabel(d_menu_jbgw['迁出审核'])
# Web_PO.swhLabel(3)
#
# # todo 1.6, 健康档案管理 - 档案交接
# Web_PO.opnLabel(d_menu_jbgw['档案交接'])
# Web_PO.swhLabel(3)
#
# # todo 1.7, 健康档案管理 - 死亡管理
Web_PO.opnLabel(d_menu_jbgw['死亡管理'])
Web_PO.swhLabel(1)
Gw_PO.death_s({"身份证号": "110101193801014594"})



# # 死亡管理 - 孙竹华
# Gw_PO.residentHealthRecord_update('孙竹华', 'http://192.168.0.203:30080/#/phs/personalAddOrUpdate/healthDetail?id=132')

# # todo 1.8, 健康档案管理 - 区域档案查询
# Web_PO.opnLabel(d_menu_jbgw['区域档案查询'])
# Web_PO.swhLabel(3)
#
# # todo 1.9, 健康档案管理 - 接诊信息查询
# Web_PO.opnLabel(d_menu_jbgw['接诊信息查询'])
# Web_PO.swhLabel(3)
#
# # todo 1.10, 健康档案管理 - 就诊管理
# Web_PO.opnLabel(d_menu_jbgw['就诊管理'])
# Web_PO.swhLabel(3)


# # todo 2.1, 高血压管理 - 高血压专项
# Web_PO.opnLabel(d_menu_jbgw['高血压专项'])
# Web_PO.swhLabel(3)
#
# # todo 2.2, 高血压管理 - 高血压随访
# Web_PO.opnLabel(d_menu_jbgw['高血压随访'])
# Web_PO.swhLabel(3)


# # todo 3.1, 糖尿病管理 - 糖尿病专项
# Web_PO.opnLabel(d_menu_jbgw['糖尿病专项'])
# Web_PO.swhLabel(3)
#
# # todo 3.2, 糖尿病管理 - 糖尿病随访
# Web_PO.opnLabel(d_menu_jbgw['糖尿病随访'])
# Web_PO.swhLabel(3)


# # todo 4.1, 慢性阻塞性肺病管理 - 慢阻肺病登记
# Web_PO.opnLabel(d_menu_jbgw['慢阻肺病登记'])
# Web_PO.swhLabel(3)
#
# # todo 4.2, 慢性阻塞性肺病管理 - 慢阻肺病专项
# Web_PO.opnLabel(d_menu_jbgw['慢阻肺病专项'])
# Web_PO.swhLabel(3)

# # todo 4.3, 慢性阻塞性肺病管理 - 慢阻肺病随访
# Web_PO.opnLabel(d_menu_jbgw['慢阻肺病随访'])
# Web_PO.swhLabel(3)



# # todo 5.1, 儿童健康管理 - 儿童概况
# Web_PO.opnLabel(d_menu_jbgw['儿童概况'])
# Web_PO.swhLabel(3)
#
# # todo 5.2, 儿童健康管理 - 儿童健康档案
# Web_PO.opnLabel(d_menu_jbgw['儿童健康档案'])
# Web_PO.swhLabel(3)

# # todo 5.3, 儿童健康管理 - 中医体质辨识列表
# Web_PO.opnLabel(d_menu_jbgw['中医体质辨识列表'])
# Web_PO.swhLabel(3)

# # todo 5.4, 儿童健康管理 - 中医体质辨识汇总
# Web_PO.opnLabel(d_menu_jbgw['中医体质辨识汇总'])
# Web_PO.swhLabel(3)
#
# # todo 4.5, 儿童健康管理 - 儿童检查记录
# Web_PO.opnLabel(d_menu_jbgw['儿童检查记录'])
# Web_PO.swhLabel(3)



# # todo 6.1, 孕产妇管理 - 孕产妇概况
# Web_PO.opnLabel(d_menu_jbgw['孕产妇概况'])
# Web_PO.swhLabel(3)
#
# # todo 6.2, 孕产妇管理 - 孕产妇登记
# Web_PO.opnLabel(d_menu_jbgw['孕产妇登记'])
# Web_PO.swhLabel(3)

# # todo 6.3, 孕产妇管理 - 孕产妇档案
# Web_PO.opnLabel(d_menu_jbgw['孕产妇档案'])
# Web_PO.swhLabel(3)

# # todo 6.4, 孕产妇管理 - 孕产妇随访
# Web_PO.opnLabel(d_menu_jbgw['孕产妇随访'])
# Web_PO.swhLabel(3)



# # todo 7.1, 老年人健康管理 - 老年人概况
# Web_PO.opnLabel(d_menu_jbgw['老年人概况'])
# Web_PO.swhLabel(3)
#
# # todo 7.2, 老年人健康管理 - 老年人专项登记
# Web_PO.opnLabel(d_menu_jbgw['老年人专项登记'])
# Web_PO.swhLabel(3)

# # todo 7.3, 老年人健康管理 - 老年人专项管理
# Web_PO.opnLabel(d_menu_jbgw['老年人专项管理'])
# Web_PO.swhLabel(3)

# # todo 7.4, 老年人健康管理 - 本年度未体检
# Web_PO.opnLabel(d_menu_jbgw['本年度未体检'])
# Web_PO.swhLabel(3)

# # todo 7.5, 老年人健康管理 - 老年人中医体质辨识
# Web_PO.opnLabel(d_menu_jbgw['老年人中医体质辨识'])
# Web_PO.swhLabel(3)
#
# # todo 7.6, 老年人健康管理 - 老年人自理能力评估查询
# Web_PO.opnLabel(d_menu_jbgw['老年人自理能力评估查询'])
# Web_PO.swhLabel(3)

# # todo 7.7, 老年人健康管理 - 老年人抑郁评估查询
# Web_PO.opnLabel(d_menu_jbgw['老年人抑郁评估查询'])
# Web_PO.swhLabel(3)

# # todo 7.8, 老年人健康管理 - 简易智力检查查询
# Web_PO.opnLabel(d_menu_jbgw['简易智力检查查询'])
# Web_PO.swhLabel(3)



# # todo 8.1, 健康体检 - 体检登记
# Web_PO.opnLabel(d_menu_jbgw['体检登记'])
# Web_PO.swhLabel(3)

# # todo 8.2, 健康体检 - 体检记录
# Web_PO.opnLabel(d_menu_jbgw['体检记录'])
# Web_PO.swhLabel(3)

# # todo 8.3, 健康体检 - 未体检人员
# Web_PO.opnLabel(d_menu_jbgw['未体检人员'])
# Web_PO.swhLabel(3)



# # todo 9.1, 肺结核患者管理 - 肺结核患者概况
# Web_PO.opnLabel(d_menu_jbgw['肺结核患者概况'])
# Web_PO.swhLabel(3)

# # todo 9.2, 肺结核患者管理 - 肺结核登记
# Web_PO.opnLabel(d_menu_jbgw['肺结核登记'])
# Web_PO.swhLabel(3)

# # todo 9.3, 肺结核患者管理 - 肺结核管理
# Web_PO.opnLabel(d_menu_jbgw['肺结核管理'])
# Web_PO.swhLabel(3)



# # todo 10.1, 残疾人健康管理 - 残疾人概况
# Web_PO.opnLabel(d_menu_jbgw['残疾人概况'])
# Web_PO.swhLabel(3)

# # todo 10.2, 残疾人健康管理 - 残疾人登记
# Web_PO.opnLabel(d_menu_jbgw['残疾人登记'])
# Web_PO.swhLabel(3)

# # todo 10.3, 残疾人健康管理 - 残疾人管理
# Web_PO.opnLabel(d_menu_jbgw['残疾人管理'])
# Web_PO.swhLabel(3)



# # todo 11.1, 严重精神障碍健康管理 - 严重精神障碍登记
# Web_PO.opnLabel(d_menu_jbgw['严重精神障碍登记'])
# Web_PO.swhLabel(3)

# # todo 11.2, 严重精神障碍健康管理 - 严重精神障碍患者
# Web_PO.opnLabel(d_menu_jbgw['严重精神障碍患者'])
# Web_PO.swhLabel(3)

# # todo 11.3, 严重精神障碍健康管理 - 严重精神障碍随访
# Web_PO.opnLabel(d_menu_jbgw['严重精神障碍随访'])
# Web_PO.swhLabel(3)

# # todo 11.4, 严重精神障碍健康管理 - 严重精神障碍概况
# Web_PO.opnLabel(d_menu_jbgw['严重精神障碍概况'])
# Web_PO.swhLabel(3)



# # todo 12.1, 健康教育 - 健康教育活动
# Web_PO.opnLabel(d_menu_jbgw['健康教育活动'])
# Web_PO.swhLabel(3)



# # todo 13.1, 健康行为积分 - 本年度未评
# Web_PO.opnLabel(d_menu_jbgw['本年度未评'])
# Web_PO.swhLabel(3)

# # todo 13.2, 健康行为积分 - 评分信息查询
# Web_PO.opnLabel(d_menu_jbgw['评分信息查询'])
# Web_PO.swhLabel(3)



# 孕产妇，第一次产前随访服务记录表
# Gw_PO.pregnantWoman('孕产妇', 'http://192.168.0.203:30080/phs/Snr/lnrindex#/phs/personal/detail?data=321&type=0&cardType=2&ID=1092&routeType=2')

# 健康体检(未处理)
# Gw_PO.physicalExamination('刘斌龙1', 'http://192.168.0.203:30080/phs/MentalDisorder/jsindex#/phs/examDetailsForm?RowId=202&ID=79&type=detail&pageType=record&tagType=detail')

# # 肺结核专项 （基本公卫 - 家庭健康档案 - 领跑）
# Gw_PO.phthisisVisit('零跑',"http://192.168.0.203:30080/#/phs/Tuberculosis/tuberculosisTableForm?id=148&isNav=true")
# 已建肺结核专项(正确)
# Gw_PO.phthisisVisit('零跑', "http://192.168.0.203:30080/#/phs/Tuberculosis/firstVisit?id=148&idCard=110117199001013970&page=1&isNav=1")

# # 严重精神障碍健康管理，严重精神障碍患者个人信息补充表
# Gw_PO.hypophrenia('陈平安', "http://192.168.0.203:30080/#/phs/MentalDisorder/FollowUpRecord?ehrId=111&ehrNum=37068500100200002")


# span = Web_PO.getTextListByX("//label/span")
# print(span)
# Web_PO.cls()
# Web_PO.swhLabel(0)




# # 三高共管菜单连接
# Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[2]/ul/li[3]", 2)
# d_menu2Url = Gw_PO.getMenu2Url()
# print(d_menu2Url)
#
# # 家医签约菜单连接
# Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[2]/ul/li[4]", 2)
# d_menu2Url = Gw_PO.getMenu2Url()
# print(d_menu2Url)
#
# # 统计报表菜单连接
# Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[2]/ul/li[5]", 2)
# d_menu2Url = Gw_PO.getMenu2Url()
# print(d_menu2Url)
#
# # 系统配置菜单连接
# Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[2]/ul/li[6]", 2)
# d_menu2Url = Gw_PO.getMenu2Url()
# print(d_menu2Url)

# # 数据维护菜单连接
# Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[2]/ul/li[7]", 2)
# d_menu2Url = Gw_PO.getMenu2Url()
# print(d_menu2Url)





# # 2.1 点击一级菜单
# Gw_PO.menu1('首页')
# Gw_PO.menu1('基本公卫')
# Gw_PO.menu1('三高共管')
# Gw_PO.menu1('家庭签约')
# Gw_PO.menu1('统计报表')
# Gw_PO.menu1('系统配置')
# Gw_PO.menu1('系统配置')


#
# # # 2.2 获取二级菜单字典
# d_menu2 = Gw_PO.menu2(d_menu1, '基本公卫')
# print(d_menu2)  # {'健康档案管理': 1, '儿童健康管理': 2, '孕产妇管理': 3, '老年人健康管理': 4, '肺结核患者管理': 5, '残疾人健康管理': 6, '严重精神障碍健康管理': 7, '健康教育': 8, '高血压管理': 9, '糖尿病管理': 10, '首页': 11, '基本公卫': 12, '三高共管六病同防': 13, '系统配置': 14, '社区管理': 15, '报表': 16, '更多菜单': 17}
# #
# # # # 2.3, 进入三级菜单
# # Gw_PO.menu3(d_menu2, "高血压管理", "高血压随访")
# # Web_PO.setTextById("name", "金浩")
# # Web_PO.clk("//button[@type='button']", 1)
# #
# Gw_PO.menu3(d_menu2, "高血压管理", "高血压专项")
# # 姓名
# Web_PO.setTextById("name", "令狐冲")
# # 身份证号
# Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[1]/div[2]/div/div/div/input', "310101198004110014")
# # 上次随访日期
# Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[1]/div[3]/div/div/div[1]/input', '2023-12-12')
# Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[1]/div[3]/div/div/div[2]/input', '2023-12-13')
# # 高血压危险分层
# Web_PO.jsReadonly('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[2]/div[4]/div/div/div/div/div/input')
# Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[2]/div[4]/div/div/div/div/div/input', '高危险')
# # 是否终止管理
# Web_PO.jsReadonly('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[1]/div/div/div/div/div/input')
# Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[1]/div/div/div/div/div/input', '否')
# # 随访提醒分类
# Web_PO.jsReadonly('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[4]/div/div/div/div/div/input')
# Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[4]/div/div/div/div/div/input','常规管理')
# Web_PO.clk("//button[@type='button']", 1)
# # 查询
# Web_PO.clk('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[5]/div/button[1]', 1)
# # 导出
# Web_PO.clk('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div[3]/div[5]/div/button[2]', 1)

#
# Gw_PO.menu3(d_menu2, "糖尿病管理", "糖尿病报病")
# Web_PO.setText('//*[@id="app"]/div/div[3]/section/div/main/div[1]/form/div/div[1]/div/div/div/input', 'yoyo')  # 姓名
# Web_PO.clk("//button[@type='button']", 1)


# d_menu2 = Gw_PO.menu2(d_menu1, '系统配置')
# Gw_PO.menu3(d_menu2, "机构管理", "医院维护")
# 1, 新增医疗机构
# Gw_PO.newMedicalInstitution('lhc的诊所', '12345678', '555555', '三级', '令狐冲', '浦东南路1000号', '13816109050', '上海知名急救诊所\n专治疑难杂病')

# 2, 编辑医疗机构
# Gw_PO.editMedicalInstitution('lhc的诊所', 'lhc的诊所1', '123456781', '5555551', '二级', '令狐冲1', '浦东南路1000号1', '13816109051', '上海知名急救诊所\n专治疑难杂病1')

# 3，科室维护
# Gw_PO.editOffice('lhc的诊所1', {'儿科': '122233', '妇科': '665544', '骨科': '565656'})

# d_menu2 = Gw_PO.menu2(d_menu1, '系统配置')
# Gw_PO.menu3(d_menu2, "用户管理", "用户维护")


