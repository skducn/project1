# 1个生产者 → 1个消费者（1个任务）
# 功能：消费者任务1从生产者中获取Xcom值，处理后，传递给任务2处理

# 场景：
# task1 (c_1p1n_TASK1) 执行 → 返回值自动存储到XCom


import os, sys

# 添加项目根目录到Python路径
# 计算项目根目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))
print(f"Current directory: {current_dir}")
print(f"Project root: {project_root}")

if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to sys.path")

# 验证PO模块是否存在
po_path = os.path.join(project_root, 'PO')
print(f"PO module path: {po_path}")
print(f"PO module exists: {os.path.exists(po_path)}")

from PO.TimePO import *
Time_PO = TimePO()

from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from datetime import datetime as dt, timedelta
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.models import TaskInstance, DagRun
from airflow.utils.session import create_session
from airflow.configuration import conf


# ===================== 1. 定义 Dataset =====================
# 用 URI 唯一标识数据集（格式：dataset://<数据源>/<表名>，自定义即可）
dataset_1p1n = Dataset(
    uri="dataset://1p1n",
    extra={
        "description": "订单同步表 dw_order，来自业务库的订单数据",
        "owner": "john",
        "version": "1.5"
    }
)

# 封装通用读取函数
def get_xcom(varDagId, varTaskId, **context):
    """
    从指定生产者/消费者任务中获取 XCom 值
    用于消费者之间的数据传递
    """
    xcom_value = None

    try:
        with create_session() as session:
            # 查找最新的成功运行的消费者 DAG Run
            latest_dag_run = session.query(DagRun).filter(
                DagRun.dag_id == varDagId,
                DagRun.state == "success"
            ).order_by(DagRun.execution_date.desc()).first()

            if latest_dag_run:
                # 查找对应的 Task Instance
                ti = session.query(TaskInstance).filter(
                    TaskInstance.dag_id == varDagId,
                    TaskInstance.task_id == varTaskId,
                    TaskInstance.run_id == latest_dag_run.run_id
                ).first()

                if ti:
                    # 从 XCom 中拉取数据
                    xcom_value = ti.xcom_pull(task_ids=varTaskId, key="return_value")
                    print(f"✅ 成功从消费者 {varDagId}.{varTaskId} 获取 XCom 值: {xcom_value}")
                else:
                    print("⚠️ 未找到对应的消费者 Task Instance")
            else:
                print("⚠️ 未找到成功的消费者 DAG Run")
    except Exception as e:
        print(f"❌ 查询消费者 XCom 失败: {str(e)}")

    return xcom_value


# ===================== 生产者 DAG（更新数据集+ 存储返回值） =====================
# 该 DAG 执行后，会标记 dataset_1p1n 为"已更新"
def p_1p1n_TASK(**context):
    result = ('6477',)
    return result
# 生产者 DAG
with DAG(
        dag_id="p_1p1n_DAGs", start_date=dt(2026, 2, 13), schedule_interval=None,  # 手动触发（也可设为时间调度，如 "@daily"）
        catchup=False, tags=["1p1n", "生产者", "订单同步"], render_template_as_native_obj=True
) as producer_dag:
    sync_task = PythonOperator(task_id="p_1p1n_TASK", python_callable=p_1p1n_TASK, outlets=[dataset_1p1n], provide_context=True)


# ===================== 消费者的任务1 DAG（监听数据集 + 读取生产者 XCom） =====================
# 该 DAG 监听 dataset_1p1n，数据更新时自动触发
def c_1p1n_TASK1(**context):
    # 读取生产者的返回值
    xcom_value = get_xcom("p_1p1n_DAGs", "p_1p1n_TASK", **context)
    print(f"【消费者任务1】从生产者获取的返回值: {xcom_value}")
    print(Time_PO.getDateTimeByMinus())
    xcom_value = int(xcom_value[0]) + 1
    return xcom_value


# 消费者 DAG 调度任务1
with DAG(
        dag_id="c_1p1n", start_date=dt(2026, 2, 13), schedule=[dataset_1p1n], catchup=False,
        tags=["1p1n", "消费者", "任务1：数据清洗", "任务2：处理数据"], render_template_as_native_obj=True
) as consumer_dag:
    task1 = PythonOperator(task_id="c_1p1n_TASK1", python_callable=c_1p1n_TASK1, provide_context=True)

