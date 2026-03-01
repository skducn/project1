# # coding=utf-8
# # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# # Author     : John
# # Created on : 2026-2-27
# # Description: 主控DAG - 最简执行版本
# # airflow UI：cdrd_主控测试流程
# # *****************************************************************
#
# from datetime import datetime as dt, timedelta
# from airflow import DAG
# from airflow.operators.bash import BashOperator
# from airflow.operators.dummy import DummyOperator
#
# # 主控DAG
# with DAG(
#         dag_id="主控_系统管理",
#         start_date=dt(2026, 2, 13),
#         schedule_interval=None,
#         catchup=False,
#         tags=["cdrd", "主控", "系统管理"],
#         dagrun_timeout=timedelta(minutes=20),
# ) as main_dag:
#     start = DummyOperator(task_id="开始")
#     end = DummyOperator(task_id="结束")
#
#     # 直接使用BashOperator执行命令
#     trigger_user = BashOperator(
#         task_id="执行_用户管理测试",
#         bash_command="""
#             echo "🚀 开始执行用户管理测试..."
#             echo "🎯 触发DAG: cdrd_用户管理"
#             airflow dags trigger cdrd_用户管理
#             echo "✅ 用户管理测试触发完成"
#         """
#     )
#
#     trigger_role = BashOperator(
#         task_id="执行_角色管理测试",
#         bash_command="""
#             echo "🚀 开始执行角色管理测试..."
#             echo "🎯 触发DAG: cdrd_角色管理"
#             airflow dags trigger cdrd_角色管理
#             echo "✅ 角色管理测试触发完成"
#         """
#     )
#
#     # 设置执行流程：并行执行两个测试
#     start >> [trigger_user, trigger_role] >> end
