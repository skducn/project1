-- todo 科室医疗组表(造数据)
-- 每个科室下2个医疗组，每个医疗组下5个人

CREATE OR ALTER PROCEDURE s_sys_dept_medgp
    @RecordCount INT = 2,   -- N个医疗组
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;   --阻止SQL Server返回受影响行数的信息，提高性能
    SET XACT_ABORT ON;  --当T-SQL语句产生运行时错误时，强制事务自动回滚

    SET @result = @RecordCount

    -- 预生成随机数据所需的基础数据
    IF OBJECT_ID('tempdb..#Names') IS NOT NULL DROP TABLE #Names;
    CREATE TABLE #tb_temp (ID INT IDENTITY(1,1), Treat NVARCHAR(50));
    INSERT INTO #tb_temp (Treat) VALUES (N'治疗1组'),(N'治疗2组');

    -- 声明科室游标
    -- 定义游标 dept_cursor，用于遍历 SYS_DEPARTMENT 表中的所有科室ID
    DECLARE @department_id INT;
    DECLARE dept_cursor CURSOR FOR
    SELECT department_id FROM SYS_DEPARTMENT;

    -- 打开游标
    OPEN dept_cursor;
    -- 从游标中获取第一条记录的科室ID
    FETCH NEXT FROM dept_cursor INTO @department_id;

    -- 遍历所有科室
    -- 当游标成功获取记录时继续循环（@@FETCH_STATUS = 0 表示成功获取记录）
    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- 循环插入指定数量的记录
        DECLARE @Counter INT = 1;
        WHILE @Counter <= @RecordCount
        BEGIN
            -- 获取医疗组
            DECLARE @Treat NVARCHAR(50);
            SELECT @Treat = Treat FROM #tb_temp WHERE ID = @Counter; -- 从临时表中按顺序获取医疗组名称

            -- 插入单条随机数据
            INSERT INTO SYS_DEPT_MEDGP (department_id, department_treat_group_name, department_treat_create_time)
            VALUES (
                    @department_id,   -- 科室ID
                    @Treat, -- 医疗组名称
                    DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()) -- 医疗组创建时间，生成过去一年内的随机日期作为创建时间
            );

            SET @Counter = @Counter + 1;
        END;

        -- 获取下一个科室ID
        FETCH NEXT FROM dept_cursor INTO @department_id;
    END;

    -- 关闭并释放游标
    CLOSE dept_cursor;
    DEALLOCATE dept_cursor;

END;
