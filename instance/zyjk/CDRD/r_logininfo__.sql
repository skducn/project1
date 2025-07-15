-- todo 登录登出 - 登录类型，方式

CREATE OR ALTER PROCEDURE r_logininfo__
    @v1 nvarchar(50) OUTPUT,
    @v2 nvarchar(50) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- 生成临时表
    IF OBJECT_ID('tempdb..#tb_temp') IS NOT NULL DROP TABLE #tb_temp;
    CREATE TABLE #tb_temp (ID INT IDENTITY(1,1), v1 NVARCHAR(50), v2 NVARCHAR(150));
    INSERT INTO #tb_temp (v1, v2) VALUES
                ('登录', '账号密码登录'),
                ('登出', '手动登出')
      ;

    -- 随机选择一个 ID
    DECLARE @RandomID INT = CAST(RAND() * (SELECT COUNT(*) FROM #tb_temp) AS INT) + 1;

    -- 赋值输出参数
    SELECT @v1 = v1, @v2 = v2 FROM #tb_temp WHERE ID = @RandomID;
END
