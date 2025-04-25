# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: fastAPI
# https://www.bilibili.com/video/BV1Ya4y1D7et?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372&p=6
# web应用程序：遵循http协议
# *****************************************************************
import socket

# 服务端
sock = socket.socket()
sock.bind(("127.0.0.1", 8082))
sock.listen(5)
while 1:
    conn, addr = sock.accept()  # 阻塞等待客户段连接
    data = conn.recv(1024)
    print("客户端发送请求信息：\n",data)

    # conn.send(b"HTTP/1.1 200 OK\r\nserver:yuna\r\n\r\nhello world")
    # conn.send(b"HTTP/1.1 200 OK\r\ncontent-type:text/plain\r\n\r\n<h2>hello world</h2>")
    conn.send(b"HTTP/1.1 200 OK\r\ncontent-type:text/html\r\n\r\n<h2>johner</h2>")
    # conn.send(b'HTTP/1.1 200 OK\r\ncontent-type:application/json\r\n\r\n{"name":"john","pwd":"123"}')
    conn.close()



