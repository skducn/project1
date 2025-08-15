-- 修改存储过程以满足新的需求
CREATE OR ALTER PROCEDURE s_sys_dept_medgp_person
    @RecordCount INT = 5,  -- 每个医疗组的人员数
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- 声明变量
    DECLARE @department_treat_group_id INT;
    DECLARE @department_id INT;
    DECLARE @counter INT;
    DECLARE @user_id INT;
    DECLARE @user_name NVARCHAR(20);
    DECLARE @job_num NVARCHAR(20);
    DECLARE @total_inserted INT = 0;

    -- 创建临时表存储用户信息和分配状态
    CREATE TABLE #UserAllocation (
        user_id INT,
        department_id INT,
        user_name NVARCHAR(20),
        job_num NVARCHAR(20),
        is_allocated BIT DEFAULT 0
    );

    -- 创建临时表存储医疗组信息
    CREATE TABLE #MedicalGroups (
        group_id INT IDENTITY(1,1),
        department_treat_group_id INT,
        department_id INT
    );

    -- 插入所有用户信息到临时表
    INSERT INTO #UserAllocation (user_id, department_id, user_name, job_num)
    SELECT user_id, department_id, user_name, job_num
    FROM sys_user
    WHERE department_id IS NOT NULL
      AND user_name IS NOT NULL
      AND job_num IS NOT NULL;

    -- 插入所有医疗组信息到临时表
    INSERT INTO #MedicalGroups (department_treat_group_id, department_id)
    SELECT department_treat_group_id, department_id
    FROM sys_dept_medgp;

    -- 声明游标，遍历所有医疗组
    DECLARE medgp_cursor CURSOR FOR
    SELECT department_treat_group_id, department_id
    FROM #MedicalGroups;

    OPEN medgp_cursor;
    FETCH NEXT FROM medgp_cursor INTO @department_treat_group_id, @department_id;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        SET @counter = 1;
        -- 为每个医疗组分配指定数量的用户
        WHILE @counter <= @RecordCount
        BEGIN
            -- 优先选择属于该科室且未分配的用户
            SELECT TOP 1
                @user_id = user_id,
                @user_name = user_name,
                @job_num = job_num
            FROM #UserAllocation
            WHERE department_id = @department_id
              AND is_allocated = 0
            ORDER BY user_id;

            -- 如果该科室没有未分配的用户，则选择任意未分配的用户
            IF @user_id IS NULL
            BEGIN
                SELECT TOP 1
                    @user_id = user_id,
                    @user_name = user_name,
                    @job_num = job_num
                FROM #UserAllocation
                WHERE is_allocated = 0
                ORDER BY user_id;
            END

            -- 如果找到了用户，则插入记录并标记为已分配
            IF @user_id IS NOT NULL
            BEGIN
                -- 插入到SYS_DEPT_MEDGP_PERSON表中
                INSERT INTO SYS_DEPT_MEDGP_PERSON (user_id, department_treat_group_id, user_name, user_job_num)
                VALUES (@user_id, @department_treat_group_id, @user_name, @job_num);

                -- 标记用户为已分配
                UPDATE #UserAllocation
                SET is_allocated = 1
                WHERE user_id = @user_id;

                SET @total_inserted = @total_inserted + 1;
            END

            SET @counter = @counter + 1;
        END

        FETCH NEXT FROM medgp_cursor INTO @department_treat_group_id, @department_id;
    END

    CLOSE medgp_cursor;
    DEALLOCATE medgp_cursor;

    -- 清理临时表
    DROP TABLE #UserAllocation;
    DROP TABLE #MedicalGroups;

    SET @result = @total_inserted;
END;
