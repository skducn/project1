# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-8-6
# Description   : set 创建CDRD_PATIENT_INFO
# *********************************************************************

from PO.SqlserverPO import *
# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_TEST", "UTF-8")
Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_TEST", "GBK")

# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC_5G", "GBK")
# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC_5G", "GBK")

import random


# import pyodbc
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

from PO.DataPO import *
Data_PO = DataPO()

from PO.TimePO import *
Time_PO = TimePO()

# AES加密函数 (128位)
def aes_encrypt(plaintext, key):
    # ECB模式不需要IV
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # 填充和加密
    padding_length = 16 - (len(plaintext) % 16)
    plaintext += chr(padding_length).encode('GBK') * padding_length
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return ciphertext  # ECB模式不返回IV
# def aes_encrypt(plaintext, key):
#     # 生成16字节的随机初始化向量
#     iv = os.urandom(16)
#
#     # 创建AES加密器 (使用CBC模式)
#     # cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
#     cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
#     encryptor = cipher.encryptor()
#
#     # 填充数据以满足16字节的倍数
#     padding_length = 16 - (len(plaintext) % 16)
#     plaintext += chr(padding_length).encode('GBK') * padding_length
#     # plaintext += chr(padding_length).encode('utf-8') * padding_length
#
#     # 加密
#     ciphertext = encryptor.update(plaintext) + encryptor.finalize()
#
#     # 返回初始化向量+加密数据 (用于解密)
#     return iv + ciphertext

#
# # AES解密函数
# def aes_decrypt(ciphertext, key):
#     # 分离初始化向量和加密数据
#     iv = ciphertext[:16]
#     encrypted_data = ciphertext[16:]
#
#     # 创建AES解密器
#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
#     decryptor = cipher.decryptor()
#
#     # 解密
#     padded_plaintext = decryptor.update(encrypted_data) + decryptor.finalize()
#
#     # 移除填充
#     padding_length = padded_plaintext[-1]
#     plaintext = padded_plaintext[:-padding_length]
#
#     return plaintext.decode('GBK')  # 使用相应的编码解码
#
# # 使用示例（在Web应用中）
# # decrypted_name = aes_decrypt(patient_name_encrypted, aes_key)


# 将十六进制字符串密钥转换为字节
hex_key = '42656E65746563684031323334353637'
aes_key = bytes.fromhex(hex_key)

print(f"密钥长度: {len(aes_key)} 字节")  # 输出: 密钥长度: 16 字节
print(f"AES密钥 (Base64): {base64.b64encode(aes_key).decode('utf-8')}")

# 验证密钥长度
if len(aes_key) != 16:
    raise ValueError("AES-128密钥必须是16字节长度")


# sys.exit(0)

for _ in range(5):
    # 身份证，出生日期，年龄，性别
    d_gender = {'男': 0, '女': 1}
    idcard = Data_PO.getIdCard()
    t_birthday = Data_PO.getBirthday(idcard)
    birthday = t_birthday[0] + "-" + t_birthday[1] + "-" + t_birthday[2]
    age = Data_PO.getAge(idcard)
    sex = Data_PO.getSex(idcard)
    # 省份
    l_d_ = Sqlserver_PO.select("select * from SYS_PROVINCE_CITY")
    random_province_seq = random.randint(1, len(l_d_)-1)
    # print(l_d_[random_province_seq])
    # print(l_d_[random_province_seq]['PROVINCECODE'])
    # sys.exit(0)

    # 城市
    l_d_city = Sqlserver_PO.select("select * from SYS_PROVINCE_CITY_AREA where PROVINCECODE=%s" % (l_d_[random_province_seq]['PROVINCECODE']))
    random_city_seq = random.randint(1, len(l_d_city)-1)
    # print(l_d_city)
    # sys.exit(0)
    # 国籍
    l_d_nation = Sqlserver_PO.select(
        "select DICT_LABEL, DICT_VALUE from SYS_DICT_DATA where DICT_TYPE='sys_common_nation'")
    random_nation_seq = random.randint(1, 56-1)
    # 职业
    random_job = random.choice(["工程师", "服务人员", "技术人员", "老师", "军人", "学生"])
    # 婚姻
    l_d_marriage = Sqlserver_PO.select(
        "select DICT_LABEL, DICT_VALUE from SYS_DICT_DATA where DICT_TYPE='patient_marriage'")
    random_marriage_seq = random.randint(1, len(l_d_marriage)-1)
    # 身份
    l_d_id_type = Sqlserver_PO.select(
        "select DICT_LABEL, DICT_VALUE from SYS_DICT_DATA where DICT_TYPE='patient_id_type'")
    random_id_type_seq = random.randint(1, len(l_d_id_type)-1)
    # 随机关系人
    random_relation = random.choice(["同事", "子女", "代理人", "监护人", "其他", "父母", "祖父母", "兄弟姐妹"])

    # 加密
    # 姓名
    random_name = Data_PO.getChineseName()
    # data_to_encrypt = random_name.encode('utf-8')
    data_to_encrypt = random_name.encode('GBK')
    random_name_encrypted = aes_encrypt(data_to_encrypt, aes_key)
    # random_name_d = aes_decrypt(random_name_encrypted, aes_key)

    # 随机地址
    random_address = random.choice(["南京路100号", "中山路11号", "复兴路44号", "东方路10号", "七浦路89号", "鲁班路54号"])
    # data_to_encrypt = random_address.encode('utf-8')
    data_to_encrypt = random_address.encode('GBK')
    random_address_encrypted = aes_encrypt(data_to_encrypt, aes_key)
    # random_address_d = aes_decrypt(random_address_encrypted, aes_key)

    # 手机
    random_phone = Data_PO.getPhone()
    # data_to_encrypt = random_phone.encode('utf-8')
    data_to_encrypt = random_phone.encode('GBK')
    random_phone_encrypted = aes_encrypt(data_to_encrypt, aes_key)
    # random_phone_d = aes_decrypt(random_phone_encrypted, aes_key)

    # # 将二进制数据转换为十六进制字符串
    # random_phone_encrypted_hex = "0x" + random_phone_encrypted.hex()
    # random_address_encrypted_hex = "0x" + random_address_encrypted.hex()
    # random_name_encrypted_hex = "0x" + random_name_encrypted.hex()


    sql = f'''INSERT INTO CDRD_PATIENT_INFO(
            PATIENT_NAME,
            PATIENT_SEX_KEY,
            PATIENT_SEX_VALUE,
            PATIENT_BIRTH_DATE,
            PATIENT_AGE,
            PATIENT_BIRTH_ADDRESS_PROVINCE_KEY,
            PATIENT_BIRTH_ADDRESS_PROVINCE,
            PATIENT_BIRTH_ADDRESS_CITY_KEY,
            PATIENT_BIRTH_ADDRESS_CITY,
            PATIENT_BIRTH_ADDRESS_COUNTRY_KEY,
            PATIENT_BIRTH_ADDRESS_COUNTRY,
            PATIENT_COUNTRY,
            PATIENT_NATIVE_PROVINCE_KEY,
            PATIENT_NATIVE_PROVINCE,
            PATIENT_NATIVE_CITY_KEY,
            PATIENT_NATIVE_CITY,
            PATIENT_NATION_KEY,
            PATIENT_NATION_VALUE,
            PATIENT_PROFESSION,
            PATIENT_MARRIAGE_KEY,
            PATIENT_MARRIAGE_VALUE,
            PATIENT_ID_TYPE_KEY,
            PATIENT_ID_TYPE_VALUE,
            PATIENT_ACCOUNT_ADDRESS,
            PATIENT_CONTACT_RELATION,
            PATIENT_UPDATE_TIME,
            PATIENT_DATA_SOURCE_KEY,
            PATIENT_SOURCE_ID,
            PATIENT_PHONE_NUM,
            PATIENT_HOME_ADDRESS,
            PATIENT_ID_NUM,
            PATIENT_HOME_PHONE,
            PATIENT_CONTACT_PHONE,
            PATIENT_CONTACT_ADDRESS,
            PATIENT_CONTACT_NAME
        ) values(
        '{Data_PO.getChineseName()}',
        '{d_gender[sex]}',
        '{sex}',
        '{birthday}',
        '{age}',
        '{l_d_[random_province_seq]['PROVINCECODE']}',
        '{l_d_[random_province_seq]['NAME']}',
        '{l_d_city[random_city_seq]['CITYCODE']}',
        '{l_d_city[random_city_seq]['NAME']}',
        '{l_d_city[random_city_seq]['CODE']}',
        '{l_d_city[random_city_seq]['NAME']}',
        N'中国',
        '{l_d_[random_province_seq]['PROVINCECODE']}',
        '{l_d_[random_province_seq]['NAME']}',
        '{l_d_city[random_city_seq]['CITYCODE']}',
        '{l_d_city[random_city_seq]['NAME']}',
        '{l_d_nation[random_nation_seq]['DICT_VALUE']}',
        '{l_d_nation[random_nation_seq]['DICT_LABEL']}',
        '{random_job}',
        '{l_d_marriage[random_marriage_seq]['DICT_VALUE']}',
        '{l_d_marriage[random_marriage_seq]['DICT_LABEL']}',
        '{l_d_id_type[random_id_type_seq]['DICT_VALUE']}',
        '{l_d_id_type[random_id_type_seq]['DICT_LABEL']}',
        '{random_address}',
        '{random_relation}',
        '{Time_PO.getDateTimeByPeriod(0)}',
        '1',
        '',
        random_phone_encrypted,       
        random_address_encrypted,     
        idcard,                       
        random_phone_encrypted,       
        random_phone_encrypted,       
        random_address_encrypted,     
        random_name_encrypted         
    )'''

        # 插入加密后的数据到表中
    Sqlserver_PO.execute(sql)


# {random_phone_encrypted_hex},
# {random_address_encrypted_hex},
# '{idcard}',
# {random_phone_encrypted_hex},
# {random_phone_encrypted_hex},
# {random_address_encrypted_hex},
# {random_name_encrypted_hex}