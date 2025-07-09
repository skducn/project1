-- todo 姓名

CREATE OR ALTER PROCEDURE p_gen_names
    @Count INT = 1,        -- 生成姓名总数量
    @MaxChinese INT = 3,   -- 最大中文姓名数量（默认3个）
    @Prefix NVARCHAR(50) = NULL,  -- 姓名前缀
    @Suffix NVARCHAR(50) = NULL,   -- 姓名后缀
    @FullName NVARCHAR(50) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- 中文姓氏字典
    DECLARE @ChineseSurnames TABLE (Surname NVARCHAR(10))
    INSERT INTO @ChineseSurnames (Surname) VALUES
    ('赵'),('钱'),('孙'),('李'),('周'),('吴'),('郑'),('王'),('冯'),('陈'),
    ('褚'),('卫'),('蒋'),('沈'),('韩'),('杨'),('朱'),('秦'),('尤'),('许'),
    ('何'),('吕'),('施'),('张'),('孔'),('曹'),('严'),('华'),('金'),('魏'),
    ('陶'),('姜'),('戚'),('谢'),('邹'),('喻'),('柏'),('水'),('窦'),('章'),
    ('云'),('苏'),('潘'),('葛'),('奚'),('范'),('彭'),('郎'),('鲁'),('韦');

    -- 中文名字字典（男女通用）
    DECLARE @ChineseNames TABLE (Name NVARCHAR(10))
    INSERT INTO @ChineseNames (Name) VALUES
    ('伟'),('芳'),('娜'),('秀英'),('敏'),('静'),('强'),('磊'),('军'),('洋'),
    ('勇'),('艳'),('杰'),('娟'),('涛'),('明'),('超'),('秀兰'),('霞'),('婷'),
    ('萍'),('慧'),('琳'),('桂英'),('德'),('刚'),('良'),('梅'),('云'),('斌');

    -- 英文姓氏字典
    DECLARE @EnglishSurnames TABLE (Surname NVARCHAR(50))
    INSERT INTO @EnglishSurnames (Surname) VALUES
    ('Smith'),('Johnson'),('Williams'),('Jones'),('Brown'),('Davis'),('Miller'),('Wilson'),
    ('Moore'),('Taylor'),('Anderson'),('Thomas'),('Jackson'),('White'),('Harris'),('Martin'),
    ('Thompson'),('Garcia'),('Martinez'),('Robinson'),('Clark'),('Rodriguez'),('Lewis'),('Lee');

    -- 英文名字字典（男女通用）
    DECLARE @EnglishNames TABLE (Name NVARCHAR(50))
    INSERT INTO @EnglishNames (Name) VALUES
    ('James'),('John'),('Robert'),('Michael'),('William'),('David'),('Richard'),('Charles'),
    ('Joseph'),('Thomas'),('Christopher'),('Daniel'),('Paul'),('Mark'),('Donald'),('George'),
    ('Kenneth'),('Steven'),('Edward'),('Brian'),('Ronald'),('Anthony'),('Kevin'),('Jason');

    -- 结果表
    DECLARE @Result TABLE (ID INT IDENTITY(1,1), FullName NVARCHAR(100), IsChinese BIT)

    -- 计算中文和英文姓名数量
    DECLARE @ChineseCount INT = CASE
        WHEN @Count <= @MaxChinese THEN @Count
        ELSE @MaxChinese
    END
    DECLARE @EnglishCount INT = @Count - @ChineseCount

    -- 生成中文姓名
    WHILE @ChineseCount > 0
    BEGIN
        -- 随机选择姓氏和名字
        DECLARE @RandomSurname NVARCHAR(10)
        DECLARE @RandomName NVARCHAR(20)

        SELECT TOP 1 @RandomSurname = Surname
        FROM @ChineseSurnames
        ORDER BY NEWID()

        -- 50%概率生成2个字名字，50%概率生成1个字名字
        IF RAND() > 0.5
        BEGIN
            SELECT TOP 2 @RandomName = ISNULL(@RandomName, '') + Name
            FROM @ChineseNames
            ORDER BY NEWID()
        END
        ELSE
        BEGIN
            SELECT TOP 1 @RandomName = Name
            FROM @ChineseNames
            ORDER BY NEWID()
        END

        -- 组合姓名（包括前缀和后缀）
        INSERT INTO @Result (FullName, IsChinese)
        VALUES (ISNULL(@Prefix, '') + @RandomSurname + @RandomName + ISNULL(@Suffix, ''), 1)

        SET @ChineseCount = @ChineseCount - 1
    END

    -- 生成英文姓名
    WHILE @EnglishCount > 0
    BEGIN
        -- 随机选择姓氏和名字
        DECLARE @RandomEName NVARCHAR(50)
        DECLARE @RandomESurname NVARCHAR(50)

        SELECT TOP 1 @RandomEName = Name
        FROM @EnglishNames
        ORDER BY NEWID()

        SELECT TOP 1 @RandomESurname = Surname
        FROM @EnglishSurnames
        ORDER BY NEWID()

        -- 组合姓名（包括前缀和后缀）
        INSERT INTO @Result (FullName, IsChinese)
        VALUES (ISNULL(@Prefix, '') + @RandomEName + ' ' + @RandomESurname + ISNULL(@Suffix, ''), 0)

        SET @EnglishCount = @EnglishCount - 1
    END

    -- 随机排序并返回结果
    SELECT @FullName =FullName FROM @Result ORDER BY NEWID()
END