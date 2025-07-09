-- todo 医疗组人员表(造数据)

CREATE OR ALTER PROCEDURE sys_dept_medgp_person
    @RecordCount INT = 10 -- 可通过参数控制记录数，默认100条
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

            -- 子存储过程
            -- 姓名
            DECLARE @RandomName NVARCHAR(50);
            EXEC p_name @FullName = @RandomName OUTPUT;

            DECLARE @RandomDepartment_treat_group_id int;
            SELECT TOP 1 @RandomDepartment_treat_group_id = department_treat_group_id FROM a_sys_dept_medgp ORDER BY NEWID();

            -- 插入单条随机数据
            INSERT INTO a_sys_dept_medgp_person (user_id, department_treat_group_id, user_name, user_job_num)
            VALUES (
                    CAST(ABS(CHECKSUM(NEWID())) % 10000 AS int),   -- 用户ID
                    @RandomDepartment_treat_group_id,   -- 治疗组ID
                    @RandomName + RIGHT('000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 1000), 3), -- 姓名 + 固定3位数
                    CAST(ABS(CHECKSUM(NEWID())) % 100000 AS NVARCHAR(10)) -- 工号
            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_sys_dept_medgp_person);
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