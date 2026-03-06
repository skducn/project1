# 2个生产者 → 1个消费者
# 功能：消费者 DAG 同时监听多个数据集，仅当所有生产者都更新了对应数据集后，消费者才会被触发。
# 场景：订单数据 + 用户数据 都同步完成后，才执行 “订单 - 用户关联分析”

from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from airflow.models import TaskInstance, DagRun
from airflow.utils.session import create_session
from datetime import datetime, timedelta
import pytz

# ===================== 1. 定义两个独立数据集（对应两个生产者） =====================
# 数据集1：订单数据
dw_order_dataset = Dataset(
    uri="dataset://N_1/dw_order",
    extra = {
        "description": "订单同步表：来自业务库的订单核心数据",
        "owner": "john",
        "version": "1.5"
    }
)
# 数据集2：用户数据
dw_user_dataset = Dataset(
    uri="dataset://N_1/dw_user",
    extra = {
        "description": "用户同步表：来自业务库的用户核心数据",
        "owner": "john",
        "version": "1.5"
    }
)


# ===================== 2. 生产者1：同步订单数据 =====================
def sync_order_data():
    """模拟：从业务库同步订单数据到数仓 dw_order 表"""
    print("【生产者1-订单】开始同步订单数据...")
    # 模拟订单数据（实际场景：替换为MySQL查询/同步逻辑）
    order_data = {
        "order_id": "OD20260214001",
        "user_id": "U10086",
        "order_amount": 199.99,
        "order_time": datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")
    }
    print(f"【生产者1-订单】订单数据同步完成：{order_data}")
    return order_data  # 存入XCom，供消费者读取
with DAG(
        dag_id="p_2p1n_dw_order_sync",  # 生产者1 DAG ID
        start_date=datetime(2026, 2, 14),
        schedule_interval=None,  # 手动触发
        catchup=False,
        tags=["2p1n", "生产者1", "订单同步"]
) as producer1_dag:
    sync_order_task = PythonOperator(
        task_id="sync_order_data",
        python_callable=sync_order_data,
        outlets=[dw_order_dataset]  # 标记更新订单数据集
    )


# ===================== 3. 生产者2：同步用户数据 =====================
def sync_user_data():
    """模拟：从业务库同步用户数据到数仓 dw_user 表"""
    print("【生产者2-用户】开始同步用户数据...")
    # 模拟用户数据（实际场景：替换为MySQL查询/同步逻辑）
    user_data = {
        "user_id": "U10086",
        "user_name": "张三",
        "user_phone": "13800138000",
        "user_reg_time": "2026-01-01 10:00:00"
    }
    print(f"【生产者2-用户】用户数据同步完成：{user_data}")
    return user_data  # 存入XCom，供消费者读取


with DAG(
        dag_id="p_2p1n_dw_user_sync",
        start_date=datetime(2026, 2, 14),
        schedule_interval=None,  # 手动触发
        catchup=False,
        tags=["2p1n","生产者2", "用户同步"]
) as producer2_dag:
    sync_user_task = PythonOperator(
        task_id="sync_user_data",
        python_callable=sync_user_data,
        outlets=[dw_user_dataset]  # 标记更新用户数据集
    )


# ===================== 4. 消费者：订单-用户关联分析（依赖两个生产者） =====================
def analyze_order_user(**context):
    """
    核心逻辑：
    1. 读取生产者1（订单）的XCom数据
    2. 读取生产者2（用户）的XCom数据
    3. 执行关联分析
    """

    # 工具函数：读取指定生产者的最新XCom数据
    def get_producer_xcom(producer_dag_id, producer_task_id):
        xcom_value = None
        with create_session() as session:
            # 查询最新成功运行的生产者DagRun
            latest_run = session.query(DagRun).filter(
                DagRun.dag_id == producer_dag_id,
                DagRun.state == "success",
                # DagRun.execution_date >= datetime.now() - timedelta(hours=1)  # 限定1小时内
                # DagRun.execution_date >= datetime.now(pytz.timezone("Asia/Shanghai")) - timedelta(hours=1)
            ).order_by(DagRun.execution_date.desc()).first()

            if latest_run:
                # 查询对应TaskInstance的XCom
                ti = session.query(TaskInstance).filter(
                    TaskInstance.dag_id == producer_dag_id,
                    TaskInstance.task_id == producer_task_id,
                    TaskInstance.run_id == latest_run.run_id
                ).first()
                if ti:
                    xcom_value = ti.xcom_pull(task_ids=producer_task_id, key="return_value")
        return xcom_value

    # 步骤1：读取两个生产者的数据
    order_data = get_producer_xcom("p_2p1n_dw_order_sync", "sync_order_data")
    user_data = get_producer_xcom("p_2p1n_dw_user_sync", "sync_user_data")

    # 步骤2：校验数据是否完整
    if not order_data or not user_data:
        raise ValueError(f"数据源不完整！订单数据：{order_data}，用户数据：{user_data}")

    # 步骤3：执行关联分析
    print("【消费者】开始订单-用户关联分析...")
    analysis_result = {
        "分析时间": datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S"),
        "关联订单ID": order_data["order_id"],
        "关联用户ID": user_data["user_id"],
        "用户姓名": user_data["user_name"],
        "订单金额": order_data["order_amount"],
        "用户手机号": user_data["user_phone"],
        "分析结论": f"用户{user_data['user_name']}（{user_data['user_phone']}）于{order_data['order_time']}下单，金额{order_data['order_amount']}元"
    }

    print(f"【消费者】关联分析完成！结果：{analysis_result}")
    return analysis_result


with DAG(
        dag_id="c_2p1n_order_user_analysis",  # 消费者DAG ID
        start_date=datetime(2026, 2, 14),
        # 关键配置：同时监听两个数据集（必须都更新才触发）
        schedule=[dw_order_dataset, dw_user_dataset],
        catchup=False,
        tags=["2p1n","消费者", "多数据源依赖", "关联分析"]
) as consumer_dag:
    analyze_task = PythonOperator(
        task_id="analyze_order_user",
        python_callable=analyze_order_user,
        # 标记依赖的数据集（仅UI展示，不影响触发逻辑）
        inlets=[dw_order_dataset, dw_user_dataset],
        provide_context=True  # 传递上下文，用于XCom查询
    )