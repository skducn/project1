
import time
from .celery import app

@app.task
def crawl_baidu():
    print("baidu")
    time.sleep(3)
    return "baidu爬取成功！"

@app.task
def crawl_jd(name='京东'):
    print("jd")
    time.sleep(3)
    return "jd爬取成功！" + str(name)