import pyodbc
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from PO.SqlserverPO import *
# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC_5G", "GBK")
# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_TEST", "GBK")
# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_PT", "GBK")
Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_PT", "UTF-8")


def aes_encrypt_with_hex_key(data, hex_key):
    """使用AES-128 ECB模式和十六进制密钥加密数据"""
    # 将十六进制密钥转换为字节
    key = bytes.fromhex(hex_key)

    if len(key) != 16:
        raise ValueError("AES-128需要16字节的密钥")

    # 将数据转换为字节
    data_bytes = data.encode('utf-8')

    # 初始化加密器
    cipher = AES.new(key, AES.MODE_ECB)

    # 对数据进行填充
    padded_data = pad(data_bytes, AES.block_size)

    # 加密
    encrypted_data = cipher.encrypt(padded_data)

    return encrypted_data



if __name__ == "__main__":
    # 待加密的数据
    data_to_encrypt = "这是需要加密并存储的数据"

    # 十六进制密钥
    hex_key = "42656E65746563684031323334353637"

    try:
        # 加密数据
        encrypted_bytes = aes_encrypt_with_hex_key(data_to_encrypt, hex_key)
        print(encrypted_bytes)
        print(f"加密后的二进制数据长度: {len(encrypted_bytes)} 字节")

        # 存入数据库
        # save_to_database(encrypted_bytes)

        sql = '''INSERT INTO CDRD_test(
                            name,
                            content
                        ) values(
                        %s, %s)'''

        params = (
            '你好',
            pyodbc.Binary(encrypted_bytes))

        Sqlserver_PO.execute2(sql, params)



    except Exception as e:
        print(f"处理失败: {str(e)}")
