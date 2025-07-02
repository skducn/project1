CREATE OR ALTER PROCEDURE a_sys_role__data
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
        INSERT INTO #Names (Name) VALUES ('科主任'),('副主任'),('医疗组长'),('主治医生'),('门/急诊医生、住院医生');
        DECLARE @InsertedNamesCount INT = @@ROWCOUNT; -- 快速获取上一条插入/更新/删除的行数

        -- 循环插入指定数量的记录
        WHILE @Counter <= @InsertedNamesCount
        BEGIN
            -- 随机选择姓名和域名
            DECLARE @RoleName NVARCHAR(50);
            SELECT @RoleName = Name FROM #Names WHERE ID = @Counter;
            -- 增加非空校验
            IF @RoleName IS NULL OR @RoleName = ''
            BEGIN
                SET @RoleName = '默认名称'; -- 设置默认值
            END

            -- 插入单条随机数据
            INSERT INTO a_sys_role (role_name,role_key,role_sort,status,menu_check_strictly,role_creater_name,role_create_time,update_by,update_time,remark)
            VALUES (
                    @RoleName , -- 角色名称 + 固定3位数
                    @RoleName + RIGHT('00000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100000), 5), -- 角色权限字符串 + 固定5位数
                    '0', -- 显示顺序
                    '0', -- 角色状态
                    '1', -- 菜单树选择项是否关联显示
                    'admin', -- 创建人
                    GETDATE(), -- 创建时间
                    'admin', -- 更新者
                    GETDATE(), -- 更新时间
                    'jioqwejoqwejoqwejqwe' -- 备注
            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_sys_role);
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