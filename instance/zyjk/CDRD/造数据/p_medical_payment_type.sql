-- todo 付费方式

CREATE OR ALTER PROCEDURE p_medical_payment_type
    @k nvarchar(50) OUTPUT,
    @v nvarchar(50) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- 生成临时表
    IF OBJECT_ID('tempdb..#tb_temp') IS NOT NULL DROP TABLE #tb_temp;
    CREATE TABLE #tb_temp (ID INT IDENTITY(1,1), k NVARCHAR(50), v NVARCHAR(50));
    INSERT INTO #tb_temp (k, v) VALUES ('1',N'城镇职工基本医疗保险'),('2',N'城镇居民基本医疗保险'),('3',N'新型农村合作医疗'),
                                       ('4',N'贫困救助'),('5',N'商业医疗保险'),('6',N'全公费'),
                                       ('7',N'全自费'),('8',N'其他社会保险(指生育保险、工伤保险、农民工保险等)'),('9',N'其他');

    -- 随机选择一个 ID
    DECLARE @RandomID INT = CAST(RAND() * (SELECT COUNT(*) FROM #tb_temp) AS INT) + 1;

    -- 赋值输出参数
    SELECT @k = k, @v = v FROM #tb_temp WHERE ID = @RandomID;
END
