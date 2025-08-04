-- todo  手术记录表(造数据)
-- 数据量：每名患者5条（共15万），其中两条只有patientid，三条均有patientid、patient_visit_id
-- # 5w，耗时: 0.6143 秒

CREATE OR ALTER PROCEDURE s_cdrd_patient_operation_info
    @RecordCount INT = 5,
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- 获取患者数量
    DECLARE @re INT = 1;
    SELECT @re = COUNT(*) FROM CDRD_PATIENT_INFO;
    SET @result = @re * @RecordCount;

    -- 生成固定长字符串
    DECLARE @TwoHundredChars NVARCHAR(MAX) = REPLICATE(N'你好', 100);

    BEGIN TRY
        BEGIN TRANSACTION;

        -- Step 1: 获取所有患者 ID
        ;WITH Patients AS (
            SELECT patient_id
            FROM CDRD_PATIENT_INFO
        ),

        -- Step 2: 生成每位患者 2 条无就诊记录
        NoVisitRecords AS (
            SELECT p.patient_id, n.n
            FROM Patients p
            CROSS JOIN (SELECT 1 AS n UNION ALL SELECT 2) n
        ),

        -- Step 3: 生成每位患者最多 3 条就诊记录
        VisitRecords AS (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY patient_visit_in_time DESC) AS seq
            FROM CDRD_PATIENT_VISIT_INFO
        ),
        PatientVisitRecords AS (
            SELECT vr.*
            FROM VisitRecords vr
            WHERE vr.seq <= 3
        ),

        -- Step 4: 为无就诊记录生成随机字段
        NoVisitRandomFields AS (
            SELECT nvr.patient_id,
                   NULL AS patient_visit_id,
                   NULL AS patient_hospital_visit_id,
                   NULL AS patient_hospital_code,
                   h.name AS RandomHospital,
                   '2' AS patient_operation_source_key
            FROM NoVisitRecords nvr
            CROSS APPLY (SELECT TOP 1 name FROM ab_hospital ORDER BY NEWID()) h
        ),

        -- Step 5: 为有就诊记录生成随机字段
        VisitRandomFields AS (
            SELECT pvr.patient_id,
                   pvr.patient_visit_id,
                   pvr.patient_hospital_visit_id,
                   pvr.patient_hospital_code,
                   h.name AS RandomHospital,
                   '1' AS patient_operation_source_key
            FROM PatientVisitRecords pvr
            CROSS APPLY (SELECT TOP 1 name FROM ab_hospital ORDER BY NEWID()) h
        ),

        -- Step 6: 合并所有记录
        AllRecords AS (
            SELECT
                v.patient_id,
                v.patient_visit_id,
                v.patient_hospital_visit_id,
                v.patient_hospital_code,
                v.RandomHospital AS patient_hospital_name,
                v.patient_operation_source_key
            FROM VisitRandomFields v
            UNION ALL
            SELECT
                n.patient_id,
                n.patient_visit_id,
                n.patient_hospital_visit_id,
                n.patient_hospital_code,
                n.RandomHospital AS patient_hospital_name,
                n.patient_operation_source_key
            FROM NoVisitRandomFields n
        ),

        -- Step 7: 生成所有字段
        FinalData AS (
            SELECT
                ar.patient_id,
                ar.patient_visit_id,
                ar.patient_hospital_visit_id,
                ar.patient_hospital_code,
                ar.patient_hospital_name,
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(ar.patient_id * 1000 + ar.patient_visit_id)) % 10000000), 7) AS OperationNum,
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(ar.patient_id * 1000 + ar.patient_visit_id)) % 10000000), 7) AS SourceOperationNum,
                DATEADD(DAY, ABS(CHECKSUM(ar.patient_id * 1000 + ar.patient_visit_id)) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS OperationBeginTime,
                DATEADD(DAY, ABS(CHECKSUM(ar.patient_id * 1000 + ar.patient_visit_id)) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS OperationEndTime,
                DATEADD(DAY, -ABS(CHECKSUM(ar.patient_id * 1000 + ar.patient_visit_id)) % 365, GETDATE()) AS UpdateTime,
                ABS(CHECKSUM(ar.patient_id * 1000 + ar.patient_visit_id)) % 2 + 1 AS DeleteState,

                -- 随机字段
                ol.n_key AS OperationLevelKey,
                ol.n_value AS OperationLevelValue,
                ot.n_key AS OperationTypeKey,
                ot.n_value AS OperationTypeValue,
                gh.n_key AS IncisionHealingGradeKey,
                gh.n_value AS IncisionHealingGradeValue
            FROM AllRecords ar
            CROSS APPLY (SELECT TOP 1 n_key, n_value FROM ab_operationLevel ORDER BY NEWID()) ol
            CROSS APPLY (SELECT TOP 1 n_key, n_value FROM ab_operationType ORDER BY NEWID()) ot
            CROSS APPLY (SELECT TOP 1 n_key, n_value FROM ab_operationIncisionHealingGrade ORDER BY NEWID()) gh
        )

        -- Step 8: 插入数据（使用 TABLOCKX 提高性能）
        INSERT INTO CDRD_PATIENT_OPERATION_INFO WITH (TABLOCKX) (
            patient_id,
            patient_visit_id,
            patient_hospital_visit_id,
            patient_hospital_code,
            patient_hospital_name,
            patient_operation_num,
            patient_operation_source_num,
            patient_operation_name,
            patient_operation_doc_name,
            patient_operation_assist_I,
            patient_operation_assit_II,
            patient_operation_before_diag,
            patient_operation_during_diag,
            patient_operation_after_diag,
            patient_operation_level_key,
            patient_operation_level_value,
            patient_operation_type_key,
            patient_operation_type_value,
            patient_operation_incision_healing_grade_key,
            patient_operation_incision_healing_grade_value,
            patient_operation_anesthesiologist,
            patient_operation_anesthesia_type,
            patient_operation_step_process,
            patient_operation_begin_time,
            patient_operation_end_time,
            patient_operation_delete_state_key,
            patient_operation_update_time,
            patient_operation_source_key
        )
        SELECT
            fd.patient_id,
            fd.patient_visit_id,
            fd.patient_hospital_visit_id,
            fd.patient_hospital_code,
            fd.patient_hospital_name,
            fd.OperationNum,
            fd.SourceOperationNum,
            '手术名称',
            '主刀/手术者',
            'I助',
            'II助',
            @TwoHundredChars,
            @TwoHundredChars,
            @TwoHundredChars,
            fd.OperationLevelKey,
            fd.OperationLevelValue,
            fd.OperationTypeKey,
            fd.OperationTypeValue,
            fd.IncisionHealingGradeKey,
            fd.IncisionHealingGradeValue,
            '麻醉者',
            '麻醉方式',
            '手术步骤及经过',
            fd.OperationBeginTime,
            fd.OperationEndTime,
            fd.DeleteState,
            fd.UpdateTime,
            '1'
        FROM FinalData fd
        ORDER BY fd.patient_id;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
