-- todo  手术记录表(造数据)

CREATE OR ALTER PROCEDURE cdrd_patient_operation_info
    @RecordCount INT = 1, -- 可通过参数控制记录数，默认100条
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    select @result = count(*) from a_cdrd_patient_info;

    DECLARE @TwoHundredChars NVARCHAR(MAX);
    SET @TwoHundredChars = REPLICATE(N'你好', 100); -- 每句4个字符，重复250次=1000字符

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

                -- 手术级别
                DECLARE @RandomOperationLevelIdKey NVARCHAR(50), @RandomOperationLevelIdValue NVARCHAR(50);
                EXEC p_operation_level @k = @RandomOperationLevelIdKey OUTPUT, @v = @RandomOperationLevelIdValue OUTPUT;

                -- 手术类型
                DECLARE @RandomOperationTypeIdKey NVARCHAR(50), @RandomOperationTypeIdValue NVARCHAR(50);
                EXEC p_operation_type @k = @RandomOperationTypeIdKey OUTPUT, @v = @RandomOperationTypeIdValue OUTPUT;

                -- 切口愈合等级
                DECLARE @RandomOperationIncisionHealingGradeIdKey NVARCHAR(50), @RandomOperationIncisionHealingGradeIdValue NVARCHAR(50);
                EXEC p_operation_incision_healing_grade @k = @RandomOperationIncisionHealingGradeIdKey OUTPUT, @v = @RandomOperationIncisionHealingGradeIdValue OUTPUT;



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
                    INSERT INTO a_cdrd_patient_operation_info (patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_operation_num,patient_operation_source_num,patient_operation_name,patient_operation_doc_name,patient_operation_assist_I,patient_operation_assit_II,patient_operation_before_diag,patient_operation_during_diag,patient_operation_after_diag,patient_operation_level_key,patient_operation_level_value,patient_operation_type_key,patient_operation_type_value,patient_operation_incision_healing_grade_key,patient_operation_incision_healing_grade_value,patient_operation_anesthesiologist,patient_operation_anesthesia_type,patient_operation_step_process,patient_operation_begin_time,patient_operation_end_time,patient_operation_delete_state_key,patient_operation_update_time,patient_operation_source_key)
                    VALUES (
                        @patient_id, -- 患者ID
                        @patient_visit_id, -- 就诊记录ID
                        RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊编号
                        RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊医疗机构编号
                        @RandomHospital, -- 医院名称
                        RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 手术记录编号
                        RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 源系统手术记录编号
                        '手术名称', -- 手术名称
                        '主刀/手术者', -- 主刀/手术者
                        'I助', -- I助
                        'II助', -- II助
                        @TwoHundredChars, -- 术前诊断
                        @TwoHundredChars, -- 术中诊断
                        @TwoHundredChars, -- 术后诊断
                        @RandomOperationLevelIdKey, -- 手术级别key [1,4]
                        @RandomOperationLevelIdValue, -- 手术级别
                        @RandomOperationTypeIdKey, -- 手术类型key [1,3]
                        @RandomOperationTypeIdValue, -- 手术类型
                        @RandomOperationIncisionHealingGradeIdKey, -- 切口愈合等级-key [1,4]
                        @RandomOperationIncisionHealingGradeIdValue, -- 切口愈合等级
                        '麻醉者', -- 麻醉者
                        '麻醉方式', -- 麻醉方式
                        '手术步骤及经过', -- 手术步骤及经过
                        DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 手术开始时间
                        DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 手术结束时间
                        ABS(CHECKSUM(NEWID())) % 2 + 1, -- 删除状态1或2
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
                    INSERT INTO a_cdrd_patient_operation_info (patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_operation_num,patient_operation_source_num,patient_operation_name,patient_operation_doc_name,patient_operation_assist_I,patient_operation_assit_II,patient_operation_before_diag,patient_operation_during_diag,patient_operation_after_diag,patient_operation_level_key,patient_operation_level_value,patient_operation_type_key,patient_operation_type_value,patient_operation_incision_healing_grade_key,patient_operation_incision_healing_grade_value,patient_operation_anesthesiologist,patient_operation_anesthesia_type,patient_operation_step_process,patient_operation_begin_time,patient_operation_end_time,patient_operation_delete_state_key,patient_operation_update_time,patient_operation_source_key)
                    VALUES (
                        @patient_id, -- 患者ID
                        @patient_visit_id, -- 就诊记录ID
                        @patient_hospital_visit_id, -- 就诊编号
                        @patient_hospital_code, -- 就诊医疗机构编号
                        @RandomHospital, -- 医院名称
                        RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 手术记录编号
                        RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 源系统手术记录编号
                        '手术名称', -- 手术名称
                        '主刀/手术者', -- 主刀/手术者
                        'I助', -- I助
                        'II助', -- II助
                        @TwoHundredChars, -- 术前诊断
                        @TwoHundredChars, -- 术中诊断
                        @TwoHundredChars, -- 术后诊断
                        @RandomOperationLevelIdKey, -- 手术级别key [1,4]
                        @RandomOperationLevelIdValue, -- 手术级别
                        @RandomOperationTypeIdKey, -- 手术类型key [1,3]
                        @RandomOperationTypeIdValue, -- 手术类型
                        @RandomOperationIncisionHealingGradeIdKey, -- 切口愈合等级-key [1,4]
                        @RandomOperationIncisionHealingGradeIdValue, -- 切口愈合等级
                        '麻醉者', -- 麻醉者
                        '麻醉方式', -- 麻醉方式
                        '手术步骤及经过', -- 手术步骤及经过
                        DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 手术开始时间
                        DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 手术结束时间
                        ABS(CHECKSUM(NEWID())) % 2 + 1, -- 删除状态1或2
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