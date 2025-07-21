-- todo 体征信息表(造数据)
-- 5w, 耗时: 1836.6717 秒, 7,086,080字节

CREATE OR ALTER PROCEDURE cdrd_patient_physical_sign_info
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

            -- 体征
            DECLARE @RandomPhysicalSignIdKey NVARCHAR(100)
            DECLARE @RandomPhysicalSignIdValue NVARCHAR(100)
            SELECT TOP 1 @RandomPhysicalSignIdKey=n_key, @RandomPhysicalSignIdValue=n_value FROM ab_physicalSign ORDER BY NEWID()
--             DECLARE @RandomPhysicalSignIdKey NVARCHAR(50), @RandomPhysicalSignIdValue NVARCHAR(50);
--             EXEC p_physical_sign @k = @RandomPhysicalSignIdKey OUTPUT, @v = @RandomPhysicalSignIdValue OUTPUT;

            -- 体征单位
            DECLARE @RandomPhysicalSignUnitIdKey NVARCHAR(50), @RandomPhysicalSignUnitIdValue NVARCHAR(50);
            EXEC p_physical_sign_unit @k = @RandomPhysicalSignUnitIdKey OUTPUT, @v = @RandomPhysicalSignUnitIdValue OUTPUT;



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
                INSERT INTO a_cdrd_patient_physical_sign_info (patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_physical_sign_type_key,patient_physical_sign_type_value,patient_physical_sign_other,patient_physical_sign_value,patient_physical_sign_unit_key,patient_physical_sign_unit_value,patient_physical_sign_other_unit,patient_physical_sign_time,patient_physical_sign_delete_state_key,patient_physical_sign_update_time,patient_physical_sign_data_source_key)
                VALUES (
                    @patient_id, -- 患者ID
                    @patient_visit_id, -- 就诊编号ID
                    @patient_visit_id, -- 就诊编号
                    @patient_visit_id, -- 就诊医疗机构编号
                    @RandomHospital, -- 医院名称
                    @RandomPhysicalSignIdKey, -- 体征key
                    @RandomPhysicalSignIdValue, -- 体征
                    '其他体征', -- 其他体征
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 体征数值
                    @RandomPhysicalSignUnitIdKey, -- 体征单位key
                    @RandomPhysicalSignUnitIdValue, -- 体征单位
                    '其他体征单位', -- 其他体征单位
                    DATEADD(DAY, ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01'), -- 检查时间, 从2022年06月01日至今随机，精确到秒
                    ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                    DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                    '2'  -- 数据来源1或2
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
                INSERT INTO a_cdrd_patient_physical_sign_info (patient_id,patient_visit_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_physical_sign_type_key,patient_physical_sign_type_value,patient_physical_sign_other,patient_physical_sign_value,patient_physical_sign_unit_key,patient_physical_sign_unit_value,patient_physical_sign_other_unit,patient_physical_sign_time,patient_physical_sign_delete_state_key,patient_physical_sign_update_time,patient_physical_sign_data_source_key)
                VALUES (
                    @patient_id, -- 患者ID
                    @patient_visit_id, -- 就诊编号ID
                    @patient_hospital_visit_id, -- 就诊编号
                    @patient_hospital_code, -- 就诊医疗机构编号
                    @patient_hospital_name, -- 医院名称
                    @RandomPhysicalSignIdKey, -- 体征key
                    @RandomPhysicalSignIdValue, -- 体征
                    '其他体征', -- 其他体征
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 体征数值
                    @RandomPhysicalSignUnitIdKey, -- 体征单位key
                    @RandomPhysicalSignUnitIdValue, -- 体征单位
                    '其他体征单位', -- 其他体征单位
                    DATEADD(DAY, ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01'), -- 检查时间, 从2022年06月01日至今随机，精确到秒
                    ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                    DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                    '1'  -- 数据来源1或2
                );

                SET @i = @i + 1;
            END

        END;

    SET @Counter1 = @Counter1 + 1;
    END;


END