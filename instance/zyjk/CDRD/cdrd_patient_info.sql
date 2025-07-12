-- todo 检查项目明细(造数据)

CREATE OR ALTER PROCEDURE cdrd_patient_test_project_info
    @RecordCount INT = 1, -- 可通过参数控制记录数，默认100条
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    select @result = count(*) from a_cdrd_patient_lab_examination_info;

    BEGIN
        BEGIN TRANSACTION;
        DECLARE @totalRecords INT = 0;
        DECLARE @Counter1 INT = 1;
        SELECT @totalRecords = COUNT(*)  FROM a_cdrd_patient_lab_examination_info;

        -- 遍历实验室检查报告表 a_cdrd_patient_lab_examination_info
        WHILE @Counter1 <= @totalRecords
        BEGIN

            DECLARE @Counter INT = 1;
            DECLARE @TotalCount INT =0;
            DECLARE @MaxRecords INT = @RecordCount;

            -- 循环插入指定数量的记录
            WHILE @Counter <= @MaxRecords
            BEGIN

                -- 获取 patient_id 和 patient_visit_id（按指定次数插入）
                DECLARE @i INT = 1;
                -- DECLARE @patient_id INT;
                -- DECLARE @patient_visit_id INT;

                # 获取 patient_lab_examination_id
                SELECT patient_lab_examination_id
                FROM (
                    SELECT 
                        patient_lab_examination_id,
                        ROW_NUMBER() OVER (ORDER BY patient_lab_examination_id) AS row_num
                    FROM a_cdrd_patient_lab_examination_info
                ) AS subquery
                WHERE row_num = @Counter1;

                -- -- 子存储过程
                -- -- 医院
                -- DECLARE @RandomHospital NVARCHAR(350);
                -- EXEC p_hospital @v = @RandomHospital OUTPUT;

                -- -- 辅助检查类型
                -- DECLARE @RandomAssitExaminationTypeIdKey NVARCHAR(50), @RandomAssitExaminationTypeIdValue NVARCHAR(50);
                -- EXEC p_assit_examination_type @k = @RandomAssitExaminationTypeIdKey OUTPUT, @v = @RandomAssitExaminationTypeIdValue OUTPUT;


                -- 执行 20 次 
                WHILE @i <= 20
                BEGIN

                    -- 插入单条随机数据
                    INSERT INTO a_cdrd_patient_test_project_info (patient_superior_examination_id,patient_report_num,patient_test_item_name,patient_test_numerical_value,patient_test_unit_name,patient_test_text_value,patient_test_abnormal_flag,patient_test_reference_range,patient_test_delete_state_key,patient_test_update_time,patient_test_data_source_key)
                    VALUES (
                        @patient_superior_examination_id, -- 上级检查ID (取值实验室检查ID或者辅助检查ID)
                        RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 报告编号
                        '空腹血糖（GLU）', -- 项目名称
                        '5。8', -- 定量结果
                        'mmol', -- 定量结果单位
                        '正常', -- 定性结果
                        '异常', -- 异常标识
                        '3.9-6.1', -- 参考值（范围）
                        ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                        DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                        ABS(CHECKSUM(NEWID())) % 2 + 1  -- 数据来源1或2
                    );

                    SET @i = @i + 1;
                END

                
            SET @Counter = @Counter + 1;
            END;

        SET @Counter1 = @Counter1 + 1;
        END;

        COMMIT TRANSACTION;
    END

END