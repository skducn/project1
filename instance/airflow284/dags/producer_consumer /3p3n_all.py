# 3个生产者 → 3 个消费者（多数据源依赖） → 消费者DAG - 等待所有数据源
# 部署方式：
# 将此代码保存为 .py 文件放入 Airflow 的 dags 目录
# 确保 Airflow 配置中启用了 enable_dataset_cross_dag_dependencies = True
# 执行流程：
# 三个生产者DAG按不同频率独立运行
# 消费者DAG会等待所有三个数据集都被标记为更新后才执行
# 消费者从每个生产者获取最新的XCom数据进行综合分析
# 监控要点：
# 可在Airflow UI中查看数据集依赖关系图
# 消费者DAG只有在所有生产者都成功运行后才会触发
# 每个生产者的执行频率可以不同，消费者会等待最新的数据
# 扩展建议：
# 可以根据实际需求调整数据集的数量
# 可以为不同的数据集设置不同的更新条件
# 可以添加错误处理和重试机制

from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.models import TaskInstance, DagRun
from airflow.utils.session import create_session

# ===================== 1. 定义多个数据集 =====================
# 数据集A：用户表数据
dataset_user = Dataset(
    uri="dataset://mysql/users",
    extra={
        "description": "用户信息表，包含用户基本信息",
        "owner": "data_team",
        "version": "1.0"
    }
)

# 数据集B：订单表数据
dataset_order = Dataset(
    uri="dataset://mysql/orders",
    extra={
        "description": "订单信息表，包含订单交易数据",
        "owner": "data_team",
        "version": "1.0"
    }
)

# 数据集C：产品表数据
dataset_product = Dataset(
    uri="dataset://mysql/products",
    extra={
        "description": "产品信息表，包含商品基础信息",
        "owner": "data_team",
        "version": "1.0"
    }
)


# ===================== 2. 生产者DAGs =====================
# 生产者1：用户数据同步
def producer_user_task(**context):
    """同步用户数据到数据仓库"""
    print("开始同步用户数据...")
    # 模拟用户数据处理逻辑
    user_count = 1000
    print(f"用户数据同步完成！共处理 {user_count} 条记录")
    return {"user_count": user_count, "status": "success"}


# 生产者2：订单数据同步
def producer_order_task(**context):
    """同步订单数据到数据仓库"""
    print("开始同步订单数据...")
    # 模拟订单数据处理逻辑
    order_count = 5000
    total_amount = 250000.00
    print(f"订单数据同步完成！共处理 {order_count} 条记录，总金额 {total_amount}")
    return {"order_count": order_count, "total_amount": total_amount, "status": "success"}


# 生产者3：产品数据同步
def producer_product_task(**context):
    """同步产品数据到数据仓库"""
    print("开始同步产品数据...")
    # 模拟产品数据处理逻辑
    product_count = 200
    print(f"产品数据同步完成！共处理 {product_count} 条记录")
    return {"product_count": product_count, "status": "success"}


# ===================== 3. 消费者DAG（等待所有生产者）=====================
def consumer_multi_source_task(**context):
    """消费多个数据源的数据进行综合分析"""
    print("检测到所有数据源已更新，开始综合处理...")

    # 从各个生产者获取数据
    user_data = get_producer_xcom("producer_user_dag", "producer_user_task")
    order_data = get_producer_xcom("producer_order_dag", "producer_order_task")
    product_data = get_producer_xcom("producer_product_dag", "producer_product_task")

    print(f"获取到用户数据: {user_data}")
    print(f"获取到订单数据: {order_data}")
    print(f"获取到产品数据: {product_data}")

    # 综合分析处理
    if user_data and order_data and product_data:
        # 计算平均客单价
        avg_order_value = order_data.get('total_amount', 0) / order_data.get('order_count', 1)
        # 计算人均订单数
        avg_orders_per_user = order_data.get('order_count', 0) / user_data.get('user_count', 1)

        result = {
            "analysis_type": "multi_source_analysis",
            "avg_order_value": round(avg_order_value, 2),
            "avg_orders_per_user": round(avg_orders_per_user, 2),
            "total_users": user_data.get('user_count'),
            "total_orders": order_data.get('order_count'),
            "total_products": product_data.get('product_count'),
            "status": "analysis_completed"
        }

        print(f"综合分析完成: {result}")
        return result
    else:
        print("警告：部分数据源数据获取失败")
        return {"status": "partial_data", "available_sources": [bool(user_data), bool(order_data), bool(product_data)]}


# 通用XCom读取函数
def get_producer_xcom(producer_dag_id, producer_task_id):
    """从指定生产者获取XCom数据"""
    try:
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
                    print(f"✅ 从 {producer_dag_id}.{producer_task_id} 获取数据: {xcom_value}")
                    return xcom_value
            print(f"⚠️ 未找到 {producer_dag_id}.{producer_task_id} 的成功运行记录")
            return None
    except Exception as e:
        print(f"❌ 获取XCom数据失败: {str(e)}")
        return None


# ===================== 4. DAG定义 =====================
# 生产者DAG 1 - 用户数据
with DAG(
        dag_id="producer_user_dag",
        start_date=datetime(2026, 2, 13),
        schedule_interval="@daily",  # 每天执行
        catchup=False,
        tags=["multi_producer", "user_data"]
) as user_dag:
    user_task = PythonOperator(
        task_id="producer_user_task",
        python_callable=producer_user_task,
        outlets=[dataset_user],  # 标记更新用户数据集
        provide_context=True
    )

# 生产者DAG 2 - 订单数据
with DAG(
        dag_id="producer_order_dag",
        start_date=datetime(2026, 2, 13),
        schedule_interval="@hourly",  # 每小时执行
        catchup=False,
        tags=["multi_producer", "order_data"]
) as order_dag:
    order_task = PythonOperator(
        task_id="producer_order_task",
        python_callable=producer_order_task,
        outlets=[dataset_order],  # 标记更新订单数据集
        provide_context=True
    )

# 生产者DAG 3 - 产品数据
with DAG(
        dag_id="producer_product_dag",
        start_date=datetime(2026, 2, 13),
        schedule_interval="@weekly",  # 每周执行
        catchup=False,
        tags=["multi_producer", "product_data"]
) as product_dag:
    product_task = PythonOperator(
        task_id="producer_product_task",
        python_callable=producer_product_task,
        outlets=[dataset_product],  # 标记更新产品数据集
        provide_context=True
    )

# 消费者DAG - 等待所有数据源
with DAG(
        dag_id="consumer_multi_source_analysis",
        start_date=datetime(2026, 2, 13),
        # 关键：同时监听所有数据集，只有当所有数据集都更新时才会触发
        schedule=[dataset_user, dataset_order, dataset_product],
        catchup=False,
        tags=["multi_producer", "consumer", "data_analysis"]
) as consumer_dag:
    analysis_task = PythonOperator(
        task_id="consumer_multi_source_task",
        python_callable=consumer_multi_source_task,
        # 标记依赖的所有数据集（用于UI展示）
        inlets=[dataset_user, dataset_order, dataset_product],
        provide_context=True
    )
