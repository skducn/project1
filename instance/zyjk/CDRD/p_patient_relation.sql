-- todo 与患者关系

CREATE OR ALTER PROCEDURE p_patient_relation
    @v nvarchar(50) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- 生成临时表
    IF OBJECT_ID('tempdb..#tb_temp') IS NOT NULL DROP TABLE #tb_temp;
    CREATE TABLE #tb_temp (ID INT IDENTITY(1,1), k NVARCHAR(50), v NVARCHAR(50));
    INSERT INTO #tb_temp (v) VALUES (N'本人'),(N'父亲'),(N'母亲'),(N'配偶'),(N'子女'),(N'兄弟姐妹'),(N'父母'),(N'祖父母'),(N'外祖父母'),
                                    (N'子女（多人）'),(N'亲戚'),(N'朋友'),(N'同事'),(N'监护人'),(N'代理人'),(N'其他');

    -- 随机选择一个 ID
    DECLARE @RandomID INT = CAST(RAND() * (SELECT COUNT(*) FROM #tb_temp) AS INT) + 1;

    -- 赋值输出参数
    SELECT @v = v FROM #tb_temp WHERE ID = @RandomID;
END
