# 完整的链式传递：生产者 → 消费者1 → 消费者2 → 消费者3 (废弃)
# 功能：消费者1从生产者中获取Xcom值，消费者1处理XCom值后，消费者2再从消费者1中获取XCom值

# 生产者 → 更新数据集
# 消费者1 → 被触发 → 处理数据 → 触发消费者2
# 消费者2 → 被触发 → 处理消费者1的结果 → 触发消费者3
# 消费者3 → 被触发 → 处理消费者2的结果 → 完成

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
from datetime import datetime, timedelta
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.models import TaskInstance, DagRun
from airflow.utils.session import create_session
from airflow.configuration import conf

from airflow.operators.trigger_dagrun import TriggerDagRunOperator

# ===================== 1. 定义 Dataset =====================
# 用 URI 唯一标识数据集（格式：dataset://<数据源>/<表名>，自定义即可）
dataset_1p1n1n = Dataset(
    uri="dataset://1p1n1n",
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
# 该 DAG 执行后，会标记 dataset_1p1n1n 为"已更新"
def p_1p1n1n_TASK(**context):
    """模拟：从业务库同步订单数据到 dw_order 表"""
    print("开始同步订单数据...")
    result = ('333',)
    return result
# 生产者 DAG
with DAG(
        dag_id="p_1p1n1n_DAGs",  # 生产者DAG名称
        start_date=datetime(2026, 2, 13),
        schedule_interval=None,  # 手动触发（也可设为时间调度，如 "@daily"）
        catchup=False,
        tags=["1p1n1n", "生产者", "订单同步"],
        # 添加 Dataset 相关配置
        render_template_as_native_obj=True
) as producer_dag:
    sync_task = PythonOperator(
        task_id="p_1p1n1n_TASK",
        python_callable=p_1p1n1n_TASK,
        # 关键：任务完成后，标记数据集已更新
        outlets=[dataset_1p1n1n],
        provide_context=True
    )



# ===================== 消费者1 DAG（监听数据集 + 读取生产者 XCom） =====================
# 该 DAG 监听 dataset_1p1n1n，数据更新时自动触发
def c_1p1n1n_TASK1(**context):
    print("检测到订单数据更新，开始清洗...")
    # 读取生产者的返回值
    xcom_value = get_xcom("p_1p1n1n_DAGs", "p_1p1n1n_TASK", **context)
    print(f"【消费者1】从生产者获取的返回值: {xcom_value}")
    print(Time_PO.getDateTimeByMinus())
    xcom_value = int(xcom_value[0]) + 1
    return xcom_value

# 消费者1 DAG
with DAG(
        dag_id="c_1p1n1n_DAG1",
        start_date=datetime(2026, 2, 13),
        schedule=[dataset_1p1n1n],
        catchup=False,
        tags=["1p1n1n", "消费者1", "数据清洗"],
        # 确保 Dataset 功能启用
        render_template_as_native_obj=True
) as consumer1_dag:
    clean_task = PythonOperator(
        task_id="c_1p1n1n_TASK1",
        python_callable=c_1p1n1n_TASK1,
        provide_context=True
    )

    # 添加触发消费者2的任务
    trigger_consumer2 = TriggerDagRunOperator(
        task_id='trigger_consumer2',
        trigger_dag_id='c_1p1n1n_DAG2',
        wait_for_completion=False
    )

    clean_task >> trigger_consumer2


# ===================== 消费者2 DAG（监听数据集 + 读取生产者 XCom） =====================
def c_1p1n1n_TASK2(**context):
    """统计订单数据 + 读取消费者1的返回值"""
    print("【消费者2】检测到订单数据更新，开始统计...")
    # 修改：从消费者1获取XCom值，而不是从生产者获取
    xcom_value = get_xcom("c_1p1n1n_DAG1", "c_1p1n1n_TASK1", **context)
    print(f"【消费者2】从消费者1获取的返回值: {xcom_value}")
    # 对获取到的值进行处理
    if xcom_value is not None:
        processed_value = xcom_value + 100  # 示例处理逻辑
        print(f"【消费者2】处理后的值: {processed_value}")
        print(Time_PO.getDateTimeByMinus())
        return processed_value
    else:
        print("【消费者2】未能获取到消费者1的数据")
        return None
# 消费者2 DAG
with DAG(
        dag_id="c_1p1n1n_DAG2",
        start_date=datetime(2026, 2, 13),
        schedule=None,
        catchup=False,
        tags=["1p1n1n", "消费者2", "数据统计"],
        render_template_as_native_obj=True
) as consumer2_dag:
    stat_task = PythonOperator(
        task_id="c_1p1n1n_TASK2",
        python_callable=c_1p1n1n_TASK2,
        provide_context=True
    )

    # 添加触发消费者3的任务
    trigger_consumer3 = TriggerDagRunOperator(
        task_id='trigger_consumer3',
        trigger_dag_id='c_1p1n1n_DAG3',
        wait_for_completion=False
    )

    stat_task >> trigger_consumer3


# ===================== 消费者3 DAG（处理消费者2的结果） =====================
def c_1p1n1n_TASK3(**context):
    """最终处理 + 读取消费者2的返回值"""
    print("【消费者3】开始最终处理...")
    # 从消费者2获取XCom值
    xcom_value = get_xcom("c_1p1n1n_DAG2", "c_1p1n1n_TASK2", **context)
    print(f"【消费者3】从消费者2获取的返回值: {xcom_value}")
    # 对获取到的值进行最终处理
    if xcom_value is not None:
        final_value = xcom_value * 2  # 示例最终处理逻辑
        print(f"【消费者3】最终处理后的值: {final_value}")
        print(Time_PO.getDateTimeByMinus())
        return final_value
    else:
        print("【消费者3】未能获取到消费者2的数据")
        return None

# 消费者3 DAG
with DAG(
        dag_id="c_1p1n1n_DAG3",
        start_date=datetime(2026, 2, 13),
        schedule=None,
        catchup=False,
        tags=["1p1n1n", "消费者3", "最终处理"],
        render_template_as_native_obj=True
) as consumer3_dag:
    final_task = PythonOperator(
        task_id="c_1p1n1n_TASK3",
        python_callable=c_1p1n1n_TASK3,
        provide_context=True
    )

