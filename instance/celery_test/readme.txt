pip install eventlet
pip install celery,redis

2.4 Celery 架构
Celery 架构，它采用典型的生产者 - 消费者模式，主要由以下部分组成：
Producer：它负责把任务（发送短信任务，爬虫任务）提交得到 broker 中
celery Beat：会读取文件 --> 周期性的向 broker 中提交任务
broker：消息中间件，放任务的地方，celery 本身不提供，借助于 redis --> rabbitmq
worker：工人，消费者，负责从消息中间件中取出任务 --> 执行
backend：worker 执行完，会有结果，结果存储在 backend，celery 不提供 --> 借助于 redis