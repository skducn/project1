# 1 个生产者 → 多个并行消费者
# Datasets 仅完成了 "触发消费者 DAG" 的核心功能，但不会主动把生产者的 XCom 数据传给消费者；
# 消费者当前代码中没有 "读取生产者 XCom" 的逻辑，所以获取到的是 None。
# 解决方案：消费者主动读取生产者的 XCom
# 以下是修改后的完整代码，核心是在消费者任务中通过 Variable 临时存储生产者返回值，或直接通过 XCom API 读取生产者的 XCom 数据（推荐后者）：
#

import pymysql
pymysql.install_as_MySQLdb()

from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.models import TaskInstance, DagRun
from airflow.utils.session import create_session
from airflow.configuration import conf

# ===================== 1. 定义 Dataset =====================
# 用 URI 唯一标识数据集（格式：dataset://<数据源>/<表名>，自定义即可）
dataset_1_N = Dataset(
    uri="dataset://mysql/1_N",
    extra={
        "description": "订单同步表 dw_order，来自业务库的订单数据",
        "owner": "john",
        "version": "1.5"
    }
)


# ===================== 2. 生产者 DAG（更新数据集+ 存储返回值） =====================
# 该 DAG 执行后，会标记 dataset_1_N 为"已更新"
def producer_1_N_save_data(**context):
    """模拟：从业务库同步订单数据到 dw_order 表"""
    print("开始同步订单数据...")
    # 实际场景：这里写数据库同步逻辑（如读取 MySQL → 写入数仓）
    print("订单数据同步完成！已更新 dw_order 表")
    """查询 MySQL 数据的核心函数"""
    try:
        # mysql_hook = MySqlHook(mysql_conn_id='mysql_234_crm')
        # update_sql = "UPDATE a_test1 SET sex = 6 where name='titi'"
        # mysql_hook.run(update_sql)
        #
        # test_sql = " SELECT sex FROM a_test1 where name='titi'"
        # result = mysql_hook.get_first(test_sql)

        result = ('6477',)

        print(f"✅ MySQL 连接成功！测试查询结果: {result}")
        # 返回值会自动存入 XCom，key 默认为 "return_value"
        return result
    except Exception as e:
        print(f"❌ MySQL 操作失败: {str(e)}")
        raise  # 抛出异常让 Airflow 标记任务失败


# 封装通用读取函数
def get_producer_xcom(producer_dag_id, producer_task_id, **context):
    """
    从生产者任务中获取 XCom 值
    注意：此函数在消费者 DAG 中调用时，需要等待生产者任务完成
    """
    xcom_value = None

    # 方法1：使用 context 获取上游任务的 XCom（推荐）
    if context and 'task_instance' in context:
        # 尝试从上下文获取
        ti = context['task_instance']
        # 注意：这种方式需要正确的依赖关系设置
        pass

    # 方法2：直接查询数据库（更可靠）
    try:
        with create_session() as session:
            # 查找最新的成功运行的生产者 DAG Run
            latest_dag_run = session.query(DagRun).filter(
                DagRun.dag_id == producer_dag_id,
                DagRun.state == "success"
            ).order_by(DagRun.execution_date.desc()).first()

            if latest_dag_run:
                # 查找对应的 Task Instance
                ti = session.query(TaskInstance).filter(
                    TaskInstance.dag_id == producer_dag_id,
                    TaskInstance.task_id == producer_task_id,
                    TaskInstance.run_id == latest_dag_run.run_id
                ).first()

                if ti:
                    # 从 XCom 中拉取数据
                    xcom_value = ti.xcom_pull(task_ids=producer_task_id, key="return_value")
                    print(f"✅ 成功从生产者获取 XCom 值: {xcom_value}")
                else:
                    print("⚠️ 未找到对应的 Task Instance")
            else:
                print("⚠️ 未找到成功的生产者 DAG Run")
    except Exception as e:
        print(f"❌ 查询 XCom 失败: {str(e)}")

    return xcom_value


# ===================== 3. 消费者 DAG（监听数据集 + 读取生产者 XCom） =====================
# 该 DAG 监听 dataset_1_N，数据更新时自动触发
def consumer_1_N_read_clean_order_data(**context):
    """模拟：清洗 dw_order 表的脏数据"""
    print("检测到订单数据更新，开始清洗...")
    # 实际场景：这里写数据清洗逻辑（如去重、补全缺失值）
    print("订单数据清洗完成！")
    print("【消费者1】检测到订单数据更新，开始清洗...")

    # 读取生产者的返回值
    xcom_value = get_producer_xcom("producer_1_N_sync", "producer_1_N_save_data", **context)
    print(f"【消费者1】从生产者获取的返回值: {xcom_value}")

    # 可选：将获取到的值存入消费者自己的 XCom
    return xcom_value


def consumer_1_N_read_stat_order_data(**context):
    """统计订单数据 + 读取生产者的返回值"""
    print("【消费者2】检测到订单数据更新，开始统计...")
    xcom_value = get_producer_xcom("producer_1_N_sync", "producer_1_N_save_data", **context)
    print(f"【消费者2】从生产者获取的返回值: {xcom_value}")
    return xcom_value


# 生产者 DAG
with DAG(
        dag_id="producer_1_N_sync",  # 生产者DAG名称
        start_date=datetime(2026, 2, 13),
        schedule_interval=None,  # 手动触发（也可设为时间调度，如 "@daily"）
        catchup=False,
        tags=["1N", "生产者", "订单同步"],
        # 添加 Dataset 相关配置
        render_template_as_native_obj=True
) as producer_dag:
    sync_task = PythonOperator(
        task_id="producer_1_N_save_data",
        python_callable=producer_1_N_save_data,
        # 关键：任务完成后，标记数据集已更新
        outlets=[dataset_1_N],
        provide_context=True
    )

# 消费者1 DAG
with DAG(
        dag_id="consumer_1_N_clean_order_data",  # 消费者DAG名称
        start_date=datetime(2026, 2, 13),
        # 关键：调度规则改为监听数据集，而非时间
        schedule=[dataset_1_N],
        catchup=False,
        tags=["1N", "消费者1", "数据清洗"],
        # 确保 Dataset 功能启用
        render_template_as_native_obj=True
) as consumer_dag:
    clean_task = PythonOperator(
        task_id="consumer_1_N_read_clean_order_data",
        python_callable=consumer_1_N_read_clean_order_data,
        # 可选：标记该DAG依赖的数据集（仅用于UI展示）
        inlets=[dataset_1_N],
        provide_context=True
    )

# 消费者2 DAG
with DAG(
        dag_id="consumer_1_N_stat_order_data",  # 消费者2 DAG ID（需唯一）
        start_date=datetime(2026, 2, 13),
        schedule=[dataset_1_N],  # 监听同一个数据集
        catchup=False,
        tags=["1N", "消费者2", "数据统计"],
        render_template_as_native_obj=True
) as consumer2_dag:
    stat_task = PythonOperator(
        task_id="consumer_1_N_read_stat_order_data",
        python_callable=consumer_1_N_read_stat_order_data,
        inlets=[dataset_1_N],
        provide_context=True
    )
