# Datasets 仅完成了 “触发消费者 DAG” 的核心功能，但不会主动把生产者的 XCom 数据传给消费者；
# 消费者当前代码中没有 “读取生产者 XCom” 的逻辑，所以获取到的是 None。
# 解决方案：消费者主动读取生产者的 XCom
# 核心是在消费者任务中通过 Variable 临时存储生产者返回值，或直接通过 XCom API 读取生产者的 XCom 数据（推荐后者）：

import pymysql
pymysql.install_as_MySQLdb()

from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.models import TaskInstance, DagRun
from airflow.utils.session import create_session


# ===================== 1. 定义 Dataset =====================
# 用 URI 唯一标识数据集（格式：dataset://<数据源>/<表名>，自定义即可）
dataset_xcom = Dataset(
    uri="dataset://xcom",
    extra={
            "description": "直接通过 XCom API 读取生产者的 XCom 数据",
            "owner": "john",
            "version": "1.3"
        }
)

# ===================== 2. 生产者 DAG（更新数据集+ 存储返回值） =====================
# 该 DAG 执行后，会标记 dataset_xcom 为“已更新”
def producer_xcom_save_data():
    """模拟：从业务库同步订单数据到 dw_order 表"""
    # 实际场景：这里写数据库同步逻辑（如读取 MySQL → 写入数仓）
    """查询 MySQL 数据的核心函数"""
    try:
        # mysql_hook = MySqlHook(mysql_conn_id='mysql_234_crm')
        # update_sql = "UPDATE a_test1 SET sex = 6 where name='titi'"
        # mysql_hook.run(update_sql)
        #
        # test_sql = " SELECT sex FROM a_test1 where name='titi'"
        # result = mysql_hook.get_first(test_sql)

        result = ('64',)

        print(f"✅ MySQL 连接成功！测试查询结果: {result}")
        # 返回值会自动存入 XCom，key 默认为 "return_value"
        return result
    except Exception as e:
        print(f"❌ MySQL 操作失败: {str(e)}")
        raise  # 抛出异常让 Airflow 标记任务失败

with DAG(
    dag_id="producer_xcom_sync",  # 生产者DAG名称
    start_date=datetime(2026, 2, 13),
    schedule_interval=None,  # 手动触发（也可设为时间调度，如 "@daily"）
    catchup=False,
    tags=["生产者", "xcom"]
) as producer_dag:
    sync_task = PythonOperator(
        task_id="producer_xcom_save_data",
        python_callable=producer_xcom_save_data,
        # 关键：任务完成后，标记数据集已更新
        outlets=[dataset_xcom]
    )

# 封装通用读取函数
def get_producer_xcom(producer_dag_id, producer_task_id):
    xcom_value = None
    with create_session() as session:
        latest_dag_run = session.query(DagRun).filter(
            DagRun.dag_id == producer_dag_id,
            DagRun.state == "success"
        ).order_by(DagRun.execution_date.desc()).first()
        if latest_dag_run:
            ti = session.query(TaskInstance).filter(
                TaskInstance.dag_id == producer_dag_id,
                TaskInstance.task_id == producer_task_id,
                TaskInstance.run_id == latest_dag_run.run_id
            ).first()
            if ti:
                xcom_value = ti.xcom_pull(task_ids=producer_task_id, key="return_value")
    return xcom_value

# ===================== 3. 消费者 DAG（监听数据集 + 读取生产者 XCom） =====================
# 该 DAG 监听 dataset_xcom，数据更新时自动触发
def consumer_xcom_read_data1(**context):
    """模拟：清洗 dw_order 表的脏数据"""
    print("检测到订单数据更新，开始清洗...")
    # 实际场景：这里写数据清洗逻辑（如去重、补全缺失值）
    print("订单数据清洗完成！")
    print("【消费者1】检测到订单数据更新，开始清洗...")
    xcom_value = get_producer_xcom("producer_xcom_sync", "producer_xcom_save_data")
    print(f"【消费者1】从生产者获取的返回值: {xcom_value}")
    # 可选：将获取到的值存入消费者自己的 XCom
    return xcom_value

with DAG(
    dag_id="consumer_xcom1",  # 消费者DAG名称
    start_date=datetime(2026, 2, 13),
    # 关键：调度规则改为监听数据集，而非时间
    schedule=[dataset_xcom],
    catchup=False,
    tags=["消费者", "xcom1"]
) as consumer_dag:
    clean_task = PythonOperator(
        task_id="consumer_xcom_read_data1",
        python_callable=consumer_xcom_read_data1,
        # 可选：标记该DAG依赖的数据集（仅用于UI展示）
        inlets=[dataset_xcom],
        provide_context=True,  # 必须开启，让函数能接收 context 参数
        # Airflow 2.x 推荐用 op_kwargs 或 templates_dict，也可直接用 kwargs
        op_kwargs={"producer_dag_id": "producer_xcom_sync", "producer_task_id": "producer_xcom_save_data"}
    )


# ===================== 4. 消费者2：订单数据统计 =====================
def consumer_xcom_read_data2(**context):
    """统计订单数据 + 读取生产者的返回值"""
    print("【消费者2】检测到订单数据更新，开始统计...")
    xcom_value = get_producer_xcom("producer_xcom_sync", "producer_xcom_save_data")
    print(f"【消费者2】从生产者获取的返回值: {xcom_value}")
    return xcom_value


with DAG(
        dag_id="consumer_xcom2",  # 消费者2 DAG ID（需唯一）
        start_date=datetime(2026, 2, 13),
        schedule=[dataset_xcom],  # 监听同一个数据集
        catchup=False,
        tags=["消费者", "xcom2"]
) as consumer2_dag:
    stat_task = PythonOperator(
        task_id="consumer_xcom_read_data2",
        python_callable=consumer_xcom_read_data2,
        inlets=[dataset_xcom],
        provide_context=True
    )