CREATE OR ALTER PROCEDURE a_sys_dept_medgp_person__data
    @RecordCount INT = 10 -- 可通过参数控制记录数，默认100条
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

        CREATE TABLE #Names (ID INT IDENTITY(1,1), Name NVARCHAR(50));
        INSERT INTO #Names (Name) VALUES ('东大名'),('朴志镐'),('洁神明'),('苗胸'),('格格'),('张桂芳'),('金制成'),('孙俪'),('濮存昕'),('黎明');

        -- 循环插入指定数量的记录
        WHILE @Counter <= @MaxRecords
        BEGIN
            -- 随机选择姓名和域名
            DECLARE @RandomName NVARCHAR(50);
            SELECT @RandomName = Name FROM #Names WHERE ID = ABS(CHECKSUM(NEWID())) % 10;

            DECLARE @RandomDepartment_treat_group_id int;
            SELECT TOP 1 @RandomDepartment_treat_group_id = department_treat_group_id FROM a_sys_dept_medgp ORDER BY NEWID();

--             DECLARE @RandomDepartment_treat_group_id int;
--             SELECT @RandomDepartment_treat_group_id = department_treat_group_id FROM a_treat WHERE department_id = @RandomId;

            -- 插入单条随机数据
            INSERT INTO a_sys_dept_medgp_person (department_treat_group_id, user_id, user_name, user_job_num)
            VALUES (
                    @RandomDepartment_treat_group_id,   -- 治疗组ID
                    CAST(ABS(CHECKSUM(NEWID())) % 10000 AS int),   -- 用户ID
                    @RandomName + CAST(ABS(CHECKSUM(NEWID())) % 1000 AS NVARCHAR(10)),  -- 姓名
                    CAST(ABS(CHECKSUM(NEWID())) % 100000 AS NVARCHAR(10)) -- 工号
            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_sys_dept_medgp_person);
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