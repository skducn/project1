CREATE OR ALTER PROCEDURE s_cdrd_patient_death_info
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- 设置输出参数
    SET @result = 500;

    -- 固定长字符串
    DECLARE @ThousandChars NVARCHAR(MAX) = REPLICATE(N'哈喽你好', 250);
    DECLARE @TwoHundredChars NVARCHAR(MAX) = REPLICATE(N'你好', 100);

    BEGIN TRY
        BEGIN TRANSACTION;

        -- Step 1: 随机生成 300 条无就诊记录的死亡数据
        ;WITH NoVisitRecords AS (
            SELECT TOP 300   --修改1
                p.patient_id,
                NULL AS patient_visit_id,
                NULL AS patient_hospital_visit_id,
                '2' AS patient_death_source_key
            FROM CDRD_PATIENT_INFO p
            ORDER BY NEWID()
        ),

        -- Step 2: 随机生成 200 条有就诊记录的死亡数据
        VisitRecords AS (
            SELECT TOP 200  -- 修改2
                v.patient_id,
                v.patient_visit_id,
                v.patient_hospital_visit_id,
                '1' AS patient_death_source_key
            FROM CDRD_PATIENT_VISIT_INFO v
            ORDER BY NEWID()
        ),

        -- Step 3: 合并两组数据
        AllRecords AS (
            SELECT * FROM NoVisitRecords
            UNION ALL
            SELECT * FROM VisitRecords
        ),

        -- Step 4: 生成所有字段
        FinalData AS (
            SELECT
                ar.patient_id,
                ar.patient_visit_id,
                ar.patient_hospital_visit_id,
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(ar.patient_id * 1000)) % 10000000), 7) AS patient_death_record_id,
--                 RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(ar.patient_id * 1000 + ar.patient_visit_id)) % 10000000), 7) AS patient_death_record_id,
                DATEADD(DAY, ABS(CHECKSUM(ar.patient_id * 1000 + ar.patient_visit_id)) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS patient_death_time,
                @ThousandChars AS patient_death_in_situation,
                @TwoHundredChars AS patient_death_in_diag,
                @ThousandChars AS patient_death_diag_process,
                @TwoHundredChars AS patient_death_reason,
                @TwoHundredChars AS patient_death_diag,
                DATEADD(DAY, -ABS(CHECKSUM(ar.patient_id * 1000 + ar.patient_visit_id)) % 365, GETDATE()) AS patient_death_update_time,
                ar.patient_death_source_key
            FROM AllRecords ar
        )

        -- Step 5: 一次性插入数据（使用 TABLOCKX 提高性能）
        INSERT INTO CDRD_PATIENT_DEATH_INFO WITH (TABLOCKX) (
            patient_id,
            patient_visit_id,
            patient_hospital_visit_id,
            patient_death_record_id,
            patient_death_time,
            patient_death_in_situation,
            patient_death_in_diag,
            patient_death_diag_process,
            patient_death_reason,
            patient_death_diag,
            patient_death_update_time,
            patient_death_source_key
        )
        SELECT
            fd.patient_id,
            fd.patient_visit_id,
            fd.patient_hospital_visit_id,
            fd.patient_death_record_id,
            fd.patient_death_time,
            fd.patient_death_in_situation,
            fd.patient_death_in_diag,
            fd.patient_death_diag_process,
            fd.patient_death_reason,
            fd.patient_death_diag,
            fd.patient_death_update_time,
            fd.patient_death_source_key
        FROM FinalData fd;

        SET @result = @@ROWCOUNT;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
