# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-7-25
# Description: 社区健康管理中心 - 西航港大屏
# 测试环境 # http://192.168.0.243:8010/#/login
# 账号: lbl 密码：Qa@123456
#***************************************************************
from ChcPO_quanqu import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Chc_PO = ChcPO_quanqu(logName, '西航港社区')


# 获取大屏
Chc_PO.getScreenData()


