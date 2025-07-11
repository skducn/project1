-- todo 症状信息 - 症状名称，症状编号，具体描述

CREATE OR ALTER PROCEDURE r_symptom_info__
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
            ('头晕', N'SYM101', N'患者反复头晕 1 个月，血压 150-160/95-100mmHg，无靶器官损害'),
            ('心悸', N'SYM102', N'自觉心跳不规则，心电图示 P 波消失，心室率 110 次 / 分'),
            ('手足麻木', N'SYM103', N'双足对称性刺痛感，HbA1c 8.5%，神经传导速度减慢'),
            ('胸痛', N'SYM104', N'劳累后胸骨后压榨性疼痛，持续 3-5 分钟，硝酸甘油可缓解'),
            ('气促', N'SYM105', N'活动后呼吸困难加重，FEV1/FVC 65%，伴咳嗽、黄痰'),
            ('肢体无力', N'SYM106', N'突发右侧肢体乏力，NIHSS 评分 6 分，MRI 示 DWI 高信号'),
            ('反酸', N'SYM107', N'餐后胸骨后烧灼感，胃镜见食管下段条状糜烂'),
            ('腰背痛', N'SYM108', N'轻微外伤后 L1 椎体压缩性骨折，骨密度 T 值 - 3.2'),
            ('体重下降', N'SYM109', N'3 个月体重减轻 8kg，FT3 12.5pmol/L，TSH<0.01mIU/L'),
            ('夜尿增多', N'SYM110', N'夜间排尿 3-4 次，eGFR 45ml/min/1.73m2，尿蛋白 1+');


    -- 随机选择一个 ID
    DECLARE @RandomID INT = CAST(RAND() * (SELECT COUNT(*) FROM #tb_temp) AS INT) + 1;

    -- 赋值输出参数
    SELECT @v1 = v1, @v2 = v2, @v3 = v3 FROM #tb_temp WHERE ID = @RandomID;
END
