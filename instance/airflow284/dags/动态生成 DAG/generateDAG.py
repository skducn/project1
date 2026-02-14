from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import yaml

# 1. 定义DAG配置文件（可存于数据库/配置中心）
DAG_CONFIG_YAML = """
- dag_id: dynamic_dag_store_001
  schedule: "@daily"
  store_id: "001"
  store_name: "北京朝阳店"
  default_args:
    owner: "data_team"
    retries: 1
    retry_delay: 30
- dag_id: dynamic_dag_store_002
  schedule: "@daily"
  store_id: "002"
  store_name: "上海浦东店"
  default_args:
    owner: "data_team"
    retries: 1
    retry_delay: 30
"""

# 2. 解析配置并动态生成DAG
config_list = yaml.safe_load(DAG_CONFIG_YAML)

def sync_store_data(store_id, store_name, **kwargs):
    """通用的门店数据同步逻辑"""
    print(f"开始同步【{store_name}（ID:{store_id}）】的销售数据...")
    # 实际业务逻辑：根据store_id查询对应门店数据
    sync_result = {
        "store_id": store_id,
        "store_name": store_name,
        "sync_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "success"
    }
    print(f"同步完成：{sync_result}")
    return sync_result

# 3. 循环生成DAG
for config in config_list:
    dag_id = config["dag_id"]
    store_id = config["store_id"]
    store_name = config["store_name"]
    schedule = config["schedule"]
    default_args = {
        "owner": config["default_args"]["owner"],
        "retries": config["default_args"]["retries"],
        "retry_delay": timedelta(seconds=config["default_args"]["retry_delay"]),
        "start_date": datetime(2026, 2, 14),
        "catchup": False
    }

    # 动态创建DAG对象
    dag = DAG(
        dag_id=dag_id,
        default_args=default_args,
        schedule_interval=schedule,
        tags=["动态DAG", "门店同步", store_id]
    )

    # 动态添加任务
    with dag:
        sync_task = PythonOperator(
            task_id=f"sync_store_{store_id}_data",
            python_callable=sync_store_data,
            op_kwargs={"store_id": store_id, "store_name": store_name},
            provide_context=True
        )

    # 将DAG注册到Airflow
    globals()[dag_id] = dag