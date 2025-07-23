-- 检查项目明细表(造数据)优化版
-- 数据量：每个实验室检查记录对应一组检查项目明细（每组20条，总量100条）
-- 原耗时: 不适用（当前逻辑错误） → 优化后预计耗时: 0.5~1 秒

CREATE OR ALTER PROCEDURE cdrd_patient_test_project_info
    @RecordCount INT = 20, -- 每个实验室检查记录生成20条检查项目明细
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- 获取实验室检查报告记录数，用于输出计算
    DECLARE @re INT = 1;
    select @re = count(*) from a_cdrd_patient_lab_examination_info;
    SET @result = @re * @RecordCount;

    BEGIN TRY
        BEGIN TRANSACTION;

        -- Step 1: 获取所有实验室检查记录（来自 a_cdrd_patient_lab_examination_info）
        ;WITH LabExaminations AS (
            SELECT
                patient_lab_examination_id AS patient_superior_examination_id,
                patient_lab_examination_report_num AS patient_report_num,
                patient_visit_id
            FROM a_cdrd_patient_lab_examination_info
        ),

        -- Step 2: 获取 ab_lab_project 中的报告名称列表（2组报告）
        ReportNames AS (
            SELECT DISTINCT report_name
            FROM ab_lab_project
        ),

        -- Step 3: 为每条实验室检查记录随机分配一组 report_name
        LabExaminationsWithReport AS (
            SELECT
                le.patient_superior_examination_id,
                le.patient_report_num,
                le.patient_visit_id,
                rn.report_name,
                CHECKSUM(le.patient_superior_examination_id, rn.report_name) % 100 AS sort_key
            FROM LabExaminations le
            CROSS JOIN ReportNames rn
        ),

        -- Step 4: 为每条实验室检查记录只保留一组 report_name（随机选一组）
        LabExaminationsWithOneReport AS (
            SELECT *
            FROM (
                SELECT *,
                       ROW_NUMBER() OVER (PARTITION BY patient_superior_examination_id ORDER BY sort_key) AS seq
                FROM LabExaminationsWithReport
            ) t
            WHERE seq = 1
        ),

        -- Step 5: 获取 ab_lab_project 中的检查项目明细（精确每组20条）
        TestProjects AS (
            SELECT
                report_name,
                patient_test_item_name,
                patient_test_numerical_value,
                patient_test_unit_name,
                patient_test_text_value,
                patient_test_abnormal_flag,
                patient_test_reference_range,
                ROW_NUMBER() OVER (PARTITION BY report_name ORDER BY (SELECT NULL)) AS seq
            FROM ab_lab_project
        ),

        -- Step 6: 关联实验室检查记录与对应的检查项目明细（1:20）
        Combined AS (
            SELECT
                le.patient_superior_examination_id,
                '1' AS patient_superior_examination_type, -- 实验室检查
                le.patient_report_num,
                tp.patient_test_item_name,
                tp.patient_test_numerical_value,
                tp.patient_test_unit_name,
                tp.patient_test_text_value,
                tp.patient_test_abnormal_flag,
                tp.patient_test_reference_range,
                ABS(CHECKSUM(le.patient_superior_examination_id, tp.patient_test_item_name)) % 2 + 1 AS delete_state,
                DATEADD(DAY, -ABS(CHECKSUM(le.patient_superior_examination_id, tp.patient_test_item_name)) % 365, GETDATE()) AS update_time,
                CASE WHEN le.patient_visit_id IS NULL THEN '2' ELSE '1' END AS data_source_key
            FROM LabExaminationsWithOneReport le
            INNER JOIN TestProjects tp
                ON le.report_name = tp.report_name
            WHERE tp.seq <= @RecordCount -- 精确控制每组20条
        )

        -- Step 7: 一次性插入数据（使用 TABLOCKX 提高性能）
        INSERT INTO a_cdrd_patient_test_project_info WITH (TABLOCKX) (
            patient_superior_examination_id,
            patient_superior_examination_type,
            patient_report_num,
            patient_test_item_name,
            patient_test_numerical_value,
            patient_test_unit_name,
            patient_test_text_value,
            patient_test_abnormal_flag,
            patient_test_reference_range,
            patient_test_delete_state_key,
            patient_test_update_time,
            patient_test_data_source_key
        )
        SELECT
            patient_superior_examination_id,
            patient_superior_examination_type,
            patient_report_num,
            patient_test_item_name,
            patient_test_numerical_value,
            patient_test_unit_name,
            patient_test_text_value,
            patient_test_abnormal_flag,
            patient_test_reference_range,
            delete_state,
            update_time,
            data_source_key
        FROM Combined
        ORDER BY patient_superior_examination_id;

        -- Step 8: 设置输出参数
--         SELECT @result = COUNT(*) FROM Combined;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
