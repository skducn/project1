import pymysql
pymysql.install_as_MySQLdb()

from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.models import TaskInstance, DagRun
from airflow.utils.session import create_session


# def query_mysql_data():
#     """查询 MySQL 数据的核心函数"""
#     try:
#         mysql_hook = MySqlHook(mysql_conn_id='mysql_234_crm')
#         test_sql = " SELECT sex FROM a_test1 "
#         result = mysql_hook.get_first(test_sql)
#         print(f"✅ MySQL 连接成功！测试查询结果: {result}")
#         return result
#     except Exception as e:
#         print(f"❌ MySQL 操作失败: {str(e)}")
#         raise  # 抛出异常让 Airflow 标记任务失败


# ===================== 1. 定义 Dataset =====================
# 用 URI 唯一标识数据集（格式：dataset://<数据源>/<表名>，自定义即可）
dw_order_dataset = Dataset(
    uri="dataset://mysql/dw_order",
    # description="订单同步表 dw_order，来自业务库的订单数据"
    extra={
            "description": "订单同步表 dw_order，来自业务库的订单数据",
            "owner": "data_team",
            "version": "1.0"
        }
)

# ===================== 2. 生产者 DAG（更新数据集） =====================
# 该 DAG 执行后，会标记 dw_order_dataset 为“已更新”
def sync_order_data():
    """模拟：从业务库同步订单数据到 dw_order 表"""
    print("开始同步订单数据...")
    # 实际场景：这里写数据库同步逻辑（如读取 MySQL → 写入数仓）
    print("订单数据同步完成！已更新 dw_order 表")
    """查询 MySQL 数据的核心函数"""
    try:
        mysql_hook = MySqlHook(mysql_conn_id='mysql_234_crm')
        # 更新 sex 字段为 2
        update_sql = "UPDATE a_test1 SET sex = 6 where name='titi'"
        mysql_hook.run(update_sql)

        test_sql = " SELECT sex FROM a_test1 where name='titi'"
        result = mysql_hook.get_first(test_sql)
        print(f"✅ MySQL 连接成功！测试查询结果: {result}")
        return result
    except Exception as e:
        print(f"❌ MySQL 操作失败: {str(e)}")
        raise  # 抛出异常让 Airflow 标记任务失败

with DAG(
    dag_id="producer_dw_order_sync",  # 生产者DAG名称
    start_date=datetime(2026, 2, 13),
    schedule_interval=None,  # 手动触发（也可设为时间调度，如 "@daily"）
    catchup=False,
    tags=["生产者", "订单同步"]
) as producer_dag:
    sync_task = PythonOperator(
        task_id="sync_order_data",
        python_callable=sync_order_data,
        # 关键：任务完成后，标记数据集已更新
        outlets=[dw_order_dataset]
    )

# ===================== 3. 消费者 DAG（监听数据集） =====================
# 该 DAG 监听 dw_order_dataset，数据更新时自动触发
def clean_order_data(**context):
    """模拟：清洗 dw_order 表的脏数据"""
    print("检测到订单数据更新，开始清洗...")
    # 实际场景：这里写数据清洗逻辑（如去重、补全缺失值）
    print("订单数据清洗完成！")

    # 核心逻辑：读取生产者 DAG 的最新 XCom 数据
    producer_dag_id = "producer_dw_order_sync"
    producer_task_id = "sync_order_data"
    xcom_value = None

    # 使用 Airflow 会话查询生产者最新一次成功运行的 XCom
    with create_session() as session:
        # 1. 获取生产者 DAG 最新的成功运行记录
        latest_dag_run = session.query(DagRun).filter(
            DagRun.dag_id == producer_dag_id,
            DagRun.state == "success"  # 只取成功的运行
        ).order_by(DagRun.execution_date.desc()).first()

        if latest_dag_run:
            # 2. 根据 DagRun ID 获取对应的 TaskInstance
            ti = session.query(TaskInstance).filter(
                TaskInstance.dag_id == producer_dag_id,
                TaskInstance.task_id == producer_task_id,
                TaskInstance.run_id == latest_dag_run.run_id
            ).first()

            # 3. 读取 XCom 中的 return_value
            if ti:
                xcom_value = ti.xcom_pull(
                    task_ids=producer_task_id,
                    key="return_value",  # PythonOperator 默认的 XCom key
                    dag_id=producer_dag_id
                )

    print(f"订单数据清洗完成！")
    print(f"从生产者获取的返回值: {xcom_value}")
    return xcom_value  # 可选：将获取到的值存入消费者自己的 XCom


    # 从 XCom 中获取 query_mysql_data 任务的返回值
    # result = context['task_instance'].xcom_pull(task_ids='sync_order_data')
    # # result = context['task_instance'].xcom_pull(task_ids='sync_order_data', key='return_value')
    # print(f"从 XCom 获取的结果: {result}")

with DAG(
    dag_id="consumer_dw_order_clean",  # 消费者DAG名称
    start_date=datetime(2026, 2, 13),
    # 关键：调度规则改为监听数据集，而非时间
    schedule=[dw_order_dataset],
    catchup=False,
    tags=["消费者", "数据清洗"]
) as consumer_dag:
    clean_task = PythonOperator(
        task_id="clean_order_data",
        python_callable=clean_order_data,
        # 可选：标记该DAG依赖的数据集（仅用于UI展示）
        inlets=[dw_order_dataset],
        provide_context=True,  # 必须开启，让函数能接收 context 参数
        # Airflow 2.x 推荐用 op_kwargs 或 templates_dict，也可直接用 kwargs
        op_kwargs={"producer_dag_id": "producer_dw_order_sync", "producer_task_id": "sync_order_data"}
    )
