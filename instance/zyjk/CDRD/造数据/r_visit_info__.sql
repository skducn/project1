-- todo 就诊信息 - 就诊诊断

CREATE OR ALTER PROCEDURE r_visit_info__
    @v1 nvarchar(550) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- 生成临时表
    IF OBJECT_ID('tempdb..#tb_temp') IS NOT NULL DROP TABLE #tb_temp;
    CREATE TABLE #tb_temp (ID INT IDENTITY(1,1), v1 NVARCHAR(550));
    INSERT INTO #tb_temp (v1) VALUES
            ('患者因 "反复头晕 1 月余，血压波动在 150-160/95-100mmHg" 入院，伴视物模糊，无恶心呕吐'),
            ('入院主诉 "心悸、气短 3 周"，心电图示房颤心律，心室率 110 次 / 分，心超示左房增大（42mm）'),
            ('因 "双足麻木刺痛半年，加重伴行走困难 1 月" 入院，随机血糖 15.6mmol/L，肌电图示周围神经传导速度减慢'),
            ('以 "反复胸痛 3 个月，劳累后加重" 收治，冠脉 CTA 示前降支狭窄 70%，运动负荷试验阳性'),
            ('因 "咳嗽咳痰加重伴气促 1 周" 急诊入院，血气分析示 PaO2 55mmHg，肺功能 FEV1 占预计值 48%'),
            ('突发 "右侧肢体无力伴言语含糊 6 小时" 入院，NIHSS 评分 8 分，头 MRI 示左侧基底节区新鲜梗死灶（1.5×2.0cm）'),
            ('因 "反酸烧心半年，加重伴胸痛 2 周" 入院，胃镜见食管下段多发纵向糜烂，最长径＞5mm'),
            ('以 "腰部剧痛 1 天" 入院，X 线示 L1 椎体压缩性骨折（椎体高度丢失约 30%），骨密度 T 值 - 3.5'),
            ('因 "心悸、消瘦 3 月（体重下降 8kg）" 收治，甲功示 FT3 15.2pmol/L，TRAb 阳性，甲状腺超声示弥漫性肿大'),
            ('因 "夜尿增多伴乏力半年" 入院，eGFR 42ml/min，尿蛋白定量 1.2g/24h，肾穿示高血压性肾小球硬化');

    -- 随机选择一个 ID
    DECLARE @RandomID INT = CAST(RAND() * (SELECT COUNT(*) FROM #tb_temp) AS INT) + 1;

    -- 赋值输出参数
    SELECT @v1 = v1 FROM #tb_temp WHERE ID = @RandomID;
END
