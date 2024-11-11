# -- coding: utf-8 --
# ***************************************************************
# Author     : John
# Data       : 2024-10-31
# Description: test
# https://www.jb51.net/article/264740.htm
# ***************************************************************
from PO.SqlserverPO import *

# todo 社区健康平台
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")

# print(Sqlserver_PO._genTypeValue("a_api_wow_info"))  # {'ID': 1, 'NAME': 'a', 'AGE': 1, 'ADDRESS': 'a', 'SALARY': 1.0, 'time': '08:12:23'}
# Sqlserver_PO.genFirstRecord('a_api_wow_info')

# Sqlserver_PO.genRecord('a_api_wow_info')

# 删除字段id
# Sqlserver_PO.execute("alter table a_api_wow_info drop column id")
# 新增字段id
# Sqlserver_PO.execute("alter table a_api_wow_info add id type not null default 0 ")


# Sqlserver_PO.delIdentityPrimaryKey('a_api_wow_info','id')
# Sqlserver_PO.setIdentityPrimaryKey('a_api_wow_info','id')

# 查找表的主键PK
a = Sqlserver_PO.select("SELECT * FROM sys.key_constraints WHERE type = 'PK' AND OBJECT_NAME(parent_object_id) = 'a_api_wow_info'")
print(a)
#
Sqlserver_PO.execute("alter TABLE a_api_wow_info DROP CONSTRAINT PK__a_api_wo__3213E83F3084ADB7")
