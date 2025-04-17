import os
import paramiko
import subprocess

from flask import Flask, send_from_directory

from PO.LogPO import *

# _path = os.path.dirname(__file__)  # 获取当前文件路径
Log_PO = LogPO('nohup.out', level="debug")
# import fabric
# print(f"Fabric version: {fabric.__version__}")

user = 'root'
host = '192.168.0.243'
password = 'Benetech79$#-'
# Allure 报告生成的目录
ALLURE_REPORT_DIR = 'allureReport'
s_localFolder = f"/Users/linghuchong/Downloads/51/Python/project/flask/flask_gw_i/{ALLURE_REPORT_DIR}"
s_remoteFolder = f"/home/flask_gw_i/{ALLURE_REPORT_DIR}"

app = Flask(__name__)

# 创建日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 创建文件处理器
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# 创建格式化器并添加到处理器
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 将处理器添加到记录器
logger.addHandler(file_handler)


def upload_directory(local_dir, remote_dir):
    # 上传整个目录
    try:
        # 创建 SSH 对象
        ssh = paramiko.SSHClient()
        # 允许连接不在 know_hosts 文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(hostname=host, port=22, username=user, password=password)
        # 创建 SFTP 对象
        sftp = ssh.open_sftp()

        def upload(local_path, remote_path):
            if os.path.isfile(local_path):
                sftp.put(local_path, remote_path)
                # print(f"上传文件 {local_path} 到 {remote_path}")
            elif os.path.isdir(local_path):
                try:
                    sftp.stat(remote_path)
                except FileNotFoundError:
                    sftp.mkdir(remote_path)
                for item in os.listdir(local_path):
                    local_item_path = os.path.join(local_path, item)
                    remote_item_path = os.path.join(remote_path, item)
                    upload(local_item_path, remote_item_path)

        upload(local_dir, remote_dir)

        # 关闭连接
        sftp.close()
        ssh.close()
        print("Allure 上传完成")
        logger.debug('Allure 上传完成')

    except Exception as e:
        print(f"上传过程中出现错误: {e}")
        logger.debug(f"上传过程中出现错误: {e}")


# todo 删除 allureReport
if os.path.exists(ALLURE_REPORT_DIR):
    # 删除allureReport
    os.system(f"rm -rf {ALLURE_REPORT_DIR}")

# todo 生成 allureReport
subprocess.run(["pytest --alluredir=allure-results"], shell=True)
subprocess.run([f"allure generate allure-results -o {ALLURE_REPORT_DIR}"], shell=True)
print("Allure 报告已生成")
logger.debug('Allure 报告已生成')

# todo 上传 allureReport 到远程服务器
upload_directory(s_localFolder, s_remoteFolder)


@app.route('/')
def index():
    logger.debug('这是一条调试级别的日志')
    logger.info('这是一条信息级别的日志')
    logger.warning('这是一条警告级别的日志')
    logger.error('这是一条错误级别的日志')
    logger.critical('这是一条严重错误级别的日志')
    return send_from_directory(ALLURE_REPORT_DIR, 'index.html')


@app.route('/<path:path>')
def send_report(path):
    return send_from_directory(ALLURE_REPORT_DIR, path)


if __name__ == '__main__':
    # 确保 Allure 报告目录存在
    if not os.path.exists(ALLURE_REPORT_DIR):
        print(f"Allure 报告目录 {ALLURE_REPORT_DIR} 不存在，请先生成 Allure 报告。")
    else:
        app.run(debug=True)
