# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-12-19
# Description: 公卫 - 系统配置
# *****************************************************************

from GwPO import *
Gw_PO = GwPO()

# 1，登录
Gw_PO.login('http://192.168.0.203:30080/#/login', '11011', 'HHkk2327447')


# 获取系统配置二级菜单连接
Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li[6]", 2)  # 点击一级菜单系统配置
d_menu_system = Gw_PO.getMenu2Url()
print('系统配置 =>', d_menu_system)
# 系统配置 => {'定时任务': 'http://192.168.0.203:30080/system/monitor/dsindex', '系统配置': 'http://192.168.0.203:30080/system/monitor/config', '缓存监控': 'http://192.168.0.203:30080/system/monitor/cache', '缓存列表': 'http://192.168.0.203:30080/system/monitor/cachelist', '医院维护': 'http://192.168.0.203:30080/system/OrgManage/HospitalMaintain', '用户维护': 'http://192.168.0.203:30080/system/UserManage/UserMaintain', '角色维护': 'http://192.168.0.203:30080/system/UserManage/RoleMaintain'}

# todo 7 系统配置

# todo 1.1, 系统配置 - 定时任务
# Web_PO.opnLabel(d_menu_system['定时任务'])
# Web_PO.swhLabel(1)

# todo 1.2, 系统配置 - 系统配置
# Web_PO.opnLabel(d_menu_system['系统配置'])
# Web_PO.swhLabel(2)

# todo 1.3, 系统配置 - 缓存监控
# Web_PO.opnLabel(d_menu_system['缓存监控'])
# Web_PO.swhLabel(1)

# todo 1.4, 数系统配置据统计 - 缓存列表
# Web_PO.opnLabel(d_menu_system['缓存列表'])
# Web_PO.swhLabel(2)




# todo 2.1, 机构管理 - 医院维护
# Web_PO.opnLabel(d_menu_system['医院维护'])
# Web_PO.swhLabel(1)



# todo 3.1, 用户管理 - 用户维护
# Web_PO.opnLabel(d_menu_system['用户维护'])
# Web_PO.swhLabel(2)

# todo 3.2, 用户管理 - 角色维护
# Web_PO.opnLabel(d_menu_system['角色维护'])
