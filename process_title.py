#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import Process
import os
import psutil         #pip3 install psutil
import setproctitle   #pip3 install setproctitle
import sys
import time

def task(name):
    time.sleep(3)
    
    print("subprocess name = : ", name)
    print(psutil.Process(os.getpid()).name())
    os.system("ps axu | grep -v grep | grep {}".format(name))
    print()
    print()

    setproctitle.setproctitle(name)
    print("after setproctitle: ", name)
    print(psutil.Process(os.getpid()).name())
    os.system("ps axu | grep -v grep | grep {}".format(name))
    
def main():
    #<NOTE>just work for 'ps aux | grep mdms';
    #      NOT by psutil.Process().name(), its just 'python'
    setproctitle.setproctitle("test-proc")
    print(psutil.Process(os.getpid()).name())
    os.system("ps axu | grep -v grep | grep test-proc")
    print()
    print()

    p = Process(target=task, args=("sub-process",), name="sub-process name")
    p.start()
    p.join()

if __name__ == "__main__":
    sys.exit(main())
