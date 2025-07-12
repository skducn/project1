-- todo 实验室检查报告 - 报告名称，样本类型，项目名称

CREATE OR ALTER PROCEDURE r_lab_examination_info__
    @v1 nvarchar(50) OUTPUT,
    @v2 nvarchar(50) OUTPUT,
    @v3 nvarchar(50) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- 生成临时表
    IF OBJECT_ID('tempdb..#tb_temp') IS NOT NULL DROP TABLE #tb_temp;
    CREATE TABLE #tb_temp (ID INT IDENTITY(1,1), v1 NVARCHAR(50), v2 NVARCHAR(150), v3 NVARCHAR(50));
    INSERT INTO #tb_temp (v1, v2, v3) VALUES 
                ('血生化检测', '全血', '无'),
                ('凝血功能检验', '全血', '无')
      ;

    -- 随机选择一个 ID
    DECLARE @RandomID INT = CAST(RAND() * (SELECT COUNT(*) FROM #tb_temp) AS INT) + 1;

    -- 赋值输出参数
    SELECT @v1 = v1, @v2 = v2, @v3 = v3 FROM #tb_temp WHERE ID = @RandomID;
END
