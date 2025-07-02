CREATE OR ALTER PROCEDURE a_sys_department__data
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
--         INSERT INTO #Names (Department, Name) VALUES ('内科'),('外科'),('妇产科'),('儿科'),('肿瘤科'),('五官科'),('其他临床科室'),('医技科室'),('内分泌科'),('骨科');
        INSERT INTO #Names (Department, Name) VALUES ('内科','东大名'),('外科','朴志镐'),('妇产科','洁神明'),('儿科','苗胸'),('肿瘤科','格格'),('五官科','张桂芳'),('其他临床科室','金制成'),('医技科室','孙俪'),('内分泌科','濮存昕'),('骨科','黎明');
--         INSERT INTO #Names (Name) VALUES ('东大名'),('朴志镐'),('洁神明'),('苗胸'),('格格'),('张桂芳'),('金制成'),('孙俪'),('濮存昕'),('黎明');

        -- 循环插入指定数量的记录
        WHILE @Counter <= @MaxRecords
        BEGIN
            -- 随机选择科室和姓
            DECLARE @RandomDepartment NVARCHAR(50);
            SELECT @RandomDepartment = Department FROM #Names WHERE ID = ABS(CHECKSUM(NEWID())) % 10;
            DECLARE @RandomName NVARCHAR(50);
            SELECT @RandomName = Name FROM #Names WHERE ID = ABS(CHECKSUM(NEWID())) % 10;

            -- 插入单条随机数据
            INSERT INTO a_sys_department (department_name, department_code, department_charge_id, department_charge_job_num,
            department_charge_name,department_creater_name,department_create_time)
            VALUES (
                @RandomDepartment + RIGHT('0000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000), 4), -- 科室名称 + 固定4位数
--                 @RandomDepartment + CAST(ABS(CHECKSUM(NEWID())) % 10000 AS NVARCHAR(10)), --科室名称
                RIGHT('0000000' + CAST(ABS(CHECKSUM(NEWID())) % 10000000 AS VARCHAR(20)), 7), -- 科室编码
                CAST(ABS(CHECKSUM(NEWID())) % 10000 AS int), -- 科室负责人ID
                CAST(ABS(CHECKSUM(NEWID())) % 10000 AS NVARCHAR(10)), -- 科室负责人工号
                @RandomName + RIGHT('00000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100000), 5), -- 科室负责人姓名 + 固定5位数
--                 @RandomName + RIGHT('00000' + CAST(ABS(CHECKSUM(NEWID())) % 100000 AS VARCHAR(20)), 5), -- 科室负责人姓名
                @RandomName, -- 创建人
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()) -- 创建时间
            );

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