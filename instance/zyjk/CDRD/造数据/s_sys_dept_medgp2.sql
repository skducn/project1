-- todo 科室医疗组表(造数据)
-- 每个科室下2个医疗组，每个医疗组下5个人

CREATE OR ALTER PROCEDURE s_sys_dept_medgp
    @RecordCount INT = 2,   -- N个医疗组
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    SET @result = @RecordCount

    -- 预生成随机数据所需的基础数据
    IF OBJECT_ID('tempdb..#Names') IS NOT NULL DROP TABLE #Names;
    CREATE TABLE #tb_temp (ID INT IDENTITY(1,1), Treat NVARCHAR(50));
    INSERT INTO #tb_temp (Treat) VALUES (N'治疗1组'),(N'治疗2组');

    -- 循环插入指定数量的记录
    DECLARE @Counter INT = 1;
    WHILE @Counter <= @RecordCount
    BEGIN
        -- 顺序获取医疗组
        DECLARE @Treat NVARCHAR(50);
        SELECT @Treat = Treat FROM #tb_temp WHERE ID = @Counter; -- 默认按顺序输出

        -- 获取1个科室id
        DECLARE @department_id int;
        SELECT @department_id = department_id FROM SYS_DEPARTMENT;

        -- 插入单条随机数据
        INSERT INTO SYS_DEPT_MEDGP (department_id, department_treat_group_name, department_treat_create_time)
        VALUES (
                @department_id,   -- 科室ID
                @Treat, -- 医疗组名称
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()) -- 医疗组创建时间
        );

        SET @Counter = @Counter + 1;
    END;


END;