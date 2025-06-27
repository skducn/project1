# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-3-27
# Description   : sqlserverApp
# *********************************************************************

from PO.SqlserverPO import *

# todo 社区健康平台（静安）
# Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC_JINGAN", "GBK")

# todo 社区健康平台（全市）
# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS", "GBK")
# Sqlserver_PO2 = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "ZYCONFIG", "GBK")



Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC_5G", "GBK")

# 创建表
# Sqlserver_PO.crtTableByCover('a_test',
#                                    '''UserId INT IDENTITY(1,1) PRIMARY KEY,
#                                     UserName NVARCHAR(50),
#                                     Email NVARCHAR(500),
#                                     Age int,
#                                     CreatedDate DATETIME
#                                   ''')


# 创建存储过程，方法1 执行
sql = """
CREATE OR ALTER PROCEDURE CreateTestData102
    @RecordCount INT = 100 -- 可通过参数控制记录数，默认100条
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRANSACTION;
        
        DECLARE @Counter INT = 1;
        DECLARE @TotalCount INT =0;
        DECLARE @MaxRecords INT = @RecordCount;
        
        -- 预生成随机数据所需的基础数据
        IF OBJECT_ID('tempdb..#Names') IS NOT NULL DROP TABLE #Names;
        IF OBJECT_ID('tempdb..#Domains') IS NOT NULL DROP TABLE #Domains;
        
        CREATE TABLE #Names (ID INT IDENTITY(1,1), Name NVARCHAR(50));
        CREATE TABLE #Domains (ID INT IDENTITY(1,1), Domain NVARCHAR(50));
        
        INSERT INTO #Names (Name) VALUES ('张三'),('李四'),('王五'),('赵六'),('钱七'),('孙八'),('周九'),('吴十'),('郑十一'),('王十二');
        INSERT INTO #Domains (Domain) VALUES ('example.com'),('test.com'),('demo.org'),('sample.net');
        
        -- 循环插入指定数量的记录
        WHILE @Counter <= @MaxRecords
        BEGIN
            -- 随机选择姓名和域名
            DECLARE @RandomName NVARCHAR(50);
            DECLARE @RandomDomain NVARCHAR(50);
            
            SELECT @RandomName = Name FROM #Names WHERE ID = ABS(CHECKSUM(NEWID())) % 10 + 1;
            SELECT @RandomDomain = Domain FROM #Domains WHERE ID = ABS(CHECKSUM(NEWID())) % 4 + 1;
            
            -- 插入单条随机数据
            INSERT INTO a_test (UserName, Email, Age, CreatedDate)
            VALUES (
                @RandomName + CAST(ABS(CHECKSUM(NEWID())) % 100 AS NVARCHAR(10)),
                LOWER(@RandomName) + CAST(ABS(CHECKSUM(NEWID())) % 1000 AS NVARCHAR(10)) + '@' + @RandomDomain,
                18 + ABS(CHECKSUM(NEWID())) % 60,
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE())
            );
                        
            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_test);
        END;
        
        -- 返回插入的记录数
        SELECT @RecordCount AS RequestedCount, @TotalCount AS TotalCount;
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
            
        THROW;
    END CATCH;
END;
"""
# Sqlserver_PO.execute(sql)


# 创建存储过程，方法2，外部读取存储过程sql文件
# with open("CreateTestData104.sql", 'r', encoding='utf-8') as file:
#     sql_script = file.read()
# Sqlserver_PO.execute(sql_script)


# 执行存储过程
# Sqlserver_PO.execute("exec CreateTestData100 @RecordCount=5;")   # 插入5条记录
# Sqlserver_PO.execCall("CreateTestData102",  (6,))   # 插入6条记录
# Sqlserver_PO.execCall("CreateTestData104",  (6,))   # 插入6条记录


# print("7.1 查看表结构".center(100, "-"))
# Sqlserver_PO.desc()
# Sqlserver_PO.desc(['id', 'page'])
# Sqlserver_PO.desc('a_c%')
# Sqlserver_PO.desc({'a_%':['id','sql']})
# Sqlserver_PO.desc('QYYH')
# Sqlserver_PO.desc({'a_test':['number', 'rule1']})

# print("7.2 查找记录".center(100, "-"))
# Sqlserver_PO.record('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
# Sqlserver_PO.record('*', 'varchar', '%13710078886%', False)
# Sqlserver_PO.record('*', 'varchar', '%基础服务包（2019版）%')
# Sqlserver_PO.record('*', 'varchar', '%13710078886%')
# Sqlserver_PO.record('*', 'varchar', u'%ef04737c5b4f4b93be85576e58b97ff2%')
# Sqlserver_PO.record('*', 'varchar', u'%310101195001293595%')
# Sqlserver_PO.record('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# Sqlserver_PO.record('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。

# print("7.3 插入记录".center(100, "-"))
# Sqlserver_PO.insert("a_test", {'result': str(Fake_PO.genPhone_number('Zh_CN', 1)), 'createDate': Time_PO.getDateTimeByPeriod(0), 'ruleParam': 'param'})


