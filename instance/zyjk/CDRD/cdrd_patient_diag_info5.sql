-- 创建或修改存储过程 cdrd_patient_diag_info5
-- 用于批量生成诊断信息模拟数据
CREATE OR ALTER PROCEDURE cdrd_patient_diag_info5
    @RecordCount INT = 5,          -- 每个患者生成的诊断记录数（默认5条）
    @result INT OUTPUT             -- 输出总生成记录数
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON; -- 出错时回滚整个事务

    BEGIN TRY
        -- 获取患者总数
        DECLARE @TotalPatients INT;
        SELECT @TotalPatients = COUNT(*) FROM a_cdrd_patient_info;

        -- 如果没有患者数据，直接退出
        IF @TotalPatients = 0
        BEGIN
            PRINT '警告：a_cdrd_patient_info 表中没有患者数据，无法生成诊断信息。';
            SET @result = 0;
            RETURN;
        END

        -- 设置总记录数
        SET @result = @TotalPatients * @RecordCount;

        -- 生成患者ID与行号映射
        ;WITH PatientCTE AS (
            SELECT patient_id, ROW_NUMBER() OVER (ORDER BY patient_id) AS RowNum
            FROM a_cdrd_patient_info
        ),
        -- 生成就诊记录映射（每个患者最多3条就诊记录）
        VisitCTE AS (
            SELECT
                patient_id,
                patient_visit_id,
                patient_hospital_visit_id,
                patient_hospital_code,
                patient_case_num,
                ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY patient_visit_id) AS VisitRow
            FROM a_cdrd_patient_visit_info
        )
        -- 插入诊断信息
        INSERT INTO a_cdrd_patient_diag_info (
            patient_id, patient_visit_id, patient_hospital_visit_id, patient_hospital_code, patient_hospital_name,
            patient_case_num, patient_diag_num, patient_diag_class, patient_diag_name, patient_diag_is_primary_key,
            patient_diag_is_primary_value, patient_diag_code, patient_in_state_key, patient_in_state_value,
            patient_outcome_state_key, patient_outcome_state_value, patient_diag_date,
            patient_diag_delete_state_key, patient_diag_update_time, patient_diag_data_source_key
        )
        SELECT
            p.patient_id,
            CASE WHEN seq <= 2 THEN NULL ELSE v.patient_visit_id END AS patient_visit_id,
            CASE WHEN seq <= 2 THEN NULL ELSE v.patient_hospital_visit_id END AS patient_hospital_visit_id,
            CASE WHEN seq <= 2 THEN NULL ELSE v.patient_hospital_code END AS patient_hospital_code,
            h.hospital_name,
            CASE WHEN seq <= 2 THEN NULL ELSE v.patient_case_num END AS patient_case_num,
            RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7) AS patient_diag_num,
            d.diag_class,
            d.diag_name,
            t.key_value AS patient_diag_is_primary_key,
            t.display_value AS patient_diag_is_primary_value,
            d.diag_code,
            i.state_key AS patient_in_state_key,
            i.state_value AS patient_in_state_value,
            o.state_key AS patient_outcome_state_key,
            o.state_value AS patient_outcome_state_value,
            DATEADD(DAY, ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS patient_diag_date,
            ABS(CHECKSUM(NEWID())) % 2 + 1 AS patient_diag_delete_state_key,
            DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()) AS patient_diag_update_time,
            CASE WHEN seq <= 2 THEN '2' ELSE '1' END AS patient_diag_data_source_key
        FROM PatientCTE p
        CROSS JOIN (VALUES (1),(2),(3),(4),(5)) AS Seq(seq)
        CROSS APPLY (
            SELECT TOP 1 hospital_name FROM a_hospital ORDER BY NEWID()
        ) h
        CROSS APPLY (
            SELECT TOP 1 diag_class, diag_name, diag_code FROM a_diag_info ORDER BY NEWID()
        ) d
        CROSS APPLY (
            SELECT TOP 1 key_value, display_value FROM a_true_false_info ORDER BY NEWID()
        ) t
        CROSS APPLY (
            SELECT TOP 1 state_key, state_value FROM a_in_state_info ORDER BY NEWID()
        ) i
        CROSS APPLY (
            SELECT TOP 1 state_key, state_value FROM a_outcome_state_info ORDER BY NEWID()
        ) o
        LEFT JOIN VisitCTE v ON p.patient_id = v.patient_id AND v.VisitRow = seq - 2
        WHERE seq <= 2 OR v.patient_visit_id IS NOT NULL;

        PRINT '成功插入 ' + CAST(@result AS NVARCHAR(10)) + ' 条诊断信息记录。';

    END TRY
    BEGIN CATCH
        PRINT '发生错误：' + ERROR_MESSAGE();
        THROW;
    END CATCH;
END;
