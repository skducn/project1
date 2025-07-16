-- todo 医疗组人员表(造数据)
-- 1个科室，每个科室3个医疗组，每个医疗组下5个人

CREATE OR ALTER PROCEDURE sys_dept_medgp_person
    @RecordCount INT = 15,  -- 每个科室3个医疗组，每个医疗组下5个人
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    SET @result = @RecordCount

    -- 循环插入指定数量的记录
    DECLARE @Counter INT = 1;
    WHILE @Counter <= 3  -- 每组科室
    BEGIN

--         DECLARE @RandomDepartment_treat_group_id int;
--         SELECT @RandomDepartment_treat_group_id = department_treat_group_id FROM a_sys_dept_medgp WHERE department_treat_group_id = @Counter;

        -- 循环插入指定数量的记录
        DECLARE @Counter2 INT = 1;
        WHILE @Counter2 <= 5  -- 每组科室下5人
        BEGIN

            -- 子存储过程
            -- 姓名
            DECLARE @RandomName NVARCHAR(50);
            EXEC p_name @FullName = @RandomName OUTPUT;

            -- 插入单条随机数据
            INSERT INTO a_sys_dept_medgp_person (user_id, department_treat_group_id, user_name, user_job_num)
            VALUES (
                    CAST(ABS(CHECKSUM(NEWID())) % 10000 AS int),   -- 用户ID
                    @Counter,   -- 医疗组ID
                    @RandomName, -- 姓名
                    CAST(ABS(CHECKSUM(NEWID())) % 100000 AS NVARCHAR(10)) -- 工号
            );
            SET @Counter2 = @Counter2 + 1;
        END;

        SET @Counter = @Counter + 1;
    END;


END;