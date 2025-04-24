# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-3-25
# Description: 基本公卫 - 家医签约 - 履约服务
# *****************************************************************
from GwPO_sign import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO_sign = GwPO_sign(logName, '履约服务')


# todo 1 查询
Gw_PO_sign.query({"身份证号": "310101197712137029"})
# Gw_PO_sign.query({"姓名": "胡成", "身份证号": "110101199001014999", '签约日期': [[2025,1,2],[2025,2,3]], "签约服务包": '基础服务包（2019版）',
#                    '签约团队': 'testAuto', '履约情况': '未履约', '居民基本信息': ['一般人群', '孕产妇'], '家庭地址': '123个人'
# })


# # todo 2 批量履约
# # 选几个
# Gw_PO_sign.batch({'option': {"身份证号": "372922198510281068"}, 'data': {
#     # '更换团队': '',
#     # '签约医生':'',
#     '更换原因':'123'
# }})
# 选所有
# Gw_PO_sign.batch({'option': 'all', 'data': {
#     # '更换团队': '',
#     # '签约医生':'',
#     '更换原因':'123'
# }})

# # todo 3。1 查看
Gw_PO_sign.sign_jmsign_qyservice_operation({'operate': '查看', 'option': {'身份证号': '310101197712137029'}})
Gw_PO_sign.sign_jmsign_qyservice_operation({'operate': '查看', 'data': {}})

# # # todo 3。2 履约
Gw_PO_sign.sign_jmsign_qyservice_operation({'operate': '履约', 'option': {'身份证号': '310101197712137029'}})
Gw_PO_sign.sign_jmsign_qyservice_operation({'operate': '履约', 'data': {}})
