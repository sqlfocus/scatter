#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scapy.all import *


def cons_UDP(dip):
    payload = "A"*250+"B"*500
    packet = IP(dst=dip, id=12345)/UDP(sport=1500, dport=1501)/payload
    frags = fragment(packet, fragsize = 500)

    for f in frags:
        send(f)
    
def main():
    cons_UDP("110.242.68.4")

if __name__ == "__main__":
    sys.exit(main())

