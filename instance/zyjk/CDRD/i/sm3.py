# -*- coding: utf-8 -*-
# *****************************************************************
# pip install pycryptodome
# pip install crypto


# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2025-8-6
# Description   : SM3 哈希算法实现
# *****************************************************************

try:
    from Crypto.Hash import SM3
    import binascii


    def sm3_encrypt(data):
        """
        使用SM3算法对数据进行哈希计算

        参数:
            data: 待哈希的数据，可以是字符串或字节流

        返回:
            哈希后的十六进制字符串
        """
        # 如果输入是字符串，转换为字节流
        if isinstance(data, str):
            data = data.encode('utf-8')

        # 创建SM3哈希对象
        sm3_hash = SM3.new()
        # 更新哈希对象
        sm3_hash.update(data)
        # 获取十六进制的哈希值
        return sm3_hash.hexdigest()

except ImportError:
    print("警告: 未安装 pycryptodome 库，使用备用实现")

    # 备用实现 - 如果没有 Crypto 库，提供简单的占位函数
    import hashlib


    def sm3_encrypt(data):
        """
        备用实现：使用SHA256模拟SM3功能（仅用于测试，非真正的SM3）

        参数:
            data: 待哈希的数据，可以是字符串或字节流

        返回:
            哈希后的十六进制字符串
        """
        # 如果输入是字符串，转换为字节流
        if isinstance(data, str):
            data = data.encode('utf-8')

        # 使用SHA256作为临时替代
        sha256_hash = hashlib.sha256()
        sha256_hash.update(data)
        return sha256_hash.hexdigest()

        print("警告: 使用SHA256代替SM3算法")

if __name__ == "__main__":
    # 测试数据
    test_data = "Jinhao123"
    print(f"原始数据: {test_data}")

    # 进行SM3哈希计算
    encrypted_data = sm3_encrypt(test_data)
    print(f"SM3哈希结果: {encrypted_data}")
    print(f"哈希长度: {len(encrypted_data)} 字符")

    # 测试字节流输入
    test_bytes = b"Test byte data"
    print(f"\n原始字节数据: {test_bytes}")
    encrypted_bytes = sm3_encrypt(test_bytes)
    print(f"SM3哈希结果: {encrypted_bytes}")
    print(f"哈希长度: {len(encrypted_bytes)} 字符")

    # 测试中文数据
    test_chinese = "测试中文数据"
    print(f"\n原始中文数据: {test_chinese}")
    encrypted_chinese = sm3_encrypt(test_chinese)
    print(f"SM3哈希结果: {encrypted_chinese}")
    print(f"哈希长度: {len(encrypted_chinese)} 字符")
