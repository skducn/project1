# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-8-4
# Description: 专病库
# 需求gitlab：http://192.168.0.241/cdrd_product_doc/product_doc
# *****************************************************************

from CdrdPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Cdrd_PO = CdrdPO(logName)

from PO.TimePO import *
time_PO = TimePO()
from PO.ListPO import *
List_PO = ListPO()
from PO.ColorPO import *
Color_PO = ColorPO()

# 登录
Cdrd_PO.login()

# 打开菜单
# Cdrd_PO.opnMenu('角色管理')
# Cdrd_PO.opnMenu('菜单管理')
Cdrd_PO.opnMenu('患者列表')
Cdrd_PO.swhMenu('患者列表')

# 获取数量总数
Cdrd_PO.getCount()


# 登出
# Cdrd_PO.logout()


