# 文件 / 对象存储（适合大数据）
# 原理
# 生产者将数据写入本地文件、CSV、JSON 或云存储（S3/OSS），消费者读取该文件。
# 适用场景
# 传递大数据（如数据文件、报表、批量处理结果）；
# 跨系统 / 跨集群传递数据（如生产者在 A 机器，消费者在 B 机器）。

from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from datetime import datetime

# ===================== 1. 定义 Dataset =====================
# 用 URI 唯一标识数据集（格式：dataset://<数据源>/<表名>，自定义即可）
dateset_object = Dataset(
    uri="dataset://object",
    extra={
            "description": "文件 / 对象存储（适合大数据）,生产者将数据写入本地文件、CSV、JSON 或云存储（S3/OSS），消费者读取该文件。",
            "owner": "john",
            "version": "1.1"
        }
)

# 生产者任务：写入JSON文件
def producer_object_save_data():
    import json
    import os
    result = {'sex': '6', 'count': 100, 'update_time': str(datetime.now())}
    # 写入本地文件（生产环境建议用S3/OSS）
    file_path = "/Users/linghuchong/Downloads/51/Python/project/instance/airflow284/data/object.json"
    with open(file_path, 'w') as f:
        json.dump(result, f)
    print(f"生产者：已将结果写入文件: {file_path}")
    return result

with DAG(
    dag_id="producer_object_sync",  # 生产者DAG名称
    start_date=datetime(2026, 2, 13),
    schedule_interval=None,  # 手动触发（也可设为时间调度，如 "@daily"）
    catchup=False,
    tags=["生产者", "object"]
) as producer_dag:
    sync_task = PythonOperator(
        task_id="producer_object_save_data",
        python_callable=producer_object_save_data,
        # 关键：任务完成后，标记数据集已更新
        outlets=[dateset_object]
    )


# 消费者任务：读取JSON文件
def consumer_object_read_data():
    import json,os
    file_path = "/Users/linghuchong/Downloads/51/Python/project/instance/airflow284/data/object.json"
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            result = json.load(f)
        print(f"消费者：从文件获取生产者数据: {result}")
        return result
    else:
        print("消费者：未找到生产者数据文件")
        return None

with DAG(
    dag_id="consumer_object",  # 消费者DAG名称
    start_date=datetime(2026, 2, 13),
    # 关键：调度规则改为监听数据集，而非时间
    schedule=[dateset_object],
    catchup=False,
    tags=["消费者", "object"]
) as consumer_dag:
    clean_task = PythonOperator(
        task_id="consumer_object_read_data",
        python_callable=consumer_object_read_data,
        # 可选：标记该DAG依赖的数据集（仅用于UI展示）
        inlets=[dateset_object],
    )
