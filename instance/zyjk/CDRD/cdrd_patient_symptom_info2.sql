-- todo 症状信息(造数据)
-- 5w，耗时: 1902.2599 秒， 8,986,624字节

CREATE OR ALTER PROCEDURE cdrd_patient_symptom_info
    @RecordCount INT = 5,
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @re INT = 1;
    select @re = count(*) from a_cdrd_patient_info;
    SET @result = @re * @RecordCount;

    -- 遍历基本信息表
    DECLARE @Counter1 INT = 1;
    WHILE @Counter1 <= @re
    BEGIN

        -- 循环插入5条
        BEGIN

            -- 获取 patient_id 和 patient_visit_id（按指定次数插入）
            DECLARE @i INT = 1;
            DECLARE @patient_id INT;
            DECLARE @patient_visit_id INT;
            DECLARE @patient_hospital_visit_id NVARCHAR(100);
            DECLARE @patient_hospital_code NVARCHAR(100);
            DECLARE @patient_hospital_name NVARCHAR(50);
            DECLARE @patient_visit_in_time DATETIME;


--             -- 子存储过程
--             -- 医院
--             DECLARE @RandomHospital NVARCHAR(350);
--             EXEC p_hospital @v = @RandomHospital OUTPUT;
            -- ab表
            -- 医院
            DECLARE @RandomHospital NVARCHAR(100)
            SELECT TOP 1 @RandomHospital=name FROM ab_hospital ORDER BY NEWID()


            -- 症状名称，症状编号，具体描述
            DECLARE @RandomSymptomName NVARCHAR(100)
            DECLARE @RandomSymptomNum NVARCHAR(100)
            DECLARE @RandomSymptomDescription NVARCHAR(100)
            SELECT TOP 1 @RandomSymptomName=name,@RandomSymptomNum=code,@RandomSymptomDescription=desc1 FROM ab_symptom ORDER BY NEWID()

--             DECLARE @RandomSymptomName NVARCHAR(50), @RandomSymptomNum NVARCHAR(50), @RandomSymptomDescription NVARCHAR(50);
--             EXEC r_symptom_info__ @v1 = @RandomSymptomName OUTPUT, @v2 = @RandomSymptomNum OUTPUT, @v3 = @RandomSymptomDescription OUTPUT;


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
                INSERT INTO a_cdrd_patient_symptom_info (patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_symptom_num,patient_symptom_name,patient_symptom_description,patient_symptom_start_time,patient_symptom_end_time,patient_symptom_delete_state_key,patient_symptom_update_time,patient_symptom_data_source_key)
                VALUES (
                    @patient_id, -- 患者ID
                    @patient_visit_id, -- 就诊记录ID
                    @patient_visit_id, -- 就诊编号
                    @patient_visit_id, -- 就诊医疗机构编号
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
                INSERT INTO a_cdrd_patient_symptom_info (patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_symptom_num,patient_symptom_name,patient_symptom_description,patient_symptom_start_time,patient_symptom_end_time,patient_symptom_delete_state_key,patient_symptom_update_time,patient_symptom_data_source_key)
                VALUES (
                    @patient_id, -- 患者ID
                    @patient_visit_id, -- 就诊记录ID
                    @patient_hospital_visit_id, -- 就诊编号
                    @patient_hospital_code, -- 就诊医疗机构编号
                    @patient_hospital_name, -- 医院名称
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

        END;

    SET @Counter1 = @Counter1 + 1;
    END;



END