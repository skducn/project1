# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-3-25
# Description: 基本公卫 - 家医签约 - 档案未签约
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
Web_PO.opnLabel(d_menu_basicPHS['档案未签约'])
Web_PO.swhLabel(1)



# todo 1 查询
Gw_PO_three.query({"身份证号": "310101197712137029"})
# Gw_PO_three.query({'管理机构': '张星卫生院','档案状态': '在档', "姓名": "胡成", '年龄':['1','3'], "身份证号": "110119199001019312",
#     '联系电话': '58776566', '现住址':["泉山街道", "花园社区居民委员会", "123"], '人群分类': ['一般人群', '孕产妇'],
#     "出生日期":  [[2025,1,2],[2025,2,3]]
# })


# # todo 2 签约登记
# Gw_PO_three.sign_jmsign_ready_operation({'operate': '签约登记', 'data': {
#     '身份证号':'3101011980410014', '性别':'男',
#     '居民姓名': '章三', '手机号': '13534343435', '家庭住址': '上海浦东00号',
#     '居民基本情况': ['五保', '低保'],
#     '签约类型': '个人',
#     '签约类型': '个人',
#     '服务包选择': '基础服务包（2019版）',
#     '签约医生': '村卫生院',
#     # '家庭(责任)护士': '个人22','公共卫生人员': 'chen',
#     '签约日期': [2025, 3, 4],
#     '生效日期': [2025, 3, 5],
#     '监护人姓名': '章三', '与乙方关系': '里斯本', '联系电话': '58667676', '身份证号': '310101198004110012'
# }})


# # todo 3 新增签约
Gw_PO_three.sign_jmsign_ready_operation({'operate': '新增签约', 'option': {'身份证号': '310101197712137029'}})
Gw_PO_three.sign_jmsign_ready_operation({'operate': '新增居民签约', 'data': {
    # '居民姓名': '章三', '手机号': '13534343435', '家庭住址': '上海浦东00号',
    '居民基本情况': ['65岁以上老年人', '低保'],
    '签约类型': '个人',
    '服务包选择': '51',
    '签约团队': 'testAuto',
    #'签约医生': '球蛋白', '家庭(责任)护士': '1','公共卫生人员': '张飞',
    '签约日期': [2025,3,4],
    '生效日期': [2025,3,5]
    # '监护人姓名': '章三', '与乙方关系': '里斯本', '联系电话': '58667676', '身份证号': '310101198004110012'
}})

