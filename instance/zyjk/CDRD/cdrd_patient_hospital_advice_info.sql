-- todo  住院医嘱表(造数据)

CREATE OR ALTER PROCEDURE cdrd_patient_hospital_advice_info
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

            -- 住院医嘱表的患者ID和就诊编号ID均来自 就诊信息
            DECLARE @patient_id int;
            DECLARE @patient_visit_id int;
            SELECT TOP 1 @patient_id = patient_id, @patient_visit_id = patient_visit_id FROM a_cdrd_patient_visit_info ORDER BY NEWID();


            -- 子存储过程
            -- 医院
            DECLARE @RandomHospital NVARCHAR(350);
            EXEC p_hospital @v = @RandomHospital OUTPUT;

            -- 住院医嘱类型
            DECLARE @RandomHospitalAdviceIdKey NVARCHAR(50), @RandomHospitalAdviceIdValue NVARCHAR(50);
            EXEC p_hospital_advice @k = @RandomHospitalAdviceIdKey OUTPUT, @v = @RandomHospitalAdviceIdValue OUTPUT;


            -- 插入单条随机数据
            INSERT INTO a_cdrd_patient_hospital_advice_info (patient_hospital_advice_type_key,patient_hospital_advice_type_value,patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_hospital_advice_num,patient_hospital_advice_source_num,patient_hospital_advice_class,patient_hospital_advice_name,patient_hospital_advice_remark,patient_hospital_advice_begin_time,patient_hospital_advice_end_time,patient_hospital_advice_exec_dept_name,patient_hospital_advice_update_time,patient_hospital_advice_source_key)
            VALUES (
                @RandomHospitalAdviceIdKey, -- 住院医嘱类型-key
                @RandomHospitalAdviceIdValue, -- 住院医嘱类型
                @patient_id, -- 患者ID
                @patient_visit_id, -- 就诊记录ID
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊编号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊医疗机构编号
                @RandomHospital, -- 医院名称
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 医嘱编号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 源系统医嘱编号
                '医嘱类别', -- 医嘱类别
                '医嘱名称', -- 医嘱名称
                '备注', -- 备注
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 医嘱开始时间
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 医嘱结束时间
                '执行科室', -- 执行科室
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                ABS(CHECKSUM(NEWID())) % 2 + 1  -- 数据来源1或2
            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_cdrd_patient_hospital_advice_info);
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