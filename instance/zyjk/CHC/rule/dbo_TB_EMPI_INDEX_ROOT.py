# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-9-5
# Description: TB_EMPI_INDEX_ROOT(患者主索引表)
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



def insert_TB_EMPI_INDEX_ROOT(varIdcard):


    # 3.1 删除, TB_EMPI_INDEX_ROOT(患者主索引表)
    Sqlserver_PO.execute("delete from TB_EMPI_INDEX_ROOT where IDCARDNO = '%s'" % (varIdcard))

    # 3.2 插入, TB_EMPI_INDEX_ROOT(患者主索引表)
    Sqlserver_PO.execute("insert into TB_EMPI_INDEX_ROOT(GUID, NAME, IDCARDNO) values('%s', '%s', '%s')" % (Data_PO.getFigures(8), Data_PO.getChineseName(), varIdcard))

    Color_PO.outColor([{"35": "患者主索引表 => select * from TB_EMPI_INDEX_ROOT where IDCARDNO = '" + str(varIdcard) + "'"}])


insert_TB_EMPI_INDEX_ROOT("150600195807117794")



