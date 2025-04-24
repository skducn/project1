
import time
from .celery import app

@app.task
def pay_order():
    print("开始下单")
    time.sleep(3)
    return "成功下单"

