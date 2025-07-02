CREATE OR ALTER PROCEDURE a_sys_menu__data
    @menuType nvarchar(50),
    @menuName nvarchar(50),
    @menuParentName nvarchar(50)
AS
BEGIN
--     SET NOCOUNT ON;
--     SET XACT_ABORT ON;

    -- 统计顺序
    DECLARE @isCount INT = 0;
    -- 父ID
    DECLARE @parent_id NVARCHAR(50);


    BEGIN TRY
        BEGIN TRANSACTION;
--         # ['c', '用户管理', '系统管理']
        DECLARE @isExist NVARCHAR(50);
        SELECT @isExist = menu_id FROM a_sys_menu WHERE menu_name = @menuName and menu_type = @menuType;

        -- 判断, 如果不存在且是M
        IF @isExist IS NULL and @menuType = 'M'
        BEGIN
            -- 统计顺序
            SELECT @isCount = count(*) FROM a_sys_menu WHERE menu_type = @menuType;
            set @isCount = @isCount + 1;

            -- 插入目录
            INSERT INTO a_sys_menu (menu_name,order_num,path,component,query,route_name,is_frame,is_cache,menu_type,status,visible,perms,icon,create_by,create_time,update_by,update_time,remark)
            VALUES (
                    @menuName, -- 菜单名称
                    @isCount, -- 显示顺序
                    '/test/', -- 路由地址
                    '/user/', -- 组件路径
                    'param', -- 路由参数
                    'test', -- 路由名称
                    '1',-- 是否为外链
                    '0', -- 是否缓存
                    @menuType, -- 菜单类型
                    '0',-- 菜单状态
                    '1', -- 显示状态
                    '11', -- 权限字符
                    '3', -- 菜单图标
                    'admin', -- 创建人
                    GETDATE(), -- 创建时间
                    'admin', -- 更新者
                    GETDATE(), -- 更新时间
                    'jioqwejoqwejoqwejqwe' -- 备注
            );
        END

        IF @isExist IS NULL and @menuType = 'C'
        BEGIN
            -- 统计顺序
            SELECT @isCount = count(*) FROM a_sys_menu WHERE menu_type = @menuType;
            set @isCount = @isCount + 1;

            -- 获取父级ID
            SELECT @parent_id = menu_id FROM a_sys_menu WHERE menu_name = @menuParentName and menu_type = 'M';

            IF @parent_id IS NOT NULL
            BEGIN
                -- 插入目录
                INSERT INTO a_sys_menu (menu_name,parent_id,order_num,path,component,query,route_name,is_frame,is_cache,menu_type,status,visible,perms,icon,create_by,create_time,update_by,update_time,remark)
                VALUES (
                        @menuName, -- 菜单名称
                        @parent_id, -- 父菜单ID
                        @isCount, -- 显示顺序
                        '/test/', -- 路由地址
                        '/user/', -- 组件路径
                        'param', -- 路由参数
                        'test', -- 路由名称
                        '1',-- 是否为外链
                        '0', -- 是否缓存
                        @menuType, -- 菜单类型
                        '0',-- 菜单状态
                        '1', -- 显示状态
                        '11', -- 权限字符
                        '3', -- 菜单图标
                        'admin', -- 创建人
                        GETDATE(), -- 创建时间
                        'admin', -- 更新者
                        GETDATE(), -- 更新时间
                        'jioqwejoqwejoqwejqwe' -- 备注
                );
            END
        END

        IF @isExist IS NULL and @menuType = 'F'
        BEGIN
            -- 统计顺序
            SELECT @isCount = count(*) FROM a_sys_menu WHERE menu_type = @menuType;
            set @isCount = @isCount + 1;

            -- 获取父级ID
            SELECT @parent_id = menu_id FROM a_sys_menu WHERE menu_name = @menuParentName and menu_type = 'C';

            IF @parent_id IS NOT NULL
            BEGIN
                -- 插入目录
                INSERT INTO a_sys_menu (menu_name,parent_id,order_num,path,component,query,route_name,is_frame,is_cache,menu_type,status,visible,perms,icon,create_by,create_time,update_by,update_time,remark)
                VALUES (
                        @menuName, -- 菜单名称
                        @parent_id, -- 父菜单ID
                        @isCount, -- 显示顺序
                        '/test/', -- 路由地址
                        '/user/', -- 组件路径
                        'param', -- 路由参数
                        'test', -- 路由名称
                        '1',-- 是否为外链
                        '0', -- 是否缓存
                        @menuType, -- 菜单类型
                        '0',-- 菜单状态
                        '1', -- 显示状态
                        '11', -- 权限字符
                        '3', -- 菜单图标
                        'admin', -- 创建人
                        GETDATE(), -- 创建时间
                        'admin', -- 更新者
                        GETDATE(), -- 更新时间
                        'jioqwejoqwejoqwejqwe' -- 备注
                );
            END
        END

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;