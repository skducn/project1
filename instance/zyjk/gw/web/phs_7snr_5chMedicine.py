# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-3-11
# Description: 基本公卫 - 老年人健康管理 - 老年人中医体质辨识
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
Web_PO.opnLabel(d_menu_basicPHS['老年人中医体质辨识'])
Web_PO.swhLabel(1)


# todo 1 查询
# Gw_PO.phs_snr_chmedicine_query({"身份证号": "330101194811111550"})
# Gw_PO.phs_snr_chmedicine_query({"姓名": "胡成", "身份证号": "330101194811111550", "管理机构": "招远市卫健局", '是否仅查询机构': '是',
#     '出生日期': [[2025,1,1],[2025,2,2]], '评估日期': [[2025,1,13],[2025,2,12]],
#     "现住址": ["泉山街道", "花园社区居民委员会", "123"]})


# todo 2 导出
# Gw_PO.export("/Users/linghuchong/Desktop/5chMedicine.xls")



# todo 3 操作 - 查看
# Gw_PO.phs_snr_chmedicine_operation({'operate': '查看', 'option': {"身份证号": "330101194811111550"}})


# todo 4 操作 - 编辑 (老年人中医药健康管理服务记录表)
Gw_PO.phs_snr_chmedicine_operation({'operate': '编辑', 'option': {"身份证号": "370685195505183027"}})
Gw_PO.phs_snr_chmedicine_operation({'operate': '编辑', 'data': {
    "1.你精力充沛吗？(指精神头足,乐于做事)": "1","2.您容易疲乏吗？(指体力如何，是否稍微活动一下或做一点家务劳动就感觉到累)": "2","3.您容易气短，呼吸短促，接不上气吗？": "3",
    "4.您说话声音低弱无力吗？(指说话没有力气)": "4","5.您感觉到闷闷不乐，情绪低沉吗？(指心情不愉快，情绪低落)": "5","6.您容易情绪紧张吗，焦虑不安吗？(指遇事是否心情紧张)": "1",
    "7.您因为生活状态改变而感到孤独，失落？": "2","8.您容易感到害怕或受到惊吓？": "3",
    "9.您感到身体超重不轻松吗？(感觉身体沉重)[BMI指数=体重(kg)/身高(m)]": "4","10.您眼睛干涩吗？": "5","11.您手脚发凉吗？(不包含因周围温度低或穿的少导致的手脚发冷)": "1",
    "12.您胃脘部，背部或腰部怕冷吗？(指上腹部，背部，腰部或膝关节等，有一处或多处怕冷)": "2","13.您比一般人耐受不了寒冷吗？(指比别人容易怕冬天或是夏天的冷空调，电扇等)": "3",
    "14.您容易患感冒吗？(指每年感冒次数)": "4","15.您没有感冒时会鼻塞，流鼻涕吗？": "5","16.您有口粘口腻，或睡眠打鼾？": "1","17.您容易过敏吗？(指对药物，食物，气味，花粉或在季节交替，气候变化时)": "2",
    "18.您的皮肤容易起荨麻疹吗？(包括风团，风疹块，风疙瘩)": "3","19.您的皮肤在不知不觉中会出现青紫癫斑，皮下出血吗？(指皮肤在没有外伤的情况下出现青一块紫一块的情况)": "4",
    "20.您的皮肤一抓就红，并出现抓痕吗？(指被指甲或钝物或过后皮肤的反应)": "5","21.您皮肤或口唇干吗？": "1","22.您有肢体麻木或固定部位疼痛的感觉吗？": "2",
    "23.您面部或鼻部有油腻感或者油光发亮吗？(指脸上或鼻子)": "3","24.您面色或目眶晦暗，或出现褐色板块/斑点吗？": "4",
    "25.您有皮肤湿疹，疮疖吗？": "5","26.您感到口干咽燥，总想喝水吗？": "1","27.您感到口苦或嘴里有异味吗？(指口苦或口臭)": "2","28.您腹部肥大吗？(指腹部脂肪肥厚)": "3",
    "29.您吃(喝)凉的东西会感到不舒服或者怕吃(喝)凉的东西吗？(指不喜欢凉的食物，或吃了凉的食物后会不舒服)": "4","30.您有大便黏滞不爽，解不尽的感觉吗？(答辩容易粘在马桶或便坑壁上)": "5",
    "31.您容易大便干燥吗？": "1","32.您舌苔厚腻或有舌苔厚厚的感觉吗？(如果自我感觉不清楚可由调查员观察后填写)": "2","33.您舌下静脉淤紫或增粗吗？(可由调查人员辅助观察后填写)": "3",
    "气虚质":['3.起居调摄', '6.其他'], '阳虚质':['2.饮食调养', '6.其他'], '阴虚质':['2.饮食调养', '4.运动保健'], '痰湿质':['5.穴位保健', '6.其他'],  '平和质':['5.穴位保健', '6.其他'],
    '湿热质':['1.情志调摄', '3.起居调摄'], '血瘀质':['2.饮食调养', '3.起居调摄'], '气郁质':['4.运动保健', '6.其他'], '特禀质':['2.饮食调养', '5.穴位保健'],
   '填表日期':[2025,2,3]
}})

# # todo 5 操作 - 删除
# Gw_PO.phs_snr_chmedicine_operation({'operate': '删除', 'option': {"身份证号": "330101194811111550"}})

