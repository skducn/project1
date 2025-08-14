-- todo 参数配置表

CREATE OR ALTER PROCEDURE s_sys_config
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


        -- 循环插入指定数量的记录
        WHILE @Counter <= @MaxRecords
        BEGIN

            -- 子存储过程
            -- 姓名
            DECLARE @RandomName NVARCHAR(50);
            EXEC p_name @FullName = @RandomName OUTPUT;

            -- 系统内置
            DECLARE @RandomTrueFalseIdKey NVARCHAR(50), @RandomTrueFalseIdValue NVARCHAR(50);
            EXEC p_trueFalse @k = @RandomTrueFalseIdKey OUTPUT, @v = @RandomTrueFalseIdValue OUTPUT;



--             -- 关联表 a_sys_department 的 department_id
--             DECLARE @department_id int;
--             SELECT TOP 1 @department_id = department_id FROM a_sys_department ORDER BY NEWID();
--
--             -- 关联表 a_sys_department 的 department_code
--             DECLARE @department_code NVARCHAR(20);
--             SELECT TOP 1 @department_code = department_code FROM a_sys_department where department_id=@department_id;
--
--             -- 关联表 a_sys_department 的 department_name
--             DECLARE @department_name NVARCHAR(20);
--             SELECT TOP 1 @department_name = department_name FROM a_sys_department where department_id=@department_id;

            -- 插入单条随机数据
            INSERT INTO sys_config (config_name,config_key,config_value,config_type,create_by,create_time,update_by,update_time,remark)
            VALUES (
                    @RandomName + RIGHT('000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 1000), 3), -- 参数名称
                    @RandomName + RIGHT('00000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100000), 5), -- 参数键名
                    CAST(ABS(CHECKSUM(NEWID())) % 100000 AS NVARCHAR(10)), -- 参数键值
                    @RandomTrueFalseIdKey, -- 系统内置
                    'admin', -- 创建人
                    GETDATE(), -- 创建时间
                    'admin', -- 更新者
                    GETDATE(), -- 更新时间
                    '112321321' -- 备注
            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_sys_config);
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