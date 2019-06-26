#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
import multiprocessing
import socket
import sys
import time

import tornado.ioloop
import tornado.web

IP = "127.0.0.1"
PORT = 8888

class PingHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("pong")
        
class VerHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("0.0.0")
        
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/ping", PingHandler),
            (r"/", VerHandler),
        ]
        settings = {
            "debug":True
        }
        tornado.web.Application.__init__(self, handlers, **settings)

        
class UDPClient(multiprocessing.Process):
    def __init__(self, ip, port):
        multiprocessing.Process.__init__(self)
        self._ip = ip
        self._port = port
    def run(self):
        time.sleep(3)         #sleep, wait server epoll start
        msg = "hello, world!" #msg send to server
        
        while True:
            time.sleep(1)
            cli_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            cli_sock.sendto(msg.encode(encoding="utf-8"), (self._ip, self._port))
            print("client receive: ", cli_sock.recv(1024))
            cli_sock.close()

def udp_echo(sock, fd, event):
    '''
    param sock [socket] udp服务socket，由functools.partial构造时传入
    param fd [int] udp服务socket的fd，即触发事件的fd
    param event [event] 服务事件

    <NOTE>functools.partial: 通过将一个函数的部分参数预先绑定为某些
          值，从而得到一个新的具有较少可变参数的函数
    '''
    data,addr = sock.recvfrom(1024)
    if not data:
        print("client close: ", addr)
        return
    print("receive [", data, "] from: ", addr)
    sock.sendto(data, addr)
        
def main():
    ###init http server
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(80)
    
    ###init udp server
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.setblocking(False)
    udp_sock.bind((IP, PORT))

    io_loop = tornado.ioloop.IOLoop.current()
    callback = functools.partial(udp_echo, udp_sock)
    io_loop.add_handler(udp_sock.fileno(), callback, io_loop.READ)

    ###start udp client
    p = UDPClient(IP, PORT)
    p.daemon = True
    p.start()
    #p.join()
    
    ###start ioloop
    io_loop.start()
    sys.exit("You really need exit???!!!")
    
if __name__ == "__main__":
    sys.exit(main())
