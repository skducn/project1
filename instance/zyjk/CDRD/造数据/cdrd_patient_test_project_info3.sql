-- todo 检查项目明细(造数据)
-- 数据量：每个实验室检查记录对应一份检查项目明细(每份明细预计20条左右数据，总量预计300万左右)
-- 100w, 耗时: 1127.5087 秒, 114,237,440
CREATE OR ALTER PROCEDURE cdrd_patient_test_project_info
    @RecordCount INT = 20,
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    -- 获取实验室检查报告记录数，用于输出计算
    DECLARE @re INT = 1;
    select @re = count(*) from a_cdrd_patient_lab_examination_info;
    SET @result = @re * @RecordCount;

    DECLARE @Counter1 INT = 1;
    -- 获取实验室检查报告记录数

    -- 创建一个临时表用于存储20组固定数据
    DECLARE @TestData TABLE (
        ID INT IDENTITY(1,1),
        report_id INT,
        report_name NVARCHAR(255),
        patient_test_item_name NVARCHAR(255),
        patient_test_numerical_value NVARCHAR(50),
        patient_test_unit_name NVARCHAR(50),
        patient_test_text_value NVARCHAR(50),
        patient_test_abnormal_flag NVARCHAR(50),
        patient_test_reference_range NVARCHAR(50)
    );

    -- 插入20组固定数据(血生化检测,凝血功能检验), 需要与实验室检查报告中报告名称一一对应
    INSERT INTO @TestData (report_id, report_name, patient_test_item_name, patient_test_numerical_value, patient_test_unit_name, patient_test_text_value, patient_test_abnormal_flag, patient_test_reference_range)
    VALUES
    (1, '血生化检测','空腹血糖（GLU）', '5.8', 'mmol/L', '正常', '', '3.9-6.1'),
    (2, '血生化检测','糖化血红蛋白（HbA1c）', '6.2', '%', '升高', '异常', '<6.0'),
    (3, '血生化检测','总胆固醇（TC）', '5.9', 'mmol/L', '升高', '异常', '<5.2'),
    (4, '血生化检测','甘油三酯（TG）', '2.3', 'mmol/L', '升高', '异常', '<1.7'),
    (5, '血生化检测','低密度脂蛋白（LDL-C）', '3.8', 'mmol/L', '升高', '异常', '<3.4'),
    (6, '血生化检测','高密度脂蛋白（HDL-C）', '1.1', 'mmol/L', '正常', '', '>=1.0'),
    (7, '血生化检测','血肌酐（Cr）', '78', 'mmol/L', '正常', '', '59-104'),
    (8, '血生化检测','尿素氮（BUN）', '5.6', 'mmol/L', '正常', '', '2.9-8.2'),
    (9, '血生化检测','估算 eGFR', '88', 'mL/min/1.73m2', '正常', '', '>=90'),
    (10, '血生化检测','血尿酸（UA）', '420', 'mmol/L', '升高', '异常', '208-428（男性）'),
    (11, '血生化检测','血钾（K+）', '3.9', 'mmol/L', '正常', '', '3.5-5.3'),
    (12, '血生化检测','血钠（Na+）', '140', 'mmol/L', '正常', '', '137-147'),
    (13, '血生化检测','血氯（Cl-）', '102', 'mmol/L', '正常', '', '99-110'),
    (14, '血生化检测','丙氨酸氨基转移酶（ALT）', '28', 'U/L', '正常', '', '9-50'),
    (15, '血生化检测','天门冬氨酸氨基转移酶（AST）', '25', 'U/L', '正常', '', '15-40'),
    (16, '血生化检测','总蛋白（TP）', '72', 'g/L', '正常', '', '65-85'),
    (17, '血生化检测','白蛋白（ALB）', '45', 'g/L', '正常', '', '40-55'),
    (18, '血生化检测','同型半胱氨酸（Hcy）', '16.5', 'mmol/L', '升高', '异常', '<15'),
    (19, '血生化检测','乳酸脱氢酶（LDH）', '220', 'U/L', '正常', '', '120-250'),
    (20, '血生化检测','C 反应蛋白（CRP）', '8', 'mg/L', '升高', '异常', '<5.0'),
    (1, '凝血功能检验','凝血酶原时间（PT）', '13.5', '秒', '正常', '', '11.0-14.5'),
    (2, '凝血功能检验','活化部分凝血活酶时间（APTT）', '38', '秒', '延长', '异常', '25.0-35.0'),
    (3, '凝血功能检验','国际标准化比值（INR）', '1.15', '-', '正常', '', '0.8-1.2'),
    (4, '凝血功能检验','纤维蛋白原（FIB）', '3.2', 'g/L', '正常', '', '2.0-4.0'),
    (5, '凝血功能检验','D - 二聚体（D-Dimer）', '0.8', 'mg/L', '升高', '异常', '<0.5'),
    (6, '凝血功能检验','抗凝血酶 Ⅲ（AT-Ⅲ）活性', '85', '%', '正常', '', '80-120'),
    (7, '凝血功能检验','血小板计数（PLT）', '210', 'X109/L', '正常', '', '125-350'),
    (8, '凝血功能检验','肌钙蛋白 I（cTnI）', '0.02', 'ug/L', '正常', '', '<0.04'),
    (9, '凝血功能检验','N 末端脑钠肽前体（NT-proBNP）', '450', 'pg/mL', '升高', '异常', '<125'),
    (10, '凝血功能检验','血钾（K+）', '3.9', 'mmol/L', '正常', '', '3.5-5.3'),
    (11, '凝血功能检验','血镁（Mg2+）', '0.75', 'mmol/L', '降低', '异常', '0.7-1.1'),
    (12, '凝血功能检验','甲状腺功能（TSH）', '0.1', 'mIU/L', '降低', '异常', '0.27-4.2'),
    (13, '凝血功能检验','游离甲状腺素（FT4）', '25', 'pmol/L', '升高', '异常', '12.0-22.0'),
    (14, '凝血功能检验','肝功能（ALT）', '32', 'U/L', '正常', '', '9-50'),
    (15, '凝血功能检验','肾功能（eGFR）', '68', 'mL/min', '降低', '异常', '>=90'),
    (16, '凝血功能检验','血尿酸（UA）', '480', 'umol/L', '升高', '异常', '208-428'),
    (17, '凝血功能检验','同型半胱氨酸（Hcy）', '18.5', 'umol/L', '升高', '异常', '<15'),
    (18, '凝血功能检验','糖化血红蛋白（HbA1c）', '6.2', '%', '升高', '异常', '<6.0'),
    (19, '凝血功能检验','C 反应蛋白（CRP）', '8', 'mg/L', '升高', '异常', '<5.0'),
    (20, '凝血功能检验','乳酸脱氢酶（LDH）', '220', 'U/L', '正常', '', '120-250');


    -- 遍历实验室检查报告表 a_cdrd_patient_lab_examination_info
    WHILE @Counter1 <= @re
    BEGIN

        -- 循环插入指定数量的记录
        BEGIN

            -- 按照记录顺序 获取 实验室检查ID，报告编号，报告名称
            DECLARE @j INT = 1;
            DECLARE @patient_visit_id INT;
            DECLARE @patient_superior_examination_id INT;
            DECLARE @patient_lab_examination_report_num NVARCHAR(50);
            DECLARE @patient_lab_examination_report_name NVARCHAR(150);

            SELECT @patient_visit_id = patient_visit_id,
                   @patient_superior_examination_id = patient_lab_examination_id,
                   @patient_lab_examination_report_num = patient_lab_examination_report_num,
                   @patient_lab_examination_report_name = patient_lab_examination_report_name
            FROM (
                SELECT
                    patient_visit_id,patient_lab_examination_id, patient_lab_examination_report_num,patient_lab_examination_report_name,
                    ROW_NUMBER() OVER (ORDER BY patient_lab_examination_id) AS row_num
                FROM a_cdrd_patient_lab_examination_info
            ) AS subquery
            WHERE row_num = @Counter1;

            -- 执行 20 次
            WHILE @j <= @RecordCount
            BEGIN

                -- 获取当前行的数据
                DECLARE @patient_test_item_name NVARCHAR(255);
                DECLARE @patient_test_numerical_value NVARCHAR(50);
                DECLARE @patient_test_unit_name NVARCHAR(50);
                DECLARE @patient_test_text_value NVARCHAR(50);
                DECLARE @patient_test_abnormal_flag NVARCHAR(50);
                DECLARE @patient_test_reference_range NVARCHAR(50);

                SELECT
                    @patient_test_item_name = patient_test_item_name,
                    @patient_test_numerical_value = patient_test_numerical_value,
                    @patient_test_unit_name = patient_test_unit_name,
                    @patient_test_text_value = patient_test_text_value,
                    @patient_test_abnormal_flag = patient_test_abnormal_flag,
                    @patient_test_reference_range = patient_test_reference_range
                FROM @TestData
                WHERE report_id = @j and report_name = @patient_lab_examination_report_name;

                -- 插入单条随机数据
                INSERT INTO a_cdrd_patient_test_project_info (patient_superior_examination_id,patient_superior_examination_type,patient_report_num,patient_test_item_name,patient_test_numerical_value,patient_test_unit_name,patient_test_text_value,patient_test_abnormal_flag,patient_test_reference_range,patient_test_delete_state_key,patient_test_update_time,patient_test_data_source_key)
                VALUES (
                    @patient_superior_examination_id, -- 上级检查ID (取值实验室检查ID或者辅助检查ID)
                    '1', -- 如果是实验室检查则默认为1，如果是辅助检查则默认为2
                    @patient_lab_examination_report_num, -- 报告编号
                    @patient_test_item_name, -- 项目名称
                    @patient_test_numerical_value, -- 定量结果
                    @patient_test_unit_name, -- 定量结果单位
                    @patient_test_text_value, -- 定性结果
                    @patient_test_abnormal_flag, -- 异常标识
                    @patient_test_reference_range, -- 参考值（范围）
                    ABS(CHECKSUM(NEWID())) % 2 + 1,  -- 删除状态1或2
                    DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                    ISNULL(CASE WHEN @patient_visit_id IS NULL THEN 2 ELSE 1 END, 2) --有就诊记录ID默认为“1”，没有的默认为“2”
                );

                SET @j = @j + 1;
            END

        END;

    SET @Counter1 = @Counter1 + 1;
    END;

END