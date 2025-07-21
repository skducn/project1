-- todo  用药信息表(造数据)

CREATE OR ALTER PROCEDURE cdrd_patient_drug_info
    @RecordCount INT = 8,
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @re INT = 1;
    select @re = count(*) from a_cdrd_patient_info;
    SET @result = @re * @RecordCount;
--     select @result = count(*) from a_cdrd_patient_info;

    DECLARE @ThousandChars NVARCHAR(MAX);
    SET @ThousandChars = REPLICATE(N'哈喽你好', 250); -- 每句4个字符，重复250次=1000字符

        -- 编辑基本信息表a_cdrd_patient_info
        DECLARE @Counter1 INT = 1;
        WHILE @Counter1 <= @re
        BEGIN

            -- 获取 patient_id 和 patient_visit_id（按指定次数插入）
            DECLARE @i INT = 1;
            DECLARE @patient_id INT;
            DECLARE @patient_visit_id INT;

--             -- 子存储过程
--             -- 医院
--             DECLARE @RandomHospital NVARCHAR(350);
--             EXEC p_hospital @v = @RandomHospital OUTPUT;
            -- ab表
            -- 医院
            DECLARE @RandomHospital NVARCHAR(100)
            SELECT TOP 1 @RandomHospital=name FROM ab_hospital ORDER BY NEWID()


            -- 诊断类型，诊断名称，ICD10编码
            DECLARE @RandomReportName NVARCHAR(100)
            DECLARE @RandomSampleType NVARCHAR(100)
            DECLARE @RandomProjectName NVARCHAR(100)
            SELECT TOP 1 @RandomReportName=reportname, @RandomSampleType=sampletype, @RandomProjectName=projectname FROM ab_lab ORDER BY NEWID()

--             DECLARE @RandomReportName NVARCHAR(50), @RandomSampleType NVARCHAR(50), @RandomProjectName NVARCHAR(50);
--             EXEC r_lab_examination_info__ @v1 = @RandomReportName OUTPUT, @v2 = @RandomSampleType OUTPUT, @v3 = @RandomProjectName OUTPUT;


            -- 按照记录顺序获取
            DECLARE @patient_id2 INT;
            SELECT @patient_id2 = patient_id
            FROM (
                SELECT
                    patient_id,
                    ROW_NUMBER() OVER (ORDER BY @patient_visit_id) AS row_num
                FROM a_cdrd_patient_info
            ) AS subquery
            WHERE row_num = @Counter1;

 -- 用药信息, 药物名称	规格	频次	每次用量	用量单位	用法	总量
--                 DECLARE @RandomV1 NVARCHAR(50), @RandomV2 NVARCHAR(50), @RandomV3 NVARCHAR(50);
--                 DECLARE @RandomV4 NVARCHAR(50), @RandomV5 NVARCHAR(50), @RandomV6 NVARCHAR(50), @RandomV7 NVARCHAR(50);
--                 EXEC r_drug_info__ @v1 = @RandomV1 OUTPUT, @v2 = @RandomV2 OUTPUT, @v3 = @RandomV3 OUTPUT,
--                 @v4 = @RandomV4 OUTPUT, @v5 = @RandomV5 OUTPUT, @v6 = @RandomV6 OUTPUT, @v7 = @RandomV7 OUTPUT;
            DECLARE @RandomV1 NVARCHAR(100)
            DECLARE @RandomV2 NVARCHAR(100)
            DECLARE @RandomV3 NVARCHAR(100)
            DECLARE @RandomV4 NVARCHAR(100)
            DECLARE @RandomV5 NVARCHAR(100)
            DECLARE @RandomV6 NVARCHAR(100)
            DECLARE @RandomV7 NVARCHAR(100)
            SELECT TOP 1 @RandomV1=v1,@RandomV2=v2,@RandomV3=v3,@RandomV4=v4,@RandomV5=v5,@RandomV6=v6,@RandomV7=v7 FROM ab_drug ORDER BY NEWID()


            -- 先执行 3 次 （仅 patient_id）
            WHILE @i <= 3
            BEGIN

                -- 插入单条随机数据
                INSERT INTO a_cdrd_patient_drug_info (patient_id,patient_superior_advice_id,patient_superior_advice_type,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_recipe_advice_num,patient_drug_name,patient_drug_specs,patient_drug_frequency,patient_drug_once_dose,patient_drug_dose_unit,patient_drug_usage,patient_drug_qty,patient_drug_begin_time,patient_drug_end_time,patient_drug_delete_state_key,patient_drug_update_time,patient_drug_source_key)
                VALUES (
                    @patient_id2, -- 患者ID
                    '', -- 无，取值门诊医嘱ID或者住院医嘱ID
                    '1', -- 如果是门诊医嘱则默认为1，如果是住院医嘱则默认为2
                    '', -- 就诊编号
                    '', -- 就诊医疗机构编号
                    @RandomHospital, -- 医院名称
                    '处方明细/医嘱编号', -- 处方明细/医嘱编号
                    @RandomV1, -- 药品名称
                    @RandomV2, -- 规格
                    @RandomV3, -- 频次
                    @RandomV4, -- 每次用量
                    @RandomV5, -- 用量单位
                    @RandomV6, -- 用法
                    @RandomV7, -- 总量
                    DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 开始时间
                    DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 结束时间
                    ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                    DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                    '2'  -- 数据来源1或2
                );
                SET @i = @i + 1;
            END

            -- 再执行 3 次（patient_id + patient_visit_id）
            WHILE @i <= 6
            BEGIN

--                  -- 用药信息, 药物名称	规格	频次	每次用量	用量单位	用法	总量
--                 EXEC r_drug_info__ @v1 = @RandomV1 OUTPUT, @v2 = @RandomV2 OUTPUT, @v3 = @RandomV3 OUTPUT,
--                 @v4 = @RandomV4 OUTPUT, @v5 = @RandomV5 OUTPUT, @v6 = @RandomV6 OUTPUT, @v7 = @RandomV7 OUTPUT;


                -- 就诊记录表，按照记录顺序获取
                DECLARE @patient_hospital_visit_id NVARCHAR(100);
                DECLARE @patient_hospital_code NVARCHAR(100);
                DECLARE @patient_hospital_name NVARCHAR(100);
                DECLARE @patient_visit_in_time DATETIME;
                DECLARE @patient_visit_in_dept_name NVARCHAR(100);
                SELECT @patient_visit_id = patient_visit_id,
                       @patient_id = patient_id,
                       @patient_hospital_visit_id = patient_hospital_visit_id,
                       @patient_hospital_code = patient_hospital_code,
                       @patient_hospital_name = patient_hospital_name,
                       @patient_visit_in_time = patient_visit_in_time,
                       @patient_visit_in_dept_name = patient_visit_in_dept_name
                FROM (
                    SELECT
                        patient_visit_id,patient_id, patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,
                        patient_visit_in_time, patient_visit_in_dept_name,
                        ROW_NUMBER() OVER (ORDER BY @patient_visit_id) AS row_num
                    FROM a_cdrd_patient_visit_info
                ) AS subquery
                WHERE row_num = @Counter1;


                -- 门诊医嘱，按照记录顺序获取3条门诊医嘱ID
                DECLARE @patient_clinic_advice_id INT;
                SELECT @patient_clinic_advice_id = patient_clinic_advice_id
                FROM (
                    SELECT
                        patient_clinic_advice_id, patient_id,
                        ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY patient_clinic_advice_id) AS row_num
                    FROM a_cdrd_patient_clinic_advice_info
                ) AS subquery
                WHERE row_num = @i-3 AND patient_id = @patient_id2; -- 使用 @i 控制每条记录的偏移


                -- 插入单条随机数据
                INSERT INTO a_cdrd_patient_drug_info (patient_id,patient_superior_advice_id,patient_superior_advice_type,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_recipe_advice_num,patient_drug_name,patient_drug_specs,patient_drug_frequency,patient_drug_once_dose,patient_drug_dose_unit,patient_drug_usage,patient_drug_qty,patient_drug_begin_time,patient_drug_end_time,patient_drug_delete_state_key,patient_drug_update_time,patient_drug_source_key)
                VALUES (
                    @patient_id2, -- 患者ID
                    @patient_clinic_advice_id, -- 上级医嘱ID, 取值门诊医嘱ID或者住院医嘱ID
                    '1', -- 上级医嘱类型, 如果是门诊医嘱则默认为1，如果是住院医嘱则默认为2
                    @patient_hospital_visit_id, -- 就诊编号
                    @patient_hospital_code, -- 就诊医疗机构编号
                    @patient_hospital_name, -- 医院名称
                    '处方明细/医嘱编号', -- 处方明细/医嘱编号
                    @RandomV1, -- 药品名称
                    @RandomV2, -- 规格
                    @RandomV3, -- 频次
                    @RandomV4, -- 每次用量
                    @RandomV5, -- 用量单位
                    @RandomV6, -- 用法
                    @RandomV7, -- 总量
                    @patient_visit_in_time, -- 医嘱开始时间, 同就诊日期
                    @patient_visit_in_time, -- 医嘱结束时间, 同就诊日期
                    ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                    DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                    '1'  -- 数据来源1或2
                );

                SET @i = @i + 1;
            END

            -- 再执行 2 次（patient_id + patient_visit_id）
            WHILE @i <= 8
            BEGIN

--                  -- 用药信息, 药物名称	规格	频次	每次用量	用量单位	用法	总量
--                 EXEC r_drug_info__ @v1 = @RandomV1 OUTPUT, @v2 = @RandomV2 OUTPUT, @v3 = @RandomV3 OUTPUT,
--                 @v4 = @RandomV4 OUTPUT, @v5 = @RandomV5 OUTPUT, @v6 = @RandomV6 OUTPUT, @v7 = @RandomV7 OUTPUT;


                -- 就诊记录表，按照记录顺序获取
                SELECT @patient_visit_id = patient_visit_id,
                       @patient_id = patient_id,
                       @patient_hospital_visit_id = patient_hospital_visit_id,
                       @patient_hospital_code = patient_hospital_code,
                       @patient_hospital_name = patient_hospital_name,
                       @patient_visit_in_time = patient_visit_in_time,
                       @patient_visit_in_dept_name = patient_visit_in_dept_name
                FROM (
                    SELECT
                        patient_visit_id,patient_id, patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,
                        patient_visit_in_time, patient_visit_in_dept_name,
                        ROW_NUMBER() OVER (ORDER BY @patient_visit_id) AS row_num
                    FROM a_cdrd_patient_visit_info
                ) AS subquery
                WHERE row_num = @Counter1;

                -- 住院医嘱，按照记录顺序获取2条住院医嘱ID
                DECLARE @patient_hospital_advice_id INT;
                SELECT @patient_hospital_advice_id = patient_hospital_advice_id
                FROM (
                    SELECT
                        patient_hospital_advice_id, patient_id,
                        ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY patient_hospital_advice_id) AS row_num2
                    FROM a_cdrd_patient_hospital_advice_info
                ) AS subquery2
                WHERE row_num2 = @i-6 AND patient_id = @patient_id2; -- 使用 @i 控制每条记录的偏移


                -- 插入单条随机数据
                INSERT INTO a_cdrd_patient_drug_info (patient_id,patient_superior_advice_id,patient_superior_advice_type,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_recipe_advice_num,patient_drug_name,patient_drug_specs,patient_drug_frequency,patient_drug_once_dose,patient_drug_dose_unit,patient_drug_usage,patient_drug_qty,patient_drug_begin_time,patient_drug_end_time,patient_drug_delete_state_key,patient_drug_update_time,patient_drug_source_key)
                VALUES (
                    @patient_id2, -- 患者ID
                    @patient_hospital_advice_id, -- 上级医嘱ID, 取值门诊医嘱ID或者住院医嘱ID
                    '2', -- 上级医嘱类型, 如果是门诊医嘱则默认为1，如果是住院医嘱则默认为2
                    @patient_hospital_visit_id, -- 就诊编号
                    @patient_hospital_code, -- 就诊医疗机构编号
                    @patient_hospital_name, -- 医院名称
                    '处方明细/医嘱编号', -- 处方明细/医嘱编号
                    @RandomV1, -- 药品名称
                    @RandomV2, -- 规格
                    @RandomV3, -- 频次
                    @RandomV4, -- 每次用量
                    @RandomV5, -- 用量单位
                    @RandomV6, -- 用法
                    @RandomV7, -- 总量
                    @patient_visit_in_time, -- 医嘱开始时间, 同就诊日期
                    @patient_visit_in_time, -- 医嘱结束时间, 同就诊日期
                    ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                    DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                    '1'  -- 数据来源1或2
                );

                SET @i = @i + 1;
            END

        SET @Counter1 = @Counter1 + 1;
        END;


END