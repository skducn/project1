-- todo 科室

CREATE OR ALTER PROCEDURE p_dept
    @RandomID INT,
    @v NVARCHAR(50) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- 生成临时表
    IF OBJECT_ID('tempdb..#tb_temp') IS NOT NULL DROP TABLE #tb_temp;
    CREATE TABLE #tb_temp (ID INT IDENTITY(1,1), v NVARCHAR(50));
    INSERT INTO #tb_temp (v) VALUES (N'内科'),(N'外科'),(N'儿科'),(N'妇产科'),(N'骨科'),
                                    (N'眼科'),(N'耳鼻喉科'),(N'口腔科'),(N'皮肤科'),(N'心血管科'),
                                    (N'神经科'),(N'精神科'),(N'放射科'),(N'检验科'),(N'影像科'),
                                    (N'重症医学科'),(N'麻醉科'),(N'急诊科'),(N'临床药学'),(N'康复科');



    -- 随机选择一个 ID
--     DECLARE @RandomID INT = CAST(RAND() * (SELECT COUNT(*) FROM #tb_temp) AS INT) + 1;

    -- 赋值输出参数
    SELECT @v = v FROM #tb_temp WHERE ID = @RandomID; -- 默认按顺序输出
END
