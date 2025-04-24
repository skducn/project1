# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-4-18
# Description: # 延迟任务 apply_async()
# 视频：https://www.bilibili.com/video/BV1bvPXeeEqL?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372&p=10
# 步骤：
# 1, 启动worker监控，执行 celery -A celeryPO worker -l info
# 2, 运行 延迟任务.py 执行延迟5s任务
# 3，观察worker监控console，received后等了5s后执行 显示jd
# [2025-04-21 16:57:01,628: INFO/MainProcess] Connected to redis://localhost:6379/1
# [2025-04-21 16:57:01,637: INFO/MainProcess] mingle: searching for neighbors
# [2025-04-21 16:57:02,652: INFO/MainProcess] mingle: all alone
# [2025-04-21 16:57:02,675: INFO/MainProcess] celery@localhost-2.local ready.
# [2025-04-21 16:57:07,807: INFO/MainProcess] Task celeryPO.crawl_task.crawl_jd[2e7b09c1-b460-4d00-89be-3eee37d9800c] received
# [2025-04-21 16:57:12,672: WARNING/ForkPoolWorker-8] jd
# [2025-04-21 16:57:15,691: INFO/ForkPoolWorker-8] Task celeryPO.crawl_task.crawl_jd[2e7b09c1-b460-4d00-89be-3eee37d9800c] succeeded in 3.0191455649983254s: 'jd爬取成功！参数1'

# 问题：
# 如果延迟任务提交了，但worker没有启动，等了5s后，worker才启动，此时worker会立即执行。
# 一般情况，worker会一直运行，没有任务阻阻塞。worker是一个单独的进程，
# 如果只启动1个worker，同时有2个任务，这2个任务是串行执行。可以在多个机器上启动多个worker
# ***************************************************************u**
from celeryPO.crawl_task import crawl_jd
from datetime import datetime, timedelta

eta = datetime.utcnow() + timedelta(seconds=5)
res = crawl_jd.apply_async(args=['参数1'], eta=eta)
print(res)  # 2e7b09c1-b460-4d00-89be-3eee37d9800c

