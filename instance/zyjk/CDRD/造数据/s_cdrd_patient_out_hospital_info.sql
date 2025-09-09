-- todo  出院记录表(造数据)
-- 数据量：每名患者2条（共6万）
-- 耗时: 4.0556 秒
CREATE OR ALTER PROCEDURE s_cdrd_patient_out_hospital_info
    @RecordCount INT = 2,
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- 获取就诊表中住院记录数量
    DECLARE @re INT = 1;
    select @re = count(*) from CDRD_PATIENT_INFO;
    SET @result = @re * @RecordCount;

    -- 主诉
    DECLARE @ChiefComplaint NVARCHAR(MAX) = '患者，女，29 岁，2003 年 1 月 6 日从广州出差回太原，1 月 8 日突感发热，常伴寒颤、头痛、乏力、关节酸痛，并干咳，咳血丝痰。'

    -- 入院诊断
    DECLARE @AdmissionDiagnosis NVARCHAR(MAX) = '初步诊断：发热待查，考虑传染性非典型肺炎（SARS）可能性大。
诊断依据：
流行病学史：患者有广州出差史，广州当时为 SARS 疫区。
临床表现：患者出现发热、寒颤、头痛、乏力、关节酸痛、干咳及咳血丝痰等症状，符合 SARS 的常见临床表现。
体格检查：体温 39℃，有少许湿啰音。'


    -- 诊疗经过
    DECLARE @CourseOfDiagnosisAndTreatment NVARCHAR(MAX) = '一般治疗：患者入院后立即给予单间隔离，卧床休息，给予吸氧治疗，维持血氧饱和度在 95% 以上。同时，加强营养支持，给予静脉营养补液，保证患者每日所需的能量和营养物质。
抗病毒治疗：入院后即开始给予利巴韦林抗病毒治疗，剂量为每日 1000mg，分两次静脉滴注，疗程为 10 天。
抗感染治疗：考虑到患者可能存在继发细菌感染，给予头孢曲松钠抗感染治疗，剂量为每日 2g，静脉滴注，每日一次，疗程为 7 天。
糖皮质激素治疗：根据患者的病情和胸部影像学表现，给予甲泼尼龙琥珀酸钠静脉滴注，初始剂量为每日 80mg，分两次给药。随着病情的好转，逐渐减少糖皮质激素的用量，每周减量 10-20mg，直至停药。
对症治疗：对于患者的发热症状，给予物理降温及对乙酰氨基酚口服退热治疗；对于干咳症状，给予右美沙芬止咳治疗。'

    -- 出院诊断 - 定义多个可能的诊断值
    DECLARE @DischargeDiagnoses TABLE (id INT IDENTITY(1,1), diagnosis NVARCHAR(MAX));
    INSERT INTO @DischargeDiagnoses (diagnosis)
    SELECT patient_out_hospital_diag
    FROM ab_outHospitalDiag;

    -- 出院情况
    DECLARE @DischargeStatus NVARCHAR(MAX) = '症状体征：患者体温正常已超过 3 天，咳嗽、呼吸困难等呼吸道症状基本消失，精神状态良好，食欲正常。
实验室检查：血常规提示白细胞、淋巴细胞计数均恢复正常范围。连续两次 SARS 病毒核酸检测阴性（间隔 24 小时以上）。
影像学检查：胸部 CT 显示双肺斑片状阴影明显吸收，肺部炎症较入院时明显好转。';

    --出院医嘱
    DECLARE @DischargeInstructions NVARCHAR(MAX) = '出院后继续居家隔离 7 天，期间避免与他人密切接触，保持室内通风良好。
注意休息，避免劳累，保持均衡饮食，适当进行室内活动。
每日监测体温两次，如有发热（体温≥38℃）、咳嗽、呼吸困难等不适症状，及时就医。
一周后回医院复查胸部 X 线、血常规等相关检查。
遵医嘱按时服药，如有不适及时告知医生。';

    BEGIN TRY
        BEGIN TRANSACTION;

        -- 将出院类型加载到临时表并分配序号
        SELECT n_key, n_value, ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS idx
        INTO #TempDischargeTypes
        FROM ab_dischargeRecordType;

        -- 获取出院类型的总数量
        DECLARE @MaxType INT;
        SELECT @MaxType = COUNT(*) FROM #TempDischargeTypes;

        -- 获取出院诊断的数量
        DECLARE @MaxDiagnosis INT;
        SELECT @MaxDiagnosis = COUNT(*) FROM @DischargeDiagnoses;

        ;WITH VisitRecords AS (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY patient_visit_in_time DESC) AS seq
            FROM CDRD_PATIENT_VISIT_INFO
            WHERE patient_visit_type_key = 2
        ),

        PatientRecords AS (
            SELECT vr.*
            FROM VisitRecords vr
            WHERE vr.seq <= @RecordCount
        ),

        -- 使用 CHECKSUM 生成伪随机数，避免每次 NEWID()
        RandomFields AS (
            SELECT pr.*,
                   t.n_key AS patient_out_hospital_type_key,
                   t.n_value AS patient_out_hospital_type_value,
                   RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(pr.patient_id * 1000 + pr.seq)) % 10000000), 7) AS record_num,
                   DATEADD(DAY, -ABS(CHECKSUM(pr.patient_id * 1000 + pr.seq)) % 365, GETDATE()) AS record_time,
                   DATEADD(DAY, -ABS(CHECKSUM(pr.patient_id * 1000 + pr.seq)) % 365, GETDATE()) AS update_time,
                   ABS(CHECKSUM(pr.patient_id * 1000 + pr.seq)) % @MaxDiagnosis + 1 AS diagnosis_id
            FROM PatientRecords pr
            CROSS APPLY (
                SELECT TOP 1 *
                FROM #TempDischargeTypes
                WHERE idx = ABS(CHECKSUM(pr.patient_id, pr.seq)) % @MaxType + 1
            ) t
        )

        INSERT INTO CDRD_PATIENT_OUT_HOSPITAL_INFO WITH (TABLOCKX) (
            patient_out_hospital_type_key,
            patient_out_hospital_type_value,
            patient_id,
            patient_visit_id,
            patient_hospital_visit_id,
            patient_hospital_code,
            patient_hospital_name,
            patient_out_hospital_record_num,
            patient_out_hospital_main_describe,
            patient_out_hospital_in_situation,
            patient_out_hospital_in_diag,
            patient_out_hospital_diag_process,
            patient_out_hospital_diag,
            patient_out_hospital_situation,
            patient_out_hospital_advice,
            patient_out_hospital_record_time,
            patient_out_hospital_update_time,
            patient_out_hospital_source_key
        )
        SELECT
            rf.patient_out_hospital_type_key,
            rf.patient_out_hospital_type_value,
            rf.patient_id,
            rf.patient_visit_id,
            rf.patient_hospital_visit_id,
            rf.patient_hospital_code,
            rf.patient_hospital_name,
            rf.record_num,
            @ChiefComplaint,  -- 主诉
            @AdmissionDiagnosis,  --入院情况
            rf.patient_visit_diag,
            @CourseOfDiagnosisAndTreatment,  -- 入院诊断
            d.diagnosis,  -- 随机出院诊断
            @DischargeStatus,  -- 出院情况
            @DischargeInstructions,  --出院医嘱
            rf.record_time,
            rf.update_time,
            '1'
        FROM RandomFields rf
        JOIN @DischargeDiagnoses d ON d.id = rf.diagnosis_id
        ORDER BY rf.patient_id;


        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
