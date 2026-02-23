# 链式传递：1 个生产者 → 2个消费者
# 功能：N个消费者同时从生产者中获取Xcom值


from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.models import TaskInstance, DagRun
from airflow.utils.session import create_session
from airflow.configuration import conf

# ===================== 1. 定义 Dataset =====================
# 用 URI 唯一标识数据集（格式：dataset://<数据源>/<表名>，自定义即可）
dataset_1p2n = Dataset(
    uri="dataset://1p2n",
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
# 该 DAG 执行后，会标记 dataset_1p2n 为"已更新"
def p_1p2n_TASK(**context):
    """模拟：从业务库同步订单数据到 dw_order 表"""
    result = ('6477',)
    return result
# 生产者 DAG
with DAG(
        dag_id="p_1p2n_DAGs",  # 生产者DAG名称
        start_date=datetime(2026, 2, 13),
        schedule_interval=None,  # 手动触发（也可设为时间调度，如 "@daily"）
        catchup=False,
        tags=["1p2n", "生产者", "订单同步"],
        # 添加 Dataset 相关配置
        render_template_as_native_obj=True
) as producer_dag:
    sync_task = PythonOperator(
        task_id="p_1p2n_TASK",
        python_callable=p_1p2n_TASK,
        # 关键：任务完成后，标记数据集已更新
        outlets=[dataset_1p2n],
        provide_context=True
    )


# ===================== 消费者1 DAG（监听数据集 + 读取生产者 XCom） =====================
# 该 DAG 监听 dataset_1p2n，数据更新时自动触发
def c_1p2n_TASK1(**context):
    # 读取生产者的返回值
    xcom_value = get_xcom("p_1p2n_DAGs", "p_1p2n_TASK", **context)
    print(f"【消费者1】从生产者获取的返回值: {xcom_value}")
    return xcom_value
# 消费者1 DAG
with DAG(
        dag_id="c_1p2n_DAG1",  # 消费者DAG名称
        start_date=datetime(2026, 2, 13),
        # 关键：调度规则改为监听数据集，而非时间
        schedule=[dataset_1p2n],
        catchup=False,
        tags=["1p2n", "消费者1", "数据清洗"],
        # 确保 Dataset 功能启用
        render_template_as_native_obj=True
) as consumer_dag:
    clean_task = PythonOperator(
        task_id="c_1p2n_TASK1",
        python_callable=c_1p2n_TASK1,
        # 可选：标记该DAG依赖的数据集（仅用于UI展示）
        inlets=[dataset_1p2n],
        provide_context=True
    )

def c_1p2n_TASK2(**context):
    """统计订单数据 + 读取生产者的返回值"""
    print("【消费者2】检测到订单数据更新，开始统计...")
    xcom_value = get_xcom("p_1p2n_DAGs", "p_1p2n_TASK", **context)
    print(f"【消费者2】从生产者获取的返回值: {xcom_value}")
    return xcom_value
# 消费者2 DAG
with DAG(
        dag_id="c_1p2n_DAG2",  # 消费者2 DAG ID（需唯一）
        start_date=datetime(2026, 2, 13),
        schedule=[dataset_1p2n],  # 监听同一个数据集
        catchup=False,
        tags=["1p2n", "消费者2", "数据统计", "测试用例", "病毒", "工作流"],
        render_template_as_native_obj=True
) as consumer2_dag:
    stat_task = PythonOperator(
        task_id="c_1p2n_TASK2",
        python_callable=c_1p2n_TASK2,
        inlets=[dataset_1p2n],
        provide_context=True
    )
