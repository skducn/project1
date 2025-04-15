# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-4-15
# 上传整个目录到服务器
# *****************************************************************
import os
import paramiko

def upload_directory(local_dir, remote_dir, host, user, password):
    # 上传目录到服务器
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
        print("上传完成")
    except Exception as e:
        print(f"上传过程中出现错误: {e}")


if __name__ == "__main__":
    # 本地要上传的目录
    local_directory = '/Users/linghuchong/Downloads/51/Python/project/flask/flask_gw_i/allureReport'
    # 服务器上的目标目录
    remote_directory = '/home/flask_gw_i/4446'
    # 服务器主机名或 IP 地址
    # 服务器主机名或 IP 地址
    server_host = '192.168.0.243'
    # 服务器用户名
    server_user = 'root'
    # 服务器密码
    server_password = 'Benetech79$#-'

    upload_directory(local_directory, remote_directory, server_host, server_user, server_password)
