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
    ('人民'), ('解放'), ('中山'), ('建设'), ('朝阳'), ('浦东'), ('浦西'), ('南京'), ('北京'),
    ('长安'), ('淮海'), ('延安'), ('东湖'), ('西湖'), ('南湖'), ('北湖'), ('光华'), ('新华'), ('时代');
    -- 地址后缀（如：路、街、大道等）
    CREATE TABLE #Suffixes (ID INT IDENTITY(1,1), Suffix NVARCHAR(50));
    INSERT INTO #Suffixes (Suffix) VALUES ('路'), ('街'), ('大道'), ('巷'), ('弄'), ('东路'), ('西路'), ('南路'), ('北路');

    -- 随机选择一个 ID
    DECLARE @RandomID INT = CAST(RAND() * (SELECT COUNT(*) FROM #tb_street) AS INT) + 1;

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
    SET @RandomAddress1 = @RandomStreet + @RandomSuffix + CAST(@RandomHouseNumber AS NVARCHAR(10)) + '号';
    SET @RandomAddress2 = @RandomStreet2 + @RandomSuffix2 + CAST(@RandomHouseNumber2 AS NVARCHAR(10)) + '号';

    -- 赋值输出参数
    SELECT @v1 = @RandomAddress1, @v2 = @RandomAddress2

END
