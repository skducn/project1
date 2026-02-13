
import pymysql
pymysql.install_as_MySQLdb()

from airflow import DAG
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


# 第三步：定义 MySQL 查询函数
def query_mysql_data():
    """查询 MySQL 数据的核心函数"""
    try:
        # 创建 MySQL Hook 实例（使用你配置的连接ID：mysql_234_crm）
        # 登录 Airflow Web UI。
        # 导航到 Admin > Connections 页面。
        # 点击 + 按钮创建一个新的连接。
        # 填写以下字段：
        # Conn Id: 自定义一个唯一的连接 ID（例如：mysql_234_crm），这个 ID 会在代码中用到。
        # Conn Type: 选择 MySQL。
        # Host: MySQL 服务器地址（例如：localhost 或 IP 地址）。
        # Schema: 数据库名称（例如：crm_db）。
        # Login: MySQL 用户名（例如：root）。
        # Password: MySQL 密码。
        # Port: MySQL 端口号（默认是 3306）。
        # 点击 Save 保存连接。
        mysql_hook = MySqlHook(mysql_conn_id='mysql_234_crm')

        # 测试查询（替换成你实际要执行的SQL）
        # test_sql = "SELECT 1 AS test_result FROM DUAL"
        test_sql = " SELECT * FROM user where UID=82"

        # 执行查询并获取结果
        result = mysql_hook.get_first(test_sql)

        # 打印结果，方便在日志中查看
        print(f"✅ MySQL 连接成功！测试查询结果: {result}")

        # 返回结果，自动推送到 XCom
        return result

    except Exception as e:
        print(f"❌ MySQL 操作失败: {str(e)}")
        raise  # 抛出异常让 Airflow 标记任务失败


# 新增任务：处理从 MySQL 查询得到的结果
def process_result(**context):
    """处理从 MySQL 查询得到的结果"""
    # 从 XCom 中获取 query_mysql_data 任务的返回值
    result = context['task_instance'].xcom_pull(task_ids='query_mysql')
    print(f"从 XCom 获取的结果: {result[2]}")

    # 在这里可以对 result 进行进一步处理
    if result:
        print("处理结果...")
    else:
        print("没有获取到结果")
# 第四步：定义 DAG 配置
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
        dag_id='test_crm',
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

    # 定义第二个任务：处理查询结果
    process_result_task = PythonOperator(
        task_id='process_result',
        python_callable=process_result
    )

# 设置任务执行顺序（这里只有一个任务，可省略）
query_mysql_task  >> process_result_task