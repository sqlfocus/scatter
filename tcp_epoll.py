#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import multiprocessing
import select
import socket
import sys
import time

'''
USAGE: select.epoll() only supported by linux, NOT windows/mac os X, so
       run this example in linux environment
'''
IP = "127.0.0.1"
PORT = 8888

class TCPClient(multiprocessing.Process):
    def __init__(self, ip, port):
        multiprocessing.Process.__init__(self)
        self._ip = ip
        self._port = port
    def run(self):
        msg = "hello, world!"
        #sleep, wait server epoll start
        time.sleep(3)
        
        #send msg to server and receive
        cli_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        cli_sock.connect((self._ip, self._port))
        cli_sock.sendall(msg.encode(encoding="utf-8"))
        print("client receive: ", cli_sock.recv(1024))
        cli_sock.shutdown(socket.SHUT_RDWR)
        cli_sock.close()

def main():
    #init server socket
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv_sock.bind((IP, PORT))
    serv_sock.listen()
    serv_sock.setblocking(False)

    #init map: fd <-> socket
    msg = None
    fd_to_sock = {serv_sock.fileno():serv_sock,}

    #init epoll
    epoll = select.epoll()
    epoll.register(serv_sock.fileno(), select.EPOLLIN)

    #start client
    p = TCPClient(IP, PORT)
    p.daemon = True
    p.start()
    
    #server loop
    while True:
        #receive
        events = epoll.poll()
        if not events:
            print("Should NOT be here!!!")
            continue
        print("receive events: ", len(events))

        #dispose
        for fd, event in events:
            sock = fd_to_sock.get(fd)
            
            if sock == serv_sock:
                print("accept client")
                #receive new connection
                cli_sock,cli_addr = serv_sock.accept()
                cli_sock.setblocking(False)
                epoll.register(cli_sock.fileno(), select.EPOLLIN)
                fd_to_sock[cli_sock.fileno()] = cli_sock
            elif event & select.EPOLLIN:
                #receive data from client
                msg = sock.recv(1024)
                if len(msg) == 0: #client closed
                    print("client closed")
                    epoll.unregister(fd)
                    sock.shutdown(socket.SHUT_RDWR)
                    sock.close()
                    fd_to_sock.pop(fd)
                    continue
                epoll.modify(fd, select.EPOLLOUT)
                print("server receive: ", msg)
            elif event & select.EPOLLOUT:
                print("send to client: ", msg)
                #CAN send data to client
                epoll.modify(fd, select.EPOLLIN)
                sock.send(msg)
            else:
                print("some error")
                #client disconnect
                epoll.unregister(fd)
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
                fd_to_sock.pop(fd)
                
    #release    
    epoll.unregister(serv_sock.fileno())
    epoll.close()
    serv_sock.close()
    p.join()

if __name__ == "__main__":
    sys.exit(main())
