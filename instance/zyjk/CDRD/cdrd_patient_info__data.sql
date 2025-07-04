CREATE OR ALTER PROCEDURE cdrd_patient_info__data
    @RecordCount INT = 1 -- 可通过参数控制记录数，默认100条
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

            -- 随机手机号
            DECLARE @phone1 NVARCHAR(11);
            DECLARE @phone2 NVARCHAR(11);
            DECLARE @phone3 NVARCHAR(8);
            SELECT @phone1 = '138' + RIGHT('00000000' + CAST(ABS(CHECKSUM(NEWID())) % 99999999 AS VARCHAR(8)), 8);
            SELECT @phone2 = '130' + RIGHT('00000000' + CAST(ABS(CHECKSUM(NEWID())) % 99999999 AS VARCHAR(8)), 8);
            SELECT @phone3 = '5' + RIGHT('0000000' + CAST(ABS(CHECKSUM(NEWID())) % 9999999 AS VARCHAR(7)), 7);

            -- 存储过程
            -- 姓名
            DECLARE @RandomName NVARCHAR(50);
            EXEC p_gen_names @FullName = @RandomName OUTPUT;

            -- 婚姻
            DECLARE @RandomMarriageKey NVARCHAR(50), @RandomMarriage NVARCHAR(50);
            EXEC p_marriage @k = @RandomMarriageKey OUTPUT, @v = @RandomMarriage OUTPUT;

            -- 职业
            DECLARE @RandomJob NVARCHAR(50);
            EXEC p_job @v = @RandomJob OUTPUT;

            -- 证件类型
            DECLARE @RandomIdtypeKey NVARCHAR(50), @RandomIdtype NVARCHAR(50);
            EXEC p_cert_type @k = @RandomIdtypeKey OUTPUT, @v = @RandomIdtype OUTPUT;

            -- 民族
            DECLARE @RandomNationKey NVARCHAR(50), @RandomNation NVARCHAR(50);
            EXEC p_nationality @k = @RandomNationKey OUTPUT, @v = @RandomNation OUTPUT;

            -- 与患者关系
            DECLARE @RandomRelation NVARCHAR(50);
            EXEC p_patient_relation @v = @RandomRelation OUTPUT;

            -- 住址
            DECLARE @RandomAddress1 NVARCHAR(150), @RandomAddress2 NVARCHAR(150);
            EXEC p_address @v1 = @RandomAddress1 OUTPUT, @v2 = @RandomAddress2 OUTPUT;

            -- 出生地
            DECLARE @provinceKey NVARCHAR(150), @province NVARCHAR(150);
            DECLARE @cityKey NVARCHAR(150), @city NVARCHAR(150);
            DECLARE @countyKey NVARCHAR(150), @county NVARCHAR(150);
            EXEC p_birth_place @provinceKey = @provinceKey OUTPUT, @province = @province OUTPUT,
                @cityKey = @cityKey OUTPUT, @city = @city OUTPUT,
                @countyKey = @countyKey OUTPUT, @county = @county OUTPUT;

            -- 身份证，性别，性别key，出生日期,年龄
            DECLARE @idcard NVARCHAR(18), @gender NVARCHAR(10);
            DECLARE @genderKey NVARCHAR(10), @birthday NVARCHAR(18), @age NVARCHAR(150);
            EXEC p_idcard @countyKey = @countyKey, @idcard = @idcard OUTPUT, @gender = @gender OUTPUT,
                 @genderKey = @genderKey OUTPUT, @birthday = @birthday OUTPUT,
                 @age = @age OUTPUT;



            -- 插入单条随机数据
            INSERT INTO a_cdrd_patient_info (patient_name,patient_sex_key,patient_sex_value,patient_birth_date,patient_age,patient_birth_address_province_key,patient_birth_address_province,patient_birth_address_city_key,patient_birth_address_city,patient_birth_address_country_key,patient_birth_address_country,patient_country,patient_native_province_key,patient_native_province,patient_native_city_key,patient_native_city,patient_nation_key,patient_nation_value,patient_phone_num,patient_home_address,patient_profession,patient_marriage_key,patient_marriage_value,patient_id_type_key,patient_id_type_value,patient_id_num,patient_home_phone,patient_account_address,patient_contact_name,patient_contact_relation,patient_contact_phone,patient_contact_address,patient_update_time,patient_data_source_key)
            VALUES (
                @RandomName + RIGHT('000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 1000), 3), -- 姓名 + 固定5位数
                @GenderKey, -- 性别key
                @Gender, -- 性别
                @birthday, -- 出生日期
                @age, -- 年龄
                @provinceKey, -- 出生地-省key
                @province, -- 出生地-省
                @cityKey, -- 出生地-市key
                @city, -- 出生地-市
                @countyKey, -- 出生地-县key
                @county, -- 出生地-县
                '中国', -- 国籍
                @provinceKey, -- 籍贯省key
                @province, -- 籍贯省名称
                @cityKey, -- 籍贯市key
                @city, -- 籍贯市名称
                @RandomNationKey, -- 民族key
                @RandomNation, -- 民族
                @phone1, -- 联系电话
                @RandomAddress1, -- 现住址
                @RandomJob, -- 职业
                @RandomMarriageKey, -- 婚姻key
                @RandomMarriage, -- 婚姻
                @RandomIdtypeKey, --证件类型key
                @RandomIdtype, --证件类型
                @idcard, --证件号码 IDCardNumber
                @phone3, -- 家庭电话
                @RandomAddress1, -- 户口地址
                @RandomName + RIGHT('000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 1000), 3), -- 联系人姓名
                @RandomRelation, -- 与患者关系
                @phone2, -- 联系人电话
                @RandomAddress2, -- 联系人地址
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()), -- 更新时间
                '1' -- 数据来源
            );

            SET @Counter = @Counter + 1;
            SET @TotalCount = (select count(*) from a_cdrd_patient_info);
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