-- todo 住址

CREATE OR ALTER PROCEDURE p_address
    @v1 nvarchar(150) OUTPUT,
    @v2 nvarchar(150) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- 预生成字典临时表
    IF OBJECT_ID('tempdb..#tb_street') IS NOT NULL DROP TABLE #tb_street;
    CREATE TABLE #tb_street (ID INT IDENTITY(1,1), Street NVARCHAR(50));
    INSERT INTO #tb_street (Street) VALUES
    (N'人民'), (N'解放'), (N'中山'), (N'建设'), (N'朝阳'), (N'浦东'), (N'浦西'), (N'南京'), (N'北京'),
    (N'长安'), (N'淮海'), (N'延安'), (N'东湖'), (N'西湖'), (N'南湖'), (N'北湖'), (N'光华'), (N'新华'), (N'时代');
    -- 地址后缀（如：路、街、大道等）
    CREATE TABLE #Suffixes (ID INT IDENTITY(1,1), Suffix NVARCHAR(50));
    INSERT INTO #Suffixes (Suffix) VALUES (N'路'), (N'街'), (N'大道'), (N'巷'), (N'弄'), (N'东路'), (N'西路'), (N'南路'), (N'北路');

--     随机选择一个 ID
--     DECLARE @RandomID INT = CAST(RAND() * (SELECT COUNT(*) FROM #tb_street) AS INT) + 1;

     -- 随机选择一个路名
    DECLARE @RandomStreet NVARCHAR(50);
    DECLARE @RandomStreet2 NVARCHAR(50);
    SELECT @RandomStreet = Street FROM #tb_street WHERE ID = CAST(RAND() * (SELECT COUNT(*) FROM #tb_street) AS INT) + 1;
    SELECT @RandomStreet2 = Street FROM #tb_street WHERE ID = CAST(RAND() * (SELECT COUNT(*) FROM #tb_street) AS INT) + 1;

    -- 随机选择一个后缀
    DECLARE @RandomSuffix NVARCHAR(10);
    DECLARE @RandomSuffix2 NVARCHAR(10);
    SELECT @RandomSuffix = Suffix FROM #Suffixes WHERE ID = CAST(RAND() * 9 AS INT) + 1;
    SELECT @RandomSuffix2 = Suffix FROM #Suffixes WHERE ID = CAST(RAND() * 9 AS INT) + 1;

    -- 随机门牌号（1-999号）
    DECLARE @RandomHouseNumber INT = CAST(RAND() * 999 AS INT) + 1;
    DECLARE @RandomHouseNumber2 INT = CAST(RAND() * 999 AS INT) + 1;

    -- 拼接地址
    DECLARE @RandomAddress1 NVARCHAR(100);
    DECLARE @RandomAddress2 NVARCHAR(100);
    SET @RandomAddress1 = @RandomStreet + @RandomSuffix + CAST(@RandomHouseNumber AS NVARCHAR(10)) + N'号';
    SET @RandomAddress2 = @RandomStreet2 + @RandomSuffix2 + CAST(@RandomHouseNumber2 AS NVARCHAR(10)) + N'号';

    -- 赋值输出参数
    SELECT @v1 = @RandomAddress1, @v2 = @RandomAddress2

END
