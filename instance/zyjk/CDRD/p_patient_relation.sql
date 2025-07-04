-- todo 与患者关系

CREATE OR ALTER PROCEDURE p_patient_relation
    @v nvarchar(50) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- 生成临时表
    IF OBJECT_ID('tempdb..#tb_temp') IS NOT NULL DROP TABLE #tb_temp;
    CREATE TABLE #tb_temp (ID INT IDENTITY(1,1), k NVARCHAR(50), v NVARCHAR(50));
    INSERT INTO #tb_temp (v) VALUES ('本人'),('父亲'),('母亲'),('配偶'),('子女'),('兄弟姐妹'),('父母'),('祖父母'),('外祖父母'),
                                    ('子女（多人）'),('亲戚'),('朋友'),('同事'),('监护人'),('代理人'),('其他');

    -- 随机选择一个 ID
    DECLARE @RandomID INT = CAST(RAND() * (SELECT COUNT(*) FROM #tb_temp) AS INT) + 1;

    -- 赋值输出参数
    SELECT @v = v FROM #tb_temp WHERE ID = @RandomID;
END
