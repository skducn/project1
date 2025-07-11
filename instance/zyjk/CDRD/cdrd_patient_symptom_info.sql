-- todo 门(急)诊住院就诊信息(造数据)

CREATE OR ALTER PROCEDURE cdrd_patient_symptom_info
    @RecordCount INT = 1, -- 可通过参数控制记录数，默认100条
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    select @result = count(*) from a_cdrd_patient_info;

    BEGIN
        BEGIN TRANSACTION;
        DECLARE @totalRecords INT = 0;
        DECLARE @Counter1 INT = 1;
        SELECT @totalRecords = COUNT(*)  FROM a_cdrd_patient_info;

        -- 编辑基本信息表a_cdrd_patient_info
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
                DECLARE @patient_id INT;
                DECLARE @patient_visit_id INT;


                -- 子存储过程
                -- 医院
                DECLARE @RandomHospital NVARCHAR(350);
                EXEC p_hospital @v = @RandomHospital OUTPUT;

                 -- 症状名称，症状编号，具体描述
                DECLARE @RandomSymptomName NVARCHAR(50), @RandomSymptomNum NVARCHAR(50), @RandomSymptomDescription NVARCHAR(50);
                EXEC r_symptom_info__ @v1 = @RandomSymptomName OUTPUT, @v2 = @RandomSymptomNum OUTPUT, @v3 = @RandomSymptomDescription OUTPUT;


                -- 先执行 2 次 （仅 patient_id）
                WHILE @i <= 2
                BEGIN
                    SELECT TOP 1 @patient_id = patient_id
                    FROM a_cdrd_patient_info
                    ORDER BY NEWID();

                    SET @patient_visit_id = NULL;

                    -- 插入单条随机数据
                    INSERT INTO a_cdrd_patient_symptom_info (patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_symptom_num,patient_symptom_name,patient_symptom_description,patient_symptom_start_time,patient_symptom_end_time,patient_symptom_delete_state_key,patient_symptom_update_time,patient_symptom_data_source_key)
                    VALUES (
                        @patient_id, -- 患者ID
                        @patient_visit_id, -- 就诊记录ID
                        RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊编号
                        RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊医疗机构编号
                        @RandomHospital, -- 医院名称
                        @RandomSymptomNum, -- 症状编号
                        @RandomSymptomName, -- 症状名称
                        @RandomSymptomDescription, -- 具体描述
                        DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 出现时间
                        DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 结束时间
                        ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                        DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                        '2'  -- 数据来源1或2, 没有的默认为“2”
                    );

                    SET @i = @i + 1;
                END

                -- 再执行 3 次（patient_id + patient_visit_id）
                WHILE @i <= 5
                BEGIN
                    SELECT TOP 1
                        @patient_id = patient_id,
                        @patient_visit_id = patient_visit_id
                    FROM a_cdrd_patient_visit_info
                    WHERE patient_id IS NOT NULL
                    ORDER BY NEWID();

                    -- 插入单条随机数据
                    INSERT INTO a_cdrd_patient_symptom_info (patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_symptom_num,patient_symptom_name,patient_symptom_description,patient_symptom_start_time,patient_symptom_end_time,patient_symptom_delete_state_key,patient_symptom_update_time,patient_symptom_data_source_key)
                    VALUES (
                        @patient_id, -- 患者ID
                        @patient_visit_id, -- 就诊记录ID
                        RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊编号
                        RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊医疗机构编号
                        @RandomHospital, -- 医院名称
                        @RandomSymptomNum, -- 症状编号
                        @RandomSymptomName, -- 症状名称
                        @RandomSymptomDescription, -- 具体描述
                        DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 出现时间
                        DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 结束时间
                        ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                        DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                        '1'  -- 数据来源1或2,有就诊记录ID默认为“1”
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