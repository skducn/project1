# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-7-25
# Description: 社区健康管理中心 - 居民健康服务 - 健康服务
# 测试环境 # http://192.168.0.243:8010/#/login
# 'cs', '12345678'
#***************************************************************
from ChcPO_quanqu import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Chc_PO_quanqu = ChcPO_quanqu(logName, '健康服务')



# todo 查询
Chc_PO_quanqu.query({"身份证号": "410203196112238333"})
# Chc_PO_quanqu.query({"姓名": "张三", "身份证号": "410203196112238333", "人群分类": "老年人", "家庭医生": "小猴子", "上次服务日期": [[2025,1,1], [2025,1,3]]})


# todo 服务记录
# Chc_PO_quanqu.signManage_service_operation({'operate': '服务记录', 'option': {'身份证号': '410203196112238333'}})
# Chc_PO_quanqu.signManage_service_operation({'operate': '服务记录', 'data': {}})


# todo 新增服务
# Chc_PO_quanqu.signManage_service_operation({'operate': '新增服务', 'option': {'身份证号': '410203196112238333'}})
# Chc_PO_quanqu.signManage_service_operation({'operate': '新增服务', 'data': {
#     '服务时间': [2025,1,2],
#     '服务形式': '微信',
#     '服务内容': ['随访管理：医嘱及用药记录', {'其他服务': '123'}]
# }})