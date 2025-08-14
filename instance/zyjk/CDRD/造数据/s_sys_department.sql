-- todo 科室表(造数据)
-- 20个科室，每个科室2个医疗组，每个医疗组下5个人

CREATE OR ALTER PROCEDURE s_sys_department
    @RecordCount INT = 20,  -- N个科室
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    SET @result = @RecordCount

    -- 循环插入指定数量的记录
    DECLARE @Counter INT = 1;
    WHILE @Counter <= @RecordCount
    BEGIN
        -- 子存储过程
        -- 科室
        DECLARE @RandomDepartment NVARCHAR(50);
        EXEC p_dept @RandomID = @Counter, @v = @RandomDepartment OUTPUT;

        -- 姓名
        DECLARE @RandomName NVARCHAR(50);
        EXEC p_name @FullName = @RandomName OUTPUT;


        -- 插入单条随机数据
        INSERT INTO SYS_DEPARTMENT (department_name, department_code, department_charge_id, department_charge_job_num,
        department_charge_name,department_creater_name,department_create_time)
        VALUES (
            @RandomDepartment, -- 科室名称
            RIGHT('0000000' + CAST(ABS(CHECKSUM(NEWID())) % 10000000 AS VARCHAR(20)), 7), -- 科室编码
            CAST(ABS(CHECKSUM(NEWID())) % 10000 AS int), -- 科室负责人ID
            CAST(ABS(CHECKSUM(NEWID())) % 10000 AS NVARCHAR(10)), -- 科室负责人工号
            @RandomName + RIGHT('00000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100000), 5), -- 科室负责人姓名 + 固定5位数
            @RandomName, -- 创建人
            DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()) -- 创建时间
        );

        SET @Counter = @Counter + 1;
    END;


END;