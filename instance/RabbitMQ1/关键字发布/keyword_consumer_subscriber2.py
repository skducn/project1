# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-4-18
# Description: # 关键字发布，publish/Subscribe 发布者/订阅者
# 功能：发布者对所有订阅者发送消息
# 视频：https://www.bilibili.com/video/BV1hS4y1R7f2?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372&p=5
# 步骤：
# 1，执行 k_like_consumer_subscriber1.py  订阅者1
# 2，执行 k_like_consumer_subscriber2.py  订阅者2
# 3，执行 producer_publisher.py  发布者，发布消息后订阅1和订阅者2都收到消息（消费）

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

# 发布订阅模式fanout
# 1, 声明了一个exchange
# exchange ， 秘书的名称
# echange_type=fannou 秘书工作方式将消息发送给所有的队列
channel.exchange_declare(exchange='m2', exchange_type='direct')

# 2, 随机生成一个队列queue
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# 3, 让exchange和queue进行绑定
channel.queue_bind(exchange='m2', queue=queue_name, routing_key='sb')


# 定义一个回调函数来处理接收到的消息
def callback(ch, method, properties, body):
    print(f" [x] Received '{body.decode()}'")
    # int("213wqeqwe")
    # ch.basic_ack(delivery_tag=method.delivery_tag)


# # 多个消费者时，谁闲着谁先获取数据
# channel.basic_qos(prefetch_count=1)

# 4，告诉 RabbitMQ 这个回调函数将从队列中接收消息
channel.basic_consume(queue=queue_name,
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始消费消息
channel.start_consuming()
