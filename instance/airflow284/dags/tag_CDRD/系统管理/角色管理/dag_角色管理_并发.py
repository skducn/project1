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

from typing import List, Dict, Any


# 注意：这里不再创建全局的Sqlserver_PO实例，改为在线程中动态创建

def get_thread_safe_sqlserver_po():
    """为每个线程创建独立的数据库连接"""
    return SqlserverPO(
        Configparser_PO.DB("host"),
        Configparser_PO.DB("username"),
        Configparser_PO.DB("password"),
        Configparser_PO.DB("database")
    )


# 校验前置条件的MaxConcurrency，并设置默认值
def get_max_concurrency(config):
    # 1. 检查 MaxConcurrency 键是否存在
    if "MaxConcurrency" not in config:
        return 2

    # 2. 获取值并校验类型和合法性（数字类型且非负）
    max_conc = config["MaxConcurrency"]
    # 判断是否为数字类型（int/float）且值 >= 0
    if not isinstance(max_conc, (int, float)) or max_conc < 0:
        return 2

    # 3. 校验通过，返回原值
    return max_conc


def producer_task(**context):
    """生产者任务：读取Excel测试用例"""
    try:
        shape = Openpyxl_PO.getL_shape(Configparser_PO.EXCEL("sheet"))
        l_col_values = []
        for i in range(shape[0]):
            if Openpyxl_PO.getCell(i + 1, 11, Configparser_PO.EXCEL("sheet")) == "并发":
                module = Openpyxl_PO.getCell(i + 1, 2, Configparser_PO.EXCEL("sheet"))
                subModule = Openpyxl_PO.getCell(i + 1, 3, Configparser_PO.EXCEL("sheet"))
                s_precondition = Openpyxl_PO.getCell(i + 1, 4, Configparser_PO.EXCEL("sheet"))
                d_precondition = eval(s_precondition)  # {'MaxConcurrency': 2, 'priorityConcurrency': ['新增用户', '编辑用户']}

        for i in range(shape[0]):
            if Openpyxl_PO.getCell(i + 1, 2, Configparser_PO.EXCEL("sheet")) == module and \
                    Openpyxl_PO.getCell(i + 1, 3, Configparser_PO.EXCEL("sheet")) == subModule and \
                    Openpyxl_PO.getCell(i + 1, 11, Configparser_PO.EXCEL("sheet")) == "是":
                l_col_value = []
                l_col_value.append(i + 1)
                l_col_value.append(Openpyxl_PO.getCell(i + 1, 2, Configparser_PO.EXCEL("sheet")))  # 1 模块
                l_col_value.append(Openpyxl_PO.getCell(i + 1, 3, Configparser_PO.EXCEL("sheet")))  # 2 子模块
                l_col_value.append(Openpyxl_PO.getCell(i + 1, 4, Configparser_PO.EXCEL("sheet")))  # 3 前置条件
                l_col_value.append(Openpyxl_PO.getCell(i + 1, 12, Configparser_PO.EXCEL("sheet")))  # 4 自动化校验
                l_col_value.append(Openpyxl_PO.getCell(i + 1, 13, Configparser_PO.EXCEL("sheet")))  # 5 自动化脚本
                l_col_value.append(Openpyxl_PO.getCell(i + 1, 14, Configparser_PO.EXCEL("sheet")))  # 6 自动化后置
                l_col_values.append(l_col_value)

        print(f"【生产者】共找到 {len(l_col_values)} 条自动化测试用例")

        # 将结果存储到XCom供后续任务使用
        return l_col_values, d_precondition
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
            Openpyxl_PO.setCell(l_col_values[0], 9, "", Configparser_PO.EXCEL("sheet"))  # web实测结果
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


def categorize_tasks(l_col_values: List[List[Any]], priority_tasks: List[str]) -> tuple:
    """
    将任务分类为优先任务和普通任务

    Args:
        l_col_values: 所有测试用例数据
        priority_tasks: 优先执行的任务列表

    Returns:
        tuple: (优先任务列表, 普通任务列表)
    """
    priority_task_items = []
    normal_task_items = []

    # 创建优先任务集合用于快速查找
    priority_set = set(priority_tasks) if priority_tasks else set()

    for item in l_col_values:
        if len(item) >= 6 and item[5]:
            task_name = str(item[5]).strip()
            if priority_tasks and task_name in priority_set:  # 只有当优先任务列表不为空时才进行优先任务筛选
                priority_task_items.append(item)
                print(f"✅ 识别为优先任务: {task_name}")
            else:
                normal_task_items.append(item)
                if priority_tasks:  # 只在有优先任务配置时显示普通任务标识
                    print(f"📝 识别为普通任务: {task_name}")
                else:
                    print(f"📝 任务: {task_name}")

    print(f"📊 任务分类结果 - 优先任务: {len(priority_task_items)}个, 普通任务: {len(normal_task_items)}个")
    return priority_task_items, normal_task_items

def extract_unique_tasks(task_items: List[List[Any]]) -> List[str]:
    """
    从任务项中提取唯一任务名称

    Args:
        task_items: 任务数据列表

    Returns:
        List[str]: 唯一任务名称列表
    """
    unique_tasks = []
    task_set = set()

    for item in task_items:
        if len(item) >= 6 and item[5]:
            task_name = str(item[5]).strip()
            if task_name and task_name not in task_set:
                task_set.add(task_name)
                unique_tasks.append(task_name)

    return unique_tasks

def parallel_consumers_task(**context):
    """优化版并行执行任务 - 支持优先任务和普通任务分类执行"""
    print("=" * 60)
    print("【优化版并行消费者】开始执行测试任务...")
    print("=" * 60)

    try:
        # 从XCom获取生产者的数据
        l_col_values, d_precondition = context['task_instance'].xcom_pull(task_ids='读取测试用例')
        print(f"📊 从XCom获取到的测试用例数据: {len(l_col_values) if l_col_values else 0} 条")
        # print(699,d_precondition) {'MaxConcurrency': 2, 'priorityConcurrency': ['新增用户', '编辑用户']}

        if not l_col_values:
            print("⚠️ 没有找到测试用例数据")
            return {}

        # 获取优先任务配置
        PRIORITY_TASKS = d_precondition['priorityConcurrency']
        # PRIORITY_TASKS = d_precondition.get('priorityConcurrency', [])
        print(f"⚙️ 优先执行任务配置: {PRIORITY_TASKS}")

        # 优化：检查优先任务列表是否为空
        if not PRIORITY_TASKS:
            print("⚠️ 优先任务列表为空，将直接执行所有任务为普通任务")

        # 获取最大并发数配置并确保转换为整数
        max_concurrency_raw = get_max_concurrency(d_precondition)
        MAX_CONCURRENT_WORKERS = int(max_concurrency_raw)  # 确保转换为整数
        print(f"⚙️ 最大并发数配置: {MAX_CONCURRENT_WORKERS}")

        # 任务分类
        priority_task_items, normal_task_items = categorize_tasks(l_col_values, PRIORITY_TASKS)

        # 提取优先任务名称
        priority_task_names = extract_unique_tasks(priority_task_items)
        print(f"🎯 识别的优先任务: {priority_task_names}")

        # 存储所有执行结果
        all_results = {}

        # 优化：只有当存在优先任务时才执行第一步
        if priority_task_names:
            print("\n" + "=" * 50)
            print("🚀 第一步：执行优先任务")
            print("=" * 50)
            priority_results = execute_priority_tasks(
                priority_task_names,
                l_col_values,
                MAX_CONCURRENT_WORKERS
            )
            all_results.update(priority_results)
        else:
            print("⏭️ 无优先任务需要执行")

        # 第二步：执行普通任务
        if normal_task_items or not PRIORITY_TASKS:
            print("\n" + "=" * 50)
            print("🔄 执行任务（普通模式）")
            print("=" * 50)

            # 如果优先任务为空，则将所有任务作为普通任务执行
            if not PRIORITY_TASKS:
                print("💡 检测到优先任务为空，将所有任务按普通任务模式执行")
                normal_task_items = l_col_values

            normal_results = execute_normal_tasks(
                normal_task_items,
                MAX_CONCURRENT_WORKERS
            )
            all_results.update(normal_results)
        else:
            print("⏭️ 无普通任务需要执行")

        print("\n" + "=" * 60)
        print("🎉 【优化版并行消费者】所有测试执行完成")
        print("=" * 60)

        # 统计总体执行情况
        total_success = sum(result.get('success_count', 0) for result in all_results.values())
        total_fail = sum(result.get('fail_count', 0) for result in all_results.values())
        total_executed = sum(result.get('total_count', 0) for result in all_results.values())

        print(f"📈 总体统计:")
        print(f"   • 总执行任务数: {total_executed}")
        print(f"   • 成功: {total_success}")
        print(f"   • 失败: {total_fail}")
        print(f"   • 成功率: {total_success / total_executed * 100:.1f}%" if total_executed > 0 else "   • 成功率: 0%")

        return all_results

    except Exception as e:
        print(f"❌ 优化版并行消费者任务执行失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise e


def execute_normal_tasks(normal_task_items: List[List[Any]], max_concurrent: int) -> Dict[str, Any]:
    """
    执行普通任务（按原模式执行）

    Args:
        normal_task_items: 普通任务数据
        max_concurrent: 最大并发数

    Returns:
        Dict[str, Any]: 执行结果
    """
    if not normal_task_items:
        print("⚠️ 没有普通任务需要执行")
        return {}

    print("🔄 开始执行普通任务（按原模式）")

    # 提取普通任务的唯一名称
    unique_normal_tasks = extract_unique_tasks(normal_task_items)
    print(f"📋 普通任务列表: {unique_normal_tasks}")

    # 确保max_concurrent是整数类型
    try:
        max_concurrent = int(max_concurrent)
    except (ValueError, TypeError):
        max_concurrent = 2  # 默认值
        print(f"⚠️ 无法转换max_concurrent为整数，使用默认值: {max_concurrent}")

    # 按原模式执行普通任务
    all_results = {}
    batch_size = max_concurrent

    # 确保batch_size也是整数
    try:
        batch_size = int(batch_size)
    except (ValueError, TypeError):
        batch_size = 2
        print(f"⚠️ 无法转换batch_size为整数，使用默认值: {batch_size}")

    # 确保计算不会出错
    if len(unique_normal_tasks) == 0:
        total_batches = 0
    else:
        total_batches = (len(unique_normal_tasks) + batch_size - 1) // batch_size

    print(f"📊 普通任务将分为 {total_batches} 批执行，每批最多 {batch_size} 个任务并发")

    for batch_index in range(total_batches):
        start_index = batch_index * batch_size
        end_index = min((batch_index + 1) * batch_size, len(unique_normal_tasks))
        current_batch = unique_normal_tasks[start_index:end_index]

        print(f"\n🔄 开始执行普通任务第 {batch_index + 1}/{total_batches} 批: {current_batch}")

        futures_dict = {}
        results_dict = {}

        with concurrent.futures.ThreadPoolExecutor(
                max_workers=len(current_batch),
                thread_name_prefix=f"Normal_Batch{batch_index + 1}"
        ) as executor:

            for task_name in current_batch:
                print(f"📥 提交普通任务: {task_name}")
                future = executor.submit(_consumer_task_wrapper, task_name, normal_task_items)
                futures_dict[task_name] = future

            print(f"⏳ 等待普通任务批次 {batch_index + 1} 完成...")

            for task_name, future in futures_dict.items():
                try:
                    result = future.result(timeout=300)
                    results_dict[task_name] = result
                    print(f"✅ 普通任务 {task_name} 执行完成 - 成功:{result['success_count']}, 失败:{result['fail_count']}")
                except concurrent.futures.TimeoutError:
                    print(f"❌ 普通任务 {task_name} 执行超时")
                    results_dict[task_name] = {
                        "module": f"系统管理-角色管理-{task_name}",
                        "success_count": 0,
                        "fail_count": 0,
                        "total_count": 0,
                        "error": "执行超时"
                    }
                except Exception as e:
                    print(f"❌ 普通任务 {task_name} 执行失败: {str(e)}")
                    results_dict[task_name] = {
                        "module": f"系统管理-角色管理-{task_name}",
                        "success_count": 0,
                        "fail_count": 0,
                        "total_count": 0,
                        "error": str(e)
                    }

        all_results.update(results_dict)
        print(f"🏁 普通任务批次 {batch_index + 1} 执行完成")

        if batch_index < total_batches - 1:
            print("⏰ 等待2秒后开始下一批普通任务...")
            import time
            time.sleep(2)

    return all_results


def execute_priority_tasks(priority_tasks: List[str], l_col_values: List[List[Any]],
                           max_concurrent: int) -> Dict[str, Any]:
    """
    执行优先任务（并发执行）

    Args:
        priority_tasks: 优先任务列表
        l_col_values: 所有测试用例数据
        max_concurrent: 最大并发数

    Returns:
        Dict[str, Any]: 执行结果
    """
    if not priority_tasks:
        print("⚠️ 没有优先任务需要执行")
        return {}

    print(f"🚀 开始执行优先任务: {priority_tasks}")

    # 确保max_concurrent是整数类型
    try:
        max_concurrent = int(max_concurrent)
    except (ValueError, TypeError):
        max_concurrent = 2  # 默认值
        print(f"⚠️ 无法转换max_concurrent为整数，使用默认值: {max_concurrent}")

    # 分批执行优先任务
    batch_size = min(max_concurrent, len(priority_tasks))

    # 确保batch_size是整数
    try:
        batch_size = int(batch_size)
    except (ValueError, TypeError):
        batch_size = 1
        print(f"⚠️ 无法转换batch_size为整数，使用默认值: {batch_size}")

    # 确保计算不会出错
    if len(priority_tasks) == 0:
        total_batches = 0
    else:
        total_batches = (len(priority_tasks) + batch_size - 1) // batch_size

    all_results = {}

    for batch_index in range(total_batches):
        start_index = batch_index * batch_size
        end_index = min((batch_index + 1) * batch_size, len(priority_tasks))
        current_batch = priority_tasks[start_index:end_index]

        print(f"\n🎯 执行优先任务批次 {batch_index + 1}/{total_batches}: {current_batch}")

        futures_dict = {}
        results_dict = {}

        with concurrent.futures.ThreadPoolExecutor(
                max_workers=len(current_batch),
                thread_name_prefix=f"Priority_Batch{batch_index + 1}"
        ) as executor:

            # 提交当前批次的所有任务
            for task_name in current_batch:
                print(f"📥 提交优先任务: {task_name}")
                future = executor.submit(_consumer_task_wrapper, task_name, l_col_values)
                futures_dict[task_name] = future

            # 等待任务完成
            print(f"⏳ 等待优先任务批次 {batch_index + 1} 完成...")

            for task_name, future in futures_dict.items():
                try:
                    result = future.result(timeout=300)  # 5分钟超时
                    results_dict[task_name] = result
                    print(f"✅ 优先任务 {task_name} 执行完成 - 成功:{result['success_count']}, 失败:{result['fail_count']}")
                except concurrent.futures.TimeoutError:
                    print(f"❌ 优先任务 {task_name} 执行超时")
                    results_dict[task_name] = {
                        "module": f"系统管理-角色管理-{task_name}",
                        "success_count": 0,
                        "fail_count": 0,
                        "total_count": 0,
                        "error": "执行超时"
                    }
                except Exception as e:
                    print(f"❌ 优先任务 {task_name} 执行失败: {str(e)}")
                    results_dict[task_name] = {
                        "module": f"系统管理-角色管理-{task_name}",
                        "success_count": 0,
                        "fail_count": 0,
                        "total_count": 0,
                        "error": str(e)
                    }

        # 合并结果
        all_results.update(results_dict)
        print(f"🏁 优先任务批次 {batch_index + 1} 执行完成")

        # 批次间延迟
        if batch_index < total_batches - 1:
            print("⏰ 等待2秒后开始下一批优先任务...")
            import time
            time.sleep(2)

    return all_results




# 单个DAG，真正的并行执行
with DAG(
        dag_id="cdrd_角色管理_并发",
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
