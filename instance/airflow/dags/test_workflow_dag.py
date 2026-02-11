# 停止已运行的 Web Server
#      ps aux | grep airflow
#      kill -9 1809  # 替换为实际的 PID
# 或者直接删除 PID 文件（通常位于 $AIRFLOW_HOME/airflow-webserver.pid）
# rm $AIRFLOW_HOME / airflow - webserver.pid

# 重新启动 Web Server
#  airflow webserver --port 8080 -D

# 手动触发解析（可选）
# airflow dags reserialize

# 重启 Airflow Scheduler（必要时）
# airflow scheduler -D  # 后台运行

# 或用 airflow 命令停止（根据你的启动方式）
# pkill -f "airflow scheduler"
# pkill -f "airflow webserver"

# 查看环境

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import requests, json, mimetypes, smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from email.mime.application import MIMEApplication
import xlrd
from urllib.request import urlretrieve
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
from multiprocessing import Pool, cpu_count

import os

from cryptography.fernet import Fernet

def load_encrypted_api_key():
    # 读取密钥文件
    with open("/Users/linghuchong/Downloads/51/Python/project/instance/airflow/dags/secret.key", "rb") as key_file:
        key = key_file.read()

    # 读取加密的 API Key 文件
    with open("/Users/linghuchong/Downloads/51/Python/project/instance/airflow/dags/encrypted_api_key.txt", "rb") as encrypted_file:
        encrypted_api_key = encrypted_file.read()

    # 解密 API Key
    cipher_suite = Fernet(key)
    decrypted_api_key = cipher_suite.decrypt(encrypted_api_key).decode()
    return decrypted_api_key

def isFileType(varFilePath):
    # 4.1 判断文件类型
    # 根据文件的MIME类型判断文件类型
    # isFileType("/path/to/file.jpg")  # 返回: image
    # isFileType("/path/to/file.txt")  # 返回: text
    # isFileType("/path/to/file.pdf")  # 返回: application
    # isFileType("/path/to/unknown")    # 返回: unknown

    if not os.path.exists(varFilePath):
        return "file not found"

    # 获取文件的MIME类型
    mime_type, encoding = mimetypes.guess_type(varFilePath)

    if mime_type is None:
        return "unknown"

    # 根据MIME类型的主要类别进行分类
    main_type = mime_type.split('/')[0]

    return main_type


# 1，163邮件发送
def sendEmail(varAddresser, varTo, varCc,
              varSubject, varMIMEText,
              varHead, varConent, varFoot,*varAccessory):
    """

    :param varAddresser:
    :param varTo:
    :param varCc:
    varHead : 页眉
    :param varSubject:
    varFoot ：页脚
    :param varMIMEText: html/plain
    :param varConent:
    :param varAccessory:  文件可以是多个,用逗号分隔。
    :return:
    # 注意：邮件主题为‘test’时会出现错误。
    # 163邮箱密码为授权密码管理，在设置 - POP/SMTP/IMAP - 授权密码管理 - 新增，并在脚本中设置的登录密码为授权码。
    # 参数：发件人昵称，接收人邮箱，抄送人邮箱，主题，正文类型，正文，附件。
    """

    # 发件人（发件人名称，发件人邮箱）=> 令狐冲 <skducn@163.com>
    msg = email.mime.multipart.MIMEMultipart()
    addresser, addresserEmail = parseaddr(varAddresser + "<skducn@163.com>")
    # addresser, addresserEmail = parseaddr(varAddresser + u' <%s>' % "<skducn@163.com>")
    msg["From"] = formataddr((Header(addresser, "utf-8").encode(), addresserEmail))
    # 将邮件的name转换成utf-8格式，addresserEmail如果是unicode，则转换utf-8输出，否则直接输出，如：令狐冲 <skducn@163.com>

    # 收件人（收件人名称，收件人邮箱）=> 金浩 <h.jin@zy-healthtech.com>
    if "," in varTo:
        # 多个邮箱用逗号分隔
        varTo = [varTo.split(",")[0], varTo.split(",")[1]]
    msg["To"] = ";".join(varTo)

    # 抄送邮箱
    if varCc != None:
        msg["Cc"] = ";".join(varCc)
        # 所有接收邮箱
        reciver = varTo + varCc
    else:
        reciver = varTo

    # 标题
    msg["Subject"] = Header(varSubject, "utf-8").encode()

    # 正文 - 调用外部html文件
    if varMIMEText == "htmlFile":
        with open(varConent, "r", encoding="utf-8") as f:
            varConent = f.read()
        varConent = varHead + varConent + varFoot
        html = MIMEText(varConent, "html", "utf-8")
    elif varMIMEText == "htmlContent":
        # html格式的变量
        html = MIMEText(varConent, "html", "utf-8")
    elif varMIMEText == "excel":
        # excel转html格式
        ...
        # varConent = self.mailWrite(varConent)
        # print(varConent)
        # sys.exit(0)
        varConent = varHead + varConent + varFoot
        html = MIMEText(varConent, "html", "utf-8")
    else:
        # 文本格式
        varConent = varHead + varConent + varFoot
        html = MIMEText(varConent, "plain", "utf-8")
    msg.attach(html)

    # 附件
    for i in range(len(varAccessory)):
        # 获取文件类型
        varType = isFileType(varAccessory[i])

        # jpg\png\bmp
        if "image/" in varType:
            sendimagefile = open(varAccessory[i], "rb").read()
            image = MIMEImage(sendimagefile)
            # image.add_header('Content-ID', '<image1>')  # 默认文件名
            image.add_header(
                "Content-Disposition",
                "attachment",
                filename=("utf-8", "", os.path.basename(varAccessory[i])),
            )
            msg.attach(image)

        # html\txt\doc\xlsx\json\mp3\mp4\pdf\xmind
        elif (
                "text/html"
                or "text/plain"
                or "application/msword"
                or "spreadsheetml.sheet"
                or "application/json"
                or "audio/mpeg"
                or "video/mp4"
                or "application/pdf"
                or "application/vnd.xmind.workbook" in varType
        ):
            sendfile = open(varAccessory[i], "rb").read()
            text_att = MIMEText(sendfile, "base64", "utf-8")
            text_att["Content-Type"] = "application/octet-stream"
            # text_att.add_header('Content-Disposition', 'attachment', filename='interface.xls')   # 不支持中文格式文件名
            text_att.add_header(
                "Content-Disposition",
                "attachment",
                filename=("utf-8", "", os.path.basename(varAccessory[i])),
            )  # 支持中文格式文件名
            msg.attach(text_att)

    smtp = smtplib.SMTP()
    smtp.connect("smtp.163.com", "25")
    smtp.login("skducn@163.com", "MWiVfWqgVTrssv4s")
    smtp.sendmail("skducn@163.com", reciver, msg.as_string())
    smtp.quit()
    print("\n邮件已发送给：" + str(reciver) + "")


def send_report_email(**kwargs):
    sendEmail("令狐冲", ['h.jin@zy-healthtech.com'], ['skducn@163.com'],
              "自动化测试邮件", "plain", "你好", "\n\n附件是本次自动化接口测试结果，请查阅。",
              "\n\n这是一封自动生成的email，请勿回复，如有打扰请谅解。 \n\n测试组\nBest Regards",
              r'/Users/linghuchong/Downloads/51/Python/project/instance/摄像头/camera20231117163527.jpg'
              )


# ====================== 第一步：定义基础配置 ======================
default_args = {
    'owner': '金浩1',  # 负责人
    'depends_on_past': False,  # 不依赖上一次执行结果
    'start_date': datetime(2026, 1, 1),
    'email': ['skducn@163.com'],  # 报错时发送邮件
    'email_on_failure': True,
    'retries': 1,  # 失败重试1次
    'retry_delay': timedelta(minutes=5),
}


# ====================== 第二步：定义工作流函数 ======================
# 1. 调用通义千问API生成测试用例
def generate_test_cases(**kwargs):
    # 读取Airflow变量中的API Key（避免明文）
    api_key = kwargs['ti'].xcom_pull(key='dashscope_api_key') or 'sk-f3e3d8f64cab416fb028d582533c1e01'
    requirement_text = """用户登录功能，支持手机号/验证码登录，验证码有效期5分钟，错误3次锁定账号10分钟"""

    # 调用通义千问API
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"""
    角色：资深测试专家，生成结构化测试用例，格式为Markdown表格，包含：用例ID、测试模块、测试标题、前置条件、操作步骤、预期结果、优先级。
    需求：{requirement_text}
    """
    data = {
        "model": "qwen-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=data)
    # test_cases = response.json()["choices"][0]["message"]["content"]
    try:
        test_cases = response.json()["choices"][0]["message"]["content"]
    except KeyError as e:
        # logging.error(f"Missing key in response: {e}")
        test_cases = None  # 或设置默认值

    # 保存用例到文件（也可写入TestLink等管理工具）
    with open("/Users/linghuchong/Downloads/51/Python/project/instance/airflow/dags/test_cases.md", "w", encoding="utf-8") as f:
        f.write(test_cases)
    print("测试用例生成完成，路径：/Users/linghuchong/Downloads/51/Python/project/instance/airflow/dags/test_cases.md")


# 2. 执行自动化测试脚本（调用pytest）
def run_automation_test(**kwargs):
    import subprocess
    # 执行自动化测试并生成报告
    # capture_output=True：
    # 捕获命令的标准输出（stdout）和标准错误（stderr），避免直接打印到终端。
    # text=True：
    # 将输出以文本形式返回，而不是字节形式
    result = subprocess.run(
        ["pytest", "/Users/linghuchong/Downloads/51/Python/project/instance/pytest1/test_2.py", "-v",
         "--html=/Users/linghuchong/Downloads/51/Python/project/instance/airflow/dags/test_report.html"],
        capture_output=False, text=True
    )
    # 返回测试结果，供后续步骤使用
    return result.returncode  # 0=成功，非0=失败


# def downstream_task(**kwargs):
#     # 从 XCom 中拉取 API Key
#     api_key = kwargs['ti'].xcom_pull(task_ids='set_api_key')
#     print(f"获取到的 API Key 是: {api_key}")


# ====================== 第三步：定义DAG ======================
with DAG(
        '项目_工作流_hello',  # DAG名称（唯一）
        default_args=default_args,
        description='项目AI生成测试用例+自动化测试执行工作流',
        schedule_interval=timedelta(days=1),  # 每天执行一次，也可设为None（手动触发）
        catchup=False,  # 不补跑历史任务
        tags=['测试', '自动化123', 'AI'],
) as dag:
    # Task1：设置API Key（推荐用Airflow Variables管理，这里简化）
    set_api_key = BashOperator(
        task_id='set_api_key',
        bash_command=f'echo "{load_encrypted_api_key()}"',
        do_xcom_push=True,
    )

    some_task = BashOperator(
        task_id='some_task',
        bash_command='echo "API Key 是: {{ ti.xcom_pull(task_ids="set_api_key") }}"'
    )

    # Task2：生成测试用例
    gen_test_cases = PythonOperator(
        task_id='generate_test_cases',
        python_callable=generate_test_cases,
        provide_context=True,
    )

    # Task3：执行自动化测试
    run_test = PythonOperator(
        task_id='run_automation_test',
        python_callable=run_automation_test,
    )

    # # Task4：推送测试报告（示例：发送邮件，可替换为企业微信/钉钉）
    # send_report = PythonOperator(
    #     task_id='send_report',
    #     python_callable=send_report_email,
    #     # bash_command='echo "测试报告已生成：/tmp/test_report.html" | mail -s "自动化测试报告" skducn@163.com',
    # )

    # 定义任务执行顺序：se_api_key → gen_test_cases → run_test → send_report
    # set_api_key >> gen_test_cases >> run_test >> send_report
    set_api_key >> gen_test_cases >> run_test
    # gen_test_cases >> run_test >> send_report >> set_api_key
    # set_api_key >> some_task


# 测试工作流 2：数据校验
with DAG(
    dag_id="test_workflow_2",
    schedule="@weekly",
    default_args=default_args,
    tags=["test", "data_check"]
) as dag2:
    task1 = BashOperator(
        task_id="data_check",
        bash_command='echo "数据校验测试工作流 2 执行"'
    )

# 测试工作流 2：数据校验
with DAG(
    dag_id="test_workflow_3",
    schedule="@weekly",
    default_args=default_args,
    tags=["test", "data_check"]
) as dag2:
    task1 = BashOperator(
        task_id="data_check",
        bash_command='echo "数据校验测试工作流 2 执行"'
    )