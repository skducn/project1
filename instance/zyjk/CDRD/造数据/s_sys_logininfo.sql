CREATE OR ALTER PROCEDURE s_sys_logininfo
    @RecordCount INT = 500000, -- 默认10条
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- 创建临时表存储预生成的随机数据
    CREATE TABLE #NamePool (id INT IDENTITY(1,1), FullName NVARCHAR(50));
    CREATE TABLE #LoginTypePool (id INT IDENTITY(1,1), n_key NVARCHAR(100), n_value NVARCHAR(100));
    
    -- 预生成足够数量的姓名数据（至少生成1000个姓名以确保有足够随机性）
    DECLARE @i INT = 1;
    DECLARE @nameCount INT = CASE
        WHEN @RecordCount < 1000 THEN 1000
        ELSE CEILING(SQRT(@RecordCount))
    END;

    WHILE @i <= @nameCount
    BEGIN
        DECLARE @RandomName NVARCHAR(50);
        EXEC p_name @FullName = @RandomName OUTPUT;
        INSERT INTO #NamePool (FullName) VALUES (@RandomName);
        SET @i = @i + 1;
    END

    -- 预生成登录类型数据
    INSERT INTO #LoginTypePool (n_key, n_value)
    SELECT n_key, n_value FROM ab_loginout;

    -- 使用CTE生成序列并批量插入数据
    WITH
    Sequence AS (
        SELECT TOP (@RecordCount)
            ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS RowNum
        FROM
            (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10)) AS a(n)
            CROSS JOIN (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10)) AS b(n)
            CROSS JOIN (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10)) AS c(n)
            CROSS JOIN (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10)) AS d(n)
            CROSS JOIN (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10)) AS e(n)
            CROSS JOIN (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10)) AS f(n)
    ),
    RandomizedData AS (
        SELECT
            s.RowNum,
            n.FullName AS BaseName,
            lt.n_key AS RandomLoginType,
            lt.n_value AS RandomWay,
            ABS(CHECKSUM(NEWID())) % 1000 AS RandomNum1,
            ABS(CHECKSUM(NEWID())) % 100000 AS RandomNum2,
            DATEADD(DAY, ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS RandomDate
        FROM Sequence s
        CROSS JOIN (SELECT COUNT(*) AS NameCount FROM #NamePool) nc
        CROSS JOIN (SELECT COUNT(*) AS LoginTypeCount FROM #LoginTypePool) lc
        JOIN #NamePool n ON n.id = (s.RowNum % nc.NameCount) + 1
        JOIN #LoginTypePool lt ON lt.id = (s.RowNum % lc.LoginTypeCount) + 1
    )
    INSERT INTO sys_logininfo (user_name, nick_name, type, access_time, ipaddr, way, status, msg, client_info)
    SELECT 
        BaseName + RIGHT('000' + CONVERT(NVARCHAR(10), RandomNum1), 3), -- 账号
        BaseName + RIGHT('00000' + CONVERT(NVARCHAR(10), RandomNum2), 5), -- 姓名
        RandomLoginType, -- 登录类型
        RandomDate, -- 访问时间
        '192.168.0.123', -- IP地址
        RandomWay, -- 方式
        '成功', -- 结果
        '', -- 备注
        'win/mac' -- 客户端信息
    FROM RandomizedData;

    SET @result = @@ROWCOUNT;
END;
