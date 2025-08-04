-- todo 医院

CREATE OR ALTER PROCEDURE p_hospital
    @v nvarchar(350) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- 生成临时表
    IF OBJECT_ID('tempdb..#tb_temp') IS NOT NULL DROP TABLE #tb_temp;
    CREATE TABLE #tb_temp (ID INT IDENTITY(1,1), v NVARCHAR(350));
    INSERT INTO #tb_temp (v) VALUES ('东方医院'),('复旦大学附属眼耳鼻喉科医院'),('上海交通大学医学院附属第九人民医院'),('上海市第一人民医院'),('上海交通大学医学院附属新华医院');

    -- 随机选择一个 ID
    DECLARE @RandomID INT = CAST(RAND() * (SELECT COUNT(*) FROM #tb_temp) AS INT) + 1;

    -- 赋值输出参数
    SELECT @v = v FROM #tb_temp WHERE ID = @RandomID;
END
