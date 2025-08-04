CREATE OR ALTER PROCEDURE CreateTestData104
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
                18 + ABS(CHECKSUM(NEWID())) % 60,  --18-77岁
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE())  -- 最近1年内
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
