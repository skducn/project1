# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-4-17
# Description: # cryptography
# cryptography 是 Python 中一个功能强大的加密库，它提供了各种加密算法和工具，用于保障数据的安全性和完整性。
# 主要功能
# 对称加密：支持 AES、ChaCha20 等对称加密算法，用于对数据进行加密和解密。
# 非对称加密：提供 RSA、ECC 等非对称加密算法，可用于数字签名、密钥交换等。
# 哈希算法：实现了 SHA - 256、MD5 等哈希算法，用于生成数据的哈希值。
# *****************************************************************
from cryptography.fernet import Fernet

# 生成加密密钥
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# 要加密的数据(必须是字节)
message = b"Hello, cryptography!"

# 加密数据
encrypted_message = cipher_suite.encrypt(message)

# 解密数据
decrypted_message = cipher_suite.decrypt(encrypted_message)

print(f"Original message: {message}")
print(f"Encrypted message: {encrypted_message}")
print(f"Decrypted message: {decrypted_message}")


# 字符串如何转字节？