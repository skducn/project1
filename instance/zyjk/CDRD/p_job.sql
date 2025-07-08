-- todo 随机职业

CREATE OR ALTER PROCEDURE p_job
    @v nvarchar(50) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- 生成临时表
    IF OBJECT_ID('tempdb..#tb_temp') IS NOT NULL DROP TABLE #tb_temp;
    CREATE TABLE #tb_temp (ID INT IDENTITY(1,1), v NVARCHAR(50));
    INSERT INTO #tb_temp (v) VALUES (N'军人'),(N'医生'),(N'自由职业者'),(N'技术人员'),(N'工程师'),(N'学生'),(N'老师'),(N'服务人员');

    -- 随机选择一个 ID
    DECLARE @RandomID INT = CAST(RAND() * (SELECT COUNT(*) FROM #tb_temp) AS INT) + 1;

    -- 赋值输出参数
    SELECT @v = v FROM #tb_temp WHERE ID = @RandomID;
END
