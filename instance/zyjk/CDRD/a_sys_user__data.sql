CREATE OR ALTER PROCEDURE a_sys_user__data
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
            DECLARE @RandomID INT = CAST(RAND() * 10 AS INT) + 1; -- 避免使用 CHECKSUM 和 NEWID 的组合
            SELECT @RandomName = Name FROM #Names WHERE ID = @RandomID;
            -- 增加非空校验
            IF @RandomName IS NULL OR @RandomName = ''
            BEGIN
                SET @RandomName = '默认名称'; -- 设置默认值
            END

            -- 关联表 a_sys_department 的 department_id
            DECLARE @department_id int;
            SELECT TOP 1 @department_id = department_id FROM a_sys_department ORDER BY NEWID();

            -- 关联表 a_sys_department 的 department_code
            DECLARE @department_code NVARCHAR(20);
            SELECT TOP 1 @department_code = department_code FROM a_sys_department where department_id=@department_id;

            -- 关联表 a_sys_department 的 department_name
            DECLARE @department_name NVARCHAR(20);
            SELECT TOP 1 @department_name = department_name FROM a_sys_department where department_id=@department_id;

            -- 插入单条随机数据
            INSERT INTO a_sys_user (nick_name,user_name,user_type,password,job_num,email,phonenumber,sex,avatar,department_id,department_code,department_name,user_account_state,remark,creater_by,create_time,update_by,update_time,pwd_update_state,pwd_update_time,pwd_next_update_time
)
            VALUES (
                    @RandomName + RIGHT('000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 1000), 3), -- nick_name: 姓名 + 固定3位数
                    @RandomName + RIGHT('00000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100000), 5), -- user_name: 姓名 + 固定5位数
                    '00', -- 用户类型
                    '123456', -- 密码
                    CAST(ABS(CHECKSUM(NEWID())) % 100000 AS NVARCHAR(10)), -- 工号
                    LOWER(@RandomName) + CAST(ABS(CHECKSUM(NEWID())) % 1000 AS NVARCHAR(10)) + '@example.com', --邮箱
                    '13816' + CAST(ABS(CHECKSUM(NEWID())) % 1000000 AS NVARCHAR(10)), -- 手机号
                    '1',  -- 性别
                    'http:www.baidu.com', -- 头像地址
                    @department_id, -- 科室ID
                    @department_code, -- 所属科室code
                    @department_name, -- 所属科室名称
                    0, -- 账号状态
                    'jioqwejoqwejoqwejqwe', -- 备注
                    'admin', -- 创建人
                    GETDATE(), -- 创建时间
                    'admin', -- 更新者
                    GETDATE(), -- 更新时间
                    0, -- 密码重置状态
                    GETDATE(), -- 密码最后更新时间
                    GETDATE() + 365 -- 秘密下次更新时间
            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_sys_user);
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