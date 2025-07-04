-- todo 科室

CREATE OR ALTER PROCEDURE p_dept
    @v nvarchar(50) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- 生成临时表
    IF OBJECT_ID('tempdb..#tb_temp') IS NOT NULL DROP TABLE #tb_temp;
    CREATE TABLE #tb_temp (ID INT IDENTITY(1,1), v NVARCHAR(50));
    INSERT INTO #tb_temp (v) VALUES ('内科'),('外科'),('妇产科'),('儿科'),('肿瘤科'),('五官科'),('其他临床科室'),('医技科室'),('内分泌科'),('骨科');

    -- 随机选择一个 ID
    DECLARE @RandomID INT = CAST(RAND() * (SELECT COUNT(*) FROM #tb_temp) AS INT) + 1;

    -- 赋值输出参数
    SELECT @v = v FROM #tb_temp WHERE ID = @RandomID;
END
