CREATE OR ALTER PROCEDURE cdrd_patient_info
    @RecordCount INT = 30000 -- 默认插入30000条
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @StartTime DATETIME2 = SYSUTCDATETIME();
    DECLARE @BatchSize INT = 1; -- 每次插入5000条
    DECLARE @Inserted INT = 0;

    -- 定义局部变量用于子程序返回值
    DECLARE
        @FullName NVARCHAR(50),
        @provinceKey NVARCHAR(150), @province NVARCHAR(150),
        @cityKey NVARCHAR(150), @city NVARCHAR(150),
        @countyKey NVARCHAR(150), @county NVARCHAR(150),
        @nationKey NVARCHAR(50), @nation NVARCHAR(50),
        @marriageKey NVARCHAR(50), @marriage NVARCHAR(50),
        @job NVARCHAR(50),
        @certTypeKey NVARCHAR(50), @certTypeValue NVARCHAR(50),
        @relation NVARCHAR(50),
        @address1 NVARCHAR(150), @address2 NVARCHAR(150),
        @idcard NVARCHAR(18), @gender NVARCHAR(10), @genderKey NVARCHAR(10),
        @birthday NVARCHAR(18), @age NVARCHAR(150),
        @phone1 NVARCHAR(11), @phone2 NVARCHAR(11), @phone3 NVARCHAR(8);

    WHILE @Inserted < @RecordCount
    BEGIN
        BEGIN TRANSACTION;

        -- 获取随机数据
--         EXEC p_name @FullName = @FullName OUTPUT;
--         EXEC p_birth_place
--             @provinceKey = @provinceKey OUTPUT,
--             @province = @province OUTPUT,
--             @cityKey = @cityKey OUTPUT,
--             @city = @city OUTPUT,
--             @countyKey = @countyKey OUTPUT,
--             @county = @county OUTPUT;
--         EXEC p_nationality @k = @nationKey OUTPUT, @v = @nation OUTPUT;
--         EXEC p_marriage @k = @marriageKey OUTPUT, @v = @marriage OUTPUT;
--         EXEC p_job @v = @job OUTPUT;
--         EXEC p_cert_type @k = @certTypeKey OUTPUT, @v = @certTypeValue OUTPUT;
--         EXEC p_patient_relation @v = @relation OUTPUT;
--         EXEC p_address @v1 = @address1 OUTPUT, @v2 = @address2 OUTPUT;
--         EXEC p_idcard
--             @countyKey = @countyKey,
--             @idcard = @idcard OUTPUT,
--             @gender = @gender OUTPUT,
--             @genderKey = @genderKey OUTPUT,
--             @birthday = @birthday OUTPUT,
--             @age = @age OUTPUT;

        -- 随机电话生成
        SELECT
            @phone1 = '138' + RIGHT('00000000' + CAST(ABS(CHECKSUM(NEWID())) % 99999999 AS VARCHAR(8)), 8),
            @phone2 = '130' + RIGHT('00000000' + CAST(ABS(CHECKSUM(NEWID())) % 99999999 AS VARCHAR(8)), 8),
            @phone3 = '5' + RIGHT('0000000' + CAST(ABS(CHECKSUM(NEWID())) % 9999999 AS VARCHAR(7)), 7);

        -- 批量插入主表
        INSERT INTO a_cdrd_patient_info (
            patient_name, patient_sex_key, patient_sex_value, patient_birth_date, patient_age,
            patient_birth_address_province_key, patient_birth_address_province,
            patient_birth_address_city_key, patient_birth_address_city,
            patient_birth_address_country_key, patient_birth_address_country,
            patient_country,
            patient_native_province_key, patient_native_province,
            patient_native_city_key, patient_native_city,
            patient_nation_key, patient_nation_value,
            patient_phone_num, patient_home_address,
            patient_profession,
            patient_marriage_key, patient_marriage_value,
            patient_id_type_key, patient_id_type_value,
            patient_id_num,
            patient_home_phone,
            patient_account_address,
            patient_contact_name, patient_contact_relation, patient_contact_phone, patient_contact_address,
            patient_update_time, patient_data_source_key
        )
        SELECT TOP (@BatchSize)
--         SELECT TOP 1
--             dbo.fn_name(),
            dbo.fn_name('M'),
--             @FullName + RIGHT('000' + CAST(ABS(CHECKSUM(NEWID())) % 999 AS NVARCHAR(3)), 3),
            @genderKey, @gender,
            @birthday, @age,
            @provinceKey, @province,
            @cityKey, @city,
            @countyKey, @county,
            N'中国', 
            @provinceKey, @province,
            @cityKey, @city,
            @nationKey, @nation,
            @phone1,
            @address1,
            @job,
            @marriageKey, @marriage,
            @certTypeKey, N'身份证号',
            @idcard,
            @phone3,
            @address1,
            @FullName + RIGHT('000' + CAST(ABS(CHECKSUM(NEWID())) % 999 AS NVARCHAR(3)), 3),
            @relation,
            @phone2,
            @address2,
            DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()),
            ABS(CHECKSUM(NEWID())) % 2 + 1
        FROM sys.all_objects ao
        WHERE name IS NOT NULL;

        SET @Inserted = @Inserted + @@ROWCOUNT;

        COMMIT TRANSACTION;

        WAITFOR DELAY '00:00:01';
    END

    -- 输出总耗时
    DECLARE @DurationMs INT = DATEDIFF(MILLISECOND, @StartTime, SYSUTCDATETIME());
    PRINT CONCAT('成功插入 ', @RecordCount, ' 条记录，总耗时：', @DurationMs, ' 毫秒');
END
