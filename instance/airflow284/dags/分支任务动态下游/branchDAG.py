# 分支任务（BranchPythonOperator）+ 动态下游
# 业务痛点
# 根据任务执行结果（如数据是否达标），动态选择后续执行的任务分支。
# 核心亮点
# BranchPythonOperator返回的任务 ID 决定执行哪个分支；
# trigger_rule='one_success'：解决多分支汇聚的触发规则问题（默认是all_success，会导致未执行的分支阻塞）；
# 通过 XCom 传递分支判断的结果，供下游任务使用。

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
# from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta


def check_data_quality(**kwargs):
    """分支判断逻辑：检查数据质量是否达标"""
    # 模拟数据质量校验结果（实际从数据库/文件读取）
    data_quality_score = 95  # 满分100
    kwargs['ti'].xcom_push(key='quality_score', value=data_quality_score)

    # 根据分数选择分支
    if data_quality_score >= 90:
        return "task_process_normal"  # 正常处理分支
    elif 80 <= data_quality_score < 90:
        return "task_process_warning"  # 警告处理分支
    else:
        return "task_process_error"  # 错误处理分支


def process_normal(**kwargs):
    score = kwargs['ti'].xcom_pull(key='quality_score')
    print(f"数据质量优秀（{score}分），执行正常处理流程...")


def process_warning(**kwargs):
    score = kwargs['ti'].xcom_pull(key='quality_score')
    print(f"数据质量警告（{score}分），执行降级处理流程...")


def process_error(**kwargs):
    score = kwargs['ti'].xcom_pull(key='quality_score')
    print(f"数据质量不达标（{score}分），执行告警+终止流程...")


default_args = {
    'owner': 'data_team',
    'start_date': datetime(2026, 2, 14),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
        dag_id='branch_task_data_quality',
        default_args=default_args,
        # schedule_interval='@hourly',
        schedule_interval='@weekly',
        catchup=False,
        tags=['分支任务', '数据质量']
) as dag:
    # 1. 开始节点
    start = DummyOperator(task_id='start')

    # 2. 分支判断任务
    branch_task = BranchPythonOperator(
        task_id='branch_check_quality',
        python_callable=check_data_quality,
        provide_context=True
    )

    # 3. 各分支任务
    task_normal = PythonOperator(
        task_id='task_process_normal',
        python_callable=process_normal,
        provide_context=True
    )
    task_warning = PythonOperator(
        task_id='task_process_warning',
        python_callable=process_warning,
        provide_context=True
    )
    task_error = PythonOperator(
        task_id='task_process_error',
        python_callable=process_error,
        provide_context=True
    )

    # 4. 结束节点（所有分支最终汇聚）
    end = DummyOperator(
        task_id='end',
        trigger_rule='one_success'  # 只要有一个分支成功就执行
    )

    # 5. 任务依赖
    start >> branch_task
    branch_task >> task_normal >> end
    branch_task >> task_warning >> end
    branch_task >> task_error >> end