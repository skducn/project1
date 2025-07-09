-- todo  手术记录表(造数据)

CREATE OR ALTER PROCEDURE cdrd_patient_operation_info
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

            -- 手术级别
            DECLARE @RandomOperationLevelIdKey NVARCHAR(50), @RandomOperationLevelIdValue NVARCHAR(50);
            EXEC p_operation_level @k = @RandomOperationLevelIdKey OUTPUT, @v = @RandomOperationLevelIdValue OUTPUT;

            -- 手术类型
            DECLARE @RandomOperationTypeIdKey NVARCHAR(50), @RandomOperationTypeIdValue NVARCHAR(50);
            EXEC p_operation_type @k = @RandomOperationTypeIdKey OUTPUT, @v = @RandomOperationTypeIdValue OUTPUT;

            -- 切口愈合等级
            DECLARE @RandomOperationIncisionHealingGradeIdKey NVARCHAR(50), @RandomOperationIncisionHealingGradeIdValue NVARCHAR(50);
            EXEC p_operation_incision_healing_grade @k = @RandomOperationIncisionHealingGradeIdKey OUTPUT, @v = @RandomOperationIncisionHealingGradeIdValue OUTPUT;


            -- 插入单条随机数据
            INSERT INTO a_cdrd_patient_operation_info (patient_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_operation_num,patient_operation_source_num,patient_operation_name,patient_operation_doc_name,patient_operation_assist_I,patient_operation_assit_II,patient_operation_before_diga,patient_operation_during_diga,patient_operation_after_diga,patient_operation_level_key,patient_operation_level_value,patient_operation_type_key,patient_operation_type_value,patient_operation_incision_healing_grade_key,patient_operation_incision_healing_grade_value,patient_operation_anesthesiologist,patient_operation_anesthesia_type,patient_operation_step_process,patient_operation_begin_time,patient_operation_end_time,patient_operation_delete_state_key,patient_operation_update_time,patient_operation_source_key)
            VALUES (
                @patient_id, -- 患者ID
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊编号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊医疗机构编号
                @RandomHospital, -- 医院名称
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 手术记录编号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 源系统手术记录编号
                '手术名称', -- 手术名称
                '主刀/手术者', -- 主刀/手术者
                'I助', -- I助
                'II助', -- II助
                '术前诊断', -- 术前诊断
                '术中诊断', -- 术中诊断
                '术后诊断', -- 术后诊断
                @RandomOperationLevelIdKey, -- 手术级别key [1,4]
                @RandomOperationLevelIdValue, -- 手术级别
                @RandomOperationTypeIdKey, -- 手术类型key [1,3]
                @RandomOperationTypeIdValue, -- 手术类型
                @RandomOperationIncisionHealingGradeIdKey, -- 切口愈合等级-key [1,4]
                @RandomOperationIncisionHealingGradeIdValue, -- 切口愈合等级
                '麻醉者', -- 麻醉者
                '麻醉方式', -- 麻醉方式
                '手术步骤及经过', -- 手术步骤及经过
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 手术开始时间
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 手术结束时间
                ABS(CHECKSUM(NEWID())) % 2 + 1, -- 删除状态1或2
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                ABS(CHECKSUM(NEWID())) % 2 + 1  -- 数据来源1或2

            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_cdrd_patient_operation_info);
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