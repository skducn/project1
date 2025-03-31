# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-3-25
# Description: 基本公卫 - 家医签约 - 归档记录
# *****************************************************************
from GwPO_sign import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO_sign = GwPO_sign(logName, '归档记录')


# todo 1 查询
Gw_PO_sign.query({"身份证号": "110101202307019439"})
# Gw_PO_sign.query({"姓名": "胡成", "身份证号": "110101202307019439", '签约日期': [[2025,1,2],[2025,2,3]], '签约服务包': '基础服务包（2019版）',
#                    '签约机构': '张星卫生院', '履约情况': '部分履约', "居民基本情况": ['孕产妇', '糖尿病']
# })
# '签约团队': '',   //无数据


# # todo 2 查看
Gw_PO_sign.sign_jmsign_qyfile_operation({'operate': '查看', 'option': {'身份证号': '110101202307019439'}})
Gw_PO_sign.sign_jmsign_qyfile_operation({'operate': '查看', 'data': {  }})


