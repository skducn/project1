-- todo 登录登出表

CREATE OR ALTER PROCEDURE sys_logininfo
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



            -- 插入单条随机数据
            INSERT INTO a_sys_logininfo (user_name,nick_name,type,access_time,ipaddr,way,status,msg,client_info)
            VALUES (
                    @RandomName + RIGHT('000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 1000), 3), -- 账号
                    @RandomName + RIGHT('00000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100000), 5), -- 姓名
                    CAST(ABS(CHECKSUM(NEWID())) % 100000 AS NVARCHAR(10)), -- 登录类型
                    GETDATE(), -- 访问时间
                    '192.168.0.123', -- 更新者
                    'pc登录', -- 方式
                    '登录成功', -- 结果
                    '备注123123', -- 备注
                    'win/mac' -- 客户端信息
            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_sys_logininfo);
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