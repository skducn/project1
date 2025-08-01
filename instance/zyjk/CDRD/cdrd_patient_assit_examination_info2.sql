-- todo  辅助检查报告表(造数据)
-- 5w, 耗时: 1807.5582 秒, 547,831,808


CREATE OR ALTER PROCEDURE cdrd_patient_assit_examination_info
    @RecordCount INT = 5,
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @ThousandChars NVARCHAR(MAX);
    SET @ThousandChars = REPLICATE(N'哈喽你好', 250); -- 每句4个字符，重复250次=1000字符

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
            DECLARE @AssitExaminationTypeIdValue NVARCHAR(50);
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

                if @i = 1
                BEGIN
                    SET @AssitExaminationTypeIdValue = '电生理检查';
                END
                if @i = 2
                BEGIN
                    SET @AssitExaminationTypeIdValue = '放射学检查';
                END


                -- 插入单条随机数据
                INSERT INTO a_cdrd_patient_assit_examination_info (patient_assit_examination_type_key,patient_assit_examination_type_value,patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_assit_examination_report_num,patient_assit_examination_source_report_num,patient_assit_examination_report_name,patient_assit_examination_check_method,patient_assit_examination_body_site,patient_assit_examination_sample_body,patient_assit_examination_eye_find,patient_assit_examination_microscope_find,patient_assit_examination_check_find,patient_assit_examination_check_conclusion,patient_assit_examination_check_time,patient_assit_examination_report_time,patient_assit_examination_delete_state_key,patient_assit_examination_update_time,patient_assit_examination_data_source_key)
                VALUES (
                    @i, -- 辅助检查类型-key
                    @AssitExaminationTypeIdValue, -- 辅助检查类型
                    @patient_id, -- 患者ID
                    @patient_visit_id, -- 就诊记录ID
                    @patient_visit_id, -- 就诊编号
                    @patient_visit_id, -- 就诊医疗机构编号
                    @RandomHospital, -- 医院名称
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 报告编号
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 源系统报告编号
                    '报告名称', -- 报告名称
                    '检查方法', -- 检查方法
                    '检查部位', -- 检查部位
                    '取材部位及组织名称', -- 取材部位及组织名称
                    @ThousandChars, -- 肉眼所见
                    @ThousandChars, -- 镜下所见
                    @ThousandChars, -- 检查所见
                    @ThousandChars, -- 检查结论
                    DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 检查日期
                    DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 报告日期
                    ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                    DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                    '2' -- 数据来源1或2
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


                if @i = 3
                BEGIN
                    SET @AssitExaminationTypeIdValue = '超声检查';
                END
                if @i = 4
                BEGIN
                    SET @AssitExaminationTypeIdValue = '内镜检查';
                END
                if @i = 5
                BEGIN
                    SET @AssitExaminationTypeIdValue = '病理检查';
                END

                -- 插入单条随机数据
                INSERT INTO a_cdrd_patient_assit_examination_info (patient_assit_examination_type_key,patient_assit_examination_type_value,patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_assit_examination_report_num,patient_assit_examination_source_report_num,patient_assit_examination_report_name,patient_assit_examination_check_method,patient_assit_examination_body_site,patient_assit_examination_sample_body,patient_assit_examination_eye_find,patient_assit_examination_microscope_find,patient_assit_examination_check_find,patient_assit_examination_check_conclusion,patient_assit_examination_check_time,patient_assit_examination_report_time,patient_assit_examination_delete_state_key,patient_assit_examination_update_time,patient_assit_examination_data_source_key)
                VALUES (
                    @i, -- 辅助检查类型-key
                    @AssitExaminationTypeIdValue, -- 辅助检查类型
                    @patient_id, -- 患者ID
                    @patient_visit_id, -- 就诊记录ID
                    @patient_hospital_visit_id, -- 就诊编号
                    @patient_hospital_code, -- 就诊医疗机构编号
                    @RandomHospital, -- 医院名称
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 报告编号
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 源系统报告编号
                    '报告名称', -- 报告名称
                    '检查方法', -- 检查方法
                    CASE WHEN @i = 5 THEN '' ELSE '随机值123' END, -- 检查部位，如果类型为“病理检查”则为空，否则随机需有值
                    CASE WHEN @i = 5 THEN '随机值' ELSE '' END, -- 取材部位及组织名称，如果类型为“病理检查”则随机需有值，否则为空
                    @ThousandChars, -- 肉眼所见
                    @ThousandChars, -- 镜下所见
                    @ThousandChars, -- 检查所见
                    @ThousandChars, -- 检查结论
                    DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 检查日期
                    DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1,'2022-06-01'), -- 报告日期
                    ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                    DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                    '1' -- 数据来源1或2
                );

                SET @i = @i + 1;
            END

        END;

    SET @Counter1 = @Counter1 + 1;
    END;

END