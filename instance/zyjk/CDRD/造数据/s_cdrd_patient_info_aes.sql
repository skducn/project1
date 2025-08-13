CREATE OR ALTER PROCEDURE s_cdrd_patient_info_aes
    @result INT OUTPUT
AS
BEGIN
    --1. 初始化设置
    SET NOCOUNT ON;  --防止返回受影响行数的信息
    SET XACT_ABORT ON;  --遇到错误时自动回滚事务

    -- 如果 @result 没有被传入或为0，则设置默认值
    IF @result IS NULL OR @result = 0
        SET @result = 10;

    -- 定义16进制密钥
    DECLARE @KeyHex VARCHAR(32) = '42656E65746563684031323334353637';
    DECLARE @EncryptionKey VARBINARY(16);

    -- 将16进制字符串转换为二进制密钥(16字节，AES128需要16字节密钥)
    SET @EncryptionKey = CONVERT(VARBINARY(16), @KeyHex, 2);

    -- 检查密钥长度是否正确(16字节)
    IF LEN(@EncryptionKey) <> 16
    BEGIN
        RAISERROR('AES128 requires a 16-byte encryption key.', 16, 1);
        RETURN;
    END

    -- 创建对称密钥（如果不存在）使用指定的16进制密钥
    IF NOT EXISTS (SELECT * FROM sys.symmetric_keys WHERE name = 'AES128_Key')
    BEGIN
        CREATE SYMMETRIC KEY AES128_Key
        WITH ALGORITHM = AES_128
        ENCRYPTION BY CERTIFICATE YourCertificate; -- 需要先创建证书
        -- 或者使用密码加密:
        -- ENCRYPTION BY PASSWORD = 'StrongPassword123!';
    END

    -- 如果无法直接使用16进制密钥创建对称密钥，则使用EncryptByPassPhrase
    -- 打开对称密钥（如果使用证书或密码方式）
    -- OPEN SYMMETRIC KEY AES128_Key DECRYPTION BY PASSWORD = 'StrongPassword123!';

    --2. 临时表结构
    -- 创建临时表存储批量数据
    CREATE TABLE #BatchData (
        patient_name NVARCHAR(50),
        patient_sex_key NVARCHAR(10),
        patient_sex_value NVARCHAR(10),
        patient_birth_date NVARCHAR(18),
        patient_age NVARCHAR(150),
        patient_birth_address_province_key NVARCHAR(150),
        patient_birth_address_province NVARCHAR(150),
        patient_birth_address_city_key NVARCHAR(150),
        patient_birth_address_city NVARCHAR(150),
        patient_birth_address_country_key NVARCHAR(150),
        patient_birth_address_country NVARCHAR(150),
        patient_country NVARCHAR(50),
        patient_native_province_key NVARCHAR(150),
        patient_native_province NVARCHAR(150),
        patient_native_city_key NVARCHAR(150),
        patient_native_city NVARCHAR(150),
        patient_nation_key NVARCHAR(100),
        patient_nation_value NVARCHAR(100),
        patient_profession NVARCHAR(100),
        patient_marriage_key NVARCHAR(100),
        patient_marriage_value NVARCHAR(100),
        patient_id_type_key NVARCHAR(100),
        patient_id_type_value NVARCHAR(100),
        patient_account_address NVARCHAR(150),
        patient_contact_relation NVARCHAR(100),
        patient_update_time DATETIME,
        patient_data_source_key NVARCHAR(10),
        patient_source_id int,
        patient_phone_num varbinary(128),
        patient_home_address varbinary(400),
        patient_id_num VARCHAR(100),
        patient_home_phone varbinary(160),
        patient_contact_phone varbinary(160),
        patient_contact_address varbinary(400),
        patient_contact_name varbinary(160)
    );

    --3. 批量数据生成机制
    DECLARE @Counter INT = 0;
    DECLARE @BatchSize INT = 1000; -- 批量大小，使用批处理方式，每批生成1000条记录

    WHILE @Counter < @result
    BEGIN
        -- 清空临时表
        DELETE FROM #BatchData;

        -- 计算本批次要生成的记录数
        DECLARE @CurrentBatchSize INT =
            CASE
                WHEN (@result - @Counter) > @BatchSize THEN @BatchSize
                ELSE (@result - @Counter)
            END;

        -- 批量生成数据
        DECLARE @i INT = 1;
        WHILE @i <= @CurrentBatchSize
        BEGIN
            --4. 数据生成逻辑
            -- 电话号码：生成随机手机号和固定电话号
            DECLARE @phone1 NVARCHAR(11) = '138' + RIGHT('00000000' + CAST(ABS(CHECKSUM(NEWID())) % 99999999 AS VARCHAR(8)), 8);
            DECLARE @phone2 NVARCHAR(11) = '130' + RIGHT('00000000' + CAST(ABS(CHECKSUM(NEWID())) % 99999999 AS VARCHAR(8)), 8);
            DECLARE @phone3 NVARCHAR(8) = '5' + RIGHT('0000000' + CAST(ABS(CHECKSUM(NEWID())) % 9999999 AS VARCHAR(7)), 7);

            -- 婚姻状况：从 ab_marriage 表随机选取
            DECLARE @RandomMarriageKey NVARCHAR(100);
            DECLARE @RandomMarriage NVARCHAR(100);
            SELECT TOP 1 @RandomMarriageKey = n_key, @RandomMarriage = n_value
            FROM ab_marriage ORDER BY NEWID();

            -- 职业：从 ab_job 表随机选取
            DECLARE @RandomJob NVARCHAR(100);
            SELECT TOP 1 @RandomJob = n_value FROM ab_job ORDER BY NEWID();

            -- 证件类型：从 ab_IDtype 表随机选取
            DECLARE @RandomIdtypeKey NVARCHAR(100);
            DECLARE @RandomIdtype NVARCHAR(100);
            SELECT TOP 1 @RandomIdtypeKey = n_key, @RandomIdtype = n_value
            FROM ab_IDtype ORDER BY NEWID();

            -- 民族：从 ab_ethnicGroup 表随机选取
            DECLARE @RandomNationKey NVARCHAR(100);
            DECLARE @RandomNation NVARCHAR(100);
            SELECT TOP 1 @RandomNationKey = n_key, @RandomNation = n_value
            FROM ab_ethnicGroup ORDER BY NEWID();

            -- 关系：从 ab_relationship 表随机选取
            DECLARE @RandomRelation NVARCHAR(100);
            SELECT TOP 1 @RandomRelation = n_value FROM ab_relationship ORDER BY NEWID();

            -- 姓名：调用 p_name 存储过程生成
            DECLARE @RandomName NVARCHAR(50);
            EXEC p_name @FullName = @RandomName OUTPUT;

            -- 地址：调用 p_address 存储过程生成
            DECLARE @RandomAddress1 NVARCHAR(150), @RandomAddress2 NVARCHAR(150);
            EXEC p_address @v1 = @RandomAddress1 OUTPUT, @v2 = @RandomAddress2 OUTPUT;

            -- 出生地：调用 p_birth_place 存储过程生成
            DECLARE @provinceKey NVARCHAR(150), @province NVARCHAR(150);
            DECLARE @cityKey NVARCHAR(150), @city NVARCHAR(150);
            DECLARE @countyKey NVARCHAR(150), @county NVARCHAR(150);
            EXEC p_birth_place @provinceKey = @provinceKey OUTPUT, @province = @province OUTPUT,
                @cityKey = @cityKey OUTPUT, @city = @city OUTPUT,
                @countyKey = @countyKey OUTPUT, @county = @county OUTPUT;

            -- 身份证号：调用 p_idcard 存储过程生成（同时生成性别、生日、年龄）
            DECLARE @idcard NVARCHAR(18), @gender NVARCHAR(10);
            DECLARE @genderKey NVARCHAR(10), @birthday NVARCHAR(18), @age NVARCHAR(150);
            EXEC p_idcard @countyKey = @countyKey, @idcard = @idcard OUTPUT, @gender = @gender OUTPUT,
                 @genderKey = @genderKey OUTPUT, @birthday = @birthday OUTPUT,
                 @age = @age OUTPUT;

            --5. 数据插入
            -- 先将生成的数据插入临时表 #BatchData
            INSERT INTO #BatchData VALUES (
                @RandomName + RIGHT('000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 1000), 3),
                @GenderKey,
                @Gender,
                @birthday,
                @age,
                @provinceKey,
                @province,
                @cityKey,
                @city,
                @countyKey,
                @county,
                N'中国',
                @provinceKey,
                @province,
                @cityKey,
                @city,
                @RandomNationKey,
                @RandomNation,
                @RandomJob,
                @RandomMarriageKey,
                @RandomMarriage,
                @RandomIdtypeKey,
                '居民身份证',
                @RandomAddress1,
                @RandomRelation,
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()),
                '1',
                RIGHT('000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 1000), 3),
                EncryptByPassPhrase(@KeyHex, @phone1),
                EncryptByPassPhrase(@KeyHex, @RandomAddress1),
                @idcard,
                EncryptByPassPhrase(@KeyHex, @phone2),
                EncryptByPassPhrase(@KeyHex, @phone3),
                EncryptByPassPhrase(@KeyHex, @RandomAddress2),
                EncryptByPassPhrase(@KeyHex, @RandomName)
            );

            SET @i = @i + 1;
        END;

        -- 再将临时表数据批量插入到目标表 CDRD_PATIENT_INFO
        INSERT INTO CDRD_PATIENT_INFO (
            PATIENT_NAME,
            PATIENT_SEX_KEY,
            PATIENT_SEX_VALUE,
            PATIENT_BIRTH_DATE,
            PATIENT_AGE,
            PATIENT_BIRTH_ADDRESS_PROVINCE_KEY,
            PATIENT_BIRTH_ADDRESS_PROVINCE,
            PATIENT_BIRTH_ADDRESS_CITY_KEY,
            PATIENT_BIRTH_ADDRESS_CITY,
            PATIENT_BIRTH_ADDRESS_COUNTRY_KEY,
            PATIENT_BIRTH_ADDRESS_COUNTRY,
            PATIENT_COUNTRY,
            PATIENT_NATIVE_PROVINCE_KEY,
            PATIENT_NATIVE_PROVINCE,
            PATIENT_NATIVE_CITY_KEY,
            PATIENT_NATIVE_CITY,
            PATIENT_NATION_KEY,
            PATIENT_NATION_VALUE,
            PATIENT_PROFESSION,
            PATIENT_MARRIAGE_KEY,
            PATIENT_MARRIAGE_VALUE,
            PATIENT_ID_TYPE_KEY,
            PATIENT_ID_TYPE_VALUE,
            PATIENT_ACCOUNT_ADDRESS,
            PATIENT_CONTACT_RELATION,
            PATIENT_UPDATE_TIME,
            PATIENT_DATA_SOURCE_KEY,
            PATIENT_SOURCE_ID,
            PATIENT_PHONE_NUM,
            PATIENT_HOME_ADDRESS,
            PATIENT_ID_NUM,
            PATIENT_HOME_PHONE,
            PATIENT_CONTACT_PHONE,
            PATIENT_CONTACT_ADDRESS,
            PATIENT_CONTACT_NAME
        )
        SELECT
            PATIENT_NAME,
            PATIENT_SEX_KEY,
            PATIENT_SEX_VALUE,
            PATIENT_BIRTH_DATE,
            PATIENT_AGE,
            PATIENT_BIRTH_ADDRESS_PROVINCE_KEY,
            PATIENT_BIRTH_ADDRESS_PROVINCE,
            PATIENT_BIRTH_ADDRESS_CITY_KEY,
            PATIENT_BIRTH_ADDRESS_CITY,
            PATIENT_BIRTH_ADDRESS_COUNTRY_KEY,
            PATIENT_BIRTH_ADDRESS_COUNTRY,
            PATIENT_COUNTRY,
            PATIENT_NATIVE_PROVINCE_KEY,
            PATIENT_NATIVE_PROVINCE,
            PATIENT_NATIVE_CITY_KEY,
            PATIENT_NATIVE_CITY,
            PATIENT_NATION_KEY,
            PATIENT_NATION_VALUE,
            PATIENT_PROFESSION,
            PATIENT_MARRIAGE_KEY,
            PATIENT_MARRIAGE_VALUE,
            PATIENT_ID_TYPE_KEY,
            PATIENT_ID_TYPE_VALUE,
            PATIENT_ACCOUNT_ADDRESS,
            PATIENT_CONTACT_RELATION,
            PATIENT_UPDATE_TIME,
            PATIENT_DATA_SOURCE_KEY,
            PATIENT_SOURCE_ID,
            PATIENT_PHONE_NUM,
            PATIENT_HOME_ADDRESS,
            PATIENT_ID_NUM,
            PATIENT_HOME_PHONE,
            PATIENT_CONTACT_PHONE,
            PATIENT_CONTACT_ADDRESS,
            PATIENT_CONTACT_NAME
        FROM #BatchData;

        SET @Counter = @Counter + @CurrentBatchSize;
    END;

    -- 设置输出参数为实际生成的记录数
    SET @result = @Counter;

    -- 如果使用了对称密钥则关闭它
    -- CLOSE SYMMETRIC KEY AES128_Key;

    DROP TABLE #BatchData;
END;
