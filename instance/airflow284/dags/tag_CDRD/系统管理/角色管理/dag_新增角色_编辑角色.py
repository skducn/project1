# # coding=utf-8
# # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# # Author     : John
# # Created on : 2026-2-26
# # Description: 单个DAG内串行执行
# # airflow UI：cdrd_新增用户
# # 设置依赖关系
# #     start >> producer >> [新增用户] >> final >> end
# # *****************************************************************
#
# import os, sys
# import re
# from datetime import datetime as dt, timedelta
#
# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from airflow.operators.dummy import DummyOperator
# import importlib.util
#
# # 添加项目根目录到Python路径
# current_dir = os.path.dirname(os.path.abspath(__file__))
# print(f"Current directory: {current_dir}")
#
# # 定位添加PO
# project_root = os.path.normpath(os.path.join(current_dir, "../../../../../.."))
# print(f"Calculated project root: {project_root}")
# if project_root not in sys.path:
#     sys.path.insert(0, project_root)
#     print(f"Added {project_root} to sys.path")
# # 验证PO模块路径
# po_path = os.path.join(project_root, 'PO')
# print(f"PO module path: {po_path}")
# # print(f"PO module exists: {os.path.exists(po_path)}")
#
# from PO.TimePO import *
# Time_PO = TimePO()
#
#
#
# # 定位项目配置路径
# web_project_root = os.path.normpath(os.path.join(current_dir, "../../../../../zyjk/CDRD/web"))
# print("项目配置路径", web_project_root)
#
# # 添加web目录到路径以便导入config模块
# if web_project_root not in sys.path:
#     sys.path.insert(0, web_project_root)
#     print(f"Added web project root to sys.path: {web_project_root}")
#
# from PO.OpenpyxlPO import OpenpyxlPO
# Openpyxl_PO = OpenpyxlPO(f"{web_project_root}/config/testcase.xlsx")
#
# # 配置文件路径
# config_file_path = os.path.join(web_project_root, "config", "config.ini")
# print(f"Config file path: {config_file_path}")
#
# from config.ConfigparserPO import ConfigparserPO
# Configparser_PO = ConfigparserPO(config_file_path)
# print("✓ 成功导入配置解析器")
#
# from PO.SqlserverPO import *
# Sqlserver_PO = SqlserverPO(
#     Configparser_PO.DB("host"),
#     Configparser_PO.DB("username"),
#     Configparser_PO.DB("password"),
#     Configparser_PO.DB("database")
# )
#
#
#
# def producer_task(**context):
#     """生产者任务：读取Excel测试用例"""
#     try:
#         shape = Openpyxl_PO.getL_shape(Configparser_PO.EXCEL("sheet"))
#         l_col_values = []
#         for i in range(shape[0]):
#             if Openpyxl_PO.getCell(i + 1, 2, Configparser_PO.EXCEL("sheet")) == "系统管理" and \
#                     Openpyxl_PO.getCell(i + 1, 3, Configparser_PO.EXCEL("sheet")) == "角色管理" and \
#                     Openpyxl_PO.getCell(i + 1, 11, Configparser_PO.EXCEL("sheet")) == "是":
#                 l_col_value = []
#                 l_col_value.append(i + 1)
#                 l_col_value.append(Openpyxl_PO.getCell(i + 1, 2, Configparser_PO.EXCEL("sheet")))  # 1 模块
#                 l_col_value.append(Openpyxl_PO.getCell(i + 1, 3, Configparser_PO.EXCEL("sheet")))  # 2 子模块
#                 l_col_value.append(Openpyxl_PO.getCell(i + 1, 4, Configparser_PO.EXCEL("sheet")))  # 3 前置条件
#                 l_col_value.append(Openpyxl_PO.getCell(i + 1, 12, Configparser_PO.EXCEL("sheet")))  # 4 自动化数据库校验
#                 l_col_value.append(Openpyxl_PO.getCell(i + 1, 13, Configparser_PO.EXCEL("sheet")))  # 5 自动化脚本
#                 l_col_value.append(Openpyxl_PO.getCell(i + 1, 14, Configparser_PO.EXCEL("sheet")))  # 6 自动化后置
#                 l_col_values.append(l_col_value)
#
#         print(f"【生产者】共找到 {len(l_col_values)} 条自动化测试用例")
#
#         # print(274, l_col_values)
#         # [[6, '系统管理', '用户管理', None, '[{"k": "select count(*) as qty from sys_user where job_num=\'{result[\'job_num\']}\'", "v": 1}]',
#         # '新增用户', '[["delete from sys_user where user_name=\'{result[\'user_name\']}\' and job_num=\'{result[\'job_num\']}\'"]]']]
#
#         # 将结果存储到XCom供后续任务使用
#         return l_col_values
#     except Exception as e:
#         print(f"❌ 生产者任务执行失败: {str(e)}")
#         raise e
#
#
# def consumer1_task(**context):
#     """消费者1任务：系统管理-用户管理"""
#     print("=" * 50)
#     print("【消费者1】开始执行系统管理-角色管理测试用例...")
#     print("=" * 50)
#
#     try:
#         # 从XCom获取生产者的数据 - 修正task_id
#         l_col_values = context['task_instance'].xcom_pull(task_ids='读取测试用例')
#         print(f"从XCom获取到的测试用例数据: {len(l_col_values) if l_col_values else 0} 条")
#
#         # 遍历符合条件的测试用例
#         if l_col_values:
#             for i in range(len(l_col_values)):
#                 test_execution(l_col_values[i], i)
#
#     except Exception as e:
#         print(f"❌ 消费者1任务执行失败: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         raise e
#
#
#
# def _execute_playwright_script(file, num):
#     """执行Playwright脚本"""
#     try:
#         file_path = f"{web_project_root}/{file}"
#         print(f"\n{num+1}, 执行脚本: {file_path}")
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
#             # print("✅ 找到run_playwright函数，开始执行...")
#             result = module.run_playwright()
#             # print(f"✅ Playwright执行完成，返回结果: {result}")
#             return result
#         else:
#             print("❌ 未找到 run_playwright 函数")
#             return None
#     except Exception as e:
#         print(f"❌ 执行失败: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return None
#
# def _updateStatus(status_count, errorLog, replace_variable, l_col_values):
#     # 依据状态更新
#
#     if status_count == 0:
#         # 通过，更新状态、处理后置
#         Openpyxl_PO.setCell(l_col_values[0], 10, "通过", Configparser_PO.EXCEL("sheet"))  # 状态
#         # 判断处理后置是否存在
#         if l_col_values[6] != None:
#             # 正则 - 处理后置
#             s_postposition_re = re.sub(r"\{result\['([^']+)'\]\}", replace_variable, l_col_values[6])
#             print(192, s_postposition_re)
#             l_postposition = eval(s_postposition_re)
#             print(f"解析后置数据: {l_postposition}")
#             if len(l_postposition) == 1:
#                 # 后置处理1
#                 try:
#                     Sqlserver_PO.execute(l_postposition[0][0])
#                     print("✅ 后置操作", l_postposition[0][0])
#                 except Exception as e:
#                     print(f"后置操作出错: {e}")
#             elif len(l_postposition) > 1:
#                 # 后置处理N
#                 try:
#                     for j in range(len(l_postposition)):
#                         Sqlserver_PO.execute(l_postposition[j][0])
#                         print("✅ 后置操作" + str(j + 1), l_postposition[j][0])
#                 except Exception as e:
#                     print(f"后置操作N出错: {e}")
#     else:
#         # 失败，更新状态、web实测结果
#         Openpyxl_PO.setCell(l_col_values[0], 10, "失败", Configparser_PO.EXCEL("sheet"))  # 状态
#         Openpyxl_PO.setCell(l_col_values[0], 9, errorLog, Configparser_PO.EXCEL("sheet"))  # web实测结果
#
#     # 更新时间
#     Openpyxl_PO.setCell(l_col_values[0], 15, Time_PO.getDateTimeByMinus(), Configparser_PO.EXCEL("sheet"))  # 完成时间
#
# def test_execution(l_col_values, num):
#     """执行单个测试用例并进行验证"""
#     # l_col_value.append(Openpyxl_PO.getCell(i + 1, 2, Configparser_PO.EXCEL("sheet")))  # 1 模块
#     # l_col_value.append(Openpyxl_PO.getCell(i + 1, 3, Configparser_PO.EXCEL("sheet")))  # 2 子模块
#     # l_col_value.append(Openpyxl_PO.getCell(i + 1, 4, Configparser_PO.EXCEL("sheet")))  # 3 前置条件
#     # l_col_value.append(Openpyxl_PO.getCell(i + 1, 12, Configparser_PO.EXCEL("sheet")))  # 4 自动化数据库校验
#     # l_col_value.append(Openpyxl_PO.getCell(i + 1, 13, Configparser_PO.EXCEL("sheet")))  # 5 自动化脚本
#     # l_col_value.append(Openpyxl_PO.getCell(i + 1, 14, Configparser_PO.EXCEL("sheet")))  # 6 自动化后置
#     # print(f"开始执行测试用例: {pathFile}")
#
#     pathFile = os.path.join(l_col_values[1], l_col_values[2], l_col_values[5] + ".py")  # 系统管理/用户管理/新增用户.py
#
#     # 执行自动化脚本
#     result = _execute_playwright_script(pathFile, num)
#     print(f"脚本执行成功，返回值: {result}")
#
#     # 如果Playwright执行失败，直接返回False
#     if result is None:
#         print("❌ Playwright执行失败，测试用例失败")
#         sys.exit(0)
#
#     # 正则匹配变量
#     def replace_variable(match):
#         var_name = match.group(1)
#         if isinstance(result, dict) and var_name in result:
#             return str(result[var_name])
#         else:
#             return match.group(0)
#
#     # try:
#     # 正则 - 自动化校验
#     s_validation = re.sub(r"\{result\['([^']+)'\]\}", replace_variable, l_col_values[4])
#     d_validation = eval(s_validation)
#     print(f"解析验证数据: {d_validation}")
#
#     if len(d_validation) == 1:
#         # 1条校验
#         errorLog = ""
#         status_count = 0
#         l_d_ = Sqlserver_PO.select(d_validation[0]['k'])
#         if l_d_[0]['qty'] == int(d_validation[0]['v']):
#             print("✅ 通过校验", d_validation[0])
#             status_count = status_count + 0
#         else:
#             print("❌ 失败校验", d_validation[0])
#             print("config中isSave:", Configparser_PO.用户管理("isSave"))
#             status_count = status_count + 1
#             errorLog = "v=" + str(l_d_[0]['qty'])
#
#         # 依据状态更新
#         _updateStatus(status_count, errorLog, replace_variable, l_col_values)
#
#     elif len(d_validation) > 1:
#         # 多条校验
#         errorLog = ""
#         status_count = 0
#         for j in range(len(d_validation)):
#             l_d_ = Sqlserver_PO.select(d_validation[j]['k'])
#             if l_d_[0]['qty'] == int(d_validation[j]['v']):
#                 print("✅ 通过校验" + str(j+1), d_validation[j])
#                 status_count = status_count + 0
#             else:
#                 print("❌ 失败校验" + str(j+1), d_validation[j])
#                 status_count = status_count + 1
#                 errorLog = str(d_validation[j]) + errorLog
#
#         # 依据状态更新
#         _updateStatus(status_count, errorLog, replace_variable, l_col_values)
#
#     else:
#         print("error, 自动化校验不能为空！")
#         # return False
#
#     # except Exception as e:
#     #     print(f"验证过程出错: {e}")
#     #     # return False
#
#
#
# # 单个DAG，任务并行执行
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
#     # 消费者任务（并行执行）
#     consumer1 = PythonOperator(
#         task_id="新增角色",
#         python_callable=consumer1_task,
#         provide_context=True
#     )
#
#
#     # 设置依赖关系 - 并行执行消费者
#     start >> producer >> consumer1 >> end
