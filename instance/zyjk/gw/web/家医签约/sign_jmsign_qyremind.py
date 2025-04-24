# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-3-25
# Description: 基本公卫 - 家医签约 - 履约提醒
# *****************************************************************
from GwPO_sign import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO_sign = GwPO_sign(logName, '履约提醒')


# todo 1 查询
Gw_PO_sign.query({"姓名": "110101202307019439"})
Gw_PO_sign.query({"姓名": "胡成",  '签约机构': '张星卫生院', '预期服务时间':[[2025,1,1],[2025,2,2]]
})
# '签约团队': '',   //无数据




