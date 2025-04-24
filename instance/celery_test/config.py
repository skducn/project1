# config.py

# 文件名
filename = ['celeryPO.user_task', 'celeryPO.order_task',
    'celeryPO.crawl_task', 'celeryPO.add_task',
    'celeryPO.runStock', 'celeryPO.crawal_today_sh']

# 定时任务配置
beat_schedule = {
    'task1': {
        'task': 'celeryPO.runStock.run',
        'schedule': {'hour': 15, 'minute': 47},  # 指定时间为每天23点0分
        'args': ("4-22", "4-23")
    },
    'task2': {
        'task': 'celeryPO.crawal_today_sh.genData',
        'schedule': {'hour': 15, 'minute': 51},  # 指定时间为每天13点0分
        'args': ()
    },
    'task3': {
        'name': 'celeryPO.add_task',
        'task': 'celeryPO.add_task.add',
        'schedule': {'hour': 15, 'minute': 44},  # 指定时间为每天13点0分
        'args': (11, 44)
    }
}

