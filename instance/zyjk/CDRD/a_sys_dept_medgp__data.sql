CREATE OR ALTER PROCEDURE a_sys_dept_medgp__data
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

        CREATE TABLE #Names (ID INT IDENTITY(1,1), Treat NVARCHAR(50));
        INSERT INTO #Names (Treat) VALUES ('治疗1组'),('治疗2组'),('治疗3组'),('治疗4组'),('治疗5组');

        -- 循环插入指定数量的记录
        WHILE @Counter <= @MaxRecords
        BEGIN
            -- 随机选择姓名和域名
            DECLARE @RandomTreat NVARCHAR(50);
            SELECT @RandomTreat = Treat FROM #Names WHERE ID = ABS(CHECKSUM(NEWID())) % 5 + 1;

            DECLARE @department_id int;
            SELECT TOP 1 @department_id = department_id FROM a_sys_department ORDER BY NEWID();

--             DECLARE @department_id int;
--             SELECT @department_id = department_id FROM a_sys_department WHERE department_id = ABS(CHECKSUM(NEWID())) % 10 + 1;

            -- 插入单条随机数据
            INSERT INTO a_sys_dept_medgp (department_id, department_treat_group_id, department_treat_group_name, department_treat_create_time)
            VALUES (
                    @department_id,   -- 科室ID
                    CAST(ABS(CHECKSUM(NEWID())) % 1000 AS int),   -- 医疗组ID
                    @RandomTreat + CAST(ABS(CHECKSUM(NEWID())) % 1000 AS NVARCHAR(10)),  -- 医疗组名称
                    DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()) -- 医疗组创建时间
            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_sys_dept_medgp);
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