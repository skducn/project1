# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
#  publicKey: 04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249
#  privateKey: 124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62
# *****************************************************************
# pip install selenium tensorflow numpy scikit-learn

# # 3. 数据准备
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
#
# # 4. 构建RNN模型
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense

import os
import paramiko


def upload_directory(local_dir, remote_dir, host, user, password):
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

# features = []
# labels = []
#
# for button in buttons:
#     text = button.text
#     size = button.size
#     location = button.location
#
#     # 将特征转换为数值
#     feature = [len(text), size['width'], size['height'], location['x'], location['y']]
#     features.append(feature)
#     labels.append('button')  # 假设所有提取的元素都是按钮
#
# # 关闭浏览器
# Web_PO.quit()
# //*[@id="app"]/div/div/div/div/div[4]/div[2]/form/div[7]/button
# /html/body/div[1]/div/div/div/div/div[2]/div[2]/form/div[4]/button
# /html/body/div[1]/div/div/div/div/div[3]/div[2]/form/div[4]/button
# /html/body/div[1]/div/div/div/div/div[4]/div[2]/form/div[7]/button


# /html/body/  div[1]/div/div/div/div/div[2]/div[2]/form/div[1]/div/div[1]/input
# id("app")/   DIV[1]/DIV[1]/DIV[1]/DIV[1]/DIV[2]/DIV[2]/FORM[1]/DIV[1]/DIV[1]/DIV[1]/INPUT[1]

# /html/body/  div[1]/div/div/div/div/div[2]/div[2]/form/div[2]/div/div[1]/input
# Button 2: XPath = id("app")/DIV[1]/DIV[1]/DIV[1]/DIV[1]/DIV[2]/DIV[2]/FORM[1]/DIV[2]/DIV[1]/DIV[1]/INPUT[1]

#
# # 将特征和标签转换为numpy数组
# features = np.array(features)
# labels = np.array(labels)

# /html/body/div[1]/div/div/div/div/div[2]/div[2]/form/div[4]/button


