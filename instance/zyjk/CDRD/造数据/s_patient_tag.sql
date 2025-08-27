-- todo 标签表
-- 每个患者信息4条标签，即3万*4 = 12万
-- 每条就诊记录2条标签，即15万*2 = 30万

CREATE OR ALTER PROCEDURE GeneratePatientTagRecords
-- 创建生成标签记录的存储过程
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        -- 创建临时表存储标签类型和标签数据的映射关系
        CREATE TABLE #TagTypeMapping (
            category_key VARCHAR(50),
            tag_id INT,
            tag_key VARCHAR(100),
            tag_data_id INT,
            tag_data_key VARCHAR(100),
            row_num INT
        );

        -- 插入患者基本信息标签类型映射（每个标签类型取前4个数据）
        INSERT INTO #TagTypeMapping (category_key, tag_id, tag_key, tag_data_id, tag_data_key, row_num)
        SELECT
            st.category_key,
            st.tag_id,
            st.tag_key,
            sd.tag_data_id,
            sd.tag_data_key,
            ROW_NUMBER() OVER (PARTITION BY st.tag_id ORDER BY sd.tag_data_id) as row_num
        FROM sys_tag_type st
        INNER JOIN sys_tag_data sd ON st.tag_id = sd.tag_id
        WHERE st.category_key = 'cdrd_patient_info';

        -- 插入就诊信息标签类型映射（每个标签类型取前2个数据）
        INSERT INTO #TagTypeMapping (category_key, tag_id, tag_key, tag_data_id, tag_data_key, row_num)
        SELECT
            st.category_key,
            st.tag_id,
            st.tag_key,
            sd.tag_data_id,
            sd.tag_data_key,
            ROW_NUMBER() OVER (PARTITION BY st.tag_id ORDER BY sd.tag_data_id) as row_num
        FROM sys_tag_type st
        INNER JOIN sys_tag_data sd ON st.tag_id = sd.tag_id
        WHERE st.category_key = 'cdrd_patient_visit_info';

        -- 获取患者基本信息数量
        DECLARE @PatientCount INT;
        SELECT @PatientCount = COUNT(*) FROM cdrd_patient_info;
        IF @PatientCount > 30000 SET @PatientCount = 30000;

        -- 获取就诊信息数量
        DECLARE @VisitCount INT;
        SELECT @VisitCount = COUNT(*) FROM cdrd_patient_visit_info;
        IF @VisitCount > 150000 SET @VisitCount = 150000;

        -- 为cdrd_patient_info表中的每个患者生成4条标签记录（总共12万条）
        INSERT INTO patient_tag (
            category_key,
            category_source_id,
            tag_id,
            tag_key,
            tag_data_id,
            tag_data_key,
            create_time,
            update_time
        )
        SELECT TOP (@PatientCount * 4)
            'cdrd_patient_info' AS category_key,
            p.patient_id AS category_source_id,
            ttm.tag_id,
            ttm.tag_key,
            ttm.tag_data_id,
            ttm.tag_data_key,
            GETDATE() AS create_time,
            GETDATE() AS update_time
        FROM (
            SELECT TOP (@PatientCount) patient_id
            FROM cdrd_patient_info
            ORDER BY patient_id
        ) p
        CROSS JOIN (
            SELECT tag_id, tag_key, tag_data_id, tag_data_key
            FROM #TagTypeMapping
            WHERE category_key = 'cdrd_patient_info' AND row_num <= 4
        ) ttm
        ORDER BY p.patient_id;

        -- 为cdrd_patient_visit_info表中的每条就诊记录生成2条标签记录（总共30万条）
        INSERT INTO patient_tag (
            category_key,
            category_source_id,
            tag_id,
            tag_key,
            tag_data_id,
            tag_data_key,
            create_time,
            update_time
        )
        SELECT TOP (@VisitCount * 2)
            'cdrd_patient_visit_info' AS category_key,
            v.patient_visit_id AS category_source_id,
            ttm.tag_id,
            ttm.tag_key,
            ttm.tag_data_id,
            ttm.tag_data_key,
            GETDATE() AS create_time,
            GETDATE() AS update_time
        FROM (
            SELECT TOP (@VisitCount) patient_visit_id
            FROM cdrd_patient_visit_info
            ORDER BY patient_visit_id
        ) v
        CROSS JOIN (
            SELECT tag_id, tag_key, tag_data_id, tag_data_key
            FROM #TagTypeMapping
            WHERE category_key = 'cdrd_patient_visit_info' AND row_num <= 2
        ) ttm
        ORDER BY v.patient_visit_id;

        -- 删除临时表
        DROP TABLE #TagTypeMapping;

        COMMIT TRANSACTION;

        PRINT '标签记录生成完成';
        PRINT '患者基本信息标签记录数: ' + CAST((SELECT COUNT(*) FROM patient_tag WHERE category_key = 'cdrd_patient_info') AS VARCHAR(10));
        PRINT '就诊信息标签记录数: ' + CAST((SELECT COUNT(*) FROM patient_tag WHERE category_key = 'cdrd_patient_visit_info') AS VARCHAR(10));
        PRINT '总标签记录数: ' + CAST((SELECT COUNT(*) FROM patient_tag) AS VARCHAR(10));

    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
        DECLARE @ErrorState INT = ERROR_STATE();

        PRINT '生成标签记录时发生错误: ' + @ErrorMessage;
        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END
