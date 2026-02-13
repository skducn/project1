# Airflow DagRun 关联（读取生产者运行元数据）
# 原理
# 通过 Airflow 内置的 DagRun 模型，读取生产者 DAG 的运行元数据（如运行 ID、执行时间、状态），再结合业务逻辑关联数据。
# 输出：[2026-02-13, 22:18:45 CST] {logging_mixin.py:190} INFO - 消费者：生产者运行元数据: {'run_id': 'manual__2026-02-13T14:18:33.086772+00:00', 'execution_date': datetime.datetime(2026, 2, 13, 22, 18, 33, 86772, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>), 'start_date': datetime.datetime(2026, 2, 13, 22, 18, 36, 832831, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>), 'end_date': datetime.datetime(2026, 2, 13, 22, 18, 42, 914955, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)}
# 适用场景
# 不需要传递具体业务数据，仅需获取生产者的运行状态 / 时间 / ID；
# 需基于生产者的运行元数据做后续逻辑（如 “仅处理 1 小时内的生产者运行”）。


from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.utils import timezone
import pytz  # 需安装：pip install pytz
# ===================== 1. 定义 Dataset =====================
# 用 URI 唯一标识数据集（格式：dataset://<数据源>/<表名>，自定义即可）
dateset_dagRun = Dataset(
    uri="dataset://dagRun",
    extra={
            "description": "通过 Airflow 内置的 DagRun 模型，读取生产者 DAG 的运行元数据（如运行 ID、执行时间、状态），再结合业务逻辑关联数据。",
            "owner": "john",
            "version": "1.2"
        }
)

def producer_dagRun_read_data():
    """模拟：从业务库同步订单数据到 dw_order 表"""
    print("开始同步订单数据...")
    # 实际场景：这里写数据库同步逻辑（如读取 MySQL → 写入数仓）
    print("订单数据同步完成！已更新 dw_order 表")
    """查询 MySQL 数据的核心函数"""
    try:

        result = ('64',)

        print(f"✅ MySQL 连接成功！测试查询结果: {result}")
        # 返回值会自动存入 XCom，key 默认为 "return_value"
        return result
    except Exception as e:
        print(f"❌ MySQL 操作失败: {str(e)}")
        raise  # 抛出异常让 Airflow 标记任务失败

with DAG(
    dag_id="producer_dagRun_sync",  # 生产者DAG名称
    start_date=datetime(2026, 2, 13),
    schedule_interval=None,  # 手动触发（也可设为时间调度，如 "@daily"）
    catchup=False,
    tags=["生产者", "dagRun"]
) as producer_dag:
    sync_task = PythonOperator(
        task_id="producer_dagRun_read_data",
        python_callable=producer_dagRun_read_data,
        # 关键：任务完成后，标记数据集已更新
        outlets=[dateset_dagRun]
    )


# 消费者任务：读取生产者DagRun元数据 + 关联业务数据
def consumer_dagRun_read_data():
    from airflow.models import DagRun
    from airflow.utils.session import create_session
    import datetime

    # 定义上海时区
    shanghai_tz = pytz.timezone('Asia/Shanghai')
    utc_tz = pytz.timezone('UTC')

    # 获取带时区的当前时间
    # now = timezone.utcnow()  # 或 timezone.make_aware(datetime.datetime.now())
    # 获取带时区的当前时间，并转换为上海时区
    now_utc = timezone.utcnow()  # 获取UTC时间
    now_shanghai = now_utc.astimezone(shanghai_tz)  # 转换为上海时间


    # 获取生产者最新成功的DagRun
    with create_session() as session:
        latest_run = session.query(DagRun).filter(
            DagRun.dag_id == "producer_dagRun_sync",
            DagRun.state == "success",
            # 可选：限定时间范围
            DagRun.execution_date >= now_shanghai - datetime.timedelta(hours=1)
        ).order_by(DagRun.execution_date.desc()).first()

    if latest_run:
        # 提取 run_id 中的时间戳并转换为上海时间
        timestamp_str = latest_run.run_id.split("__")[1]
        utc_time = datetime.datetime.strptime(timestamp_str.replace("Z", "+00:00"), "%Y-%m-%dT%H:%M:%S.%f%z")
        shanghai_time = utc_time.astimezone(shanghai_tz)

        # 读取生产者运行元数据
        producer_info = {
            "run_id": latest_run.run_id,
            "execution_date": latest_run.execution_date.astimezone(shanghai_tz),  # 转换为上海时间
            "start_date": latest_run.start_date.astimezone(shanghai_tz),  # 转换为上海时间
            "end_date": latest_run.end_date.astimezone(shanghai_tz)  # 转换为上海时间
        }
        print(f"消费者：生产者运行元数据: {producer_info}")
        # 结合业务逻辑：用run_id查询外部数据库的对应数据
        return producer_info
    else:
        print("消费者：未找到生产者最新成功运行记录")
        return None
    
with DAG(
    dag_id="consumer_dagRun",  # 消费者DAG名称
    start_date=datetime(2026, 2, 13),
    # 关键：调度规则改为监听数据集，而非时间
    schedule=[dateset_dagRun],
    catchup=False,
    tags=["消费者", "dagRun"]
) as consumer_dag:
    clean_task = PythonOperator(
        task_id="consumer_dagRun_read_data",
        python_callable=consumer_dagRun_read_data,
        # 可选：标记该DAG依赖的数据集（仅用于UI展示）
        inlets=[dateset_dagRun],
    )