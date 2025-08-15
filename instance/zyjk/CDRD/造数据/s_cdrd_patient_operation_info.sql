-- todo  手术记录表(造数据)
-- 数据量：每名患者5条（共15万），其中两条只有patientid，三条均有patientid、patient_visit_id
-- # 5w，耗时: 0.6143 秒

CREATE OR ALTER PROCEDURE s_cdrd_patient_operation_info
    @RecordCount INT = 5,
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- 获取患者数量
    DECLARE @re INT = 1;
    SELECT @re = COUNT(*) FROM CDRD_PATIENT_INFO;
    SET @result = @re * @RecordCount;


    -- 术前诊断
    -- 术中诊断
    -- 术后诊断
    DECLARE @PreoperativeDiagnosis1 NVARCHAR(MAX) = '乳腺肿瘤：患者女性，62 岁，主因 “发现左侧乳腺肿物 7 月、乳头血性溢液伴乳头溃疡 2 月” 就诊。查体发现左侧乳头凹陷结痂，左侧乳腺皮肤可见多发红斑，左侧乳头内侧触及肿物，直径约 3cm，质硬，左侧腋窝触及多发肿大淋巴结，2cm，质硬，可活动。BI-RADS 5 类，左腋窝肿大淋巴结，转移待排。术前诊断为左侧乳腺癌，cT4bN2M0，IIIB 期，HR 阳性、Her2 阴性。';
    DECLARE @PreoperativeDiagnosis2 NVARCHAR(MAX) = '肺部结节：患者主诉体检发现肺部结节 1 个月。1 个月前在单位体检中进行胸部 CT 检查，发现右肺上叶有一个直径约 1.5cm 的结节，边缘不规则，有毛刺征，患者无咳嗽、咳痰、咯血、胸痛、呼吸困难等症状。术前诊断为右肺上叶结节，性质待查，恶性可能性大。';
    DECLARE @PreoperativeDiagnosis3 NVARCHAR(MAX) = '椎管内肿瘤：患者女性，72 岁，因 “腰痛伴双下肢麻木 5 个月，加重伴二便失禁 1 周” 入院。5 个月前突发腰痛伴双下肢麻木，当地医院腰椎 MRI 报告显示 “腰椎管狭窄”，经药物保守治疗症状短暂缓解后，病情因感冒恶化，双腿完全丧失行走能力，大小便功能进行性障碍。查体发现腹股沟平面以下皮肤感觉明显减退，双下肢关键肌群肌力仅为 III 级，肌张力异常增高，双侧病理性巴彬斯基征阳性。完善全脊柱 MRI 检查发现胸椎椎管内肿瘤。术前诊断为胸椎椎管内肿瘤。';

    -- 手术经过步骤
    DECLARE @OperationWay NVARCHAR(MAX) = '术前准备：患者入室后建立静脉通路，常规监测心电图、血压、血氧饱和度，麻醉诱导后行气管插管，确认麻醉效果满意。患者取仰卧位，术区常规消毒、铺无菌巾单，连接腹腔镜设备并检查其功能正常。
建立气腹：于脐下缘做一长约 10mm 弧形切口，切开皮肤及皮下组织，用气腹针穿刺进入腹腔，注入二氧化碳气体建立气腹，维持腹内压在 12-14mmHg。
置入 Trocar：通过脐部切口置入 10mm Trocar，置入腹腔镜探查腹腔：肝脏形态正常，胆囊张力中等，大小约 8cm×3cm，胆囊壁增厚（约 3mm），胆囊颈部可见结石嵌顿，胆总管无明显扩张，腹腔内无积液及粘连。分别于剑突下 2cm、右锁骨中线肋缘下 2cm 处各做一 5mm 切口，置入 Trocar 作为操作孔。
游离胆囊三角：用分离钳仔细分离胆囊周围粘连，显露胆囊三角（Calot 三角），确认胆囊管、肝总管及胆总管的解剖关系，避免损伤。用钛夹夹闭胆囊管近胆囊侧，暂不切断，继续游离胆囊动脉，确认后用钛夹夹闭并切断。
切除胆囊：提起胆囊，用电钩沿胆囊床浆膜层剥离胆囊，剥离过程中仔细止血（必要时用电凝止血），完整切除胆囊。检查胆囊床无渗血、胆漏，确认切除的胆囊内有 1 枚直径约 1.5cm 结石。
取出胆囊及关腹：将胆囊装入取物袋，经脐部 Trocar 取出。再次探查腹腔，确认无出血、胆漏及器械遗留后，放出腹腔内二氧化碳气体，拔除各 Trocar，切口用可吸收线皮下缝合，无菌敷料覆盖。
术毕：麻醉苏醒后，患者生命体征平稳，安返病房。';




    BEGIN TRY
        BEGIN TRANSACTION;

        -- Step 1: 获取所有患者 ID
        ;WITH Patients AS (
            SELECT patient_id
            FROM CDRD_PATIENT_INFO
        ),

        -- Step 2: 生成每位患者 2 条无就诊记录
        NoVisitRecords AS (
            SELECT p.patient_id, n.n
            FROM Patients p
            CROSS JOIN (SELECT 1 AS n UNION ALL SELECT 2) n
        ),

        -- Step 3: 生成每位患者最多 3 条就诊记录
        VisitRecords AS (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY patient_visit_in_time DESC) AS seq
            FROM CDRD_PATIENT_VISIT_INFO
        ),
        PatientVisitRecords AS (
            SELECT vr.*
            FROM VisitRecords vr
            WHERE vr.seq <= 3
        ),

        -- Step 4: 为无就诊记录生成随机字段
        NoVisitRandomFields AS (
            SELECT nvr.patient_id,
                   NULL AS patient_visit_id,
                   NULL AS patient_hospital_visit_id,
                   NULL AS patient_hospital_code,
                   h.name AS RandomHospital,
                   '2' AS patient_operation_source_key
            FROM NoVisitRecords nvr
            CROSS APPLY (SELECT TOP 1 name FROM ab_hospital ORDER BY NEWID()) h
        ),

        -- Step 5: 为有就诊记录生成随机字段
        VisitRandomFields AS (
            SELECT pvr.patient_id,
                   pvr.patient_visit_id,
                   pvr.patient_hospital_visit_id,
                   pvr.patient_hospital_code,
                   h.name AS RandomHospital,
                   '1' AS patient_operation_source_key
            FROM PatientVisitRecords pvr
            CROSS APPLY (SELECT TOP 1 name FROM ab_hospital ORDER BY NEWID()) h
        ),

        -- Step 6: 合并所有记录
        AllRecords AS (
            SELECT
                v.patient_id,
                v.patient_visit_id,
                v.patient_hospital_visit_id,
                v.patient_hospital_code,
                v.RandomHospital AS patient_hospital_name,
                v.patient_operation_source_key
            FROM VisitRandomFields v
            UNION ALL
            SELECT
                n.patient_id,
                n.patient_visit_id,
                n.patient_hospital_visit_id,
                n.patient_hospital_code,
                n.RandomHospital AS patient_hospital_name,
                n.patient_operation_source_key
            FROM NoVisitRandomFields n
        ),

        -- Step 7: 生成所有字段
        FinalData AS (
            SELECT
                ar.patient_id,
                ar.patient_visit_id,
                ar.patient_hospital_visit_id,
                ar.patient_hospital_code,
                ar.patient_hospital_name,
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(ar.patient_id * 1000 + ar.patient_visit_id)) % 10000000), 7) AS OperationNum,
                RIGHT('0000000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(ar.patient_id * 1000 + ar.patient_visit_id)) % 10000000), 7) AS SourceOperationNum,
                DATEADD(DAY, ABS(CHECKSUM(ar.patient_id * 1000 + ar.patient_visit_id)) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS OperationBeginTime,
                DATEADD(DAY, ABS(CHECKSUM(ar.patient_id * 1000 + ar.patient_visit_id)) % DATEDIFF(DAY, '2022-06-01', GETDATE()) + 1, '2022-06-01') AS OperationEndTime,
                DATEADD(DAY, -ABS(CHECKSUM(ar.patient_id * 1000 + ar.patient_visit_id)) % 365, GETDATE()) AS UpdateTime,
                ABS(CHECKSUM(ar.patient_id * 1000 + ar.patient_visit_id)) % 2 + 1 AS DeleteState,

                -- 随机字段
                ol.n_key AS OperationLevelKey,
                ol.n_value AS OperationLevelValue,
                ot.n_key AS OperationTypeKey,
                ot.n_value AS OperationTypeValue,
                gh.n_key AS IncisionHealingGradeKey,
                gh.n_value AS IncisionHealingGradeValue
            FROM AllRecords ar
            CROSS APPLY (SELECT TOP 1 n_key, n_value FROM ab_operationLevel ORDER BY NEWID()) ol
            CROSS APPLY (SELECT TOP 1 n_key, n_value FROM ab_operationType ORDER BY NEWID()) ot
            CROSS APPLY (SELECT TOP 1 n_key, n_value FROM ab_operationIncisionHealingGrade ORDER BY NEWID()) gh
        )

        -- Step 8: 插入数据（使用 TABLOCKX 提高性能）
        INSERT INTO CDRD_PATIENT_OPERATION_INFO WITH (TABLOCKX) (
            patient_id,
            patient_visit_id,
            patient_hospital_visit_id,
            patient_hospital_code,
            patient_hospital_name,
            patient_operation_num,
            patient_operation_source_num,
            patient_operation_name,
            patient_operation_doc_name,
            patient_operation_assist_I,
            patient_operation_assist_II,
            patient_operation_before_diag,
            patient_operation_during_diag,
            patient_operation_after_diag,
            patient_operation_level_key,
            patient_operation_level_value,
            patient_operation_type_key,
            patient_operation_type_value,
            patient_operation_incision_healing_grade_key,
            patient_operation_incision_healing_grade_value,
            patient_operation_anesthesiologist,
            patient_operation_anesthesia_type,
            patient_operation_step_process,
            patient_operation_begin_time,
            patient_operation_end_time,
            patient_operation_delete_state_key,
            patient_operation_update_time,
            patient_operation_source_key
        )
        SELECT
            fd.patient_id,
            fd.patient_visit_id,
            fd.patient_hospital_visit_id,
            fd.patient_hospital_code,
            fd.patient_hospital_name,
            fd.OperationNum,
            fd.SourceOperationNum,
            '腹腔镜胆囊切除术',
            '主刀/手术者',
            'I助',
            'II助',
            @PreoperativeDiagnosis1,  --术前诊断
            @PreoperativeDiagnosis2,  --术中诊断
            @PreoperativeDiagnosis3,  --术后诊断
            fd.OperationLevelKey,
            fd.OperationLevelValue,
            fd.OperationTypeKey,
            fd.OperationTypeValue,
            fd.IncisionHealingGradeKey,
            fd.IncisionHealingGradeValue,
            '麻醉者张三',
            '全身麻醉（气管插管）',
            @OperationWay,
            fd.OperationBeginTime,
            fd.OperationEndTime,
            fd.DeleteState,
            fd.UpdateTime,
            '1'
        FROM FinalData fd
        ORDER BY fd.patient_id;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
