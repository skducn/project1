CREATE OR ALTER PROCEDURE cdrd_patient_info__data
    @RecordCount INT = 3 -- 可通过参数控制记录数，默认100条
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

        CREATE TABLE #Names (ID INT IDENTITY(1,1), Department NVARCHAR(50), Name NVARCHAR(50));
        INSERT INTO #Names (Department, Name) VALUES ('内科','东大名'),('外科','朴志镐'),('妇产科','洁神明'),('儿科','苗胸'),('肿瘤科','格格'),('五官科','张桂芳'),('其他临床科室','金制成'),('医技科室','孙俪'),('内分泌科','濮存昕'),('骨科','黎明');

        -- 循环插入指定数量的记录
        WHILE @Counter <= @MaxRecords
        BEGIN
            --             随机获取手机号
            DECLARE @phone NVARCHAR(50);
            SELECT @phone = '1' + RIGHT('00000000' + CAST(ABS(CHECKSUM(NEWID())) % 99999999 AS VARCHAR(8)), 8);
            PRINT'生成手机号: ' + @phone;

            IF OBJECT_ID('tempdb..#Debug') IS NOT NULL DROP TABLE #Debug;
            CREATE TABLE #Debug (Msg NVARCHAR(MAX));

            -- 在需要打印的地方插入记录
            INSERT INTO #Debug (Msg) VALUES ('生成手机号: ' + @phone);

            -- 最后输出调试信息
            SELECT * FROM #Debug;

--             添加延迟让 PRINT 内容有机会输出
--             WAITFOR DELAY '00:00:07'; -- 等待2秒
--             ROLLBACK TRANSACTION; -- 如果已经开启事务，则回滚
--             RETURN;
--             SELECT '1' + RIGHT('00000000' + CAST(ABS(CHECKSUM(NEWID())) % 99999999 AS VARCHAR(8)), 8) AS Mobile
--             SELECT @RandomDepartment = Department FROM #Names WHERE ID = ABS(CHECKSUM(NEWID())) % 10;


            -- 随机出生日期（年龄范围：18-60岁）
            SELECT DATEADD(YEAR, - (18 + ABS(CHECKSUM(NEWID())) % 43), GETDATE()) AS BirthDate

            -- 随机身份证号（中国大陆格式
            -- 前6位模拟地区码（可替换为真实省份编码）
            DECLARE @AreaCode CHAR(6) = '440000'; -- 示例：广东
            -- 生成年份（1960-2005）
            DECLARE @Year INT = 1960 + ABS(CHECKSUM(NEWID())) % 45;
            -- 月份和日期
            DECLARE @Month INT = 1 + ABS(CHECKSUM(NEWID())) % 12;
            DECLARE @Day INT = 1 + ABS(CHECKSUM(NEWID())) % 28;

            -- 构造身份证号前17位
            DECLARE @BaseID NVARCHAR(17) = @AreaCode +
                                           RIGHT('00' + CAST(@Year AS VARCHAR), 4) +
                                           RIGHT('00' + CAST(@Month AS VARCHAR), 2) +
                                           RIGHT('00' + CAST(@Day AS VARCHAR), 2) +
                                           RIGHT('000' + CAST(ABS(CHECKSUM(NEWID())) % 999 AS VARCHAR), 3);
            -- 校验位计算（简化处理）
            SELECT @BaseID + 'X' AS IDCardNumber

            -- 随机地址（街道+门牌号）
--             SELECT @RandomProvince + '某路' + CAST(ABS(CHECKSUM(NEWID())) % 100 AS VARCHAR) + '号' AS Address

            -- 随机选择科室和姓
            DECLARE @RandomDepartment NVARCHAR(50);
            SELECT @RandomDepartment = Department FROM #Names WHERE ID = ABS(CHECKSUM(NEWID())) % 10;
            DECLARE @RandomName NVARCHAR(50);
            SELECT @RandomName = Name FROM #Names WHERE ID = ABS(CHECKSUM(NEWID())) % 10;

--             -- 插入单条随机数据
--             INSERT INTO a_sys_department (department_name, department_code, department_charge_id, department_charge_job_num,
--             department_charge_name,department_creater_name,department_create_time)
--             VALUES (
--                 @RandomDepartment + RIGHT('0000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000), 4), -- 科室名称 + 固定4位数
-- --                 @RandomDepartment + CAST(ABS(CHECKSUM(NEWID())) % 10000 AS NVARCHAR(10)), --科室名称
--                 RIGHT('0000000' + CAST(ABS(CHECKSUM(NEWID())) % 10000000 AS VARCHAR(20)), 7), -- 科室编码
--                 CAST(ABS(CHECKSUM(NEWID())) % 10000 AS int), -- 科室负责人ID
--                 CAST(ABS(CHECKSUM(NEWID())) % 10000 AS NVARCHAR(10)), -- 科室负责人工号
--                 @RandomName + RIGHT('00000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100000), 5), -- 科室负责人姓名 + 固定5位数
-- --                 @RandomName + RIGHT('00000' + CAST(ABS(CHECKSUM(NEWID())) % 100000 AS VARCHAR(20)), 5), -- 科室负责人姓名
--                 @RandomName, -- 创建人
--                 DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()) -- 创建时间
--             );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_sys_department);
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