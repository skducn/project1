-- todo  死亡记录表(造数据)
-- 数据量：从3万名患者中随机500人有死亡记录，其中200均有patientid、patient_visit_id，剩余300只有patientid

CREATE OR ALTER PROCEDURE cdrd_patient_death_info
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    select @result = 5;  --修改为500


    DECLARE @ThousandChars NVARCHAR(MAX);
    SET @ThousandChars = REPLICATE(N'哈喽你好', 250); -- 每句4个字符，重复250次=1000字符

    DECLARE @TwoHundredChars NVARCHAR(MAX);
    SET @TwoHundredChars = REPLICATE(N'你好', 100); -- 每句4个字符，重复250次=1000字符

    -- 取3条，（500条）
    DECLARE @Counter1 INT = 1;
    WHILE @Counter1 <= @result
    BEGIN

        -- 获取 patient_id 和 patient_visit_id（按指定次数插入）
        DECLARE @patient_id INT;
        DECLARE @patient_visit_id INT;
        DECLARE @AssitExaminationTypeIdValue NVARCHAR(50);
        DECLARE @patient_hospital_visit_id NVARCHAR(100);
        DECLARE @patient_hospital_code NVARCHAR(100);
        DECLARE @patient_hospital_name NVARCHAR(50);
        DECLARE @patient_visit_in_time DATETIME;

        -- ab表
        -- 医院
        DECLARE @RandomHospital NVARCHAR(100)
        SELECT TOP 1 @RandomHospital=name FROM ab_hospital ORDER BY NEWID()


        -- 步骤1
        -- 先执行 300 次 （仅 patient_id）
        IF @Counter1 <= 3   -- 修改为300
        BEGIN

            -- 按照记录顺序获取
            SELECT @patient_id = patient_id
            FROM (
                SELECT
                    patient_id,
                    ROW_NUMBER() OVER (ORDER BY @patient_visit_id) AS row_num
                FROM a_cdrd_patient_info
            ) AS subquery
            WHERE row_num = @Counter1;

            SET @patient_visit_id = NULL;

            -- 插入单条随机数据
            INSERT INTO a_cdrd_patient_death_info (patient_id,patient_visit_id,patient_hospital_visit_id,patient_death_record_id,patient_death_time,patient_death_in_situation,patient_death_in_diag,patient_death_diag_process,patient_death_reason,patient_death_diag,patient_death_update_time,patient_death_source_key)
            VALUES (
                @patient_id, -- 患者ID
                @patient_visit_id, -- 就诊记录ID
                @patient_visit_id, -- 就诊编号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 文书编号
                DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 死亡时间
                @ThousandChars, -- 入院情况
                @TwoHundredChars, -- 入院诊断
                @ThousandChars, -- 诊疗经过（抢救经过）
                @TwoHundredChars, -- 死亡原因
                @TwoHundredChars, -- 死亡诊断
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                '2'  -- 数据来源1或2
            );

        END

        -- 步骤2
        -- 再执行 200 次（patient_id + patient_visit_id）
        IF @Counter1 >= 4  -- 修改为301
        BEGIN
            -- 按照记录顺序获取
            SELECT @patient_visit_id = patient_visit_id,
                   @patient_id = patient_id,
                   @patient_hospital_visit_id = patient_hospital_visit_id, -- 就诊编号
                   @patient_visit_in_time = patient_visit_in_time -- 就诊日期
            FROM (
                SELECT
                    patient_visit_id,patient_id, patient_hospital_visit_id,patient_visit_in_time,
                    ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY @patient_visit_id) AS row_num
                FROM a_cdrd_patient_visit_info
            ) AS subquery
            WHERE row_num = @Counter1 and patient_id = @patient_id; -- 使用 @i 控制每条记录的偏移


            -- 插入单条随机数据
            INSERT INTO a_cdrd_patient_death_info (patient_id,patient_visit_id,patient_hospital_visit_id,patient_death_record_id,patient_death_time,patient_death_in_situation,patient_death_in_diag,patient_death_diag_process,patient_death_reason,patient_death_diag,patient_death_update_time,patient_death_source_key)
            VALUES (
                @patient_id, -- 患者ID
                @patient_visit_id, -- 就诊记录ID
                @patient_hospital_visit_id, -- 就诊编号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 文书编号
                @patient_visit_in_time, -- 死亡时间
                @ThousandChars, -- 入院情况
                @TwoHundredChars, -- 入院诊断
                @ThousandChars, -- 诊疗经过（抢救经过）
                @TwoHundredChars, -- 死亡原因
                @TwoHundredChars, -- 死亡诊断
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                '1'  -- 数据来源1或2
            );
        END

        SET @Counter1 = @Counter1 + 1;
    END;

END