-- 诊断信息表(造数据)优化版
-- 数据量：每名患者5条（共15万）
-- 需求：https://docs.qq.com/doc/DYnZXTVZ1THpPVEVC?g=X2hpZGRlbjpoaWRkZW4xNzUzMzM4MjMzNDAx#g=X2hpZGRlbjpoaWRkZW4xNzUzMzM4MjMzNDAx
-- 5w,耗时: 0.5827 秒

CREATE OR ALTER PROCEDURE s_cdrd_patient_diag_info
    @RecordCount INT = 5, -- 每位患者生成5条诊断记录
    @result INT OUTPUT
AS
BEGIN
    -- 1. 初始化设置
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- 获取患者数量
    DECLARE @re INT = 1;
    SELECT @re = COUNT(*) FROM CDRD_PATIENT_INFO;
    SET @result = @re * @RecordCount;

    BEGIN TRY
        BEGIN TRANSACTION;

        -- Step 1: 生成1~@RecordCount 的序列（使用递归 CTE 确保唯一）
        -- 使用递归CTE生成1到@RecordCount的数字序列
        -- 确保为每位患者生成指定数量的记录
        ;WITH Numbers AS (
            SELECT 1 AS n
            UNION ALL
            SELECT n + 1 FROM Numbers WHERE n < @RecordCount
        ),

        -- Step 2: 获取所有患者 ID（来自患者主表）
        Patients AS (
            SELECT patient_id
            FROM CDRD_PATIENT_INFO
        ),

        -- Step 3: 为每位患者生成1~@RecordCount 的编号
        -- 通过 CROSS JOIN 将每位患者与数字序列关联
        PatientSequences AS (
            SELECT p.patient_id, n.n
            FROM Patients p
            CROSS JOIN Numbers n
        ),

        -- Step 4: 获取每位患者的就诊记录（每人最多 @RecordCount 条）
        -- 从就诊信息表 a_cdrd_patient_visit_info 获取门诊记录
        -- 使用 ROW_NUMBER() 为每位患者的就诊记录编号
        -- 只选择门诊记录（patient_visit_type_key = 1）
        VisitRecords AS (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY patient_visit_in_time DESC) AS seq
            FROM CDRD_PATIENT_VISIT_INFO
            WHERE patient_visit_type_key = 1
        ),

        -- Step 5: 关联每位患者生成的序号与就诊记录
        -- 将患者序列与就诊记录关联
        -- 使用LEFT JOIN确保即使没有就诊记录也能生成诊断记录
        PatientVisitMapping AS (
            SELECT ps.patient_id, ps.n,
                   v.patient_visit_id, v.patient_hospital_visit_id, v.patient_hospital_code, v.patient_case_num
            FROM PatientSequences ps
            LEFT JOIN VisitRecords v
                ON ps.patient_id = v.patient_id
                AND ps.n = v.seq
        ),

        -- Step 6: 创建临时表存储随机诊断信息
        RandomDiagData AS (
            SELECT
                pm.patient_id,
                pm.n,
                ROW_NUMBER() OVER (ORDER BY NEWID()) AS rn
            FROM PatientVisitMapping pm
        ),

        -- Step 7: 获取所有需要的随机数据并关联
        HospitalData AS (
            SELECT
                rd.patient_id,
                rd.n,
                h.name AS RandomHospital,
                ROW_NUMBER() OVER (PARTITION BY rd.patient_id, rd.n ORDER BY NEWID()) AS rn
            FROM RandomDiagData rd
            CROSS JOIN ab_hospital h
        ),

        DiagnosticData AS (
            SELECT
                rd.patient_id,
                rd.n,
                dh.diag_class,
                dh.diag_name,
                dh.diag_code,
                ROW_NUMBER() OVER (PARTITION BY rd.patient_id, rd.n ORDER BY NEWID()) AS rn
            FROM RandomDiagData rd
            CROSS JOIN ab_diagnosticHistory dh
        ),

        BooleanData AS (
            SELECT
                rd.patient_id,
                rd.n,
                ab.n_key AS diag_is_primary_key,
                ab.n_value AS diag_is_primary_value,
                ROW_NUMBER() OVER (PARTITION BY rd.patient_id, rd.n ORDER BY NEWID()) AS rn
            FROM RandomDiagData rd
            CROSS JOIN ab_boolean ab
        ),

        AdmissionData AS (
            SELECT
                rd.patient_id,
                rd.n,
                aa.n_key AS in_state_key,
                aa.n_value AS in_state_value,
                ROW_NUMBER() OVER (PARTITION BY rd.patient_id, rd.n ORDER BY NEWID()) AS rn
            FROM RandomDiagData rd
            CROSS JOIN ab_admissionCondition aa
        ),

        DischargeData AS (
            SELECT
                rd.patient_id,
                rd.n,
                ad.n_key AS outcome_state_key,
                ad.n_value AS outcome_state_value,
                ROW_NUMBER() OVER (PARTITION BY rd.patient_id, rd.n ORDER BY NEWID()) AS rn
            FROM RandomDiagData rd
            CROSS JOIN ab_dischargeStatus ad
        ),

        -- Step 8: 为每个患者-序号组合选择一条随机记录
        RandomStaticFields AS (
            SELECT
                hd.patient_id,
                hd.n,
                hd.RandomHospital,
                dd.diag_class,
                dd.diag_name,
                dd.diag_code,
                bd.diag_is_primary_key,
                bd.diag_is_primary_value,
                ad.in_state_key,
                ad.in_state_value,
                ddg.outcome_state_key,
                ddg.outcome_state_value
            FROM (
                SELECT patient_id, n, RandomHospital
                FROM (
                    SELECT patient_id, n, RandomHospital,
                           ROW_NUMBER() OVER (PARTITION BY patient_id, n ORDER BY rn) AS final_rn
                    FROM HospitalData
                ) h WHERE final_rn = 1
            ) hd
            JOIN (
                SELECT patient_id, n, diag_class, diag_name, diag_code
                FROM (
                    SELECT patient_id, n, diag_class, diag_name, diag_code,
                           ROW_NUMBER() OVER (PARTITION BY patient_id, n ORDER BY rn) AS final_rn
                    FROM DiagnosticData
                ) d WHERE final_rn = 1
            ) dd ON hd.patient_id = dd.patient_id AND hd.n = dd.n
            JOIN (
                SELECT patient_id, n, diag_is_primary_key, diag_is_primary_value
                FROM (
                    SELECT patient_id, n, diag_is_primary_key, diag_is_primary_value,
                           ROW_NUMBER() OVER (PARTITION BY patient_id, n ORDER BY rn) AS final_rn
                    FROM BooleanData
                ) b WHERE final_rn = 1
            ) bd ON hd.patient_id = bd.patient_id AND hd.n = bd.n
            JOIN (
                SELECT patient_id, n, in_state_key, in_state_value
                FROM (
                    SELECT patient_id, n, in_state_key, in_state_value,
                           ROW_NUMBER() OVER (PARTITION BY patient_id, n ORDER BY rn) AS final_rn
                    FROM AdmissionData
                ) a WHERE final_rn = 1
            ) ad ON hd.patient_id = ad.patient_id AND hd.n = ad.n
            JOIN (
                SELECT patient_id, n, outcome_state_key, outcome_state_value
                FROM (
                    SELECT patient_id, n, outcome_state_key, outcome_state_value,
                           ROW_NUMBER() OVER (PARTITION BY patient_id, n ORDER BY rn) AS final_rn
                    FROM DischargeData
                ) d WHERE final_rn = 1
            ) ddg ON hd.patient_id = ddg.patient_id AND hd.n = ddg.n
        ),

        -- Step 9: 关联患者序列和就诊信息
        FinalData AS (
            SELECT
                pm.patient_id,
                pm.n,
                ISNULL(pm.patient_visit_id, RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(pm.patient_id * 10000 + pm.n)) % 10000000), 7)) AS patient_visit_id,
                ISNULL(pm.patient_hospital_visit_id, RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(pm.patient_id * 10000 + pm.n)) % 10000000), 7)) AS patient_hospital_visit_id,
                ISNULL(pm.patient_hospital_code, RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(pm.patient_id * 10000 + pm.n)) % 10000000), 7)) AS patient_hospital_code,
                ISNULL(pm.patient_case_num, RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(pm.patient_id * 10000 + pm.n)) % 10000000), 7)) AS patient_case_num,
                pm.n AS data_source_key,
                rs.RandomHospital,
                rs.diag_class,
                rs.diag_name,
                rs.diag_code,
                rs.diag_is_primary_key,
                rs.diag_is_primary_value,
                rs.in_state_key,
                rs.in_state_value,
                rs.outcome_state_key,
                rs.outcome_state_value,
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(pm.patient_id * 10000 + pm.n)) % 10000000), 7) AS diag_num,
                DATEADD(DAY, ABS(CHECKSUM(pm.patient_id * 10000 + pm.n)) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS diag_date,
                DATEADD(DAY, -ABS(CHECKSUM(pm.patient_id * 10000 + pm.n)) % 365, GETDATE()) AS diag_update_time,
                ABS(CHECKSUM(pm.patient_id * 10000 + pm.n)) % 2 + 1 AS diag_delete_state
            FROM PatientVisitMapping pm
            INNER JOIN RandomStaticFields rs ON pm.patient_id = rs.patient_id AND pm.n = rs.n
        )

        -- 4. 数据插入
        -- Step 10: 插入数据
        INSERT INTO CDRD_PATIENT_DIAG_INFO (
            patient_id,
            patient_visit_id,
            patient_hospital_visit_id,
            patient_hospital_code,
            patient_hospital_name,
            patient_case_num,
            patient_diag_num,
            patient_diag_class,
            patient_diag_name,
            patient_diag_is_primary_key,
            patient_diag_is_primary_value,
            patient_diag_code,
            patient_diag_ata,
            patient_diag_cas,
            patient_in_state_key,
            patient_in_state_value,
            patient_outcome_state_key,
            patient_outcome_state_value,
            patient_diag_date,
            patient_diag_delete_state_key,
            patient_diag_update_time,
            patient_diag_data_source_key
        )
        SELECT
            patient_id,
            patient_visit_id,
            patient_hospital_visit_id,
            patient_hospital_code,
            RandomHospital AS patient_hospital_name,
            patient_case_num,
            diag_num AS patient_diag_num,
            diag_class AS patient_diag_class,
            diag_name AS patient_diag_name,
            '1','是',
            diag_code AS patient_diag_code,
            RIGHT('0000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(patient_id * 10000 + n)) % 10000), 4) AS patient_diag_ata,
            RIGHT('0000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(patient_id * 10000 + n * 2)) % 10000), 4) AS patient_diag_cas,
            in_state_key AS patient_in_state_key,
            in_state_value AS patient_in_state_value,
            outcome_state_key AS patient_outcome_state_key,
            outcome_state_value AS patient_outcome_state_value,
            diag_date AS patient_diag_date,
            diag_delete_state AS patient_diag_delete_state_key,
            diag_update_time AS patient_diag_update_time,
            '1' AS patient_diag_data_source_key
        FROM FinalData
        ORDER BY patient_id, n;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
