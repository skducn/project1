# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-7-25
# Description: 社区健康管理中心 - 居民健康服务 - 老年人体检
# 测试环境 # http://192.168.0.243:8010/#/login
# 'cs', '12345678'
#***************************************************************
from ChcPO_quanqu import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Chc_PO_quanqu = ChcPO_quanqu(logName, '老年人体检')


# todo 查询
# Chc_PO_quanqu.query({"身份证号": "310110194304210023"})
Chc_PO_quanqu.query({"姓名": "张三", "身份证号": "410203196112238333", "家庭医生": "小猴子"})



