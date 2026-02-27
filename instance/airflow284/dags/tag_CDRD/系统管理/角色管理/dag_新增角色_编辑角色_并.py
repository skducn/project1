# # coding=utf-8
# # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# # Author     : John
# # Created on : 2026-2-26
# # Description: 优化版 - 真正并行执行消费者，同时打开Playwright
# # airflow UI：cdrd_新增角色_编辑角色
# # 设置依赖关系
# #     start >> producer >> [新增角色, 编辑角色] >> final >> end
# # *****************************************************************
#
# import os, sys
# import re
# from datetime import datetime as dt, timedelta
# import concurrent.futures
# import threading
#
# # 添加项目根目录到Python路径
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.normpath(os.path.join(current_dir, "../../../../../.."))
# print(f"Current directory: {current_dir}")
# print(f"Project root: {project_root}")
#
# if project_root not in sys.path:
#     sys.path.insert(0, project_root)
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
#
# from PO.OpenpyxlPO import *
#
# Openpyxl_PO = OpenpyxlPO("/Users/linghuchong/Downloads/51/Python/project/instance/zyjk/CDRD/web/testcase.xlsx")
#
# from PO.SqlserverPO import *
#
# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_TEST", "GBK")
#
#
# def execute_playwright_script(file):
#     """执行Playwright脚本"""
#     try:
#         file_path = f"/Users/linghuchong/Downloads/51/Python/project/instance/zyjk/CDRD/web/{file}"
#         print(f"[线程 {threading.current_thread().name}] 准备执行Playwright脚本: {file_path}")
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
#         if hasattr(module, 'run_playwright'):
#             print(f"[线程 {threading.current_thread().name}] ✅ 找到run_playwright函数，开始执行...")
#             result = module.run_playwright()
#             print(f"[线程 {threading.current_thread().name}] ✅ Playwright执行完成，返回结果: {result}")
#             return result
#         else:
#             print(f"[线程 {threading.current_thread().name}] ❌ 未找到 run_playwright 函数")
#             return None
#     except Exception as e:
#         print(f"[线程 {threading.current_thread().name}] ❌ 执行失败: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return None
#
#
# def test_execution(pathFile, l_col_values, i):
#     """执行单个测试用例并进行验证"""
#     thread_name = threading.current_thread().name
#     print(f"[{thread_name}] 开始执行测试用例: {pathFile}")
#     result = execute_playwright_script(pathFile)
#     print(f"[{thread_name}] Playwright执行结果: {result}")
#
#     # 如果Playwright执行失败，直接返回False
#     if result is None:
#         print(f"[{thread_name}] ❌ Playwright执行失败，测试用例失败")
#         return False
#
#     def replace_variable(match):
#         var_name = match.group(1)
#         if isinstance(result, dict) and var_name in result:
#             return str(result[var_name])
#         else:
#             return match.group(0)
#
#     formatted_string = re.sub(r"\{result\['([^']+)'\]\}", replace_variable, l_col_values[i][4])
#     print(f"[{thread_name}] 正则替换结果: {formatted_string}")
#
#     try:
#         d_validation = eval(formatted_string)
#         print(f"[{thread_name}] 解析后的验证数据: {d_validation}")
#
#         if len(d_validation) == 1:
#             l_d_ = Sqlserver_PO.select(d_validation[0]['k'])
#             print(f"[{thread_name}] 查询结果: {l_d_[0]['qty']}")
#
#             if l_d_[0]['qty'] == int(d_validation[0]['v']):
#                 print(f"[{thread_name}] ✅ 断言通过")
#                 Openpyxl_PO.setCell(l_col_values[i][0], 10, "通过", "v1.0")
#                 return True
#             else:
#                 print(f"[{thread_name}] ❌ 断言失败")
#                 Openpyxl_PO.setCell(l_col_values[i][0], 10, "失败", "v1.0")
#                 Openpyxl_PO.setCell(l_col_values[i][0], 9, "v=" + str(l_d_[0]['qty']), "v1.0")
#                 return False
#         elif len(d_validation) > 1:
#             error = 0
#             errorLog = ""
#             for j in range(len(d_validation)):
#                 l_d_ = Sqlserver_PO.select(d_validation[j]['k'])
#                 if l_d_[0]['qty'] == int(d_validation[j]['v']):
#                     print(f"[{thread_name}] ✅ 断言通过")
#                     Openpyxl_PO.setCell(l_col_values[i][0], 10, "通过", "v1.0")
#                 else:
#                     print(f"[{thread_name}] ❌ 断言失败")
#                     Openpyxl_PO.setCell(l_col_values[i][0], 10, "失败", "v1.0")
#                     errorLog = str(d_validation[j]) + errorLog
#                     error = 1
#             if error == 1:
#                 Openpyxl_PO.setCell(l_col_values[i][0], 9, errorLog, "v1.0")
#                 return False
#             else:
#                 return True
#         else:
#             print(f"[{thread_name}] error, 自动化校验不能为空！")
#             return False
#
#     except Exception as e:
#         print(f"[{thread_name}] 验证过程出错: {e}")
#         return False
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
#             if Openpyxl_PO.getCell(i + 1, 11, "v1.0") == "是":
#                 l_col_value = []
#                 l_col_value.append(i + 1)
#                 l_col_value.append(Openpyxl_PO.getCell(i + 1, 2, "v1.0"))  # 模块
#                 l_col_value.append(Openpyxl_PO.getCell(i + 1, 3, "v1.0"))  # 子模块
#                 l_col_value.append(Openpyxl_PO.getCell(i + 1, 4, "v1.0"))  # 前置条件
#                 l_col_value.append(Openpyxl_PO.getCell(i + 1, 12, "v1.0"))  # 自动化数据库校验
#                 l_col_value.append(Openpyxl_PO.getCell(i + 1, 13, "v1.0"))  # 自动化脚本
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
# def consumer_task_wrapper(test_type, l_col_values):
#     """消费者任务包装器 - 支持并行执行"""
#     print(f"={'=' * 20} {test_type} 消费者开始执行 {'=' * 20}")
#
#     success_count = 0
#     fail_count = 0
#
#     if l_col_values:
#         for i in range(len(l_col_values)):
#             # 根据测试类型过滤测试用例
#             if test_type == "新增角色":
#                 condition = (l_col_values[i][1] == "系统管理" and
#                              l_col_values[i][2] == "角色管理" and
#                              "新增角色" in str(l_col_values[i][5]))
#             else:  # 编辑角色
#                 condition = (l_col_values[i][1] == "系统管理" and
#                              l_col_values[i][2] == "角色管理" and
#                              "编辑角色" in str(l_col_values[i][5]))
#
#             if condition:
#                 print(f"[{test_type}] 找到测试用例: {l_col_values[i][5]}")
#                 pathFile = os.path.join(l_col_values[i][1], l_col_values[i][2], l_col_values[i][5])
#                 print(f"[{test_type}] 执行路径: {pathFile}")
#
#                 result = test_execution(pathFile, l_col_values, i)
#                 if result:
#                     success_count += 1
#                     print(f"[{test_type}] ✅ 测试用例执行成功")
#                 else:
#                     fail_count += 1
#                     print(f"[{test_type}] ❌ 测试用例执行失败")
#             else:
#                 print(f"[{test_type}] 跳过不匹配的测试用例: {l_col_values[i][5]}")
#
#     print(f"={'=' * 20} {test_type} 消费者执行完成 {'=' * 20}")
#     print(f"[{test_type}] 成功: {success_count}, 失败: {fail_count}")
#
#     return {
#         "module": f"系统管理-角色管理-{test_type}",
#         "success_count": success_count,
#         "fail_count": fail_count,
#         "total_count": success_count + fail_count
#     }
#
#
# def parallel_consumers_task(**context):
#     """并行执行两个消费者任务"""
#     print("=" * 50)
#     print("【并行消费者】开始同时执行新增角色和编辑角色测试...")
#     print("=" * 50)
#
#     try:
#         # 从XCom获取生产者的数据
#         l_col_values = context['task_instance'].xcom_pull(task_ids='读取测试用例')
#         print(f"从XCom获取到的测试用例数据: {len(l_col_values) if l_col_values else 0} 条")
#
#         # 使用线程池并行执行两个消费者
#         with concurrent.futures.ThreadPoolExecutor(max_workers=2, thread_name_prefix="Consumer") as executor:
#             # 提交两个任务
#             future_new_role = executor.submit(consumer_task_wrapper, "新增角色", l_col_values)
#             future_edit_role = executor.submit(consumer_task_wrapper, "编辑角色", l_col_values)
#
#             # 等待两个任务完成
#             result_new_role = future_new_role.result()
#             result_edit_role = future_edit_role.result()
#
#         print("=" * 50)
#         print("【并行消费者】所有测试执行完成")
#         print("=" * 50)
#
#         # 返回两个消费者的结果
#         return {
#             "新增角色": result_new_role,
#             "编辑角色": result_edit_role
#         }
#     except Exception as e:
#         print(f"❌ 并行消费者任务执行失败: {str(e)}")
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
#         # 获取并行消费者的结果
#         consumer_results = context['task_instance'].xcom_pull(task_ids='并行执行消费者')
#
#         print(f"消费者结果: {consumer_results}")
#
#         # 汇总统计
#         total_success = 0
#         total_fail = 0
#         total_tests = 0
#
#         if consumer_results:
#             # 处理新增角色结果
#             new_role_result = consumer_results.get('新增角色')
#             if new_role_result:
#                 total_success += new_role_result.get('success_count', 0)
#                 total_fail += new_role_result.get('fail_count', 0)
#                 total_tests += new_role_result.get('total_count', 0)
#                 print(f"新增角色 - 成功: {new_role_result.get('success_count')}, 失败: {new_role_result.get('fail_count')}")
#
#             # 处理编辑角色结果
#             edit_role_result = consumer_results.get('编辑角色')
#             if edit_role_result:
#                 total_success += edit_role_result.get('success_count', 0)
#                 total_fail += edit_role_result.get('fail_count', 0)
#                 total_tests += edit_role_result.get('total_count', 0)
#                 print(f"编辑角色 - 成功: {edit_role_result.get('success_count')}, 失败: {edit_role_result.get('fail_count')}")
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
#             "execution_time": Time_PO.getDateTimeByMinus(),
#             "detailed_results": consumer_results
#         }
#     except Exception as e:
#         print(f"❌ 收尾工作执行失败: {str(e)}")
#         raise e
#
#
# # 单个DAG，真正的并行执行
# with DAG(
#         dag_id="cdrd_新增角色_编辑角色",
#         start_date=dt(2026, 2, 13),
#         schedule_interval=None,  # 手动触发
#         catchup=False,
#         tags=["cdrd", "1系统管理", "2角色管理"],
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
#     # 真正并行执行的消费者任务
#     parallel_consumers = PythonOperator(
#         task_id="并行执行消费者",
#         python_callable=parallel_consumers_task,
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
#     # 设置依赖关系 - 真正的并行执行
#     start >> producer >> parallel_consumers >> final >> end
