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
                print(f"上传文件 {local_path} 到 {remote_path}")
            elif os.path.isdir(local_path):
                try:
                    sftp.stat(remote_path)
                except FileNotFoundError:
                    sftp.mkdir(remote_path)
                    print(f"创建远程目录 {remote_path}")
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


def download_directory(remote_dir, local_dir, host, user, password):
    # 从服务器下载目录到本地
    try:
        # 创建 SSH 对象
        ssh = paramiko.SSHClient()
        # 允许连接不在 know_hosts 文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(hostname=host, port=22, username=user, password=password)
        # 创建 SFTP 对象
        sftp = ssh.open_sftp()

        def download(remote_path, local_path):
            # 获取远程路径信息
            try:
                remote_stat = sftp.stat(remote_path)
            except FileNotFoundError:
                print(f"远程路径不存在: {remote_path}")
                return

            # 如果是文件
            if not hasattr(remote_stat, 'st_mode') or not stat.S_ISDIR(remote_stat.st_mode):
                # 确保本地目录存在
                local_dir_path = os.path.dirname(local_path)
                if not os.path.exists(local_dir_path):
                    os.makedirs(local_dir_path)
                # 下载文件
                sftp.get(remote_path, local_path)
                print(f"下载文件 {remote_path} 到 {local_path}")
            else:
                # 如果是目录
                if not os.path.exists(local_path):
                    os.makedirs(local_path)
                    print(f"创建本地目录 {local_path}")

                # 列出目录内容
                try:
                    items = sftp.listdir_attr(remote_path)
                    for item in items:
                        remote_item_path = os.path.join(remote_path, item.filename).replace('\\', '/')
                        local_item_path = os.path.join(local_path, item.filename)
                        download(remote_item_path, local_item_path)
                except Exception as e:
                    print(f"列出目录 {remote_path} 时出错: {e}")

        # 添加 stat 模块导入
        import stat
        download(remote_dir, local_dir)

        # 关闭连接
        sftp.close()
        ssh.close()
        print("下载完成")
    except Exception as e:
        print(f"下载过程中出现错误: {e}")


def download_file(remote_file, local_file, host, user, password):
    # 从服务器下载单个文件到本地
    try:
        # 创建 SSH 对象
        ssh = paramiko.SSHClient()
        # 允许连接不在 know_hosts 文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(hostname=host, port=22, username=user, password=password)
        # 创建 SFTP 对象
        sftp = ssh.open_sftp()

        # 确保本地目录存在
        local_dir = os.path.dirname(local_file)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        # 下载文件
        sftp.get(remote_file, local_file)
        print(f"下载文件 {remote_file} 到 {local_file}")

        # 关闭连接
        sftp.close()
        ssh.close()
        print("文件下载完成")
    except Exception as e:
        print(f"文件下载过程中出现错误: {e}")


if __name__ == "__main__":
    # 本地要上传的目录
    local_directory = '/Users/linghuchong/Downloads/51/Python/project/flask/flask_gw_i/po'

    # 服务器上的目标目录
    remote_directory = '/home/flask_gw_i/4447'

    # 服务器主机名或 IP 地址
    server_host = '192.168.0.243'

    # 服务器用户名
    server_user = 'root'

    # 服务器密码
    server_password = 'Benetech79$#-'


    # 上传功能
    # upload_directory(local_directory, remote_directory, server_host, server_user, server_password)

    # 下载整个目录功能
    # local_download_dir = '/Users/linghuchong/Downloads/123'
    # download_directory(remote_directory, local_download_dir, server_host, server_user, server_password)

    # 下载单个文件功能,如日志
    remote_file_path = '/root/cdrd/server/logs/server/error.log'
    local_file_path = '/Users/linghuchong/Downloads/123/4/error.log'
    download_file(remote_file_path, local_file_path, server_host, server_user, server_password)