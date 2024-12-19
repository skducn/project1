# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-12-19
# Description: 公卫 - 家医签约
# *****************************************************************

from GwPO import *
Gw_PO = GwPO()


# 1，登录
Gw_PO.login('http://192.168.0.203:30080/#/login', '11011', 'HHkk2327447')

# 获取家医签约二级菜单连接
Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li[4]", 2)  # 点击一级菜单家医签约
d_menu_sign = Gw_PO.getMenu2Url()
print('家医签约 =>', d_menu_sign)
# 家医签约 => {'签约居民概况': 'http://192.168.0.203:30080/Sign/jmsign/qyindex', '已签约居民': 'http://192.168.0.203:30080/Sign/jmsign/signed', '履约服务': 'http://192.168.0.203:30080/Sign/jmsign/qyservice', '归档记录': 'http://192.168.0.203:30080/Sign/jmsign/qyfile', '履约提醒': 'http://192.168.0.203:30080/Sign/jmsign/qyremind', '档案未签约': 'http://192.168.0.203:30080/Sign/jmsign/ready'}

# todo 4 家医签约

# todo 1.1, 居民签约管理 - 签约居民概况
# Web_PO.opnLabel(d_menu_sign['签约居民概况'])
# Web_PO.swhLabel(1)

# todo 1.2, 居民签约管理 - 已签约居民
# Web_PO.opnLabel(d_menu_sign['已签约居民'])
# Web_PO.swhLabel(1)

# todo 1.3, 居民签约管理 - 履约服务
# Web_PO.opnLabel(d_menu_sign['履约服务'])
# Web_PO.swhLabel(2)

# todo 1.4, 居民签约管理 - 归档记录
# Web_PO.opnLabel(d_menu_sign['归档记录'])
# Web_PO.swhLabel(1)

# todo 1.5, 居民签约管理 - 履约提醒
# Web_PO.opnLabel(d_menu_sign['履约提醒'])
# Web_PO.swhLabel(2)

# todo 1.6, 居民签约管理 - 档案未签约
# Web_PO.opnLabel(d_menu_sign['档案未签约'])
# Web_PO.swhLabel(1)



# todo 2.1, 冠心病患者管理 - 冠心病登记
# Web_PO.opnLabel(d_menu_sign['冠心病登记'])
# Web_PO.swhLabel(2)

# todo 2.2, 冠心病患者管理 - 冠心病管理
# Web_PO.opnLabel(d_menu_sign['冠心病管理'])



# todo 3.1, 脑卒中患者管理 - 脑卒中登记
# Web_PO.opnLabel(d_menu_sign['脑卒中登记'])
# Web_PO.swhLabel(2)

# todo 3.2, 脑卒中患者管理 - 脑卒中管理
# Web_PO.opnLabel(d_menu_sign['脑卒中管理'])
# Web_PO.swhLabel(2)



# todo 4.1, 高血脂管理 - 高血脂登记
# Web_PO.opnLabel(d_menu_sign['高血脂登记'])
# Web_PO.swhLabel(2)

# todo 4.2, 高血脂管理 - 高血脂专项
# Web_PO.opnLabel(d_menu_sign['高血脂专项'])
# Web_PO.swhLabel(2)

# todo 4.3, 高血脂管理 - 高血脂随访
# Web_PO.opnLabel(d_menu_sign['高血脂随访'])
# Web_PO.swhLabel(2)

