import time
from .celery import app

@app.task # 被装饰器才是celery的任务
def add(a,b):
    time.sleep(1)
    return a+b
