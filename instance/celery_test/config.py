# config.py

# 定时任务配置
beat_schedule = {
    'task1': {
        'task': 'celeryPO.runStock.run',
        'schedule': {'hour': 14, 'minute': 28},  # 指定时间为每天23点0分
        'args': ("4-22", "4-23")
    }
    # },
    # 'task2': {
    #     'task': 'celeryPO.add_task.add',
    #     'schedule': {'hour': 14, 'minute': 7},  # 指定时间为每天13点0分
    #     'args': (4, 55)
    # }
}
