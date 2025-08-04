-- todo 角色表(造数据)

CREATE OR ALTER PROCEDURE sys_role
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

        CREATE TABLE #Names (ID INT IDENTITY(1,1), Role NVARCHAR(50), RoleKey NVARCHAR(50));
        INSERT INTO #Names (Role, RoleKey) VALUES ('运营负责人','director'),('科主任','chief_doctor'),('副主任','deputy_chief'),('医疗组长','group_leader'),('主治医生','attending_doctor'),('门/急诊医生、住院医生','doctor');
        DECLARE @InsertedNamesCount INT = @@ROWCOUNT; -- 快速获取上一条插入/更新/删除的行数

        -- 循环插入指定数量的记录
        WHILE @Counter <= @InsertedNamesCount
        BEGIN

             -- 子存储过程
             -- 角色状态
            DECLARE @RandomStatusIdKey NVARCHAR(50), @RandomStatusIdValue NVARCHAR(50);
            EXEC p_status @k = @RandomStatusIdKey OUTPUT, @v = @RandomStatusIdValue OUTPUT;


            -- 获取角色名称和权限标识
            DECLARE @RoleName NVARCHAR(50), @RoleKey NVARCHAR(50);
            SELECT @RoleName = Role, @RoleKey = RoleKey FROM #Names WHERE ID = @Counter;

            -- 增加非空校验
            IF @RoleName IS NULL OR @RoleName = ''
            BEGIN
                PRINT '错误：RoleName不存在！';
                ROLLBACK TRANSACTION; -- 如果已经开启事务，则回滚
                RETURN; -- 退出存储过程
            END

            -- 插入单条随机数据
            INSERT INTO a_sys_role (role_name,role_key,role_sort,status,menu_check_strictly,create_by,create_time,update_by,update_time,remark)
            VALUES (
                    @RoleName ,
                    @RoleKey ,
                    '0', -- 显示顺序
                    @RandomStatusIdKey, -- 角色状态
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