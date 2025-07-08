-- todo  死亡记录表(造数据)

CREATE OR ALTER PROCEDURE cdrd_patient_death_info__data
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
            INSERT INTO a_cdrd_patient_death_info (patient_id,patient_hospital_visit_id,patient_death_record_id,patient_death_time,patient_death_in_situation,patient_death_in_diag,patient_death_diga_process,patient_death_reason,patient_death_diag,patient_death_update_time,patient_death_source_key)
            VALUES (
                @patient_id, -- 患者ID
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊编号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 文书编号
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 死亡时间
                '入院情况', -- 入院情况
                '入院诊断', -- 入院诊断
                '诊疗经过（抢救经过）', -- 诊疗经过（抢救经过）
                '死亡原因', -- 死亡原因
                '死亡诊断', -- 死亡诊断
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                ABS(CHECKSUM(NEWID())) % 2 + 1  -- 数据来源1或2
            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_cdrd_patient_death_info);
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