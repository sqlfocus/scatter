#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#for server
from gevent.server import DatagramServer

#for client
import multiprocessing
from gevent import socket
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
        #sleep, wait server start
        time.sleep(3)
        
        #send msg to server and receive
        cli_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cli_sock.sendto(msg.encode(encoding="utf-8"), (self._ip, self._port))
        print("client receive: ", cli_sock.recv(1024))
        cli_sock.close()


class EchoServer(DatagramServer):
    '''
    self.socket [gevent.socket] server socket
    self.address [tuple(string, int)] local address
    '''
    def handle(self, data, addr):
        '''
        param data [bytes array] data from client
        param addr [tuple] client address, (ip, port)
        '''
        print(self.address)
        print('{}: got {}'.format(addr[0], data))
        self.socket.sendto('Received {} bytes'.format(len(data)).encode('utf-8'), addr)

if __name__ == '__main__':
    #start client
    p = UDPClient(IP, PORT)
    p.daemon = True
    p.start()
    #p.join()

    EchoServer((IP, PORT)).serve_forever()

