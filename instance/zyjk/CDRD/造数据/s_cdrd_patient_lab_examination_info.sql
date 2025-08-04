-- 实验室检查信息表(造数据)优化版
-- 数据量：每名患者5条（共15万）
-- 优化目标：提升性能，避免嵌套循环
-- 5w, 耗时: 0.4701 秒

CREATE OR ALTER PROCEDURE s_cdrd_patient_lab_examination_info
    @RecordCount INT = 5, -- 每位患者生成5条实验室检查记录
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @re INT = 1;
    SELECT @re = COUNT(*) FROM CDRD_PATIENT_INFO;
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
            SELECT *,
                   h.RandomHospitalName AS RandomHospitalName_,
                   l.report_name AS report_name_,
                   l.sample_type AS sample_type_,
                   l.project_name AS project_name_
            FROM PatientVisitMapping pm
            CROSS APPLY (
                SELECT TOP 1 name AS RandomHospitalName FROM ab_hospital ORDER BY NEWID()
            ) h
            CROSS APPLY (
                SELECT TOP 1 reportname AS report_name, sampletype AS sample_type, projectname AS project_name FROM ab_lab ORDER BY NEWID()
            ) l
        )
        ,

        -- Step 7: 生成最终字段
        FinalData AS (
            SELECT *,
                   RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(patient_id * 10000 + n)) % 10000000), 7) AS report_num,
                   RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(patient_id * 10000 + n)) % 10000000), 7) AS source_report_num,
                   DATEADD(DAY, ABS(CHECKSUM(patient_id * 10000 + n)) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS test_time,
                   DATEADD(DAY, ABS(CHECKSUM(patient_id * 10000 + n)) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS sample_time,
                   DATEADD(DAY, ABS(CHECKSUM(patient_id * 10000 + n)) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS report_time,
                   DATEADD(DAY, -ABS(CHECKSUM(patient_id * 10000 + n)) % 365, GETDATE()) AS update_time,
                   ABS(CHECKSUM(patient_id * 10000 + n)) % 2 + 1 AS delete_state,
                   CASE WHEN patient_visit_id IS NULL THEN '2' ELSE '1' END AS data_source_key
            FROM RandomFields
        )

        -- Step 8: 一次性插入数据（使用 TABLOCKX 提高性能）
        INSERT INTO CDRD_PATIENT_LAB_EXAMINATION_INFO (
            patient_id,
            patient_visit_id,
            patient_hospital_visit_id,
            patient_hospital_code,
            patient_hospital_name,
            patient_lab_examination_report_num,
            patient_lab_examination_source_report_num,
            patient_lab_examination_report_name,
            patient_lab_examination_sample_type,
            patient_lab_examination_test_time,
            patient_lab_examination_sampling_time,
            patient_lab_examination_report_time,
            patient_lab_examination_delete_state_key,
            patient_lab_examination_update_time,
            patient_lab_examination_data_source_key
        )
        SELECT
            patient_id,
            patient_visit_id,
            patient_hospital_visit_id,
            patient_hospital_code,
            RandomHospitalName AS patient_hospital_name,
            report_num AS patient_lab_examination_report_num,
            source_report_num AS patient_lab_examination_source_report_num,
            report_name AS patient_lab_examination_report_name,
            sample_type AS patient_lab_examination_sample_type,
            test_time AS patient_lab_examination_test_time,
            sample_time AS patient_lab_examination_sampling_time,
            report_time AS patient_lab_examination_report_time,
            delete_state AS patient_lab_examination_delete_state_key,
            update_time AS patient_lab_examination_update_time,
            data_source_key AS patient_lab_examination_data_source_key
        FROM FinalData
        ORDER BY patient_id, n;

        -- Step 9: 设置输出参数
--         SELECT @result = COUNT(*) FROM FinalData;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
