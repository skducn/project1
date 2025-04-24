from celery import Celery
from celery.schedules import crontab
import config

# 消息中间件，使用redis 1库
broker = 'redis://localhost:6379/1'
# 结果存储，使用redis 2库
backend = 'redis://localhost:6379/2'

app = Celery('demo', broker=broker, backend=backend, include=config.filename)

# # 配置 Celery
# app.conf.update(
#     result_backend='redis://localhost:6379/1',
#     task_serializer='json',
#     result_serializer='json',
#     accept_content=['json'],
#     timezone='Asia/Shanghai',
#     enable_utc=True,
# )

# celery配置
# 制定了时区，中国时间，以后延迟任务，时间直接取 eta = datetime.now() + timedelta(seconds=5)
# 时区
app.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
app.conf.enable_utc = False


# todo 加入定时任务是配置
# # 动态加载 beat_schedule 配置
def create_crontab(schedule_dict):
    return crontab(**schedule_dict)

app.conf.beat_schedule = {
    task_name: {
        'task': task_config['task'],
        'schedule': create_crontab(task_config['schedule']),
        'args': task_config['args']
    }
    for task_name, task_config in config.beat_schedule.items()
}
