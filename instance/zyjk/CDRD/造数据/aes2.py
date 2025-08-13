from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import binascii

from PO.SqlserverPO import *
# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC_5G", "GBK")
# Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_TEST", "GBK")
Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CDRD_PT", "GBK")


# 固定的十六进制密钥
HEX_KEY = "42656E65746563684031323334353637"
# 转换为字节密钥（全局唯一，避免重复转换）
KEY = binascii.unhexlify(HEX_KEY)


def aes_ecb_encrypt(plaintext):
    """
    使用固定密钥的AES-ECB模式加密数据
    :param plaintext: 明文数据（str类型或bytes类型）
    :return: 加密后的二进制数据（bytes类型）
    """
    # 处理输入：如果是字符串则转换为bytes
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    # 验证密钥长度（确保是16字节，AES-128）
    if len(KEY) != 16:
        raise ValueError(f"密钥长度错误，应为16字节，实际为{len(KEY)}字节")

    # 创建加密器
    cipher = Cipher(algorithms.AES(KEY), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # 数据填充（PKCS7）
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    # 执行加密并返回二进制数据
    return encryptor.update(padded_data) + encryptor.finalize()


# def aes_ecb_decrypt(ciphertext, encoding='utf-8'):
#     """
#     使用固定密钥的AES-ECB模式解密数据
#     :param ciphertext: 密文数据（bytes类型）
#     :return: 解密后的明文（str类型）
#     """
#     # 验证输入类型
#     if not isinstance(ciphertext, bytes):
#         raise TypeError("密文必须是bytes类型")
#
#     # 创建解密器
#     cipher = Cipher(algorithms.AES(KEY), modes.ECB(), backend=default_backend())
#     decryptor = cipher.decryptor()
#
#     # 执行解密
#     padded_data = decryptor.update(ciphertext) + decryptor.finalize()
#
#     # 去除填充
#     unpadder = padding.PKCS7(128).unpadder()
#     plaintext_bytes = unpadder.update(padded_data) + unpadder.finalize()
#
#     # 转换为字符串返回
#     return plaintext_bytes.decode('utf-8')

def aes_ecb_decrypt(ciphertext, encoding='utf-8'):
    """
    使用固定密钥的AES-ECB模式解密数据
    :param ciphertext: 密文数据（bytes类型）
    :param encoding: 解码格式，默认为utf-8
    :return: 解密后的明文（str类型）
    """
    # 验证输入类型
    if not isinstance(ciphertext, bytes):
        raise TypeError("密文必须是bytes类型")

    # 创建解密器
    cipher = Cipher(algorithms.AES(KEY), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    # 执行解密
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # 去除填充
    unpadder = padding.PKCS7(128).unpadder()
    plaintext_bytes = unpadder.update(padded_data) + unpadder.finalize()

    # 使用指定编码转换为字符串返回
    return plaintext_bytes.decode(encoding)

# 示例用法
if __name__ == "__main__":
    # 测试数据
    original_text = "这是加密后返回二进制数据的AES-ECB测试"
    print(f"原始文本: {original_text}")

    # 加密（返回二进制数据）
    encrypted_binary = aes_ecb_encrypt(original_text)
    print(encrypted_binary)
    print(f"加密后(二进制长度): {len(encrypted_binary)} 字节")
    print(f"加密后(十六进制表示): {binascii.hexlify(encrypted_binary).decode('utf-8')}")

    # 解密
    decrypted_text = aes_ecb_decrypt(encrypted_binary)
    print(f"解密后: {decrypted_text}")

    # 验证解密是否正确
    assert original_text == decrypted_text, "解密结果与原始文本不一致"
    print("验证成功: 解密结果与原始文本一致")

    sql = '''INSERT INTO CDRD_test(
                name,
                content
            ) values(
            %s, %s)'''

    params = (
        '你好',
        encrypted_binary)

    Sqlserver_PO.execute2(sql, params)
