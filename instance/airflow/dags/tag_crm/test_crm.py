# 第一步：关键修复 - 让 pymysql 冒充 MySQLdb，解决模块缺失问题
import pymysql

pymysql.install_as_MySQLdb()

# 第二步：导入 Airflow 相关依赖
from airflow import DAG
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


# 第三步：定义 MySQL 查询函数
def query_mysql_data():
    """查询 MySQL 数据的核心函数"""
    try:
        # 创建 MySQL Hook 实例（使用你配置的连接ID：mysql_234_crm）
        mysql_hook = MySqlHook(mysql_conn_id='mysql_234_crm')

        # 测试查询（替换成你实际要执行的SQL）
        # test_sql = "SELECT 1 AS test_result FROM DUAL"
        test_sql = " SELECT * FROM user where UID=82"

        # 执行查询并获取结果
        result = mysql_hook.get_first(test_sql)

        # 打印结果，方便在日志中查看
        print(f"✅ MySQL 连接成功！测试查询结果: {result}")

    except Exception as e:
        print(f"❌ MySQL 操作失败: {str(e)}")
        raise  # 抛出异常让 Airflow 标记任务失败


# 第四步：定义 DAG 配置
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
        dag_id='test_connection_mysql',
        default_args=default_args,
        start_date=datetime(2026, 2, 12),
        schedule_interval='@once',  # 仅执行一次，方便测试
        catchup=False,
        tags=['mysql', 'test', 'connection']
) as dag:
    # 定义 Python 任务
    query_mysql_task = PythonOperator(
        task_id='query_mysql',
        python_callable=query_mysql_data
    )

# 设置任务执行顺序（这里只有一个任务，可省略）
query_mysql_task