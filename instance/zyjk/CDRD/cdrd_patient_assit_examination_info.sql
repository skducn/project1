-- 辅助检查信息表(造数据)优化版
-- 数据量：每名患者5条（共15万）
-- 优化目标：提升性能，避免嵌套循环
-- 5w, 耗时: 8.1996 秒

CREATE OR ALTER PROCEDURE cdrd_patient_assit_examination_info
    @RecordCount INT = 5, -- 每位患者生成5条辅助检查记录
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @re INT = 1;
    select @re = count(*) from a_cdrd_patient_info;
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
                   v.patient_visit_id, v.patient_hospital_visit_id, v.patient_hospital_code, v.patient_hospital_name,
                   v.patient_visit_in_time
            FROM PatientSequences ps
            LEFT JOIN VisitRecords v
                ON ps.patient_id = v.patient_id
                AND ps.n = v.seq
        ),

        -- Step 6: 一次性生成随机字段（避免逐条生成）
        -- Step 6: 一次性生成随机字段（避免逐条生成）
        RandomFields AS (
            SELECT
                   pm.patient_id,
                   pm.n,
                   pm.patient_visit_id,
                   pm.patient_hospital_visit_id,
                   pm.patient_hospital_code,
                   pm.patient_hospital_name,
                   pm.patient_visit_in_time,

                   h.RandomHospitalName,
                   CASE
                       WHEN pm.n <= 2 THEN '电生理检查'
                       WHEN pm.n = 3 THEN '超声检查'
                       WHEN pm.n = 4 THEN '内镜检查'
                       WHEN pm.n = 5 THEN '病理检查'
                   END AS AssitExaminationTypeIdValue
            FROM PatientVisitMapping pm
            CROSS APPLY (
                SELECT TOP 1 name AS RandomHospitalName FROM ab_hospital ORDER BY NEWID()
            ) h
        ),

        -- Step 7: 生成最终字段
        FinalData AS (
            SELECT *,
                   RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(patient_id * 10000 + n)) % 10000000), 7) AS report_num,
                   RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(patient_id * 10000 + n)) % 10000000), 7) AS source_report_num,
                   DATEADD(DAY, ABS(CHECKSUM(patient_id * 10000 + n)) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS check_time,
                   DATEADD(DAY, ABS(CHECKSUM(patient_id * 10000 + n)) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS report_time,
                   DATEADD(DAY, -ABS(CHECKSUM(patient_id * 10000 + n)) % 365, GETDATE()) AS update_time,
                   ABS(CHECKSUM(patient_id * 10000 + n)) % 2 + 1 AS delete_state,
                   CASE WHEN patient_visit_id IS NULL THEN '2' ELSE '1' END AS data_source_key,
                   REPLICATE(N'哈喽你好', 250) AS ThousandChars
            FROM RandomFields
        )

        -- Step 8: 一次性插入数据（使用 TABLOCKX 提高性能）
        INSERT INTO a_cdrd_patient_assit_examination_info (
            patient_assit_examination_type_key,
            patient_assit_examination_type_value,
            patient_id,
            patient_visit_id,
            patient_hospital_visit_id,
            patient_hospital_code,
            patient_hospital_name,
            patient_assit_examination_report_num,
            patient_assit_examination_source_report_num,
            patient_assit_examination_report_name,
            patient_assit_examination_check_method,
            patient_assit_examination_body_site,
            patient_assit_examination_sample_body,
            patient_assit_examination_eye_find,
            patient_assit_examination_microscope_find,
            patient_assit_examination_check_find,
            patient_assit_examination_check_conclusion,
            patient_assit_examination_check_time,
            patient_assit_examination_report_time,
            patient_assit_examination_delete_state_key,
            patient_assit_examination_update_time,
            patient_assit_examination_data_source_key
        )
        SELECT
            n AS patient_assit_examination_type_key,
            AssitExaminationTypeIdValue AS patient_assit_examination_type_value,
            patient_id,
            patient_visit_id,
            patient_hospital_visit_id,
            patient_hospital_code,
            RandomHospitalName AS patient_hospital_name,
            report_num AS patient_assit_examination_report_num,
            source_report_num AS patient_assit_examination_source_report_num,
            '报告名称' AS patient_assit_examination_report_name,
            '检查方法' AS patient_assit_examination_check_method,
            CASE WHEN AssitExaminationTypeIdValue = '病理检查' THEN '' ELSE '随机值123' END AS patient_assit_examination_body_site,
            CASE WHEN AssitExaminationTypeIdValue = '病理检查' THEN '随机值' ELSE '' END AS patient_assit_examination_sample_body,
            ThousandChars AS patient_assit_examination_eye_find,
            ThousandChars AS patient_assit_examination_microscope_find,
            ThousandChars AS patient_assit_examination_check_find,
            ThousandChars AS patient_assit_examination_check_conclusion,
            check_time AS patient_assit_examination_check_time,
            report_time AS patient_assit_examination_report_time,
            delete_state AS patient_assit_examination_delete_state_key,
            update_time AS patient_assit_examination_update_time,
            data_source_key AS patient_assit_examination_data_source_key
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
