-- todo 民族

CREATE OR ALTER PROCEDURE p_nationality
    @k nvarchar(50) OUTPUT,
    @v nvarchar(50) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- 生成临时表
    IF OBJECT_ID('tempdb..#tb_temp') IS NOT NULL DROP TABLE #tb_temp;
    CREATE TABLE #tb_temp (ID INT IDENTITY(1,1), k NVARCHAR(50), v NVARCHAR(50));
    INSERT INTO #tb_temp (k, v) VALUES ('01','汉族'),('02','蒙古族'),('03','回族'),('04','藏族'),('05','维吾尔族'),('06','苗族'),('07','彝族'),('08','壮族'),('09','布依族'),('10','朝鲜族');

    -- 随机选择一个 ID
    DECLARE @RandomID INT = CAST(RAND() * (SELECT COUNT(*) FROM #tb_temp) AS INT) + 1;

    -- 赋值输出参数
    SELECT @k = k, @v = v FROM #tb_temp WHERE ID = @RandomID;
END
