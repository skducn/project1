-- todo 患者信息表
-- 数据量：3000
-- 需求：https://docs.qq.com/doc/DYnZXTVZ1THpPVEVC?g=X2hpZGRlbjpoaWRkZW4xNzUzMjYyNzc0ODQ3#g=X2hpZGRlbjpoaWRkZW4xNzUzMjYyNzc0ODQ3
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
        SET @result = 10;

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
        patient_phone_num NVARCHAR(11),
        patient_home_address NVARCHAR(150),
        patient_profession NVARCHAR(100),
        patient_marriage_key NVARCHAR(100),
        patient_marriage_value NVARCHAR(100),
        patient_id_type_key NVARCHAR(100),
        patient_id_type_value NVARCHAR(100),
        patient_id_num NVARCHAR(18),
        patient_home_phone NVARCHAR(8),
        patient_account_address NVARCHAR(150),
        patient_contact_name NVARCHAR(50),
        patient_contact_relation NVARCHAR(100),
        patient_contact_phone NVARCHAR(11),
        patient_contact_address NVARCHAR(150),
        patient_update_time DATETIME,
        patient_data_source_key NVARCHAR(10)
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

            -- 2. 生成随机AES-128密钥(16字节)和IV(16字节)
            SET @AESKey = CRYPT_GEN_RANDOM(16); -- 生成16字节随机密钥

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
                @phone1,
                @RandomAddress1,
                @RandomJob,
                @RandomMarriageKey,
                @RandomMarriage,
                @RandomIdtypeKey,
                '居民身份证',
                @idcard,
                @phone3,
                @RandomAddress1,
                @RandomName + RIGHT('000' + CONVERT(NVARCHAR(10), ABS(CHECKSUM(NEWID())) % 1000), 3),
                @RandomRelation,
                @phone2,
                @RandomAddress2,
                DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 365, GETDATE()),
                '1'
            );

            SET @i = @i + 1;
        END;

        -- 再将临时表数据批量插入到目标表 a_cdrd_patient_info
        INSERT INTO CDRD_PATIENT_INFO (
            patient_name, patient_sex_key, patient_sex_value, patient_birth_date, patient_age,
            patient_birth_address_province_key, patient_birth_address_province, patient_birth_address_city_key,
            patient_birth_address_city, patient_birth_address_country_key, patient_birth_address_country,
            patient_country, patient_native_province_key, patient_native_province, patient_native_city_key,
            patient_native_city, patient_nation_key, patient_nation_value, patient_phone_num, patient_home_address,
            patient_profession, patient_marriage_key, patient_marriage_value, patient_id_type_key,
            patient_id_type_value, patient_id_num, patient_home_phone, patient_account_address,
            patient_contact_name, patient_contact_relation, patient_contact_phone, patient_contact_address,
            patient_update_time, patient_data_source_key
        )
        SELECT
            patient_name, patient_sex_key, patient_sex_value, patient_birth_date, patient_age,
            patient_birth_address_province_key, patient_birth_address_province, patient_birth_address_city_key,
            patient_birth_address_city, patient_birth_address_country_key, patient_birth_address_country,
            patient_country, patient_native_province_key, patient_native_province, patient_native_city_key,
            patient_native_city, patient_nation_key, patient_nation_value, patient_phone_num, patient_home_address,
            patient_profession, patient_marriage_key, patient_marriage_value, patient_id_type_key,
            patient_id_type_value, patient_id_num, patient_home_phone, patient_account_address,
            patient_contact_name, patient_contact_relation, patient_contact_phone, patient_contact_address,
            patient_update_time, patient_data_source_key
        FROM #BatchData;

        SET @Counter = @Counter + @CurrentBatchSize;
    END;

    -- 设置输出参数为实际生成的记录数
    SET @result = @Counter;

    DROP TABLE #BatchData;
END;
