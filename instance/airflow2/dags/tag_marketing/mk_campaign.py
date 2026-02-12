from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.operators.python import PythonOperator
import subprocess
from airflow.models import Variable  # 导入 Variable 模块


# 2. 执行自动化测试脚本（调用pytest）
def run_automation_test(**kwargs):

    # 执行自动化测试并生成报告
    # capture_output=True：
    # 捕获命令的标准输出（stdout）和标准错误（stderr），避免直接打印到终端。
    # text=True：
    # 将输出以文本形式返回，而不是字节形式
    result = subprocess.run(
        ["python", "/Users/linghuchong/Downloads/51/Python/project/instance/zyjk/CDRD/web/main3.py"],
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


with DAG(
    dag_id="mk_campaign",
    start_date=datetime(2026, 2, 11),
    schedule="@weekly",
    catchup=False,
    tags=["marketing", "campaign", "analysis"]  # 主标签+子标签
) as dag:
    run_campaign = BashOperator(
        task_id="run_campaign_analysis",
        # bash_command='echo "分析营销活动效果"'
        bash_command='echo ' + Variable.get("my_conn", default_var="/data/default")
        # Variable.get("etl_file_path", default_var="/data/default", cache_timeout=3600)  # 缓存 1 小时

    )

    # 方式 3：Jinja2 模板引用 Variable（格式：{{ var.value.变量名 }}）
    task3 = BashOperator(
        task_id="bash_use_variable",
        # 引用 etl_file_path 变量，拼接成脚本执行命令
        bash_command="""
               echo "ETL 文件路径：{{ var.value.etl_file_path }}"
               # 实际场景：执行脚本并传入变量
               # python /scripts/order_sync.py --path {{ var.value.etl_file_path }} --retry {{ var.value.max_retry_times }}
           """
    )

    # # Task1：执行自动化测试
    # run_test = PythonOperator(
    #     task_id='run_automation_test',
    #     python_callable=run_automation_test,
    # )

    run_campaign >> task3
    # run_campaign >> run_test