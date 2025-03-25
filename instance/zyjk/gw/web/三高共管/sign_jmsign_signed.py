# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-3-25
# Description: 基本公卫 - 家医签约 - 已签约居民
# *****************************************************************
import sys,os
# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取 上层 目录的绝对路径
project_dir = os.path.abspath(os.path.join(current_dir, '..'))
# 将 上层 目录添加到 sys.path
sys.path.insert(0, project_dir)
from GwPO_three import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO_three = GwPO_three(logName)
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('../config.ini')
# 登录
Gw_PO_three.login(Configparser_PO.HTTP("url"), Configparser_PO.ACCOUNT("user"), Configparser_PO.ACCOUNT("password"))
# 菜单
d_menu_basicPHS =  {'签约居民概况': 'http://192.168.0.203:30080/Sign/jmsign/qyindex', '已签约居民': 'http://192.168.0.203:30080/Sign/jmsign/signed', '履约服务': 'http://192.168.0.203:30080/Sign/jmsign/qyservice', '归档记录': 'http://192.168.0.203:30080/Sign/jmsign/qyfile', '履约提醒': 'http://192.168.0.203:30080/Sign/jmsign/qyremind', '档案未签约': 'http://192.168.0.203:30080/Sign/jmsign/ready'}
Web_PO.opnLabel(d_menu_basicPHS['已签约居民'])
Web_PO.swhLabel(1)



# todo 1 查询
# Gw_PO_three.query({"身份证号": "110101199001014999"})
Gw_PO_three.query({"姓名": "丽丽"})
# Gw_PO_three.query({"姓名": "胡成", "身份证号": "110101199001014999", "居民基本情况": ['孕产妇', '糖尿病'], '签约机构': '张星卫生院',
#                    '签约服务包': ['基础服务包（2019版）','老年人签约服务包（2019版）'], '签约状态': '已签约',
#                    '家庭住址': '123123', '录入人员': 'zhangsn', '签约类型': '个人',
#                    '签约日期': [[2025,1,2],[2025,2,3]], '出生日期': [[2025,2,2],[2025,3,3]],
# })
# '签约团队': '',   //无数据


# # todo 2 导出
# # Gw_PO_three.export("/Users/linghuchong/Desktop/sign_jmsign_signed.xls")
#

# # todo 3 批量更换家医团队
# 选几个
Gw_PO_three.batch({'option': {"身份证号": "372922198510281068"}, 'data': {
    # '更换团队': '',
    # '签约医生':'',
    '更换原因':'123'
}})
# 选所有
# Gw_PO_three.batch({'option': 'all', 'data': {
#     # '更换团队': '',
#     # '签约医生':'',
#     '更换原因':'123'
# }})


#
# # todo 4。1 更新签约
# Gw_PO_three.sign_jmsign_signed_operation({'operate': '更新签约', 'option': {"身份证号": "110107199001012801"}})
# Gw_PO_three.sign_jmsign_signed_operation({'operate': '更新居民签约', 'data': {
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
# Gw_PO_three.sign_jmsign_signed_operation({'operate': '解约', 'option': {"身份证号": "110107199001012801"}})
# Gw_PO_three.sign_jmsign_signed_operation({'operate': '解约', 'data': {
#         '申请日期': [2025,1,6], '解约原因': '总体风险评估'
# }})
#
#
# # # todo 4。3 历史记录
# Gw_PO_three.sign_jmsign_signed_operation({'operate': '历史记录', 'option': {"身份证号": "110107199001012801"}})
# Gw_PO_three.sign_jmsign_signed_operation({'operate': '历史记录', 'data': {
# }})


