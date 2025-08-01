-- todo 登录登出表
-- sys_logininfo(登录登出表) => 生成 10000 条！
-- 耗时: 16.7572 秒
CREATE OR ALTER PROCEDURE sys_logininfo
    @RecordCount INT = 10000, -- 默认10条
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    SET @result = @RecordCount;

    -- 循环插入指定数量的记录
    DECLARE @Counter INT = 1;
    WHILE @Counter <= @RecordCount
    BEGIN

        -- 子存储过程
        -- 姓名
        DECLARE @RandomName NVARCHAR(50);
        EXEC p_name @FullName = @RandomName OUTPUT;

        -- 系统内置
        DECLARE @RandomTrueFalseIdKey NVARCHAR(100)
        DECLARE @RandomTrueFalseIdValue NVARCHAR(100)
        SELECT TOP 1 @RandomTrueFalseIdKey=n_key,@RandomTrueFalseIdValue=n_value FROM ab_boolean ORDER BY NEWID()

        -- 登录类型，方式
        DECLARE @RandomLoginType NVARCHAR(100)
        DECLARE @RandomWay NVARCHAR(100)
        SELECT TOP 1 @RandomLoginType=n_key,@RandomWay=n_value FROM ab_loginout ORDER BY NEWID()


        -- 插入单条随机数据
        INSERT INTO a_sys_logininfo (user_name,nick_name,type,access_time,ipaddr,way,status,msg,client_info)
        VALUES (
            @RandomName + RIGHT('000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 1000), 3), -- 账号
            @RandomName + RIGHT('00000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100000), 5), -- 姓名
            @RandomLoginType, -- 登录类型
            DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 访问时间
            '192.168.0.123', -- 更新者
            @RandomWay, -- 方式
            '成功', -- 结果
            '', -- 备注
            'win/mac' -- 客户端信息
            );

        SET @Counter = @Counter + 1;

    END;



END;