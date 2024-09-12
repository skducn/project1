# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-9-5
# Description: HRPERSONBASICINFO(基本信息表)
# 测试环境 # http://192.168.0.243:8010/#/login
# 'cs', '12345678'
#***************************************************************

from PO.DataPO import *
Data_PO = DataPO()

from PO.FakePO import *
Fake_PO = FakePO()

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO(Configparser_PO.DB_SQL("host"), Configparser_PO.DB_SQL("user"), Configparser_PO.DB_SQL("password"), Configparser_PO.DB_SQL("database"), Configparser_PO.DB_SQL("charset"))
Sqlserver_PO2 = SqlServerPO(Configparser_PO.DB_SQL("host"), Configparser_PO.DB_SQL("user"), Configparser_PO.DB_SQL("password"), Configparser_PO.DB_SQL("database2"), Configparser_PO.DB_SQL("charset"))


def insert_HRPERSONBASICINFO(varIdcard):

    # 1.1 删除, HRPERSONBASICINFO(基本信息表)
    Sqlserver_PO.execute("delete from HRPERSONBASICINFO where ARCHIVENUM = '%s'" % (varIdcard))

    # 1.2 插入, HRPERSONBASICINFO(基本信息表)
    Sqlserver_PO.execute('set identity_insert HRPERSONBASICINFO on')
    r = Sqlserver_PO.select('select max(ID) as qty from HRPERSONBASICINFO')
    id = r[0]['qty'] + 1
    Sqlserver_PO.execute("insert into HRPERSONBASICINFO(ARCHIVENUM,NAME,sex,IDCARD,CREATETIME,ID,ISGOVERNANCE) "
                         "values ('%s', '%s', '1', '%s','%s', %s, '0')"
                         % (varIdcard, Data_PO.getChineseName(), varIdcard, time.strftime("%Y-%m-%d %H:%M:%S.000"),
                            str(id)))
    Sqlserver_PO.execute('set identity_insert HRPERSONBASICINFO off')

    Color_PO.outColor([{"35": "基本信息表 => select * from HRPERSONBASICINFO where ARCHIVENUM = '" + str(varIdcard) + "'"}])


insert_HRPERSONBASICINFO("150600195807117794")


