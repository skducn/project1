-- 修改存储过程以满足新的需求
CREATE OR ALTER PROCEDURE s_sys_dept_medgp_person
    @RecordCount INT = 5,  -- 每个医疗组的人员数
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- 清空旧数据
--     DELETE FROM SYS_DEPT_MEDGP_PERSON;

    -- 声明变量
    DECLARE @department_treat_group_id INT;
    DECLARE @department_id INT;
    DECLARE @counter INT;
    DECLARE @user_id INT;
    DECLARE @user_name NVARCHAR(20);
    DECLARE @job_num NVARCHAR(20);

    -- 声明游标，遍历sys_dept_medgp表中的医疗组
    DECLARE medgp_cursor CURSOR FOR
    SELECT department_treat_group_id, department_id
    FROM sys_dept_medgp;

    OPEN medgp_cursor;
    FETCH NEXT FROM medgp_cursor INTO @department_treat_group_id, @department_id;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        SET @counter = 1;
        -- 为每个医疗组分配指定数量的用户
        WHILE @counter <= @RecordCount
        BEGIN
            -- 从sys_user中选择一个属于该科室的用户
            SELECT TOP 1 @user_id = user_id ,@user_name = user_name, @job_num = job_num
            FROM sys_user
            WHERE department_id = @department_id
            ORDER BY user_id;  -- 按用户ID顺序选择

            -- 如果找到了用户，则生成姓名和工号并插入记录
            IF @user_id IS NOT NULL
            BEGIN
                -- 插入到SYS_DEPT_MEDGP_PERSON表中
                INSERT INTO SYS_DEPT_MEDGP_PERSON (user_id, department_treat_group_id, user_name, user_job_num)
                VALUES (@user_id, @department_treat_group_id, @user_name, @job_num);
            END

            SET @counter = @counter + 1;
        END

        FETCH NEXT FROM medgp_cursor INTO @department_treat_group_id, @department_id;
    END

    CLOSE medgp_cursor;
    DEALLOCATE medgp_cursor;

    SET @result = @RecordCount;
END;
