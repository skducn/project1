-- todo 实验室检查报告表(造数据)

CREATE OR ALTER PROCEDURE cdrd_patient_lab_examination_info
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

            -- 获取 patient_id 和 patient_visit_id
            DECLARE @patient_id int;
            DECLARE @patient_visit_id int;
            if ABS(CHECKSUM(NEWID())) % 2 = 0
            BEGIN
                -- 50% 概率：仅获取 patient_id（不关联就诊
                SELECT TOP 1 @patient_id = patient_id FROM a_cdrd_patient_info ORDER BY NEWID();
                SET @patient_visit_id = NULL;
            END
            ELSE
            BEGIN
                 -- 50% 概率：获取 patient_id 和 patient_visit_id
                SELECT TOP 1 @patient_id = patient_id, @patient_visit_id = patient_visit_id FROM a_cdrd_patient_visit_info ORDER BY NEWID();
            END

            -- 子存储过程
            -- 医院
            DECLARE @RandomHospital NVARCHAR(350);
            EXEC p_hospital @v = @RandomHospital OUTPUT;


            -- 插入单条随机数据
            INSERT INTO a_cdrd_patient_lab_examination_info (patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_lab_examination_report_num,patient_lab_examination_source_report_num,patient_lab_examination_report_name,patient_lab_examination_sample_type,patient_lab_examination_test_time,patient_lab_examination_sampling_time,patient_lab_examination_report_time,patient_lab_examination_delete_state_key,patient_lab_examination_update_time,patient_lab_examination_data_source_key)
            VALUES (
                @patient_id, -- 患者ID
                @patient_visit_id, -- 就诊记录ID
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊编号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊医疗机构编号
                @RandomHospital, -- 医院名称
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 报告编号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 源系统报告编号
                '报告名称', -- 报告名称
                '样本类型', -- 样本类型
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 检查时间
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 采样时间
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 报告时间
                ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                ABS(CHECKSUM(NEWID())) % 2 + 1  -- 数据来源1或2
            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_cdrd_patient_lab_examination_info);
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