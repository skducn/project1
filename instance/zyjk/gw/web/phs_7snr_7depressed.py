# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-3-11
# Description: 基本公卫 - 老年人健康管理 - 老年人抑郁评估查询
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
Web_PO.opnLabel(d_menu_basicPHS['老年人抑郁评估查询'])
Web_PO.swhLabel(1)


# todo 1 查询
Gw_PO.phs_snr_depressed_query({"身份证号": "110101193801014615"})
# Gw_PO.phs_snr_depressed_query({"姓名": "胡成", "身份证号": "110101193801014615", '出生日期': [[2025,1,1],[2025,2,2]], '评估日期': [[2025,1,13],[2025,2,12]],
#     "管理机构": "招远市卫健局", '是否仅查询机构': '是',"现住址": ["泉山街道", "花园社区居民委员会", "123"]})


# todo 2 导出
# Gw_PO.export("/Users/linghuchong/Desktop/7depressed.xls")


# todo 3 操作 - 详情
# Gw_PO.phs_snr_depressed_operation({'operate': '详情', 'option': {"身份证号": "110101193801014615"}})


# todo 4 操作 - 编辑 (老年人抑郁评估查询)
Gw_PO.phs_snr_depressed_operation({'operate': '编辑', 'option': {"身份证号": "110101193801014615"}})
Gw_PO.phs_snr_depressed_operation({'operate': '编辑', 'data': {
    " 你对生活基本上满意吗？ ": "是",
    " 你是否已经放弃了许多活动和兴趣？ ": "是",
    " 你是否觉的生活空虚？ ": "是",
    " 你是否常感到厌倦？ ": "是",
    " 你觉的未来有希望吗？ ": "是",
    " 你是否因为脑子里有一些想法摆脱不掉而烦恼？ ": "是",
    " 你是否大部分时间精力充沛？ ": "是", " 你是否害怕会有不幸的事落在你头上？ ":"是",
    " 你是否大部分时间感到幸福？ ": "是",
    " 你是否常感到孤立无援？ ": "是",
    " 你是否经常坐立不安，心烦意乱？ ": "是",
    " 你是否希望呆在家里而不愿意去做些新鲜事？ ": "是",
    " 你是否常常担心将来？ ": "是",
    " 你是否觉得记忆力比以前差？ ": "是",
    " 你觉得现在生活很惬意？ ": "是",
    " 你是否常感到心情沉重、郁闷？ ": "是",
    " 你是否觉得像现在这样生活毫无意义？ ": "是",
    " 你是否常为过去的事忧愁？ ": "是",
    " 你开始一件新的工作困难吗？ ": "是",
    " 你觉得生活充满活力吗？ ": "是",
    " 你是否觉得你的处境毫无希望？ ": "是",
    " 你是否觉得大多数人比你强的多？ ": "是",
    " 你是否常为些小事伤心？ ": "是",
    " 你是否常觉得想哭？ ": "是",
    " 你集中精力困难吗？ ": "是",
    " 你早晨起的很快活吗？ ": "是",
    " 你希望避开聚会吗？ ": "是",
    " 你的头脑像往常一样清晰吗？ ": "是"
}
    })

# # todo 5 操作 - 删除
# Gw_PO.phs_snr_depressed_operation({'operate': '删除', 'option': {"身份证号": "110101193801014615"}})

