-- todo 体征

CREATE OR ALTER PROCEDURE p_physical_sign
    @k nvarchar(50) OUTPUT,
    @v nvarchar(50) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- 生成临时表
    IF OBJECT_ID('tempdb..#tb_temp') IS NOT NULL DROP TABLE #tb_temp;
    CREATE TABLE #tb_temp (ID INT IDENTITY(1,1), k NVARCHAR(50), v NVARCHAR(50));
    INSERT INTO #tb_temp (k, v) VALUES ('1',N'体温'),('2',N'脉搏'),('3',N'心率'),('4',N'呼吸'),
                                       ('5',N'收缩压'),('6',N'舒张压'),('7',N'指尖血氧饱和度'),('8',N'其他');

    -- 随机选择一个 ID
    DECLARE @RandomID INT = CAST(RAND() * (SELECT COUNT(*) FROM #tb_temp) AS INT) + 1;

    -- 赋值输出参数
    SELECT @k = k, @v = v FROM #tb_temp WHERE ID = @RandomID;
END
