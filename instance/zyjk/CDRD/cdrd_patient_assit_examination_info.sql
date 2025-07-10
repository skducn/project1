-- todo  辅助检查报告表(造数据)

CREATE OR ALTER PROCEDURE cdrd_patient_assit_examination_info
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

            -- 随机获取50% 概率
            DECLARE @patient_id int;
            DECLARE @patient_visit_id int;
            if ABS(CHECKSUM(NEWID())) % 2 = 0
            BEGIN
                -- 获取 基本信息表的患者ID
                SELECT TOP 1 @patient_id = patient_id FROM a_cdrd_patient_info ORDER BY NEWID();
                SET @patient_visit_id = NULL;
            END
            ELSE
            BEGIN
                 -- 获取就诊信息表的患者ID和就诊记录ID
                SELECT TOP 1 @patient_id = patient_id, @patient_visit_id = patient_visit_id FROM a_cdrd_patient_visit_info ORDER BY NEWID();
            END

            -- 子存储过程
            -- 医院
            DECLARE @RandomHospital NVARCHAR(350);
            EXEC p_hospital @v = @RandomHospital OUTPUT;

            -- 随机辅助检查类型
            DECLARE @RandomAssitExaminationTypeIdKey NVARCHAR(50), @RandomAssitExaminationTypeIdValue NVARCHAR(50);
            EXEC p_assit_examination_type @k = @RandomAssitExaminationTypeIdKey OUTPUT, @v = @RandomAssitExaminationTypeIdValue OUTPUT;

            -- 插入单条随机数据
            INSERT INTO a_cdrd_patient_assit_examination_info (patient_assit_examination_type_key,patient_assit_examination_type_value,patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_assit_examination_report_num,patient_assit_examination_source_report_num,patient_assit_examination_report_name,patient_assit_examination_check_method,patient_assit_examination_body_site,patient_assit_examination_sample_body,patient_assit_examination_eye_find,patient_assit_examination_microscope_find,patient_assit_examination_check_find,patient_assit_examination_check_conclusion,patient_assit_examination_check_time,patient_assit_examination_report_time,patient_assit_examination_delete_state_key,patient_assit_examination_update_time,patient_assit_examination_data_source_key)
            VALUES (
                @RandomAssitExaminationTypeIdKey, -- 辅助检查类型-key
                @RandomAssitExaminationTypeIdValue, -- 辅助检查类型
                @patient_id, -- 患者ID
                @patient_visit_id, -- 就诊记录ID
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊编号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊医疗机构编号
                @RandomHospital, -- 医院名称
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 报告编号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 源系统报告编号
                '报告名称', -- 报告名称
                '检查方法', -- 检查方法
                '检查部位', -- 检查部位
                '取材部位及组织名称', -- 取材部位及组织名称
                '肉眼所见', -- 肉眼所见
                '镜下所见', -- 镜下所见
                '检查所见', -- 检查所见
                '检查结论', -- 检查结论
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 检查日期
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 报告日期
                ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                ABS(CHECKSUM(NEWID())) % 2 + 1  -- 数据来源1或2
            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_cdrd_patient_assit_examination_info);
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