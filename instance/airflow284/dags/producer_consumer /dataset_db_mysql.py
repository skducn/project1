# 功能：生产者在mysql库里插入一条记录，消费者读取生产者的数据，并将status修改为2。
# 设置 admin - connections设置 "mysql_234_crm"

# MySQL 数据库中创建 airflow_producer_data 表，用于存储生产者的运行数据：
# sql
# CREATE TABLE IF NOT EXISTS airflow_producer_data (
#     id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
#     run_id VARCHAR(255) NOT NULL COMMENT '生产者DAG的Run ID（唯一标识一次运行）',
#     dag_id VARCHAR(100) NOT NULL COMMENT '生产者DAG ID',
#     task_id VARCHAR(100) NOT NULL COMMENT '生产者任务ID',
#     result TEXT COMMENT '生产者返回的业务数据（JSON格式）',
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '数据写入时间',
#     update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新时间',
#     status TINYINT(1) DEFAULT 0 COMMENT '数据状态（0-正常，2-消费）' ,
#     UNIQUE KEY uk_run_id (run_id) COMMENT '确保Run ID唯一'
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Airflow生产者数据存储表';

import pymysql
pymysql.install_as_MySQLdb()

from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime, timedelta
import json

# ===================== 1. 定义数据集（触发消费者） =====================
dw_order_dataset2 = Dataset(
    uri="dataset://mysql/dw_order2",
    extra={
        "description": "使用Variable存储（基于元数据库）",
        "owner": "john",
        "version": "1.0"
    }
)


# ===================== 2. 工具函数（通用数据库操作） =====================
def get_mysql_hook(conn_id="mysql_234_crm"):
    """获取MySQL Hook（封装通用连接逻辑）"""
    return MySqlHook(mysql_conn_id=conn_id)

def insert_producer_data(run_id, dag_id, task_id, result, conn_id="mysql_234_crm"):
    try:
        mysql_hook = get_mysql_hook(conn_id)
        result_json = json.dumps(result, ensure_ascii=False)
        sql = """
        INSERT INTO airflow_producer_data (run_id, dag_id, task_id, result,status)
        VALUES (%s, %s, %s, %s, 0)
        ON DUPLICATE KEY UPDATE 
            result = %s, 
            update_time = CURRENT_TIMESTAMP
        """
        mysql_hook.run(sql, parameters=(run_id, dag_id, task_id, result_json, result_json))
        print(f"生产者数据已写入MySQL：run_id={run_id}, result={result}")
    except Exception as e:
        print(f"写入MySQL失败：{e}")


def get_latest_producer_data(dag_id, task_id, conn_id="mysql_234_crm"):
    """消费者读取生产者最新数据"""
    mysql_hook = get_mysql_hook(conn_id)
    sql = """
    SELECT run_id, result, create_time 
    FROM airflow_producer_data 
    WHERE dag_id = %s AND task_id = %s 
    ORDER BY create_time DESC 
    LIMIT 1
    """
    # 执行查询并获取结果
    result = mysql_hook.get_first(sql, parameters=(dag_id, task_id))
    if result:
        run_id, result_json, create_time = result
        # 反序列化JSON为Python对象
        result_data = json.loads(result_json)
        return {
            "run_id": run_id,
            "result": result_data,
            "create_time": create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
    else:
        return None


# ===================== 3. 生产者DAG（写入外部数据库+更新数据集） =====================
# 生产者任务（调用封装函数版本）
def sync_order_data(**context):
    print("=" * 50)
    print("【生产者】开始执行同步订单数据任务")
    print("=" * 50)

    # 模拟业务数据
    order_data = {
        "order_id": "OD20260215001",
        "user_id": "U10086",
        "order_amount": 299.99,
        "order_status": "paid",
        "pay_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    print(f"【生产者】生成业务数据：{order_data}")

    try:
        # 1. 获取上下文参数
        run_id = context.get("run_id", "unknown_run_id")
        dag_id = context["dag"].dag_id
        task_id = context["task"].task_id
        print(f"【生产者】上下文参数：run_id={run_id}, dag_id={dag_id}, task_id={task_id}")

        # 2. 使用封装函数插入数据
        print("【生产者】调用封装函数插入数据...")
        insert_producer_data(run_id, dag_id, task_id, order_data, conn_id="mysql_234_crm")
        print("✅ 数据成功写入airflow_producer_data表！")

    except Exception as e:
        print(f"❌ 任务执行失败：{str(e)}")
        # 抛出异常，标记任务失败
        raise e

    print("=" * 50)
    print("【生产者】任务执行完成")
    print("=" * 50)
    return order_data


# 定义生产者DAG
with DAG(
        dag_id="producer_order_mysql",
        start_date=datetime(2026, 2, 15),
        schedule_interval=None,
        catchup=False,
        tags=["生产者", "外部数据库", "订单同步"],
        # 调试阶段：关闭任务超时，确保日志完整输出
        default_args={
            "owner": "data_team",
            "retries": 0,
            "execution_timeout": None
        }
) as producer_dag:
    sync_task = PythonOperator(
        task_id="sync_order_data",
        python_callable=sync_order_data,
        outlets=[dw_order_dataset2],
        provide_context=True,
        # 强制输出所有日志
        do_xcom_push=True
    )


# ===================== 4. 消费者DAG（读取外部数据库+业务处理） =====================
def clean_order_data(**context):
    """模拟：读取生产者数据并清洗"""
    print("【消费者】开始读取生产者数据...")
    # 读取生产者最新数据
    producer_info = get_latest_producer_data(
        dag_id="producer_order_mysql",
        task_id="sync_order_data"
    )

    # 异常处理：数据不存在则抛出错误
    if not producer_info:
        raise ValueError("【消费者】未找到生产者的最新数据！")

    # 解析生产者数据
    run_id = producer_info["run_id"]
    order_data = producer_info["result"]
    create_time = producer_info["create_time"]

    print(f"【消费者】读取到生产者数据：")
    print(f"  - Run ID: {run_id}")
    print(f"  - 写入时间: {create_time}")
    print(f"  - 业务数据: {order_data}")

    # 模拟数据清洗逻辑
    cleaned_data = order_data.copy()
    cleaned_data["order_amount"] = round(cleaned_data["order_amount"], 2)  # 格式化金额
    cleaned_data["is_valid"] = True if cleaned_data["order_status"] == "paid" else False  # 标记有效订单
    cleaned_data["clean_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"【消费者】数据清洗完成：{cleaned_data}")

    # 2. 使用封装函数插入数据
    print("【生产者】调用封装函数插入数据...")
    update_producer_data(run_id, conn_id="mysql_234_crm")
    print("✅ 数据成功写入airflow_producer_data表！")
    return cleaned_data

with DAG(
        dag_id="consumer_order_mysql",
        start_date=datetime(2026, 2, 15),
        schedule=[dw_order_dataset2],  # 监听数据集，被生产者触发
        catchup=False,
        tags=["消费者", "外部数据库", "数据清洗"]
) as consumer_dag:
    clean_task = PythonOperator(
        task_id="clean_order_data",
        python_callable=clean_order_data,
        inlets=[dw_order_dataset2],
        provide_context=True
    )

# 消费者更新数据
def update_producer_data(run_id, conn_id="mysql_234_crm"):
    try:
        mysql_hook = get_mysql_hook(conn_id)
        sql = """
        UPDATE airflow_producer_data SET status = '2' WHERE run_id = %s
        """
        mysql_hook.run(sql, parameters=(run_id))
        print(f"消费者更新status状态，已写入MySQL：status=2")
    except Exception as e:
        print(f"写入MySQL失败：{e}")
