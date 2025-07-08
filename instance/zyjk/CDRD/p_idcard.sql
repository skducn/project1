-- todo 随机身份证

CREATE OR ALTER PROCEDURE p_idcard
    @countyKey nvarchar(6),
    @idcard nvarchar(18) OUTPUT,
    @gender nvarchar(18) OUTPUT,
    @genderKey nvarchar(18) OUTPUT,
    @birthday nvarchar(18) OUTPUT,
    @age nvarchar(18) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- 1 随机生成身份证号
    -- 使用县级编码作为身份证前6位
    DECLARE @AreaCode CHAR(6);
    SET @AreaCode = @countyKey; -- 替换原来的 '440000'

    DECLARE @Year INT = 1960 + ABS(CHECKSUM(NEWID())) % 60; -- 年份范围：1960 - 2019
    DECLARE @Month INT = 1 + ABS(CHECKSUM(NEWID())) % 12; -- 月份
    DECLARE @Day INT = 1 + ABS(CHECKSUM(NEWID())) % 28; -- 日期（避免非法日期）

    -- 构造前17位
    DECLARE @BaseID NVARCHAR(17) =
        @AreaCode +
        RIGHT('0000' + CAST(@Year AS NVARCHAR), 4) +
        RIGHT('00' + CAST(@Month AS NVARCHAR), 2) +
        RIGHT('00' + CAST(@Day AS NVARCHAR), 2) +
        RIGHT('000' + CAST(ABS(CHECKSUM(NEWID())) % 999 AS NVARCHAR), 3);
    -- 简化校验码处理（实际应根据 ISO 7064:1983.MOD 11-2 计算）
    DECLARE @IDCardNumber VARCHAR(18) = @BaseID + 'X'; -- 临时使用 'X' 表示最后一位校验码

    -- 2 获取性别
--     DECLARE @Gender NVARCHAR(10);
--     DECLARE @genderKey NVARCHAR(10);
    -- 提取第17位数字
    DECLARE @genderDigit INT = CAST(SUBSTRING(@IDCardNumber, 17, 1) AS INT);
    -- 2 判断性别
    IF @genderDigit % 2 = 1
    BEGIN
        SET @Gender = N'男';
        SET @genderKey = 0;
    END
    ELSE
    BEGIN
        SET @Gender = N'女';
        SET @genderKey = 1;
    END


    -- 3 出生日期
    SET @birthday = CAST(CAST(@Year AS VARCHAR) + '-' + CAST(@Month AS VARCHAR) + '-' + CAST(@Day AS VARCHAR) AS DATE);

    -- 4 年龄
--     DECLARE @age INT = DATEDIFF(YEAR, @birthday, GETDATE()) -
    set @age  = DATEDIFF(YEAR, @birthday, GETDATE()) -
    CASE
       WHEN DATEADD(YEAR, DATEDIFF(YEAR, @birthday, GETDATE()), @birthday) > GETDATE()
           THEN 1
       ELSE 0
    END;

    -- 赋值输出参数
    SELECT @idcard = @IDCardNumber, @birthday = @birthday

END
