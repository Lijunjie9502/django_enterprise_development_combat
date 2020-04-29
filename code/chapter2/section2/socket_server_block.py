# -*- coding:utf-8 -*-
###
# Author: Li Junjie
# Date: 2020-04-29 18:37:43
# LastEditors: Li Junjie
# LastEditTime: 2020-04-29 18:38:34
# FilePath: \django_enterprise_development_combat\code\chapter2\section2\socket_server_block.py
###

import socket
import time

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
body = '''Hello world! <h1> form the5fire 《Django 企业开发实战》　</h1>'''
response_params = [
    'HTTP/1.0 200 OK', 
    'Date: Wed, 29 Apr 2020 09:12:50 GMT',
    'Content-Type: text/html; charset=utf-8',
    # 'Content-Type: text/plain; charset=utf-8',
    'Content-Length: {}\r\n'.format(len(body.encode())),
    body,
]
response = '\r\n'.join(response_params)


def handle_connection(coon, addr):
    print("oh, new coon", coon, addr)
    time.sleep(10)
    request = b""
    while EOL1 not in request and EOL2 not in request:
        request += coon.recv(1024)
    print(request)
    coon.send(response.encode())
    coon.close()


def main():
    # socket.AF_INET 用于服务器与服务器之间的网络通信
    # socket.SOCKET_STREAM 用于基于 TCP 的流式 socket 通信
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口可复用，保证每次 Ctrl+C 后可快速重启
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('127.0.0.1', 8000))
    serversocket.listen(5)  # 设置 backlog--socket 连接最大排队数量
    print('http://127.0.0.1:8000')

    try:
        while True:
            conn, address = serversocket.accept()
            handle_connection(conn, address)
    finally:
        serversocket.close()


if __name__ == "__main__":
    main()
