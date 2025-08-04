-- todo 门(急)诊住院就诊信息
-- 数据量：每个患者5条（3条门诊，2条住院）
-- 需求：https://docs.qq.com/doc/DYnZXTVZ1THpPVEVC?g=X2hpZGRlbjpoaWRkZW4xNzUzMzIxODczNDE0#g=X2hpZGRlbjpoaWRkZW4xNzUzMzIxODczNDE0
-- 5w, 耗时: 6.5393 秒

CREATE OR ALTER PROCEDURE cdrd_patient_visit_info
    @RecordCount INT = 5, -- 每位患者生成5条就诊记录（3门诊+2住院）
    @result INT OUTPUT
AS
BEGIN
    --1. 初始化设置
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    --2. 数据准备
    -- 生成100个字符的重复字段
    DECLARE @TwoHundredChars NVARCHAR(MAX) = REPLICATE(N'职能', 100);

    -- 计算总记录数：患者数 × 每人生成就诊记录数
    SELECT @result = COUNT(*) * @RecordCount FROM a_cdrd_patient_info;

    IF @result <= 0
    BEGIN
        PRINT 'No eligible patient records found.';
        RETURN;
    END;

    --3. 核心数据生成逻辑
    -- 通过多个CTE（公用表表达式）逐步构建数据：
    -- 获取每位患者生成的就诊记录编号（1~5）

    --为每位患者生成 @RecordCount 条记录（默认5条）
    -- 使用 CROSS JOIN 和 ROW_NUMBER() 实现每位患者生成多条记录
    ;WITH PatientSequences AS (
        SELECT p.patient_id, n.n
        FROM a_cdrd_patient_info p
        CROSS JOIN (
            SELECT TOP (@RecordCount) ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n
            FROM sys.all_columns
        ) n
    ),

    -- 构造就诊类型（门诊/住院）分布：3门诊 + 2住院
    -- 前 3 条记录为门诊（type=1），后 2 条为住院（type=2）
    VisitTypeMapping AS (
        SELECT *,
               CASE WHEN n <= 3 THEN '1' ELSE '2' END AS patient_visit_type_key,
               CASE WHEN n <= 3 THEN '门诊' ELSE '住院' END AS patient_visit_type_value
        FROM PatientSequences
    ),

    -- 为每条记录随机分配各种字段值：
    -- 使用 CROSS APPLY 从多个参考表中随机选取字段值（如医院、就诊类型、医疗付费方式等）。
    RandomFields AS (
        SELECT vt.*,
               h.name AS RandomHospital,
               t.n_key AS VisitTypeKey, t.n_value AS VisitTypeValue,
               pmt.n_key AS MedicalPaymentTypeKey, pmt.n_value AS MedicalPaymentTypeValue,
               ohw.n_key AS OutHospitalWayKey, ohw.n_value AS OutHospitalWayValue,
               vw.n_key AS VisitWayKey, vw.n_value AS VisitWayValue,
               da.n_key AS DrugAllergyKey, da.n_value AS DrugAllergyValue,
               abo.n_key AS AboTypeKey, abo.n_value AS AboTypeValue,
               rh.n_key AS RhTypeKey, rh.n_value AS RhTypeValue,
               diag.n_value AS VisitDiagnosis
        FROM VisitTypeMapping vt
        CROSS APPLY (SELECT TOP 1 name FROM ab_hospital ORDER BY NEWID()) h -- 医院
        CROSS APPLY (SELECT TOP 1 n_key, n_value FROM ab_visitType ORDER BY NEWID()) t -- 就诊类型
        CROSS APPLY (SELECT TOP 1 n_key, n_value FROM ab_paymentMethod ORDER BY NEWID()) pmt -- 医疗付费方式
        CROSS APPLY (SELECT TOP 1 n_key, n_value FROM ab_dischargeMethod ORDER BY NEWID()) ohw -- 离院方式
        CROSS APPLY (SELECT TOP 1 n_key, n_value FROM ab_admissionRoute ORDER BY NEWID()) vw -- 入院途径
        CROSS APPLY (SELECT TOP 1 n_key, n_value FROM ab_drugAllergy ORDER BY NEWID()) da -- 药物过敏
        CROSS APPLY (SELECT TOP 1 n_key, n_value FROM ab_ABO_bloodType ORDER BY NEWID()) abo -- ABO血型
        CROSS APPLY (SELECT TOP 1 n_key, n_value FROM ab_rh_bloodType ORDER BY NEWID()) rh -- RH血型
        CROSS APPLY (SELECT TOP 1 n_value FROM ab_visitDiagnosis ORDER BY NEWID()) diag -- 就诊诊断
    ),

    -- 为每条记录随机分配科室和医生信息：
    -- 从 a_sys_department 表随机选择科室
    -- 从 a_sys_dept_medgp_person 表随机选择医生
    DeptInfo AS (
        SELECT rf.*,
               d.department_id, d.department_name, d.department_code,
               p.user_name, p.user_job_num
        FROM RandomFields rf
        CROSS APPLY (
            SELECT TOP 1 department_id, department_name, department_code
            FROM a_sys_department
            ORDER BY NEWID()
        ) d
        CROSS APPLY (
            SELECT TOP 1 user_name, user_job_num
            FROM a_sys_dept_medgp_person
            WHERE department_treat_group_id = (
                SELECT TOP 1 department_treat_group_id
                FROM a_sys_dept_medgp
                WHERE department_id = d.department_id
                ORDER BY department_treat_group_id
            )
            ORDER BY NEWID()
        ) p
    ),

    -- 生成时间相关字段：
    -- 就诊时间（jzrq）：2022年6月1日之后的随机日期
    -- 就诊年龄（visit_age）：随机生成的年龄
    -- 住院天数（visit_days）：随机生成的住院天数
    -- 序列号（seq_num）：随机编号
    FinalData AS (
        SELECT *,
               DATEADD(DAY, ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS jzrq, --就诊时间
               RIGHT('00' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100), 2) AS visit_age, -- 年龄
               RIGHT('00' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100), 2) AS visit_days, -- 住院天数
               RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7) AS seq_num -- 随机编号
        FROM DeptInfo
    )

    --4. 数据插入
    INSERT INTO a_cdrd_patient_visit_info (
        patient_visit_type_key, patient_visit_type_value, patient_id,
        patient_hospital_visit_id, patient_hospital_code, patient_hospital_name,
        patient_mz_zy_num, patient_visit_age, patient_visit_in_dept_num,
        patient_visit_in_dept_name, patient_visit_in_ward_name,
        patient_visit_doc_num, patient_visit_doc_name, patient_visit_in_time,
        patient_visit_record_num, patient_visit_main_describe,
        patient_visit_present_illness, patient_visit_past_illness,
        patient_visit_personal_illness, patient_visit_menstrual_history,
        patient_visit_obsterical_history, patient_visit_family_history,
        patient_visit_physical_examination, patient_visit_speciality_examination,
        patient_visit_assit_examination, patient_visit_diag, patient_visit_deal,
        patient_visit_record_time, patient_case_num, patient_case_health_card_num,
        patient_case_medical_payment_type_key, patient_case_medical_payment_type_value,
        patient_case_visit_time, patient_case_visit_in_way_key,
        patient_case_visit_in_way_value, patient_case_visit_in_days,
        patient_visit_out_dept_num, patient_visit_out_dept_name,
        patient_visit_out_ward_name, patient_visit_out_time,
        patient_case_clinic_diag, patient_case_diag_name,
        patient_case_drug_allergy_type_key, patient_case_drug_allergy_type_value,
        patient_case_drug_allergy_name, patient_case_abo_type_key,
        patient_case_abo_type_value, patient_case_rh_type_key,
        patient_case_rh_type_value, patient_case_dept_chief_doc_num,
        patient_case_dept_chief_doc_name, patient_case_director_doc_num,
        patient_case_director_doc_name, patient_case_attend_doc_num,
        patient_case_attend_doc_name, patient_case_resident_num,
        patient_case_resident_name, patient_case_out_hospital_type_key,
        patient_case_out_hospital_type_value, patient_case_transfer_to_hospital,
        patient_case_make_over_hospital, patient_case_in_total_cost,
        patient_case_in_selfpay_cost, patient_visit_update_time,
        patient_visit_data_source_key
    )
    SELECT
        patient_visit_type_key,
        patient_visit_type_value,
        patient_id,
        seq_num AS patient_hospital_visit_id,
        seq_num AS patient_hospital_code,
        RandomHospital AS patient_hospital_name,
        seq_num AS patient_mz_zy_num,
        visit_age AS patient_visit_age,
        department_code AS patient_visit_in_dept_num,
        department_name AS patient_visit_in_dept_name,
        N'入院病房' AS patient_visit_in_ward_name,
        user_job_num AS patient_visit_doc_num,
        user_name AS patient_visit_doc_name,
        jzrq AS patient_visit_in_time,
        seq_num AS patient_visit_record_num,
        @TwoHundredChars AS patient_visit_main_describe,
        @TwoHundredChars AS patient_visit_present_illness,
        @TwoHundredChars AS patient_visit_past_illness,
        @TwoHundredChars AS patient_visit_personal_illness,
        @TwoHundredChars AS patient_visit_menstrual_history,
        @TwoHundredChars AS patient_visit_obsterical_history,
        @TwoHundredChars AS patient_visit_family_history,
        @TwoHundredChars AS patient_visit_physical_examination,
        @TwoHundredChars AS patient_visit_speciality_examination,
        @TwoHundredChars AS patient_visit_assit_examination,
        VisitDiagnosis AS patient_visit_diag,
        @TwoHundredChars AS patient_visit_deal,
        jzrq AS patient_visit_record_time,
        seq_num AS patient_case_num,
        seq_num AS patient_case_health_card_num,
        MedicalPaymentTypeKey AS patient_case_medical_payment_type_key,
        MedicalPaymentTypeValue AS patient_case_medical_payment_type_value,
        visit_days AS patient_case_visit_time,
        VisitWayKey AS patient_case_visit_in_way_key,
        VisitWayValue AS patient_case_visit_in_way_value,
        visit_days AS patient_case_visit_in_days,
        department_code AS patient_visit_out_dept_num,
        department_name AS patient_visit_out_dept_name,
        N'出院病房' AS patient_visit_out_ward_name,
        jzrq AS patient_visit_out_time,
        N'门（急）诊诊断' AS patient_case_clinic_diag,
        N'入院诊断' AS patient_case_diag_name,
        DrugAllergyKey AS patient_case_drug_allergy_type_key,
        DrugAllergyValue AS patient_case_drug_allergy_type_value,
        N'青霉素' AS patient_case_drug_allergy_name,
        AboTypeKey AS patient_case_abo_type_key,
        AboTypeValue AS patient_case_abo_type_value,
        RhTypeKey AS patient_case_rh_type_key,
        RhTypeValue AS patient_case_rh_type_value,
        seq_num AS patient_case_dept_chief_doc_num,
        N'科主任' AS patient_case_dept_chief_doc_name,
        seq_num AS patient_case_director_doc_num,
        N'主任（副主任）医师' AS patient_case_director_doc_name,
        user_job_num AS patient_case_attend_doc_num,
        user_name AS patient_case_attend_doc_name,
        seq_num AS patient_case_resident_num,
        N'住院医师' AS patient_case_resident_name,
        OutHospitalWayKey AS patient_case_out_hospital_type_key,
        OutHospitalWayValue AS patient_case_out_hospital_type_value,
        N'' AS patient_case_transfer_to_hospital,
        N'' AS patient_case_make_over_hospital,
        CASE WHEN patient_visit_type_key = '2' THEN '35000.55' ELSE '40000.1234' END AS patient_case_in_total_cost,
        CASE WHEN patient_visit_type_key = '2' THEN '6300.66' ELSE '6000.12345678' END AS patient_case_in_selfpay_cost,
        DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()) AS patient_visit_update_time,
        '1' AS patient_visit_data_source_key
    FROM FinalData
    ORDER BY patient_id, n;

END;
