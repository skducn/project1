from celery import Celery
import time

# export PYTHONPATH=/Users/linghuchong/Downloads/51/Python/project/instance/celery_test/celeryPO

# 消息中间件，使用redis 1库
broker = 'redis://localhost:6379/1'
# 结果存储，使用redis 2库
backend = 'redis://localhost:6379/2'

app = Celery('demo', broker=broker, backend=backend,
             include=['celeryPO.user_task', 'celeryPO.order_task', 'celeryPO.crawl_task', 'celeryPO.add_task'])



# celery配置
# 制定了时区，中国时间，以后延迟任务，时间直接取 eta = datetime.now() + timedelta(seconds=5)
# 时区
app.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
app.conf.enable_utc = False


# todo 加入定时任务是配置
from datetime import timedelta
app.conf.beat_schedule = {
    'low-task':{
        'task': 'celeryPO.add_task.add',
        'schedule': timedelta(seconds=3),
        'args': (11, 22)
    }
}

# 启动beat，提交定时任务
# 每隔3秒，beat负责向broker提交一个任务，worker执行任务
# celery -A celeryPO beat -l debug

# beat每隔3s提交一个任务
# [2025-04-21 17:42:37,090: INFO/MainProcess] beat: Starting...
# [2025-04-21 17:42:40,108: INFO/MainProcess] Scheduler: Sending due task low-task (celeryPO.add_task.add)
# [2025-04-21 17:42:43,096: INFO/MainProcess] Scheduler: Sending due task low-task (celeryPO.add_task.add)
# [2025-04-21 17:42:46,096: INFO/MainProcess] Scheduler: Sending due task low-task (celeryPO.add_task.add)
# [2025-04-21 17:42:49,096: INFO/MainProcess] Scheduler: Sending due task low-task (celeryPO.add_task.add)

# worker每隔3s执行一次任务
# [2025-04-21 17:42:40,127: INFO/MainProcess] Task celeryPO.add_task.add[66bf1b13-32fd-4753-8c67-803b7326aa6b] received
# [2025-04-21 17:42:41,137: INFO/ForkPoolWorker-8] Task celeryPO.add_task.add[66bf1b13-32fd-4753-8c67-803b7326aa6b] succeeded in 1.0070511659978365s: 33
# [2025-04-21 17:42:43,099: INFO/MainProcess] Task celeryPO.add_task.add[34aa9dc0-695d-486f-a536-88758b750870] received
# [2025-04-21 17:42:44,103: INFO/ForkPoolWorker-8] Task celeryPO.add_task.add[34aa9dc0-695d-486f-a536-88758b750870] succeeded in 1.0025651290015958s: 33
# [2025-04-21 17:42:46,098: INFO/MainProcess] Task celeryPO.add_task.add[f3d322c8-e5b8-435a-bfe6-8bcbf37cdc30] received
# [2025-04-21 17:42:47,102: INFO/ForkPoolWorker-8] Task celeryPO.add_task.add[f3d322c8-e5b8-435a-bfe6-8bcbf37cdc30] succeeded in 1.0024925449979492s: 33
# [2025-04-21 17:42:49,098: INFO/MainProcess] Task celeryPO.add_task.add[b18b4483-e9f2-4837-8d8d-0246276e6e1b] received
# [2025-04-21 17:42:50,102: INFO/ForkPoolWorker-8] Task celeryPO.add_task.add[b18b4483-e9f2-4837-8d8d-0246276e6e1b] succeeded in 1.002945929998532s: 33
