-- 优化后的用药信息表造数据存储过程
CREATE OR ALTER PROCEDURE s_CDRD_PATIENT_DRUG_INFO_test
    @RecordCount INT = 8,
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @re INT = 1;
    SELECT @re = COUNT(*) FROM CDRD_PATIENT_INFO;
    SET @result = @re * @RecordCount;

    -- 创建临时表存储基础数据，按patient_id排序
    CREATE TABLE #TempPatients (
        id INT IDENTITY(1,1),
        patient_id INT PRIMARY KEY
    )

    -- 预加载数据到临时表，按patient_id排序
    INSERT INTO #TempPatients (patient_id)
    SELECT patient_id FROM CDRD_PATIENT_INFO ORDER BY patient_id

    -- 预加载随机数据
    CREATE TABLE #RandomDrugs (
        id INT IDENTITY(1,1) PRIMARY KEY,
        v1 NVARCHAR(100),
        v2 NVARCHAR(100),
        v3 NVARCHAR(100),
        v4 NVARCHAR(100),
        v5 NVARCHAR(100),
        v6 NVARCHAR(100),
        v7 NVARCHAR(100)
    )

    CREATE TABLE #RandomHospitals (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(100)
    )

    INSERT INTO #RandomDrugs (v1, v2, v3, v4, v5, v6, v7)
    SELECT TOP 5000 v1, v2, v3, v4, v5, v6, v7
    FROM ab_drug
    ORDER BY NEWID()

    INSERT INTO #RandomHospitals (name)
    SELECT TOP 1000 name
    FROM ab_hospital
    ORDER BY NEWID()

    -- 批量生成数据
    -- 1. 生成只有patient_id的3条记录（每患者）
    ;WITH PatientNumbers AS (
        SELECT patient_id, id AS patient_seq
        FROM #TempPatients
    ),
    Numbers AS (
        SELECT 1 AS num UNION ALL SELECT 2 UNION ALL SELECT 3
    )
    INSERT INTO CDRD_PATIENT_DRUG_INFO_test (
        patient_id, patient_superior_advice_id, patient_superior_advice_type,
        patient_hospital_visit_id, patient_hospital_code, patient_hospital_name,
        patient_recipe_advice_num, patient_drug_name, patient_drug_specs,
        patient_drug_frequency, patient_drug_once_dose, patient_drug_dose_unit,
        patient_drug_usage, patient_drug_qty, patient_drug_begin_time,
        patient_drug_end_time, patient_drug_delete_state_key,
        patient_drug_update_time, patient_drug_source_key
    )
    SELECT
        pn.patient_id,
        '', -- 无上级医嘱ID
        '1', -- 门诊医嘱类型
        '', -- 无就诊编号
        '', -- 无医疗机构编号
        rh.name, -- 随机医院名称
        '处方明细/医嘱编号',
        rd.v1, rd.v2, rd.v3, rd.v4, rd.v5, rd.v6, rd.v7,
        DATEADD(DAY, ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01'),
        DATEADD(DAY, ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01'),
        ABS(CHECKSUM(NEWID())) % 2 + 1,
        DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()),
        '2' -- 数据来源
    FROM PatientNumbers pn
    CROSS JOIN Numbers n
    JOIN #RandomDrugs rd ON (pn.patient_seq + n.num) % 5000 + 1 = rd.id
    JOIN #RandomHospitals rh ON (pn.patient_seq + n.num) % 1000 + 1 = rh.id

    -- 2. 生成包含就诊信息的5条记录（每患者）
    -- 先获取一些就诊相关信息
    DECLARE @VisitInfo TABLE (
        patient_id INT,
        patient_hospital_visit_id NVARCHAR(100),
        patient_hospital_code NVARCHAR(100),
        patient_hospital_name NVARCHAR(100),
        patient_visit_in_time DATETIME
    )

    INSERT INTO @VisitInfo
    SELECT
        patient_id,
        patient_hospital_visit_id,
        patient_hospital_code,
        patient_hospital_name,
        patient_visit_in_time
    FROM CDRD_PATIENT_VISIT_INFO

    -- 2.1 门诊记录（3条）
    ;WITH PatientNumbers AS (
        SELECT patient_id, id AS patient_seq
        FROM #TempPatients
    ),
    Numbers AS (
        SELECT 1 AS num UNION ALL SELECT 2 UNION ALL SELECT 3
    ),
    ClinicAdviceInfo AS (
        SELECT
            patient_id,
            patient_clinic_advice_id,
            ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY
                CASE WHEN patient_clinic_advice_id IS NULL THEN 1 ELSE 0 END,
                patient_clinic_advice_id
            ) AS rn
        FROM (
            SELECT patient_id, patient_clinic_advice_id FROM CDRD_PATIENT_CLINIC_ADVICE_INFO
            UNION ALL
            SELECT patient_id, NULL AS patient_clinic_advice_id
            FROM #TempPatients
        ) ca
    )
    INSERT INTO CDRD_PATIENT_DRUG_INFO_test (
        patient_id, patient_superior_advice_id, patient_superior_advice_type,
        patient_hospital_visit_id, patient_hospital_code, patient_hospital_name,
        patient_recipe_advice_num, patient_drug_name, patient_drug_specs,
        patient_drug_frequency, patient_drug_once_dose, patient_drug_dose_unit,
        patient_drug_usage, patient_drug_qty, patient_drug_begin_time,
        patient_drug_end_time, patient_drug_delete_state_key,
        patient_drug_update_time, patient_drug_source_key
    )
    SELECT
        pn.patient_id,
        ISNULL(ca.patient_clinic_advice_id, ''), -- 门诊医嘱ID
        '1', -- 门诊医嘱类型
        ISNULL(vi.patient_hospital_visit_id, ''),
        ISNULL(vi.patient_hospital_code, ''),
        ISNULL(vi.patient_hospital_name, ''),
        '处方明细/医嘱编号',
        rd.v1, rd.v2, rd.v3, rd.v4, rd.v5, rd.v6, rd.v7,
        ISNULL(vi.patient_visit_in_time, DATEADD(DAY, ABS(CHECKSUM(NEWID())) % 365, '2023-01-01')),
        ISNULL(vi.patient_visit_in_time, DATEADD(DAY, ABS(CHECKSUM(NEWID())) % 365, '2023-01-01')),
        ABS(CHECKSUM(NEWID())) % 2 + 1,
        DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()),
        '1' -- 数据来源
    FROM PatientNumbers pn
    CROSS JOIN Numbers n
    LEFT JOIN @VisitInfo vi ON pn.patient_id = vi.patient_id
    LEFT JOIN ClinicAdviceInfo ca ON pn.patient_id = ca.patient_id AND ca.rn = n.num
    JOIN #RandomDrugs rd ON (pn.patient_seq + n.num) % 5000 + 1 = rd.id

    -- 2.2 住院记录（2条）
    ;WITH PatientNumbers AS (
        SELECT patient_id, id AS patient_seq
        FROM #TempPatients
    ),
    Numbers AS (
        SELECT 1 AS num UNION ALL SELECT 2
    ),
    HospitalAdviceInfo AS (
        SELECT
            patient_id,
            patient_hospital_advice_id,
            ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY
                CASE WHEN patient_hospital_advice_id IS NULL THEN 1 ELSE 0 END,
                patient_hospital_advice_id
            ) AS rn
        FROM (
            SELECT patient_id, patient_hospital_advice_id FROM CDRD_PATIENT_HOSPITAL_ADVICE_INFO
            UNION ALL
            SELECT patient_id, NULL AS patient_hospital_advice_id
            FROM #TempPatients
        ) ha
    )
    INSERT INTO CDRD_PATIENT_DRUG_INFO_test (
        patient_id, patient_superior_advice_id, patient_superior_advice_type,
        patient_hospital_visit_id, patient_hospital_code, patient_hospital_name,
        patient_recipe_advice_num, patient_drug_name, patient_drug_specs,
        patient_drug_frequency, patient_drug_once_dose, patient_drug_dose_unit,
        patient_drug_usage, patient_drug_qty, patient_drug_begin_time,
        patient_drug_end_time, patient_drug_delete_state_key,
        patient_drug_update_time, patient_drug_source_key
    )
    SELECT
        pn.patient_id,
        ISNULL(ha.patient_hospital_advice_id, ''), -- 住院医嘱ID
        '2', -- 住院医嘱类型
        ISNULL(vi.patient_hospital_visit_id, ''),
        ISNULL(vi.patient_hospital_code, ''),
        ISNULL(vi.patient_hospital_name, ''),
        '处方明细/医嘱编号',
        rd.v1, rd.v2, rd.v3, rd.v4, rd.v5, rd.v6, rd.v7,
        ISNULL(vi.patient_visit_in_time, DATEADD(DAY, ABS(CHECKSUM(NEWID())) % 365, '2023-01-01')),
        ISNULL(vi.patient_visit_in_time, DATEADD(DAY, ABS(CHECKSUM(NEWID())) % 365, '2023-01-01')),
        ABS(CHECKSUM(NEWID())) % 2 + 1,
        DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()),
        '1' -- 数据来源
    FROM PatientNumbers pn
    CROSS JOIN Numbers n
    LEFT JOIN @VisitInfo vi ON pn.patient_id = vi.patient_id
    LEFT JOIN HospitalAdviceInfo ha ON pn.patient_id = ha.patient_id AND ha.rn = n.num
    JOIN #RandomDrugs rd ON (pn.patient_seq * 2 + n.num) % 5000 + 1 = rd.id

    -- 清理临时表
    DROP TABLE #TempPatients
    DROP TABLE #RandomDrugs
    DROP TABLE #RandomHospitals
END
