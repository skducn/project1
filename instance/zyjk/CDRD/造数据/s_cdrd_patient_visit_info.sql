-- todo 门(急)诊住院就诊信息
-- 数据量：每个患者5条（3条门诊，2条住院）
-- 需求：https://docs.qq.com/doc/DYnZXTVZ1THpPVEVC?g=X2hpZGRlbjpoaWRkZW4xNzUzMzIxODczNDE0#g=X2hpZGRlbjpoaWRkZW4xNzUzMzIxODczNDE0
-- 5w, 耗时: 6.5393 秒

CREATE OR ALTER PROCEDURE s_cdrd_patient_visit_info
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
    DECLARE @PatientCount INT = 0;

    -- 检查患者表是否有数据
    SELECT @PatientCount = COUNT(*)
    FROM CDRD_PATIENT_INFO
    WHERE patient_id IS NOT NULL;

    SET @result = @PatientCount * @RecordCount;

    IF @PatientCount <= 0
    BEGIN
        RETURN;
    END;

    -- 检查引用表是否有数据
    IF NOT EXISTS (SELECT 1 FROM ab_hospital WHERE name IS NOT NULL) OR
       NOT EXISTS (SELECT 1 FROM ab_visitType WHERE n_key IS NOT NULL) OR
       NOT EXISTS (SELECT 1 FROM ab_paymentMethod WHERE n_key IS NOT NULL) OR
       NOT EXISTS (SELECT 1 FROM ab_dischargeMethod WHERE n_key IS NOT NULL) OR
       NOT EXISTS (SELECT 1 FROM ab_admissionRoute WHERE n_key IS NOT NULL) OR
       NOT EXISTS (SELECT 1 FROM ab_drugAllergy WHERE n_key IS NOT NULL) OR
       NOT EXISTS (SELECT 1 FROM ab_ABO_bloodType WHERE n_key IS NOT NULL) OR
       NOT EXISTS (SELECT 1 FROM ab_rh_bloodType WHERE n_key IS NOT NULL) OR
       NOT EXISTS (SELECT 1 FROM ab_visitDiagnosis WHERE n_value IS NOT NULL) OR
       NOT EXISTS (SELECT 1 FROM SYS_DEPARTMENT WHERE department_id IS NOT NULL) OR
       NOT EXISTS (SELECT 1 FROM SYS_DEPT_MEDGP WHERE department_id IS NOT NULL) OR
       NOT EXISTS (SELECT 1 FROM SYS_DEPT_MEDGP_PERSON WHERE user_name IS NOT NULL AND user_job_num IS NOT NULL)
    BEGIN
        RETURN;
    END;

    BEGIN TRY
        --3. 核心数据生成逻辑
        ;WITH PatientSequences AS (
            -- 只选择 patient_id 字段，避免处理加密字段
            SELECT p.patient_id, n.n
            FROM (SELECT TOP (@PatientCount) patient_id FROM CDRD_PATIENT_INFO WHERE patient_id IS NOT NULL) p
            CROSS JOIN (
                SELECT TOP (@RecordCount) ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n
                FROM sys.all_columns
            ) n
        ),
        VisitTypeMapping AS (
            SELECT
                patient_id,
                n,
                CASE WHEN n <= 3 THEN '1' ELSE '2' END AS patient_visit_type_key,
                CASE WHEN n <= 3 THEN '门诊' ELSE '住院' END AS patient_visit_type_value
            FROM PatientSequences
        ),
        RandomFields AS (
            SELECT TOP (@result)
                vt.patient_id,
                vt.n,
                vt.patient_visit_type_key,
                vt.patient_visit_type_value,
                h.name AS RandomHospital,
                t.n_key AS VisitTypeKey,
                t.n_value AS VisitTypeValue,
                pmt.n_key AS MedicalPaymentTypeKey,
                pmt.n_value AS MedicalPaymentTypeValue,
                ohw.n_key AS OutHospitalWayKey,
                ohw.n_value AS OutHospitalWayValue,
                vw.n_key AS VisitWayKey,
                vw.n_value AS VisitWayValue,
                da.n_key AS DrugAllergyKey,
                da.n_value AS DrugAllergyValue,
                abo.n_key AS AboTypeKey,
                abo.n_value AS AboTypeValue,
                rh.n_key AS RhTypeKey,
                rh.n_value AS RhTypeValue,
                diag.n_value AS VisitDiagnosis,
                DATEADD(DAY, ABS(CHECKSUM(NEWID())) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS jzrq,
                RIGHT('00' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100), 2) AS visit_age,
                RIGHT('00' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100), 2) AS visit_days,
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000000), 7) AS seq_num
            FROM VisitTypeMapping vt
            OUTER APPLY (SELECT TOP 1 name FROM ab_hospital WHERE name IS NOT NULL ORDER BY NEWID()) h
            OUTER APPLY (SELECT TOP 1 n_key, n_value FROM ab_visitType WHERE n_key IS NOT NULL ORDER BY NEWID()) t
            OUTER APPLY (SELECT TOP 1 n_key, n_value FROM ab_paymentMethod WHERE n_key IS NOT NULL ORDER BY NEWID()) pmt
            OUTER APPLY (SELECT TOP 1 n_key, n_value FROM ab_dischargeMethod WHERE n_key IS NOT NULL ORDER BY NEWID()) ohw
            OUTER APPLY (SELECT TOP 1 n_key, n_value FROM ab_admissionRoute WHERE n_key IS NOT NULL ORDER BY NEWID()) vw
            OUTER APPLY (SELECT TOP 1 n_key, n_value FROM ab_drugAllergy WHERE n_key IS NOT NULL ORDER BY NEWID()) da
            OUTER APPLY (SELECT TOP 1 n_key, n_value FROM ab_ABO_bloodType WHERE n_key IS NOT NULL ORDER BY NEWID()) abo
            OUTER APPLY (SELECT TOP 1 n_key, n_value FROM ab_rh_bloodType WHERE n_key IS NOT NULL ORDER BY NEWID()) rh
            OUTER APPLY (SELECT TOP 1 n_value FROM ab_visitDiagnosis WHERE n_value IS NOT NULL ORDER BY NEWID()) diag
        ),
        DeptInfo AS (
            SELECT
                rf.patient_visit_type_key,
                rf.patient_visit_type_value,
                rf.patient_id,
                rf.n,
                rf.RandomHospital,
                rf.VisitTypeKey,
                rf.VisitTypeValue,
                rf.MedicalPaymentTypeKey,
                rf.MedicalPaymentTypeValue,
                rf.OutHospitalWayKey,
                rf.OutHospitalWayValue,
                rf.VisitWayKey,
                rf.VisitWayValue,
                rf.DrugAllergyKey,
                rf.DrugAllergyValue,
                rf.AboTypeKey,
                rf.AboTypeValue,
                rf.RhTypeKey,
                rf.RhTypeValue,
                rf.VisitDiagnosis,
                rf.jzrq,
                rf.visit_age,
                rf.visit_days,
                rf.seq_num,
                d.department_id,
                d.department_name,
                d.department_code,
                p.user_name,
                p.user_job_num
            FROM RandomFields rf
            OUTER APPLY (
                SELECT TOP 1 department_id, department_name, department_code
                FROM SYS_DEPARTMENT
                WHERE department_id IS NOT NULL
                ORDER BY NEWID()
            ) d
            OUTER APPLY (
                SELECT TOP 1 user_name, user_job_num
                FROM SYS_DEPT_MEDGP_PERSON
                WHERE department_treat_group_id = (
                    SELECT TOP 1 department_treat_group_id
                    FROM SYS_DEPT_MEDGP
                    WHERE department_id = d.department_id
                    ORDER BY NEWID()
                )
                AND user_name IS NOT NULL AND user_job_num IS NOT NULL
                ORDER BY NEWID()
            ) p
        ),
        FinalData AS (
            SELECT TOP (@result)
                patient_visit_type_key,
                patient_visit_type_value,
                patient_id,
                n,
                RandomHospital,
                VisitTypeKey,
                VisitTypeValue,
                MedicalPaymentTypeKey,
                MedicalPaymentTypeValue,
                OutHospitalWayKey,
                OutHospitalWayValue,
                VisitWayKey,
                VisitWayValue,
                DrugAllergyKey,
                DrugAllergyValue,
                AboTypeKey,
                AboTypeValue,
                RhTypeKey,
                RhTypeValue,
                VisitDiagnosis,
                jzrq,
                visit_age,
                visit_days,
                seq_num,
                department_id,
                department_name,
                department_code,
                user_name,
                user_job_num
            FROM DeptInfo
        )

        --4. 数据插入
        INSERT INTO CDRD_PATIENT_VISIT_INFO (
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
            CASE WHEN patient_visit_type_key = '2' THEN '3500.55' ELSE '400.34' END AS patient_case_in_total_cost,
            CASE WHEN patient_visit_type_key = '2' THEN '630.66' ELSE '600.18' END AS patient_case_in_selfpay_cost,
            DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()) AS patient_visit_update_time,
            '1' AS patient_visit_data_source_key
        FROM FinalData
        ORDER BY patient_id, n;

    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END;

