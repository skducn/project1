# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
#  publicKey: 04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249
#  privateKey: 124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62
# *****************************************************************
import re
import random


def generate_all_cases(conditions, num_samples=1):
    """
    生成所有4种可能的条件组合情况

    参数:
    conditions (list): 条件列表，例如 ['BMI>=24', '年龄>=18', '年龄<65']
    num_samples (int): 每种情况生成的样本数量

    返回:
    dict: 包含4种情况的样本字典
    """
    # 分离BMI和年龄条件
    bmi_conditions = [c for c in conditions if c.startswith('BMI')]
    age_conditions = [c for c in conditions if c.startswith('年龄')]

    # 生成每种情况的样本
    return {
        "both_satisfied": [generate_sample(bmi_conditions, age_conditions, True, True) for _ in range(num_samples)],
        "bmi_satisfied_age_not": [generate_sample(bmi_conditions, age_conditions, True, False) for _ in
                                  range(num_samples)],
        "age_satisfied_bmi_not": [generate_sample(bmi_conditions, age_conditions, False, True) for _ in
                                  range(num_samples)],
        "both_not_satisfied": [generate_sample(bmi_conditions, age_conditions, False, False) for _ in
                               range(num_samples)]
    }


def generate_sample(bmi_conditions, age_conditions, satisfy_bmi, satisfy_age):
    """
    生成一个符合指定条件组合的样本

    参数:
    bmi_conditions (list): BMI相关条件
    age_conditions (list): 年龄相关条件
    satisfy_bmi (bool): 是否满足BMI条件
    satisfy_age (bool): 是否满足年龄条件

    返回:
    dict: 包含BMI和年龄的字典
    """
    # 生成BMI值
    if satisfy_bmi:
        bmi = generate_valid_bmi(bmi_conditions)
    else:
        bmi = generate_invalid_bmi(bmi_conditions)

    # 生成年龄值
    if satisfy_age:
        age = generate_valid_age(age_conditions)
    else:
        age = generate_invalid_age(age_conditions)

    # 返回字典格式
    return {'BMI': bmi, '年龄': age}


def generate_valid_bmi(conditions):
    """生成符合所有BMI条件的值"""
    bmi_min = 10.0
    bmi_max = 60.0

    for condition in conditions:
        match = re.match(r'BMI([<>=]+)(\d+)', condition)
        if not match:
            continue

        operator, value = match.groups()
        value = float(value)

        if operator == '>':
            bmi_min = max(bmi_min, value + 0.1)
        elif operator == '>=':
            bmi_min = max(bmi_min, value)
        elif operator == '<':
            bmi_max = min(bmi_max, value - 0.1)
        elif operator == '<=':
            bmi_max = min(bmi_max, value)

    return round(random.uniform(bmi_min, bmi_max), 1)


def generate_invalid_bmi(conditions):
    """生成不符合所有BMI条件的值"""
    if not conditions:
        return round(random.uniform(10.0, 60.0), 1)

    # 计算所有BMI条件的有效范围
    bmi_min = 10.0
    bmi_max = 60.0

    for condition in conditions:
        match = re.match(r'BMI([<>=]+)(\d+)', condition)
        if not match:
            continue

        operator, value = match.groups()
        value = float(value)

        if operator == '>':
            bmi_min = max(bmi_min, value + 0.1)
        elif operator == '>=':
            bmi_min = max(bmi_min, value)
        elif operator == '<':
            bmi_max = min(bmi_max, value - 0.1)
        elif operator == '<=':
            bmi_max = min(bmi_max, value)

    # 如果有效范围存在，生成范围外的值
    if bmi_min <= bmi_max:
        # 有效范围外有两个区间：[10.0, bmi_min) 和 (bmi_max, 60.0]
        if random.random() < 0.5:
            # 选择下界区间
            return round(random.uniform(10.0, bmi_min - 0.1), 1)
        else:
            # 选择上界区间
            return round(random.uniform(bmi_max + 0.1, 60.0), 1)
    else:
        # 条件矛盾，所有值都不符合条件
        return round(random.uniform(10.0, 60.0), 1)


def generate_valid_age(conditions):
    """生成符合所有年龄条件的值"""
    age_min = 0
    age_max = 120

    for condition in conditions:
        match = re.match(r'年龄([<>=]+)(\d+)', condition)
        if not match:
            continue

        operator, value = match.groups()
        value = float(value)

        if operator == '>':
            age_min = max(age_min, value + 1)
        elif operator == '>=':
            age_min = max(age_min, value)
        elif operator == '<':
            age_max = min(age_max, value - 1)
        elif operator == '<=':
            age_max = min(age_max, value)

    return random.randint(int(age_min), int(age_max))


def generate_invalid_age(conditions):
    """生成不符合所有年龄条件的值"""
    if not conditions:
        return random.randint(0, 120)

    # 计算所有年龄条件的有效范围
    age_min = 0
    age_max = 120

    for condition in conditions:
        match = re.match(r'年龄([<>=]+)(\d+)', condition)
        if not match:
            continue

        operator, value = match.groups()
        value = float(value)

        if operator == '>':
            age_min = max(age_min, value + 1)
        elif operator == '>=':
            age_min = max(age_min, value)
        elif operator == '<':
            age_max = min(age_max, value - 1)
        elif operator == '<=':
            age_max = min(age_max, value)

    # 如果有效范围存在，生成范围外的值
    if age_min <= age_max:
        # 有效范围外有两个区间：[0, age_min) 和 (age_max, 120]
        if random.random() < 0.5:
            # 选择下界区间
            return random.randint(0, int(age_min - 1))
        else:
            # 选择上界区间
            return random.randint(int(age_max + 1), 120)
    else:
        # 条件矛盾，所有值都不符合条件
        return random.randint(0, 120)


# 使用示例
if __name__ == "__main__":
    # 条件列表
    conditions = ['BMI>=24', '年龄>=18', '年龄<65']

    try:
        # 生成每种情况的样本
        cases = generate_all_cases(conditions)
        print(cases)

        # 打印结果
        for case_name, samples in cases.items():
            print(f"\n情况: {case_name}")
            for i, sample in enumerate(samples, 1):
                print(f"样本 {i}: {sample}")

    except ValueError as e:
        print(f"错误: {e}")


# def upload_directory(local_dir, remote_dir, host, user, password):
#     try:
#         # 创建 SSH 对象
#         ssh = paramiko.SSHClient()
#         # 允许连接不在 know_hosts 文件中的主机
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         # 连接服务器
#         ssh.connect(hostname=host, port=22, username=user, password=password)
#         # 创建 SFTP 对象
#         sftp = ssh.open_sftp()
#
#         def upload(local_path, remote_path):
#             if os.path.isfile(local_path):
#                 sftp.put(local_path, remote_path)
#                 # print(f"上传文件 {local_path} 到 {remote_path}")
#             elif os.path.isdir(local_path):
#                 try:
#                     sftp.stat(remote_path)
#                 except FileNotFoundError:
#                     sftp.mkdir(remote_path)
#                 for item in os.listdir(local_path):
#                     local_item_path = os.path.join(local_path, item)
#                     remote_item_path = os.path.join(remote_path, item)
#                     upload(local_item_path, remote_item_path)
#
#         upload(local_dir, remote_dir)
#
#         # 关闭连接
#         sftp.close()
#         ssh.close()
#         print("上传完成")
#     except Exception as e:
#         print(f"上传过程中出现错误: {e}")

#
# if __name__ == "__main__":
#     # 本地要上传的目录
#     local_directory = '/Users/linghuchong/Downloads/51/Python/project/flask/flask_gw_i/allureReport'
#     # 服务器上的目标目录
#     remote_directory = '/home/flask_gw_i/4446'
#     # 服务器主机名或 IP 地址
#     # 服务器主机名或 IP 地址
#     server_host = '192.168.0.243'
#     # 服务器用户名
#     server_user = 'root'
#     # 服务器密码
#     server_password = 'Benetech79$#-'
#
#     upload_directory(local_directory, remote_directory, server_host, server_user, server_password)
#
# # features = []
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


