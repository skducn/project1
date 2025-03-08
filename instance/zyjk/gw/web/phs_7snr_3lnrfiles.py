# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-3-4
# Description: 基本公卫 - 老年人健康管理 - 老年人专项管理
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
Web_PO.opnLabel(d_menu_basicPHS['老年人专项管理'])
Web_PO.swhLabel(1)


# todo 1 查询
Gw_PO.phs_snr_lnrfiles_query({"性别": "男"})
# Gw_PO.phs_snr_lnrfiles_query({"管理机构": "招远市卫健局", '是否仅查询机构': '是', "档案状态": "在档", "姓名": "胡成", "性别": "男",
#     "身份证号": "370685193905042226", "出生日期": [[2025, 1, 1], [2025, 1, 2]] ,
#     "现住址": ["泉山街道", "花园社区居民委员会", "123"]})


# todo 2 导出
# Gw_PO.export("/Users/linghuchong/Desktop/3lnrfiles.xls")


# todo 3 操作 - 详情(编辑)
# Gw_PO.phs_snr_lnrfiles_operation({'operate': '详情', 'option': {"身份证号": "330101194811111550"}})
# Gw_PO.phs_snr_lnrfiles_operation({'operate': '详情', 'data': {
#     '生活赡养': ['政府', '其他'], '护理情况': "邻居", '登记日期': [2025, 2, 2]}})


# todo 4 操作 - 体验记录（新增）
Gw_PO.phs_snr_lnrfiles_operation({'operate': '体检记录', 'option': {"身份证号": "330101194811111550"}})
Gw_PO.phs_snr_lnrfiles_operation({'operate': '新增体验', 'data': {
    '体检来源': "老年人体检", '体检日期': [2025,3,2], '责任医生': '何飞飞', '症状': ['头痛', '胸闷', {'其他': '123'}],
    '体温':'37', '脉率':'66','呼吸频率':'88','腰围':'90','右侧血压':['100','90'],'身高': '177', '体重': '66',
    ' 老年人健康': '不满意', '老年人认知能力': {'粗筛阳性': '30'}, ' 老年人生活自理': '中度依赖(9~18分)', '老年人情感状态': {'粗筛阳性': '20'},
    '体育锻炼': {'锻炼频率': '每天', '每次锻炼时间': '12', '坚持锻炼时间': '2', '坚持方式': 'zao'}, ' 饮食习惯 ': ['荤食为主', '嗜油'],
    ' 吸烟情况 ': {'吸烟状况': '现在每天吸', '日吸烟量': '4', '开始吸烟年龄': '22', '戒烟年龄': '44'},
    ' 饮酒情况 ': {'饮酒频率': '经常', '日饮酒量': '12', '开始饮酒年龄': '2', '近一年内是否曾醉酒': '否', '是否戒酒': {'已戒酒': '13'}, '饮酒种类': '其他'},
    '职业病危害': {'有': ['高空作业','4'], '毒物种类': {
        '粉尘': ['勾选', '10', {'防护措施': {'有': '1'}}],
        '化学有害因素': ['不勾选', '20', {'防护措施': {'有': '2'}}],
        '物理有害因素': ['勾选', '30', {'防护措施': {'有': '3'}}],
        '生物因素': ['勾选', '40', {'防护措施': {'有': '4'}}],
        '放射物质类': ['勾选', '50', {'防护措施': {'无': '5'}}],
        '不详': ['勾选', '', {'防护措施': {'有': '6'}}],
        '其他': ['勾选', '70', {'防护措施': {'有': '77'}}]}},
    ' 口腔 ': {'口唇': '其他', '齿列': {'缺齿': [1,2,3,4], '龋齿': [11,22,33,44], '义齿(假牙)': [67,42,83,14]}, '咽部': '充血'},
    ' 视力 ': {'左眼': '1.1', '右眼': '1.2', '矫正视力左眼': '1.3', '矫正视力右眼': '1.4'},
    ' 听力 ': '听不清或无法听见', ' 运动能力 ': '无法独立完成其中任何一个动作',' 眼底 ': '异常', ' 皮肤 ': {'其他': '333'}, ' 巩膜 ': {'其他':'444'}, ' 淋巴结 ': {'其他':'555'},
    ' 肺 ': {'桶状胸': {'是': '23'}, '呼吸音': {'异常': '123'}, '罗音': {'其他': '777'}},
    ' 心脏 ': {'心率': '12', '心律': '不齐', '杂音': {'有': '44'}},
    ' 腹部 ': {'压痛': {'有': '1'}, '包块': {'无': ''}, '肝大': {'有': '3'}, '脾大': {'有': '4'}, '移动性浊音': {'有': '5'}},
    ' 下肢水肿 ': '双侧不对称下肢水肿', ' 足背动脉搏动 ': '触及左侧弱或消失',
    ' 肛门指诊 ': {'其他': 'eee'},
    ' 乳腺 ': ['乳房切除', {'其他': 'ww'}], ' 妇科 ': {'外阴': '异常', '阴道': '未见异常', '宫颈': '异常', '宫体': '异常', '附件': '异常'},
    ' 其他 ': 'rty',
    ' 脑血管疾病 ': ['蛛网膜下腔出血', {'其他': '12'}], ' 肾脏疾病 ': ['慢性肾炎', {'其他': '456'}], ' 心血管疾病 ': ['高血压', {'其他': '456'}],
    ' 眼部疾病 ': ['白内障', {'其他': '12'}], ' 神经系统疾病 ': ['帕金森病', {'其他': '12'}], ' 其他系统疾病 ': ['恶性肿瘤', {'其他': '12'}],
    ' 住院史 ': [{'入院日期': [2025, 1, 1], '出院日期': [2025, 3, 3], '原因': '123', '医疗机构及科室名称': 'rrr', '病案号':'78'}, {'入院日期': [2025,2,2],'出院日期':[2025,4,4], '原因':'00', '医疗机构及科室名称':'uui', '病案号':'9090'}],
    ' 家庭病床 ': [{'建床日期': [2025, 1, 13], '撤床日期': [2025, 1, 16], '原因':'123', '医疗机构及科室名称': 'abc', '病案号': '1278'}, {'建床日期': [2025,1,11], '撤床日期':[2025,1,14], '原因':'yu', '医疗机构及科室名称':'john', '病案号':'44'}],
    '主要用药情况': [{'药物名称': '女金丸', '途径': '皮下注射', '频次': '每天二次', '单次剂量': '2','剂量单位': '袋','每日剂量': '3','用药时间': '4', '服药依从性': '规律'},
               {'药物名称': '三九感冒灵', '途径': '口服', '频次': '每天四次', '单次剂量': '6','剂量单位': '包','每日剂量': '2','用药时间': '7', '服药依从性': '不服药'}],
    ' 非免疫规划预防接种史 ': [{'接种名称': '结核疫苗','接种日期': [2025,1,2], '接种机构':'ayoto机构'}, {'接种名称': '麻疹疫苗','接种日期':[2025,1,1], '接种机构':'bai机构'}],
    '血常规': {'血红蛋白值 ': '23', '白细胞计数值': '244', '血小板计数值 ': '55','血常规其他': '44'},
    '尿常规': {'尿蛋白定性检测结果': '+', '尿蛋白定量检测值': '22', '尿糖定性检测结果 ':'++', '尿糖定量检测值': '34', '尿酮体定性检测结果': '++', '尿潜血定性检测结果': '+++', '尿比重': '2323', '尿液酸碱度':'3434', '尿常规其他': '6767','尿白细胞': '+'},
    '血糖': {'空腹血糖值 ': '213', '餐后2小时血糖值': '678'}, '尿微量白蛋白': '234','大便潜血': '阳性','糖化血红蛋白':'34',
    '乙型五项检查': {'乙型肝炎病毒表面抗原检测结果': '不详', '乙型肝炎病毒e抗原检测结果': '阴性','乙型肝炎病毒表面抗体检测结果': '阳性','乙型肝炎病毒e抗体检测结果': '不详','乙型肝炎病毒核心抗体检测结果': '阳性'},
    '肝功能': {'血清谷丙 转氨酶 ': '1', '血清谷草 转氨酶': '2', '白蛋白浓度 ': '3', '总胆红素值': '4', '结合胆红素值': '5'},
    '肾功能': {'血清肌酐检测值': '6', '血尿素氮检测值': '7', '血钾浓度': '8', '血钠浓度': '9', '尿酸': '10'},
    '血脂': {'总胆固醇值': '11','甘油三酯值': '12', '血清低密度脂蛋白胆固醇值': '13', '血清高密度脂蛋白胆固醇值': '14', '癌胚抗原浓度值': '15'},
    '心电图': {'异常': '123'}, '胸部X线片':{'异常': '456'},'B超': {'异常':'hello'}, '宫颈涂片':{'异常':'peter'}, '其他辅助检查':"678",
    '健康评价': {'有异常': ['22','444']},
    '健康指导': ['建议复查', '建议转诊'], '危险因素控制': [['饮食', '锻炼'], ['减体重', '12'], ['建议接种疫苗', ['脊髓灰质炎疫苗','白喉百日咳破伤风疫苗']], ['其他','234']],
    '建议':'45345',
    '结果反馈': {'本人':'张三', '家属': '李四', '反馈人':'小明', '时间':[2025,2,3]},
    '医生签名': {'症状': '金1', '一般状况': '金2', '生活方式': '金3', '脏器功能': '金4',
             '查体1_眼底': '金5', '查体2': '金6', '查体3_肛门指诊': '金7', '查体4_乳腺': '金8', '查体5_妇科': '金9', '查体6_其他': '金10',
             '现存主要健康问题和住院治疗情况': '金11', '主要用药情况和非免疫规划预防接种史': '金12', '辅助检验1_血常规和尿常规': '金13', '辅助检验2_尿微量白蛋白': '金14', '辅助检验3':'金15',
             '辅助检查1_心电图': '金16', '辅助检查2_胸部X线片': '金17','辅助检查3_B超': '金18', '辅助检查4_宫颈涂片': '金19', '辅助检查4_其他辅助检查':'金20',
             '健康评价':'金21', '健康指导和危险因素控制': '金22'},
    }})
# Gw_PO.phs_healthrecord_personal_new({'button': '保存复核'})




# todo 操作 - 更新
# Gw_PO.phs_healthrecord_personal_operation({'operate': ' 更新 ', 'option': {"姓名": "李丽丽", "档案编号": "37068500000000047"}})
# Gw_PO.phs_healthrecord_personal_operation({'operate': ' 更新 ', 'operate2': '仅保存', 'data': {
#     ' 姓名 ': "李四", ' 性别 ': "女", ' 出生日期 ': [2024, 2, 2], ' 民族 ': "回族",
#     ' 现住址 ': ["上海市", "市辖区", "虹口区", "广中路街道", "商业一村居委会", "多媒体100号"],
#     ' 本人电话 ': "13815161718", ' 联系人姓名 ': "令狐冲", ' 联系人电话 ': "58771234", ' 常住类型 ': '非户籍',
#     ' 文化程度 ': "专科教育", ' 职业 ': "军人", ' 工作单位 ': "上海智赢", ' 婚姻状况 ': "离婚", ' 血型 ': '不详',
#     ' RH血型 ': 'Rh阳性',
#     ' 医疗费用支付方式 ': [['全自费', {'其他': '123'}], {'城镇职工基本医疗保险': '555', '城镇居民基本医疗保险': '666', '贫困救助': "777"}],
#     ' 药物过敏史 ': ['青霉素类抗生素', '含碘药品', {'其他药物过敏源': "12345"}],
#     ' 暴露史 ': ['化学品', '不详'],
#     ' 既往史 ': {'疾病': {"有": [['高血压', [2025, 1, 1]], ['冠心病', [2025, 2, 1]]]},
#               '手术': {'有': [['手术1', [2025, 1, 3]], ['手术2', [2025, 1, 4]], ['手术3', [2025, 2, 4]]]},
#               '外伤': {"有": [['外伤1', [2025, 4, 11]], ['外伤2', [2025, 5, 5]]]},
#               '输血': {"有": [['输血1', [2025, 3, 3]], ['输血2', [2025, 4, 4]]]}},
#     ' 家族史 ': {'有': [['高血压', '母亲'], ['高血压', '母亲'], ['脑卒中', '子女']]},
#     ' 遗传病史 ': {'有': {"疾病名称": '帕金森'}},
#     ' 残疾情况 ': [['听力残疾', '精神残疾', {'其他残疾': "90"}], {' 残疾证号 ': 'ab123'}],
#     ' 家庭情况 ': {' 与户主关系 ': '子', ' 户主姓名 ': "李四2", ' 户主身份证号 ': "310101198004110013", ' 家庭人口数 ': "4", ' 家庭结构 ': "3", ' 居住情况 ': '独居'},
#     ' 厨房排风设施 ': '烟囱', ' 燃料类型 ': '煤', ' 饮水 ': '自来水', ' 厕所 ': '马桶', ' 禽畜栏 ': '无',
#     ' 管理机构 ': '招远市卫健局', ' 档案是否开放 ': "否", ' 建档日期 ': [2025, 1, 16],
#     ' 更新方式 ': '门诊',' 更新内容 ': "测试三峡",
#     }})

# ' 既往史 ': {'疾病': {"有": [['高血压', [2025, 1, 1]], ['冠心病', [2025, 2, 1]]]},
# ' 既往史 ': {'疾病': {"无": ''},
# ' 家族史 ': {'无': ''},
# ' 家族史 ': {'有': [['高血压', '母亲'], ['高血压', '母亲'], ['脑卒中', '子女']]},
# ' 遗传病史 ': {'无': ''}
# ' 遗传病史 ':{'有': {"疾病名称": '帕金森'}},
# ' 管理机构 ': "招远市卫健局"
# ' 管理机构 ': "金岭镇卫生院"
# ' 管理机构 ': {"金岭镇卫生院": "金岭镇山上候家村卫生室"}


# todo 操作 - 终结
# Gw_PO.phs_healthrecord_personal_operation({'operate': ' 终结 ', 'option': {"姓名": "李丽丽", "档案编号": "37068500000000047"}})
# Gw_PO.phs_healthrecord_personal_operation({'operate': ' 终结 ', 'data': {
#     '档案状态': {'暂不管理': {'暂不管理原因': '住院', '暂不管理日期': [2025, 1, 2]}}
#     }})
# Gw_PO.phs_healthrecord_personal_operation({'operate': ' 终结 ', 'data': {
#     '档案状态': {'已死亡': {'档案注销日期': [2025, 1, 3], '死亡日期': [2025, 1, 3]}}
#     }})


# todo 操作 - 更新历史
# Gw_PO.phs_healthrecord_personal_operation({'operate': '更新历史', 'option': {"姓名": "李丽丽", "档案编号": "37068500000000047"}})
# Gw_PO.phs_healthrecord_personal_operation({'operate': '更新历史', 'data': {}
#     })


# todo 3 姓名 (更新)
# Gw_PO.phs_healthrecord_personal_operation({'operate': '姓名', 'option': {"姓名": "李丽丽", "档案编号": "37068500000000047"}})
# Gw_PO.phs_healthrecord_personal_operation({'operate': '姓名', 'operate2': '更新', 'data': {
#     ' 姓名 ': "李四", ' 性别 ': "女", ' 出生日期 ': [2024, 2, 2], ' 民族 ': "回族",
#     ' 现住址 ': ["上海市", "市辖区", "虹口区", "广中路街道", "商业一村居委会", "多媒体100号"],
#     ' 本人电话 ': "13815161718", ' 联系人姓名 ': "令狐冲", ' 联系人电话 ': "58771234", ' 常住类型 ': '非户籍',
#     ' 文化程度 ': "专科教育", ' 职业 ': "军人", ' 工作单位 ': "上海智赢", ' 婚姻状况 ': "离婚", ' 血型 ': '不详',
#     ' RH血型 ': 'Rh阳性',
#     ' 医疗费用支付方式 ': [['全自费', {'其他': '123'}], {'城镇职工基本医疗保险': '555', '城镇居民基本医疗保险': '666', '贫困救助': "777"}],
#     ' 药物过敏史 ': ['青霉素类抗生素', '含碘药品', {'其他药物过敏源': "12345"}],
#     ' 暴露史 ': ['化学品', '不详'],
#     ' 既往史 ': {'疾病': {"有": [['高血压', [2025, 1, 1]], ['冠心病', [2025, 2, 1]]]},
#               '手术': {'有': [['手术1', [2025, 1, 3]], ['手术2', [2025, 1, 4]], ['手术3', [2025, 2, 4]]]},
#               '外伤': {"有": [['外伤1', [2025, 4, 11]], ['外伤2', [2025, 5, 5]]]},
#               '输血': {"有": [['输血1', [2025, 3, 3]], ['输血2', [2025, 4, 4]]]}},
#     ' 家族史 ': {'有': [['高血压', '母亲'], ['高血压', '母亲'], ['脑卒中', '子女']]},
#     ' 遗传病史 ': {'有': {"疾病名称": '帕金森'}},
#     ' 残疾情况 ': [['听力残疾', '精神残疾', {'其他残疾': "90"}], {' 残疾证号 ': 'ab123'}],
#     ' 家庭情况 ': {' 与户主关系 ': '子', ' 户主姓名 ': "李四2", ' 户主身份证号 ': "310101198004110013", ' 家庭人口数 ': "4", ' 家庭结构 ': "3", ' 居住情况 ': '独居'},
#     ' 厨房排风设施 ': '烟囱', ' 燃料类型 ': '煤', ' 饮水 ': '自来水', ' 厕所 ': '马桶', ' 禽畜栏 ': '无',
#     ' 管理机构 ': '招远市卫健局', ' 档案是否开放 ': "否", ' 建档日期 ': [2025, 1, 16],
#     ' 更新方式 ': '门诊',' 更新内容 ': "测试三峡",
#     }})

# todo 3 姓名（获取）
# Gw_PO.phs_healthrecord_personal_operation({'operate': '姓名', 'option': {"姓名": "李丽丽", "档案编号": "37068500100100157"}})
# # Gw_PO.phs_healthrecord_personal_operation({'operate': '姓名', 'option': {"姓名": "陈美"}})
# d_ = Gw_PO.phs_healthrecord_personal_operation({'operate': '姓名', 'operate2': '获取', 'data': {}})
# print(d_)  # {'身份证号码': ['372922198510281068'], '档案编号': ['37068500100100157'], ...