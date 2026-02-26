# 1个生产者 → 1个消费者（2个任务）
# 功能：消费者任务1从生产者中获取Xcom值，处理后，传递给任务2处理

# 场景：
# task1 (c_cdrd_TASK1) 执行 → 返回值自动存储到XCom
# task1 >> task2 依赖关系确保顺序
# task2 (c_cdrd_TASK2) 执行 → 从XCom获取task1的返回值 → 进行后续处理
# 这样就实现了任务间的数据传递和处理链。

import os, sys

# 添加项目根目录到Python路径
# 计算项目根目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))
print(f"Current directory: {current_dir}")
print(f"Project root: {project_root}")

if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to sys.path")

# 验证PO模块是否存在
po_path = os.path.join(project_root, 'PO')
print(f"PO module path: {po_path}")
print(f"PO module exists: {os.path.exists(po_path)}")

from PO.TimePO import *
Time_PO = TimePO()

from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from datetime import datetime as dt, timedelta
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.models import TaskInstance, DagRun
from airflow.utils.session import create_session
from airflow.configuration import conf
import importlib.util
import sys

from PO.OpenpyxlPO import *
Openpyxl_PO = OpenpyxlPO("/Users/linghuchong/Downloads/51/Python/project/instance/zyjk/CDRD/web/testcase.xlsx")

from PO.SqlserverPO import *




# 患者发现
Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_TEST", "GBK")
# ===================== 1. 定义 Dataset =====================
# 用 URI 唯一标识数据集（格式：dataset://<数据源>/<表名>，自定义即可）
dataset_cdrd = Dataset(
    uri="dataset://cdrd/1p1n2t",
    extra={
        "description": "订单同步表 dw_order，来自业务库的订单数据",
        "owner": "john",
        "version": "1.5"
    }
)

# 封装通用读取函数
def get_xcom(varDagId, varTaskId, **context):
    """
    从指定生产者/消费者任务中获取 XCom 值
    用于消费者之间的数据传递
    """
    xcom_value = None

    try:
        with create_session() as session:
            # 查找最新的成功运行的消费者 DAG Run
            latest_dag_run = session.query(DagRun).filter(
                DagRun.dag_id == varDagId,
                DagRun.state == "success"
            ).order_by(DagRun.execution_date.desc()).first()

            if latest_dag_run:
                # 查找对应的 Task Instance
                ti = session.query(TaskInstance).filter(
                    TaskInstance.dag_id == varDagId,
                    TaskInstance.task_id == varTaskId,
                    TaskInstance.run_id == latest_dag_run.run_id
                ).first()

                if ti:
                    # 从 XCom 中拉取数据
                    xcom_value = ti.xcom_pull(task_ids=varTaskId, key="return_value")
                    print(f"✅ 成功从消费者 {varDagId}.{varTaskId} 获取 XCom 值: {xcom_value}")
                else:
                    print("⚠️ 未找到对应的消费者 Task Instance")
            else:
                print("⚠️ 未找到成功的消费者 DAG Run")
    except Exception as e:
        print(f"❌ 查询消费者 XCom 失败: {str(e)}")

    return xcom_value


# ===================== 生产者 DAG（更新数据集+ 存储返回值） =====================
# 该 DAG 执行后，会标记 dataset_cdrd 为"已更新"
def p_cdrd_TASK(**context):
    shape = Openpyxl_PO.getL_shape("v1.0")
    l_col_values = []
    for i in range(shape[0]):
        if Openpyxl_PO.getCell(i + 1, 11, "v1.0") == "是":
            l_col_value = []
            l_col_value.append(i + 1)
            l_col_value.append(Openpyxl_PO.getCell(i+1, 2, "v1.0"))  # 模块
            l_col_value.append(Openpyxl_PO.getCell(i+1, 3, "v1.0"))  # 子模块
            l_col_value.append(Openpyxl_PO.getCell(i+1, 4, "v1.0"))  # 前置条件
            l_col_value.append(Openpyxl_PO.getCell(i+1, 12, "v1.0"))  # 自动化数据库校验
            l_col_value.append(Openpyxl_PO.getCell(i+1, 13, "v1.0"))  # 自动化脚本
            l_col_values.append(l_col_value)


    return l_col_values
# 生产者 DAG
with DAG(
        dag_id="p_cdrd_all", start_date=dt(2026, 2, 13), schedule_interval=None,  # 手动触发（也可设为时间调度，如 "@daily"）
        catchup=False, tags=["cdrd", "生产者"], render_template_as_native_obj=True
) as producer_dag:
    sync_task = PythonOperator(task_id="p_cdrd_TASK", python_callable=p_cdrd_TASK, outlets=[dataset_cdrd], provide_context=True)




def execute_playwright_script(file):
    file_path = f"/Users/linghuchong/Downloads/51/Python/project/instance/zyjk/CDRD/web/{file}"
    # 动态导入模块
    spec = importlib.util.spec_from_file_location("playwright_script", file_path)
    module = importlib.util.module_from_spec(spec)
    # 添加到系统路径
    script_dir = os.path.dirname(file_path)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    try:
        spec.loader.exec_module(module)
        # 调用模块中的函数并传递测试数据
        if hasattr(module, 'run_playwright'):
            result = module.run_playwright()
            # print(f"Playwright 执行结果: {result}")
            return result
        else:
            print("未找到 run_playwright 函数")
            return None
    except Exception as e:
        print(f"执行失败: {str(e)}")


# ===================== 消费者1 DAG（监听数据集 + 读取生产者 XCom） =====================
# 该 DAG 监听 dataset_1p2n，数据更新时自动触发
def c_cdrd_TASK1(**context):
    # 读取生产者的返回值
    l_col_values = get_xcom("p_cdrd_all", "p_cdrd_TASK", **context)
    for i in range(len(l_col_values)):
        if l_col_values[i][1] == "系统管理" and l_col_values[i][2] == "用户管理":

            pathFile = os.path.join(l_col_values[i][1], l_col_values[i][2], l_col_values[i][5])
            result = execute_playwright_script(pathFile)
            # print(f"最终返回结果: {result}") #  {'status': 'success', 'name': '沙龙', 'phone': '13618714419', 'email': 'xiulan66@example.com', 'account': '377754', 'work_id': '769777'}

            def replace_variable(match):
                var_name = match.group(1)
                # 从result字典中获取对应值
                if isinstance(result, dict) and var_name in result:
                    return str(result[var_name])
                else:
                    # 如果找不到对应值，返回原字符串
                    return match.group(0)

            formatted_string = re.sub(r"\{result\['([^']+)'\]\}", replace_variable, l_col_values[i][4])
            print(f"正则替换结果: {formatted_string}")

            # 如果需要eval执行SQL查询
            try:
                d_validation = eval(formatted_string)
                print(f"解析后的验证数据: {d_validation}")

                # 执行数据库查询验证
                if len(d_validation) == 1:
                    l_d_ = Sqlserver_PO.select(d_validation[0]['k'])
                    print(f"查询结果: {l_d_[0]['qty']}")

                    if l_d_[0]['qty'] == int(d_validation[0]['v']):
                        print("✅ 断言通过")
                        Openpyxl_PO.setCell(l_col_values[i][0], 10, "通过", "v1.0")
                    else:
                        print("❌ 断言失败")
                        Openpyxl_PO.setCell(l_col_values[i][0], 10, "失败", "v1.0")
                        Openpyxl_PO.setCell(l_col_values[i][0], 9, "v=" + str(l_d_[0]['qty']), "v1.0")
                elif len(d_validation) > 1:
                    error = 0
                    errorLog = ""
                    for j in range(len(d_validation)):
                        l_d_ = Sqlserver_PO.select(d_validation[j]['k'])
                        print(f"查询结果: {l_d_[0]['qty']}")

                        if l_d_[0]['qty'] == int(d_validation[j]['v']):
                            print("✅ 断言通过")
                            Openpyxl_PO.setCell(l_col_values[i][0], 10, "通过", "v1.0")
                        else:
                            print("❌ 断言失败")
                            Openpyxl_PO.setCell(l_col_values[i][0], 10, "失败", "v1.0")
                            errorLog = str(d_validation[j]) + errorLog
                            error = 1
                    if error == 1:
                        Openpyxl_PO.setCell(l_col_values[i][0], 9, errorLog, "v1.0")
                else:
                    print("error, 自动化校验不能为空！")


            except Exception as e:
                    print(f"验证过程出错: {e}")
# 消费者1 DAG
with DAG(
        dag_id="c_cdrd_DAG1", start_date=dt(2026, 2, 13), schedule=[dataset_cdrd], catchup=False,
        tags=["cdrd", "系统管理", "用户管理"], render_template_as_native_obj=True
) as consumer_dag:
    clean_task = PythonOperator(task_id="c_cdrd_TASK1", python_callable=c_cdrd_TASK1,
                                inlets=[dataset_cdrd], provide_context=True)



# ===================== 消费者2 DAG（监听数据集 + 读取生产者 XCom） =====================
def c_cdrd_TASK2(**context):
    l_col_values = get_xcom("p_cdrd_all", "p_cdrd_TASK", **context)
    for i in range(len(l_col_values)):
        if l_col_values[i][1] == "系统管理" and l_col_values[i][2] == "角色管理":
            pathFile = os.path.join(l_col_values[i][1], l_col_values[i][2], l_col_values[i][5])

            result = execute_playwright_script(pathFile)
            print(f"最终返回结果: {result}")

            def replace_variable(match):
                var_name = match.group(1)
                # 从result字典中获取对应值
                if isinstance(result, dict) and var_name in result:
                    return str(result[var_name])
                else:
                    # 如果找不到对应值，返回原字符串
                    return match.group(0)

            formatted_string = re.sub(r"\{result\['([^']+)'\]\}", replace_variable, l_col_values[i][4])
            print(f"正则替换结果: {formatted_string}")

            # 如果需要eval执行SQL查询
            try:
                d_validation = eval(formatted_string)
                print(f"解析后的验证数据: {d_validation}")

                # 执行数据库查询验证
                if len(d_validation) == 1:
                    l_d_ = Sqlserver_PO.select(d_validation[0]['k'])
                    print(f"查询结果: {l_d_[0]['qty']}")

                    if l_d_[0]['qty'] == int(d_validation[0]['v']):
                        print("✅ 断言通过")
                        Openpyxl_PO.setCell(l_col_values[i][0], 10, "通过", "v1.0")
                    else:
                        print("❌ 断言失败")
                        Openpyxl_PO.setCell(l_col_values[i][0], 10, "失败", "v1.0")
                        Openpyxl_PO.setCell(l_col_values[i][0], 9, "v=" + str(l_d_[0]['qty']), "v1.0")
                elif len(d_validation) > 1:
                    error = 0
                    errorLog = ""
                    for j in range(len(d_validation)):
                        l_d_ = Sqlserver_PO.select(d_validation[j]['k'])
                        print(f"查询结果: {l_d_[0]['qty']}")

                        if l_d_[0]['qty'] == int(d_validation[j]['v']):
                            print("✅ 断言通过")
                            Openpyxl_PO.setCell(l_col_values[i][0], 10, "通过", "v1.0")
                        else:
                            print("❌ 断言失败")
                            Openpyxl_PO.setCell(l_col_values[i][0], 10, "失败", "v1.0")
                            errorLog = str(d_validation[j]) + errorLog
                            error = 1
                    if error == 1:
                        Openpyxl_PO.setCell(l_col_values[i][0], 9, errorLog, "v1.0")
                else:
                    print("error, 自动化校验不能为空！")

            except Exception as e:
                    print(f"验证过程出错: {e}")

# 消费者2 DAG
with DAG(
        dag_id="c_cdrd_DAG2", start_date=dt(2026, 2, 13), schedule=[dataset_cdrd], catchup=False,
        tags=["cdrd", "系统管理", "角色管理"], render_template_as_native_obj=True
) as consumer2_dag:
    stat_task = PythonOperator(task_id="c_cdrd_TASK2", python_callable=c_cdrd_TASK2,
                               inlets=[dataset_cdrd], provide_context=True)


