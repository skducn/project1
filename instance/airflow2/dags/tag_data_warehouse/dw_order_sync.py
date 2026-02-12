from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from datetime import datetime
import subprocess

# 每个 DAG 文件中，通过 tags 参数明确指定标签（可指定多个 tag），确保标签与目录名对应，示例如下：
# tags=["data_warehouse", "order", "sync"]  对应目录
# dag_id="dw_order_sync" 对应文件

# 2. 执行自动化测试脚本（调用pytest）
def run_automation_test(**kwargs):

    # 执行自动化测试并生成报告
    # capture_output=True：
    # 捕获命令的标准输出（stdout）和标准错误（stderr），避免直接打印到终端。
    # text=True：
    # 将输出以文本形式返回，而不是字节形式
    result = subprocess.run(
        ["python", "/Users/linghuchong/Downloads/51/Python/project/instance/zyjk/CDRD/web/main.py"],
        capture_output=True,
        text=True
    )
    print("子进程输出内容:")
    print(result.stdout)
    # 如果有错误信息也打印出来
    if result.stderr:
        print("子进程错误信息:")
        print(result.stderr)

    # 返回测试结果，供后续步骤使用
    return result.returncode  # 0=成功，非0=失败

def run_automation_test2(**kwargs):

    # 执行自动化测试并生成报告
    # capture_output=True：
    # 捕获命令的标准输出（stdout）和标准错误（stderr），避免直接打印到终端。
    # text=True：
    # 将输出以文本形式返回，而不是字节形式
    result = subprocess.run(
        ["python", "/Users/linghuchong/Downloads/51/Python/project/instance/zyjk/CDRD/web/main2.py"],
        capture_output=True,
        text=True
    )
    print("子进程输出内容:")
    print(result.stdout)
    # 如果有错误信息也打印出来
    if result.stderr:
        print("子进程错误信息:")
        print(result.stderr)

    # 返回测试结果，供后续步骤使用
    return result.returncode  # 0=成功，非0=失败

# ====================== 第三步：定义DAG ======================
# 核心：tags 参数指定标签（与目录标签一致，可加额外标签）
# schedule 内置的一些常用调度间隔
# @once: 只执行一次。
# @hourly: 每小时执行一次（等价于 0 * * * *）。
# @daily: 每天执行一次（等价于 0 0 * * *）。
# @weekly: 每周执行一次（等价于 0 0 * * 0）。
# @monthly: 每月执行一次（等价于 0 0 1 * *）。
# @yearly 或 @annually: 每年执行一次（等价于 0 0 1 1 *）
# Cron 表达式
# * * * * *
# │ │ │ │ │
# │ │ │ │ └── 星期几 (0 - 7) (0 和 7 都表示星期日)
# │ │ │ └──── 月份 (1 - 12)
# │ │ └────── 日期 (1 - 31)
# │ └──────── 小时 (0 - 23)
# └────────── 分钟 (0 - 59)
# 例如：
# "0 9 * * 1": 每周一上午 9 点执行。
# "30 14 * * *": 每天下午 2:30 执行。
# "0 0 1 */3 *": 每季度第一天午夜执行。
# 使用 DAG 类创建一个新的工作流对象，并通过上下文管理器（with 语句）将其作用域限定在当前块内
with DAG(
    dag_id="dw_order_sync",  # 唯一 DAG ID，用于区分不同的工作流
    start_date=datetime(2026, 2, 11),
    schedule="@daily",
    catchup=False,  # 控制是否对过去未运行的调度周期进行“补跑”。设置为 False 表示不补跑历史任务；若为 True，则会在 DAG 启用后立即运行所有错过的调度周期。
    tags=["data_warehouse", "订单", "sync"]  # 主标签+子标签
) as dag:
    sync_order = BashOperator(
        task_id="sync_order_data",
        bash_command='echo "同步订单数据到数据仓库"',
        # 重定向所有输出到 Airflow 日志（关键）
        do_xcom_push=False,
        execution_timeout=timedelta(minutes=5)
    )
    # Task1：执行自动化测试
    run_test = PythonOperator(
        task_id='run_automation_test',
        python_callable=run_automation_test,
    )

    # Task1：执行自动化测试
    run_test2 = PythonOperator(
        task_id='run_automation_test2',
        python_callable=run_automation_test2,
    )

    sync_order >> run_test >> run_test2




from airflow.models import DagModel
from airflow.utils.session import create_session

# 自动启用 DAG
with create_session() as session:
    dag_model = session.query(DagModel).filter(DagModel.dag_id == "dw_order_sync").first()
    if dag_model:
        dag_model.is_paused = False  # 设置为启用状态
        session.commit()
