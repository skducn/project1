import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii,random

# 16字节（128位）密钥，必须与Java端完全一致
HEX_KEY = "42656E65746563684031323334353637"
SECRET_KEY = binascii.unhexlify(HEX_KEY)


def encrypt_to_bytes(content: str) -> bytes:
    """
    使用AES-128/ECB/PKCS5Padding加密字符串，返回16字节密文
    """
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    encrypted_bytes = cipher.encrypt(pad(content.encode('utf-8'), AES.block_size))
    return encrypted_bytes


def encrypt_to_base64(content: str) -> str:
    """
    先加密为16字节，再进行Base64编码，得到24位结果
    """
    try:
        encrypted_bytes = encrypt_to_bytes(content)
        if len(encrypted_bytes) != 16:
            raise ValueError("加密结果长度不正确，应为16字节")
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    except Exception as e:
        raise e


def decrypt_from_base64(base64_content: str) -> str:
    """
    先Base64解码，再使用AES-128/ECB/PKCS5Padding解密字符串
    """
    try:
        # Base64解码
        encrypted_bytes = base64.b64decode(base64_content)
        if len(encrypted_bytes) != 16:
            raise ValueError("密文长度不正确，应为16字节")

        # 创建AES解密器
        cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
        # 解密并去除PKCS5填充
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        raise e

def generate_random_phone_numbers(count=150):
    phone_numbers = []
    for _ in range(count):
        # 中国大陆手机号通常以 1 开头，第二位通常是 3、4、5、7、8 中的一个数字
        prefix = random.choice(['13', '14', '15', '17', '18'])
        # 剩余的 9 位数字随机生成
        suffix = ''.join(random.choices('0123456789', k=9))
        phone_number = prefix + suffix
        phone_numbers.append(phone_number)
    return phone_numbers

def generate_random_chinese_names(count=150):
        # 常见的中文姓氏
        surnames = ['王', '李', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴',
                    '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗']

        # 常见的中文名字用字（单字）
        first_names = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '军',
                       '洋', '勇', '艳', '杰', '娟', '涛', '明', '超', '秀兰', '霞',
                       '平', '刚', '桂英', '辉', '丽华', '丹', '萍', '华', '红', '玉梅']

        names = []
        for _ in range(count):
            surname = random.choice(surnames)
            first_name = random.choice(first_names)
            full_name = surname + first_name
            names.append(full_name)

        return names



# 示例调用
if __name__ == "__main__":
    try:
        plaintext = "13816109050"
        # 加密
        base64_result = encrypt_to_base64(plaintext)
        print(f"加密结果: {base64_result}")  # Ku9FUmJrOqMBdy/+HjXxEA==
        print(f"结果长度: {len(base64_result)}")  # 24

        # 解密
        base64_result = "/BKMNHO1wc314cWZWbayYg=="
        decrypted_result = decrypt_from_base64(base64_result)
        print(f"解密结果: {decrypted_result}")  # 18521400797
    except Exception as e:
        print(f"操作失败: {e}")


    # 生成 100 个随机手机号
    random_phones = generate_random_phone_numbers(100)
    for phone in random_phones:
        result = encrypt_to_base64(phone)
        print(phone, result)

    print("~~~~~~~~~~~~~~~~~~~")

    # 生成 100 个随机中文姓名
    random_names = generate_random_chinese_names(100)
    for name in random_names:
        result = encrypt_to_base64(name)
        print(name, result)