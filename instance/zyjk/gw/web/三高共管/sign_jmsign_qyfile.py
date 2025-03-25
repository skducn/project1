# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-3-25
# Description: 基本公卫 - 家医签约 - 归档记录
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
d_menu_basicPHS = {'签约居民概况': 'http://192.168.0.203:30080/Sign/jmsign/qyindex', '已签约居民': 'http://192.168.0.203:30080/Sign/jmsign/signed', '履约服务': 'http://192.168.0.203:30080/Sign/jmsign/qyservice', '归档记录': 'http://192.168.0.203:30080/Sign/jmsign/qyfile', '履约提醒': 'http://192.168.0.203:30080/Sign/jmsign/qyremind', '档案未签约': 'http://192.168.0.203:30080/Sign/jmsign/ready'}
Web_PO.opnLabel(d_menu_basicPHS['归档记录'])
Web_PO.swhLabel(1)



# todo 1 查询
Gw_PO_three.query({"身份证号": "110101202307019439"})
# Gw_PO_three.query({"姓名": "胡成", "身份证号": "110101202307019439", '签约日期': [[2025,1,2],[2025,2,3]], '签约服务包': '基础服务包（2019版）',
#                    '签约机构': '张星卫生院', '履约情况': '部分履约', "居民基本情况": ['孕产妇', '糖尿病']
# })
# '签约团队': '',   //无数据



# # todo 2 查看
Gw_PO_three.sign_jmsign_qyfile_operation({'operate': '查看', 'option': {'身份证号': '110101202307019439'}})
Gw_PO_three.sign_jmsign_qyfile_operation({'operate': '查看', 'data': {  }})


