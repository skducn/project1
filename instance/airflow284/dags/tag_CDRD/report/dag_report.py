from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List

# 定义默认参数
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 3, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# 报告保存路径（可根据实际情况修改）
REPORT_OUTPUT_PATH = '/Users/linghuchong/Downloads/51/Python/project/instance/airflow284/dags/tag_CDRD/report'


# 确保报告目录存在
# os.makedirs(REPORT_OUTPUT_PATH, exist_ok=True)


def simulate_business_task(**kwargs):
    """模拟业务任务执行"""
    import time
    time.sleep(2)  # 模拟任务耗时
    ti = kwargs['ti']
    # 模拟生成一些业务数据，用于报告展示
    business_metrics = {
        'processed_records': 15890,
        'valid_records': 15878,
        'invalid_records': 12,
        'error_rate': 0.075
    }
    ti.xcom_push(key='business_metrics', value=business_metrics)
    return "Business task completed successfully"


# ... existing code ...

def generate_test_report(**kwargs):
    """生成专业的DAG执行测试报告"""
    ti = kwargs['ti']
    dag_run = kwargs['dag_run']

    # 1. 收集基础执行信息
    report_data = {
        'report_generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'dag_id': dag_run.dag_id,
        'run_id': dag_run.run_id,
        'execution_date': dag_run.execution_date.strftime('%Y-%m-%d %H:%M:%S'),
        'start_date': dag_run.start_date.strftime('%Y-%m-%d %H:%M:%S') if dag_run.start_date else "N/A",
        'end_date': dag_run.end_date.strftime('%Y-%m-%d %H:%M:%S') if dag_run.end_date else "N/A",
        'state': dag_run.state,
        'duration': (
                dag_run.end_date - dag_run.start_date).total_seconds() if dag_run.end_date and dag_run.start_date else 0
    }

    # 2. 收集所有任务实例信息
    task_instances = []
    for task_instance in dag_run.get_task_instances():
        task_info = {
            'task_id': task_instance.task_id,
            'state': task_instance.state or "unknown",
            'start_date': task_instance.start_date.strftime('%Y-%m-%d %H:%M:%S') if task_instance.start_date else "N/A",
            'end_date': task_instance.end_date.strftime('%Y-%m-%d %H:%M:%S') if task_instance.end_date else "N/A",
            'duration': (
                    task_instance.end_date - task_instance.start_date).total_seconds() if task_instance.end_date and task_instance.start_date else 0,
            'try_number': task_instance.try_number or 0,
            'max_tries': task_instance.max_tries or 0
        }
        task_instances.append(task_info)

    # 3. 获取业务指标
    business_metrics = ti.xcom_pull(key='business_metrics', task_ids='simulate_business_task') or {}

    # 4. 生成Markdown格式的专业测试报告
    report_filename = f"{dag_run.dag_id}_test_report_{dag_run.execution_date.strftime('%Y%m%d_%H%M%S')}.md"
    report_filepath = os.path.join(REPORT_OUTPUT_PATH, report_filename)

    # 构建报告内容
    report_content = f"""# Airflow DAG 执行测试报告

## 执行概要
| 项目 | 数值 |
|------|------|
| DAG ID | {report_data['dag_id']} |
| 运行ID | {report_data['run_id']} |
| 执行时间 | {report_data['execution_date']} |
| 开始时间 | {report_data['start_date']} |
| 结束时间 | {report_data['end_date']} |
| 执行状态 | **{report_data['state']}** |
| 总耗时 | {report_data['duration']:.2f} 秒 |

## 任务执行明细
| 任务ID | 状态 | 开始时间 | 结束时间 | 耗时(秒) | 尝试次数 | 最大重试 |
|--------|------|----------|----------|----------|----------|----------|
"""

    # 添加任务明细行
    for task in task_instances:
        duration = f"{task['duration']:.2f}" if task['duration'] > 0 else "0.00"
        report_content += f"| {task['task_id']} | **{task['state']}** | {task['start_date']} | {task['end_date']} | {duration} | {task['try_number']} | {task['max_tries']} |\n"

    # 添加业务指标部分
    report_content += f"""
## 业务指标
| 指标 | 数值 | 说明 |
|------|------|------|
| 处理记录总数 | {business_metrics.get('processed_records', 0)} | 本次执行处理的总记录数 |
| 有效记录数 | {business_metrics.get('valid_records', 0)} | 通过校验的记录数 |
| 无效记录数 | {business_metrics.get('invalid_records', 0)} | 未通过校验的记录数 |
| 错误率 | {business_metrics.get('error_rate', 0):.4f} | 无效记录占总记录的比例 |

## 执行分析
### 整体状态
- DAG 执行状态：{report_data['state']}
- {'✅ 所有任务执行成功' if report_data['state'] == 'success' else '❌ 存在执行失败的任务'}

### 性能分析
- 总执行耗时：{report_data['duration']:.2f} 秒
- 单任务平均耗时：{sum([t['duration'] for t in task_instances if t['duration'] > 0]) / len([t for t in task_instances if t['duration'] > 0]) if any(t['duration'] > 0 for t in task_instances) else 0:.2f} 秒

### 异常排查
"""

    # 添加异常信息
    failed_tasks = [t for t in task_instances if t['state'] not in ['success', 'skipped']]
    if failed_tasks:
        report_content += "#### 失败任务列表\n"
        for task in failed_tasks:
            report_content += f"- **{task['task_id']}**: 状态={task['state']}, 尝试次数={task['try_number']}/{task['max_tries']}\n"
    else:
        report_content += "#### 无异常任务\n"

    # 报告结尾
    report_content += f"""
## 建议
1. {'检查失败任务的日志和依赖，优化任务逻辑' if failed_tasks else '保持当前执行配置，定期监控执行性能'}
2. 关注错误率指标，{'建议优化数据校验规则' if business_metrics.get('error_rate', 0) > 0.01 else '当前错误率在可接受范围内'}
3. 定期清理历史执行日志，确保Airflow调度性能

---
报告生成时间：{report_data['report_generated_at']}
"""

    # 确保报告目录存在
    os.makedirs(REPORT_OUTPUT_PATH, exist_ok=True)

    # 保存报告文件
    with open(report_filepath, 'w', encoding='utf-8') as f:
        f.write(report_content)

    # 输出报告路径（方便在Airflow日志中查看）
    print(f"✅ 测试报告已生成：{report_filepath}")

    # 将报告路径推送到XCom，方便后续任务使用
    ti.xcom_push(key='test_report_path', value=report_filepath)

    return f"Test report generated successfully: {report_filepath}"


# ... existing code ...


# 定义DAG
with DAG(
        'dag_with_professional_test_report',
        default_args=default_args,
        description='A DAG that generates professional test report after execution',
        schedule_interval=timedelta(days=1),
        catchup=False,
        tags=['cdrd', 'report', 'professional']
) as dag:
    # 模拟业务任务
    task_business = PythonOperator(
        task_id='simulate_business_task',
        python_callable=simulate_business_task,
        provide_context=True,
        do_xcom_push=True
    )

    # 生成测试报告任务
    task_generate_report = PythonOperator(
        task_id='generate_professional_test_report',
        python_callable=generate_test_report,
        provide_context=True,
        do_xcom_push=True
    )

    # 设置任务依赖
    task_business >> task_generate_report