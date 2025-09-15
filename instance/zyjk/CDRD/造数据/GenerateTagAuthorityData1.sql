-- 创建存储过程用于生成标签权限数据
CREATE OR ALTER PROCEDURE GenerateTagAuthorityData1
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        -- 检查源表是否有数据
        DECLARE @DeptCount INT, @TagCount INT;
        SELECT @DeptCount = COUNT(*) FROM sys_dept_medgp;
        SELECT @TagCount = COUNT(*) FROM sys_tag_type WHERE category_key = 'cdrd_patient_info';

        PRINT 'sys_dept_medgp 表记录数: ' + CAST(@DeptCount AS VARCHAR(10));
        PRINT 'sys_tag_type 表记录数 (category_key=''cdrd_patient_info''): ' + CAST(@TagCount AS VARCHAR(10));

        IF @DeptCount = 0 OR @TagCount = 0
        BEGIN
            PRINT '源表数据为空，无法生成数据';
            RETURN;
        END

        BEGIN TRANSACTION;

        -- 使用表变量存储中间结果以提高效率
        DECLARE @TempTagAuthority TABLE (
            tag_id INT,
            authority_relative_module NVARCHAR(20),
            authority_relative_id INT
        );

        -- 插入数据到表变量
        -- 实现 authority_relative_id 与 tag_id 的一对多关系
        -- 每个 DEPARTMENT_TREAT_GROUP_ID 对应所有符合条件的 tag_id
        INSERT INTO @TempTagAuthority (tag_id, authority_relative_module, authority_relative_id)
        SELECT
            st.tag_id,
            'sys_dept_medgp' AS authority_relative_module,
            sdm.DEPARTMENT_TREAT_GROUP_ID AS authority_relative_id
        FROM sys_dept_medgp sdm
        CROSS JOIN sys_tag_type st
        WHERE st.category_key = 'cdrd_patient_info'
        -- 确保只处理有效的非空ID
        AND sdm.DEPARTMENT_TREAT_GROUP_ID IS NOT NULL
        AND st.tag_id IS NOT NULL;

        -- 检查表变量是否有数据
        DECLARE @TempCount INT;
        SELECT @TempCount = COUNT(*) FROM @TempTagAuthority;
        PRINT '中间数据条数: ' + CAST(@TempCount AS VARCHAR(10));

        -- 显示关系统计信息
        DECLARE @UniqueAuthorityIds INT, @UniqueTagIds INT;
        SELECT @UniqueAuthorityIds = COUNT(DISTINCT authority_relative_id) FROM @TempTagAuthority;
        SELECT @UniqueTagIds = COUNT(DISTINCT tag_id) FROM @TempTagAuthority;

        PRINT '唯一的 authority_relative_id 数量: ' + CAST(@UniqueAuthorityIds AS VARCHAR(10));
        PRINT '唯一的 tag_id 数量: ' + CAST(@UniqueTagIds AS VARCHAR(10));
        PRINT '每个 authority_relative_id 平均对应的 tag_id 数量: ' +
              CAST(CAST(@TempCount AS FLOAT) / CASE WHEN @UniqueAuthorityIds = 0 THEN 1 ELSE @UniqueAuthorityIds END AS VARCHAR(10));

        IF @TempCount = 0
        BEGIN
            PRINT '没有符合条件的数据';
            COMMIT TRANSACTION;
            RETURN;
        END

        -- 批量插入到目标表sys_tag_authority1
        INSERT INTO sys_tag_authority1 (tag_id, authority_relative_module, authority_relative_id)
        SELECT
            tag_id,
            authority_relative_module,
            authority_relative_id
        FROM @TempTagAuthority
        ORDER BY authority_relative_id, tag_id; -- 按照关联关系排序，提高查询性能

        -- 获取插入的行数
        DECLARE @RowCount INT = @@ROWCOUNT;

        COMMIT TRANSACTION;

        PRINT '数据插入完成，共插入 ' + CAST(@RowCount AS VARCHAR(10)) + ' 条记录';
        PRINT '实现了一对多关系: 每个 authority_relative_id 对应多个 tag_id';

    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
        DECLARE @ErrorState INT = ERROR_STATE();

        PRINT '发生错误: ' + @ErrorMessage;
        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END;

-- 执行存储过程
-- EXEC GenerateTagAuthorityData;
