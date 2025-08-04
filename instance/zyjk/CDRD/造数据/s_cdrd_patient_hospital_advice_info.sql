-- 住院医嘱表(造数据)优化版
-- 数据量：每名患者2条（共6万）
-- 优化目标：提高执行效率，减少锁竞争和事务日志压力
-- 1w, 耗时: 0.7865 秒

CREATE OR ALTER PROCEDURE s_cdrd_patient_hospital_advice_info
    @RecordCount INT = 2,  -- 每名患者2条
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- 随机生成1000个汉字
    DECLARE @ThousandChars NVARCHAR(MAX);
    SET @ThousandChars = REPLICATE(N'哈喽你好', 250); -- 每句4个字符，重复250次=1000字符

    -- 计算目标记录数：患者数量 × 每位患者生成的医嘱数量
    SELECT @result = COUNT(*) * @RecordCount
    FROM CDRD_PATIENT_INFO;

    IF @result <= 0
    BEGIN
        PRINT 'No eligible patient records found.';
        RETURN;
    END;

    -- 构造每位患者生成 @RecordCount 条记录的数据集
    ;WITH NumberedPatients AS (
        SELECT
            p.patient_id,
            p.patient_visit_id,
            p.patient_hospital_visit_id,
            p.patient_hospital_code,
            p.patient_hospital_name,
            p.patient_visit_in_time,
            p.patient_visit_in_dept_name,
            ROW_NUMBER() OVER (ORDER BY p.patient_id) AS seq
        FROM CDRD_PATIENT_VISIT_INFO p
        WHERE p.patient_visit_type_key = 2
    ),
    PatientRecords AS (
        SELECT
            pp.*,
            n.n AS record_seq
        FROM NumberedPatients pp
        CROSS JOIN (
            SELECT TOP (1) ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n
            FROM sys.all_columns
        ) n
    )
    -- 插入数据
    INSERT INTO CDRD_PATIENT_HOSPITAL_ADVICE_INFO (
        patient_hospital_advice_type_key,
        patient_hospital_advice_type_value,
        patient_id,
        patient_visit_id,
        patient_hospital_visit_id,
        patient_hospital_code,
        patient_hospital_name,
        patient_hospital_advice_num,
        patient_hospital_advice_source_num,
        patient_hospital_advice_class,
        patient_hospital_advice_name,
        patient_hospital_advice_remark,
        patient_hospital_advice_begin_time,
        patient_hospital_advice_end_time,
        patient_hospital_advice_exec_dept_name,
        patient_hospital_advice_update_time,
        patient_hospital_advice_source_key
    )
    SELECT TOP (@result)
        '1',
        '住院药物医嘱',
        p.patient_id,
        p.patient_visit_id,
        p.patient_hospital_visit_id,
        p.patient_hospital_code,
        p.patient_hospital_name,
        RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7),
        RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7),
        '医嘱类别',
        '医嘱名称',
        @ThousandChars,
        p.patient_visit_in_time,
        p.patient_visit_in_time,
        p.patient_visit_in_dept_name,
        DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()),
        '1'
    FROM PatientRecords p
    ORDER BY p.patient_id, p.record_seq;

END;
