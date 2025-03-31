# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-7-25
# Description: 社区健康管理中心 - 居民健康服务 - 老年人体检
# 测试环境 # http://192.168.0.243:8010/#/login
# 'cs', '12345678'
#***************************************************************

import sys,os
# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取 上层 目录的绝对路径
project_dir = os.path.abspath(os.path.join(current_dir, '..'))
# 将 上层 目录添加到 sys.path
sys.path.insert(0, project_dir)
from ChcPO_quanqu import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Chc_PO_quanqu = ChcPO_quanqu(logName)
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')
# 登录
Chc_PO_quanqu.login(Configparser_PO.HTTP("url"), Configparser_PO.ACCOUNT("user"), Configparser_PO.ACCOUNT("password"))
# d_menu = Chc_PO_quanqu.getMenu2Url()
# print('d_menu =', d_menu)
d_menu = {'首页': 'http://192.168.0.243:8010/#/index', '健康服务': 'http://192.168.0.243:8010/#/SignManage/service', '健康评估及干预': 'http://192.168.0.243:8010/#/SignManage/signAssess', '慢病管理': 'http://192.168.0.243:8010/#/SignManage/chronic', '老年人体检': 'http://192.168.0.243:8010/#/SignManage/snrExam', '重点人群': 'http://192.168.0.243:8010/#/SignManage/keyPopulation', '居民登记': 'http://192.168.0.243:8010/#/OpManage/register', '健康评估': 'http://192.168.0.243:8010/#/OpManage/assess', '机构维护': 'http://192.168.0.243:8010/#/UserManage/org', '用户维护': 'http://192.168.0.243:8010/#/UserManage/user', '角色维护': 'http://192.168.0.243:8010/#/UserManage/role', '接口管理': 'http://192.168.0.243:8010/#/UserManage/interface', '批量评估': 'http://192.168.0.243:8010/#/UserManage/MassAppraisal', '错误日志': 'http://192.168.0.243:8010/#/UserManage/errorLog', '报告模板引用': 'http://192.168.0.243:8010/#/UserManage/templateReference', '报告模板管理': 'http://192.168.0.243:8010/#/UserManage/templateManage', '常住人口': 'http://192.168.0.243:8010/#/Community/permanent', '家医团队维护': 'http://192.168.0.243:8010/#/Community/team', '家医助手': 'http://192.168.0.243:8010/#/Community/assistant', '干预规则配置': 'http://192.168.0.243:8010/#/Community/interveneRule', '打印': 'http://192.168.0.243:8010/#/Community/print', '停止评估名单': 'http://192.168.0.243:8010/#/Community/stopList', '社区用户维护': 'http://192.168.0.243:8010/#/Community/communityUser', '评估建议': 'http://192.168.0.243:8010/#/Community/SuggestionTemplate', '定时任务': 'http://192.168.0.243:8010/#/monitor/index', '社区健康评估': 'http://192.168.0.243:8010/#/dataStatistics/communityHealth', '全区健康评估': 'http://192.168.0.243:8010/#/dataStatistics/allHealth', '全区评估率': 'http://192.168.0.243:8010/#/dataStatistics/allAssessRate', '社区评估率': 'http://192.168.0.243:8010/#/dataStatistics/communityAssessRate', '档案首页': 'http://192.168.0.243:8010/#/HealthRecord/archiveIndex', '居民评估报告': 'http://192.168.0.243:8010/#/HealthManage/AssessReport'}
Web_PO.opnLabel(d_menu["老年人体检"])
Web_PO.swhLabel(1)



# todo 查询
# Chc_PO_quanqu.query({"身份证号": "310110194304210023"})
Chc_PO_quanqu.query({"姓名": "张三", "身份证号": "410203196112238333", "家庭医生": "小猴子" })



