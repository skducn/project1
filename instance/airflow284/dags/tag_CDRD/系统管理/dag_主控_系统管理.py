# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2026-2-27
# Description: 主控DAG - 集成子DAG日志到Allure报告
# airflow UI：cdrd_主控测试流程
# *****************************************************************

from datetime import datetime as dt, timedelta
import os
import json
import uuid
import time
import requests
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.configuration import conf


def get_airflow_api_config():
    """获取Airflow API配置信息"""
    try:
        # 从Airflow配置中获取API信息
        airflow_home = conf.get('core', 'airflow_home')
        web_server_port = conf.get('webserver', 'web_server_port', fallback='8080')
        web_server_host = conf.get('webserver', 'web_server_host', fallback='localhost')

        return {
            'base_url': f"http://{web_server_host}:{web_server_port}",
            'airflow_home': airflow_home
        }
    except Exception as e:
        print(f"⚠️ 获取Airflow配置失败: {str(e)}")
        # 使用默认配置
        return {
            'base_url': "http://localhost:8080",
            'airflow_home': "/Users/linghuchong/Downloads/51/Python/project/instance/airflow284"
        }


def generate_allure_test_result_with_logs(test_name, execution_result, start_time, stop_time):
    """生成包含日志的Allure测试结果"""
    test_uuid = str(uuid.uuid4())

    # 构建测试描述和日志附件
    description = f"测试DAG: {execution_result['dag_id']}\n"
    description += f"运行ID: {execution_result['dag_run_id']}\n"
    description += f"执行状态: {execution_result['status']}\n"
    description += f"执行时间: {execution_result['execution_time']:.2f}秒\n"

    if 'error' in execution_result:
        description += f"错误信息: {execution_result['error']}\n"

    # 创建日志附件
    attachments = []
    for i, task_log in enumerate(execution_result['task_logs']):
        if task_log['log']:
            attachment_name = f"{task_log['task_id']}_log.txt"
            attachments.append({
                "name": attachment_name,
                "source": f"logs/{attachment_name}",
                "type": "text/plain"
            })

    result = {
        "uuid": test_uuid,
        "name": test_name,
        "fullName": f"系统管理.{test_name}",
        "historyId": test_uuid,
        "status": "passed" if execution_result['status'] == 'success' else "failed",
        "stage": "finished",
        "description": description,
        "start": int(start_time * 1000),
        "stop": int(stop_time * 1000),
        "labels": [
            {"name": "suite", "value": "系统管理测试套件"},
            {"name": "subSuite", "value": "主控测试"},
            {"name": "host", "value": "localhost"},
            {"name": "thread", "value": "main"},
            {"name": "framework", "value": "Airflow"},
            {"name": "language", "value": "python"},
            {"name": "tag", "value": execution_result['status']}
        ],
        "links": [],
        "parameters": [
            {"name": "dag_id", "value": execution_result['dag_id']},
            {"name": "dag_run_id", "value": execution_result['dag_run_id']}
        ]
    }

    # 添加附件信息
    if attachments:
        result["attachments"] = attachments

    return result, attachments


def save_task_logs_to_files(allure_results_dir, execution_result):
    """将任务日志保存到文件"""
    logs_dir = os.path.join(allure_results_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    saved_attachments = []

    for task_log in execution_result['task_logs']:
        if task_log['log']:
            log_filename = f"{task_log['task_id']}_log.txt"
            log_filepath = os.path.join(logs_dir, log_filename)

            try:
                with open(log_filepath, 'w', encoding='utf-8') as f:
                    f.write(f"Task ID: {task_log['task_id']}\n")
                    f.write(f"State: {task_log['state']}\n")
                    f.write(f"Start Time: {task_log.get('start_date', 'N/A')}\n")
                    f.write(f"End Time: {task_log.get('end_date', 'N/A')}\n")
                    f.write("=" * 50 + "\n")
                    f.write(task_log['log'])

                saved_attachments.append({
                    "name": log_filename,
                    "path": log_filepath
                })
                print(f"💾 已保存日志文件: {log_filename}")

            except Exception as e:
                print(f"❌ 保存日志文件失败 {log_filename}: {str(e)}")

    return saved_attachments


def generate_allure_report(**context):
    """生成包含子DAG日志的Allure测试报告"""
    try:
        print("=" * 60)
        print("📊 开始生成包含子DAG日志的Allure测试报告...")
        print("=" * 60)

        # 获取执行结果（从XCom）
        user_result = context['task_instance'].xcom_pull(task_ids='execute_user_management_test')
        role_result = context['task_instance'].xcom_pull(task_ids='execute_role_management_test')

        if not user_result or not role_result:
            print("⚠️ 未找到子DAG执行结果")
            return False

        # Allure报告相关路径配置
        project_root = "/Users/linghuchong/Downloads/51/Python/project"
        allure_results_dir = f"{project_root}/instance/airflow284/allure-results"
        allure_report_dir = f"{project_root}/instance/airflow284/allure-report"

        # 创建必要的目录
        os.makedirs(allure_results_dir, exist_ok=True)
        os.makedirs(allure_report_dir, exist_ok=True)

        # 生成Allure测试结果数据
        current_timestamp = time.time()
        base_time = current_timestamp - 120  # 2分钟前作为基准时间

        # 处理用户管理测试结果
        user_test_result, user_attachments = generate_allure_test_result_with_logs(
            "用户管理测试",
            user_result,
            base_time,
            base_time + user_result['execution_time']
        )

        # 保存用户管理日志文件
        user_log_attachments = save_task_logs_to_files(allure_results_dir, user_result)

        # 处理角色管理测试结果
        role_test_result, role_attachments = generate_allure_test_result_with_logs(
            "角色管理测试",
            role_result,
            base_time + 30,
            base_time + 30 + role_result['execution_time']
        )

        # 保存角色管理日志文件
        role_log_attachments = save_task_logs_to_files(allure_results_dir, role_result)

        # 生成测试结果文件
        test_results = [user_test_result, role_test_result]
        for i, test_result in enumerate(test_results):
            result_file = f"{allure_results_dir}/{test_result['uuid']}-result.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(test_result, f, ensure_ascii=False, indent=2)

        # 生成容器文件
        container_uuid = str(uuid.uuid4())
        container_data = {
            "uuid": container_uuid,
            "name": "系统管理测试套件",
            "children": [test['uuid'] for test in test_results],
            "befores": [],
            "afters": [],
            "start": int(base_time * 1000),
            "stop": int((base_time + max(user_result['execution_time'], role_result['execution_time']) + 60) * 1000)
        }

        container_file = f"{allure_results_dir}/{container_uuid}-container.json"
        with open(container_file, 'w', encoding='utf-8') as f:
            json.dump(container_data, f, ensure_ascii=False, indent=2)

        # 生成环境信息
        environment_info = {
            "Environment": "测试环境",
            "Operating System": "macOS",
            "Python Version": "3.x",
            "Airflow Version": "2.8.4",
            "Test Execution Time": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Project Path": project_root,
            "Main DAG": "master_system_management_with_logs",
            "Sub DAGs": f"{user_result['dag_id']}, {role_result['dag_id']}"
        }

        env_file = f"{allure_results_dir}/environment.properties"
        with open(env_file, 'w', encoding='utf-8') as f:
            for key, value in environment_info.items():
                safe_value = str(value).replace('\n', '\\n').replace('\r', '\\r')
                f.write(f"{key}={safe_value}\n")

        # 生成Categories文件
        categories = [
            {
                "name": "Successful Tests",
                "matchedStatuses": ["passed"]
            },
            {
                "name": "Failed Tests",
                "matchedStatuses": ["failed", "broken"]
            },
            {
                "name": "Skipped Tests",
                "matchedStatuses": ["skipped"]
            }
        ]

        categories_file = f"{allure_results_dir}/categories.json"
        with open(categories_file, 'w', encoding='utf-8') as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)

        # 生成执行器信息
        executor_info = {
            "name": "Airflow Master Executor with Logs",
            "type": "custom",
            "url": get_airflow_api_config()['base_url'],
            "buildOrder": 1,
            "buildName": "System Management Test with Sub-DAG Logs",
            "buildUrl": get_airflow_api_config()['base_url'],
            "reportUrl": f"file://{allure_report_dir}/index.html",
            "version": "2.0.0"
        }

        executor_file = f"{allure_results_dir}/executor.json"
        with open(executor_file, 'w', encoding='utf-8') as f:
            json.dump(executor_info, f, ensure_ascii=False, indent=2)

        print(f"✅ Allure结果数据已生成到: {allure_results_dir}")
        print(f"📊 生成了 {len(test_results)} 个测试结果文件")
        print(f"📝 保存了 {len(user_log_attachments) + len(role_log_attachments)} 个日志文件")

        # 验证生成的文件
        print("\n🔍 验证生成的文件:")
        for filename in os.listdir(allure_results_dir):
            if filename.endswith('-result.json') or filename.endswith('-container.json'):
                print(f"   ✓ {filename}")

        if os.path.exists(f"{allure_results_dir}/logs"):
            log_files = os.listdir(f"{allure_results_dir}/logs")
            print(f"   ✓ 日志文件 ({len(log_files)} 个): {log_files}")

        # 生成HTML报告
        try:
            generate_cmd = f"""
                cd {project_root}
                if command -v allure &> /dev/null; then
                    echo "🚀 生成Allure HTML报告..."
                    allure generate "{allure_results_dir}" -o "{allure_report_dir}" --clean
                    if [ -f "{allure_report_dir}/index.html" ]; then
                        echo "✅ Allure报告生成成功: {allure_report_dir}/index.html"
                    else
                        echo "⚠️ Allure报告文件未找到"
                    fi
                else
                    echo "⚠️ 未找到allure命令，请安装allure-commandline"
                    echo "💡 安装方法: brew install allure"
                    echo "💡 手动执行: allure generate \"{allure_results_dir}\" -o \"{allure_report_dir}\" --clean"
                fi
            """

            import subprocess
            result = subprocess.run(generate_cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
            print(result.stdout)
            if result.stderr:
                print(f"stderr: {result.stderr}")

        except Exception as e:
            print(f"⚠️ 生成Allure报告时出现警告: {str(e)}")
            print("💡 你可以手动执行以下命令生成报告:")
            print(f"   allure generate \"{allure_results_dir}\" -o \"{allure_report_dir}\" --clean")

        print("=" * 60)
        print("🎉 包含子DAG日志的Allure测试报告生成完成!")
        print("=" * 60)
        print(f"📁 结果目录: {allure_results_dir}")
        print(f"🌐 报告目录: {allure_report_dir}")
        print(f"⏰ 生成时间: {dt.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"❌ 生成Allure报告失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False




def execute_role_management_test(**context):
    """执行角色管理测试并收集日志 - 真实执行版本"""
    print("=" * 50)
    print("📝 开始执行角色管理测试任务...")
    print("=" * 50)

    try:
        # 执行真实的DAG任务
        result = trigger_and_monitor_dag("cdrd_角色管理_并发", "角色管理测试")
        print("✅ 角色管理测试执行完成")
        return result

    except Exception as e:
        print(f"❌ 角色管理测试执行出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'dag_id': 'cdrd_角色管理_并发',
            'task_name': '角色管理测试',
            'status': 'failed',
            'error': str(e),
            'task_logs': [],
            'execution_time': 0
        }


def execute_user_management_test(**context):
    """执行用户管理测试并收集日志 - 增强调试版本"""
    print("=" * 60)
    print("📝 开始执行用户管理测试任务...")
    print("=" * 60)
    print(f"⏰ 开始时间: {dt.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        print("🔍 正在调用 trigger_and_monitor_dag 函数...")
        # 添加超时控制
        import signal

        def timeout_handler(signum, frame):
            raise TimeoutError("执行超时")

        # 设置5分钟超时
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(300)  # 300秒 = 5分钟

        try:
            print("🚀 开始执行真实DAG任务...")
            result = trigger_and_monitor_dag("cdrd_用户管理_并发", "用户管理测试", timeout=180)
            print("✅ 用户管理测试执行完成")
            signal.alarm(0)  # 取消超时
            return result
        except TimeoutError:
            print("⏰ 执行超时，返回模拟结果以确保流程继续...")
            # 超时情况下返回模拟结果
            return {
                'dag_id': 'cdrd_用户管理_并发',
                'dag_run_id': f"timeout_run_{int(time.time())}",
                'task_name': '用户管理测试',
                'status': 'timeout',
                'execution_time': 300,
                'task_logs': [{
                    'task_id': 'timeout_task',
                    'log': '执行超时，未能获取完整日志',
                    'state': 'failed',
                    'start_date': dt.now().isoformat(),
                    'end_date': dt.now().isoformat()
                }],
                'error': '执行超时'
            }

    except Exception as e:
        print(f"❌ 用户管理测试执行出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'dag_id': 'cdrd_用户管理_并发',
            'task_name': '用户管理测试',
            'status': 'failed',
            'error': str(e),
            'task_logs': [],
            'execution_time': 0
        }
    finally:
        try:
            signal.alarm(0)  # 确保取消超时
        except:
            pass


def trigger_and_monitor_dag(dag_id, task_name, timeout=180):
    """触发DAG并监控执行，收集日志信息 - 增强调试版本"""
    print(f"🔧 进入 trigger_and_monitor_dag 函数")
    print(f"📋 参数: dag_id={dag_id}, task_name={task_name}, timeout={timeout}")

    try:
        api_config = get_airflow_api_config()
        base_url = api_config['base_url']

        print(f"🌐 API配置获取完成: {base_url}")

        # 1. 验证API连接
        print("🔍 验证API连接...")
        try:
            health_check = requests.get(f"{base_url}/health", timeout=10)
            print(f"✅ API连接正常，状态码: {health_check.status_code}")
        except Exception as e:
            print(f"❌ API连接失败: {str(e)}")
            raise Exception(f"无法连接到Airflow API: {str(e)}")

        # 2. 检查DAG是否存在
        print("🔍 检查目标DAG是否存在...")
        dag_check_url = f"{base_url}/api/v1/dags/{dag_id}"
        try:
            dag_response = requests.get(dag_check_url, timeout=10)
            print(f"📊 DAG检查响应: {dag_response.status_code}")
            if dag_response.status_code == 200:
                dag_info = dag_response.json()
                print(f"✅ DAG存在，是否暂停: {dag_info.get('is_paused', 'unknown')}")
            else:
                print(f"⚠️ DAG可能不存在或不可访问: {dag_response.text}")
                # 继续执行，但记录警告
        except Exception as e:
            print(f"⚠️ DAG检查异常: {str(e)}")

        # 3. 触发DAG
        print("📤 准备触发DAG...")
        trigger_url = f"{base_url}/api/v1/dags/{dag_id}/dagRuns"
        trigger_data = {
            "dag_run_id": f"{dag_id}_run_{int(time.time())}",
            "conf": {}
        }

        print(f"📍 触发URL: {trigger_url}")

        response = requests.post(trigger_url, json=trigger_data, timeout=30)
        print(f"📊 触发响应状态: {response.status_code}")

        if response.status_code != 200:
            print(f"❌ 触发失败: {response.text}")
            raise Exception(f"触发DAG失败: {response.text}")

        dag_run_id = response.json()['dag_run_id']
        print(f"✅ DAG触发成功，运行ID: {dag_run_id}")

        # 4. 监控执行状态
        print("👀 开始监控执行状态...")
        start_time = time.time()
        task_instances_log = []

        poll_count = 0
        max_polls = int(timeout / 10)  # 每10秒检查一次

        while time.time() - start_time < timeout and poll_count < max_polls:
            poll_count += 1
            elapsed_time = time.time() - start_time
            print(f"🔍 第{poll_count}次状态检查 (已用时: {elapsed_time:.1f}秒)")

            # 获取DAG运行状态
            status_url = f"{base_url}/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}"
            try:
                status_response = requests.get(status_url, timeout=10)
                print(f"📊 状态检查响应: {status_response.status_code}")

                if status_response.status_code == 200:
                    dag_status = status_response.json()['state']
                    print(f"📊 当前状态: {dag_status}")

                    if dag_status in ['success', 'failed']:
                        print(f"✅ DAG执行完成，最终状态: {dag_status}")

                        # 获取任务实例信息
                        tasks_url = f"{base_url}/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances"
                        try:
                            tasks_response = requests.get(tasks_url, timeout=30)
                            if tasks_response.status_code == 200:
                                task_instances = tasks_response.json()['task_instances']
                                print(f"📊 找到 {len(task_instances)} 个任务实例")

                                # 收集日志
                                for task_instance in task_instances:
                                    task_id = task_instance['task_id']
                                    print(f"📝 收集任务 '{task_id}' 的日志...")
                                    try:
                                        log_url = f"{base_url}/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/logs/1"
                                        log_response = requests.get(log_url, timeout=30)

                                        if log_response.status_code == 200:
                                            log_content = log_response.json().get('content', '')
                                            task_instances_log.append({
                                                'task_id': task_id,
                                                'log': log_content,
                                                'state': task_instance['state'],
                                                'start_date': task_instance.get('start_date'),
                                                'end_date': task_instance.get('end_date')
                                            })
                                            print(f"✅ 已收集任务 '{task_id}' 的日志")
                                    except Exception as log_error:
                                        print(f"⚠️ 收集日志失败: {str(log_error)}")

                        except Exception as tasks_error:
                            print(f"⚠️ 获取任务实例失败: {str(tasks_error)}")

                        break
                    else:
                        print(f"⏳ DAG仍在执行中...")
                else:
                    print(f"❌ 状态检查失败: {status_response.status_code}")

            except Exception as status_error:
                print(f"⚠️ 状态检查异常: {str(status_error)}")

            # 避免过于频繁的检查
            if time.time() - start_time < timeout:
                print("⏰ 等待10秒后继续检查...")
                time.sleep(10)

        # 5. 返回结果
        final_status = dag_status if 'dag_status' in locals() else 'timeout'
        execution_time = time.time() - start_time

        print(f"✅ {task_name} 执行完成")
        print(f"📊 最终状态: {final_status}")
        print(f"⏱️ 执行时间: {execution_time:.2f}秒")
        print(f"📝 收集到 {len(task_instances_log)} 个任务日志")

        return {
            'dag_id': dag_id,
            'dag_run_id': dag_run_id,
            'task_name': task_name,
            'status': final_status,
            'task_logs': task_instances_log,
            'execution_time': execution_time
        }

    except Exception as e:
        print(f"❌ trigger_and_monitor_dag 执行失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise e


def cleanup_old_reports(**context):
    """清理旧的测试报告"""
    try:
        print("🧹 开始清理旧的测试报告...")

        project_root = "/Users/linghuchong/Downloads/51/Python/project"
        allure_results_dir = f"{project_root}/instance/airflow284/allure-results"

        from datetime import datetime, timedelta
        cutoff_time = datetime.now() - timedelta(days=3)

        cleaned_count = 0
        if os.path.exists(allure_results_dir):
            for filename in os.listdir(allure_results_dir):
                file_path = os.path.join(allure_results_dir, filename)
                if os.path.isfile(file_path):
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_mtime < cutoff_time:
                        try:
                            os.remove(file_path)
                            print(f"🗑️ 已删除旧文件: {filename}")
                            cleaned_count += 1
                        except Exception as e:
                            print(f"⚠️ 删除文件失败 {filename}: {str(e)}")

        print(f"✅ 旧报告清理完成，共清理 {cleaned_count} 个文件")
        return True

    except Exception as e:
        print(f"⚠️ 清理旧报告时出现警告: {str(e)}")
        return True


# 主控DAG定义 - 修复语法错误
dag = DAG(
    dag_id="master_system_management_with_logs",
    start_date=dt(2026, 2, 13),
    schedule_interval=None,
    catchup=False,
    tags=["cdrd", "master", "system_management", "allure", "log_integration"],
    dagrun_timeout=timedelta(minutes=60),
)

# 定义任务
start = DummyOperator(task_id="start", dag=dag)
end = DummyOperator(task_id="end", dag=dag)

# 清理旧报告任务
cleanup_reports = PythonOperator(
    task_id="cleanup_old_reports",
    python_callable=cleanup_old_reports,
    provide_context=True,
    dag=dag
)

# 执行用户管理测试（收集日志）
user_test = PythonOperator(
    task_id="execute_user_management_test",
    python_callable=execute_user_management_test,
    provide_context=True,
    dag=dag
)

# 执行角色管理测试（收集日志）
role_test = PythonOperator(
    task_id="execute_role_management_test",
    python_callable=execute_role_management_test,
    provide_context=True,
    dag=dag
)

# 生成包含日志的Allure报告任务
generate_allure = PythonOperator(
    task_id="generate_allure_report",
    python_callable=generate_allure_report,
    provide_context=True,
    dag=dag
)

# 设置执行流程：清理 -> 并行执行测试 -> 生成报告 -> 结束
start >> cleanup_reports >> [user_test, role_test] >> generate_allure >> end
