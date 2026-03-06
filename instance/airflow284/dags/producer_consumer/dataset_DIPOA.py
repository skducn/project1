# DIPOA模型
# 将数据视作企业生产经营的原材料，“数据驱动”的过程可理解为DIPOA模型，即Data—Input—Process—Output—Action Point，数据作为生产要素，输入到数据应用的程序化链路中，经过一定步骤的加工与处理，形成相应的输出，再将这些输出作用到对应的作用点上产生价值，完成“数据驱动”的一次作业链条。

# 你想了解 Airflow Datasets 的链式依赖场景（1 个生产者→消费者 1→消费者 2，即消费者 1 同时作为下一级的生产者），核心是通过给消费者 1 标记 outlets 数据集，让消费者 2 监听该新数据集，实现 “数据驱动的链式触发”。
# 这种模式贴合实际数据处理流程（如：数据同步→数据清洗→数据统计），每个环节完成后自动触发下一个环节，而非依赖时间调度。
# 一、核心场景：链式数据集依赖（生产者→消费者 1→消费者 2）
# 我们设计一个完整的链式流程：
# 生产者 DAG：同步订单原始数据 → 更新 dataset://mysql/dataset_DIPOA_dw_order_raw；
# 消费者 1（同时是二级生产者）：清洗订单数据 → 更新 dataset://mysql/dataset_DIPOA_dw_order_cleaned；
# 消费者 2：统计清洗后的订单数据 → 监听 dataset://mysql/dataset_DIPOA_dw_order_cleaned。

# 链式依赖核心：消费者通过 outlets 标记新数据集，下一级消费者监听该数据集，实现 “生产者→消费者→消费者” 的链式触发；
# 数据集核心价值：替代传统的 ExternalTaskSensor，以 “数据” 为核心触发调度，更贴合数据处理场景；

from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from airflow.models import TaskInstance, DagRun
from airflow.utils.session import create_session
from datetime import datetime, timedelta
import pytz

# ===================== 1. 定义三级数据集（对应链式流程） =====================
# 一级数据集：原始订单数据（生产者更新）
dataset_DIPOA_dw_order_raw = Dataset(
    uri="dataset://DIPOA/dw_order_raw",
    extra={
        "description": "原始订单数据（未清洗）",
        "owner": "john",
        "version": "1.4"
    }
)
# 二级数据集：清洗后的订单数据（消费者1更新）
dataset_DIPOA_dw_order_cleaned = Dataset(
    uri="dataset://DIPOA/dw_order_cleaned",
    extra={
        "description": "清洗后的订单数据",
        "owner": "john",
        "version": "1.5"
    }
)


# ===================== 2. 一级生产者：同步原始订单数据 =====================
def sync_raw_order_data():
    """模拟：从业务库同步原始订单数据"""
    print("【一级生产者】开始同步原始订单数据...")
    raw_data = {"order_id": 1001, "user_id": 2001, "amount": 99.9, "status": "pending"}
    print(f"【一级生产者】原始数据同步完成: {raw_data}")
    return raw_data  # 存入XCom，供消费者1读取

with DAG(
        dag_id="producer_DIPOA_dw_order_raw_sync",
        start_date=datetime(2026, 2, 13),
        schedule_interval=None,  # 手动触发
        catchup=False,
        tags=["一级生产者", "数据同步"]
) as producer_dag:
    sync_raw_task = PythonOperator(
        task_id="sync_raw_order_data",
        python_callable=sync_raw_order_data,
        outlets=[dataset_DIPOA_dw_order_raw]  # 标记更新一级数据集
    )


# ===================== 3. 消费者1（二级生产者）：清洗订单数据 =====================
def clean_order_data(**context):
    """步骤1：读取一级生产者的原始数据；步骤2：清洗数据；步骤3：标记更新二级数据集"""
    # 1. 读取一级生产者的XCom数据
    producer_dag_id = "producer_DIPOA_dw_order_raw_sync"
    producer_task_id = "sync_raw_order_data"
    raw_data = None

    with create_session() as session:
        latest_run = session.query(DagRun).filter(
            DagRun.dag_id == producer_dag_id,
            DagRun.state == "success"
        ).order_by(DagRun.execution_date.desc()).first()

        if latest_run:
            ti = session.query(TaskInstance).filter(
                TaskInstance.dag_id == producer_dag_id,
                TaskInstance.task_id == producer_task_id,
                TaskInstance.run_id == latest_run.run_id
            ).first()
            if ti:
                raw_data = ti.xcom_pull(task_ids=producer_task_id, key="return_value")

    # 2. 模拟数据清洗逻辑
    print(f"【消费者1】读取到原始数据: {raw_data}")
    if raw_data:
        cleaned_data = raw_data.copy()
        cleaned_data["status"] = "completed"  # 修正状态
        cleaned_data["amount"] = round(cleaned_data["amount"], 2)  # 格式化金额
        print(f"【消费者1】数据清洗完成: {cleaned_data}")
    else:
        cleaned_data = None
        print("【消费者1】未读取到原始数据，清洗失败")

    return cleaned_data


with DAG(
        dag_id="consumer1_order_clean",
        start_date=datetime(2026, 2, 13),
        schedule=[dataset_DIPOA_dw_order_raw],  # 监听一级数据集（被生产者触发）
        catchup=False,
        tags=["消费者1", "二级生产者", "数据清洗"]
) as consumer1_dag:
    clean_task = PythonOperator(
        task_id="clean_order_data",
        python_callable=clean_order_data,
        inlets=[dataset_DIPOA_dw_order_raw],  # 标记依赖一级数据集
        outlets=[dataset_DIPOA_dw_order_cleaned],  # 标记更新二级数据集（作为二级生产者）
        provide_context=True
    )


# ===================== 4. 消费者2：统计清洗后的订单数据 =====================
def stat_order_data(**context):
    """步骤1：读取消费者1的清洗后数据；步骤2：统计数据"""
    # 1. 读取消费者1（二级生产者）的XCom数据
    producer2_dag_id = "consumer1_order_clean"
    producer2_task_id = "clean_order_data"
    cleaned_data = None

    with create_session() as session:
        latest_run = session.query(DagRun).filter(
            DagRun.dag_id == producer2_dag_id,
            DagRun.state == "success"
        ).order_by(DagRun.execution_date.desc()).first()

        if latest_run:
            ti = session.query(TaskInstance).filter(
                TaskInstance.dag_id == producer2_dag_id,
                TaskInstance.task_id == producer2_task_id,
                TaskInstance.run_id == latest_run.run_id
            ).first()
            if ti:
                cleaned_data = ti.xcom_pull(task_ids=producer2_task_id, key="return_value")

    # 2. 模拟数据统计逻辑
    print(f"【消费者2】读取到清洗后数据: {cleaned_data}")
    if cleaned_data:
        stat_result = {
            "统计时间": datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S"),
            "订单ID": cleaned_data["order_id"],
            "用户ID": cleaned_data["user_id"],
            "订单金额": cleaned_data["amount"],
            "订单状态": cleaned_data["status"],
            "统计结论": "该订单为有效完成订单"
        }
        print(f"【消费者2】数据统计完成: {stat_result}")
    else:
        stat_result = None
        print("【消费者2】未读取到清洗后数据，统计失败")

    return stat_result


with DAG(
        dag_id="consumer2_order_stat",
        start_date=datetime(2026, 2, 13),
        schedule=[dataset_DIPOA_dw_order_cleaned],  # 监听二级数据集（被消费者1触发）
        catchup=False,
        tags=["消费者2", "数据统计"]
) as consumer2_dag:
    stat_task = PythonOperator(
        task_id="stat_order_data",
        python_callable=stat_order_data,
        inlets=[dataset_DIPOA_dw_order_cleaned],  # 标记依赖二级数据集
        provide_context=True
    )