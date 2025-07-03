CREATE OR ALTER PROCEDURE a_sys_role_menu__data
    @roleName nvarchar(50),
    @menu_id int
AS
BEGIN

    BEGIN TRY
        BEGIN TRANSACTION;

        BEGIN
            -- 获取role_id
            DECLARE @role_id int;
            SELECT @role_id = role_id FROM a_sys_role WHERE role_name = @roleName;

            -- 校验，如果不存在则退出
            IF @role_id IS NULL
            BEGIN
                PRINT '错误：roleName不存在！';
                ROLLBACK TRANSACTION; -- 如果已经开启事务，则回滚
                RETURN; -- 退出存储过程
            END

            DECLARE @isCount INT = 0;
            SELECT @isCount = count(*) FROM a_sys_role_menu WHERE role_id = @role_id and menu_id = @menu_id;

            -- 判断, 如果不存在且是M
            IF @isCount = 0
            BEGIN

                -- 插入单条随机数据
                INSERT INTO a_sys_role_menu (role_id, menu_id)
                VALUES (
                        @role_id ,
                        @menu_id
                );

            END

        END;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        THROW;
    END CATCH;
END;