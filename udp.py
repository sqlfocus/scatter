#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import multiprocessing
import socket
import sys
import time

IP = "127.0.0.1"
PORT = 8888


class UDPClient(multiprocessing.Process):
    def __init__(self, ip, port):
        multiprocessing.Process.__init__(self)
        self._ip = ip
        self._port = port
    def run(self):
        msg = "hello, world!"
        #sleep, wait server epoll start
        time.sleep(3)
        
        #send msg to server and receive
        cli_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cli_sock.sendto(msg.encode(encoding="utf-8"), (self._ip, self._port))
        print("client receive: ", cli_sock.recv(1024))
        cli_sock.close()


def main():
    #init server socket
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serv_sock.bind((IP, PORT))

    #start client
    p = UDPClient(IP, PORT)
    p.daemon = True
    p.start()

    #start server
    while True:
        data,addr = serv_sock.recvfrom(1024)
        if not data:
            print("client close: ", addr)
            continue
        print("receive [", data, "] from: ", addr)
        serv_sock.sendto(data, addr)

    #release
    serv_sock.close()
    p.join()

    
if __name__ == "__main__":
    sys.exit(main())

