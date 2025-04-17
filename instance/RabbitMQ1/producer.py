import pika

# 连接到 RabbitMQ 服务器
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 声明一个队列
channel.queue_declare(queue='hello')

# 发送消息到队列
message = 'Hello, RabbitMQ!'
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)
print(f" [x] Sent '{message}'")

# 关闭连接
connection.close()
    