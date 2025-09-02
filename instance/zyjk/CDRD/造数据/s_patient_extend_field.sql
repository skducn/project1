-- 创建生成patient_extend_field数据的存储过程
-- 15W * 6
-- 耗时: 17.5686 秒
CREATE OR ALTER PROCEDURE s_patient_extend_field
    @result INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET @result = 900000

    -- 创建临时表提高插入效率
    CREATE TABLE #TempPatientExtendField (
        category_source_id INT,
        category_key NVARCHAR(100),
        category_id INT,
        extend_field_id INT,
        extend_field_key NVARCHAR(100),
        extend_field_text NVARCHAR(MAX),
        create_id INT,
        create_by NVARCHAR(20),
        create_time DATETIME
    );

    -- 为临时表创建索引提高性能
    CREATE NONCLUSTERED INDEX IX_TempPatientExtendField_Category
    ON #TempPatientExtendField(category_key, category_source_id);

    -- 生成患者扩展字段数据
    -- 每次就诊关联所有cdrd_patient_visit_info类型的扩展字段
    INSERT INTO #TempPatientExtendField (
        category_source_id,
        category_key,
        category_id,
        extend_field_id,
        extend_field_key,
        extend_field_text,
        create_id,
        create_by,
        create_time
    )
    SELECT
        pv.patient_id AS category_source_id,
        'cdrd_patient_visit_info' AS category_key,
        pv.patient_visit_id AS category_id,
        sef.extend_field_id,
        sef.extend_field_key,
        CAST(ABS(CHECKSUM(NEWID()) % 100000 + 1) AS NVARCHAR(10)) AS extend_field_text,
        11 AS create_id,
        'tester11' AS create_by,
        GETDATE() AS create_time
    FROM cdrd_patient_visit_info pv
    CROSS JOIN sys_extend_field_manage sef
    WHERE sef.category_key = 'cdrd_patient_visit_info'
      AND sef.status = '0';  -- 假设启用状态为'0'

    -- 将临时表数据插入到正式表中
    INSERT INTO patient_extend_field (
        category_source_id,
        category_key,
        category_id,
        extend_field_id,
        extend_field_key,
        extend_field_text,
        create_id,
        create_by,
        create_time
    )
    SELECT
        category_source_id,
        category_key,
        category_id,
        extend_field_id,
        extend_field_key,
        extend_field_text,
        create_id,
        create_by,
        create_time
    FROM #TempPatientExtendField
    ORDER BY category_source_id, category_id, extend_field_id;

    -- 输出统计信息
    DECLARE @TotalCount INT = (SELECT COUNT(*) FROM #TempPatientExtendField);
    DECLARE @DistinctVisits INT = (SELECT COUNT(DISTINCT category_id) FROM #TempPatientExtendField);
    DECLARE @DistinctFields INT = (SELECT COUNT(DISTINCT extend_field_id) FROM #TempPatientExtendField);

    PRINT 'Generated ' + CAST(@TotalCount AS NVARCHAR(20)) + ' patient extend field records';
    PRINT '  - Distinct visits: ' + CAST(@DistinctVisits AS NVARCHAR(20));
    PRINT '  - Distinct field types: ' + CAST(@DistinctFields AS NVARCHAR(20));

    -- 清理临时对象
    DROP TABLE #TempPatientExtendField;
END
