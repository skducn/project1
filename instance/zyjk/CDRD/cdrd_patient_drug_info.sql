-- todo  用药信息表(造数据)

CREATE OR ALTER PROCEDURE cdrd_patient_drug_info
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
            INSERT INTO a_cdrd_patient_drug_info (patient_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_recipe_advice_num,patient_drug_name,patient_drug_specs,patient_drug_frequency,patient_drug_once_dose,patient_drug_dose_unit,patient_drug_usage,patient_drug_qty,patient_drug_begin_time,patient_drug_end_time,patient_drug_delete_state_key,patient_drug_update_time,patient_drug_source_key)
            VALUES (
                @patient_id, -- 患者ID
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊编号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊医疗机构编号
                @RandomHospital, -- 医院名称
                '处方明细/医嘱编号', -- 处方明细/医嘱编号
                '药品名称', -- 药品名称
                '规格', -- 规格
                '频次', -- 频次
                '每次用量', -- 每次用量
                '用量单位', -- 用量单位
                '用法', -- 用法
                '总量', -- 总量
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 开始时间
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 结束时间
                ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                ABS(CHECKSUM(NEWID())) % 2 + 1  -- 数据来源1或2
            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_cdrd_patient_drug_info);
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