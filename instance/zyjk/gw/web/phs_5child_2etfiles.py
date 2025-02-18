# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 儿童健康管理 - 儿童健康档案
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName)
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')
# 登录
Gw_PO.login(Configparser_PO.HTTP("url"), Configparser_PO.ACCOUNT("user"), Configparser_PO.ACCOUNT("password"))
# 菜单
d_menu_basicPHS = {'健康档案概况': 'http://192.168.0.203:30080/phs/HealthRecord/ehrindex', '个人健康档案': 'http://192.168.0.203:30080/phs/HealthRecord/Personal', '家庭健康档案': 'http://192.168.0.203:30080/phs/HealthRecord/Family', '迁入申请': 'http://192.168.0.203:30080/phs/HealthRecord/Immigration', '迁出审核': 'http://192.168.0.203:30080/phs/HealthRecord/Exit', '档案交接': 'http://192.168.0.203:30080/phs/HealthRecord/handoverFile', '死亡管理': 'http://192.168.0.203:30080/phs/HealthRecord/DeathManagement', '区域档案查询': 'http://192.168.0.203:30080/phs/HealthRecord/regionalFile', '接诊信息查询': 'http://192.168.0.203:30080/phs/HealthRecord/Diagnosis', '就诊管理': 'http://192.168.0.203:30080/phs/HealthRecord/Visit', '高血压专项': 'http://192.168.0.203:30080/phs/Hypertension/gxyregister', '高血压随访': 'http://192.168.0.203:30080/phs/Hypertension/gxyjob', '高血压报病': 'http://192.168.0.203:30080/phs/Hypertension/gxybb', '糖尿病专项': 'http://192.168.0.203:30080/phs/Diabetes/tnbregister', '糖尿病随访': 'http://192.168.0.203:30080/phs/Diabetes/tnbjob', '糖尿病报病': 'http://192.168.0.203:30080/phs/Diabetes/tnbbb', '慢阻肺病登记': 'http://192.168.0.203:30080/phs/Copd/register', '慢阻肺病专项': 'http://192.168.0.203:30080/phs/Copd/project', '慢阻肺病随访': 'http://192.168.0.203:30080/phs/Copd/visit', '儿童概况': 'http://192.168.0.203:30080/phs/Child/etindex', '儿童健康档案': 'http://192.168.0.203:30080/phs/Child/etfiles', '中医体质辨识列表': 'http://192.168.0.203:30080/phs/Child/tcm', '中医体质辨识汇总': 'http://192.168.0.203:30080/phs/Child/tzbs', '儿童检查记录': 'http://192.168.0.203:30080/phs/Child/etjob', '孕产妇概况': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfindex', '孕产妇登记': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfregister', '孕产妇档案': 'http://192.168.0.203:30080/phs/MaternalRecord/ycffiles', '孕产妇随访': 'http://192.168.0.203:30080/phs/MaternalRecord/ycfjob', '老年人概况': 'http://192.168.0.203:30080/phs/Snr/lnrindex', '老年人专项登记': 'http://192.168.0.203:30080/phs/Snr/special', '老年人专项管理': 'http://192.168.0.203:30080/phs/Snr/lnrfiles', '本年度未体检': 'http://192.168.0.203:30080/phs/Snr/unexamined', '老年人中医体质辨识': 'http://192.168.0.203:30080/phs/Snr/chMedicine', '老年人自理能力评估查询': 'http://192.168.0.203:30080/phs/Snr/selfCareAssess', '老年人抑郁评估查询': 'http://192.168.0.203:30080/phs/Snr/depressed', '简易智力检查查询': 'http://192.168.0.203:30080/phs/Snr/intelligence', '体检登记': 'http://192.168.0.203:30080/phs/HealthExamination/tjregister', '体检记录': 'http://192.168.0.203:30080/phs/HealthExamination/tjrecord', '未体检人员': 'http://192.168.0.203:30080/phs/HealthExamination/tjunexam', '肺结核患者概况': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhindex', '肺结核登记': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhregister', '肺结核管理': 'http://192.168.0.203:30080/phs/Tuberculosis/fjhfiles', '残疾人概况': 'http://192.168.0.203:30080/phs/Disabled/cjrindex', '残疾人登记': 'http://192.168.0.203:30080/phs/Disabled/cjrregister', '残疾人管理': 'http://192.168.0.203:30080/phs/Disabled/cjrfiles', '严重精神障碍登记': 'http://192.168.0.203:30080/phs/MentalDisorder/jsregister', '严重精神障碍患者': 'http://192.168.0.203:30080/phs/MentalDisorder/jsfiles', '严重精神病障碍随访': 'http://192.168.0.203:30080/phs/MentalDisorder/jsjob', '严重精神障碍概况': 'http://192.168.0.203:30080/phs/MentalDisorder/jsindex', '健康教育活动': 'http://192.168.0.203:30080/phs/HealthEducation/HealthActivity', '本年度未评': 'http://192.168.0.203:30080/phs/hbp/noassessdata', '评分信息查询': 'http://192.168.0.203:30080/phs/hbp/assessdata'}
varUrl = d_menu_basicPHS['儿童健康档案']
Web_PO.opnLabel(d_menu_basicPHS['儿童健康档案'])
Web_PO.swhLabel(1)


# todo 1 查询
# Gw_PO.phs_child_etfiles_query({"身份证号": "321254202501154625"})
# Gw_PO.phs_child_etfiles_query({"姓名": "胡成", "出生日期": [[2025, 1, 1], [2025, 1, 2]], "上次完成 检查类型": "新生儿", "上次 随访日期": [[2025, 1, 1], [2025, 1, 2]],
#                                "下次 随访日期": [[2025, 1, 1], [2025, 1, 2]],"母亲姓名": "yoyo", "父亲姓名": "john", "管理状态": "管理中", "管理类别": "本地管理",
#                                "月龄": "3月", "新生儿异常情况": "听力异常", "喂养方式": "人工", "是否满6周岁": "是", "身份证号 是否填写": "是", "儿童管理机构": ["招远市卫健局"],
#                                "是否仅查询机构": "是", "身份证号": "110101199001015000", "随访提醒分类": "常规管理", "出生地址": ["大秦家街道", "大秦家村民委员会", "123"],
#                                "随访日期": [[2025, 1, 3], [2025, 1, 5]], "随访医生": "张三费"})


# todo 2 导出
# Gw_PO.export("/Users/linghuchong/Desktop/44")


# todo 3 新增
# Gw_PO.phs_child_etfiles_new({"姓名": "胡成", "性别": "男", "出生日期": [2025, 1, 1],  "身份证号": '310101201501011123',
#                                "出生地址": ['山东省', '烟台市', '招远市', '泉山街道', '花园社区居民委员会','东方路444号'],
#                                "母亲姓名": "yoyo", "母亲职业": "军人", "母亲身份证号": "310101198004112345", "母亲联系电话": "02158776544",
#                                "父亲姓名": "john", "父亲职业": "专业技术人员", "父亲身份证号": "310101198004112346", "父亲联系电话": "02158776546",
#                                "家庭住址": ['山东省', '烟台市', '招远市', '辛庄镇', '小宋家村民委员会','东方路111号'], "同步出生地": "是",
#                                "管理类别": ["中途迁入管理", "4"]
#                                })



# todo 4 健康检查
Gw_PO.phs_child_etfiles_query({"身份证号": "110101202401015310"})

Gw_PO.phs_child_etfiles_operation({'operate': '健康检查', 'option': {"身份证号": "110101202401015310"}})

# 新生儿家庭访视记录表
# Gw_PO.phs_child_etfiles_operation({'operate': '健康检查', 'index': {'operate2': '新生儿家庭访视记录表'},
#                                    'value': {'本次访视时间': [2025, 2, 9],
#                                    '出生孕周': ['3', '2'], '母亲妊娠期': ['糖尿病', {'其他': '111'}],
#                                    '助产机构名称': '某机构', '出生情况': ['顺产', {'其他': '222'}], '新生儿窒息': '有', 'Apgar评分': ['有', ['1', '2', '3']],
#                                    ' 是否有畸形 ': ['有', {'畸形详细': "测试一下"}],
#                                    '新生儿听力检查': '未通过',
#                                    '新生儿疾病筛查 ': ['甲低', {'其他': '333'}],
#                                    '新生儿出生时': "6", '目前体重': '12', '出生身长': '44',
#                                    '喂养方式': '人工', '吃奶量':'123', '吃奶次数': '3',
#                                    '呕吐': '有', '大便': '其他', '大便次数': '3',
#                                    '体温': '33', '心率': '100', '呼吸频率': '13',
#                                    '面色 ': {'其他': '444'}, '黄疸部位': ['面部', '手足'],
#                                    '前囟': ['12','13', {'其他':'456'}],
#                                    ' 眼睛 ': {'异常': '11'}, ' 四肢活动度 ': {'异常': '88'},
#                                    ' 耳外观 ': {'异常': '22'}, ' 颈部包块 ': {'异常': '99'},
#                                    ' 鼻 ': {'异常': '33'}, '皮肤 ': {'其他': '3366'},
#                                    ' 口腔 ': {'异常': '44'}, ' 肛门 ': {'异常': '12'},
#                                    ' 心肺听诊 ': {'异常': '55'}, ' 胸部 ': {'异常': '23'},
#                                    ' 腹部触诊 ': {'异常': '66'}, ' 脊柱 ': {'异常': '34'},
#                                    ' 外生殖器 ': {'异常': '77'}, '脐带 ': {'其他': '66'},
#                                    '指导 ': ['发育指导', '口腔保健指导', {'其他': '666'}],
#                                    '转诊': ['有', {'原因': '121', '机构': '3232', '科室': '55', '联系人': 'cdg', '联系方式': '13312123344','结果': '到位'}],
#                                    '下次访视时间': [2025, 4, 9], '下次随访地点': 'sh',
#                                    '随访医生签名': '测试2', '家长签名': 'yyy'}})

# 1-8月龄儿童健康检查记录表
# Gw_PO.phs_child_etfiles_operation({'operate': '健康检查', 'index': {'operate2': '1-8月龄儿童健康检查记录表', 'age': '满月'},
#                                     'value': {
#                                    '转诊':['有', {'原因': '121', '机构及科室': '3232', '联系人': 'cdg', '联系方式': '13312123344','结果': '到位'}],
#                                    '下次随访日期': [2025, 5, 9],
#                                    '随访医生签名': '测试2',
#                                    '家长签名': "666"}})

Gw_PO.phs_child_etfiles_operation({'operate': '健康检查', 'index': {'operate2': '1-8月龄儿童健康检查记录表', 'age': '满月'},
                                    'value': {'随访日期': [2024, 12, 9],
                                   '本次服务类别': ['失访', {'失访原因': '4324'}], '体重(kg)': [34.12, '中'], '身长(cm)': [177.10, '上'], '头围(cm)': '56',
                                   '面色': '黄染', '皮肤': '异常', '前囟': ['未闭','12','44'], '颈部包块': '有',
                                   '眼睛': '异常', '耳': '异常', '口腔': '异常', '胸部': '异常', '腹部': '异常', '脐部': '其他', '四肢': '异常', '肛门/外生殖器': '异常',
                                   '户外活动(小时/日)': "12", '服用维生素D(IU/日)': "55",
                                   '两次随访间': {'无': ""},
                                   '指导': ['生长发育','口腔保健',{'其他':"123"}],
                                   '转诊': ['有', {'原因': '121', '机构及科室': '3232', '联系人': 'cdg', '联系方式': '13312123344','结果': '到位'}],
                                   '下次随访日期': [2025, 5, 9],
                                   '随访医生签名': '测试',
                                   '家长签名': "666"}})

Gw_PO.phs_child_etfiles_operation({'operate': '健康检查', 'index': {'operate2': '1-8月龄儿童健康检查记录表', 'age': '3月龄'},
                                    'value': {'随访日期': [2024, 12, 11],
                                   '本次服务类别': ['失访', {'失访原因': '11'}], '体重(kg)': [2.12, '中'], '身长(cm)': [17.10, '上'], '头围(cm)': '66',
                                   '面色': '黄染', '皮肤': '异常', '前囟': ['未闭','33','44'], '颈部包块': '有',
                                   '眼睛': '异常', '耳': '异常', '口腔': '异常', '胸部': '异常', '腹部': '异常', '脐部': '未见异常', '四肢': '异常',
                                   '可疑佝偻病': '多汗', '体征': '颅骨软化',
                                   '肛门/外生殖器': '异常',
                                   '户外活动(小时/日)': "56", '服用维生素D(IU/日)': "66",
                                   '两次随访间': {'肺炎':'90', '外伤':'91', '其他':"93"},
                                   '指导': ['生长发育','口腔保健',{'其他':"98"}],
                                   '转诊': ['有', {'原因': '56', '机构及科室': '57', '联系人': 'ere', '联系方式': '13312123222','结果': '到位'}],
                                   '下次随访日期': [2025, 5, 10],
                                   '随访医生签名': '7',
                                   '家长签名': "666"}})
















# todo 3 更新
# Gw_PO.phs_healthrecord_personal_modify()
# getattr(Gw_PO, s_func + '_query')({"身份证号": "110101199001015000"})  # 查询
# getattr(Gw_PO, s_func + '_operation')('更新')
# getattr(Gw_PO, s_func + '_modify')(File_PO.jsonfile2dict(folder + "/01.json"))
# getattr(Gw_PO, s_func + '_modify')({' 与户主关系 ': '子', ' 性别 ': "女", ' 民族 ': "回族", ' 文化程度 ': "专科教育", ' 职业 ': "军人", ' 婚姻状况 ': "离婚", ' 档案是否开放 ': "否",
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
#                                              '输血': 'remain'}})

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


# todo 4 终结
# getattr(Gw_PO, s_func + '_query')({"身份证号": "110101199001015000"})  # 查询
# getattr(Gw_PO, s_func + '_operation')(['终结', {'暂不管理': {'暂不管理原因': '住院', '暂不管理日期': [2025, 1, 2]}}])
# getattr(Gw_PO, s_func + '_operation')(['终结', {'已死亡': {'档案注销日期': [2025, 1, 3], '死亡日期': [2025, 1, 3]}}])


# todo 5 更新历史
# getattr(Gw_PO, s_func + '_operation')('更新历史')


