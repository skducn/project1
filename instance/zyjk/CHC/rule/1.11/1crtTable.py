# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-9-5
# Description: 创建表（覆盖，即如表存在先删除再创建）
# ensure_ascii=False 不将中文转换为ascii
#***************************************************************

from PO.SqlserverPO import *

# todo 社区健康平台
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")


# 创建表（覆盖，即如表存在先删除再创建），自增id主键PRIMARY KEY(id)
Sqlserver_PO.crtTableByCover('a_autoIdcard',
                           '''id INT IDENTITY(1,1) PRIMARY KEY,
                            tblName NVARCHAR(50),
                            idcard VARCHAR(18),
                            category VARCHAR(10),
                            userInfo VARCHAR(300)
                          ''')

# # 字典作为字符串插入表
# d_getUserInfo = {'doctorName': '小茄子'}
# s_getUserInfo = json.dumps(d_getUserInfo, ensure_ascii=False)
# Sqlserver_PO.execute("insert a_autoIdcard (tblName,idcard,category,userInfo) values ('%s','%s','%s','%s')" % (
# u'签约信息表,基本信息表,患者主索引表', str(310101198004110014), str(4), s_getUserInfo))






