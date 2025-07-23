-- todo  护理记录表(造数据)
-- 数据量：每条住院记录3条护理记录（共9万）

CREATE OR ALTER PROCEDURE cdrd_patient_nurse_info
    @RecordCount INT = 3,
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRANSACTION;

    -- 获取所有就诊建议记录
    SELECT
        patient_hospital_advice_id,
        patient_visit_id,
        patient_id,
        patient_hospital_visit_id,
        patient_hospital_code,
        patient_hospital_name
    INTO #TempAdvice
    FROM a_cdrd_patient_hospital_advice_info;

    -- 遍历每条记录并插入 3 条护理记录
    DECLARE @Counter INT = 1;
    DECLARE @MaxId INT = (SELECT MAX(patient_hospital_advice_id) FROM #TempAdvice);

    WHILE @Counter <= @MaxId
    BEGIN
        DECLARE
            @patient_visit_id INT,
            @patient_id INT,
            @patient_hospital_visit_id NVARCHAR(100),
            @patient_hospital_code NVARCHAR(100),
            @patient_hospital_name NVARCHAR(50);

        -- 获取当前记录
        SELECT
            @patient_visit_id = patient_visit_id,
            @patient_id = patient_id,
            @patient_hospital_visit_id = patient_hospital_visit_id,
            @patient_hospital_code = patient_hospital_code,
            @patient_hospital_name = patient_hospital_name
        FROM #TempAdvice
        WHERE patient_hospital_advice_id = @Counter;

        IF @@ROWCOUNT > 0
        --  如果前面的 SELECT 语句成功查到了至少一行数据（即当前 @Counter 对应的记录存在），才执行插入护理记录的操作。
        BEGIN
            DECLARE @i INT = 1;
            WHILE @i <= @RecordCount
            BEGIN
                INSERT INTO a_cdrd_patient_nurse_info (
                    patient_id,
                    patient_visit_id,
                    patient_hospital_visit_id,
                    patient_hospital_code,
                    patient_hospital_name,
                    patient_nurse_record_num,
                    patient_nurse_record_time,
                    patient_nurse_record_name,
                    patient_nurse_value,
                    patient_nurse_unit,
                    patient_nurse_update_time,
                    patient_nurse_source_key
                )
                VALUES (
                    @patient_id, -- 患者ID
                    @patient_visit_id, -- 就诊记录ID
                    @patient_hospital_visit_id, -- 就诊编号
                    @patient_hospital_code, -- 就诊医疗机构编号
                    @patient_hospital_name, -- 医院名称
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 记录编号
                    DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 记录时间
                    '记录名称', -- 记录名称
                    '记录结果', -- 记录结果
                    '记录结果单位', -- 记录结果单位
                    DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                    '1'  -- 数据来源1或2
                );

                SET @i = @i + 1;
            END
        END

        SET @Counter = @Counter + 1;
    END

    COMMIT TRANSACTION;

    -- 返回总记录数
    SET @result = (SELECT COUNT(*) FROM a_cdrd_patient_nurse_info);

    DROP TABLE #TempAdvice;
END
