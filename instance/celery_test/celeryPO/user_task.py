
import time
from .celery import app

@app.task
def my_user():
    print("我是用户11")
    time.sleep(3)
    return "登录成功"


