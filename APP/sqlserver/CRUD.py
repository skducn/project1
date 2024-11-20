# -- coding: utf-8 --
# ***************************************************************
# Author     : John
# Data       : 2024-10-31
# Description: CRUD
# https://www.jb51.net/article/264740.htm
# ***************************************************************
"""
8.1 创建表（覆盖，即如表存在先删除再创建） crtTableByCover()
8.2 创建表（忽略，如原表存在则忽略不创建） crtTableByExistIgnore()
8.3 设置表注释（添加、修改、删除） setTableComment()
8.4 设置字段注释（添加、修改、删除） setFieldComment()
8.5 删除表 TRUNCATE TABLE
8.6 插入，插入1条记录，插入多条记录
8.7 更新
8.8 删除，删除1条记录，删除所有记录

8.9 删除表的所有外键关系 dropKey(varTable)

"""

from PO.SqlserverPO import *

# todo 社区健康平台
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")

# import json
# d_getUserInfo = {'doctorName': '小茄子'}
#
# s_getUserInfo = json.dumps(d_getUserInfo, ensure_ascii=False)
# Sqlserver_PO.execute("insert a_autoIdcard (tblName,idcard,category,userInfo) values ('%s','%s','%s','%s')" % (
# u'签约信息表,基本信息表,患者主索引表', str(310101198004110014), str(4), s_getUserInfo))


# print(str(d_getUserInfo))
# for k,v in d_getUserInfo.items():
#     Sqlserver_PO.execute("insert into a_autoIdcard (tblName,idcard) values ('%s','%s')" % (k,v ))

# todo 8.1 创建表（覆盖，即如表存在先删除再创建），自增id主键PRIMARY KEY(id)
Sqlserver_PO.crtTableByCover('a_autoIdcard',
                           '''id INT IDENTITY(1,1) PRIMARY KEY,
                            tblName NVARCHAR(50),
                            idcard VARCHAR(18),
                            category VARCHAR(10),
                            userInfo VARCHAR(300)
                          ''')

# Sqlserver_PO.crtTableByCover('a_autoIdcard',
#                            '''id INT NOT NULL,
#                             tblName VARCHAR(50),
#                             idcard VARCHAR(18),
#                             category VARCHAR(10),
#                             userInfo VARCHAR(300),
#                             PRIMARY KEY(id)
#                           ''')

# Sqlserver_PO.crtTableByCover('a_api_wow_info',
#                            '''id INT NOT NULL,
#                             name1 VARCHAR(100),
#                             salesrep VARCHAR(100),
#                             bir DATETIME not null,
#                             ff varchar(12) not null default 123,
#                             PRIMARY KEY(id)
#                           ''')


# todo 8.2 创建表（忽略，如原表存在则忽略不创建）,自增id主键IDENTITY(1,1) PRIMARY KEY
# Sqlserver_PO.crtTableByExistIgnore('a_api_wow_info', '''
#     id INT IDENTITY(1,1) PRIMARY KEY,
#     phsField VARCHAR(20) NOT NULL,
#     phsValue VARCHAR(20) NOT NULL,
#     phusersField VARCHAR(20) NOT NULL,
#     phusersValue VARCHAR(20) NOT NULL''')

# todo 8.3 设置表注释（添加、修改、删除）
# Sqlserver_PO.setTableComment('a_api_wow_info2', "测试123")
# Sqlserver_PO.setTableComment('a_api_wow_info2', "测试", True)  # 删除注释

# todo 8.4 设置表字段（添加、修改、删除）
# Sqlserver_PO.setFieldComment('t_user','ID','编号')
# Sqlserver_PO.setFieldComment('t_user','ID','编号', True) 删除字段注释

# todo 8.5 删除表
# Sqlserver_PO.execute("DROP TABLE a_test")
# todo 8.6 插入1条记录
# Sqlserver_PO.execute("INSERT INTO a_api_wow_info values(4, 'John Smith6662','John Doe3', '2020-12-12', '123')")


# todo 插入多条记录
# Sqlserver_PO.executemany("INSERT INTO a_test VALUES (%d, %s, %s)", [(1, 'John Smith2', 'John Doe3'), (2, 'Jane Doe', 'Joe Dog'), (3, 'Mike T.', 'Sarah H.')])
# todo 8.7 更新数据
# Sqlserver_PO.execute("UPDATE a_test set name='john123' where id=1")
# todo 8.8 删除1条记录
# Sqlserver_PO.execute("DELETE FROM a_test WHERE id = 2")
# todo 删除所有记录
# Sqlserver_PO.execute("TRUNCATE TABLE a_test")






