from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="mk_campaign",
    start_date=datetime(2026, 2, 11),
    schedule="@weekly",
    catchup=False,
    tags=["marketing", "campaign", "analysis"]  # 主标签+子标签
) as dag:
    run_campaign = BashOperator(
        task_id="run_campaign_analysis",
        bash_command='echo "分析营销活动效果"'
    )