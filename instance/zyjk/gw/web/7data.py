# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-12-19
# Description: 公卫 - 数据维护
# *****************************************************************

from GwPO import *
Gw_PO = GwPO()

# 1，登录
Gw_PO.login('http://192.168.0.203:30080/#/login', '11011', 'HHkk2327447')


# 获取数据维护二级菜单连接
Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li[7]", 2)  # 点击一级菜单数据维护
d_menu_data = Gw_PO.getMenu2Url()
print('数据维护 =>', d_menu_data)
# 数据维护 => {'基础数据录入': 'http://192.168.0.203:30080/org/reportData/baseinput', '子机构数据维护': 'http://192.168.0.203:30080/org/reportData/childData', '家医团队维护': 'http://192.168.0.203:30080/org/baseData/PCPmaintenance', '常用药物维护': 'http://192.168.0.203:30080/org/baseData/drug', '服务包管理': 'http://192.168.0.203:30080/org/baseData/service', '服务项管理': 'http://192.168.0.203:30080/org/baseData/serviceItem', '团队管理员': 'http://192.168.0.203:30080/org/baseData/teamAdmin'}


# todo 8 数据维护

# todo 1.1, 上报数据维护 - 基础数据录入
# Web_PO.opnLabel(d_menu_data['基础数据录入'])
# Web_PO.swhLabel(1)

# todo 1.2, 上报数据维护 - 子机构数据维护
# Web_PO.opnLabel(d_menu_data['子机构数据维护'])
# Web_PO.swhLabel(2)



# todo 2.1, 数据维护 - 家医团队维护
# Web_PO.opnLabel(d_menu_data['家医团队维护'])
# Web_PO.swhLabel(1)

# todo 2.2, 数据维护 - 常用药物维护
# Web_PO.opnLabel(d_menu_data['常用药物维护'])
# Web_PO.swhLabel(2)

# todo 2.3, 数据维护 - 服务包管理
# Web_PO.opnLabel(d_menu_data['服务包管理'])
# Web_PO.swhLabel(1)

# todo 2.4, 数据维护 - 服务项管理
# Web_PO.opnLabel(d_menu_data['服务项管理'])
# Web_PO.swhLabel(2)

# todo 2.5, 数据维护 - 团队管理员
# Web_PO.opnLabel(d_menu_data['团队管理员'])
