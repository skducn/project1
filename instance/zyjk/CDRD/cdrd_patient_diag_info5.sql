CREATE OR ALTER PROCEDURE cdrd_patient_diag_info
    @RecordCount INT = 1, -- 控制每组生成多少“批次”的5条记录，默认每个患者生成1组
    @result INT OUTPUT
AS
BEGIN

    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRANSACTION;

    select @result = count(*) from a_cdrd_patient_info;

    -- 获取总患者数
    DECLARE @totalRecords INT = (SELECT COUNT(*) FROM a_cdrd_patient_info);
    DECLARE @Counter1 INT = 1;

    -- 创建临时表用于批量插入
    CREATE TABLE #TempDiag (
        patient_id INT,
        patient_visit_id INT NULL,
        patient_hospital_visit_id NVARCHAR(7),
        patient_hospital_code NVARCHAR(7),
        patient_hospital_name NVARCHAR(350),
        patient_case_num NVARCHAR(7),
        patient_diag_num NVARCHAR(7),
        patient_diag_class NVARCHAR(50),
        patient_diag_name NVARCHAR(50),
        patient_diag_is_primary_key NVARCHAR(50),
        patient_diag_is_primary_value NVARCHAR(50),
        patient_diag_code NVARCHAR(50),
        patient_in_state_key NVARCHAR(50),
        patient_in_state_value NVARCHAR(50),
        patient_outcome_state_key NVARCHAR(50),
        patient_outcome_state_value NVARCHAR(50),
        patient_diag_date DATE,
        patient_diag_delete_state_key INT,
        patient_diag_update_time DATETIME,
        patient_diag_data_source_key NVARCHAR(10)
    );

    WHILE @Counter1 <= @totalRecords
    BEGIN
        DECLARE @i INT = 1;
        DECLARE @TotalToInsert INT = @RecordCount * 5;

        WHILE @i <= @TotalToInsert
        BEGIN
            DECLARE
                @patient_id INT,
                @patient_visit_id INT,
                @RandomHospital NVARCHAR(350),
                @RandomInStateIdKey NVARCHAR(50), @RandomInStateIdValue NVARCHAR(50),
                @RandomOutcomeStateIdKey NVARCHAR(50), @RandomOutcomeStateIdValue NVARCHAR(50),
                @RandomTrueFalseIdKey NVARCHAR(50), @RandomTrueFalseIdValue NVARCHAR(50),
                @RandomDiagClass NVARCHAR(50), @RandomDiagName NVARCHAR(50), @RandomDiagCode NVARCHAR(50);

            -- 获取 patient_id
            SELECT TOP 1 @patient_id = patient_id FROM a_cdrd_patient_info ORDER BY NEWID();

            -- 如果当前为第1~2条，则不带 patient_visit_id
            IF @i % 5 + 1 <= 2
            BEGIN
                SET @patient_visit_id = NULL;
            END
            ELSE
            BEGIN
                -- 否则从就诊表中获取一个 patient_visit_id
                SELECT TOP 1 @patient_visit_id = patient_visit_id
                FROM a_cdrd_patient_visit_info
                WHERE patient_id = @patient_id AND patient_visit_id IS NOT NULL
                ORDER BY NEWID();
            END

            -- 调用子存储过程获取随机值
            EXEC p_hospital @v = @RandomHospital OUTPUT;
            EXEC p_in_state @k = @RandomInStateIdKey OUTPUT, @v = @RandomInStateIdValue OUTPUT;
            EXEC p_outcome_state @k = @RandomOutcomeStateIdKey OUTPUT, @v = @RandomOutcomeStateIdValue OUTPUT;
            EXEC p_trueFalse @k = @RandomTrueFalseIdKey OUTPUT, @v = @RandomTrueFalseIdValue OUTPUT;
            EXEC r_diag_info__ @v1 = @RandomDiagClass OUTPUT, @v2 = @RandomDiagName OUTPUT, @v3 = @RandomDiagCode OUTPUT;

            INSERT INTO #TempDiag
            VALUES (
                @patient_id,
                @patient_visit_id,
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7),
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7),
                @RandomHospital,
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7),
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7),
                @RandomDiagClass,
                @RandomDiagName,
                @RandomTrueFalseIdKey,
                @RandomTrueFalseIdValue,
                @RandomDiagCode,
                @RandomInStateIdKey,
                @RandomInStateIdValue,
                @RandomOutcomeStateIdKey,
                @RandomOutcomeStateIdValue,
                DATEADD(DAY, ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01'),
                ABS(CHECKSUM(NEWID())) % 2 + 1,
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()),
                CASE WHEN @i % 5 + 1 <= 2 THEN '2' ELSE '1' END
            );

            SET @i = @i + 1;
        END

        -- 插入主表
        INSERT INTO a_cdrd_patient_diag_info
        SELECT * FROM #TempDiag;

        TRUNCATE TABLE #TempDiag;

        SET @Counter1 = @Counter1 + 1;
    END

    COMMIT TRANSACTION;
END
