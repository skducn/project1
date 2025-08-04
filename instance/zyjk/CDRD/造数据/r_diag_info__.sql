-- todo 诊断病史 - 诊断类型，诊断名称，ICD10编码

CREATE OR ALTER PROCEDURE r_diag_info__
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
                ('心血管慢性病', '原发性高血压 2 级', 'I10'),
                ('心律失常', '持续性心房颤动', 'I48.1'),
                ('代谢性疾病', '2 型糖尿病伴周围神经病变', 'E11.4'),
                ('缺血性心脏病', '稳定性心绞痛', 'I25.1'),
                ('呼吸系统慢性病', 'COPD 急性加重期', 'J44.1'),
                ('神经系统急症', '急性脑梗死（左侧基底节区）', 'I63.9'),
                ('消化系统疾病', '反流性食管炎（LA-B 级）', 'K21.0'),
                ('骨骼代谢性疾病', '骨质疏松伴腰椎压缩性骨折', 'M80.8'),
                ('内分泌疾病', 'Graves 病', 'E05.0'),
                ('泌尿系统疾病', '慢性肾脏病 3 期（高血压肾病）', 'N18.3');

    -- 随机选择一个 ID
    DECLARE @RandomID INT = CAST(RAND() * (SELECT COUNT(*) FROM #tb_temp) AS INT) + 1;

    -- 赋值输出参数
    SELECT @v1 = v1, @v2 = v2, @v3 = v3 FROM #tb_temp WHERE ID = @RandomID;
END
