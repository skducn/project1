-- todo 患者信息表
-- 数据量：3000
-- 需求：https://docs.qq.com/doc/DYnZXTVZ1THpPVEVC?g=X2hpZGRlbjpoaWRkZW4xNzUzMjYyNzc0ODQ3#g=X2hpZGRlbjpoaWRkZW4xNzUzMjYyNzc0ODQ3
-- # gitlab http://192.168.0.241/cdrd_product_doc/product_doc
-- 批处理优化：避免一次性生成所有数据，减少内存压力
-- 模块化设计：通过调用其他存储过程实现功能复用
-- 随机性：使用 NEWID() 和 CHECKSUM 函数生成随机数据
-- 数据完整性：通过关联表确保生成的数据符合实际业务逻辑
-- 3000条，耗时: 11.2399 秒
-- 30000条，耗时: 113.9838 秒 ， 11M

-- todo 患者信息表
-- 数据量：3000
-- 需求：https://docs.qq.com/doc/DYnZXTVZ1THpPVEVC?g=X2hpZGRlbjpoaWRkZW4xNzUzMjYyNzc0ODQ3#g=X2hpZGRlbjpoaWRkZW4xNzUzMjYyNzc0ODQ3
-- # gitlab http://192.168.0.241/cdrd_product_doc/product_doc
-- 批处理优化：避免一次性生成所有数据，减少内存压力
-- 模块化设计：通过调用其他存储过程实现功能复用
-- 随机性：使用 NEWID() 和 CHECKSUM 函数生成随机数据
-- 数据完整性：通过关联表确保生成的数据符合实际业务逻辑
-- 3000条，耗时: 11.2399 秒
-- 30000条，耗时: 113.9838 秒 ， 11M

CREATE OR ALTER PROCEDURE s_cdrd_patient_info
    @result INT OUTPUT
AS
BEGIN
    --1. 初始化设置
    SET NOCOUNT ON;  --防止返回受影响行数的信息
    SET XACT_ABORT ON;  --遇到错误时自动回滚事务

    -- 如果 @result 没有被传入或为0，则设置默认值
    IF @result IS NULL OR @result = 0
        SET @result = 100;

--     -- 检查并创建数据库主密钥（如果不存在）
--     IF NOT EXISTS (SELECT * FROM sys.symmetric_keys WHERE name = '##MS_DatabaseMasterKey##')
--         CREATE MASTER KEY ENCRYPTION BY PASSWORD = '???';
--
--     -- 检查并创建证书（用于保护对称密钥）
--     IF NOT EXISTS (SELECT * FROM sys.certificates WHERE name = 'AESCert')
--         CREATE CERTIFICATE AESCert
--         WITH SUBJECT = 'AES Encryption Certificate';
--
--     -- 检查并创建AES对称密钥（支持128位）
--     IF NOT EXISTS (SELECT * FROM sys.symmetric_keys WHERE name = 'benetech12345678')
--         CREATE SYMMETRIC KEY AESSymKey
--         WITH ALGORITHM = AES_128
--         ENCRYPTION BY CERTIFICATE AESCert;

    -- 1. 创建主密钥（只需一次）
--     CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'Benetech12345678';

--     DECRYPTION by password = 'Benetech12345678'

    -- 2. 让它自动打开
--     ALTER MASTER KEY ADD ENCRYPTION BY SERVICE MASTER KEY;
--
--     -- 3. 创建你的对称密钥（用 benetech12345678 保护）
--     CREATE SYMMETRIC KEY PatientDataSymKey
--     WITH ALGORITHM = AES_128
--     ENCRYPTION BY PASSWORD = 'benetech12345678';
--
--     -- 打开对称密钥（使用你的密码）
--     OPEN SYMMETRIC KEY PatientDataSymKey
--     DECRYPTION BY PASSWORD = 'benetech12345678';


--     -- 1. 创建数据库主密钥（如果不存在）
--     IF NOT EXISTS (SELECT * FROM sys.symmetric_keys WHERE name = '##MS_DatabaseMasterKey##')
--     BEGIN
--         CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'benetech12345678'; -- 请更换为强密码
--     END
--
--     -- 2. 创建证书（用于保护对称密钥）
--     IF NOT EXISTS (SELECT * FROM sys.certificates WHERE name = 'AESCert')
--     BEGIN
--         CREATE CERTIFICATE AESCert
--         WITH SUBJECT = 'AES Encryption Certificate for Benetech',
--              EXPIRY_DATE = '2030-12-31'; -- 设置证书过期日期
--     END
--
--     -- 3. 创建指定密钥的AES对称密钥
--     IF NOT EXISTS (SELECT * FROM sys.symmetric_keys WHERE name = 'AESSymKey')
--     BEGIN
--         CREATE SYMMETRIC KEY AESSymKey
--         WITH ALGORITHM = AES_128,  -- 使用128位AES加密算法
--              KEY_SOURCE = 'benetech12345678',  -- 指定对称密钥
--              IDENTITY_VALUE = 'benetech_identity_123'  -- 用于生成密钥的标识值
--         ENCRYPTION BY CERTIFICATE AESCert;
--     END

--     -- 打开对称密钥
--     OPEN SYMMETRIC KEY AESSymKey
--     DECRYPTION BY CERTIFICATE AESCert;

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
        patient_phone_num NVARCHAR(128),
        patient_home_address NVARCHAR(400),
        patient_id_num VARCHAR(100),
        patient_home_phone NVARCHAR(160),
        patient_contact_phone NVARCHAR(160),
        patient_contact_address NVARCHAR(400),
        patient_contact_name NVARCHAR(160)

-- --         patient_phone_num varbinary(128),
-- --         patient_home_address varbinary(400),
--         patient_id_num VARCHAR(100)
-- --         patient_home_phone varbinary(160),
-- --         patient_contact_phone varbinary(160),
-- --         patient_contact_address varbinary(400),
-- --         patient_contact_name varbinary(160)
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
            DECLARE @AESKey VARBINARY(16); -- AES-128需要16字节密钥

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

            -- 生成随机AES-128密钥(16字节)
--             SET @AESKey = CRYPT_GEN_RANDOM(16);

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
--                 @idcard
                @phone1,
                @RandomAddress1,
                @idcard,
                @phone2,
                @phone3,
                @RandomAddress2,
                @RandomName

--                 EncryptByKey(Key_GUID('PatientDataSymKey'), @phone1),
--                 EncryptByKey(Key_GUID('PatientDataSymKey'), @RandomAddress1),
--                 @idcard,
--                 EncryptByKey(Key_GUID('PatientDataSymKey'), @phone2),
--                 EncryptByKey(Key_GUID('PatientDataSymKey'), @phone3),
--                 EncryptByKey(Key_GUID('PatientDataSymKey'), @RandomAddress2),
--                 EncryptByKey(Key_GUID('PatientDataSymKey'), @RandomName)
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

    -- 关闭对称密钥
--     CLOSE SYMMETRIC KEY AESSymKey;

    DROP TABLE #BatchData;
END;
