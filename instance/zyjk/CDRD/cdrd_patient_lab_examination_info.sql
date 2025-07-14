-- todo 实验室检查报告表(造数据)

CREATE OR ALTER PROCEDURE cdrd_patient_lab_examination_info
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
                DECLARE @patient_hospital_visit_id NVARCHAR(100);
                DECLARE @patient_hospital_code NVARCHAR(100);
                DECLARE @patient_hospital_name NVARCHAR(50);
                DECLARE @patient_visit_in_time DATETIME;


                -- 子存储过程
                -- 医院
                DECLARE @RandomHospital NVARCHAR(350);
                EXEC p_hospital @v = @RandomHospital OUTPUT;

                -- 诊断类型，诊断名称，ICD10编码
                DECLARE @RandomReportName NVARCHAR(50), @RandomSampleType NVARCHAR(50), @RandomProjectName NVARCHAR(50);
                EXEC r_lab_examination_info__ @v1 = @RandomReportName OUTPUT, @v2 = @RandomSampleType OUTPUT, @v3 = @RandomProjectName OUTPUT;


                -- 先执行 2 次 （仅 patient_id）
                WHILE @i <= 2
                BEGIN
                    -- 按照记录顺序获取
                    SELECT @patient_id = patient_id
                    FROM (
                        SELECT
                            patient_id,
                            ROW_NUMBER() OVER (ORDER BY @patient_visit_id) AS row_num
                        FROM a_cdrd_patient_info
                    ) AS subquery
                    WHERE row_num = @Counter1;

                    SET @patient_visit_id = NULL;

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
                        @RandomReportName, -- 报告名称
                        @RandomSampleType, -- 样本类型
                        DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 检查时间
                        DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 采样时间
                        DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 报告时间
                        ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                        DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                        '2'  -- 数据来源1或2
                    );
                    SET @i = @i + 1;
                END

                -- 再执行 3 次（patient_id + patient_visit_id）
                WHILE @i <= 5
                BEGIN

--                     -- 按照记录顺序获取
--                     SELECT @patient_id = patient_id, @patient_visit_id = patient_visit_id
--                     FROM (
--                         SELECT
--                             patient_visit_id, patient_id,
--                             ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY patient_visit_id) AS row_num2
--                         FROM a_cdrd_patient_visit_info
--                     ) AS subquery2
--                     WHERE row_num2 = @i AND patient_id = @patient_id; -- 使用 @i 控制每条记录的偏移

                    -- 按照记录顺序获取
                    SELECT @patient_visit_id = patient_visit_id,
                           @patient_id = patient_id,
                           @patient_hospital_visit_id = patient_hospital_visit_id, -- 就诊编号
                           @patient_hospital_code = patient_hospital_code,  -- 医疗机构编号
                           @patient_hospital_name = patient_hospital_name, -- 医院名称
                           @patient_visit_in_time = patient_visit_in_time -- 入院时间
                    FROM (
                        SELECT
                            patient_visit_id,patient_id, patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,
                            patient_visit_in_time, patient_visit_in_dept_name,patient_visit_diag,
                            ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY @patient_visit_id) AS row_num
                        FROM a_cdrd_patient_visit_info
                    ) AS subquery
                    WHERE row_num = @i AND patient_id = @patient_id; -- 使用 @i 控制每条记录的偏移


                    -- 插入单条随机数据
                    INSERT INTO a_cdrd_patient_lab_examination_info (patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_lab_examination_report_num,patient_lab_examination_source_report_num,patient_lab_examination_report_name,patient_lab_examination_sample_type,patient_lab_examination_test_time,patient_lab_examination_sampling_time,patient_lab_examination_report_time,patient_lab_examination_delete_state_key,patient_lab_examination_update_time,patient_lab_examination_data_source_key)
                    VALUES (
                        @patient_id, -- 患者ID
                        @patient_visit_id, -- 就诊记录ID
                        @patient_hospital_visit_id, -- 就诊编号
                        @patient_hospital_code, -- 就诊医疗机构编号
                        @patient_hospital_name, -- 医院名称
                        RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 报告编号
                        RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 源系统报告编号
                        @RandomReportName, -- 报告名称
                        @RandomSampleType, -- 样本类型
                        DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 检查时间
                        DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 采样时间
                        DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 报告时间
                        ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                        DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                        '1'  -- 数据来源1或2
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