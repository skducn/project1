# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-7-25
# Description: 社区健康管理中心 - 居民健康服务 - 健康评估及干预
# 测试环境 # http://192.168.0.243:8010/#/login
# 'cs', '12345678'
#***************************************************************
from ChcPO_quanqu import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Chc_PO_quanqu = ChcPO_quanqu(logName, '健康评估及干预')


# todo 查询
Chc_PO_quanqu.query({"身份证号": "310110194304210023"})
# Chc_PO_quanqu.query({"姓名": "张三", "身份证号": "410203196112238333", "人群分类": "老年人", "家庭医生": "小猴子", "签约日期范围": [[2025,1,1], [2025,1,3]],
#                      '年度评估状态': '待评估', '重点人群':'', "最近一次评估日期": [[2025,2,1], [2025,2,2]],"最近一次确认日期": [[2025,3,1], [2025,3,3]],
#                      '本年度上传情况':'本年度已上传', '已点击上传': '是' })


# todo 健康评估
Chc_PO_quanqu.signManage_signAssess_operation({'operate': '健康评估', 'option': {'身份证号': '310110194304210023'}})
# Chc_PO_quanqu.signManage_signAssess_operation({'operate': '健康评估之新增评估', 'data': {}})
# Chc_PO_quanqu.signManage_signAssess_operation({'operate': '健康评估之删除评估', 'data': {}})


