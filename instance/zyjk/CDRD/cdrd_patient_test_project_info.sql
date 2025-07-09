-- todo  检查项目明细(造数据)

CREATE OR ALTER PROCEDURE cdrd_patient_test_project_info
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

            -- 插入单条随机数据
            INSERT INTO a_cdrd_patient_test_project_info (patient_report_num,patient_test_item_name,patient_test_numerical_value,patient_test_unit_name,patient_test_text_value,patient_test_abnormal_flag,patient_test_reference_range,patient_test_delete_state_key,patient_test_update_time,patient_test_data_source_key)
            VALUES (
                 RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 报告编号
                '项目名称', -- 项目名称
                '定量结果', -- 定量结果
                '定量结果单位', -- 定量结果单位
                '定性结果', -- 定性结果
                '异常标识', -- 异常标识
                '参考值（范围）', -- 参考值（范围）
                ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                ABS(CHECKSUM(NEWID())) % 2 + 1  -- 数据来源1或2

            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_cdrd_patient_test_project_info);
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