CREATE OR ALTER FUNCTION dbo.fn_name(
    @Gender NVARCHAR(1) = NULL -- 'M' 表示男，'F' 表示女，NULL 表示随机
)
RETURNS NVARCHAR(10)
AS
BEGIN
    -- 定义常见中文姓氏
    DECLARE @Surnames NVARCHAR(1000) = N'赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮龚程嵇邢滑裴陆荣翁荀羊於惠甄麴家封芮羿储靳汲邴糜松井段富巫乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙叶幸司韶郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴鬱胥能苍双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍郤璩桑桂濮牛寿通边扈燕冀郏浦尚农温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘匡国文寇广禄阙东殴殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空曾毋沙乜养鞠须丰巢关蒯相查后荆红游竺权逯盖益桓公晋楚闫法汝鄢涂钦归海帅缑亢况后有琴梁丘左丘东门西门商牟佘佴伯赏南宫墨哈谯笪年爱阳佟第五言福';

    -- 定义男性常用名
    DECLARE @MaleNames NVARCHAR(1000) = N'伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清飞彬富顺信子杰涛昌成康星光天达安岩中茂进林有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善厚庆磊民友裕河哲江超浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽晨辰士以建家致树炎德行时泰盛';

    -- 定义女性常用名
    DECLARE @FemaleNames NVARCHAR(1000) = N'秀娟英华慧巧美娜静淑惠珠翠雅芝玉萍红娥玲芬芳燕彩春菊兰凤洁梅琳素云莲真环雪荣爱妹霞香月莺媛艳瑞凡佳嘉琼勤珍贞莉桂娣叶璧璐娅琦晶妍茜秋珊莎锦黛青倩婷姣婉娴瑾颖露瑶怡婵雁蓓纨仪荷丹蓉眉君琴蕊薇菁梦岚苑婕馨瑗琰韵融园艺咏卿聪澜纯毓悦昭冰爽琬茗羽希宁欣飘育滢馥筠柔竹霭凝晓欢霄枫芸菲寒伊亚宜可姬舒影荔枝思丽 ';

    -- 声明变量
    DECLARE @Result NVARCHAR(10);
    DECLARE @Surname NVARCHAR(1);
    DECLARE @Name NVARCHAR(8);
    DECLARE @NameLength INT;
    DECLARE @Seed BIGINT;
    DECLARE @Rand1 INT, @Rand2 INT, @Rand3 INT;
    DECLARE @DatePart BIGINT;

    -- 优化种子生成（避免溢出）：仅取时间戳的后18位+会话ID
    SET @DatePart = DATEDIFF_BIG(MILLISECOND, '2000-01-01', GETDATE()) % 1000000000000000000; -- 毫秒差取后18位
    SET @Seed = @DatePart + (@@SPID % 1000) * 1000000000000000; -- 会话ID取模后拼接，避免溢出

    -- 线性同余算法生成3个随机数（参数调整为避免溢出）
    SET @Rand1 = (1664525 * (@Seed % 2147483647) + 1013904223) % 2147483648;
    SET @Seed = @Rand1;
    SET @Rand2 = (1664525 * (@Seed % 2147483647) + 1013904223) % 2147483648;
    SET @Seed = @Rand2;
    SET @Rand3 = (1664525 * (@Seed % 2147483647) + 1013904223) % 2147483648;

    -- 生成随机姓氏
    SET @Surname = SUBSTRING(
        @Surnames,
        (ABS(@Rand1) % LEN(@Surnames)) + 1,
        1
    );

    -- 生成名字
    IF @Gender = 'M' -- 男性
    BEGIN
        SET @NameLength = CASE WHEN (ABS(@Rand2) % 10) > 3 THEN 2 ELSE 1 END;

        IF @NameLength = 1
        BEGIN
            SET @Name = SUBSTRING(@MaleNames, (ABS(@Rand3) % LEN(@MaleNames)) + 1, 1);
        END
        ELSE
        BEGIN
            SET @Name = SUBSTRING(@MaleNames, (ABS(@Rand2) % LEN(@MaleNames)) + 1, 1) +
                        SUBSTRING(@MaleNames, (ABS(@Rand3) % LEN(@MaleNames)) + 1, 1);
        END
    END
    ELSE IF @Gender = 'F' -- 女性
    BEGIN
        SET @NameLength = CASE WHEN (ABS(@Rand2) % 10) > 3 THEN 2 ELSE 1 END;

        IF @NameLength = 1
        BEGIN
            SET @Name = SUBSTRING(@FemaleNames, (ABS(@Rand3) % LEN(@FemaleNames)) + 1, 1);
        END
        ELSE
        BEGIN
            SET @Name = SUBSTRING(@FemaleNames, (ABS(@Rand2) % LEN(@FemaleNames)) + 1, 1) +
                        SUBSTRING(@FemaleNames, (ABS(@Rand3) % LEN(@FemaleNames)) + 1, 1);
        END
    END
    ELSE -- 随机性别
    BEGIN
        IF (ABS(@Rand1) % 2) = 0 -- 偶数为男性
        BEGIN
            SET @NameLength = CASE WHEN (ABS(@Rand2) % 10) > 3 THEN 2 ELSE 1 END;

            IF @NameLength = 1
            BEGIN
                SET @Name = SUBSTRING(@MaleNames, (ABS(@Rand3) % LEN(@MaleNames)) + 1, 1);
            END
            ELSE
            BEGIN
                SET @Name = SUBSTRING(@MaleNames, (ABS(@Rand2) % LEN(@MaleNames)) + 1, 1) +
                            SUBSTRING(@MaleNames, (ABS(@Rand3) % LEN(@MaleNames)) + 1, 1);
            END
        END
        ELSE -- 奇数为女性
        BEGIN
            SET @NameLength = CASE WHEN (ABS(@Rand2) % 10) > 3 THEN 2 ELSE 1 END;

            IF @NameLength = 1
            BEGIN
                SET @Name = SUBSTRING(@FemaleNames, (ABS(@Rand3) % LEN(@FemaleNames)) + 1, 1);
            END
            ELSE
            BEGIN
                SET @Name = SUBSTRING(@FemaleNames, (ABS(@Rand2) % LEN(@FemaleNames)) + 1, 1) +
                            SUBSTRING(@FemaleNames, (ABS(@Rand3) % LEN(@FemaleNames)) + 1, 1);
            END
        END
    END

    -- 组合姓名
    SET @Result = @Surname + @Name;

    RETURN @Result;
END;