#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import psutil         #pip3 install psutil
import setproctitle   #pip3 install setproctitle
import sys
import time

def main():
    while True:
        time.sleep(1)
        print(psutil.Process(os.getpid()).name())
        print(os.system("ps axu | grep -v grep | grep test-proc"))
        
if __name__ == "__main__":
    #<NOTE>just work for 'ps aux | grep mdms';
    #      NOT by psutil.Process().name(), its just 'python'
    setproctitle.setproctitle("test-proc")
    sys.exit(main())
