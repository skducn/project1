# # coding=utf-8
# # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# # Author     : John
# # Created on : 2026-2-26
# # Description: 单个DAG内串行执行
# # airflow UI：cdrd_并发
# # 设置依赖关系
# #     start >> producer >> 并发 >> final >> end
# # *****************************************************************
#
# import os, sys
# import re
# from datetime import datetime as dt, timedelta
#
# # 添加项目根目录到Python路径
# current_dir = os.path.dirname(os.path.abspath(__file__))
# print(f"Current directory: {current_dir}")
#
# # 重新计算项目根目录路径
# project_root = os.path.normpath(os.path.join(current_dir, "../../../../../.."))
# print(f"Calculated project root: {project_root}")
#
# if project_root not in sys.path:
#     sys.path.insert(0, project_root)
#     print(f"Added {project_root} to sys.path")
#
# # 验证PO模块路径
# po_path = os.path.join(project_root, 'PO')
# print(f"PO module path: {po_path}")
# print(f"PO module exists: {os.path.exists(po_path)}")
#
# from PO.TimePO import *
#
# Time_PO = TimePO()
#
# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from airflow.operators.dummy import DummyOperator
# import importlib.util
# import subprocess
#
# from PO.OpenpyxlPO import *
#
# Openpyxl_PO = OpenpyxlPO("/Users/linghuchong/Downloads/51/Python/project/instance/zyjk/CDRD/web/config/testcase.xlsx")
#
# from PO.SqlserverPO import *
#
# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_TEST", "GBK")
#
#
# def execute_playwright_script_direct(file_path):
#     """直接执行Playwright脚本（使用subprocess）"""
#     try:
#         print(f"准备直接执行Playwright脚本: {file_path}")
#
#         # 检查文件是否存在
#         if not os.path.exists(file_path):
#             print(f"❌ Playwright脚本文件不存在: {file_path}")
#             return None
#
#         # 使用subprocess直接执行Python脚本
#         result = subprocess.run(
#             [sys.executable, file_path],
#             capture_output=True,
#             text=True,
#             timeout=120  # 2分钟超时
#         )
#
#         print(f"STDOUT: {result.stdout}")
#         if result.stderr:
#             print(f"STDERR: {result.stderr}")
#
#         if result.returncode == 0:
#             print("✅ 脚本执行成功")
#             return {"status": "success", "output": result.stdout}
#         else:
#             print("❌ 脚本执行失败")
#             return {"status": "failed", "error": result.stderr}
#
#     except subprocess.TimeoutExpired:
#         print("❌ 脚本执行超时")
#         return {"status": "timeout"}
#     except Exception as e:
#         print(f"❌ 执行失败: {str(e)}")
#         return None
#
#
# def execute_playwright_script_module(file):
#     """通过模块导入方式执行Playwright脚本"""
#     try:
#         file_path = f"/Users/linghuchong/Downloads/51/Python/project/instance/zyjk/CDRD/web/{file}"
#         print(f"准备通过模块方式执行Playwright脚本: {file_path}")
#
#         # 检查文件是否存在
#         if not os.path.exists(file_path):
#             print(f"❌ Playwright脚本文件不存在: {file_path}")
#             return None
#
#         spec = importlib.util.spec_from_file_location("playwright_script", file_path)
#         module = importlib.util.module_from_spec(spec)
#         script_dir = os.path.dirname(file_path)
#         if script_dir not in sys.path:
#             sys.path.insert(0, script_dir)
#
#         spec.loader.exec_module(module)
#
#         # 检查可用的函数
#         available_functions = [attr for attr in dir(module) if callable(getattr(module, attr))]
#         print(f"模块中可用的函数: {available_functions}")
#
#         # 尝试不同的函数名
#         function_names = ['run_playwright', 'main', 'execute']
#         result = None
#
#         for func_name in function_names:
#             if hasattr(module, func_name):
#                 print(f"✅ 找到函数: {func_name}，开始执行...")
#                 func = getattr(module, func_name)
#                 try:
#                     result = func()
#                     print(f"✅ 函数执行完成，返回结果: {result}")
#                     break
#                 except Exception as e:
#                     print(f"❌ 函数 {func_name} 执行失败: {str(e)}")
#                     continue
#             else:
#                 print(f"⚠️ 未找到函数: {func_name}")
#
#         if result is None:
#             print("❌ 未找到可执行的函数")
#             return None
#
#         return result
#     except Exception as e:
#         print(f"❌ 模块执行失败: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return None
#
#
# def producer_task(**context):
#     """生产者任务：读取Excel测试用例"""
#     print("=" * 50)
#     print("【生产者】开始读取测试用例...")
#     print("=" * 50)
#
#     try:
#         shape = Openpyxl_PO.getL_shape("v1.0")
#         l_col_values = []
#         for i in range(shape[0]):
#             if Openpyxl_PO.getCell(i + 1, 11, "v1.0") == "并发":
#                 l_col_value = []
#                 l_col_value.append(i + 1)
#
#
#                 l_col_value.append(Openpyxl_PO.getCell(i + 1, 2, "v1.0"))  # 1 模块
#                 l_col_value.append(Openpyxl_PO.getCell(i + 1, 3, "v1.0"))  # 2 子模块
#                 l_col_value.append(Openpyxl_PO.getCell(i + 1, 4, "v1.0"))  # 3 前置条件
#                 l_col_value.append(Openpyxl_PO.getCell(i + 1, 12, "v1.0"))  # 4 自动化数据库校验
#                 l_col_value.append(Openpyxl_PO.getCell(i + 1, 13, "v1.0"))  # 5 自动化脚本
#                 l_col_value.append(Openpyxl_PO.getCell(i + 1, 14, "v1.0"))  # 6 自动化后置
#                 l_col_values.append(l_col_value)
#
#         print(f"【生产者】共找到 {len(l_col_values)} 个需要执行的测试用例")
#         print("=" * 50)
#         print("【生产者】任务执行完成")
#         print("=" * 50)
#
#         # 将结果存储到XCom供后续任务使用
#         return l_col_values
#     except Exception as e:
#         print(f"❌ 生产者任务执行失败: {str(e)}")
#         raise e
#
#
# def consumer1_task(**context):
#     """消费者1任务：并发管理测试"""
#     print("=" * 50)
#     print("【消费者1】开始执行并发管理测试用例...")
#     print("=" * 50)
#
#     try:
#         # 从XCom获取生产者的数据
#         l_col_values_list = context['task_instance'].xcom_pull(task_ids='读取测试用例')
#         print(f"从XCom获取到的测试用例数据: {len(l_col_values_list) if l_col_values_list else 0} 条")
#
#         success_count = 0
#         fail_count = 0
#
#         # 遍历所有测试用例
#         if l_col_values_list:
#             for l_col_values in l_col_values_list:
#                 # 调试信息：打印当前测试用例信息
#                 print(f"当前测试用例: 模块={l_col_values[1]}, 子模块={l_col_values[2]}, 脚本={l_col_values[5]}")
#
#                 # 检查是否为并发管理相关的测试用例
#                 if (isinstance(l_col_values[1], str) and
#                         isinstance(l_col_values[2], str) and
#                         l_col_values[1] == "系统管理" and
#                         l_col_values[2] == "角色管理"):
#
#                     print(f"找到匹配的测试用例: {l_col_values[5]}")
#
#                     # 构建路径
#                     module_name = l_col_values[1]  # "系统管理"
#                     submodule_name = l_col_values[2]  # "角色管理"
#                     script_name = l_col_values[5]  # 从Excel中获取脚本名
#
#                     print(f"模块: {module_name}")
#                     print(f"子模块: {submodule_name}")
#                     print(f"脚本: {script_name}")
#
#                     # 方法1: 直接执行脚本文件
#                     full_path = f"/Users/linghuchong/Downloads/51/Python/project/instance/zyjk/CDRD/web/{module_name}/{submodule_name}/{script_name}.py"
#                     print(f"完整路径: {full_path}")
#
#                     result = execute_playwright_script_direct(full_path)
#                     if result and result.get('status') == 'success':
#                         success_count += 1
#                         print(f"✅ 测试用例执行成功")
#                     else:
#                         fail_count += 1
#                         print(f"❌ 测试用例执行失败")
#
#                 else:
#                     print(f"跳过不匹配的测试用例: 模块={l_col_values[1]}, 子模块={l_col_values[2]}")
#
#         print("=" * 50)
#         print(f"【消费者1】执行完成 - 成功: {success_count}, 失败: {fail_count}")
#         print("=" * 50)
#
#         return {
#             "module": "系统管理-并发管理",
#             "success_count": success_count,
#             "fail_count": fail_count,
#             "total_count": success_count + fail_count
#         }
#     except Exception as e:
#         print(f"❌ 消费者1任务执行失败: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         raise e
#
#
# def final_task(**context):
#     """收尾工作：汇总结果并更新Excel"""
#     print("=" * 50)
#     print("【收尾工作】开始汇总测试结果...")
#     print("=" * 50)
#
#     try:
#         # 获取消费者的结果
#         consumer1_result = context['task_instance'].xcom_pull(task_ids='并发')
#
#         print(f"消费者1结果: {consumer1_result}")
#
#         # 汇总统计
#         total_success = 0
#         total_fail = 0
#         total_tests = 0
#
#         if consumer1_result:
#             total_success += consumer1_result.get('success_count', 0)
#             total_fail += consumer1_result.get('fail_count', 0)
#             total_tests += consumer1_result.get('total_count', 0)
#
#         # 更新Excel汇总信息
#         summary_info = f"总计:{total_tests},通过:{total_success},失败:{total_fail}"
#         Openpyxl_PO.setCell(1, 15, summary_info, "v1.0")
#         Openpyxl_PO.setCell(1, 16, Time_PO.getDateTimeByMinus(), "v1.0")
#
#         print("=" * 50)
#         print(f"【收尾工作】测试执行汇总 - {summary_info}")
#         print("=" * 50)
#
#         return {
#             "summary": summary_info,
#             "total_tests": total_tests,
#             "total_success": total_success,
#             "total_fail": total_fail,
#             "execution_time": Time_PO.getDateTimeByMinus()
#         }
#     except Exception as e:
#         print(f"❌ 收尾工作执行失败: {str(e)}")
#         raise e
#
#
# # 单个DAG，任务串行执行
# with DAG(
#         dag_id="cdrd_并发",
#         start_date=dt(2026, 2, 13),
#         schedule_interval=None,  # 手动触发
#         catchup=False,
#         tags=["cdrd", "1系统管理", "2并发管理"],
#         render_template_as_native_obj=True
# ) as dag:
#     start = DummyOperator(task_id="start")
#     end = DummyOperator(task_id="end")
#
#     # 生产者任务
#     producer = PythonOperator(
#         task_id="读取测试用例",
#         python_callable=producer_task,
#         provide_context=True
#     )
#
#     # 消费者任务
#     consumer1 = PythonOperator(
#         task_id="并发",
#         python_callable=consumer1_task,
#         provide_context=True
#     )
#
#     # 收尾工作
#     final = PythonOperator(
#         task_id="收尾工作",
#         python_callable=final_task,
#         provide_context=True
#     )
#
#     # 设置依赖关系
#     # start >> producer >> consumer1 >> final >> end
#     start >> producer >> consumer1 >> end
