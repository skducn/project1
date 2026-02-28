# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2026-2-26
# Description: 并发，可设置最大并发数 MaximumConcurrency ，在config.ini 中设置
# 假设您有5个不同的任务类型：
# 第1批（并发）：任务1 + 任务2
# 第2批（并发）：任务3 + 任务4
# 第3批（单独）：任务5
# *****************************************************************

import os, sys, subprocess
import re
from datetime import datetime as dt, timedelta
import concurrent.futures
import threading

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
import importlib.util

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Current directory: {current_dir}")

# 定位添加PO
project_root = os.path.normpath(os.path.join(current_dir, "../../../../../.."))
print(f"Calculated project root: {project_root}")
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to sys.path")
# 验证PO模块路径
po_path = os.path.join(project_root, 'PO')
print(f"PO module path: {po_path}")
# print(f"PO module exists: {os.path.exists(po_path)}")

from PO.TimePO import *

Time_PO = TimePO()

# 定位项目配置路径
web_project_root = os.path.normpath(os.path.join(current_dir, "../../../../../zyjk/CDRD/web"))
print("项目配置路径", web_project_root)

# 添加web目录到路径以便导入config模块
if web_project_root not in sys.path:
    sys.path.insert(0, web_project_root)
    print(f"Added web project root to sys.path: {web_project_root}")

from PO.OpenpyxlPO import OpenpyxlPO

Openpyxl_PO = OpenpyxlPO(f"{web_project_root}/config/testcase.xlsx")

# 配置文件路径
config_file_path = os.path.join(web_project_root, "config", "config.ini")
print(f"Config file path: {config_file_path}")

from config.ConfigparserPO import ConfigparserPO
Configparser_PO = ConfigparserPO(config_file_path)
print("✓ 成功导入配置解析器")

from PO.SqlserverPO import *


# 注意：这里不再创建全局的Sqlserver_PO实例，改为在线程中动态创建

def get_thread_safe_sqlserver_po():
    """为每个线程创建独立的数据库连接"""
    return SqlserverPO(
        Configparser_PO.DB("host"),
        Configparser_PO.DB("username"),
        Configparser_PO.DB("password"),
        Configparser_PO.DB("database")
    )


def producer_task(**context):
    """生产者任务：读取Excel测试用例"""
    try:
        shape = Openpyxl_PO.getL_shape(Configparser_PO.EXCEL("sheet"))
        l_col_values = []
        for i in range(shape[0]):
            if Openpyxl_PO.getCell(i + 1, 11, Configparser_PO.EXCEL("sheet")) == "并发":
                module = Openpyxl_PO.getCell(i + 1, 2, Configparser_PO.EXCEL("sheet"))
                subModule = Openpyxl_PO.getCell(i + 1, 3, Configparser_PO.EXCEL("sheet"))

        for i in range(shape[0]):
            if Openpyxl_PO.getCell(i + 1, 2, Configparser_PO.EXCEL("sheet")) == module and \
                    Openpyxl_PO.getCell(i + 1, 3, Configparser_PO.EXCEL("sheet")) == subModule and \
                    Openpyxl_PO.getCell(i + 1, 11, Configparser_PO.EXCEL("sheet")) == "是":
                l_col_value = []
                l_col_value.append(i + 1)
                l_col_value.append(Openpyxl_PO.getCell(i + 1, 2, Configparser_PO.EXCEL("sheet")))  # 1 模块
                l_col_value.append(Openpyxl_PO.getCell(i + 1, 3, Configparser_PO.EXCEL("sheet")))  # 2 子模块
                l_col_value.append(Openpyxl_PO.getCell(i + 1, 4, Configparser_PO.EXCEL("sheet")))  # 3 前置条件
                l_col_value.append(Openpyxl_PO.getCell(i + 1, 12, Configparser_PO.EXCEL("sheet")))  # 4 自动化数据库校验
                l_col_value.append(Openpyxl_PO.getCell(i + 1, 13, Configparser_PO.EXCEL("sheet")))  # 5 自动化脚本
                l_col_value.append(Openpyxl_PO.getCell(i + 1, 14, Configparser_PO.EXCEL("sheet")))  # 6 自动化后置
                l_col_values.append(l_col_value)

        print(f"【生产者】共找到 {len(l_col_values)} 条自动化测试用例")

        # 将结果存储到XCom供后续任务使用
        return l_col_values
    except Exception as e:
        print(f"❌ 生产者任务执行失败: {str(e)}")
        raise e


def _execute_playwright_script(file):
    """执行Playwright脚本"""
    try:
        file_path = f"{web_project_root}/{file}"
        # print(f"[线程 {threading.current_thread().name}] 准备执行Playwright脚本: {file_path}")

        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"❌ Playwright脚本文件不存在: {file_path}")
            return None

        spec = importlib.util.spec_from_file_location("playwright_script", file_path)
        module = importlib.util.module_from_spec(spec)
        script_dir = os.path.dirname(file_path)
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)

        spec.loader.exec_module(module)
        if hasattr(module, 'run_playwright'):
            # print(f"[线程 {threading.current_thread().name}] ✅ 找到run_playwright函数，开始执行...")
            result = module.run_playwright()
            # print(f"[线程 {threading.current_thread().name}] ✅ Playwright执行完成，返回: {result}")
            return result
        else:
            print(f"[线程 {threading.current_thread().name}] ❌ 未找到 run_playwright 函数")
            return None
    except Exception as e:
        print(f"[线程 {threading.current_thread().name}] ❌ 执行失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
def _updateStatus(thread_name, status_count, errorLog, replace_variable, l_col_values, local_sqlserver_po):
    """依据状态更新Excel和执行后置操作 - 使用线程安全的数据库连接"""
    try:
        if status_count == 0:
            # 通过，更新状态、处理后置
            Openpyxl_PO.setCell(l_col_values[0], 10, "通过", Configparser_PO.EXCEL("sheet"))  # 状态
            print(f"[{thread_name}] ✅ 测试用例执行通过")

            # 判断处理后置是否存在
            if len(l_col_values) > 6 and l_col_values[6] is not None:
                try:
                    # 正则 - 处理后置
                    s_postposition_re = re.sub(r"\{result\['([^']+)'\]\}", replace_variable, l_col_values[6])
                    l_postposition = eval(s_postposition_re)
                    print(f"[{thread_name}] 解析后置数据: {l_postposition}")

                    if len(l_postposition) == 1:
                        # 后置处理1
                        try:
                            local_sqlserver_po.execute(l_postposition[0][0])
                            print(f"[{thread_name}] ✅ 后置操作完成: {l_postposition[0][0]}")
                        except Exception as e:
                            print(f"[{thread_name}] ❌ 后置操作出错: {e}")
                    elif len(l_postposition) > 1:
                        # 后置处理N
                        try:
                            for j in range(len(l_postposition)):
                                local_sqlserver_po.execute(l_postposition[j][0])
                                print(f"[{thread_name}] ✅ 后置操作{j + 1}完成: {l_postposition[j][0]}")
                        except Exception as e:
                            print(f"[{thread_name}] ❌ 后置操作N出错: {e}")
                except Exception as e:
                    print(f"[{thread_name}] ❌ 后置数据解析错误: {e}")
        else:
            # 失败，更新状态、web实测结果
            Openpyxl_PO.setCell(l_col_values[0], 10, "失败", Configparser_PO.EXCEL("sheet"))  # 状态
            Openpyxl_PO.setCell(l_col_values[0], 9, errorLog, Configparser_PO.EXCEL("sheet"))  # web实测结果
            print(f"[{thread_name}] ❌ 测试用例执行失败: {errorLog}")

        # 更新时间
        Openpyxl_PO.setCell(l_col_values[0], 15, Time_PO.getDateTimeByMinus(), Configparser_PO.EXCEL("sheet"))  # 完成时间

    except Exception as e:
        print(f"[{thread_name}] ❌ 状态更新出错: {e}")
def _test_execution(l_col_values):
    """执行单个测试用例并进行验证 - 完全线程安全版本"""
    thread_name = threading.current_thread().name

    # 为当前线程创建独立的数据库连接
    local_sqlserver_po = get_thread_safe_sqlserver_po()

    try:
        # 执行自动化脚本
        pathFile = os.path.join(l_col_values[1], l_col_values[2], l_col_values[5] + ".py")
        print(f"[{thread_name}] 开始执行测试用例: {pathFile}")

        result = _execute_playwright_script(pathFile)
        print(f"[{thread_name}] Playwright执行结果: {result}")

        # 如果Playwright执行失败，直接返回False
        if result is None:
            print(f"[{thread_name}] ❌ Playwright执行失败，测试用例失败")
            return False

        # 正则匹配变量
        def replace_variable(match):
            var_name = match.group(1)
            if isinstance(result, dict) and var_name in result:
                return str(result[var_name])
            else:
                return match.group(0)

        try:
            # 正则 - 自动化校验
            s_validation = re.sub(r"\{result\['([^']+)'\]\}", replace_variable, l_col_values[4])
            # print(f"[{thread_name}] 正则替换结果: {s_validation}")

            d_validation = eval(s_validation)
            print(f"[{thread_name}] 解析后的验证数据: {d_validation}")

            if len(d_validation) == 1:
                # 1条校验
                errorLog = ""
                status_count = 0

                # 使用线程本地的数据库连接
                try:
                    l_d_ = local_sqlserver_po.select(d_validation[0]['k'])
                    print(f"[{thread_name}] 数据库查询结果: {l_d_}")

                    # 检查查询结果是否有效
                    if l_d_ is not None and len(l_d_) > 0 and l_d_[0] is not None:
                        if 'qty' in l_d_[0] and l_d_[0]['qty'] == int(d_validation[0]['v']):
                            print(f"[{thread_name}] ✅ 通过校验", d_validation[0])
                            status_count = 0
                        else:
                            print(f"[{thread_name}] ❌ 失败校验", d_validation[0])
                            status_count = 1
                            errorLog = "v=" + str(l_d_[0].get('qty', 'NULL'))
                    else:
                        print(f"[{thread_name}] ❌ 数据库查询返回空结果")
                        status_count = 1
                        errorLog = "数据库查询无结果"

                except Exception as db_error:
                    print(f"[{thread_name}] ❌ 数据库查询异常: {db_error}")
                    status_count = 1
                    errorLog = f"数据库错误: {str(db_error)}"

                # 依据状态更新
                _updateStatus(thread_name, status_count, errorLog, replace_variable, l_col_values, local_sqlserver_po)
                return status_count == 0

            elif len(d_validation) > 1:
                # 多条校验
                errorLog = ""
                status_count = 0

                for j in range(len(d_validation)):
                    try:
                        l_d_ = local_sqlserver_po.select(d_validation[j]['k'])
                        print(f"[{thread_name}] 数据库查询结果[{j + 1}]: {l_d_}")

                        # 检查查询结果是否有效
                        if l_d_ is not None and len(l_d_) > 0 and l_d_[0] is not None:
                            if 'qty' in l_d_[0] and l_d_[0]['qty'] == int(d_validation[j]['v']):
                                print(f"[{thread_name}] ✅ 通过校验" + str(j + 1), d_validation[j])
                                status_count += 0
                            else:
                                print(f"[{thread_name}] ❌ 失败校验" + str(j + 1), d_validation[j])
                                status_count += 1
                                errorLog = str(d_validation[j]) + errorLog
                        else:
                            print(f"[{thread_name}] ❌ 数据库查询返回空结果[{j + 1}]")
                            status_count += 1
                            errorLog = f"查询{j + 1}无结果;" + errorLog

                    except Exception as db_error:
                        print(f"[{thread_name}] ❌ 数据库查询异常[{j + 1}]: {db_error}")
                        status_count += 1
                        errorLog = f"查询{j + 1}错误:{str(db_error)};" + errorLog

                # 依据状态更新
                _updateStatus(thread_name, status_count, errorLog, replace_variable, l_col_values, local_sqlserver_po)
                return status_count == 0

            else:
                print(f"[{thread_name}] error, 自动化校验不能为空！")
                return False

        except Exception as e:
            print(f"[{thread_name}] 验证过程出错: {e}")
            import traceback
            traceback.print_exc()
            return False

    finally:
        # 确保关闭数据库连接
        try:
            local_sqlserver_po.close()
            print(f"[{thread_name}] ✅ 数据库连接已关闭")
        except Exception as e:
            print(f"[{thread_name}] ❌ 关闭数据库连接时出错: {e}")
def _consumer_task_wrapper(test_type, l_col_values):
    """消费者任务包装器 - 支持动态test_type参数"""
    print(f"={'=' * 20} {test_type} 消费者开始执行 {'=' * 20}")

    success_count = 0
    fail_count = 0

    if l_col_values:
        for i in range(len(l_col_values)):
            # 动态匹配测试类型 - 支持任意test_type
            if len(l_col_values[i]) >= 6 and l_col_values[i][5]:
                current_test_name = str(l_col_values[i][5]).strip()

                # 精确匹配或模糊匹配（根据需求选择）
                if test_type == current_test_name or test_type in current_test_name:
                    # print(f"[{test_type}] 找到匹配的测试用例: {current_test_name}")

                    # 执行测试并统计结果
                    try:
                        test_result = _test_execution(l_col_values[i])
                        if test_result:
                            success_count += 1
                            print(f"[{test_type}] ✅ 测试执行成功")
                        else:
                            fail_count += 1
                            print(f"[{test_type}] ❌ 测试执行失败")
                    except Exception as e:
                        fail_count += 1
                        print(f"[{test_type}] ❌ 测试执行异常: {str(e)}")
                else:
                    print(f"[{test_type}] 跳过不匹配的测试用例: {current_test_name}")
            else:
                print(f"[{test_type}] 跳过无效的测试用例数据: {l_col_values[i]}")

    print(f"={'=' * 20} {test_type} 消费者执行完成 {'=' * 20}")
    # print(f"[{test_type}] 成功: {success_count}, 失败: {fail_count}")

    # 返回执行统计结果
    return {
        "module": f"系统管理-角色管理-{test_type}",
        "success_count": success_count,
        "fail_count": fail_count,
        "total_count": success_count + fail_count
    }


def parallel_consumers_task(**context):
    """并行执行多个消费者任务（支持动态任务数量和test_type，限制最大并发数）"""
    print("=" * 50)
    print("【并行消费者】开始执行测试任务...")
    print("=" * 50)

    try:
        # 从XCom获取生产者的数据
        l_col_values = context['task_instance'].xcom_pull(task_ids='读取测试用例')
        print(f"从XCom获取到的测试用例数据: {len(l_col_values) if l_col_values else 0} 条")

        if not l_col_values:
            print("⚠️ 没有找到测试用例数据")
            return {}

        # 动态提取所有唯一的任务类型
        unique_tasks = list()
        task_set = set()
        for item in l_col_values:
            if len(item) >= 6 and item[5]:  # 确保有足够的列且第6列不为空
                task_name = str(item[5]).strip()
                if task_name and task_name not in task_set:
                    task_set.add(task_name)
                    unique_tasks.append(task_name)

        print(f"发现 {len(unique_tasks)} 种不同的任务类型: {unique_tasks}")

        # 设置最大并发数（可根据需要调整）
        MAX_CONCURRENT_WORKERS = Configparser_PO.EXCEL("MaximumConcurrency")  # 限制最大并发数为2


        # 存储所有批次的结果
        all_results = {}

        # 将任务分批执行
        batch_size = MAX_CONCURRENT_WORKERS
        total_batches = (len(unique_tasks) + batch_size - 1) // batch_size  # 向上取整计算批次数

        print(f"任务将分为 {total_batches} 批执行，每批最多 {batch_size} 个任务并发")

        for batch_index in range(total_batches):
            start_index = batch_index * batch_size
            end_index = min((batch_index + 1) * batch_size, len(unique_tasks))
            current_batch = unique_tasks[start_index:end_index]

            print(f"\n开始执行第 {batch_index + 1}/{total_batches} 批任务: {current_batch}")

            # 存储当前批次的Future对象和结果
            futures_dict = {}
            results_dict = {}

            # 使用线程池执行当前批次的任务
            with concurrent.futures.ThreadPoolExecutor(
                    max_workers=len(current_batch),  # 当前批次的任务数
                    thread_name_prefix=f"Consumer_Batch{batch_index + 1}"
            ) as executor:

                # 提交当前批次的所有任务到线程池
                for task_name in current_batch:
                    print(f"提交任务: {task_name}")
                    future = executor.submit(_consumer_task_wrapper, task_name, l_col_values)
                    futures_dict[task_name] = future

                # 等待当前批次所有任务完成并收集结果
                print(f"开始等待第 {batch_index + 1} 批 {len(futures_dict)} 个任务完成...")

                for task_name, future in futures_dict.items():
                    try:
                        result = future.result(timeout=300)  # 5分钟超时
                        results_dict[task_name] = result
                        print(f"✅ {task_name} 执行完成 - 成功:{result['success_count']}, 失败:{result['fail_count']}")
                    except concurrent.futures.TimeoutError:
                        print(f"❌ {task_name} 执行超时")
                        results_dict[task_name] = {
                            "module": f"系统管理-角色管理-{task_name}",
                            "success_count": 0,
                            "fail_count": 0,
                            "total_count": 0,
                            "error": "执行超时"
                        }
                    except Exception as e:
                        print(f"❌ {task_name} 执行失败: {str(e)}")
                        results_dict[task_name] = {
                            "module": f"系统管理-角色管理-{task_name}",
                            "success_count": 0,
                            "fail_count": 0,
                            "total_count": 0,
                            "error": str(e)
                        }

            # 将当前批次结果合并到总结果中
            all_results.update(results_dict)

            print(f"第 {batch_index + 1} 批任务执行完成")

            # 如果不是最后一批，可以添加短暂延迟（可选）
            if batch_index < total_batches - 1:
                print("等待2秒后开始下一批任务...")
                import time
                time.sleep(2)

        print("=" * 50)
        print("【并行消费者】所有测试执行完成")
        print("=" * 50)

        # 返回所有任务的执行结果
        return all_results

    except Exception as e:
        print(f"❌ 并行消费者任务执行失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise e


# 单个DAG，真正的并行执行
with DAG(
        dag_id="cdrd_并发",
        start_date=dt(2026, 2, 13),
        schedule_interval=None,  # 手动触发
        catchup=False,
        tags=["cdrd", "1系统管理", "2角色管理"],
        render_template_as_native_obj=True
) as dag:
    start = DummyOperator(task_id="start")
    end = DummyOperator(task_id="end")

    # 生产者任务
    producer = PythonOperator(
        task_id="读取测试用例",
        python_callable=producer_task,
        provide_context=True
    )

    # 真正并行执行的消费者任务
    parallel_consumers = PythonOperator(
        task_id="并行执行消费者",
        python_callable=parallel_consumers_task,
        provide_context=True
    )

    # # 收尾工作
    # final = PythonOperator(
    #     task_id="收尾工作",
    #     python_callable=final_task,
    #     provide_context=True
    # )

    # 设置依赖关系 - 真正的并行执行
    start >> producer >> parallel_consumers >> end
    # start >> producer >> parallel_consumers >> final >> end
