-- todo 诊断表(造数据)

CREATE OR ALTER PROCEDURE cdrd_patient_diag_info__data
    @RecordCount INT = 1 -- 可通过参数控制记录数，默认100条
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        DECLARE @Counter INT = 1;
        DECLARE @TotalCount INT =0;
        DECLARE @MaxRecords INT = @RecordCount;

        -- 循环插入指定数量的记录
        WHILE @Counter <= @MaxRecords
        BEGIN

            -- 子存储过程
            -- 医院
            DECLARE @RandomHospital NVARCHAR(350);
            EXEC p_hospital @v = @RandomHospital OUTPUT;

            -- 随机获取患者ID
            DECLARE @patient_id int;
            SELECT TOP 1 @patient_id = patient_id FROM a_cdrd_patient_info ORDER BY NEWID();


            -- 插入单条随机数据
            INSERT INTO a_cdrd_patient_diag_info (patient_id,patient_hosipital_visit_id,patient_hospital_code,patient_hospital_name,patient_case_num,patient_diag_num,patient_diag_class,patient_diag_name,patient_diag_is_primary_key,patient_diag_is_primary_value,patient_diag_code,patient_in_state_key,patient_in_state_value,patient_outcome_state_key,patient_outcome_state_value,patient_diag_date,patient_diag_delete_state_key,patient_diag_update_time,patient_diag_data_source_key
)
            VALUES (
                @patient_id, -- 患者ID
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊编号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 诊断医疗机构编号
                @RandomHospital, -- 医院名称
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 病案号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 病人诊断序号
                '诊断类型', -- 诊断类型
                '诊断名称', -- 诊断名称
                '主要诊断key', -- 主要诊断key
                '主要诊断', -- 主要诊断
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- ICD10编码
                '入院病情key', -- 入院病情key
                '入院病情', -- 入院病情
                '出院病情key', -- 出院病情key
                '出院病情', -- 出院病情
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 诊断日期
                '1', -- 删除状态
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                '1' -- 数据来源
            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_cdrd_patient_diag_info);
        END;

        -- 返回插入的记录数
        SELECT @RecordCount AS RequestedCount, @TotalCount AS TotalCount;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        THROW;
    END CATCH;
END;