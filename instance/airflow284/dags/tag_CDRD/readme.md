自动录制脚本：
playwright codegen http://192.168.0.243:8083/login?redirect=/index

# 检查DAG是否存在
airflow dags list | grep "cdrd_新增用户"

# 手动触发
airflow dags trigger cdrd_新增用户

# 查看触发结果
airflow dags list-runs -d cdrd_新增用户