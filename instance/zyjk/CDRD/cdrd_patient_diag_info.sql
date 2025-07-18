-- todo 诊断表(造数据)
-- 数据量：每个患者5条 = 患者基本信息 * 5(2条患者基本信息，3条就诊记录表) , 共15万

CREATE OR ALTER PROCEDURE cdrd_patient_diag_info
    @RecordCount INT = 5,
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @re INT = 1;
    select @re = count(*) from a_cdrd_patient_info;
    SET @result = @re * @RecordCount;

    -- 遍历基本信息表
    DECLARE @Counter1 INT = 1;
    WHILE @Counter1 <= @re
    BEGIN

        -- 循环插入5条
        BEGIN

            -- 获取 patient_id 和 patient_visit_id（按指定次数插入）
            DECLARE @i INT = 1;
            DECLARE @patient_id INT;
            DECLARE @patient_visit_id INT;

            -- 子存储过程
            -- 医院
            DECLARE @RandomHospital NVARCHAR(350);
            EXEC p_hospital @v = @RandomHospital OUTPUT;

            -- 入院病情
            DECLARE @RandomInStateIdKey NVARCHAR(50), @RandomInStateIdValue NVARCHAR(50);
            EXEC p_in_state @k = @RandomInStateIdKey OUTPUT, @v = @RandomInStateIdValue OUTPUT;

            -- 出院情况
            DECLARE @RandomOutcomeStateIdKey NVARCHAR(50), @RandomOutcomeStateIdValue NVARCHAR(50);
            EXEC p_outcome_state @k = @RandomOutcomeStateIdKey OUTPUT, @v = @RandomOutcomeStateIdValue OUTPUT;

            -- 主要诊断
            DECLARE @RandomTrueFalseIdKey NVARCHAR(50), @RandomTrueFalseIdValue NVARCHAR(50);
            EXEC p_trueFalse @k = @RandomTrueFalseIdKey OUTPUT, @v = @RandomTrueFalseIdValue OUTPUT;

            -- 诊断类型，诊断名称，ICD10编码
            DECLARE @RandomDiagClass NVARCHAR(50), @RandomDiagName NVARCHAR(50), @RandomDiagCode NVARCHAR(50);
            EXEC r_diag_info__ @v1 = @RandomDiagClass OUTPUT, @v2 = @RandomDiagName OUTPUT, @v3 = @RandomDiagCode OUTPUT;


            -- 先执行 2 次 （仅 patient_id）
            WHILE @i <= 2
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
                INSERT INTO a_cdrd_patient_diag_info (patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_case_num,patient_diag_num,patient_diag_class,patient_diag_name,patient_diag_is_primary_key,patient_diag_is_primary_value,patient_diag_code,patient_in_state_key,patient_in_state_value,patient_outcome_state_key,patient_outcome_state_value,patient_diag_date,patient_diag_delete_state_key,patient_diag_update_time,patient_diag_data_source_key)
                VALUES (
                    @patient_id, -- 患者ID
                    @patient_visit_id, -- 就诊记录ID, 空
                    @patient_visit_id, -- 就诊编号, 空
                    @patient_visit_id, -- 诊断医疗机构编号, 空
                    @RandomHospital, -- 医院名称
                    @patient_visit_id, -- 病案号, 空
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 病人诊断序号
                    @RandomDiagClass, -- 诊断类型
                    @RandomDiagName, -- 诊断名称
                    @RandomTrueFalseIdKey, -- 主要诊断key
                    @RandomTrueFalseIdValue, -- 主要诊断
                    @RandomDiagCode, -- ICD10编码
                    @RandomInStateIdKey, -- 入院病情key
                    @RandomInStateIdValue, -- 入院病情
                    @RandomOutcomeStateIdKey, -- 出院病情key
                    @RandomOutcomeStateIdValue, -- 出院病情
                    DATEADD(DAY, ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01'), -- 诊断日期, 从2022年06月01日至今随机，精确到秒
                    ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                    DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                    '2'  -- 数据来源1或2, 没有就诊记录ID为“2”
                );

                SET @i = @i + 1;
            END

            -- 再执行 3 次（patient_id + patient_visit_id）
            WHILE @i <= 5
            BEGIN

                -- 从就诊记录中获取就诊编号，诊断医疗机构编号, 病案号
                DECLARE @patient_hospital_visit_id NVARCHAR(100);
                DECLARE @patient_hospital_code NVARCHAR(100);
                DECLARE @patient_case_num NVARCHAR(100);
                -- 按照记录顺序获取
                SELECT @patient_id = patient_id, @patient_visit_id = patient_visit_id,
                       @patient_hospital_visit_id = patient_hospital_visit_id, @patient_hospital_code = patient_hospital_code,
                       @patient_case_num = patient_case_num
                FROM (
                    SELECT
                        patient_visit_id, patient_id,patient_hospital_visit_id,patient_hospital_code,patient_case_num,
                        ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY patient_visit_id) AS row_num2
                    FROM a_cdrd_patient_visit_info
                ) AS subquery2
                WHERE row_num2 = @i AND patient_id = @patient_id; -- 使用 @i 控制每条记录的偏移


                -- 插入单条随机数据
                INSERT INTO a_cdrd_patient_diag_info (patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_case_num,patient_diag_num,patient_diag_class,patient_diag_name,patient_diag_is_primary_key,patient_diag_is_primary_value,patient_diag_code,patient_in_state_key,patient_in_state_value,patient_outcome_state_key,patient_outcome_state_value,patient_diag_date,patient_diag_delete_state_key,patient_diag_update_time,patient_diag_data_source_key)
                VALUES (
                    @patient_id, -- 患者ID
                    @patient_visit_id, -- 就诊记录ID
                    @patient_hospital_visit_id, -- 就诊编号
                    @patient_hospital_code, -- 诊断医疗机构编号
                    @RandomHospital, -- 医院名称
                    @patient_case_num, -- 病案号
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 病人诊断序号
                    @RandomDiagClass, -- 诊断类型
                    @RandomDiagName, -- 诊断名称
                    @RandomTrueFalseIdKey, -- 主要诊断key
                    @RandomTrueFalseIdValue, -- 主要诊断
                    @RandomDiagCode, -- ICD10编码
                    @RandomInStateIdKey, -- 入院病情key
                    @RandomInStateIdValue, -- 入院病情
                    @RandomOutcomeStateIdKey, -- 出院病情key
                    @RandomOutcomeStateIdValue, -- 出院病情
                    DATEADD(DAY, ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01'), -- 诊断日期, 从2022年06月01日至今随机，精确到秒
                    ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                    DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                    '1'  -- 数据来源1或2，有就诊记录ID为“1”
                );

                SET @i = @i + 1;
            END

        END

    SET @Counter1 = @Counter1 + 1;
    END;

END