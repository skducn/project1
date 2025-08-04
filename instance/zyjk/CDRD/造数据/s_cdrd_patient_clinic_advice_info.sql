-- 门诊医嘱表(造数据)优化版
-- 数据量：每名患者3条（共9万）
-- 优化目标：提升性能，避免嵌套循环
-- 3w，耗时: 0.2542 秒

CREATE OR ALTER PROCEDURE s_cdrd_patient_clinic_advice_info
    @RecordCount INT = 3, -- 每位患者生成3条医嘱记录
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- 获取就诊表中门诊记录数量
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
                   v.patient_visit_in_time, v.patient_visit_in_dept_name
            FROM PatientSequences ps
            LEFT JOIN VisitRecords v
                ON ps.patient_id = v.patient_id
                AND ps.n = v.seq
        ),

        -- Step 6: 一次性生成随机字段（避免逐条生成）
        RandomFields AS (
            SELECT *,
                   tf.n_key AS drug_flag_key, tf.n_value AS drug_flag_value
            FROM PatientVisitMapping pm
            CROSS APPLY (
                SELECT TOP 1 n_key, n_value FROM ab_boolean ORDER BY NEWID()
            ) tf
        ),

        -- Step 7: 生成处方编号、时间等字段
        FinalData AS (
            SELECT *,
                   RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(patient_id * 10000 + n)) % 10000000), 7) AS recipe_detail_num,
                   DATEADD(DAY, -ABS(CHECKSUM(patient_id * 10000 + n)) % 365, GETDATE()) AS update_time
            FROM RandomFields
        )

        -- Step 8: 插入数据
        INSERT INTO CDRD_PATIENT_CLINIC_ADVICE_INFO (
            patient_id,
            patient_visit_id,
            patient_hospital_visit_id,
            patient_hospital_code,
            patient_hospital_name,
            patient_outpat_recipe_detail_num,
            patient_recipe_class,
            patient_recipe_name,
            patient_recipe_drug_flag_key,
            patient_recipe_drug_flag_value,
            patient_recipe_time,
            patient_recipe_exec_dept_name,
            patient_clinic_advice_update_time,
            patient_clinic_advice_source_key
        )
        SELECT
            patient_id,
            patient_visit_id,
            patient_hospital_visit_id,
            patient_hospital_code,
            patient_hospital_name,
            recipe_detail_num AS patient_outpat_recipe_detail_num,
            '处方类别' AS patient_recipe_class,
            '处方名称' AS patient_recipe_name,
            drug_flag_key AS patient_recipe_drug_flag_key,
            drug_flag_value AS patient_recipe_drug_flag_value,
            patient_visit_in_time AS patient_recipe_time,
            patient_visit_in_dept_name AS patient_recipe_exec_dept_name,
            update_time AS patient_clinic_advice_update_time,
            '1' AS patient_clinic_advice_source_key
        FROM FinalData
        ORDER BY patient_id, n;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
