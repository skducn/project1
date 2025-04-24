# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-4-18
# Description: # 生产者和消费者，1对1，1对多
# 视频：https://www.bilibili.com/video/BV1hS4y1R7f2?spm_id_from=333.788.videopod.episodes&vd_source=be21f48b876460dfe25064d745fdc372&p=2

# brew services start rabbitmq
# http://localhost:15672/#/queues  guest，guest
# ***************************************************************u**
import pika

# # 连接到 RabbitMQ 服务器
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()

# 有密码
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
channel = connection.channel()

varQueue = 'hello6'

# 声明一个队列(支持队列持久化)
channel.queue_declare(queue=varQueue, durable=True)

# 发送消息到队列
message = 'Hello, RabbitMQ!'
channel.basic_publish(exchange='',
                      routing_key=varQueue,
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2)) # 数据持久化
print(f" [x] Sent '{message}'")

# 关闭连接
connection.close()
    