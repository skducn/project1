-- todo 科室

CREATE OR ALTER PROCEDURE p_dept
    @v nvarchar(50) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- 生成临时表
    IF OBJECT_ID('tempdb..#tb_temp') IS NOT NULL DROP TABLE #tb_temp;
    CREATE TABLE #tb_temp (ID INT IDENTITY(1,1), v NVARCHAR(50));
    INSERT INTO #tb_temp (v) VALUES (N'内科'),(N'外科'),(N'妇产科'),(N'儿科'),(N'肿瘤科'),(N'五官科'),(N'其他临床科室'),
                                    (N'医技科室'),(N'内分泌科'),(N'骨科');

    -- 随机选择一个 ID
    DECLARE @RandomID INT = CAST(RAND() * (SELECT COUNT(*) FROM #tb_temp) AS INT) + 1;

    -- 赋值输出参数
    SELECT @v = v FROM #tb_temp WHERE ID = @RandomID;
END
