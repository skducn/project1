# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-12-19
# Description: 公卫 - 三高共管
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
Gw_PO = GwPO_three(logName)
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('../config.ini')
# 登录
Gw_PO.login(Configparser_PO.HTTP("url"), Configparser_PO.ACCOUNT("user"), Configparser_PO.ACCOUNT("password"))
# 获取基本公卫二级菜单连接
Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li[3]", 2)  # 点击一级菜单三高共管
d_menu_basicPHS = Gw_PO.getMenu2Url()
print('d_menu_basicPHS =', d_menu_basicPHS)
# d_menu_basicPHS = {'三高共管概况': 'http://192.168.0.203:30080/three/ThreeHighs/general', '三高随访管理': 'http://192.168.0.203:30080/three/ThreeHighs/ThnVisitList', '心血管评估管理': 'http://192.168.0.203:30080/three/ThreeHighs/cardiovascularCheck', '并发症管理': 'http://192.168.0.203:30080/three/ThreeHighs/Complications', '三高患者管理': 'http://192.168.0.203:30080/three/ThreeHighs/ThnList', '冠心病登记': 'http://192.168.0.203:30080/three/Coronary/CHDregister', '冠心病管理': 'http://192.168.0.203:30080/three/Coronary/CHDfiles', '脑卒中登记': 'http://192.168.0.203:30080/three/Stroke/DNTregister', '脑卒中管理': 'http://192.168.0.203:30080/three/Stroke/DNTfiles', '高血脂登记': 'http://192.168.0.203:30080/three/Hyperlipidemia/gxzregister', '高血脂专项': 'http://192.168.0.203:30080/three/Hyperlipidemia/gxzspecial', '高血脂随访': 'http://192.168.0.203:30080/three/Hyperlipidemia/gxzsvisit'}

# todo 3 三高共管

# todo 1.1, 三高共管 - 三高共管概况
# Web_PO.opnLabel(d_menu_threeHighs['三高共管概况'])
# Web_PO.swhLabel(1)

# todo 1.2, 三高共管 - 三高随访管理
# Web_PO.opnLabel(d_menu_threeHighs['三高随访管理'])
# Web_PO.swhLabel(2)

# todo 1.1, 三高共管 - 心血管评估管理
# Web_PO.opnLabel(d_menu_threeHighs['心血管评估管理'])
# Web_PO.swhLabel(1)

# todo 1.2, 三高共管 - 并发症管理
# Web_PO.opnLabel(d_menu_threeHighs['心血管评估管理'])
# Web_PO.swhLabel(2)

# todo 1.1, 三高共管 - 三高患者管理
# Web_PO.opnLabel(d_menu_threeHighs['三高患者管理'])
# Web_PO.swhLabel(1)



# todo 2.1, 冠心病患者管理 - 冠心病登记
# Web_PO.opnLabel(d_menu_threeHighs['冠心病登记'])
# Web_PO.swhLabel(2)

# todo 2.2, 冠心病患者管理 - 冠心病管理
# Web_PO.opnLabel(d_menu_threeHighs['冠心病管理'])



# todo 3.1, 脑卒中患者管理 - 脑卒中登记
# Web_PO.opnLabel(d_menu_threeHighs['脑卒中登记'])
# Web_PO.swhLabel(2)

# todo 3.2, 脑卒中患者管理 - 脑卒中管理
# Web_PO.opnLabel(d_menu_threeHighs['脑卒中管理'])
# Web_PO.swhLabel(2)



# todo 4.1, 高血脂管理 - 高血脂登记
# Web_PO.opnLabel(d_menu_threeHighs['高血脂登记'])
# Web_PO.swhLabel(2)

# todo 4.2, 高血脂管理 - 高血脂专项
# Web_PO.opnLabel(d_menu_threeHighs['高血脂专项'])
# Web_PO.swhLabel(2)

# todo 4.3, 高血脂管理 - 高血脂随访
# Web_PO.opnLabel(d_menu_threeHighs['高血脂随访'])
# Web_PO.swhLabel(2)

