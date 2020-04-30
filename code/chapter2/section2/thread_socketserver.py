# -*- coding:utf-8 -*-
###
# Author: Li Junjie
# Date: 2020-04-29 20:40:17
# LastEditors: Li Junjie
# LastEditTime: 2020-04-29 20:43:54
# FilePath: \django_enterprise_development_combat\code\chapter2\section2\thread_socketserver.py
###
# -*- coding:utf-8 -*-
###
# Author: Li Junjie
# Date: 2020-04-29 18:57:56
# LastEditors: Li Junjie
# LastEditTime: 2020-04-29 18:58:09
# FilePath: \django_enterprise_development_combat\code\chapter2\section2\thread_socketserver.py
###

import errno
import socket
import time
import threading

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
body = '''Hello world! <h1> form the5fire 《Django 企业开发实战》　</h1> - from
        {thread_name}'''
response_params = [
    'HTTP/1.0 200 OK', 
    'Date: Wed, 29 Apr 2020 09:12:50 GMT',
    'Content-Type: text/html; charset=utf-8',
    # 'Content-Type: text/plain; charset=utf-8',
    'Content-Length: {length}\r\n',
    body,
]
response = '\r\n'.join(response_params)


def handle_connection(conn, addr):
    print("oh, new conn", conn, addr)
    time.sleep(10)
    request = b""
    while EOL1 not in request and EOL2 not in request:
        try:
            request += conn.recv(1024)
        except:
            time.sleep(0.1)

    print(request)
    current_thread = threading.currentThread()
    content_length = len(body.format(thread_name=current_thread.name).encode())
    print(current_thread.name)
    conn.send(response.format(thread_name=current_thread.name, 
                length=content_length).encode())
    conn.close()


def main():
    # socket.AF_INET 用于服务器与服务器之间的网络通信
    # socket.SOCKET_STREAM 用于基于 TCP 的流式 socket 通信
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口可复用，保证每次 Ctrl+C 后可快速重启
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.setblocking(False)  # 设置为非阻塞，需要在 bind 和 listen 之前
    serversocket.bind(('0.0.0.0', 8000))
    serversocket.listen(10)  # 设置 backlog--socket 连接最大排队数量
    print('http://0.0.0.0:8000')

    try:
        i = 0
        while True:
            try:
                conn, address = serversocket.accept()
            # except socket.error as e:
            #     if e.args[0] != errno.EAGAIN:
            #         raise
            #     continue
            except BlockingIOError:
                continue
            i += 1
            print(i)
            t = threading.Thread(target=handle_connection, args=(conn, address), 
                                 name='thread - %s' % i)
            t.start()
    finally:
        serversocket.close()


if __name__ == "__main__":
    main()
