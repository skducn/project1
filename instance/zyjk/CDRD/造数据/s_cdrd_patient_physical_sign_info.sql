-- 体征信息表(造数据)优化版
-- 数据量：每名患者5条（共15万）
-- 优化目标：提升性能，避免嵌套循环
-- 耗时: 0.3652 秒

CREATE OR ALTER PROCEDURE s_cdrd_patient_physical_sign_info
    @RecordCount INT = 5, -- 每位患者生成5条体征记录
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
            SELECT
                   pm.patient_id,
                   pm.n,
                   pm.patient_visit_id,
                   pm.patient_hospital_visit_id,
                   pm.patient_hospital_code,
                   pm.patient_hospital_name,
                   pm.patient_visit_in_time,

                   h.RandomHospitalName,
                   ps.type_key AS sign_type_key,
                   ps.type_value AS sign_type_value,
                   pu.unit_key AS sign_unit_key,
                   pu.unit_value AS sign_unit_value
            FROM PatientVisitMapping pm
            CROSS APPLY (
                SELECT TOP 1 name AS RandomHospitalName FROM ab_hospital ORDER BY NEWID()
            ) h
            CROSS APPLY (
                SELECT TOP 1 n_key AS type_key, n_value AS type_value FROM ab_physicalSign ORDER BY NEWID()
            ) ps
            CROSS APPLY (
                SELECT TOP 1 n_key AS unit_key, n_value AS unit_value FROM ab_physicalSignUnit ORDER BY NEWID()
            ) pu
        ),

        -- Step 7: 生成最终字段
        FinalData AS (
            SELECT *,
                   RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(patient_id * 10000 + n)) % 10000000), 7) AS sign_value,
                   DATEADD(DAY, ABS(CHECKSUM(patient_id * 10000 + n)) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS sign_time,
                   ABS(CHECKSUM(patient_id * 10000 + n)) % 2 + 1 AS delete_state,
                   DATEADD(DAY, -ABS(CHECKSUM(patient_id * 10000 + n)) % 365, GETDATE()) AS update_time,
                   CASE WHEN patient_visit_id IS NULL THEN '2' ELSE '1' END AS data_source_key
            FROM RandomFields
        ),

        -- Step 8: 去重并确保每位患者生成5条记录
        Deduplicated AS (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY n) AS seq
            FROM FinalData
        )

        -- Step 9: 一次性插入数据（使用 TABLOCKX 提高性能）
        INSERT INTO CDRD_PATIENT_PHYSICAL_SIGN_INFO WITH (TABLOCKX) (
            patient_id,
            patient_visit_id,
            patient_hospital_visit_id,
            patient_hospital_code,
            patient_hospital_name,
            patient_physical_sign_type_key,
            patient_physical_sign_type_value,
            patient_physical_sign_other,
            patient_physical_sign_value,
            patient_physical_sign_unit_key,
            patient_physical_sign_unit_value,
            patient_physical_sign_other_unit,
            patient_physical_sign_time,
            patient_physical_sign_delete_state_key,
            patient_physical_sign_update_time,
            patient_physical_sign_data_source_key
        )
        SELECT
            patient_id,
            patient_visit_id,
            patient_hospital_visit_id,
            patient_hospital_code,
            RandomHospitalName AS patient_hospital_name,
            sign_type_key AS patient_physical_sign_type_key,
            sign_type_value AS patient_physical_sign_type_value,
            '其他体征' AS patient_physical_sign_other,
            sign_value AS patient_physical_sign_value,
            sign_unit_key AS patient_physical_sign_unit_key,
            sign_unit_value AS patient_physical_sign_unit_value,
            '其他体征单位' AS patient_physical_sign_other_unit,
            sign_time AS patient_physical_sign_time,
            delete_state AS patient_physical_sign_delete_state_key,
            update_time AS patient_physical_sign_update_time,
            data_source_key AS patient_physical_sign_data_source_key
        FROM Deduplicated
        WHERE seq <= @RecordCount
        ORDER BY patient_id, n;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
