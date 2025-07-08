-- todo 体征信息表(造数据)

CREATE OR ALTER PROCEDURE cdrd_patient_physical_sign_info__data
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
            INSERT INTO a_cdrd_patient_physical_sign_info (patient_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_physical_sign_type_key,patient_physical_sign_type_value,patient_physical_sign_other,patient_physical_sign_value,patient_physical_sign_unit_key,patient_physical_sign_unit_value,patient_physical_sign_other_unit,patient_physical_sign_time,patient_physical_sign_delete_state_key,patient_physical_sign_update_time,patient_physical_sign_data_source_key
)
            VALUES (
                @patient_id, -- 患者ID
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊编号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊医疗机构编号
                @RandomHospital, -- 医院名称
                '体征key', -- 体征key
                '体征', -- 体征
                '其他体征', -- 其他体征
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 体征数值
                '体征单位key', -- 体征单位key
                '体征单位', -- 体征单位
                '其他体征单位', -- 其他体征单位
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 检查时间
                '删除状态', -- 删除状态
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                '1' -- 数据来源
            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_cdrd_patient_physical_sign_info);
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