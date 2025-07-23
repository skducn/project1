-- 诊断信息表(造数据)优化版
-- 数据量：每名患者5条（共15万）
-- 优化目标：提升性能，每位患者生成5条记录，每条记录使用一条就诊记录
-- 5w,耗时: 0.5827 秒

CREATE OR ALTER PROCEDURE cdrd_patient_diag_info
    @RecordCount INT = 5, -- 每位患者生成5条诊断记录
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- 获取患者数量
    DECLARE @re INT = 1;
    SELECT @re = COUNT(*) FROM a_cdrd_patient_info;
    SET @result = @re * @RecordCount;

    BEGIN TRY
        BEGIN TRANSACTION;

        -- Step 1: 生成1~@RecordCount 的序列（使用递归 CTE 确保唯一）
        ;WITH Numbers AS (
            SELECT 1 AS n
            UNION ALL
            SELECT n + 1 FROM Numbers WHERE n < @RecordCount
        ),

        -- Step 2: 获取所有患者 ID（来自患者主表）
        Patients AS (
            SELECT patient_id
            FROM a_cdrd_patient_info
        ),

        -- Step 3: 为每位患者生成1~@RecordCount 的编号
        PatientSequences AS (
            SELECT p.patient_id, n.n
            FROM Patients p
            CROSS JOIN Numbers n
        ),

        -- Step 4: 获取每位患者的就诊记录（每人最多 @RecordCount 条）
        VisitRecords AS (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY patient_visit_in_time DESC) AS seq
            FROM a_cdrd_patient_visit_info
            WHERE patient_visit_type_key = 1
        ),

        -- Step 5: 关联每位患者生成的序号与就诊记录
        PatientVisitMapping AS (
            SELECT ps.patient_id, ps.n,
                   v.patient_visit_id, v.patient_hospital_visit_id, v.patient_hospital_code, v.patient_case_num
            FROM PatientSequences ps
            LEFT JOIN VisitRecords v
                ON ps.patient_id = v.patient_id
                AND ps.n = v.seq
        ),

        -- Step 6: 一次性生成随机静态字段（避免逐条生成）
        RandomStaticFields AS (
            SELECT p.patient_id,
                   h.name AS RandomHospital,
                   dc.diag_class, dc.diag_name, dc.diag_code,
                   tf.n_key AS diag_is_primary_key, tf.n_value AS diag_is_primary_value,
                   ins.n_key AS in_state_key, ins.n_value AS in_state_value,
                   outs.n_key AS outcome_state_key, outs.n_value AS outcome_state_value
            FROM a_cdrd_patient_info p
            CROSS JOIN (SELECT TOP 1 name FROM ab_hospital ORDER BY NEWID()) h
            CROSS JOIN (SELECT TOP 1 diag_class, diag_name, diag_code FROM ab_diagnosticHistory ORDER BY NEWID()) dc
            CROSS JOIN (SELECT TOP 1 n_key, n_value FROM ab_boolean ORDER BY NEWID()) tf
            CROSS JOIN (SELECT TOP 1 n_key, n_value FROM ab_admissionCondition ORDER BY NEWID()) ins
            CROSS JOIN (SELECT TOP 1 n_key, n_value FROM ab_dischargeStatus ORDER BY NEWID()) outs
        ),

        -- Step 7: 关联患者序列和就诊信息
        FinalData AS (
            SELECT
                pm.patient_id,
                pm.n,
                pm.patient_visit_id,
                pm.patient_hospital_visit_id,
                pm.patient_hospital_code,
                pm.patient_case_num,
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
            INNER JOIN RandomStaticFields rs
                ON pm.patient_id = rs.patient_id
        )

        -- Step 8: 插入数据
        INSERT INTO a_cdrd_patient_diag_info (
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
            diag_is_primary_key,
            diag_is_primary_value,
            diag_code AS patient_diag_code,
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
