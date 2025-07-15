-- todo 科室表(造数据)

CREATE OR ALTER PROCEDURE sys_department
    @RecordCount INT = 4 -- 可通过参数控制记录数，默认100条
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
            -- 科室
            DECLARE @RandomDepartment NVARCHAR(50);
            EXEC p_dept @v = @RandomDepartment OUTPUT;

            -- 姓名
            DECLARE @RandomName NVARCHAR(50);
            EXEC p_name @FullName = @RandomName OUTPUT;


            -- 插入单条随机数据
            INSERT INTO a_sys_department (department_name, department_code, department_charge_id, department_charge_job_num,
            department_charge_name,department_creater_name,department_create_time)
            VALUES (
                @RandomDepartment + RIGHT('0000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 10000), 4), -- 科室名称 + 固定4位数
                RIGHT('0000000' + CAST(ABS(CHECKSUM(NEWID())) % 10000000 AS VARCHAR(20)), 7), -- 科室编码
                CAST(ABS(CHECKSUM(NEWID())) % 10000 AS int), -- 科室负责人ID
                CAST(ABS(CHECKSUM(NEWID())) % 10000 AS NVARCHAR(10)), -- 科室负责人工号
                @RandomName + RIGHT('00000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 100000), 5), -- 科室负责人姓名 + 固定5位数
                @RandomName, -- 创建人
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()) -- 创建时间
            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_sys_department);
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