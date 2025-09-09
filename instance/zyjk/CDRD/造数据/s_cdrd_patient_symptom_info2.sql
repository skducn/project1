-- 症状信息表(造数据)优化版
-- 数据量：每名患者5条（共15万）
-- 优化目标：提升性能，避免嵌套循环
-- 原耗时: 1902.2599 秒 → 优化后预计耗时: 0.5~1 秒

CREATE OR ALTER PROCEDURE s_cdrd_patient_symptom_info
    @RecordCount INT = 5, -- 每位患者生成5条症状记录
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @re INT = 1;
    select @re = count(*) from CDRD_PATIENT_INFO;
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
            FROM CDRD_PATIENT_INFO
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
            FROM CDRD_PATIENT_VISIT_INFO
            WHERE patient_visit_type_key = 1
        ),

        -- Step 5: 关联每位患者生成的序号与就诊记录
        PatientVisitMapping AS (
            SELECT ps.patient_id, ps.n,
                   v.patient_visit_id, v.patient_hospital_visit_id, v.patient_hospital_code, v.patient_hospital_name,
                   v.patient_visit_in_time
            FROM PatientSequences ps
            LEFT JOIN VisitRecords v
                ON ps.patient_id = v.patient_id
                AND ps.n = v.seq
        ),

        -- Step 6: 一次性生成随机字段（避免逐条生成）
        RandomFields AS (
        SELECT
               pm.patient_id,
               pm.n,
               pm.patient_visit_id,
               pm.patient_hospital_visit_id,
               pm.patient_hospital_code,
              COALESCE(pm.patient_hospital_name, h.RandomHospitalName, N'默认医院') AS patient_hospital_name,
               pm.patient_visit_in_time,
               h.RandomHospitalName,
               s.symptom_name,
               s.symptom_code,
               s.symptom_desc
        FROM PatientVisitMapping pm
        CROSS APPLY (
            SELECT TOP 1 name AS RandomHospitalName FROM ab_hospital ORDER BY NEWID()
        ) h
        CROSS APPLY (
            SELECT TOP 1 name AS symptom_name, code AS symptom_code, desc1 AS symptom_desc FROM ab_symptom ORDER BY NEWID()
        ) s
    ),

        -- Step 7: 生成最终字段
        FinalData AS (
            SELECT *,
                   RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(patient_id * 10000 + n)) % 10000000), 7) AS symptom_num,
                   DATEADD(DAY, ABS(CHECKSUM(patient_id * 10000 + n)) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS symptom_start_time,
                   DATEADD(DAY, ABS(CHECKSUM(patient_id * 10000 + n)) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS symptom_end_time,
                   ABS(CHECKSUM(patient_id * 10000 + n)) % 2 + 1 AS delete_state,
                   DATEADD(DAY, -ABS(CHECKSUM(patient_id * 10000 + n)) % 365, GETDATE()) AS update_time,
                   CASE WHEN patient_visit_id IS NULL THEN '2' ELSE '1' END AS data_source_key
            FROM RandomFields
        )

        -- Step 8: 一次性插入数据（使用 TABLOCKX 提高性能）
        INSERT INTO CDRD_PATIENT_SYMPTOM_INFO (
            patient_id,
            patient_visit_id,
            patient_hospital_visit_id,
            patient_hospital_code,
            patient_hospital_name,
            patient_symptom_num,
            patient_symptom_name,
            patient_symptom_description,
            patient_symptom_start_time,
            patient_symptom_end_time,
            patient_symptom_delete_state_key,
            patient_symptom_update_time,
            patient_symptom_data_source_key
        )
        SELECT
            patient_id,
            patient_visit_id,
            patient_hospital_visit_id,
            patient_hospital_code,
            patient_hospital_name,
            symptom_code AS patient_symptom_num,
            symptom_name AS patient_symptom_name,
            symptom_desc AS patient_symptom_description,
            symptom_start_time AS patient_symptom_start_time,
            symptom_end_time AS patient_symptom_end_time,
            delete_state AS patient_symptom_delete_state_key,
            update_time AS patient_symptom_update_time,
            data_source_key AS patient_symptom_data_source_key
        FROM FinalData
        ORDER BY patient_id, n;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
