-- todo  出院记录表(造数据)
-- 数据量：每名患者2条（共6万）

CREATE OR ALTER PROCEDURE cdrd_patient_out_hospital_info
    @RecordCount INT = 2,
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- 获取就诊表中住院记录数量
    DECLARE @re INT = 1;
    select @re = count(*) from a_cdrd_patient_info;
    SET @result = @re * @RecordCount;
--     select @result = count(*) from a_cdrd_patient_visit_info where patient_visit_type_key=2;

    DECLARE @ThousandChars NVARCHAR(MAX);
    SET @ThousandChars = REPLICATE(N'哈喽你好', 250); -- 每句4个字符，重复250次=1000字符

	DECLARE @TwoHundredChars NVARCHAR(MAX);
    SET @TwoHundredChars = REPLICATE(N'职能', 100);

    BEGIN
        BEGIN TRANSACTION;
        DECLARE @patient_visit_id INT = 0;
        DECLARE @patient_id INT = 0;
        DECLARE @patient_hospital_visit_id NVARCHAR(100);
        DECLARE @patient_hospital_code NVARCHAR(100);
        DECLARE @patient_hospital_name NVARCHAR(50);
        DECLARE @patient_visit_in_time DATETIME;
        DECLARE @patient_visit_in_dept_name NVARCHAR(50);
        DECLARE @patient_visit_diag NVARCHAR(1000);
        DECLARE @Counter1 INT = 1;


        -- 遍历就诊表
        WHILE @Counter1 <= @result
        BEGIN

            -- 子存储过程
            -- 出院记录类型
            DECLARE @RandomHospitalTypeIdKey NVARCHAR(50), @RandomHospitalTypeIdValue NVARCHAR(50);
            EXEC p_out_hospital_type @k = @RandomHospitalTypeIdKey OUTPUT, @v = @RandomHospitalTypeIdValue OUTPUT;


            -- 按照记录顺序获取
            SELECT @patient_visit_id = patient_visit_id,
                   @patient_id = patient_id,
                   @patient_hospital_visit_id = patient_hospital_visit_id,
                   @patient_hospital_code = patient_hospital_code,
                   @patient_hospital_name = patient_hospital_name,
                   @patient_visit_in_time = patient_visit_in_time,
                   @patient_visit_in_dept_name = patient_visit_in_dept_name,
                   @patient_visit_diag = patient_visit_diag
            FROM (
                SELECT
                    patient_visit_id,patient_id, patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,
                    patient_visit_in_time, patient_visit_in_dept_name,patient_visit_diag,
                    ROW_NUMBER() OVER (ORDER BY @patient_visit_id) AS row_num
                FROM a_cdrd_patient_visit_info where patient_visit_type_key=2
            ) AS subquery
            WHERE row_num = @Counter1;


            -- 插入单条随机数据
            INSERT INTO a_cdrd_patient_out_hospital_info (patient_out_hospital_type_key,patient_out_hospital_type_value,patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_out_hospital_record_num,patient_out_hospital_main_describe,patient_out_hospital_in_situation,patient_out_hospital_in_diag,patient_out_hospital_diag_process,patient_out_hospital_diag,patient_out_hospital_situation,patient_out_hospital_advice,patient_out_hospital_record_time,patient_out_hospital_update_time,patient_out_hospital_source_key)
            VALUES (
                @RandomHospitalTypeIdKey, -- 出院记录类型-key
                @RandomHospitalTypeIdValue, -- 出院记录类型
                @patient_id, -- 患者ID
                @patient_visit_id, -- 就诊记录ID
                @patient_hospital_visit_id, -- 就诊编号
                @patient_hospital_code, -- 就诊医疗机构编号
                @patient_hospital_name, -- 医院名称
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 文书编号
                @TwoHundredChars, -- 主诉
                '入院情况', -- 入院情况
                @patient_visit_diag, -- 入院诊断
                @ThousandChars, -- 诊疗经过
                '出院诊断', -- 出院诊断
                @ThousandChars, -- 出院情况
                @TwoHundredChars, -- 出院医嘱
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 记录时间
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                '1'  -- 数据来源1或2
            );

            SET @Counter1 = @Counter1 + 1;
        END;

        COMMIT TRANSACTION;
    END

END