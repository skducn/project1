# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-3-25
# Description: 基本公卫 - 家医签约 - 已签约居民
# *****************************************************************
from GwPO_sign import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
GwPO_sign = GwPO_sign(logName, '已签约居民')


# todo 1 查询
# Gw_PO_three.query({"身份证号": "110101199001014999"})
GwPO_sign.query({"姓名": "丽丽"})
# GwPO_sign.query({"姓名": "胡成", "身份证号": "110101199001014999", "居民基本情况": ['孕产妇', '糖尿病'], '签约机构': '张星卫生院',
#                    '签约服务包': ['基础服务包（2019版）','老年人签约服务包（2019版）'], '签约状态': '已签约',
#                    '家庭住址': '123123', '录入人员': 'zhangsn', '签约类型': '个人',
#                    '签约日期': [[2025,1,2],[2025,2,3]], '出生日期': [[2025,2,2],[2025,3,3]],
# })
# '签约团队': '',   //无数据


# # todo 2 导出
# # GwPO_sign.export("/Users/linghuchong/Desktop/sign_jmsign_signed.xls")
#

# # todo 3 批量更换家医团队
# 选几个
GwPO_sign.batch({'option': {"身份证号": "372922198510281068"}, 'data': {
    # '更换团队': '',
    # '签约医生':'',
    '更换原因':'123'
}})
# 选所有
# GwPO_sign.batch({'option': 'all', 'data': {
#     # '更换团队': '',
#     # '签约医生':'',
#     '更换原因':'123'
# }})


#
# # todo 4。1 更新签约
# GwPO_sign.sign_jmsign_signed_operation({'operate': '更新签约', 'option': {"身份证号": "110107199001012801"}})
# GwPO_sign.sign_jmsign_signed_operation({'operate': '更新居民签约', 'data': {
#     '居民姓名': '章三', '手机号': '13534343435', '家庭住址': '上海浦东00号',
#     '居民基本情况': ['五保', '低保'],
#     '签约类型': '个人',
#     '服务包选择': '基础服务包（2019版）',
#     '签约医生': '村卫生院',
#     # '家庭(责任)护士': '个人22','公共卫生人员': 'chen',
#     '签约日期': [2025,3,4],
#     '生效日期': [2025,3,5],
#     '监护人姓名': '章三', '与乙方关系': '里斯本', '联系电话': '58667676', '身份证号': '310101198004110012'
# }})


# # # todo 4。2 解约
# GwPO_sign.sign_jmsign_signed_operation({'operate': '解约', 'option': {"身份证号": "110107199001012801"}})
# GwPO_sign.sign_jmsign_signed_operation({'operate': '解约', 'data': {
#         '申请日期': [2025,1,6], '解约原因': '总体风险评估'
# }})
#
#
# # # todo 4。3 历史记录
# GwPO_sign.sign_jmsign_signed_operation({'operate': '历史记录', 'option': {"身份证号": "110107199001012801"}})
# GwPO_sign.sign_jmsign_signed_operation({'operate': '历史记录', 'data': {
# }})


