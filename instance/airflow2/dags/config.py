from cryptography.fernet import Fernet

# 生成密钥（仅需运行一次，保存好密钥文件）
key = Fernet.generate_key()
with open("/Users/linghuchong/Downloads/51/Python/project/instance/airflow/dags/secret.key", "wb") as key_file:
    key_file.write(key)

# 加密 API Key 并写入文件
api_key = "sk-f3e3d8f64cab416fb028d582533c1e01"
cipher_suite = Fernet(key)
encrypted_api_key = cipher_suite.encrypt(api_key.encode())

with open("/Users/linghuchong/Downloads/51/Python/project/instance/airflow/dags/encrypted_api_key.txt", "wb") as encrypted_file:
    encrypted_file.write(encrypted_api_key)
