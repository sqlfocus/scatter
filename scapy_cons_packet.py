#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from scapy.compat import raw
from scapy.config import conf,lsc
from scapy.layers.http import HTTP,HTTPRequest
from scapy.layers.inet import IP,TCP
from scapy.layers.l2 import Ether
from scapy.main import load_layer
from scapy.packet import fuzz,ls
from scapy.sendrecv import send,sendp,sniff
from scapy.supersocket import StreamSocket
from scapy.utils import hexdump,rdpcap,wrpcap


'''
Scapy is a Python program that enables the user to send, 
sniff and dissect and forge network packets; This capability
allows construction of tools that can probe, scan or attack
networks

安装+使用
- pip3 install scapy          :: 安装scapy
- from scapy.all import *     :: 包含所有包
- ls(pkt)/pkt.show()          :: 罗列各层常用属性，如Ether/ARP/IP/UDP/TCP/ICMP/DNS/Dot1Q
- pkt.sprintf()               :: 格式化打印报文字段，如 “{IP:%IP.src% -> %IP.dst%\n}”
- raw(pkt)                    :: 将构建的packet转化为二进制字节串
- pkt.xxx=val                 :: 填充某个字段
- send(pkt)                   :: 3层发送, 自动管理路由、Mac
- sendp(pkt)                  :: 2层发送, 需要选择接口、二层协议
- sr/sr1/srp/srloop()         :: 发送报文并接收应答
- sniff/AsyncSniffer()        :: 监听报文
- fuzz(pkt)                   :: 随机更改指定报文部分
- lsc()                       :: 罗列scapy实现的内置高级命令


常见错误
- AttributeError: 'L2bpfSocket' object has no attribute 'ins'
   : 使用sudo权限启动scapy或脚本
- AttributeError: module 'scapy.layers' has no attribute 'http'
   : 默认不加载http层, 通过 'scapy.main.load_layer("http")' 手工加载
'''

def read_intf():
    sniff(iface="wifi0", prn=lambda x: x.summary())   ###tcpdump

def read_pcap():
    t = rdpcap("/path/to/xxx.pcap")  ###read
    wrpcap("temp.pcap", t)           ###save
    sendp(t)                         ###same to 'tcpreplay'
    
def cons_IP():
    print("in ", cons_IP.__name__, " #######")
    t_ip = IP(ttl=10)
    t_ip.src = "127.0.0.1"
    t_ip.dst = "192.168.1.1"
    ls(t_ip)
    print()
    print()

def cons_HTTP():
    print("in ", cons_HTTP.__name__, " #######")
    load_layer("http")
    req = HTTP()/HTTPRequest(
        Host=b'www.baidu.com',
        User_Agent=b'curl/7.64.1',
        Accept=b'*/*'
    )
    a = TCP_client.tcplink(HTTP, "www.baidu.com", 80)
    answser = a.sr1(req, retry=3, timeout=1)   ###maybe MISS response
    a.close()
    if answser is not None:
        print(answser.load)
    print()
    print()

def cons_HTTP_2():
    print("in ", cons_HTTP_2.__name__, " #######")
    import socket
    s = socket.socket()
    s.connect(("www.test.com",80))
    ss = StreamSocket(s, Raw)        ###recommend
    answser = ss.sr1(Raw("GET /\r\n"))
    print(answser.load)
    print()
    print()
    
def main():
    print(conf.route)                ###print/manage route
    #conf.route.delt(net="0.0.0.0/0", gw="192.168.8.1")
    #conf.route.add(net="0.0.0.0/0", gw="192.168.8.254")
    #conf.route.add(host="192.168.1.1", gw="192.168.8.1")
    #conf.route.resync()
    print()
    print()
    
    cons_IP()
    cons_HTTP()
    cons_HTTP_2()

if __name__ == "__main__":
    sys.exit(main())

