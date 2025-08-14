-- todo 用户表
-- 数据量：200

CREATE OR ALTER PROCEDURE s_sys_user
    @RecordCount INT = 200,  -- N个用户
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    SET @result = @RecordCount

--     BEGIN TRY
--         BEGIN TRANSACTION;

    DECLARE @Counter INT = 1;
--         DECLARE @TotalCount INT =0;

    -- 获取科室总数
    DECLARE @DeptCount INT;
    SELECT @DeptCount = COUNT(*) FROM sys_department;

    -- 声明科室游标
    DECLARE @department_id INT;
    DECLARE @department_code NVARCHAR(20);
    DECLARE @department_name NVARCHAR(20);
    DECLARE @CurrentDeptIndex INT = 0;

     -- 获取科室列表到临时表
    IF OBJECT_ID('tempdb..#Departments') IS NOT NULL DROP TABLE #Departments;
    SELECT
        ROW_NUMBER() OVER (ORDER BY department_id) AS DeptIndex,
        department_id,
        department_code,
        department_name
    INTO #Departments
    FROM sys_department;

--         -- 预生成随机数据所需的基础数据
--         IF OBJECT_ID('tempdb..#Names') IS NOT NULL DROP TABLE #Names;
--
--         CREATE TABLE #Names (ID INT IDENTITY(1,1), Name NVARCHAR(50));
--         INSERT INTO #Names (Name) VALUES (N'东大名'),(N'朴志镐'),(N'洁神明'),('苗胸'),('格格'),('张桂芳'),('金制成'),('孙俪'),('濮存昕'),('黎明');

    -- 循环插入指定数量的记录
    WHILE @Counter <= @RecordCount
    BEGIN

        -- 计算当前用户应该分配到的科室索引（每10个用户为一组）
        DECLARE @DeptIndex INT = ((@Counter - 1) / 10) % @DeptCount + 1;

        -- 获取对应科室信息
        SELECT
            @department_id = department_id,
            @department_code = department_code,
            @department_name = department_name
        FROM #Departments
        WHERE DeptIndex = @DeptIndex;

        -- 子存储过程
        -- 姓名
        DECLARE @RandomName NVARCHAR(50);
        EXEC p_name @FullName = @RandomName OUTPUT;

        -- 性别
        DECLARE @RandomSexIdKey NVARCHAR(50), @RandomSexIdValue NVARCHAR(50);
        EXEC p_sex @k = @RandomSexIdKey OUTPUT, @v = @RandomSexIdValue OUTPUT;

        -- 账号状态
        DECLARE @RandomStatusIdKey NVARCHAR(50), @RandomStatusIdValue NVARCHAR(50);
        EXEC p_status @k = @RandomStatusIdKey OUTPUT, @v = @RandomStatusIdValue OUTPUT;


--             -- 关联表 a_sys_department 的 department_id
--             DECLARE @department_id int;
--             SELECT TOP 1 @department_id = department_id FROM sys_department ORDER BY NEWID();
--
--             -- 关联表 a_sys_department 的 department_code
--             DECLARE @department_code NVARCHAR(20);
--             SELECT TOP 1 @department_code = department_code FROM sys_department where department_id=@department_id;
--
--             -- 关联表 a_sys_department 的 department_name
--             DECLARE @department_name NVARCHAR(20);
--             SELECT TOP 1 @department_name = department_name FROM sys_department where department_id=@department_id;

        -- 插入单条随机数据
        INSERT INTO sys_user (nick_name,user_name,user_type,password,job_num,email,phonenumber,sex,avatar,department_id,department_code,department_name,status,remark,create_by,create_time,update_by,update_time,pwd_update_state,pwd_update_time,pwd_next_update_time
)
        VALUES (
--                 @RandomName + RIGHT('000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 1000), 3), -- nick_name: 姓名 + 固定3位数
                'tester' + CAST(@Counter AS NVARCHAR(10)), -- nick_name: 姓名 + 序号
                'tester' + CAST(@Counter AS NVARCHAR(10)), -- user_name: 姓名 + 序号
                '00', -- 用户类型
                '$2a$10$vgB3iFh5CNK10RBJaQtZ3ugT.5FLznMUYRTyywvLkalWOOxTshZtq', -- 密码
                CAST(ABS(CHECKSUM(NEWID())) % 100000 AS NVARCHAR(10)), -- 工号
                LOWER(@RandomName) + CAST(ABS(CHECKSUM(NEWID())) % 1000 AS NVARCHAR(10)) + '@example.com', --邮箱
                '13816' + CAST(ABS(CHECKSUM(NEWID())) % 1000000 AS NVARCHAR(10)), -- 手机号
                @RandomSexIdKey,  -- 性别
                'http://www.baidu.com', -- 头像地址
                @department_id, -- 科室ID
                @department_code, -- 所属科室code
                @department_name, -- 所属科室名称
                '0', -- 账号状态
                'jioqwejoqwejoqwejqwe', -- 备注
                'admin', -- 创建人
                GETDATE(), -- 创建时间
                'admin', -- 更新者
                GETDATE(), -- 更新时间
                0, -- 密码重置状态
                '2055-12-12 12:12:12', -- 密码最后更新时间
                '2055-12-12 12:12:12' -- 密码下次更新时间
--                     GETDATE(), -- 密码最后更新时间
--                     GETDATE() + 365 -- 秘密下次更新时间
        );

        SET @Counter = @Counter + 1;

    END;

--         -- 返回插入的记录数
--         SELECT @RecordCount AS RequestedCount, @TotalCount AS TotalCount;

--         COMMIT TRANSACTION;
--     END TRY
--     BEGIN CATCH
--         IF @@TRANCOUNT > 0
--             ROLLBACK TRANSACTION;
--
--         THROW;
--     END CATCH;
END;