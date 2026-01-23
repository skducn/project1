# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-12-22
# Description: 社区健康5G 信创1.0 - 表与表
# 需求：/Users/linghuchong/Desktop/智赢健康/信创/主动健康管理居民表.png
#***************************************************************
import dmPython

def connect_dm_db():
    """
    连接达梦数据库并执行基本操作
    """
    # 1. 数据库连接配置
    conn = None
    cursor = None
    try:
        # 建立连接（核心参数：地址、端口、用户名、密码、数据库名）
        conn = dmPython.connect(
            host='192.168.0.232',  # 数据库IP
            port=5236,         # 端口，默认5236
            user='SYSDBA',     # 用户名，默认SYSDBA
            password='Zy@20251222' # 密码，默认SYSDBA
            # 数据库名（部分 dmPython 版本用 dbname，而非 database）
            # dbname='CHCCONFIG',
            # # 可选：如果需要指定字符集
            # charset='UTF-8'
        )
        # conn = dmPython.connect(dsn="192.168.0.232:5236/CHCCONFIG", user="SYSDBA", password="Zy@20251222")

        print("数据库连接成功！")

        # 2. 创建游标（用于执行SQL）
        cursor = conn.cursor()

        # 3. 执行查询操作
        sql_query = "SELECT * FROM CHCCONFIG.SYS_MENU WHERE ID = 3"
        cursor.execute(sql_query, (10,))  # 带参数查询，避免SQL注入
        # 获取查询结果
        columns = [desc[0] for desc in cursor.description]  # 获取列名
        results = cursor.fetchall()  # 获取所有数据
        print("\n查询结果（列名）：", columns)
        print("查询结果（数据）：")
        for row in results:
            print(row)

        # # 4. 执行增删改操作（需提交事务）
        # # 示例：插入一条测试数据
        # sql_insert = "INSERT INTO TEST_TABLE (ID, NAME) VALUES (?, ?)"
        # cursor.execute(sql_insert, (1, "测试数据"))
        # conn.commit()  # 提交事务（增删改必须提交）
        # print("\n数据插入成功！")

    except dmPython.Error as e:
        # 捕获数据库异常并回滚事务
        if conn:
            conn.rollback()
        print(f"数据库操作失败：{e}")
    finally:
        # 5. 关闭游标和连接（释放资源）
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("\n数据库连接已关闭")

# 执行函数
if __name__ == "__main__":
    connect_dm_db()