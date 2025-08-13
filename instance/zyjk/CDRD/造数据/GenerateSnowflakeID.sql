-- 修改现有的存储过程
CREATE OR ALTER PROCEDURE GenerateSnowflakeID
    @machineId INT,
    @dataCenterId INT,
    @snowflakeId BIGINT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- 验证参数
    IF @machineId < 0 OR @machineId > 31 OR @dataCenterId < 0 OR @dataCenterId > 31
    BEGIN
        RAISERROR('机器ID和数据中心ID必须在0-31之间', 16, 1);
        RETURN;
    END

    DECLARE @epoch DATETIME2 = '2020-01-01 00:00:00.000'; -- 起始时间戳
    DECLARE @timestamp BIGINT;
    DECLARE @sequence INT;
    DECLARE @currentSequence INT;
    DECLARE @lastTimestamp BIGINT;

    -- 获取当前时间戳（毫秒级）
    SET @timestamp = DATEDIFF_BIG(millisecond, @epoch, SYSUTCDATETIME());

    -- 使用事务确保并发安全
    BEGIN TRANSACTION;

    -- 获取当前序列号和最后时间戳
    SELECT @currentSequence = CurrentSequence, @lastTimestamp = LastTimestamp
    FROM SnowflakeSequence WITH (UPDLOCK, HOLDLOCK);

    -- 处理时间戳和序列号
    IF @timestamp > @lastTimestamp
    BEGIN
        SET @sequence = 0;
    END
    ELSE IF @timestamp = @lastTimestamp
    BEGIN
        SET @sequence = (@currentSequence + 1) % 4096;
        -- 如果序列号溢出，等待下一毫秒
        IF @sequence = 0
        BEGIN
            WAITFOR DELAY '00:00:00.001';
            SET @timestamp = DATEDIFF_BIG(millisecond, @epoch, SYSUTCDATETIME());
        END
    END
    ELSE -- 处理时钟回拨
    BEGIN
        RAISERROR('系统时间发生回拨，无法生成Snowflake ID', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END

    -- 更新序列号和时间戳
    UPDATE SnowflakeSequence
    SET CurrentSequence = @sequence,
        LastTimestamp = @timestamp;

    COMMIT TRANSACTION;

    -- 生成Snowflake ID (使用SQL Server兼容的位运算)
    SET @snowflakeId =
        (@timestamp * POWER(2, 22)) +
        (@dataCenterId * POWER(2, 17)) +
        (@machineId * POWER(2, 12)) +
        @sequence;
END
