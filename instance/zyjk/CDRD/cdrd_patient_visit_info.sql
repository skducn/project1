-- todo 门(急)诊住院就诊信息(造数据)
-- 数据量：每个患者5条（3条门诊，2条住院），共15万
-- 生成 150000 条！,耗时: 545.8609 秒，1,233,534,976字节  约1.15GB


CREATE OR ALTER PROCEDURE cdrd_patient_visit_info
    @RecordCount INT = 5,
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @re INT = 1;
    select @re = count(*) from a_cdrd_patient_info;
    SET @result = @re * @RecordCount;

    DECLARE @TwoHundredChars NVARCHAR(MAX);
    SET @TwoHundredChars = REPLICATE(N'职能', 100);

    -- 遍历基本信息表
    DECLARE @Counter1 INT = 1;
    WHILE @Counter1 <= @re
    BEGIN

        -- 循环插入5条
        BEGIN

            DECLARE @i INT = 1;

             -- 按照记录顺序获取患者ID
            DECLARE @patient_id int;
            SELECT @patient_id = patient_id
            FROM (
                SELECT
                    patient_id,
                    ROW_NUMBER() OVER (ORDER BY @patient_id) AS row_num
                FROM a_cdrd_patient_info
            ) AS subquery
            WHERE row_num = @Counter1;


             -- 科室表，获取 科室名称、科室编码、科室ID
            DECLARE @department_id INT;
            DECLARE @department_name NVARCHAR(20);
            DECLARE @department_code NVARCHAR(20);
            SELECT TOP 1 @department_id = department_id, @department_name = department_name, @department_code = department_code FROM a_sys_department ORDER BY NEWID();
            -- 科室医疗组，获取医疗组ID
            DECLARE @department_treat_group_id INT;
            SELECT @department_treat_group_id = department_treat_group_id FROM a_sys_dept_medgp WHERE @department_id = department_id;
            -- 科室组人员，获取 姓名和工号
            DECLARE @user_name NVARCHAR(20);
            DECLARE @user_job_num NVARCHAR(20);
            SELECT @user_name = user_name, @user_job_num=user_job_num FROM a_sys_dept_medgp_person WHERE @department_treat_group_id = department_treat_group_id;


            -- 子存储过程
            -- 医院
            DECLARE @RandomHospital NVARCHAR(350);
            EXEC p_hospital @v = @RandomHospital OUTPUT;

            -- 就诊类型
            DECLARE @RandomVisitTypeIdKey NVARCHAR(50), @RandomVisitTypeIdValue NVARCHAR(50);
            EXEC p_visit_type @k = @RandomVisitTypeIdKey OUTPUT, @v = @RandomVisitTypeIdValue OUTPUT;

            -- 医疗付费方式
            DECLARE @RandomMedicalPaymentTypeIdKey NVARCHAR(50), @RandomMedicalPaymentTypeIdValue NVARCHAR(50);
            EXEC p_medical_payment_type @k = @RandomMedicalPaymentTypeIdKey OUTPUT, @v = @RandomMedicalPaymentTypeIdValue OUTPUT;

            -- 离院方式
            DECLARE @RandomOutHospitalWayIdKey NVARCHAR(50), @RandomOutHospitalWayIdValue NVARCHAR(50);
            EXEC p_out_hospital_way @k = @RandomOutHospitalWayIdKey OUTPUT, @v = @RandomOutHospitalWayIdValue OUTPUT;

            -- 入院途径
            DECLARE @RandomVisitWayIdKey NVARCHAR(50), @RandomVisitWayIdValue NVARCHAR(50);
            EXEC p_visit_way @k = @RandomVisitWayIdKey OUTPUT, @v = @RandomVisitWayIdValue OUTPUT;

            -- 药物过敏
            DECLARE @RandomDrugAllergyTypeIdKey NVARCHAR(50), @RandomDrugAllergyTypeIdValue NVARCHAR(50);
            EXEC p_drug_allergy_type @k = @RandomDrugAllergyTypeIdKey OUTPUT, @v = @RandomDrugAllergyTypeIdValue OUTPUT;

            -- ABO血型
            DECLARE @RandomAboTypeIdKey NVARCHAR(50), @RandomAboTypeIdValue NVARCHAR(50);
            EXEC p_abo_type @k = @RandomAboTypeIdKey OUTPUT, @v = @RandomAboTypeIdValue OUTPUT;

            -- Rh血型
            DECLARE @RandomRhTypeIdKey NVARCHAR(50), @RandomRhTypeIdValue NVARCHAR(50);
            EXEC p_rh_type @k = @RandomRhTypeIdKey OUTPUT, @v = @RandomRhTypeIdValue OUTPUT;

            -- 就诊诊断
            DECLARE @RandomVisitDiag NVARCHAR(max);
            EXEC r_visit_info__ @v1 = @RandomVisitDiag OUTPUT;

            -- 就诊日期
            DECLARE @jzrq DATETIME;
            SET @jzrq = DATEADD(DAY,ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01');

            -- 3条门诊
            WHILE @i <= 3
            BEGIN

                -- 插入单条随机数据
                INSERT INTO a_cdrd_patient_visit_info (patient_visit_type_key,patient_visit_type_value,patient_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_mz_zy_num,patient_visit_age,patient_visit_in_dept_num,patient_visit_in_dept_name,patient_visit_in_ward_name,patient_visit_doc_num,patient_visit_doc_name,patient_visit_in_time,patient_visit_record_num,patient_visit_main_describe,patient_visit_present_illness,patient_visit_past_illness,patient_visit_personal_illness,patient_visit_menstrual_history,patient_visit_obsterical_history,patient_visit_family_history,patient_visit_physical_examination,patient_visit_speciality_examination,patient_visit_assit_examination,patient_visit_diag,patient_visit_deal,patient_visit_record_time,patient_case_num,patient_case_health_card_num,patient_case_medical_payment_type_key,patient_case_medical_payment_type_value,patient_case_visit_time,patient_case_visit_in_way_key,patient_case_visit_in_way_value,patient_case_visit_in_days,patient_visit_out_dept_num,patient_visit_out_dept_name,patient_visit_out_ward_name,patient_visit_out_time,patient_case_clinic_diag,patient_case_diag_name,patient_case_drug_allergy_type_key,patient_case_drug_allergy_type_value,patient_case_drug_allergy_name,patient_case_abo_type_key,patient_case_abo_type_value,patient_case_rh_type_key,patient_case_rh_type_value,patient_case_dept_chief_doc_num,patient_case_dept_chief_doc_name,patient_case_director_doc_num,patient_case_director_doc_name,patient_case_attend_doc_num,patient_case_attend_doc_name,patient_case_resident_num,patient_case_resident_name,patient_case_out_hospital_type_key,patient_case_out_hospital_type_value,patient_case_transfer_to_hospital,patient_case_make_over_hospital,patient_case_in_total_cost,patient_case_in_selfpay_cost,patient_visit_update_time,patient_visit_data_source_key)
                VALUES (
                    '1', -- 就诊类型key
                    '门诊', -- 就诊类型
                    @patient_id, -- 患者id
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊编号
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊医疗机构编号
                    @RandomHospital, -- 医院名称
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 源系统门诊/住院号
                    RIGHT('00' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100), 2), -- 就诊年龄（岁）
                    @department_code, -- 就诊科室编码
                    @department_name, -- 就诊科室
                    '入院病房', -- 入院病房
                    @user_job_num, -- 就诊医生编号
                    @user_name, -- 就诊医生
                    @jzrq, -- 就诊日期，从2022年06月01日至今随机精确到秒
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 文书编号
                    @TwoHundredChars, -- 主诉
                    @TwoHundredChars, -- 现病史
                    @TwoHundredChars, -- 既往史
                    @TwoHundredChars, -- 个人史
                    @TwoHundredChars, -- 月经史
                    @TwoHundredChars, -- 婚育史
                    @TwoHundredChars, -- 家族史
                    @TwoHundredChars, -- 体格检查
                    @TwoHundredChars, -- 专科检查
                    @TwoHundredChars, -- 辅助检查
                    @RandomVisitDiag, -- 就诊诊断
                    @TwoHundredChars, -- 处置
                    @jzrq, -- 记录时间
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 病案号
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 健康卡号
                    @RandomMedicalPaymentTypeIdKey, -- 医疗付费方式key
                    @RandomMedicalPaymentTypeIdValue, -- 医疗付费方式
                    RIGHT('00' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100), 2), -- 住院次数
                    @RandomVisitWayIdKey, -- 入院途径key
                    @RandomVisitWayIdValue, -- 入院途径
                    RIGHT('00' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100), 2), -- 实际住院天数
                    @department_code, -- 出院科室编码
                    @department_name, -- 出院科室
                    '出院病房', -- 出院病房
                    @jzrq, -- 出院日期，同就诊日期
                    '门（急）诊诊断', -- 门（急）诊诊断
                    '入院诊断', -- 入院诊断
                    @RandomDrugAllergyTypeIdKey, -- 药物过敏key
                    @RandomDrugAllergyTypeIdValue, -- 药物过敏
                    '青霉素', -- 过敏药物
                    @RandomAboTypeIdKey, -- ABO血型key
                    @RandomAboTypeIdValue, -- ABO血型
                    @RandomRhTypeIdKey, -- Rh血型key
                    @RandomRhTypeIdValue, -- Rh血型
                     RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 科主任编号
                    '科主任', -- 科主任
                     RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 主任（副主任）医师编号
                    '主任（副主任）医师', -- 主任（副主任）医师
                    @user_job_num, -- 主治医师编号
                    @user_name, -- 主治医师
                     RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 住院医师编号
                    '住院医师', -- 住院医师
                    @RandomOutHospitalWayIdKey, -- 离院方式key
                    @RandomOutHospitalWayIdValue, -- 离院方式
                    '', -- 医嘱转院，拟接收机构
                    '', -- 医嘱转让社区卫生机构，拟接收机构
                    '40000.1234', -- 住院费用-总费用
                    '6000.12345678', -- 住院费用-自付金额
                     DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                     '1' -- 数据来源1或2
                );
                SET @i = @i + 1;
            END

            -- 2 次住院
            WHILE @i <= 5
            BEGIN
                 -- 插入单条随机数据
                INSERT INTO a_cdrd_patient_visit_info (patient_visit_type_key,patient_visit_type_value,patient_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_mz_zy_num,patient_visit_age,patient_visit_in_dept_num,patient_visit_in_dept_name,patient_visit_in_ward_name,patient_visit_doc_num,patient_visit_doc_name,patient_visit_in_time,patient_visit_record_num,patient_visit_main_describe,patient_visit_present_illness,patient_visit_past_illness,patient_visit_personal_illness,patient_visit_menstrual_history,patient_visit_obsterical_history,patient_visit_family_history,patient_visit_physical_examination,patient_visit_speciality_examination,patient_visit_assit_examination,patient_visit_diag,patient_visit_deal,patient_visit_record_time,patient_case_num,patient_case_health_card_num,patient_case_medical_payment_type_key,patient_case_medical_payment_type_value,patient_case_visit_time,patient_case_visit_in_way_key,patient_case_visit_in_way_value,patient_case_visit_in_days,patient_visit_out_dept_num,patient_visit_out_dept_name,patient_visit_out_ward_name,patient_visit_out_time,patient_case_clinic_diag,patient_case_diag_name,patient_case_drug_allergy_type_key,patient_case_drug_allergy_type_value,patient_case_drug_allergy_name,patient_case_abo_type_key,patient_case_abo_type_value,patient_case_rh_type_key,patient_case_rh_type_value,patient_case_dept_chief_doc_num,patient_case_dept_chief_doc_name,patient_case_director_doc_num,patient_case_director_doc_name,patient_case_attend_doc_num,patient_case_attend_doc_name,patient_case_resident_num,patient_case_resident_name,patient_case_out_hospital_type_key,patient_case_out_hospital_type_value,patient_case_transfer_to_hospital,patient_case_make_over_hospital,patient_case_in_total_cost,patient_case_in_selfpay_cost,patient_visit_update_time,patient_visit_data_source_key)
                VALUES (
                    '2', -- 就诊类型key
                    '住院', -- 就诊类型
                    @patient_id, -- 患者id
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊编号
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊医疗机构编号
                    @RandomHospital, -- 医院名称
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 源系统门诊/住院号
                    RIGHT('00' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100), 2), -- 就诊年龄（岁）
                    @department_code, -- 就诊科室编码
                    @department_name, -- 就诊科室
                    '入院病房', -- 入院病房
                    @user_job_num, -- 就诊医生编号
                    @user_name, -- 就诊医生
                    @jzrq, -- 就诊日期，从2022年06月01日至今随机精确到秒
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 文书编号
                    @TwoHundredChars, -- 主诉
                    @TwoHundredChars, -- 现病史
                    @TwoHundredChars, -- 既往史
                    @TwoHundredChars, -- 个人史
                    @TwoHundredChars, -- 月经史
                    @TwoHundredChars, -- 婚育史
                    @TwoHundredChars, -- 家族史
                    @TwoHundredChars, -- 体格检查
                    @TwoHundredChars, -- 专科检查
                    @TwoHundredChars, -- 辅助检查
                    @RandomVisitDiag, -- 就诊诊断
                    @TwoHundredChars, -- 处置
                    @jzrq, -- 记录时间
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 病案号
                    RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 健康卡号
                    @RandomMedicalPaymentTypeIdKey, -- 医疗付费方式key
                    @RandomMedicalPaymentTypeIdValue, -- 医疗付费方式
                    RIGHT('00' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100), 2), -- 住院次数
                    @RandomVisitWayIdKey, -- 入院途径key
                    @RandomVisitWayIdValue, -- 入院途径
                    RIGHT('00' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100), 2), -- 实际住院天数
                    @department_code, -- 出院科室编码
                    @department_name, -- 出院科室
                    '出院病房', -- 出院病房
                    @jzrq, -- 出院日期，同就诊日期
                    '门（急）诊诊断', -- 门（急）诊诊断
                    '入院诊断', -- 入院诊断
                    @RandomDrugAllergyTypeIdKey, -- 药物过敏key
                    @RandomDrugAllergyTypeIdValue, -- 药物过敏
                    '青霉素', -- 过敏药物
                    @RandomAboTypeIdKey, -- ABO血型key
                    @RandomAboTypeIdValue, -- ABO血型
                    @RandomRhTypeIdKey, -- Rh血型key
                    @RandomRhTypeIdValue, -- Rh血型
                     RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 科主任编号
                    '科主任', -- 科主任
                     RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 主任（副主任）医师编号
                    '主任（副主任）医师', -- 主任（副主任）医师
                    @user_job_num, -- 主治医师编号
                    @user_name, -- 主治医师
                     RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 住院医师编号
                    '住院医师', -- 住院医师
                    @RandomOutHospitalWayIdKey, -- 离院方式key
                    @RandomOutHospitalWayIdValue, -- 离院方式
                    '', -- 医嘱转院，拟接收机构
                    '', -- 医嘱转让社区卫生机构，拟接收机构
                    '35000.55', -- 住院费用-总费用
                    '6300.66', -- 住院费用-自付金额
                     DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                     '1' -- 数据来源1或2
                );
                SET @i = @i + 1;
            END

        END;

    SET @Counter1 = @Counter1 + 1;
    END;

END