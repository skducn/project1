
-- 创建生成patient_tag数据的存储过程
CREATE OR ALTER PROCEDURE GeneratePatientTagData
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    SET @result = 5


    -- 创建临时表提高插入效率
    CREATE TABLE #TempPatientTag (
        tag_record_id BIGINT IDENTITY(1,1) PRIMARY KEY,
        category_source_id INT,
        category_key NVARCHAR(100),
        category_id INT,
        tag_id INT,
        tag_key NVARCHAR(100),
        tag_data_id INT,
        tag_data_key NVARCHAR(100),
        create_id INT,
        create_by NVARCHAR(20),
        create_time DATETIME
    );

    -- 为临时表创建索引提高性能
    CREATE NONCLUSTERED INDEX IX_TempPatientTag_CategoryKey ON #TempPatientTag(category_key);
    CREATE NONCLUSTERED INDEX IX_TempPatientTag_CategorySourceId ON #TempPatientTag(category_source_id);

    -- 处理cdrd_patient_info类别
    -- 每个患者生成4条标签记录
    INSERT INTO #TempPatientTag (
        category_source_id,
        category_key,
        category_id,
        tag_id,
        tag_key,
        tag_data_id,
        tag_data_key,
        create_id,
        create_by,
        create_time
    )
    SELECT
        p.patient_id AS category_source_id,
        'cdrd_patient_info' AS category_key,
        p.patient_id AS category_id,
        st.tag_id,
        st.tag_key,
        sd.tag_data_id,
        sd.tag_data_key,
        11 AS create_id,
        'tester11' AS create_by,
        GETDATE() AS create_time
    FROM cdrd_patient_info_5 p
    CROSS JOIN (
        SELECT TOP 4 tag_id, tag_key
        FROM sys_tag_type
        WHERE category_key = 'cdrd_patient_info' AND status = '0'
        ORDER BY tag_id
    ) st
    LEFT JOIN (
        SELECT
            tag_id,
            tag_data_id,
            tag_data_key,
            ROW_NUMBER() OVER (PARTITION BY tag_id ORDER BY tag_data_id) as rn
        FROM sys_tag_data
    ) sd ON st.tag_id = sd.tag_id AND sd.rn = 1; -- 每个tag_id只取一条数据

    -- 处理cdrd_patient_visit_info类别
    -- 每条就诊记录生成2条标签记录
    INSERT INTO #TempPatientTag (
        category_source_id,
        category_key,
        category_id,
        tag_id,
        tag_key,
        tag_data_id,
        tag_data_key,
        create_id,
        create_by,
        create_time
    )
    SELECT
        pv.patient_visit_id AS category_source_id,
        'cdrd_patient_visit_info' AS category_key,
        pv.patient_visit_id AS category_id,
        st.tag_id,
        st.tag_key,
        sd.tag_data_id,
        sd.tag_data_key,
        11 AS create_id,
        'tester11' AS create_by,
        GETDATE() AS create_time
    FROM cdrd_patient_visit_info_5 pv
    CROSS JOIN (
        SELECT TOP 2 tag_id, tag_key
        FROM sys_tag_type
        WHERE category_key = 'cdrd_patient_visit_info' AND status = '0'
        ORDER BY tag_id
    ) st
    LEFT JOIN (
        SELECT
            tag_id,
            tag_data_id,
            tag_data_key,
            ROW_NUMBER() OVER (PARTITION BY tag_id ORDER BY tag_data_id) as rn
        FROM sys_tag_data
    ) sd ON st.tag_id = sd.tag_id AND sd.rn = 1; -- 每个tag_id只取一条数据

    -- 将临时表数据插入到正式表中
    INSERT INTO patient_tag (
        tag_record_id,
        category_source_id,
        category_key,
        category_id,
        tag_id,
        tag_key,
        tag_data_id,
        tag_data_key,
        create_id,
        create_by,
        create_time
    )
    SELECT
        tag_record_id,
        category_source_id,
        category_key,
        category_id,
        tag_id,
        tag_key,
        tag_data_id,
        tag_data_key,
        create_id,
        create_by,
        create_time
    FROM #TempPatientTag
    ORDER BY tag_record_id;

    -- 输出统计信息
    DECLARE @RowCount INT = (SELECT COUNT(*) FROM #TempPatientTag);
    PRINT 'Generated ' + CAST(@RowCount AS NVARCHAR(20)) + ' patient tag records';

    -- 清理临时对象
    DROP TABLE #TempPatientTag;
END
