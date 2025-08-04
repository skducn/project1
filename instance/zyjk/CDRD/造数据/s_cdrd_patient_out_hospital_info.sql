-- todo  出院记录表(造数据)
-- 数据量：每名患者2条（共6万）
-- 耗时: 4.0556 秒
CREATE OR ALTER PROCEDURE s_cdrd_patient_out_hospital_info
    @RecordCount INT = 2,
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- 获取就诊表中住院记录数量
    DECLARE @re INT = 1;
    select @re = count(*) from CDRD_PATIENT_INFO;
    SET @result = @re * @RecordCount;

    DECLARE @ThousandChars NVARCHAR(MAX) = REPLICATE(N'哈喽你好', 250);
    DECLARE @TwoHundredChars NVARCHAR(MAX) = REPLICATE(N'职能', 100);

    BEGIN TRY
        BEGIN TRANSACTION;

        -- 将出院类型加载到临时表并分配序号
        SELECT n_key, n_value, ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS idx
        INTO #TempDischargeTypes
        FROM ab_dischargeRecordType;

        -- 获取出院类型的总数量
        DECLARE @MaxType INT;
        SELECT @MaxType = COUNT(*) FROM #TempDischargeTypes;

        ;WITH VisitRecords AS (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY patient_visit_in_time DESC) AS seq
            FROM CDRD_PATIENT_VISIT_INFO
            WHERE patient_visit_type_key = 2
        ),

        PatientRecords AS (
            SELECT vr.*
            FROM VisitRecords vr
            WHERE vr.seq <= @RecordCount
        ),

        -- 使用 CHECKSUM 生成伪随机数，避免每次 NEWID()
        RandomFields AS (
            SELECT pr.*,
                   t.n_key AS patient_out_hospital_type_key,
                   t.n_value AS patient_out_hospital_type_value,
                   RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(pr.patient_id * 1000 + pr.seq)) % 10000000), 7) AS record_num,
                   DATEADD(DAY, -ABS(CHECKSUM(pr.patient_id * 1000 + pr.seq)) % 365, GETDATE()) AS record_time,
                   DATEADD(DAY, -ABS(CHECKSUM(pr.patient_id * 1000 + pr.seq)) % 365, GETDATE()) AS update_time
            FROM PatientRecords pr
            CROSS APPLY (
                SELECT TOP 1 *
                FROM #TempDischargeTypes
                WHERE idx = ABS(CHECKSUM(pr.patient_id, pr.seq)) % @MaxType + 1
            ) t
        )

        INSERT INTO CDRD_PATIENT_OUT_HOSPITAL_INFO WITH (TABLOCKX) (
            patient_out_hospital_type_key,
            patient_out_hospital_type_value,
            patient_id,
            patient_visit_id,
            patient_hospital_visit_id,
            patient_hospital_code,
            patient_hospital_name,
            patient_out_hospital_record_num,
            patient_out_hospital_main_describe,
            patient_out_hospital_in_situation,
            patient_out_hospital_in_diag,
            patient_out_hospital_diag_process,
            patient_out_hospital_diag,
            patient_out_hospital_situation,
            patient_out_hospital_advice,
            patient_out_hospital_record_time,
            patient_out_hospital_update_time,
            patient_out_hospital_source_key
        )
        SELECT
            rf.patient_out_hospital_type_key,
            rf.patient_out_hospital_type_value,
            rf.patient_id,
            rf.patient_visit_id,
            rf.patient_hospital_visit_id,
            rf.patient_hospital_code,
            rf.patient_hospital_name,
            rf.record_num,
            @TwoHundredChars,
            '入院情况',
            rf.patient_visit_diag,
            @ThousandChars,
            '出院诊断',
            @ThousandChars,
            @TwoHundredChars,
            rf.record_time,
            rf.update_time,
            '1'
        FROM RandomFields rf
        ORDER BY rf.patient_id;


        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
