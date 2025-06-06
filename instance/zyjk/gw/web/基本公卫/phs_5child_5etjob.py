# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-19
# Description: 基本公卫 - 儿童健康管理 - 儿童检查记录
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName, '儿童检查记录')


# todo 1 查询
# Gw_PO.phs_child_etjob_query({"身份证号": "110101202401015310"})
# Gw_PO.phs_child_etjob_query({"儿童管理机构": "招远市卫健局", "是否仅查询机构": "是", "姓名": "胡成", "身份证号": "110101202401015310", "登记日期": [[2025, 1, 1], [2025, 1, 2]],
#                              "检查类型": ["3岁", '6月龄'], "随访日期": [[2025, 1, 3], [2025, 1, 5]], "下次随访日期": [[2025, 3, 2], [2025, 3, 4]],
#                            "出生日期": [[2022, 1, 3], [2022, 1, 5]], "血红蛋白": ['2', '3'], "随访医生": "张三"})


# todo 2 导出
# Gw_PO.export("/Users/linghuchong/Desktop/phs_child_etjob.xls")



# todo 3 编辑
Gw_PO.phs_child_etjob_query({"身份证号": "110101202401015310"})
# Gw_PO.phs_child_etjob_operation({'operate': '编辑', 'option': {"身份证号": "110101202401015310"}})

# todo 4.1 新生儿家庭访视记录表
# Gw_PO.phs_child_etjob_operation({'operate': '编辑', 'title': '新生儿家庭访视记录表', 'data': {
#     '新生儿': {
#     '本次访视时间': [2025, 2, 9], '出生孕周': ['3', '2'], '母亲妊娠期': ['糖尿病', {'其他': '111'}],
#     '助产机构名称': '某机构', '出生情况': ['顺产', {'其他': '222'}], '新生儿窒息': '有', 'Apgar评分': ['有', ['1', '2', '3']],
#     ' 是否有畸形 ': ['有', {'畸形详细': "测试一下"}], '新生儿听力检查': '未通过', '新生儿疾病筛查 ': ['甲低', {'其他': '333'}],
#     '新生儿出生时': "6", '目前体重': '12', '出生身长': '44', '喂养方式': '人工', '吃奶量':'123', '吃奶次数': '3',
#     '呕吐': '有', '大便': '其他', '大便次数': '3', '体温': '33', '心率': '100', '呼吸频率': '13',
#     '面色 ': {'其他': '444'}, '黄疸部位': ['面部', '手足'], '前囟': ['12','13', {'其他':'456'}],
#     ' 眼睛 ': {'异常': '11'}, ' 四肢活动度 ': {'异常': '88'}, ' 耳外观 ': {'异常': '22'}, ' 颈部包块 ': {'异常': '99'},
#     ' 鼻 ': {'异常': '33'}, '皮肤 ': {'其他': '3366'}, ' 口腔 ': {'异常': '44'}, ' 肛门 ': {'异常': '12'},
#     ' 心肺听诊 ': {'异常': '55'}, ' 胸部 ': {'异常': '23'}, ' 腹部触诊 ': {'异常': '66'}, ' 脊柱 ': {'异常': '34'},
#     ' 外生殖器 ': {'异常': '77'}, '脐带 ': {'其他': '66'}, '指导 ': ['发育指导', '口腔保健指导', {'其他': '666'}],
#     '转诊': ['有', {'原因': '121', '机构': '3232', '科室': '55', '联系人': 'cdg', '联系方式': '13312123344','结果': '到位'}],
#     '下次访视时间': [2025, 4, 9], '下次随访地点': 'sh', '随访医生签名': '测试2', '家长签名': 'yyy'}
# }})

# # todo 4.2 1-8月龄儿童健康检查记录表
# Gw_PO.phs_child_etjob_operation({'operate': '编辑', 'title': '1-8月龄儿童健康检查记录表', 'data': {
#     '满月': {'随访日期': [2024, 1, 1], '本次服务类别': ['随访'], '体重(kg)': [10.11, '上'], '身长(cm)': [20.22, '中'], '头围(cm)': '30',
#         '面色': '红润', '皮肤': '异常', '前囟': ['未闭', '10', '11'], '颈部包块': '有', '眼睛': '异常', '耳': '异常', '口腔': '异常',
#         '胸部': '异常', '腹部': '异常', '脐部': '其他', '四肢': '异常', '肛门/外生殖器': '异常',
#         '户外活动(小时/日)': "100", '服用维生素D(IU/日)': "110",
#         '两次随访间': {'肺炎': '13', '其他': "63"}, '指导': ['生长发育', '口腔保健', {'其他': "没有了"}],
#         '转诊': ['有', {'原因': '不知道', '机构及科室': '心脏科', '联系人': 'winter', '联系方式': '13611012345','结果': '到位'}],
#         '下次随访日期': [2024, 4, 1], '随访医生签名': '测试', '家长签名': "666"},
#
#     '3月龄': {'随访日期': [2024, 4, 2], '本次服务类别': ['失访', {'失访原因': '11'}], '体重(kg)': [33.0, '中'], '身长(cm)': [17.10, '上'], '头围(cm)': '33',
#         '面色': '黄染', '皮肤': '异常', '前囟': ['未闭', '33', '19'], '颈部包块': '有', '眼睛': '异常', '耳': '异常', '口腔': '异常',
#         '胸部': '异常', '腹部': '异常', '脐部': '异常', '四肢': '异常', '可疑佝偻病': '多汗', '体征': '颅骨软化', '肛门/外生殖器': '异常',
#         '户外活动(小时/日)': "56", '服用维生素D(IU/日)': "66", '发育评估': ['对很大声音没有反应', '俯卧时不会抬头'],
#         '两次随访间': {'腹泻': '3', '外伤': '2', '其他': "不知情"}, '指导': ['疾病预防', {'其他': "沟通中"}],
#         '转诊': ['有', {'原因': '疑难', '机构及科室': '普外科', '联系人': 'owl', '联系方式': '13816109011','结果': '到位'}],
#         '下次随访日期': [2025, 7, 1], '随访医生签名': '7', '家长签名': "666"},
#
#     '6月龄': {'随访日期': [2024, 7, 2], '本次服务类别': ['失访', {'失访原因': '644'}], '体重(kg)': [3.2, '中'], '身长(cm)': [8.6, '上'], '头围(cm)': '37',
#         '面色': '其他', '皮肤': '异常', '前囟': ['闭合', '3', '23'], '颈部包块': '有','眼睛': '异常', '耳': '异常', '听力': '未通过', '口腔': '8',
#         '胸部': '异常', '腹部': '异常', '四肢': '异常', '可疑佝偻病': '多汗', '体征': '颅骨软化', '肛门/外生殖器': '异常', ' 血红蛋白值 ': '54',
#         '户外活动(小时/日)': "56", '服用维生素D(IU/日)': "66",
#         '发育评估': ['不会伸手抓物', '紧握拳松不开'], '两次随访间': {'外伤': '21', '其他': "6"},
#         '指导': ['科学喂养', '预防伤害', {'其他': "44"}], '管理服务 ': ['中医饮食调养指导', {'其他': '11212'}],
#         '转诊': ['有', {'原因': '1', '机构及科室': '2', '联系人': 'peter', '联系方式': '13611909800','结果': '未到位'}],
#         '下次随访日期': [2024, 9, 1], '随访医生签名': '222', '家长签名': "yoyo"},
#
#     '8月龄': {'随访日期': [2024, 9, 2], '本次服务类别': ['失访', {'失访原因': '44'}], '体重(kg)': [3.2, '中'], '身长(cm)': [8.6, '上'], '头围(cm)': '40',
#         '面色': '其他', '皮肤': '异常', '前囟': ['闭合', '4','24'], '眼睛': '异常', '耳': '异常', '口腔': '9', '胸部': '异常',
#         '腹部': '异常', '四肢': '异常', '可疑佝偻病': '多汗', '体征': '颅骨软化', '肛门/外生殖器': '异常', ' 血红蛋白值 ': '54',
#         '户外活动(小时/日)': "56", '服用维生素D(IU/日)': "66", '发育评估': ['双手间不会传递玩具', '不会独坐'],
#         '两次随访间': {'肺炎': '10', '外伤': '11', '其他': "12"}, '指导': ['生长发育', '口腔保健', {'其他': "198"}],
#         '转诊': ['有', {'原因': '调查', '机构及科室': '外科', '联系人': 'peter', '联系方式': '13611909800','结果': '未到位'}],
#         '下次随访日期': [2024, 11, 1], '随访医生签名': '1', '家长签名': "sk"}
# }})



# # todo 4.3 12-30月龄儿童健康检查记录表
# Gw_PO.phs_child_etjob_operation({'operate': '编辑', 'title': '12-30月龄儿童健康检查记录表', 'data': {
#     '12月龄': {'随访日期': [2025, 1, 1], '本次服务类别': ['随访'], '体重(kg)': [10.11, '上'], '身长(cm)': [20.22, '中'],
#         '面色': '红润', '皮肤': '异常', '前囟': ['未闭', '10', '11'], '眼睛': '异常', '耳': '异常', '听力': '未通过',
#         '出牙/龋齿数': ['6', '8'], '胸部': '异常', '腹部': '异常', '四肢': '异常', '步态': '异常', '可疑佝偻病': '鸡胸',
#         '户外活动(小时/日)': "100", '服用维生素D(IU/日)': "110",
#         '发育评估': ['呼唤名字无反应', '不会扶物站立'], '两次随访间': {'肺炎': '13', '其他': "63"},
#         '指导': ['生长发育', '口腔保健', {'其他': "没有了"}], '管理服务 ': ['中医饮食调养指导', {'其他': '11212'}],
#         '转诊': ['有', {'原因': '不知道', '机构及科室': '心脏科', '联系人': 'winter', '联系方式': '13611012345', '结果': '到位'}],
#         '下次随访日期': [2025, 4, 1], '随访医生签名': '测试', '家长签名': "666"},
#
#     '18月龄': {'随访日期': [2025, 1, 5], '本次服务类别': ['失访', {'失访原因': '44'}],
#         '体重(kg)': [70.11, '上'], '身长(cm)': [80.22, '中'],
#         '面色': '红润', '皮肤': '异常', '前囟': ['未闭', '1', '41'], '眼睛': '异常', '耳': '异常',
#         '出牙/龋齿数': ['7', '9'], '胸部': '异常', '腹部': '异常', '四肢': '异常', '步态': '异常', '可疑佝偻病': '鸡胸', ' 血红蛋白值 ': '24',
#         '户外活动(小时/日)': "15", '服用维生素D(IU/日)': "68",
#         '发育评估': ['不会有意识叫“爸爸”或“妈妈”', '与人无目光交流'], '两次随访间': {'肺炎': '23', '其他': "67"},
#         '指导': ['生长发育', '口腔保健', {'其他': "3没有了"}], '管理服务 ': ['传授按揉迎香穴，足三里穴方法', {'其他': '4333'}],
#         '转诊': ['有', {'原因': '0不知道', '机构及科室': '2心脏科', '联系人': '3winter', '联系方式': '58776511', '结果': '到位'}],
#         '下次随访日期': [2025, 7, 1], '随访医生签名': '测试', '家长签名': "pepe"},
#
#     '24月龄': {'随访日期': [2025, 1, 10], '本次服务类别': ['督促'], '体重(kg)': [10.11, '上'], '身长(cm)': [20.22, '中'],
#         '面色': '红润', '皮肤': '异常', '前囟': ['未闭', '10', '11'], '眼睛': '异常', '耳': '异常', '听力': '未通过',
#         '出牙/龋齿数': ['10', '12'], '胸部': '异常', '腹部': '异常', '四肢': '异常', '步态': '异常', '可疑佝偻病': '鸡胸',
#         '户外活动(小时/日)': "100", '服用维生素D(IU/日)': "110",
#         '发育评估': ['不会按吩咐做简单事情”', '不会扶栏上楼/台阶'], '两次随访间': {'肺炎': '13', '其他': "63"},
#         '指导': ['生长发育', '口腔保健', {'其他': "没有了"}], '管理服务 ': ['中医饮食调养指导', {'其他': '11212'}],
#         '转诊': ['有', {'原因': '不知道', '机构及科室': '心脏科', '联系人': 'winter', '联系方式': '13611012345','结果': '到位'}],
#         '下次随访日期': [2025, 9, 1], '随访医生签名': '测试', '家长签名': "hello"},
#
#     '30月龄': {'随访日期': [2025, 1, 12], '本次服务类别': ['失访', {'失访原因': '44'}], '体重(kg)': [44.11, '上'], '身长(cm)': [67.22, '中'],
#         '面色': '红润', '皮肤': '异常', '眼睛': '异常', '耳': '异常',
#         '出牙/龋齿数': ['11', '13'], '胸部': '异常', '腹部': '异常', '四肢': '异常', '步态': '异常', ' 血红蛋白值 ': '12',
#         '户外活动(小时/日)': "45",
#         '发育评估': ['不会说2-3个字的短语', '兴趣单一、刻板'], '两次随访间': {'负责': '1', '其他': "哈哈"},
#         '指导': ['合理膳食', {'其他': "没有是吗？"}], '管理服务 ': ['传授按揉迎香穴，足三里穴方法', {'其他': '567'}],
#         '转诊': ['有', {'原因': '0不知道', '机构及科室': '2心脏科', '联系人': '3winter', '联系方式': '58776511', '结果': '到位'}],
#         '下次随访日期': [2025, 11, 1], '随访医生签名': '测试', '家长签名': "pepe"}
# }})



# # todo 4.4 3～6岁儿童健康检查记录表
# Gw_PO.phs_child_etjob_operation({'operate': '编辑', 'title': '3～6岁儿童健康检查记录表', 'data': {
#     '3岁': {'随访日期': [2022, 1, 1], '本次服务类别': ['随访'], '体重(kg)': [10.11, '上'], '身长(cm)': [20.22, '中'], '体重/身高': '中',
#         '体格发育评估': '消瘦',
#         '耳': '异常', '听力': '未通过',
#         '出牙/龋齿数': ['6', '8'], '胸部': '异常', '腹部': '异常', ' 血红蛋白值 ': '12', '其他':'4324234',
#         '发育评估': ['不会双脚跳'], '两次随访间': {'肺炎': '13', '其他': "63"},
#         '指导': ['生长发育', '口腔保健', {'其他': "没有了"}], '管理服务 ': ['中医饮食调养指导', {'其他': '11212'}],
#         '转诊': ['有', {'原因': '不知道', '机构及科室': '心脏科', '联系人': 'winter', '联系方式': '13611012345', '结果': '到位'}],
#         '下次随访日期': [2023, 2, 1], '随访医生签名': '测试', '家长签名': "666"},
#     '4岁': {'随访日期': [2023, 1, 1], '本次服务类别': ['随访'], '体重(kg)': [10.11, '上'], '身长(cm)': [20.22, '中'], '体重/身高': '中',
#         '体格发育评估': '发育迟缓','视力':['1.0','1.2'], '耳': '异常',
#         '出牙/龋齿数': ['6', '8'], '胸部': '异常', '腹部': '异常', ' 血红蛋白值 ': '12', '其他':'4324234',
#         '发育评估': ['不会双脚跳'], '两次随访间': {'肺炎': '13', '其他': "63"},
#         '指导': ['生长发育', '口腔保健', {'其他': "没有了"}],
#         '转诊': ['有', {'原因': '不知道', '机构及科室': '心脏科', '联系人': 'winter', '联系方式': '13611012345', '结果': '到位'}],
#         '下次随访日期': [2024, 2, 1], '随访医生签名': '测试', '家长签名': "666"},
#     '5岁': {'随访日期': [2024, 1, 1], '本次服务类别': ['随访'], '体重(kg)': [10.11, '上'], '身长(cm)': [20.22, '中'], '体重/身高': '中',
#         '体格发育评估':'超重','视力': ['1.0','1.2'], '耳': '异常',
#         '出牙/龋齿数': ['6', '8'], '胸部': '异常', '腹部': '异常', ' 血红蛋白值 ': '12', '其他':'4324234',
#         '发育评估': ['不会单脚跳'], '两次随访间': {'肺炎': '13', '其他': "63"},
#         '指导': ['生长发育', '口腔保健', {'其他': "没有了"}],
#         '转诊': ['有', {'原因': '不知道', '机构及科室': '心脏科', '联系人': 'winter', '联系方式': '13611012345', '结果': '到位'}],
#         '下次随访日期': [2025, 4, 1], '随访医生签名': '测试', '家长签名': "666"},
#     '6岁': {'随访日期': [2025, 1, 1], '本次服务类别': ['随访'], '体重(kg)': [10.11, '上'], '身长(cm)': [20.22, '中'], '体重/身高': '中',
#         '体格发育评估':'低体重','视力':['1.0','1.2'], '耳': '异常',
#         '出牙/龋齿数': ['6', '8'], '胸部': '异常', '腹部': '异常', ' 血红蛋白值 ': '12', '其他':'4324234',
#         '发育评估': ['不会画方形'], '两次随访间': {'肺炎': '13', '其他': "63"},
#         '指导': ['生长发育', '口腔保健', {'其他': "没有了"}],
#         '转诊': ['有', {'原因': '不知道', '机构及科室': '心脏科', '联系人': 'winter', '联系方式': '13611012345', '结果': '到位'}],
#         '随访医生签名': '测试', '家长签名': "666"}
# }})

# todo 4.5 结案
# Gw_PO.phs_child_etfiles_operation({'operate': '编辑', 'title': '结案', 'data': {'结案原因': '完成服务'}})




# todo 5 删除
# Gw_PO.phs_child_etjob_operation({'operate': '删除', 'option': {"身份证号": "110101202401015310"}})
