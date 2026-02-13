# Airflow Variable 是 Airflow 内置的键值对存储（基于元数据库），
# 可全局读写，生产者将数据存入 Variable，消费者直接读取。
# 适用场景
# 传递小数据（如单个值、短字符串、简单字典）；
# 不需要严格的 “一次触发对应一次数据”（Variable 是全局覆盖的）。

from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from datetime import datetime

# ===================== 1. 定义 Dataset =====================
# 用 URI 唯一标识数据集（格式：dataset://<数据源>/<表名>，自定义即可）
dateset_variable = Dataset(
    uri="dataset://variable",
    extra={
            "description": "使用Variable存储（基于元数据库）",
            "owner": "john",
            "version": "1.0"
        }
)

# 生产者任务：存入 Variable
def producer_variable_save_data():
    from airflow.models import Variable
    result = ('6',)
    # 序列化存储（支持复杂类型，如列表/元组）
    Variable.set("variable_sync_result", result, serialize_json=True)
    print(f"生产者：已将结果存入 Variable: {result}")
    return result

with DAG(
    dag_id="producer_variable_sync",  # 生产者DAG名称
    start_date=datetime(2026, 2, 13),
    schedule_interval=None,  # 手动触发（也可设为时间调度，如 "@daily"）
    catchup=False,
    tags=["生产者", "variable"]
) as producer_dag:
    sync_task = PythonOperator(
        task_id="producer_variable_save_data",
        python_callable=producer_variable_save_data,
        # 关键：任务完成后，标记数据集已更新
        outlets=[dateset_variable]
    )


# 消费者任务：读取 Variable
def consumer_variable_read_data():
    from airflow.models import Variable
    import json
    # 反序列化读取
    result = Variable.get("variable_sync_result", deserialize_json=True)
    print(f"消费者：从 Variable 获取生产者数据: {result}")
    return result

with DAG(
    dag_id="consumer_variable",  # 消费者DAG名称
    start_date=datetime(2026, 2, 13),
    # 关键：调度规则改为监听数据集，而非时间
    schedule=[dateset_variable],
    catchup=False,
    tags=["消费者", "variable"]
) as consumer_dag:
    clean_task = PythonOperator(
        task_id="consumer_variable_read_data",
        python_callable=consumer_variable_read_data,
        # 可选：标记该DAG依赖的数据集（仅用于UI展示）
        inlets=[dateset_variable],
    )
