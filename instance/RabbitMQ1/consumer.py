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

# 无密码
# 连接到 RabbitMQ 服务器
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()

# 有密码
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
channel = connection.channel()

varQueue = 'hello6'

# 声明一个队列
channel.queue_declare(queue=varQueue, durable=True)

# 定义一个回调函数来处理接收到的消息
def callback(ch, method, properties, body):
    print(f" [x] Received '{body.decode()}'")
    # int("213wqeqwe")

# # 多个消费者时，谁闲着谁先获取数据
# channel.basic_qos(prefetch_count=1)

# 告诉 RabbitMQ 这个回调函数将从队列中接收消息
channel.basic_consume(queue=varQueue,
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始消费消息
channel.start_consuming()
    