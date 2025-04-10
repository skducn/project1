# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-3-12
# Description: 基本公卫 - 肺结核患者管理 - 肺结核管理
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName, '肺结核管理')


# todo 1 查询
Gw_PO.phs_tuberculosis_fjhfiles_query({"姓名": "测试11"})
# Gw_PO.phs_tuberculosis_fjhfiles_query({"姓名": "胡成", "身份证号": "110101195901015999", '上次随访日期':[[2025,1,1],[2025,3,2]], "管理机构": "招远市卫健局",
#     '是否仅查询机构': '是', "档案状态": "在档", "登记时年龄": [2, 5],
#     '登记日期':[[2025,2,2],[2025,2,4]], "管理状态": "未结案", '患者类型':'初治', '痰菌情况':'未查痰',
#     '停止治疗原因': '丢失','随访提醒分类': '常规管理', '随访日期': [[2025,4,1],[2025,4,2]]})

# todo 2 导出
# Gw_PO.export("/Users/linghuchong/Desktop/phs_tuberculosis_fjhfiles.xls")

# 操作
Gw_PO.phs_tuberculosis_fjhfiles_operation({'operate': '访视记录', 'option': {"姓名": "测试11"}})


# todo 3.1 操作 - 访视记录 - 入户随访(编辑)
# Gw_PO.phs_tuberculosis_fjhfiles_operation({'operate': '入户随访之编辑', 'data': {
#     '随访日期': [2025,1,2], '随访方式':'家庭','患者类型':'复治','痰菌情况':'阴性','耐药情况':'未检测','症状及体征':['咳嗽咳痰',{'其他':'123'}],
#     '用药':{'化疗方案':'12','用法':'间歇','药品剂型':'注射剂'},'督导人员选择': {'其他': '555'},'家庭居住环境':{'单独的居室':'有', '通风情况':'差'},
#     '生活方式评估':{'吸烟':[1,3],'饮酒':[4,6]},
#     '健康教育及培训':{'取药地点、时间':['上海家里',[2025,3,4]],'服药记录卡的填写':'未掌握','服药方法及药品存放':'未掌握','肺结核治疗疗程':'未掌握','不规律服药危害':'未掌握',
#     '服药后不良反应及处理':'未掌握','治疗期间复诊查痰':'未掌握','外出期间如何坚持服药':'未掌握','生活习惯及注意事项':'未掌握','密切接触者检查':'未掌握'},
#     '下次随访日期':[2025,3,5],'随访医生':'金浩1','患者（家属）签字':'zhanzhang'
# }})


# todo 3.2 操作 - 访视记录 - 入户随访(删除)
# Gw_PO.phs_tuberculosis_fjhfiles_operation({'operate': '入户随访之删除', 'data': {}})


# todo 4.1 操作 - 访视记录 - 历次随访（新增随访）- 停止治疗
# Gw_PO.phs_tuberculosis_fjhfiles_operation({'operate': '历次随访之新增随访', 'data': {
#     '随访日期': [2025,1,8], '治疗月序':'5',
#     '督导人员选择': '其他' ,'随访方式':'家庭',
#     '症状及体征':['咳嗽咳痰',{'其他':'123'}],
#     '生活方式评估':{'吸烟':[1,3],'饮酒':[4,6]},
#     '用药':{'化疗方案':'12','用法':'间歇','药品剂型':'注射剂', '漏服药次数':'12'},
#     '药物不良反应': {'有':'123'}, '并发症或合并症':{'有':'12333'},
#     '转诊': {'转诊':'有', '机构及科别': '阿里机构', '原因':'343', '2周内随访,随访结果':'ggg'},
#     '处理意见':'退热贴',
#     '是否停止治疗': '否',
#     '停止治疗及原因':{'出现停止治疗时间':[2025,1,2], '停止治疗原因':'完成疗程'},
#     '全程管理情况':{'应访视患者':'3','实际访视':'4','患者在疗程,应服药':'5','实际服药':'66','评估医生签名':'金浩1'},
#     '下次随访时间':[2025,3,5],'随访医生签名':'1','患者（家属）签字':'zhanzhang'
# }})

# todo 4.2 操作 - 访视记录 - 历次随访（结案）
Gw_PO.phs_tuberculosis_fjhfiles_operation({'operate': '历次随访之结案', 'data': {
    '结案原因：': {'其他': '123'}
}})
