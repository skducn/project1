# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-4-18
# Description: # 异步任务 函数.delay()
# 视频：https://www.bilibili.com/video/BV1bvPXeeEqL?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372&p=8
# 步骤：
# 1, 启动worker监控，执行 celery -A celeryPO worker -l info
# 2, 运行 异步任务.py
# 3，查看redis
# ***************************************************************u**
from celeryPO.add_task import add

# 提交异步任务，使用delay来提交任务（没有执行）
# 此语句向消息队列中提交一个任务（放在db1中，没有计算7+8），任务id = b378a64f-2604-405e-83bb-7a46f1c81c91
uuid = add.delay(7, 8)
print(uuid)  # b378a64f-2604-405e-83bb-7a46f1c81c91

# 3，redis中可以看到任务，没执行。

# 4，启动worker（后台一直监听，直到修改了add函数），执行被提交的任务，执行后将结果存入db2
# celery -A celery_demo worker -l info  //for mac
# celery -A celery_demo worker -l info -P eventlet   //for win

# 5，redis中查看任务被执行
