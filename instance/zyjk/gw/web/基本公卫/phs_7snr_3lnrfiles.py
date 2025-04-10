# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-3-4
# Description: 基本公卫 - 老年人健康管理 - 老年人专项管理
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName, '老年人专项管理')


# todo 1 查询
Gw_PO.phs_snr_lnrfiles_query({"性别": "男"})
# Gw_PO.phs_snr_lnrfiles_query({"管理机构": "招远市卫健局", '是否仅查询机构': '是', "档案状态": "在档", "姓名": "胡成", "性别": "男",
#     "身份证号": "370685193905042226", "出生日期": [[2025, 1, 1], [2025, 1, 2]] ,
#     "现住址": ["泉山街道", "花园社区居民委员会", "123"]})


# todo 2 导出
# Gw_PO.export("/Users/linghuchong/Desktop/phs_snr_lnrfiles.xls")


# todo 3 操作 - 详情(编辑)
# Gw_PO.phs_snr_lnrfiles_operation({'operate': '详情', 'option': {"身份证号": "330101194811111550"}})
# Gw_PO.phs_snr_lnrfiles_operation({'operate': '详情', 'data': {
#     '生活赡养': ['政府', '其他'], '护理情况': "邻居", '登记日期': [2025, 2, 2]}})


# todo 4 操作 - 体验记录（新增 - 体检记录）
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
    '肝功能': {'血清谷丙转氨酶 ': '1', '血清谷草转氨酶': '2', '白蛋白浓度': '3', '总胆红素值': '4', '结合胆红素值': '5'},
    '肾功能': {'血清肌酐检测值': '6', '血尿素氮检测值': '7', '血钾浓度': '8', '血钠浓度': '9', '尿酸': '10'},
    '血脂': {'总胆固醇值': '11','甘油三酯值': '12', '血清低密度脂蛋白胆固醇值': '13', '血清高密度脂蛋白胆固醇值': '14', '癌胚抗原浓度值': '15'},
    '心电图': {'异常': '123'}, '胸部X线片':{'异常': '456'},'B超': {'异常':'hello'}, '宫颈涂片':{'异常':'peter'}, '其他辅助检查':"678",
    '健康评价': {'有异常': ['22','444']},
    '健康指导': ['建议复查', '建议转诊'], '危险因素控制': [['饮食', '锻炼'], ['减体重', '12'], ['建议接种疫苗', ['脊髓灰质炎疫苗','白喉百日咳破伤风疫苗']], ['其他','234']],
    '建议':'45345',
    '结果反馈': {'本人':'张三', '家属': '李四', '反馈人':'小明', '时间':[2025,2,3]},
    '医生签名': {'症状': '金1', '一般状况': '金2', '生活方式': '金3', '脏器功能': '金4', '查体': '金5', '皮肤': '金6', '肛门指诊': '金7', '乳腺': '金8', '妇科': '金9',
             '其他': '金10',
             ' 现存主要健康问题 ': '金11', '主要用药情况': '金12', '血常规': '金13', '尿微量白蛋白': '金14', '大便潜血':'金15',
             '心电图': '金16', '胸部X线片': '金17','B超': '金18', '宫颈涂片': '金19', '其他辅助检查':'金20',
             '健康评价':'金21', '健康指导': '金22'}
    }})


# todo 4.2 操作 - 体验记录（新增 - 中医药健康管理）
# Gw_PO.phs_snr_lnrfiles_operation({'operate': '新增中医药健康管理', 'data': {
#     "1.你精力充沛吗？(指精神头足,乐于做事)": "1","2.您容易疲乏吗？(指体力如何，是否稍微活动一下或做一点家务劳动就感觉到累)": "2","3.您容易气短，呼吸短促，接不上气吗？": "3",
#     "4.您说话声音低弱无力吗？(指说话没有力气)": "4","5.您感觉到闷闷不乐，情绪低沉吗？(指心情不愉快，情绪低落)": "5","6.您容易情绪紧张吗，焦虑不安吗？(指遇事是否心情紧张)": "1",
#     "7.您因为生活状态改变而感到孤独，失落？": "2","8.您容易感到害怕或受到惊吓？": "3",
#     "9.您感到身体超重不轻松吗？(感觉身体沉重)[BMI指数=体重(kg)/身高(m)]": "4","10.您眼睛干涩吗？": "5","11.您手脚发凉吗？(不包含因周围温度低或穿的少导致的手脚发冷)": "1",
#     "12.您胃脘部，背部或腰部怕冷吗？(指上腹部，背部，腰部或膝关节等，有一处或多处怕冷)": "2","13.您比一般人耐受不了寒冷吗？(指比别人容易怕冬天或是夏天的冷空调，电扇等)": "3",
#     "14.您容易患感冒吗？(指每年感冒次数)": "4","15.您没有感冒时会鼻塞，流鼻涕吗？": "5","16.您有口粘口腻，或睡眠打鼾？": "1","17.您容易过敏吗？(指对药物，食物，气味，花粉或在季节交替，气候变化时)": "2",
#     "18.您的皮肤容易起荨麻疹吗？(包括风团，风疹块，风疙瘩)": "3","19.您的皮肤在不知不觉中会出现青紫癫斑，皮下出血吗？(指皮肤在没有外伤的情况下出现青一块紫一块的情况)": "4",
#     "20.您的皮肤一抓就红，并出现抓痕吗？(指被指甲或钝物或过后皮肤的反应)": "5","21.您皮肤或口唇干吗？": "1","22.您有肢体麻木或固定部位疼痛的感觉吗？": "2",
#     "23.您面部或鼻部有油腻感或者油光发亮吗？(指脸上或鼻子)": "3","24.您面色或目眶晦暗，或出现褐色板块/斑点吗？": "4",
#     "25.您有皮肤湿疹，疮疖吗？": "5","26.您感到口干咽燥，总想喝水吗？": "1","27.您感到口苦或嘴里有异味吗？(指口苦或口臭)": "2","28.您腹部肥大吗？(指腹部脂肪肥厚)": "3",
#     "29.您吃(喝)凉的东西会感到不舒服或者怕吃(喝)凉的东西吗？(指不喜欢凉的食物，或吃了凉的食物后会不舒服)": "4","30.您有大便黏滞不爽，解不尽的感觉吗？(答辩容易粘在马桶或便坑壁上)": "5",
#     "31.您容易大便干燥吗？": "1","32.您舌苔厚腻或有舌苔厚厚的感觉吗？(如果自我感觉不清楚可由调查员观察后填写)": "2","33.您舌下静脉淤紫或增粗吗？(可由调查人员辅助观察后填写)": "3",
#     "气虚质":['3.起居调摄', '6.其他'], '阳虚质':['2.饮食调养', '6.其他'], '阴虚质':['2.饮食调养', '4.运动保健'], '痰湿质':['5.穴位保健', '6.其他'],  '平和质':['5.穴位保健', '6.其他'],
#     '湿热质':['1.情志调摄', '3.起居调摄'], '血瘀质':['2.饮食调养', '3.起居调摄'], '气郁质':['4.运动保健', '6.其他'], '特禀质':['2.饮食调养', '5.穴位保健'],
#    '填表日期':[2025,2,3]
# }})


# todo 4.3 操作 - 体验记录（新增 - 老年人生活自理能力评估表）
# Gw_PO.phs_snr_lnrfiles_operation({'operate': '新增老年人生活自理能力评估表', 'data': {
#     "进餐：使用餐具将饭菜送入口、咀嚼、吞咽等活动":" 需要协助，如切碎、搅拌食 物等(3) ",
#     "梳洗：梳头、洗脸、刷牙、剃须洗澡等活动":" 独立完成(0) ",
#     "穿衣：穿衣裤、袜子、鞋子等活动":" 完全需要帮助(5) ",
#     "如厕：小便、大便等活动及自控":" 完全需要帮助(10) ",
#     "活动：站立、室内行走、上下楼梯、户外活动": " 借助较大的外力才能完成站立、行走，不能上下楼梯(5) "}
#     })


# todo 4.4 操作 - 体验记录（新增 - 老年人忧郁评估）
# Gw_PO.phs_snr_lnrfiles_operation({'operate': '新增老年人忧郁评估表', 'data': {
#     " 你对生活基本上满意吗？ ": "是",
#     " 你是否已经放弃了许多活动和兴趣？ ": "是",
#     " 你是否觉的生活空虚？ ": "是",
#     " 你是否常感到厌倦？ ": "是",
#     " 你觉的未来有希望吗？ ": "是",
#     " 你是否因为脑子里有一些想法摆脱不掉而烦恼？ ": "是",
#     " 你是否大部分时间精力充沛？ ": "是", " 你是否害怕会有不幸的事落在你头上？ ":"是",
#     " 你是否大部分时间感到幸福？ ": "是",
#     " 你是否常感到孤立无援？ ": "是",
#     " 你是否经常坐立不安，心烦意乱？ ": "是",
#     " 你是否希望呆在家里而不愿意去做些新鲜事？ ": "是",
#     " 你是否常常担心将来？ ": "是",
#     " 你是否觉得记忆力比以前差？ ": "是",
#     " 你觉得现在生活很惬意？ ": "是",
#     " 你是否常感到心情沉重、郁闷？ ": "是",
#     " 你是否觉得像现在这样生活毫无意义？ ": "是",
#     " 你是否常为过去的事忧愁？ ": "是",
#     " 你开始一件新的工作困难吗？ ": "是",
#     " 你觉得生活充满活力吗？ ": "是",
#     " 你是否觉得你的处境毫无希望？ ": "是",
#     " 你是否觉得大多数人比你强的多？ ": "是",
#     " 你是否常为些小事伤心？ ": "是",
#     " 你是否常觉得想哭？ ": "是",
#     " 你集中精力困难吗？ ": "是",
#     " 你早晨起的很快活吗？ ": "是",
#     " 你希望避开聚会吗？ ": "是",
#     " 你的头脑像往常一样清晰吗？ ": "是"
# }
#     })

# todo 4.5 操作 - 体验记录（新增 - 简易智力检查）
# Gw_PO.phs_snr_lnrfiles_operation({'operate': '新增简易智力检查', 'data': {
#     "1.时间定力 (5)": {"今年是哪一年?": "0", "现在是什么季节": "0", "现在是几月份": "0", "今天是几号": "0", "今天是星期几": "0"},
#     "2.地点定向力 (5)": {"我们现在在哪个国家?": "0", "我们现在在哪个城市": "0", "我们现在在城市的哪一部分": "0", "我们现在在哪个建筑物": "0", "我们现在在第几层": "0"},
#     "3.即刻回忆 (3)": {"皮球": "0", "国旗": "0", "树": "0"},
#     "4.注意力与计算力 (5)": {"100减7等于? 93": "0", "100减7等于? 86": "0", "100减7等于? 79": "0", "100减7等于? 72": "0", "100减7等于? 65": "0"},
#     "5.回忆能力 (3)": {"皮球": "0", "国旗": "0", "树": "0"},
#     "6.命名能力 (2)": {"问:这是什么? 展示 (铅笔)": "0", "问:这是什么? 展示 (手表)": "0"},
#     "7.语言重复能力 (1)": {"说:我现在让你重复我说的。准备好了吗？瑞雪兆丰年。你说一遍 ": "0"},
#     "8.理解力 (3)": {"左手拿着这张纸": "0", "把它对折": "0", "把它放在你的右腿上": "0"},
#     "9.阅读能力 (1)": {"闭上你的眼睛": "0"},
#     "10.写的能力 (1)": {"说:写一个句子。": "0"},
#     "11.画画的能力 (1)": {"说:照下图画。 ": "0"}
# }})


