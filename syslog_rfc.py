#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import logging.handlers
import socket
import syslog

###pip3 install syslog-rfc5424-formatter
from syslog_rfc5424_formatter import RFC5424Formatter

log_5424 = logging.getLogger('rfc5424')
log_5424.setLevel(level=logging.DEBUG)

log_norm = logging.getLogger('normal')
log_norm.setLevel(level=logging.DEBUG)


def set_up_5424():
    h = logging.handlers.SysLogHandler(
        address=("127.0.0.1", 1378),  #default: '(localhost:514)'
        facility=syslog.LOG_USER,
        socktype=socket.SOCK_DGRAM)
    h.setFormatter(RFC5424Formatter())
    log_5424.addHandler(h)

def set_up_normal():
    h = logging.handlers.SysLogHandler(
        address=("127.0.0.1", 1378),
        facility=syslog.LOG_USER,
        socktype=socket.SOCK_DGRAM)
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%b %d %H:%M:%S')     #datefmt影响%(asctime)
    h.setFormatter(formatter)
    log_norm.addHandler(h)


if __name__ == "__main__":
    '''
    b'<71>1 2020-09-25T11:28:25.130133+08:00 B-44Z2MD6M-1937.local rfc5424 37517 - - hello, world\x00'
    '''    
    set_up_5424()
    log_5424.debug("hello, world")
    
    '''
    b'<71>Sep 25 11:39:51 - normal - DEBUG - hello, world\x00'
    '''
    set_up_normal()
    log_norm.debug("hello, world")



