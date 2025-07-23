-- todo  住院医嘱表(造数据)
-- 数据量：每名患者2条（共6万）
-- 2w, 耗时: 841.8728 秒, 54,861,824字节
CREATE OR ALTER PROCEDURE cdrd_patient_hospital_advice_info2
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

    BEGIN
        BEGIN TRANSACTION;
        DECLARE @patient_visit_id INT = 0;
        DECLARE @patient_id INT = 0;
        DECLARE @patient_hospital_visit_id NVARCHAR(100);
        DECLARE @patient_hospital_code NVARCHAR(100);
        DECLARE @patient_hospital_name NVARCHAR(50);
        DECLARE @patient_visit_in_time DATETIME;
        DECLARE @patient_visit_in_dept_name NVARCHAR(50);
        DECLARE @Counter1 INT = 1;


--         -- 子存储过程
--         -- 随机是否药品 true false
--         DECLARE @RandomTrueFalseIdKey NVARCHAR(100)
--         DECLARE @RandomTrueFalseIdValue NVARCHAR(100)
--         SELECT TOP 1 @RandomTrueFalseIdKey=n_key, @RandomTrueFalseIdValue=n_value FROM ab_boolean ORDER BY NEWID()
-- --         DECLARE @RandomTrueFalseIdKey NVARCHAR(50), @RandomTrueFalseIdValue NVARCHAR(50);
-- --         EXEC p_trueFalse @k = @RandomTrueFalseIdKey OUTPUT, @v = @RandomTrueFalseIdValue OUTPUT;


        -- 遍历就诊表
        WHILE @Counter1 <= @result
        BEGIN

            -- 按照记录顺序获取
            SELECT @patient_visit_id = patient_visit_id,
                   @patient_id = patient_id,
                   @patient_hospital_visit_id = patient_hospital_visit_id,
                   @patient_hospital_code = patient_hospital_code,
                   @patient_hospital_name = patient_hospital_name,
                   @patient_visit_in_time = patient_visit_in_time,
                   @patient_visit_in_dept_name = patient_visit_in_dept_name
            FROM (
                SELECT
                    patient_visit_id,patient_id, patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,
                    patient_visit_in_time, patient_visit_in_dept_name,
                    ROW_NUMBER() OVER (ORDER BY @patient_visit_id) AS row_num
                FROM a_cdrd_patient_visit_info where patient_visit_type_key=2
            ) AS subquery
            WHERE row_num = @Counter1;


            -- 插入单条随机数据
            INSERT INTO a_cdrd_patient_hospital_advice_info (patient_hospital_advice_type_key,patient_hospital_advice_type_value,patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_hospital_advice_num,patient_hospital_advice_source_num,patient_hospital_advice_class,patient_hospital_advice_name,patient_hospital_advice_remark,patient_hospital_advice_begin_time,patient_hospital_advice_end_time,patient_hospital_advice_exec_dept_name,patient_hospital_advice_update_time,patient_hospital_advice_source_key)
            VALUES (
                '1', -- 住院医嘱类型-key
                '住院药物医嘱', -- 住院医嘱类型
                @patient_id, -- 患者ID
                @patient_visit_id, -- 就诊记录ID
                @patient_hospital_visit_id, -- 就诊编号
                @patient_hospital_code, -- 就诊医疗机构编号
                @patient_hospital_name, -- 医院名称
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 医嘱编号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 源系统医嘱编号
                '医嘱类别', -- 医嘱类别
                '医嘱名称', -- 医嘱名称
                @ThousandChars, -- 备注
                @patient_visit_in_time, -- 医嘱开始时间, 同就诊日期
                @patient_visit_in_time, -- 医嘱结束时间, 同就诊日期
                @patient_visit_in_dept_name,  -- 执行科室, 同就诊科室
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                '1'  -- 数据来源1或2
            );

            SET @Counter1 = @Counter1 + 1;
        END;

        COMMIT TRANSACTION;
    END

END