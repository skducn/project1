-- todo 门(急)诊住院就诊信息(造数据)

CREATE OR ALTER PROCEDURE cdrd_patient_visit_info
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

            DECLARE @ExampleText NVARCHAR(200) = N'用于测试性能测试，以下这是一个长度为200个字符的字符串变量，包含中英文和标点符号。This is a variable with 200 characters, including Chinese and English text. 它可以用于测试字段长度、存储过程参数或数据库约束等场景。';

             -- 获取患者ID
            DECLARE @patient_id int;
            SELECT TOP 1 @patient_id = patient_id FROM a_cdrd_patient_info ORDER BY NEWID();

             -- 获取 科室名称和科室ID
            DECLARE @department_name NVARCHAR;
            DECLARE @department_code NVARCHAR;
            SELECT TOP 1 @department_name = department_name, @department_code = department_code FROM a_sys_department ORDER BY NEWID();

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


            -- 插入单条随机数据
            INSERT INTO a_cdrd_patient_visit_info (patient_visit_type_key,patient_visit_type_value,patient_id,patient_hospital_visit_id,patient_hospital_code,patient_hospital_name,patient_mz_zy_num,patient_visit_age,patient_visit_in_dept_num,patient_visit_in_dept_name,patient_visit_in_ward_name,patient_visit_doc_num,patient_visit_doc_name,patient_visit_in_time,patient_visit_record_num,patient_visit_main_describe,patient_visit_present_illness,patient_visit_past_illness,patient_visit_personal_illness,patient_visit_menstrual_history,patient_visit_obsterical_history,patient_visit_family_history,patient_visit_physical_examination,patient_visit_speciality_examination,patient_visit_assit_examination,patient_visit_diag,patient_visit_deal,patient_visit_record_time,patient_case_num,patient_case_health_card_num,patient_case_medical_payment_type_key,patient_case_medical_payment_type_value,patient_case_visit_time,patient_case_visit_in_way_key,patient_case_visit_in_way_value,patient_case_visit_in_days,patient_visit_out_dept_num,patient_visit_out_dept_name,patient_visit_out_ward_name,patient_visit_out_time,patient_case_clinic_diag,patient_case_diag_name,patient_case_drug_allergy_type_key,patient_case_drug_allergy_type_value,patient_case_drug_allergy_name,patient_case_abo_type_key,patient_case_abo_type_value,patient_case_rh_type_key,patient_case_rh_type_value,patient_case_dept_chief_doc_num,patient_case_dept_chief_doc_name,patient_case_director_doc_num,patient_case_director_doc_name,patient_case_attend_doc_num,patient_case_attend_doc_name,patient_case_resident_num,patient_case_resident_name,patient_case_out_hospital_type_key,patient_case_out_hospital_type_value,patient_case_transfer_to_hospital,patient_case_make_over_hospital,patient_case_in_total_cost,patient_case_in_selfpay_cost,patient_visit_update_time,patient_visit_data_source_key)
            VALUES (
                @RandomVisitTypeIdKey, -- 就诊类型key
                @RandomVisitTypeIdValue, -- 就诊类型
                @patient_id, -- 患者id
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊编号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊医疗机构编号
                @RandomHospital, -- 医院名称
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 源系统门诊/住院号
                '23', -- 就诊年龄（岁）
                @department_code, -- 就诊科室编码
                @department_name, -- 就诊科室
                '入院病房', -- 入院病房
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 就诊医生编号
                '就诊医生', -- 就诊医生
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 就诊日期
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 文书编号
                @ExampleText, -- 主诉
                @ExampleText, -- 现病史
                @ExampleText, -- 既往史
                @ExampleText, -- 个人史
                @ExampleText, -- 月经史
                @ExampleText, -- 婚育史
                @ExampleText, -- 家族史
                @ExampleText, -- 体格检查
                @ExampleText, -- 专科检查
                @ExampleText, -- 辅助检查
                '就诊诊断', -- 就诊诊断
                @ExampleText, -- 处置
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 记录时间
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 病案号
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 健康卡号
                @RandomMedicalPaymentTypeIdKey, -- 医疗付费方式key
                @RandomMedicalPaymentTypeIdValue, -- 医疗付费方式
                '6', -- 住院次数
                @RandomVisitWayIdKey, -- 入院途径key
                @RandomVisitWayIdValue, -- 入院途径
                '9', -- 实际住院天数
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 出院科室编码
                '出院科室', -- 出院科室
                '出院病房', -- 出院病房
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 出院日期
                '门（急）诊诊断', -- 门（急）诊诊断
                '入院诊断', -- 入院诊断
                @RandomDrugAllergyTypeIdKey, -- 药物过敏key
                @RandomDrugAllergyTypeIdValue, -- 药物过敏
                '过敏药物', -- 过敏药物
                @RandomAboTypeIdKey, -- ABO血型key
                @RandomAboTypeIdValue, -- ABO血型
                @RandomRhTypeIdKey, -- Rh血型key
                @RandomRhTypeIdValue, -- Rh血型
                 RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 科主任编号
                '科主任', -- 科主任
                 RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 主任（副主任）医师编号
                '主任（副主任）医师', -- 主任（副主任）医师
                 RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 主治医师编号
                '主治医师', -- 主治医师
                 RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7), -- 住院医师编号
                '住院医师', -- 住院医师
                @RandomOutHospitalWayIdKey, -- 离院方式key
                @RandomOutHospitalWayIdValue, -- 离院方式
                '医嘱转院，拟接收机构', -- 医嘱转院，拟接收机构
                '医嘱转让社区卫生机构，拟接收机构', -- 医嘱转让社区卫生机构，拟接收机构
                '40000.1234', -- 住院费用-总费用
                '6000.12345678', -- 住院费用-自付金额
                 DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                 ABS(CHECKSUM(NEWID())) % 2 + 1  -- 数据来源1或2

            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_cdrd_patient_visit_info);
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