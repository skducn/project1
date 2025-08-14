-- todo 用户角色关系表

CREATE OR ALTER PROCEDURE s_sys_user_role
    @user_id int,
    @role_id int
AS
BEGIN


    BEGIN TRY
        BEGIN TRANSACTION;

        BEGIN
            -- 获取user_id
            -- DECLARE @role_id int;
            SELECT @user_id = user_id FROM sys_user WHERE user_id = @user_id;

            -- 校验，如果不存在则退出
            IF @user_id IS NULL
            BEGIN
                PRINT '错误：user_id不存在！';
                ROLLBACK TRANSACTION; -- 如果已经开启事务，则回滚
                RETURN; -- 退出存储过程
            END

            DECLARE @isCount INT = 0;
            SELECT @isCount = count(*) FROM sys_user_role WHERE user_id = @user_id and role_id = @role_id;

            -- 判断, 如果不存在且是M
            IF @isCount = 0
            BEGIN

                -- 插入单条随机数据
                INSERT INTO sys_user_role (user_id, role_id)
                VALUES (
                        @user_id ,
                        @role_id
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