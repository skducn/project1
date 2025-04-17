import pika
import sys

# 连接到 RabbitMQ 服务器
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 声明一个直连交换机
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# 获取路由键和消息
severity = sys.argv[1] if len(sys.argv) > 2 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

# 发送消息到交换机
channel.basic_publish(exchange='direct_logs',
                      routing_key=severity,
                      body=message)
print(f" [x] Sent '{severity}':'{message}'")

# 关闭连接
connection.close()
    